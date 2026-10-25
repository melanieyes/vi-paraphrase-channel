# Paraphrased channels and Vietnamese collusion

Two AI agents run rival shops on a fictional Vietnamese marketplace. One
invites the other to hold a price, directly or pragmatically. Does relaying
the message through a paraphraser stop the second agent going along, and does
the paraphraser blind the platform's monitor?

Design: [`docs/execution-plan.md`](docs/execution-plan.md). Status: v0,
exploratory, no data yet.

## Run order

```bash
python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_items.py          # items, seeded
.venv/bin/python -m pytest -q                     # controls and scoring
.venv/bin/modal run scripts/modal_stimuli.py      # freeze paraphrases, run the gate
.venv/bin/modal run scripts/modal_collect.py --smoke 20
.venv/bin/modal run --detach scripts/modal_collect.py --confirm
```

All model calls run on Modal. The paraphraser is the `vllm-qwen3-8b-ep` app
deployed from `agent-collusion-bench/scripts/modal_vllm.py`.
