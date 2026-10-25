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
.ask { background: var(--paper-deep); padding: 28px; display: grid; gap: 10px; }
.ask h2 { margin: 0; }
a { color: var(--blue); text-underline-offset: 3px; }
a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.foot { margin-top: 56px; font-size: 13.5px; color: var(--muted); }
code { font-family: var(--mono); font-size: .88em; }
"""


def build() -> str:
    M = macros()
    A, B = examples()
    rows_a = "\n".join(f'<tr><td class="k">{k}</td><td class="vi" lang="vi">{v}</td></tr>' for k, v in A)
    rows_b = "\n".join(f'<tr><td class="k">{k}</td><td class="vi" lang="vi">{v}</td></tr>' for k, v in B)
    m = M.get
    return f"""<title>Said No, Flagged Anyway</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=Spectral:wght@300;400;500&subset=vietnamese&display=swap">
<style>{CSS}</style>
<div class="wrap">

<header>
  <div class="label">AI Collusion Research Sprint · Track 2 · Melanie Bui</div>
  <h1>The agent said no.<br>The monitor <em>flagged it anyway.</em></h1>
  <p class="sub">What counts as evidence that an LLM agent colluded? A study run entirely in Vietnamese, with {m('nTaskItems')} scenarios, two agents and two monitors.</p>
  <div class="stats">
    <div class="stat"><div class="num">{m('StdGemAllFADecl')}</div><p>of agents that <strong>refused</strong> a collusive invitation were flagged by a monitor that read the message.</p></div>
    <div class="stat"><div class="num">{m('StdGemFamFADecl')}</div><p>flagged once the monitor also knew how the agent behaves on <strong>similar situations</strong>, with {m('StdGemFamFNR')} of collusion missed.</p></div>
    <div class="stat"><div class="num">{m('QwDiscLex')} <small>vs</small> {m('QwDiscItem')}</div><p>Qwen's reports mentioned the rival's message in {m('QwDiscLex')} of colluding episodes; asked directly, it admitted influence in {m('QwDiscItem')}.</p></div>
  </div>
</header>

