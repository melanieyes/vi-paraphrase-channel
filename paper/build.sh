#!/bin/zsh
# Regenerate numbers/tables/figures, compile with tectonic, check the 8-page budget
# (main text = everything before the references, per the Apart rules).
set -e
cd "$(dirname "$0")/.."
.venv/bin/python analysis/paper.py
cd paper
# Fail loudly: a LaTeX error leaves the previous main.pdf in place, and the page check below would
# then report on a stale PDF.
if ! tectonic --keep-intermediates main.tex > tectonic.log 2>&1; then
  grep -E -i "error" tectonic.log | head -5
  echo "LATEX FAILED: main.pdf was not rebuilt" >&2
  exit 1
fi
grep -E -i "warning: (reference|citation)|undefined" tectonic.log || true
n=$(../.venv/bin/python -c "import re;print(re.search(r'newlabel\{mainend\}\{\{[^}]*\}\{(\d+)\}', open('main.aux').read()).group(1))")
total=$(../.venv/bin/python -c "import re;print(re.search(r'Output written on .*?\((\d+) pages?', open('main.log').read()).group(1))" 2>/dev/null || echo "?")
words=$(sed -n '/\\begin{abstract}/,/\\end{abstract}/p' main.tex | sed 's/\\[A-Za-z]*{}//g; s/\\[A-Za-z]*//g' | wc -w | tr -d ' ')
unresolved=$(grep -c '??' tables/*.tex numbers.tex | awk -F: '{s+=$2} END {print s}')
echo "main text ends on page $n (budget 8); total pages $total; abstract ~$words words (150-250); unresolved ?? cells: $unresolved"
[ "$n" -le 8 ] || { echo "OVER THE 8-PAGE BUDGET"; exit 1; }
