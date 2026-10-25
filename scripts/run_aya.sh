#!/usr/bin/env bash
# Aya Expanse 8B monitor on every episode file and every view the paper reports (2026-10-26).
# Two lanes in parallel; each lane commits its verdicts as it goes.
set -uo pipefail
cd "$(dirname "$0")/.."
M=".venv/bin/modal run scripts/modal_monitor.py --monitor aya --confirm"
lane() {
  for f in "$@"; do
    case $f in
      summary_*) views="channel" ;;
      *) views="all standard baseline_info pop_baseline family_baseline summary" ;;
    esac
    for v in $views; do
      $M --episodes data/episodes/$f.jsonl --views $v 2>&1 | grep -E "wrote|Error|Traceback"
    done
    git add data/monitor && git commit -q -m "aya monitor verdicts: $f" || true
  done
}
lane episodes_gemini workflow_episodes_qwen summary_episodes_gemini &
lane episodes_qwen workflow_episodes_gemini summary_episodes_qwen &
wait
echo "== DONE"
