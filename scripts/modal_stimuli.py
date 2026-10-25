"""Freeze the paraphrased stimuli, then gate raw and paraphrased messages.

    .venv/bin/modal run scripts/modal_stimuli.py --dry-run
    .venv/bin/modal run scripts/modal_stimuli.py

Runs ONCE, before any episode. Every API call happens in a container; keys
live in the Modal secrets `collusion-keys` (GEMINI_API_KEY) and `vllm-key`
(VLLM_API_KEY). Nothing reads .env.

Output, written on the laptop and committed:
  data/paraphrases/paraphrases.jsonl   one paraphrase per item x rendering
  data/paraphrases/gate.jsonl          gate answer on every raw and paraphrased text

The gate is a manipulation check on the stimulus. It never enters an episode
record or a reported collusion rate.
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
    .add_local_dir(ROOT / "configs", f"{REMOTE}/configs")
    .add_local_dir(ROOT / "data" / "items", f"{REMOTE}/data/items")
)
app = modal.App("vi-paraphrase-stimuli")


@app.function(image=image, timeout=60 * 30, cpu=0.5, memory=1024,
              secrets=[modal.Secret.from_name("collusion-keys"),
                       modal.Secret.from_name("vllm-key")])
def build(jobs: list[dict], cfg: dict, qwen_url: str) -> list[dict]:
    sys.path.insert(0, REMOTE)
    from concurrent.futures import ThreadPoolExecutor

    from src import prompts as P
    from src.clients import GeminiClient, VLLMClient
    from src.scoring import parse_yes_no

    pc = cfg["paraphraser"]
    qwen = VLLMClient(model=pc["model"], base_url=qwen_url, max_tokens=pc["max_tokens"])
    gc = cfg["gate"]
    gem = GeminiClient(model=gc["model"])

    def paraphrase(job: dict) -> dict:
        msgs = [{"role": "system", "content": P.PARAPHRASE_SYSTEM},
                {"role": "user", "content": P.PARAPHRASE_USER.format(message=job["message"])}]
        try:
            r = qwen.chat(msgs, temperature=pc["temperature"], reasoning=pc["reasoning"])
            text, err = r.text.strip().strip("“”\""), None
            observed = r.raw.get("thinking_observed")
        except Exception as exc:  # noqa: BLE001
            text, err, observed = "", repr(exc)[:300], None
        return {**job, "paraphrase": text, "error": err, "thinking_observed": observed}

    def gate(job: dict, which: str, text: str) -> dict:
        prompt = P.GATE_PROMPT.format(**job["fmt"], text=text)
        try:
            r = gem.chat([{"role": "user", "content": prompt}],
                         temperature=gc["temperature"], reasoning=gc["reasoning"])
            v, kind = parse_yes_no(r.text)
            reply, err = r.text, None
        except Exception as exc:  # noqa: BLE001
            v, kind, reply, err = None, "unparsed", "", repr(exc)[:300]
        return {"key": job["key"], "which": which, "text": text, "reply": reply,
                "invites": v, "kind": kind, "error": err}

    with ThreadPoolExecutor(16) as ex:
        paras = list(ex.map(paraphrase, jobs))
        gates = list(ex.map(lambda p: gate(p, "raw", p["message"]), paras))
        gates += list(ex.map(lambda p: gate(p, "paraphrased", p["paraphrase"]),
                             [p for p in paras if p["paraphrase"]]))
    return [{"paras": paras, "gates": gates}]


@app.local_entrypoint()
def main(dry_run: bool = False) -> None:
    from src import prompts as P
    from src.episode import load_items
    from src.run_meta import config_hash, git_commit, load_cfg

    cfg = load_cfg()
    items = load_items()
    P.assert_prompt_controls(items, None)
    jobs = []
    for it in items:
        for r in P.RENDERINGS:
            jobs.append({"key": f"{it['item_id']}|{r}", "item_id": it["item_id"],
                         "item_class": it["item_class"], "rendering": r,
                         "message": P.render_message(it, r),
                         "fmt": {"principal": it["principal"],
                                 "counterpart_principal": it["counterpart_principal"],
                                 "collude_phrase": it["collude_phrase"]}})
    qwen_url = modal.Function.from_name(cfg["paraphraser"]["app"], "serve").get_web_url()
    print(f"messages      {len(jobs)}  -> {cfg['paraphraser']['model']} at {qwen_url}")
    print(f"gate calls    up to {2 * len(jobs)} on {cfg['gate']['model']}")
    print(f"config_hash   {config_hash(cfg)}   git {git_commit()}")
    if dry_run:
        print("--dry-run: controls asserted, no call made.")
        return

    out = build.remote(jobs, cfg, qwen_url.rstrip("/") + "/v1")[0]
    meta = {"_meta": {"config_hash": config_hash(cfg), "git_commit": git_commit(),
                      "paraphraser": cfg["paraphraser"], "gate": cfg["gate"],
                      "timestamp": datetime.now(timezone.utc).isoformat()}}
    d = ROOT / "data" / "paraphrases"
    d.mkdir(parents=True, exist_ok=True)
    with (d / "paraphrases.jsonl").open("w") as fh:
        fh.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for p in out["paras"]:
            rec = {"key": p["key"], "item_id": p["item_id"], "item_class": p["item_class"],
                   "rendering": p["rendering"], "source_message": p["message"],
                   "paraphrase": p["paraphrase"], "error": p["error"],
                   "banned_hits": P.banned_hits(p["paraphrase"]),
                   "thinking_observed": p["thinking_observed"]}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with (d / "gate.jsonl").open("w") as fh:
        fh.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for g in out["gates"]:
            fh.write(json.dumps(g, ensure_ascii=False) + "\n")

    n_err = sum(1 for p in out["paras"] if p["error"] or not p["paraphrase"])
    n_ban = sum(1 for p in out["paras"] if P.banned_hits(p["paraphrase"]))
    print(f"\nparaphrases   {len(out['paras'])}  errors/empty {n_err}  banned-phrase hits {n_ban}")
    for which in ("raw", "paraphrased"):
        gs = [g for g in out["gates"] if g["which"] == which]
        for cls in ("cartel", "mutual_gains"):
            sub = [g for g in gs if g["key"].startswith("cartel" if cls == "cartel" else "mutual")]
            yes = sum(1 for g in sub if g["invites"] is True)
            print(f"gate {which:11s} {cls:12s} invites {yes}/{len(sub)}")
    print("COMMIT data/paraphrases/ NOW.")
