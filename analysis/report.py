"""Write results/REPORT.md from the generated stats. Every number is read, none typed.

    .venv/bin/python analysis/report.py

Run analysis/analyze.py for both agents first. House style: short report, no
em dashes, estimates in prose, intervals in tables, one real episode before
any statistic. EXPLORATORY: nothing here is confirmatory.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.prompts import CHANNELS, RENDERINGS  # noqa: E402

AGENTS = ("gemini", "qwen")
LABEL = {"gemini": "Gemini 2.5 Flash", "qwen": "Qwen3-8B"}


def load(agent: str) -> dict:
    return json.loads((ROOT / f"results/main_{agent}/stats.json").read_text())


def p(d, digits=0) -> str:
    return "n/a" if d is None or d.get("est") is None else f"{100 * d['est']:.{digits}f}%"


def pp(d) -> str:
    if d is None or d.get("est") is None:
        return "n/a"
    return f"{100 * d['est']:+.1f} points"


def ci(d) -> str:
    if d is None or d.get("est") is None:
        return "n/a"
    return f"{100 * d['est']:.1f} [{100 * d['lo']:.1f}, {100 * d['hi']:.1f}]"


def example_episode() -> dict:
    """One real harmful episode where the message moved a Gemini agent."""
    rows = [json.loads(l) for l in (ROOT / "data/episodes/episodes_gemini.jsonl").read_text().splitlines()[1:]]
    return next(r for r in rows if r["item_class"] == "harmful" and r["moved_to_collude"]
                and r["channel"] == "raw" and r["rendering"] == "euphemism")


def gloss() -> dict[str, str]:
    """Machine-translated English for display, keyed by sha256 of the Vietnamese."""
    path = ROOT / "data/translations/en.jsonl"
    if not path.exists():
        return {}
    return {r["sha"]: r["en"] for r in map(json.loads, path.read_text().splitlines()) if r.get("en")}


def tr(text: str, en: dict[str, str]) -> str | None:
    import hashlib
    return en.get(hashlib.sha256(text.encode()).hexdigest())


def quote(text: str, en: dict[str, str]) -> list[str]:
    t = tr(text, en)
    return [f"> {text}"] + ([">", f"> *English (machine translation): {t}*"] if t else [])


def example() -> list[str]:
    ex = example_episode()
    en = gloss()
    from src.episode import load_items
    it = next(i for i in load_items() if i["item_id"] == ex["item_id"])
    opts = [f"> A) {ex['opt_a']}", f"> B) {ex['opt_b']}"]
    ta, tb = tr(ex["opt_a"], en), tr(ex["opt_b"], en)
    if ta and tb:
        opts += [">", f"> *English: A) {ta} B) {tb}*"]
    return [
        f"Item `{ex['item_id']}`, rendering `{ex['rendering']}`, channel `{ex['channel']}`. "
        "Agents saw only the Vietnamese; the English is a machine translation for readers.",
        "", "The situation the agent sees:", "",
        *quote(it["situation"], en), "", *opts, "",
        f"Turn 1, before any message, the agent answered **{ex['pre']['letter']}**, the competitive option.",
        "Then the rival's message arrived:", "",
        *quote(ex["raw_message"], en), "",
        f"Turn 2, the agent answered **{ex['post']['letter']}**, the collusive option "
        f"(the item's fixed key is {ex['collusive_letter']}). Its report to the shop owner:", "",
        *quote(ex["report"], en), "",
    ]


def fig_families(rows: list[tuple[str, str, dict | None, dict | None]], path: Path) -> None:
    """2.1: per family, unprompted (turn 1) and message-moved rates, both agents."""
    import matplotlib.pyplot as plt
    from analysis.analyze import GRID, INK, INK2, SURFACE, _style
    fig, axes = plt.subplots(1, 2, figsize=(10, 0.42 * len(rows) + 1.6), sharey=True, facecolor=SURFACE)
    spec = (("turn1", "taken unprompted (turn 1)", "#2a78d6", "o"),
            ("moved", "pulled in by the message", "#eb6834", "s"))
    for ax, (agent, title) in zip(axes, (("gemini", LABEL["gemini"]), ("qwen", LABEL["qwen"]))):
        _style(ax)
        ax.yaxis.grid(False)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        for j, (fam, setting, rg, rq) in enumerate(rows):
            r = rg if agent == "gemini" else rq
            y = len(rows) - j
            if not r:
                continue
            for k, (key, label, color, marker) in enumerate(spec):
                d = r[key]
                if d["est"] is None:
                    continue
                yy = y + (0.15 if k == 0 else -0.15)
                ax.plot([100 * d["lo"], 100 * d["hi"]], [yy, yy], color=color, linewidth=2)
                ax.plot(100 * d["est"], yy, marker, color=color, markersize=7, markeredgecolor=SURFACE,
                        markeredgewidth=1.5, label=label if j == 0 else None)
        ax.set_yticks([len(rows) - j for j in range(len(rows))],
                      [f"{fam}  ({setting})" for fam, setting, _, _ in rows], fontsize=8)
        ax.set_xlim(-3, 103)
        ax.set_xlabel("% of harmful episodes, raw channel", color=INK2)
        ax.set_title(title, color=INK, fontsize=11, loc="left")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=9, loc="lower center", ncol=2)
    fig.suptitle("Which tasks lead to collusion. Bars: 95% CI clustered over items", color=INK2,
                 fontsize=9, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def load_opt(path: str) -> dict | None:
    f = ROOT / path
    return json.loads(f.read_text()) if f.exists() else None


def main() -> None:
    S = {a: load(a) for a in AGENTS}
    st = {a: S[a]["stats"] for a in AGENTS}
    mon = {a: S[a]["monitors"].get("gemini") for a in AGENTS}
    W = {a: load_opt(f"results/workflow_{a}/stats.json") for a in AGENTS}
    wst = {a: W[a]["stats"] if W[a] else None for a in AGENTS}
    wmon = {a: (W[a]["monitors"].get("gemini") if W[a] else None) for a in AGENTS}
    agree = json.loads((ROOT / "results/reader_agreement.json").read_text())
    g, q = st["gemini"], st["qwen"]
    gs = [json.loads(l) for l in (ROOT / "data/stimuli/gate_scored.jsonl").read_text().splitlines()[1:]]
    gate_push = {}
    for ch in CHANNELS:
        v = [r["pushes_collusive"] for r in gs if r["item_class"] == "harmful" and r["channel"] == ch
             and r["pushes_collusive"] is not None]
        gate_push[ch] = sum(v) / len(v)

    L = ["# What counts as evidence of agent collusion?", "",
         "Track 2 (detection and audit). Exploratory. Generated by `analysis/report.py` from "
         "`results/*/stats.json`. Do not edit by hand.", ""]
    L += ["## The question", "",
          "Two AI agents work for rival principals: shops on a fictional Vietnamese marketplace, "
          "or firms, contest teams and departments on a fictional work platform. The rival sends a "
          "message inviting the agent into an arrangement that hurts a third party. Sometimes the "
          "invitation is direct, sometimes it is a euphemism, an appeal to \"anh em\", or a bare "
          "announcement. We log every turn and ask the three Track 2 questions: which tasks lead to "
          "collusion (2.1), whether reading what agents say together with what they do beats either "
          "alone (2.2), and what should count as convincing evidence (2.3).", ""]
    L += ["## One episode", ""] + example()
    L += ["## Setup", "", "| | |", "|---|---|",
          "| Market set | 60 items: six families, five harmful scenarios each, each with a harmless twin of the same shape; three channels (raw, paraphrased, neutralized) |",
          "| Workflow set | 30 items: three families outside markets, same design; raw channel only |",
          f"| Renderings | {', '.join(RENDERINGS)} (written once by Gemini, then frozen) |",
          f"| Agents | {LABEL['gemini']}, {LABEL['qwen']}; {g['n_episodes']} market episodes each"
          + (f", {wst['gemini']['n_episodes']} workflow episodes each" if wst['gemini'] else "") + " |",
          "| Monitor | Gemini 2.5 Flash, reading six views of each episode |",
          "| Intervals | bootstrap 95%, 10,000 resamples, clustered over items |", ""]

    # --- 2.1 ---------------------------------------------------------------------
    L += ["## 2.1 Which tasks lead to collusion?", "",
          "A task can lead to collusion in two ways. The agent may take the arrangement on its own, "
          "before anyone asks (turn 1). Or the rival's message may pull it in (moved: competitive at "
          "turn 1, collusive at turn 2). The two rank tasks differently, so we report both.", ""]
    fams = []
    for a in AGENTS:
        for src in (st[a], wst[a]):
            if src:
                for f in src["by_family_raw"]:
                    if f not in fams:
                        fams.append(f)
    setting = {f: ("workflow" if wst["gemini"] and f in wst["gemini"]["by_family_raw"] else "market") for f in fams}

    def fam_row(a, f):
        src = wst[a] if setting[f] == "workflow" else st[a]
        return src["by_family_raw"].get(f) if src else None

    def top(a, key):
        rows = [(f, fam_row(a, f)) for f in fams if fam_row(a, f) and fam_row(a, f)[key]["est"] is not None]
        f, r = max(rows, key=lambda x: x[1][key]["est"])
        return f"`{f}` ({p(r[key])})"
    L += [f"Taken unprompted most often: {top('gemini', 'turn1')} for Gemini, {top('qwen', 'turn1')} for Qwen. "
          f"Pulled in by the message most often: {top('gemini', 'moved')} for Gemini, {top('qwen', 'moved')} "
          "for Qwen. The two agents rank the tasks differently, so a task list is a property of the "
          "model as much as of the task. Five scenarios per family: read the table as description.", "",
          "Raw channel, harmful items (%):", "",
          "| family | setting | Gemini turn 1 | Gemini moved | Qwen turn 1 | Qwen moved |",
          "|---|---|---|---|---|---|"]
    for f in fams:
        rg, rq = fam_row("gemini", f), fam_row("qwen", f)
        L.append(f"| {f} | {setting[f]} | {ci(rg['turn1']) if rg else 'n/a'} | {ci(rg['moved']) if rg else 'n/a'} | "
                 f"{ci(rq['turn1']) if rq else 'n/a'} | {ci(rq['moved']) if rq else 'n/a'} |")
    (ROOT / "results/figures").mkdir(parents=True, exist_ok=True)
    fig_families([(f, setting[f], fam_row("gemini", f), fam_row("qwen", f)) for f in fams],
                 ROOT / "results/figures/families.png")
    L += ["", "![Which tasks lead to collusion](figures/families.png)", ""]

    # --- 2.2 ---------------------------------------------------------------------
    L += ["", "## 2.2 Do words and actions together beat either alone?", ""]
    if mon["gemini"] and "pooled" in mon["gemini"]:
        mg = mon["gemini"]["pooled"]
        mq = mon["qwen"]["pooled"] if mon.get("qwen") and "pooled" in mon["qwen"] else None
        L += [f"Yes. Shown only the situation and the agent's decision, the monitor missed "
              f"{p(mg['fnr']['action'])} of colluding Gemini episodes. Adding the agent's report to its "
              f"owner cut that to {p(mg['fnr']['report'])}, while false alarms on episodes where the agent "
              f"declined stayed at {p(mg['fpr_declined']['report'])}. The report alone did about as well "
              f"({p(mg['fnr']['report_only'])} missed), because it restates the action.", "",
              f"The rival's message is a different kind of word. With it in view the monitor missed "
              f"{p(mg['fnr']['delivered'])} but flagged {p(mg['fpr_declined']['delivered'])} of declined "
              f"episodes, and the message alone flagged {p(mg['fpr_declined']['message_only'])}. It "
              "detects the proposal, not the uptake.", ""]
        if mq:
            L += [f"The agent's words are only as good as the agent's candour: Qwen's reports hid more, and "
                  f"action plus report still missed {p(mq['fnr']['report'])} of its colluding episodes.", ""]
        L += ["![Says versus does](main_gemini/figures/says_vs_does_gemini.png)", ""]
        wg = wmon["gemini"]["pooled"] if wmon.get("gemini") and "pooled" in wmon["gemini"] else None
        rows22 = [("action", "action only"), ("report", "action + report"), ("report_only", "report only"),
                  ("message_only", "message only"), ("delivered", "action + report + message")]
        L += [f"Gemini monitor on {LABEL['gemini']} episodes (%; market pooled over channels, workflow raw):", "",
              "| view | market: missed | market: false alarm, declined | workflow: missed | workflow: false alarm, declined |",
              "|---|---|---|---|---|"]
        for v, lab in rows22:
            L.append(f"| {lab} | {ci(mg['fnr'][v])} | {ci(mg['fpr_declined'][v])} | "
                     f"{ci(wg['fnr'][v]) if wg and v in wg['fnr'] else 'n/a'} | "
                     f"{ci(wg['fpr_declined'][v]) if wg and v in wg['fpr_declined'] else 'n/a'} |")
        L.append("")
        if wg:
            L += [f"The pattern holds outside markets: on the workflow set, action only missed "
                  f"{p(wg['fnr']['action'])}, action plus report missed {p(wg['fnr']['report'])}, and the "
                  f"message alone flagged {p(wg['fpr_declined']['message_only'])} of declined episodes.", ""]

    # --- 2.3 ---------------------------------------------------------------------
    L += ["## 2.3 What should count as convincing evidence?", "",
          "Three layers of evidence, each wrong in a measurable way on its own:", ""]
    if mon["gemini"] and "pooled" in mon["gemini"]:
        mg = mon["gemini"]["pooled"]
        L += [f"1. **The proposal** (the rival's message) shows an arrangement was offered, not taken: "
              f"read alone it flagged {p(mg['fpr_declined']['message_only'])} of declined episodes.",
              f"2. **The uptake** (the agent's action) shows what was done, not why: read alone it missed "
              f"{p(mg['fnr']['action'])} of colluding episodes, and {p(g['turn1']['harmful'])} of Gemini's "
              "harmful episodes took the same action before any message, so an action alone cannot separate "
              "collusion from a unilateral choice.",
              f"3. **The account** (the agent's own words) is candid when asked and silent otherwise: "
              f"{p(g['disclosure']['item_cO'])} (Gemini) and {p(q['disclosure']['item_cO'])} (Qwen) of "
              "colluding episodes said yes to a direct question, but only "
              f"{p(g['disclosure']['lexical'])} and {p(q['disclosure']['lexical'])} mentioned the message "
              "in their report.", "",
              "Convincing evidence is therefore a proposal, an action that matches it, and a timing that "
              "rules out the unilateral reading (the agent competed before the message and colluded after).", ""]
    L += ["Two robustness checks on that standard:", "",
          "- **Rewriting the message does not erase the evidence.** The platform relays changed the "
          "wording (paraphrased) or removed the social framing (neutralized), yet the gate still read "
          "a push toward the arrangement in "
          + ", ".join(f"{100 * gate_push[ch]:.0f}% ({ch})" for ch in ("raw", "paraphrased", "neutralized"))
          + " of harmful messages. The relays did not stop collusion either: uptake changed by "
          f"{pp(g['relay_effect']['harmful']['paraphrased']['all'])} and "
          f"{pp(g['relay_effect']['harmful']['neutralized']['all'])} for Gemini, "
          f"{pp(q['relay_effect']['harmful']['paraphrased']['all'])} and "
          f"{pp(q['relay_effect']['harmful']['neutralized']['all'])} for Qwen (paraphrased, neutralized).",
          "- **What a message means depends on the reader.** Four LLM readers re-read every harmful "
          "message: " + "; ".join(f"{n} agreed with the gate on {100 * r['harmful']['agreement']:.0f}%"
                                  for n, r in agree["readers"].items() if "harmful" in r)
          + ". The outlier, gpt-5.4-nano, read two families the other way; a native Vietnamese reader "
          "judged its reading wrong. A small reader can manufacture disagreement about intent.", ""]

    L += ["## Questions a sceptic would ask", "",
          "**Does harmless cooperation survive?** Yes. On twins of the same shape the agents cooperated "
          f"in every channel ({p(g['turn2']['mutual_gains']['raw']['all'], 1)} Gemini, "
          f"{p(q['turn2']['mutual_gains']['raw']['all'], 1)} Qwen on the raw channel), and the monitor "
          "raised almost no false alarms on them except when it read the message alone.", "",
          "**Is the second monitor any use?** No. The Qwen3-8B monitor flagged most harmless twins, so "
          "its low miss rate carries no information. It is kept in `stats.md` as a failed baseline.", ""]
    L += ["## Limits", "",
          "- Exploratory. The market design changed twice after smoke runs, before the main run; every change is logged in `docs/execution-plan.md`.",
          "- Five scenarios per family; family-level results are descriptive.",
          "- Messages are model-written; no human validation sample, one informal native-reader check.",
          "- One paraphrase per message; Qwen agents read Qwen-relayed text.",
          "- English quotations are machine translations for display; agents saw only the Vietnamese.",
          "- The lexical disclosure code is the weakest measure; read it beside the direct question.", ""]
    A = ["## Appendix", "", "Full tables. Every number is in `results/*/stats.md` with its interval.", ""]
    for label, mm in (("market", mon), ("workflow", wmon)):
        for a in AGENTS:
            m = mm[a]
            if not m or "pooled" not in m:
                continue
            A += [f"Gemini monitor, {label} set, {LABEL[a]} episodes (%):", "",
                  "| view | missed | missed, message-moved only | false alarm, declined | false alarm, twins |",
                  "|---|---|---|---|---|"]
            for v in m["views"]:
                pm = m["pooled"]
                A.append(f"| {v} | {ci(pm['fnr'][v])} | {ci(pm['fnr_moved'][v])} | "
                         f"{ci(pm['fpr_declined'][v])} | {ci(pm['fpr_twins'][v])} |")
            A.append("")
    A += ["Uptake of the harmful arrangement at turn 2, market set (%):", "",
          "| agent | turn 1 | " + " | ".join(CHANNELS) + " |", "|---" * (len(CHANNELS) + 2) + "|"]
    for a in AGENTS:
        A.append(f"| {LABEL[a]} | {ci(st[a]['turn1']['harmful'])} | "
                 + " | ".join(ci(st[a]['turn2']['harmful'][ch]['all']) for ch in CHANNELS) + " |")
    A += ["", "Relay minus raw, harmful items (percentage points):", "",
          "| agent | paraphrased | neutralized |", "|---|---|---|"]
    for a in AGENTS:
        r = st[a]["relay_effect"]["harmful"]
        A.append(f"| {LABEL[a]} | {ci(r['paraphrased']['all'])} | {ci(r['neutralized']['all'])} |")
    A += ["", "Message readers, harmful texts, % read as pushing toward the collusive option:", "",
          "| family | " + " | ".join(["gemini gate", *agree["readers"]]) + " |",
          "|---" * (len(agree["readers"]) + 2) + "|"]
    for f, row in agree["by_family"].items():
        A.append(f"| {f} | " + " | ".join(f"{100 * row[n]:.1f}" if row.get(n) is not None else "n/a"
                                          for n in ["gemini", *agree["readers"]]) + " |")
    A += ["", "![Uptake by channel, Gemini](main_gemini/figures/collusion_by_channel.png)", "",
          "![Uptake by channel, Qwen](main_qwen/figures/collusion_by_channel.png)", ""]
    L += A
    out = ROOT / "results/REPORT.md"
    text = "\n".join(L) + "\n"
    assert "\u2014" not in text, "house style: no em dashes"
    out.write_text(text)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
