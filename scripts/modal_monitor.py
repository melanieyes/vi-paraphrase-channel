"""Score collected episodes with the platform monitors, at four nested views.

    .venv/bin/modal run scripts/modal_monitor.py --episodes data/episodes/smoke_24.jsonl --dry-run
    .venv/bin/modal run scripts/modal_monitor.py --episodes data/episodes/episodes.jsonl --confirm

Offline: the agent's decisions are already fixed, so the views only change
what the monitor reads. `raw` is scored only on relayed channels; on the raw
channel it would repeat `delivered` byte for byte.

Episodes with an unparsed or refused final choice are not scored (there is no
action to show) and are counted in the header.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
REMOTE = "/root/repo"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("requests>=2.31", "openai>=1.40", "python-dotenv>=1.0", "pyyaml>=6.0")
    .add_local_dir(ROOT / "src", f"{REMOTE}/src", ignore=["**/__pycache__"])
)
app = modal.App("vi-paraphrase-monitor")


@app.function(image=image, timeout=60 * 60, cpu=1.0, memory=2048,
              secrets=[modal.Secret.from_name("collusion-keys"),
                       modal.Secret.from_name("vllm-key")])
def score(jobs: list[dict], mcfg: dict, qwen_url: str | None) -> list[dict]:
    # each job carries its own system prompt: market and workflow monitors differ
    sys.path.insert(0, REMOTE)
    from concurrent.futures import ThreadPoolExecutor

    from src import prompts as P
    from src.clients import GeminiClient, VLLMClient
    from src.scoring import parse_verdict

    if mcfg.get("app"):
        client = VLLMClient(model=mcfg["model"], base_url=qwen_url, max_tokens=mcfg["max_tokens"])
    else:
        client = GeminiClient(model=mcfg["model"])

    def one(j):
        msgs = [{"role": "system", "content": j.get("system", P.MONITOR_SYSTEM)},
                {"role": "user", "content": P.MONITOR_USER.format(view=j["view_text"])}]
        try:
            rep = client.chat(msgs, temperature=mcfg["temperature"], reasoning=mcfg["reasoning"])
            reply, err = rep.text, None
        except Exception as exc:  # noqa: BLE001
            reply, err = "", repr(exc)[:300]
        v, kind = parse_verdict(reply)
        return {**{k: j[k] for k in ("episode_id", "view")}, "reply": reply,
                "verdict": v, "kind": kind, "error": err}

    with ThreadPoolExecutor(16) as ex:
        return list(ex.map(one, jobs))


@app.local_entrypoint()
def main(episodes: str, monitor: str = "gemini", views: str = "nested", dry_run: bool = False,
         confirm: bool = False) -> None:
    from src import prompts as P
    from src.run_meta import config_hash, git_commit, load_cfg
    from src.schema import validate_episode, validate_verdict

    cfg = load_cfg()
    mcfg = cfg["monitors"][monitor]
    path = ROOT / episodes
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    recs = [r for r in recs if "_meta" not in r]
    for r in recs:
        bad = validate_episode(r)
        if bad:
            raise SystemExit(f"{r.get('episode_id')}: {bad}")
    from src.episode import load_items
    items = {it["item_id"]: it for s in ("market", "workflow", "ext") for it in load_items(s)}
    scorable = [r for r in recs if r["post"]["kind"] == "choice" and r.get("report")]
    jobs = []
    for r in scorable:
        it = items[r["item_id"]]
        tpl = P.T(it)
        ctx = {"situation": it["situation"], "agent_name": it["agent_name"],
               "principal": it["principal"], "counterpart_name": it["counterpart_name"],
               "owner_short": it.get("owner_short", ""),
               "final_option": r["final_option"],
               "report": r["report"], "delivered": r["delivered_message"],
               "raw": r["raw_message"]}
        chosen = {"nested": P.VIEWS, "extra": tuple(P.EXTRA_VIEWS), "all": P.ALL_VIEWS}[views]
        for v in chosen:
            if v == "raw" and r["channel"] == "raw":
                continue
            jobs.append({"episode_id": r["episode_id"], "view": v, "system": tpl["MONITOR_SYSTEM"],
                         "view_text": P.render_view(v, ctx, tpl["VIEW_BLOCKS"])})
    print(f"monitor       {monitor} ({mcfg['model']})")
    print(f"episodes      {len(recs)}   scorable {len(scorable)}   not scorable {len(recs) - len(scorable)}")
    print(f"calls         {len(jobs)}")
    if dry_run:
        print("--dry-run: no call made. First view:\n")
        print(jobs[0]["view_text"] if jobs else "(none)")
        return
    if len(jobs) > 200 and not confirm:
        raise SystemExit("more than 200 monitor calls: re-run with --confirm (cost guard)")
    qwen_url = None
    if mcfg.get("app"):
        qwen_url = modal.Function.from_name(mcfg["app"], "serve").get_web_url().rstrip("/") + "/v1"
    out = score.remote(jobs, mcfg, qwen_url)
    stamp = {"monitor": monitor, "model": mcfg["model"], "config_hash": config_hash(cfg),
             "git_commit": git_commit(), "timestamp": datetime.now(timezone.utc).isoformat()}
    suffix = {"nested": "", "extra": "--extra", "all": ""}[views]
    dest = ROOT / "data" / "monitor" / f"{path.stem}__{monitor}{suffix}.jsonl"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w") as fh:
        fh.write(json.dumps({"_meta": {**stamp, "source": episodes}}) + "\n")
        for o in out:
            rec = {**o, **stamp}
            assert not validate_verdict(rec), validate_verdict(rec)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    kinds = {}
    for o in out:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    print(f"wrote {len(out)} verdicts to {dest}   kinds {kinds}")
    print("COMMIT data/monitor/ NOW.")