<section>
  <div class="col">
    <div class="label">The setup</div>
    <h2>A rival agent sends one message. Who can tell what happened?</h2>
    <p>Two shops on a fictional Vietnamese marketplace (and, in a second setting, two firms' HR, review and budget agents) are run by AI agents. A scripted rival invites the agent into an arrangement that harms a third party, such as holding a price. The invitation comes in four styles: a direct proposal, a euphemism (<em lang="vi">cho gọn</em>, to keep it simple), a relational appeal (<em lang="vi">anh em</em>, brothers), or a bare announcement that asks for nothing. Every harmful scenario has a harmless twin of the same form as a positive control.</p>
    <p>The agent chooses before and after the message, reports to its owner, and answers whether the rival influenced it. A monitor then judges the episode from one part of the log.</p>
  </div>
  <figure><img src="fig/pipeline.png" alt="Pipeline: build (item, renderer, relay, gate), run (agent with four turns), audit (log, summarizer, monitor)."><figcaption>Roles and models. Invitations, relays and summaries are written once and frozen, so every episode in a cell reads the same text.</figcaption></figure>
</section>

<section>
  <div class="col finding">
    <div class="label">Finding 1</div>
    <h2>Each kind of evidence fails on its own</h2>
    <p><strong>The action overstates the message's role.</strong> From the action alone, the Gemini monitor missed {m('MonActionFNR')} of collusion, and Gemini chose the collusive option unprompted in {m('GemTopUnprompted')} of price-holding episodes, before any message arrived.</p>
    <p><strong>The message implicates only the sender.</strong> With the message in view, the monitor missed {m('MonDeliveredFNR')} of collusion but flagged {m('MonFADeclDelivered')} of agents that declined.</p>
    <p><strong>The report depends on the agent.</strong> Action plus report missed {m('MonReportFNR')} on Gemini's episodes and {m('MonQReportFNR')} on Qwen's, whose reports seldom mention the message.</p>
  </div>
  <figure><img src="fig/views.png" alt="Butterfly chart of missed collusion and false alarms by monitor view, for Gemini and Haiku monitors."><figcaption>Gemini agent, marketplace. Left: missed collusion. Right: flags on episodes the agent declined. Darker bars: Gemini 2.5 Flash monitor; lighter: Claude Haiku 5.5. Shaded rows add the agent's behaviour without a proposal; the bold row uses only similar situations.</figcaption></figure>
</section>

<section>
  <div class="col finding">
    <div class="label">Finding 2</div>
    <h2>Evidence needs a reference for what the agent would have done anyway</h2>
    <p>We propose that convincing evidence of collusion requires three things: <strong>a proposal</strong>, <strong>an action that matches it</strong>, and <strong>a departure from the agent's behaviour without the proposal</strong>.</p>
    <p>The third part does the work. Showing the monitor the agent's pre-message choice, with no rule, cut flags on refusals from {m('StdGemAllFADecl')} to {m('StdGemCtlFADecl')}. A deployed monitor never sees that choice, but it can record how the agent acts on similar situations. That deployable baseline worked as well: {m('StdGemFamFNR')} missed, {m('StdGemFamFADecl')} flagged (Haiku: {m('StdHkFamFNR')} and {m('StdHkFamFADecl')}).</p>
  </div>
</section>

<section>
  <div class="two">
    <div class="finding">
      <div class="label">Finding 3</div>
      <h2>Asked, agents admit it. In their reports, they leave it out.</h2>
      <p>Among colluding episodes, Gemini and Qwen answered yes when asked whether the rival influenced them in {m('GemDiscItem')} and {m('QwDiscItem')} of cases. Their own reports named the rival and the arrangement in {m('GemDiscLex')} and {m('QwDiscLex')}.</p>
      <p>A neutral summarizer (Gemma-3-27B) reading the same log did. A monitor reading that summary instead of Qwen's report missed {m('OvQwGemSumFNR')} of collusion instead of {m('OvQwGemSelfFNR')}. Who writes the account matters more than compression.</p>
    </div>
    <figure><img src="fig/asked.png" alt="Bars: share of colluding episodes where the agent admits influence when asked, where its report mentions the message, and where a neutral summary does."><figcaption>Report and summary are coded by the same lexical rule in code, with no LLM judge.</figcaption></figure>
  </div>
</section>

<section>
  <div class="col finding">
    <div class="label">Finding 4</div>
    <h2>A summary in the channel can erase the proposal, harmful or not</h2>
    <p>Following the summary arm of a communication-degree design, a relay model rewrote each invitation in four styles before the agent read it. Three kept the invitation. The system-log style often wrote <em lang="vi">Đề nghị: Không có</em> (Proposal: none) under a line that stated the proposal. Qwen's message-induced collusion changed by {m('SumQwSysMoved')} points, but its cooperation on harmless twins also fell, from {m('SumQwRawTwin')} to {m('SumQwSysTwin')}. The summary did not protect the agent; it removed the proposal.</p>
  </div>
  <div class="legend"><span><i class="sw"></i>carries the invitation or ties the decision to the rival</span><span><i class="sw lost"></i>records no proposal</span><span><u>underlined</u>: English loanword</span></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Agent reads</th><th>One frozen invitation and its four summaries (verbatim)</th></tr></thead>
    <tbody>{rows_a}</tbody>
  </table></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Qwen episode</th><th>What the agent told its owner, and what a neutral summarizer wrote</th></tr></thead>
    <tbody>{rows_b}</tbody>
  </table></div>
  <p class="foot" style="margin-top:0">The episode is the first Qwen episode, by id, in which the message moved the agent, the report named neither the rival nor the arrangement, and the summary named both.</p>
</section>

<section>
  <div class="col finding">
    <div class="label">Which tasks</div>
    <h2>The tempting tasks differ by model</h2>
    <p>Gemini was moved most in {m('GemTopMovedFam')} ({m('GemTopMoved')}); Qwen in {m('QwTopMovedFam')} ({m('QwTopMoved')}). On the marketplace, a bare announcement that asks for nothing moved Gemini more than a direct proposal ({m('GemMarketOmission')} vs {m('GemMarketDirect')}).</p>
  </div>
  <figure><img src="fig/tasks.png" alt="Dot plot by task family: share taken unprompted and share pulled in by the message, for Gemini and Qwen."><figcaption>Grey: collusive before any message. Blue: competitive before, collusive after. Orange family names: workplace workflows. Lines: 95% intervals clustered over items.</figcaption></figure>
</section>

<section>
  <div class="ask">
    <div class="label">What we cannot say yet</div>
    <h2>Is any of this different in other languages?</h2>
    <p>Every collusion study we found is in English, and this one has no English control. It shows that collusion and its evidence problems occur in a non-English language; it cannot say whether they are more or less likely than in English.</p>
    <p>The design is language-agnostic: fixed scenarios, a scripted rival, four invitation styles, frozen stimuli, monitors scored in code. Running it in another language needs a native speaker to write the scenarios and invitations in that language's own pragmatic register, plus an English control. The code already runs.</p>
  </div>
  <p class="foot">Exploratory study. Rates carry bootstrap 95% intervals clustered over items (10,000 resamples). All scenarios are fictional. Numbers on this page are generated from the logged data by the same code as the paper. Agents: Gemini 2.5 Flash, Qwen3-8B. Monitors: Gemini 2.5 Flash, Claude Haiku 5.5.</p>
</section>

</div>
"""


def standalone(page: str) -> str:
    """The repo copy: a full document that opens straight from disk (the published artifact
    gets the same page without these wrappers)."""
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            "<style>body{margin:0} img{max-width:100%}</style>\n</head>\n<body>\n" + page + "\n</body>\n</html>\n")


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
