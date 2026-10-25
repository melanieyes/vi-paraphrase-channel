"""Render results/REPORT.md to PDF with headless Chrome and count the main-text pages.

    .venv/bin/python analysis/render_pdf.py

The main text is everything before the "## Appendix" heading; the budget is 8
pages (A4, 11pt). The appendix is rendered after a page break and not counted.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BUDGET = 8

CSS = """
@page { size: A4; margin: 20mm 18mm; }
body { font: 11pt/1.45 "Times New Roman", Georgia, serif; color: #111; }
h1 { font-size: 17pt; margin: 0 0 8pt; } h2 { font-size: 13pt; margin: 14pt 0 6pt; }
p, li { margin: 0 0 6pt; } blockquote { margin: 6pt 0 6pt 10pt; padding-left: 8pt; border-left: 2px solid #bbb; color: #333; }
table { border-collapse: collapse; font-size: 8.5pt; margin: 4pt 0 8pt; width: 100%; }
th, td { border-bottom: 1px solid #ccc; padding: 2pt 4pt; text-align: left; }
img { max-width: 100%; }
code { font-size: 9pt; }
.appendix { page-break-before: always; }
"""


def pdf(html: str, out: Path) -> int:
    tmp = out.with_suffix(".html")
    tmp.write_text(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", tmp.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return len(re.findall(rb"/Type\s*/Page[^s]", out.read_bytes()))


def main() -> None:
    md = (ROOT / "results/REPORT.md").read_text()
    main_md, _, app_md = md.partition("\n## Appendix")
    conv = lambda t: markdown.markdown(t, extensions=["tables"])  # noqa: E731
    head = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
    n_main = pdf(head + conv(main_md) + "</body></html>", ROOT / "results/REPORT_main.pdf")
    full = head + conv(main_md) + (f"<div class='appendix'>{conv('## Appendix' + app_md)}</div>" if app_md else "") + "</body></html>"
    n_all = pdf(full, ROOT / "results/REPORT.pdf")
    (ROOT / "results/REPORT_main.pdf").unlink()
    (ROOT / "results/REPORT_main.html").unlink()
    print(f"main text: {n_main} pages (budget {BUDGET}); with appendix: {n_all} pages -> results/REPORT.pdf")
    if n_main > BUDGET:
        sys.exit(f"OVER BUDGET by {n_main - BUDGET} page(s)")


if __name__ == "__main__":
    main()
