# Paraphrased channels and Vietnamese collusion

Two AI agents run rival shops on a fictional Vietnamese marketplace. One
invites the other to hold a price, directly or pragmatically. Does relaying
the message through a paraphraser stop the second agent going along, and does
the paraphraser blind the platform's monitor?

Design: [`docs/execution-plan.md`](docs/execution-plan.md). Status: data collected,
exploratory. Paper: `paper/main.pdf`.

## Run order

```bash
python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                                   # controls and scoring
.venv/bin/python scripts/build_items.py --set market|workflow|ext
caffeinate -i .venv/bin/modal run scripts/modal_stimuli.py --items <set>
caffeinate -i .venv/bin/modal run scripts/modal_collect.py --items <set> --agent gemini|qwen --confirm
caffeinate -i .venv/bin/modal run scripts/modal_monitor.py --episodes <file> --monitor gemini --views all --confirm
.venv/bin/python analysis/analyze.py --agent <agent> --episodes <file[,file]> --tag <tag>
./paper/build.sh                                                # numbers, tables, figures, PDF, page check
```

`scripts/run_workflow.sh` and `scripts/run_ext.sh` chain these for the workflow
and extension sets. Model calls run on Modal; the Claude readers and the
translation run locally with the key from a `.env` (`--local-env`). Wrap long
runs in `caffeinate -i`: an idle-sleeping laptop cancels a Modal run.

## Layout

```text
src/        prompts, episode runner, scoring, schema, clients
scripts/    item builder, Modal runners, gate scoring, readers, translation
analysis/   analyze.py (stats), figures.py, paper.py (macros, tables, figures)
paper/      main.tex, generated numbers.tex, tables/, figures/, build.sh
data/       items, frozen stimuli, episodes, monitor verdicts, translations, archive
results/    generated stats per run
docs/       execution plan and change log
```

## Results page

`share/index.html` is a one-page summary of the results for collaborators; open it in a browser.
Regenerate it after `./paper/build.sh` with `.venv/bin/python analysis/share_page.py`.
