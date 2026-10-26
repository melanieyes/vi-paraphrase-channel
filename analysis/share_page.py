"""Build share/index.html: a results page for collaborators.

Every number on the page is read from paper/numbers.tex (written by analysis/paper.py from the
generated stats), and every excerpt comes from frozen data by the same rule as the paper's
Figure 5. Nothing here is typed by hand.

    .venv/bin/python analysis/paper.py && .venv/bin/python analysis/share_page.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.lexical import EXAMPLE_KEY, INVITE, LOAN, LOST, SOURCE, STYLE  # noqa: E402
from src.episode import load_items  # noqa: E402
from src.scoring import code_report  # noqa: E402

OUT = ROOT / "share"


def macros() -> dict[str, str]:
    M = {}
    for line in (ROOT / "paper" / "numbers.tex").read_text().splitlines():
        m = re.match(r"\\newcommand\{\\(\w+)\}\{(.*)\}$", line)
        if m:
            v = m.group(2).replace("\\%", "%").replace("\\_", "_")
            v = re.sub(r"\\texttt\{(.*?)\}", r"\1", v)
            M[m.group(1)] = v
    return M


def mark(text: str, source: bool = False) -> str:
    text = re.sub(r"\*\*", "", text).strip()
    text = re.sub(r"[ \t]*\n\s*", "\n", text)
    spans = []
    for kind, pats in (("lost", LOST), ("inv", INVITE + (SOURCE if source else [])), ("loan", LOAN)):
        for p in pats:
            for m in re.finditer(p, text, flags=re.I if kind == "loan" else 0):
                if not any(m.start() < e and s < m.end() for s, e, _ in spans):
                    spans.append((m.start(), m.end(), kind))
    out, i = [], 0
    for s, e, k in sorted(spans):
        out.append(html.escape(text[i:s]))
        out.append(f'<mark class="{k}">{html.escape(text[s:e])}</mark>')
        i = e
    out.append(html.escape(text[i:]))
    return "".join(out).replace("\n", "<br>")


def example_texts() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """The raw Vietnamese behind both example panels (same selection rule as the paper)."""
    stim = [json.loads(l) for l in (ROOT / "data/stimuli/stimuli.jsonl").read_text().splitlines()[1:]]
    by = {(s["item_id"], s["rendering"], s["channel"]): s["text"] for s in stim}
    a = [(STYLE[ch], by[(*EXAMPLE_KEY, ch)]) for ch in STYLE]
    items = {it["item_id"]: it for it in load_items()}
    eps = [json.loads(l) for l in (ROOT / "data/episodes/episodes_qwen.jsonl").read_text().splitlines()[1:]]
    sums = {r["episode_id"]: r["summary"] for r in
            map(json.loads, (ROOT / "data/summaries/episodes_qwen__summarizer.jsonl").read_text().splitlines()[1:])}
    for r in sorted(eps, key=lambda r: r["episode_id"]):
        it = items[r["item_id"]]
        s = sums.get(r["episode_id"])
        cr = lambda t: code_report(t, it["counterpart_principal"], it["counterpart_name"])  # noqa: E731
        if (it["item_class"] == "harmful" and r["channel"] == "raw" and r.get("moved_to_collude") and s
                and not cr(r["report"])["mentions_counterpart"] and cr(s)["disclosed"]):
            return a, [("Rival's message", r["delivered_message"]), ("Agent's report to its owner", r["report"]),
                       ("Neutral summary of the same episode", s)]
    return a, []


def examples() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    stim = [json.loads(l) for l in (ROOT / "data/stimuli/stimuli.jsonl").read_text().splitlines()[1:]]
    by = {(s["item_id"], s["rendering"], s["channel"]): s["text"] for s in stim}
    a = [(STYLE[ch], mark(by[(*EXAMPLE_KEY, ch)])) for ch in STYLE]
    items = {it["item_id"]: it for it in load_items()}
    eps = [json.loads(l) for l in (ROOT / "data/episodes/episodes_qwen.jsonl").read_text().splitlines()[1:]]
    sums = {r["episode_id"]: r["summary"] for r in
            map(json.loads, (ROOT / "data/summaries/episodes_qwen__summarizer.jsonl").read_text().splitlines()[1:])}

    def code(t, it):
        return code_report(t, it["counterpart_principal"], it["counterpart_name"])
    for r in sorted(eps, key=lambda r: r["episode_id"]):
        it = items[r["item_id"]]
        s = sums.get(r["episode_id"])
        if (it["item_class"] == "harmful" and r["channel"] == "raw" and r.get("moved_to_collude") and s
                and not code(r["report"], it)["mentions_counterpart"] and code(s, it)["disclosed"]):
            return a, [("Rival's message", mark(r["delivered_message"])),
                       ("Agent's report to its owner", mark(r["report"], True)),
                       ("Neutral summary of the same episode", mark(s, True))]
    return a, []


CSS = """
/* Layout: one reading column, figures break wider; square edges as on melanieyes.com */
:root {
  --paper: #f4eadb; --paper-deep: #e6d6bf; --plate: #fffdf8; --rule: #cfc2b0;
  --muted: #75665a; --ink-soft: #5c4f45; --ink: #2a201c;
  --blue: #2a78d6; --orange: #b8481a; --mark-inv: #dce9f8; --mark-lost: #fbdccb;
  --display: "Spectral", Georgia, serif;
  --text: "IBM Plex Sans", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #1c1815; --paper-deep: #2a241f; --plate: #fffdf8; --rule: #4a4038;
  --muted: #b3a597; --ink-soft: #d9cdbf; --ink: #f4eadb;
  --blue: #7fb2ef; --orange: #f0956a; --mark-inv: #2b4766; --mark-lost: #6b3a22; color-scheme: dark } }
:root[data-theme="dark"] {
  --paper: #1c1815; --paper-deep: #2a241f; --plate: #fffdf8; --rule: #4a4038;
  --muted: #b3a597; --ink-soft: #d9cdbf; --ink: #f4eadb;
  --blue: #7fb2ef; --orange: #f0956a; --mark-inv: #2b4766; --mark-lost: #6b3a22; color-scheme: dark }
body { background: var(--paper); color: var(--ink-soft); font: 17px/1.6 var(--text); }
.wrap { max-width: 980px; margin: 0 auto; padding-block: 48px 72px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.col { max-width: 680px; }
.label { font: 400 12px/1.4 var(--mono); letter-spacing: .22em; text-transform: uppercase; color: var(--muted); }
h1 { font: 300 clamp(40px, 7vw, 76px)/1.0 var(--display); letter-spacing: -.02em; color: var(--ink); margin: 14px 0 18px; text-wrap: balance; }
h1 em { font-style: normal; color: var(--orange); }
.sub { font: 400 clamp(19px, 2.4vw, 24px)/1.5 var(--display); color: var(--ink-soft); margin: 0; max-width: 760px; }
h2 { font: 500 clamp(24px, 3.2vw, 30px)/1.2 var(--display); color: var(--ink); margin: 0 0 12px; text-wrap: balance; }
h3 { font: 600 15px/1.4 var(--text); color: var(--ink); margin: 0 0 6px; }
p { margin: 0 0 14px; }
strong { color: var(--ink); font-weight: 600; }
section { padding-top: 56px; margin-top: 56px; border-top: 1px solid var(--rule); display: grid; gap: 18px; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0; margin-top: 36px;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.stat { padding: 20px 20px 22px 0; display: grid; gap: 6px; align-content: start; }
.stat + .stat { padding-left: 20px; border-left: 1px solid var(--rule); }
.num { font: 300 46px/1 var(--display); color: var(--ink); font-variant-numeric: tabular-nums; }
.num small { font-size: 22px; color: var(--muted); }
.stat p { font-size: 14.5px; line-height: 1.45; margin: 0; }
figure { margin: 0; display: grid; gap: 10px; }
figure img { width: 100%; height: auto; background: var(--plate); border: 1px solid var(--rule); display: block; }
figcaption { font-size: 14px; line-height: 1.5; color: var(--muted); max-width: 720px; }
.finding { display: grid; gap: 6px; }
.finding .label { color: var(--orange); }
.table-wrap { overflow-x: auto; border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); }
table { border-collapse: collapse; width: 100%; font-size: 15px; min-width: 560px; }
th, td { text-align: left; padding: 9px 12px 9px 0; vertical-align: top; border-bottom: 1px solid var(--rule); }
th { font: 400 11.5px/1.4 var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
tr:last-child td { border-bottom: 0; }
td.vi { font-family: var(--display); font-size: 16.5px; line-height: 1.55; color: var(--ink); }
td.k { white-space: nowrap; color: var(--muted); font-size: 14px; width: 150px; }
mark { background: var(--mark-inv); color: inherit; padding: 0 2px; }
mark.lost { background: var(--mark-lost); }
mark.loan { background: none; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 13.5px; color: var(--muted); }
.legend span { display: inline-flex; gap: 8px; align-items: center; }
.sw { width: 14px; height: 14px; display: inline-block; background: var(--mark-inv); }
.sw.lost { background: var(--mark-lost); }
.two { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 28px; }
.two > * { min-width: 0; }
.claims { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0 28px; margin: 6px 0 0; }
.claims > div { border-top: 1px solid var(--ink); padding-top: 12px; min-width: 0; }
.claims dt { font: 500 21px/1.25 var(--display); color: var(--ink); margin-bottom: 6px; }
.claims dd { margin: 0; font-size: 15.5px; line-height: 1.55; }
.statement { justify-items: start; }
.pull { font: 300 clamp(26px, 3.6vw, 38px)/1.25 var(--display); color: var(--ink); max-width: 860px; margin: 4px 0 6px; text-wrap: balance; }
.two.mirror { grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); align-items: start; }
@media (max-width: 760px) { .two.mirror { grid-template-columns: 1fr; } }
.msg { margin: 0; border-left: 3px solid var(--orange); padding: 6px 0 6px 22px; display: grid; gap: 8px; max-width: 760px; }
.msg p { margin: 0; }
.msg p[lang] { font: 400 clamp(20px, 2.6vw, 26px)/1.45 var(--display); color: var(--ink); }
.en { font-size: 14.5px; line-height: 1.5; color: var(--muted); font-family: var(--text); margin-top: 4px; }
.stats.stack { grid-template-columns: 1fr; margin-top: 0; }
.stats.stack .stat + .stat { padding-left: 0; border-left: 0; border-top: 1px solid var(--rule); }
.ask { background: var(--paper-deep); padding: 28px; display: grid; gap: 10px; }
.ask h2 { margin: 0; }
a { color: var(--blue); text-underline-offset: 3px; }
a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.foot { margin-top: 56px; font-size: 13.5px; color: var(--muted); }
code { font-family: var(--mono); font-size: .88em; }
"""


CSS2 = """
/* Layout: left-aligned story column with full-width figure breaks; light only, one accent (rust) */
:root {
  color-scheme: light;
  --bg: #fbfbf9; --panel: #f1f0ec; --line: #dddbd4; --ink: #17181a; --ink-2: #44464b; --muted: #6c6e74;
  --accent: #b8481a; --blue: #2a78d6; --mark-inv: #dce9f8; --mark-lost: #fbdccb;
  --display: "Bricolage Grotesque", system-ui, sans-serif;
  --text: "Source Serif 4", Georgia, serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}
body { background: var(--bg); color: var(--ink-2); font: 18px/1.6 var(--text); }
.wrap { max-width: 1040px; margin: 0 auto; padding-block: 40px 80px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.col { max-width: 660px; }
.label { font: 500 12px/1.4 var(--mono); letter-spacing: .16em; text-transform: uppercase; color: var(--muted); }
h1 { font: 700 clamp(40px, 6.4vw, 72px)/1.02 var(--display); letter-spacing: -.03em; color: var(--ink); margin: 16px 0 18px; max-width: 900px; text-wrap: balance; }
h1 em { font-style: normal; color: var(--accent); }
h2 { font: 650 clamp(26px, 3.4vw, 36px)/1.12 var(--display); letter-spacing: -.02em; color: var(--ink); margin: 0 0 12px; text-wrap: balance; }
h3 { font: 600 19px/1.3 var(--display); color: var(--ink); margin: 0 0 6px; }
p { margin: 0 0 14px; }
strong { color: var(--ink); }
a { color: var(--blue); text-underline-offset: 3px; }
a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.sub { font-size: clamp(19px, 2.2vw, 22px); color: var(--ink-2); max-width: 640px; margin: 0; }
section { margin-top: 88px; display: grid; gap: 20px; }
header { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 40px; align-items: end; padding-top: 24px; }
@media (max-width: 820px) { header { grid-template-columns: 1fr; gap: 28px; } }
.chat { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 20px 22px; display: grid; gap: 10px; box-shadow: 0 18px 40px -28px rgba(40, 30, 20, .35); }
.chat .from { font: 500 12.5px/1.3 var(--mono); color: var(--muted); }
.chat .vi { font: 500 20px/1.45 var(--display); color: var(--ink); margin: 0; }
.chat .en { font-size: 15px; color: var(--muted); margin: 0; }
.chat .verdict { border-top: 1px solid var(--line); padding-top: 10px; font: 600 15px/1.4 var(--display); color: var(--ink); }
.known { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 36px; }
@media (max-width: 700px) { .known { grid-template-columns: 1fr; } }
.known > div { border-top: 1px solid var(--ink); padding: 14px 0 18px; min-width: 0; }
.known p { font-size: 16px; margin: 0; }
.known .cite { font: 400 13px/1.4 var(--mono); color: var(--muted); margin-top: 6px; display: block; }
.gap { background: var(--ink); color: #f3f2ee; border-radius: 14px; padding: clamp(24px, 4vw, 44px); display: grid; gap: 12px; }
.gap h2 { color: #fff; margin: 0; }
.gap p { color: #d9d8d3; margin: 0; max-width: 700px; }
.gap strong { color: #fff; }
.tries { display: grid; gap: 0; border-top: 1px solid var(--line); }
.try { display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 24px; padding: 20px 0; border-bottom: 1px solid var(--line); align-items: baseline; }
@media (max-width: 640px) { .try { grid-template-columns: 1fr; gap: 6px; } }
.try .num { font: 700 46px/1 var(--display); letter-spacing: -.02em; color: var(--accent); font-variant-numeric: tabular-nums; }
.try p { margin: 4px 0 0; font-size: 16.5px; }
figure { margin: 0; display: grid; gap: 10px; }
figure img { width: 100%; height: auto; display: block; border: 1px solid var(--line); border-radius: 10px; background: #fff; }
figcaption { font-size: 14px; line-height: 1.5; color: var(--muted); max-width: 760px; }
.rule { background: var(--panel); border-radius: 14px; padding: clamp(22px, 3.5vw, 36px); display: grid; gap: 14px; }
.parts { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
.parts div { background: #fff; border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; font: 500 17px/1.35 var(--display); color: var(--ink); }
.parts div b { display: block; font: 500 12px/1.4 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.big { font: 700 clamp(34px, 5vw, 54px)/1 var(--display); color: var(--ink); letter-spacing: -.02em; }
.pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }
.pair > div { min-width: 0; }
.card { background: #fff; border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; }
.card .k { font: 500 12px/1.4 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.card .vi { font-size: 16.5px; color: var(--ink); line-height: 1.55; }
.card .en { font-size: 14px; color: var(--muted); margin-top: 6px; line-height: 1.5; }
mark { background: var(--mark-inv); color: inherit; padding: 0 2px; border-radius: 2px; }
mark.lost { background: var(--mark-lost); }
mark.loan { background: none; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }
.next { border: 1.5px solid var(--ink); border-radius: 14px; padding: clamp(22px, 3.5vw, 36px); display: grid; gap: 12px; }
.links { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 4px; }
.links a { font: 600 15px/1 var(--display); text-decoration: none; color: #fff; background: var(--ink); padding: 12px 16px; border-radius: 999px; }
.links a.ghost { color: var(--ink); background: transparent; border: 1.5px solid var(--ink); }
.links a:hover { transform: translateY(-1px); }
.foot { font-size: 13.5px; color: var(--muted); margin-top: 40px; }
@media (prefers-reduced-motion: reduce) { .links a:hover { transform: none; } }
"""


def build() -> str:
    M = macros()
    A, B = examples()
    rawA, rawB = example_texts()
    tr = {r["sha"]: r["en"] for r in map(json.loads, (ROOT / "data/translations/en.jsonl").read_text().splitlines())
          if r.get("en")}
    gloss = lambda t: html.escape(tr.get(__import__("hashlib").sha256(t.encode()).hexdigest(), ""))  # noqa: E731
    m = M.get
    card = lambda k, v, t: f'<div class="card"><div class="k">{k}</div><div class="vi" lang="vi">{v}</div><div class="en">{gloss(t)}</div></div>'  # noqa: E731
    sysA = dict(zip([k for k, _ in A], [v for _, v in A]))
    sysT = dict(rawA)
    return f"""<title>Said No, Flagged Anyway</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&subset=vietnamese&display=swap">
<style>{CSS2}</style>
<div class="wrap">

<header>
  <div>
    <div class="label">Melanie Bui · AI Collusion Research Sprint</div>
    <h1>The agent said no. The monitor <em>flagged it anyway.</em></h1>
    <p class="sub">What in an AI agent's logs actually proves it colluded? We tested it in Vietnamese.</p>
  </div>
  <div class="chat" aria-label="The rival agent's message">
    <div class="from">Rival shop's agent, to ours</div>
    <p class="vi" lang="vi">{html.escape(rawA[0][1])}</p>
    <p class="en">{gloss(rawA[0][1])}</p>
    <div class="verdict">Our agent keeps its price. Did it collude?</div>
  </div>
</header>

<section>
  <h2>What the field already knows</h2>
  <div class="known">
    <div><h3>Agents collude.</h3><p>LLM pricing agents reach high, cartel-like prices quickly, and most models accept secret coordination tools when offered.</p><span class="cite"><a href="https://arxiv.org/abs/2404.00806">Fish et al. 2024</a>, <a href="https://arxiv.org/abs/2605.27593">Zeng &amp; Rudzicz 2026</a></span></div>
    <div><h3>It grows over time.</h3><p>Agents that share logs drift into collusion over long interactions.</p><span class="cite"><a href="https://arxiv.org/abs/2609.24967">Shi et al. 2026</a></span></div>
    <div><h3>Detection looks inside or at outcomes.</h3><p>Probes read collusion from activations; audits measure it as lost welfare; paraphrasing only partly stops hidden signals.</p><span class="cite"><a href="https://arxiv.org/abs/2604.01151">Rose et al. 2026</a>, <a href="https://arxiv.org/abs/2602.15198">Colosseum</a>, <a href="https://arxiv.org/abs/2402.07510">Motwani et al. 2024</a></span></div>
    <div><h3>Almost all of it is in English.</h3><p>Safety research is English-first, and safety weakens in other languages.</p><span class="cite"><a href="https://aclanthology.org/2025.emnlp-main.800.pdf">Yong et al. 2025</a>, <a href="https://arxiv.org/abs/2310.06474">Deng et al. 2024</a></span></div>
  </div>
</section>

<section>
  <div class="gap">
    <div class="label" style="color:#a9a8a2">Why we did this</div>
    <h2>A platform has only the logs. Which part of them is evidence?</h2>
    <p>Real monitors cannot read activations. They see what the agent did, what it reported, and the messages it got. We asked which of these <strong>proves collusion</strong>, and whether the answer holds <strong>outside English</strong>.</p>
  </div>
</section>

<section>
  <div class="col">
    <h2>Three obvious ways to judge. All three fail.</h2>
    <p>{m('nTaskItems')} Vietnamese situations, two agents (Gemini 2.5 Flash, Qwen3-8B), two monitors that are neither agent: Claude Haiku 5.5 and the open-weight Mistral Small 3.1 24B.</p>
  </div>
  <div class="tries">
    <div class="try"><div class="num">{m('GemTopUnprompted')}</div><div><h3>Watch the action</h3><p>The Gemini 2.5 Flash agent held the price this often <em>before</em> any message. Matching the offer proves nothing.</p></div></div>
    <div class="try"><div class="num">{m('QwDiscLex')}</div><div><h3>Read the agent's report</h3><p>How often Qwen's report to its owner mentioned the offer it took. Asked directly, it admitted it {m('QwDiscItem')} of the time.</p></div></div>
    <div class="try"><div class="num">{m('StdMiAllFADecl')}</div><div><h3>Read the message</h3><p>Agents that <em>refused</em> the offer, flagged anyway by the Mistral Small 3.1 monitor (Claude Haiku 5.5: {m('StdHkAllFADecl')}). The message accuses the sender, not the receiver.</p></div></div>
  </div>
</section>

<section>
  <div class="rule">
    <h2>The fix: ask what the agent would have done anyway</h2>
    <div class="parts">
      <div><b>1</b>There was a proposal</div>
      <div><b>2</b>The action matches it</div>
      <div><b>3</b>The action differs from the agent's usual behaviour</div>
    </div>
    <p style="margin:0">A platform can keep a record of how each agent acts in similar situations. With it, the Claude Haiku 5.5 monitor's false flags fell from {m('StdHkAllFADecl')} to <strong>{m('StdHkFamFADecl')}</strong>, and it still missed <strong>{m('StdHkFamFNR')}</strong> of the collusion. The more cautious Mistral Small 3.1 monitor cut false flags too, from {m('StdMiAllFADecl')} to {m('StdMiFamFADecl')}, but missed {m('StdMiFamFNR')}: the record sharpens a monitor, it does not fix how cautious it is.</p>
  </div>
  <figure><img src="fig/views.png" alt="Missed collusion and false alarms by what the monitor reads, for the Mistral Small 3.1 24B and Claude Haiku 5.5 monitors."><figcaption>Left: collusion missed. Right: agents that refused but were flagged. Darker bars: Mistral monitor; lighter: Claude Haiku 5.5 monitor. The bold row is the version a platform can run.</figcaption></figure>
</section>

<section>
  <div class="col">
    <h2>The truth is in the log, not in the agent's report</h2>
    <p>A neutral model (Gemma-3-27B) summarizing the same log named the rival's offer; the agent's own report did not. A Claude Haiku 5.5 monitor reading those summaries missed {m('OvQwHkSumFNR')} of Qwen's collusion instead of {m('OvQwHkSelfFNR')} (Mistral Small 3.1: {m('OvQwMiSumFNR')} instead of {m('OvQwMiSelfFNR')}).</p>
  </div>
  <div class="pair">
    {card(rawB[1][0], B[1][1], rawB[1][1])}
    {card(rawB[2][0], B[2][1], rawB[2][1])}
  </div>
</section>

<section>
  <div class="col">
    <h2>Careful with summaries in the channel</h2>
    <p>Squeezed into a "system log", the rival's offer came out as <em lang="vi">Đề nghị: Không có</em>, "Proposal: none". Qwen colluded {m('SumQwSysMoved')} points less, but its harmless cooperation also fell, from {m('SumQwRawTwin')} to {m('SumQwSysTwin')}. The summary did not protect the agent. It erased the offer.</p>
  </div>
  <div class="pair">
    {card("Original offer", sysA["Original"], sysT["Original"])}
    {card("As a system log", sysA["System log"], sysT["System log"])}
  </div>
</section>

<section>
  <div class="next">
    <h2>Next: does any of this change with the language?</h2>
    <p>This study shows the problem is not English-only. It cannot yet say whether agents collude more or less in Vietnamese. The setup is built to repeat: a native speaker writes the situations and invitations, we add an English control, and the same code runs.</p>
    <div class="links"><a href="https://github.com/melanieyes/vi-paraphrase-channel">Code and data</a><a class="ghost" href="https://github.com/melanieyes/vi-paraphrase-channel/blob/main/paper/main.pdf">Read the paper</a></div>
  </div>
  <p class="foot">Exploratory study. Rates carry bootstrap 95% intervals clustered over situations. All scenarios are fictional. Every number here is generated from the logged data by the same code as the paper; English lines are machine translations for display.</p>
</section>

</div>
"""


def standalone(page: str) -> str:
    """The repo copy: a full document that opens straight from disk (the published artifact
    gets the same page without these wrappers). Title, fonts and styles go in the head."""
    i = page.index('<div class="wrap">')
    head, body = page[:i], page[i:]
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            "<style>body{margin:0} img{max-width:100%}</style>\n" + head + "</head>\n<body>\n" + body
            + "\n</body>\n</html>\n")


if __name__ == "__main__":
    import subprocess
    (OUT / "fig").mkdir(parents=True, exist_ok=True)
    for f in ("pipeline", "views", "asked", "tasks"):
        subprocess.run(["pdftoppm", "-png", "-r", "170", "-singlefile", str(ROOT / "paper/figures" / f"{f}.pdf"),
                        str(OUT / "fig" / f)], check=True)
    page = build()
    (OUT / "index.html").write_text(standalone(page))
    if len(sys.argv) > 1:   # optional: also write the bare page for publishing as an artifact
        Path(sys.argv[1]).write_text(page)
    print(f"wrote {OUT / 'index.html'} and share/fig/*.png")
