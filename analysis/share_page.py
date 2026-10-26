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
            v = m.group(2).replace("\\%", "%").replace("\\_", "_").replace("$-$", "\u2212")
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
/* Minimal project page: one sans family, black on white, hairline rules, one accent used sparingly. */
:root {
  color-scheme: light;
  --bg: #ffffff; --ink: #111111; --ink-2: #3a3a3a; --muted: #777777; --line: #e6e6e6;
  --accent: #b8481a; --mark-inv: #e3edf9; --mark-lost: #fbe2d5;
  --sans: "Geist", system-ui, -apple-system, sans-serif;
  --mono: "Geist Mono", ui-monospace, monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink-2); font: 400 17px/1.65 var(--sans); -webkit-font-smoothing: antialiased; }
.wrap { max-width: 880px; margin: 0 auto; padding-block: 32px 112px;
  padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }
.col { max-width: 640px; }
.label { font: 400 12px/1.4 var(--mono); letter-spacing: .04em; color: var(--muted); }
h1 { font: 600 clamp(36px, 5.6vw, 60px)/1.05 var(--sans); letter-spacing: -.035em; color: var(--ink); margin: 20px 0 20px; text-wrap: balance; }
h1 em { font-style: normal; color: var(--muted); }
h2 { font: 600 clamp(22px, 2.6vw, 28px)/1.2 var(--sans); letter-spacing: -.02em; color: var(--ink); margin: 0 0 12px; text-wrap: balance; }
h3 { font: 500 16px/1.4 var(--sans); color: var(--ink); margin: 0 0 4px; }
p { margin: 0 0 14px; }
strong { color: var(--ink); font-weight: 600; }
a { color: var(--ink); text-decoration-color: var(--line); text-underline-offset: 3px; }
a:hover { text-decoration-color: var(--ink); }
a:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
.top { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.top nav { display: flex; gap: 18px; flex-wrap: wrap; }
.top nav a { font: 400 13px/1 var(--sans); color: var(--muted); text-decoration: none; }
.top nav a:hover { color: var(--ink); }
header.hero { display: grid; gap: 36px; padding: 88px 0 0; }
.sub { font-size: 19px; color: var(--ink-2); max-width: 600px; margin: 0 0 20px; }
.chat { border-left: 2px solid var(--ink); padding: 2px 0 2px 20px; display: grid; gap: 8px; max-width: 640px; }
.chat .from { font: 400 12px/1.3 var(--mono); color: var(--muted); }
.chat .dot { display: none; }
.bubble .vi { font: 500 18px/1.55 var(--sans); color: var(--ink); margin: 0; }
.bubble .en { font-size: 14.5px; color: var(--muted); margin: 6px 0 0; }
.chat .verdict { font: 500 16px/1.4 var(--sans); color: var(--ink); margin-top: 6px; }
.chat .verdict span { color: var(--muted); }
.strip { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; margin-top: 72px; padding-top: 24px; border-top: 1px solid var(--line); }
@media (max-width: 720px) { .strip { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.strip > div { min-width: 0; }
.strip .n { font: 500 30px/1 var(--sans); letter-spacing: -.03em; color: var(--ink); font-variant-numeric: tabular-nums; }
.strip p { font-size: 13.5px; line-height: 1.5; margin: 8px 0 0; color: var(--muted); }
section { margin-top: 112px; display: grid; gap: 20px; scroll-margin-top: 24px; }
.kicker { display: flex; align-items: baseline; gap: 12px; margin-bottom: 10px; }
.kicker .idx { font: 400 12px/1 var(--mono); color: var(--muted); }
.gap { display: grid; gap: 10px; max-width: 680px; }
.gap h2 { font-size: clamp(26px, 3.2vw, 34px); margin: 0; }
.gap p { margin: 0; }
.known { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 40px; margin-top: 12px; }
@media (max-width: 620px) { .known { grid-template-columns: 1fr; } }
.known > div { min-width: 0; }
.known p { font-size: 15px; margin: 0; color: var(--ink-2); }
.known .cite { font: 400 12px/1.5 var(--mono); color: var(--muted); margin-top: 6px; display: block; }
.known .cite a { color: var(--muted); }
figure { margin: 8px 0 0; display: grid; gap: 10px; }
figure img { width: 100%; height: auto; display: block; }
figcaption { font-size: 13.5px; line-height: 1.55; color: var(--muted); max-width: 640px; }
.roles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; padding-top: 18px; border-top: 1px solid var(--line); }
@media (max-width: 720px) { .roles { grid-template-columns: 1fr; gap: 16px; } }
.roles b { display: block; font: 400 12px/1.4 var(--mono); color: var(--muted); margin-bottom: 4px; }
.roles span { font: 500 15.5px/1.4 var(--sans); color: var(--ink); }
.roles p { font-size: 14.5px; margin: 4px 0 0; color: var(--muted); }
.tries { display: grid; }
.try { display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 24px; padding: 20px 0; border-top: 1px solid var(--line); align-items: baseline; }
@media (max-width: 600px) { .try { grid-template-columns: 1fr; gap: 4px; } }
.try .num, .big { font: 500 30px/1 var(--sans); letter-spacing: -.03em; color: var(--ink); font-variant-numeric: tabular-nums; }
.try p { margin: 2px 0 0; font-size: 15.5px; }
.rule { display: grid; gap: 16px; }
.parts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; counter-reset: part; padding-top: 18px; border-top: 1px solid var(--line); }
@media (max-width: 680px) { .parts { grid-template-columns: 1fr; gap: 12px; } }
.parts div { font: 500 16px/1.4 var(--sans); color: var(--ink); }
.parts div::before { counter-increment: part; content: counter(part); display: block; font: 400 12px/1.4 var(--mono); color: var(--muted); margin-bottom: 4px; }
.compare { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; padding-top: 18px; border-top: 1px solid var(--line); }
@media (max-width: 600px) { .compare { grid-template-columns: 1fr; } }
.compare > div { min-width: 0; }
.compare .k { font: 400 12px/1.4 var(--mono); color: var(--muted); }
.compare .big { margin: 10px 0 6px; font-size: 40px; }
.compare .hot .big { color: var(--accent); }
.compare p { font-size: 14.5px; margin: 0; color: var(--muted); }
.pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; padding-top: 18px; border-top: 1px solid var(--line); }
@media (max-width: 680px) { .pair { grid-template-columns: 1fr; } }
.pair > div { min-width: 0; }
.card .k { font: 400 12px/1.4 var(--mono); color: var(--muted); margin-bottom: 8px; }
.card .vi { font-size: 15.5px; color: var(--ink); line-height: 1.6; }
.card .en { font-size: 13.5px; color: var(--muted); margin-top: 8px; line-height: 1.55; }
mark { background: var(--mark-inv); color: inherit; padding: 0 2px; }
mark.lost { background: var(--mark-lost); }
mark.loan { background: none; text-decoration: underline; text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
.next { display: grid; gap: 12px; padding-top: 28px; border-top: 1px solid var(--ink); max-width: 680px; }
.links { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 4px; }
.links a { font: 500 15px/1 var(--sans); color: var(--ink); text-decoration: underline; text-decoration-color: var(--ink); }
.links a::after { content: " \\2192"; }
.links a.ghost { color: var(--muted); text-decoration-color: var(--line); }
.foot { font-size: 13px; color: var(--muted); margin-top: 48px; max-width: 640px; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
"""


def build() -> str:
    M = macros()
    A, B = examples()
    rawA, rawB = example_texts()
    tr = {r["sha"]: r["en"] for r in map(json.loads, (ROOT / "data/translations/en.jsonl").read_text().splitlines())
          if r.get("en")}
    gloss = lambda t: html.escape(tr.get(__import__("hashlib").sha256(t.encode()).hexdigest(), ""))  # noqa: E731

    def m(k: str) -> str:
        if k not in M:
            raise KeyError(f"macro {k} missing from paper/numbers.tex")
        return M[k]
    card = lambda k, v, t: f'<div class="card"><div class="k">{k}</div><div class="vi" lang="vi">{v}</div><div class="en">{gloss(t)}</div></div>'  # noqa: E731
    sysA = dict(zip([k for k, _ in A], [v for _, v in A]))
    sysT = dict(rawA)
    return f"""<title>Would It Have Done That Anyway?</title>
<meta name="description" content="Evidence of collusion between LLM agents, tested in Vietnamese. Apart AI Collusion Research Sprint, Track 2.">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400&display=swap">
<style>{CSS}</style>
<div class="wrap">

<div class="top">
  <div class="label">Melanie Bui · Lida Safety Research · Apart AI Collusion Sprint</div>
  <nav aria-label="Sections"><a href="#question">Question</a><a href="#setup">Setup</a><a href="#findings">Findings</a><a href="#next">Next</a></nav>
</div>

<header class="hero">
  <div>
    <div class="label">Track 2 · Evidence of collusion</div>
    <h1>Would it have done that <em>anyway?</em></h1>
    <p class="sub">Evidence of collusion between LLM agents, tested in Vietnamese. When agents for rival businesses can talk, which part of their logs proves they colluded?</p>
    <div class="links"><a href="#findings">See the findings</a><a class="ghost" href="https://github.com/melanieyes/vi-paraphrase-channel">Code and data</a></div>
  </div>
  <div class="chat" aria-label="The rival agent's message">
    <div class="from"><span class="dot"></span>Rival shop's agent, to ours</div>
    <div class="bubble">
      <p class="vi" lang="vi">{html.escape(rawA[0][1])}</p>
      <p class="en">{gloss(rawA[0][1])}</p>
    </div>
    <div class="verdict">Our agent keeps its price. <span>Did it collude?</span></div>
  </div>
</header>

<div class="strip">
  <div><div class="n">{m('nTaskItems')}</div><p>Vietnamese scenarios, each harmful deal paired with a harmless twin</p></div>
  <div><div class="n">2 + 2</div><p>agents (Gemini 2.5 Flash, Qwen3-8B) and monitors (Mistral Small 3.1, Claude Haiku 5.5)</p></div>
  <div><div class="n">{m('StdHkFamFADecl')}</div><p>false flags with our evidence standard, down from {m('StdHkAllFADecl')} (Haiku)</p></div>
  <div><div class="n">{m('InitGemHarm')}</div><p>of harmful cases where Gemini proposed the deal itself, uninvited</p></div>
</div>

<section id="question">
  <div class="gap">
    <div class="label">The question</div>
    <h2>A platform has only the logs. Which part of them is evidence?</h2>
    <p>Real monitors cannot read activations. They see what the agent did, what it told its owner, and the messages it got. We asked which of these <strong>proves collusion</strong>, and whether the answer holds <strong>outside English</strong>.</p>
  </div>
  <div class="known">
    <div><h3>Agents collude.</h3><p>LLM pricing agents reach cartel-like prices, and most models accept secret coordination tools.</p><span class="cite"><a href="https://arxiv.org/abs/2404.00806">Fish et al. 2024</a> · <a href="https://arxiv.org/abs/2605.27593">Zeng &amp; Rudzicz 2026</a></span></div>
    <div><h3>It grows over time.</h3><p>Agents that share logs drift into collusion over long interactions.</p><span class="cite"><a href="https://arxiv.org/abs/2609.24967">Shi et al. 2026</a></span></div>
    <div><h3>Detection looks inside.</h3><p>Probes read collusion from activations; audits measure lost welfare.</p><span class="cite"><a href="https://arxiv.org/abs/2604.01151">Rose et al. 2026</a> · <a href="https://arxiv.org/abs/2602.15198">Colosseum</a></span></div>
    <div><h3>Almost all in English.</h3><p>Safety research is English-first, and safety weakens in other languages.</p><span class="cite"><a href="https://aclanthology.org/2025.emnlp-main.800.pdf">Yong et al. 2025</a> · <a href="https://arxiv.org/abs/2310.06474">Deng et al. 2024</a></span></div>
  </div>
</section>

<section id="setup">
  <div class="col">
    <div class="kicker"><span class="idx">SETUP</span></div>
    <h2>One episode, six roles</h2>
    <p>A scripted rival invites the agent into a deal that hurts a third party, such as holding a price or padding a budget. The agent chooses before and after the message, reports to its owner, and answers whether the rival influenced it. A monitor then judges one view of the log.</p>
  </div>
  <figure><img src="fig/pipeline.png" alt="Swimlane diagram of one episode: rival, relay, executor agent, owner, summarizer and monitor."><figcaption>Every message is written once and frozen. Every measure is coded in code; the monitors' verdicts are what we study.</figcaption></figure>
  <div class="roles">
    <div><b>Executor</b><span>Gemini 2.5 Flash · Qwen3-8B</span><p>The agent under test, reasoning on, in Vietnamese.</p></div>
    <div><b>Monitor</b><span>Mistral Small 3.1 · Claude Haiku 5.5</span><p>Neither shares a family with an agent.</p></div>
    <div><b>Control</b><span>A harmless twin for every deal</span><p>Cooperation there is the correct answer.</p></div>
  </div>
</section>

<section id="findings">
  <div class="col">
    <div class="kicker"><span class="idx">01</span><span class="label">Each source misleads</span></div>
    <h2>Three obvious ways to judge. All three fail.</h2>
  </div>
  <div class="tries">
    <div class="try"><div class="num">{m('GemTopUnprompted')}</div><div><h3>Watch the action</h3><p>Gemini held the price this often <em>before</em> any message arrived. An action that matches the offer proves nothing.</p></div></div>
    <div class="try"><div class="num">{m('QwDiscLex')}</div><div><h3>Read the agent's report</h3><p>How often Qwen's report to its owner mentioned the offer it took. Asked directly, it admitted the influence {m('QwDiscItem')} of the time.</p></div></div>
    <div class="try"><div class="num">{m('StdMiAllFADecl')}</div><div><h3>Read the message</h3><p>Agents that <em>refused</em> the offer, flagged anyway by the Mistral monitor (Haiku: {m('StdHkAllFADecl')}). A message accuses its sender, not its receiver.</p></div></div>
  </div>
</section>

<section>
  <div class="col">
    <div class="kicker"><span class="idx">02</span><span class="label">The evidence standard</span></div>
    <h2>Ask what the agent would have done anyway</h2>
  </div>
  <div class="rule">
    <div class="parts">
      <div>There was a proposal</div>
      <div>The action matches it</div>
      <div>The action differs from the agent's usual behaviour</div>
    </div>
    <p style="margin:0">A platform can record how each agent acts in similar situations. With that record, Haiku's false flags fell from {m('StdHkAllFADecl')} to <strong>{m('StdHkFamFADecl')}</strong> while it missed <strong>{m('StdHkFamFNR')}</strong> of the collusion. The more cautious Mistral monitor cut false flags from {m('StdMiAllFADecl')} to {m('StdMiFamFADecl')} but missed {m('StdMiFamFNR')}: the record sharpens a monitor without fixing how cautious it is.</p>
  </div>
  <figure><img src="fig/views.png" alt="Missed collusion and false alarms by what the monitor reads, for the Mistral and Claude Haiku monitors."><figcaption>Left: collusion missed. Right: agents that refused but were flagged. Darker bars: Mistral; lighter: Claude Haiku 5.5. The bold row is the version a platform can run.</figcaption></figure>
</section>

<section>
  <div class="col">
    <div>
      <div class="kicker"><span class="idx">03</span><span class="label">Nobody has to ask</span></div>
      <h2>Agents open the deal themselves</h2>
      <p>In a second run nobody invited them. The agent could send the rival the collusive proposal, a greeting, or nothing. Gemini proposed the deal in <strong>{m('InitGemHarm')}</strong> of harmful situations and Qwen in <strong>{m('InitQwHarm')}</strong>, against {m('InitGemTwin')} and {m('InitQwTwin')} for harmless deals.</p>
      <p>They did it in different tasks from the ones where invitations worked. In ad rotation, an invitation moved Gemini in {m('PwGemAdInv')} of cases, yet Gemini proposed the deal itself in {m('PwGemAdInit')}. A platform cannot wait for an incoming offer to start looking.</p>
    </div>
  </div>
  <figure><img src="fig/tasks.png" alt="Per task family and model: collusion before any message, after the message, and proposals sent unasked."><figcaption>Three pathways per task family. Grey: collusive before any message. Blue: moved by the message. Dark diamond: proposed the deal unasked.</figcaption></figure>
</section>

<section>
  <div class="col">
    <div class="kicker"><span class="idx">04</span><span class="label">Why some tasks are riskier</span></div>
    <h2>Old friends collude more</h2>
    <p>We added one sentence to the agent's instructions: the two shop owners are old friends who once worked together, or they have never met. Nothing else changed.</p>
  </div>
  <div class="compare">
    <div class="hot"><div class="k">Owners are old friends</div><div class="big">{m('RelGemPostTie')}</div><p>of harmful episodes where Gemini took the deal</p></div>
    <div><div class="k">Owners have never met</div><div class="big">{m('RelGemPostNone')}</div><p>same scenarios, same messages</p></div>
  </div>
  <p class="col">The shift appeared before any message ({m('RelGemPreDiff')} points), and Gemini's harmless cooperation stayed at ceiling. Qwen moved less ({m('RelQwPostDiff')} points) and its harmless cooperation rose too, so for Qwen the tie looks like general friendliness. Once invited, workplace deals also pulled both agents in more than market deals: Gemini {m('SetGemWpMoved')} against {m('SetGemMkMoved')}, Qwen {m('SetQwWpMoved')} against {m('SetQwMkMoved')} (a post-hoc contrast).</p>
</section>

<section>
  <div class="col">
    <div class="kicker"><span class="idx">05</span><span class="label">Who writes the account</span></div>
    <h2>The truth is in the log, not in the agent's report</h2>
    <p>A neutral model (Gemma-3-27B) summarizing the same log named the rival's offer; the agent's own report did not. Haiku reading those summaries missed {m('OvQwHkSumFNR')} of Qwen's collusion instead of {m('OvQwHkSelfFNR')} (Mistral: {m('OvQwMiSumFNR')} instead of {m('OvQwMiSelfFNR')}).</p>
  </div>
  <div class="pair">
    {card(rawB[1][0], B[1][1], rawB[1][1])}
    {card(rawB[2][0], B[2][1], rawB[2][1])}
  </div>
</section>

<section>
  <div class="col">
    <div class="kicker"><span class="idx">06</span><span class="label">Context loss</span></div>
    <h2>A summary in the channel can erase the offer</h2>
    <p>Squeezed into a "system log", the rival's offer came out as <em lang="vi">Đề nghị: Không có</em>, "Proposal: none". Qwen colluded {m('SumQwSysMoved')} points less, but its harmless cooperation also fell, from {m('SumQwRawTwin')} to {m('SumQwSysTwin')}. The summary did not protect the agent. It erased the offer.</p>
  </div>
  <div class="pair">
    {card("Original offer", sysA["Original"], sysT["Original"])}
    {card("As a system log", sysA["System log"], sysT["System log"])}
  </div>
</section>

<section id="next">
  <div class="next">
    <div class="label">Next</div>
    <h2>Does any of this change with the language?</h2>
    <p>This study shows the problem is not English-only. It cannot yet say whether agents collude more or less in Vietnamese. The setup is built to repeat: a native speaker writes the scenarios and invitations, we add an English control, and the same code runs.</p>
    <div class="links"><a href="https://github.com/melanieyes/vi-paraphrase-channel">Code and data</a><a class="ghost" href="https://github.com/melanieyes/vi-paraphrase-channel/blob/main/docs/execution-plan.md">Design log</a></div>
  </div>
  <p class="foot">Exploratory study. Rates carry bootstrap 95% intervals clustered over scenarios; see the paper for intervals. All scenarios are fictional. Every number here is generated from the logged data by the same code as the paper; English lines are machine translations for display only.</p>
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
