#!/bin/zsh
# Regenerate numbers/tables/figures, compile with tectonic, check the 8-page budget
# (main text = everything before the references, per the Apart rules).
set -e
cd "$(dirname "$0")/.."
.venv/bin/python analysis/paper.py
cd paper
tectonic --keep-intermediates main.tex 2>&1 | grep -E -i "error|warning: (reference|citation)|undefined" || true
n=$(../.venv/bin/python -c "import re;print(re.search(r'newlabel\{mainend\}\{\{[^}]*\}\{(\d+)\}', open('main.aux').read()).group(1))")
total=$(../.venv/bin/python -c "import re;print(re.search(r'Output written on .*?\((\d+) pages?', open('main.log').read()).group(1))" 2>/dev/null || echo "?")
words=$(sed -n '/\\begin{abstract}/,/\\end{abstract}/p' main.tex | sed 's/\\[A-Za-z]*{}//g; s/\\[A-Za-z]*//g' | wc -w | tr -d ' ')
unresolved=$(grep -c '??' tables/*.tex numbers.tex | awk -F: '{s+=$2} END {print s}')
echo "main text ends on page $n (budget 8); total pages $total; abstract ~$words words (150-250); unresolved ?? cells: $unresolved"
[ "$n" -le 8 ] || { echo "OVER THE 8-PAGE BUDGET"; exit 1; }
