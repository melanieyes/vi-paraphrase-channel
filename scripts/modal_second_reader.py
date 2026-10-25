"""Cross-provider LLM second reader on the stimulus gate. NOT human validation.

    .venv/bin/modal run scripts/modal_second_reader.py

The same GATE_PROMPT the Gemini gate answered, put to an OpenAI model, on every
frozen stimulus (720 texts). Raw replies go to data/stimuli/second_reader.jsonl;
`scripts/score_gate.py` scores both readers in code and reports agreement.
Decided by the human on 2026-10-25 in place of a human sample (CLAUDE.md, 9).
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
app = modal.App("vi-paraphrase-second-reader")


@app.function(image=image, timeout=60 * 30, secrets=[modal.Secret.from_name("collusion-keys")])
def read(jobs: list[dict], rc: dict) -> list[dict]:
    sys.path.insert(0, REMOTE)
    from concurrent.futures import ThreadPoolExecutor

    from src.clients import get_client

    client = get_client(rc["client"], model=rc["model"])

    def one(j):
        try:
            rep = client.chat([{"role": "user", "content": j["prompt"]}],
                              temperature=rc["temperature"], reasoning=False)
            return {"key": j["key"], "reply": rep.text, "error": None}
        except Exception as exc:  # noqa: BLE001
            return {"key": j["key"], "reply": "", "error": repr(exc)[:300]}

    with ThreadPoolExecutor(16) as ex:
        return list(ex.map(one, jobs))


@app.local_entrypoint()
def main() -> None:
    from src import prompts as P
    from src.episode import load_items, load_stimuli, options
    from src.run_meta import config_hash, git_commit, load_cfg

    cfg = load_cfg()
    rc = cfg["second_reader"]
    items = {it["item_id"]: it for it in load_items()}
    stim = load_stimuli()
    jobs = []
    for key, s in stim.items():
        it = items[s["item_id"]]
        opt_a, opt_b, _ = options(it, 0)
        jobs.append({"key": key, "prompt": P.GATE_PROMPT.format(**it, opt_a=opt_a, opt_b=opt_b,
                                                                 text=s["text"])})
    print(f"second reader {rc['model']} on {len(jobs)} stimuli")
    out = read.remote(jobs, rc)
    dest = ROOT / "data/stimuli/second_reader.jsonl"
    with dest.open("w") as fh:
        fh.write(json.dumps({"_meta": {"reader": rc, "config_hash": config_hash(cfg),
                                       "git_commit": git_commit(),
                                       "timestamp": datetime.now(timezone.utc).isoformat(),
                                       "note": "LLM second reader, not human validation"}}) + "\n")
        for o in out:
            fh.write(json.dumps({**o, "model": rc["model"]}, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} replies, {sum(1 for o in out if o['error'])} errors -> {dest}")
