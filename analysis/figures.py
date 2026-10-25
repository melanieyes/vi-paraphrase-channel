"""The paper's figures, drawn from generated stats only.

Style: one accent hue plus neutral grey, direct labels instead of legends where
possible, thin interval lines, no top/right spines, light grid. Colours come from
the dataviz reference palette (validated light-mode: blue #2a78d6, orange #eb6834).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

INK, INK2, GRID, BG = "#1d1d1b", "#6b6a66", "#e9e8e4", "#ffffff"
ACCENT, ACCENT2, NEUTRAL = "#2a78d6", "#eb6834", "#a8a7a2"
LABEL = {"gemini": "Gemini 2.5 Flash", "qwen": "Qwen3-8B"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
    "xtick.major.size": 0, "ytick.major.size": 0, "savefig.dpi": 300,
})


def _pct(d):
    return None if not d or d.get("est") is None else (100 * d["est"], 100 * d["lo"], 100 * d["hi"])


def tasks(by_family: dict[str, dict[str, dict]], workflow_fams: set[str], path: Path) -> None:
    """Figure 1. Per family: taken unprompted (grey) and pulled in by the message (blue)."""
    fams = sorted(by_family["gemini"],
                  key=lambda f: -sum((by_family[a].get(f, {}).get("moved") or {}).get("est") or 0
                                     for a in by_family))
    n = len(fams)
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 0.27 * n + 1.0), sharey=True)
    for ax, agent in zip(axes, ("gemini", "qwen")):
        ax.set_facecolor(BG)
        ax.xaxis.grid(True, color=GRID, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        for i, f in enumerate(fams):
            y = n - 1 - i
            row = by_family.get(agent, {}).get(f)
            if not row:
                continue
            for key, color, dy, size in (("turn1", NEUTRAL, 0.17, 4.5), ("moved", ACCENT, -0.17, 5.5)):
                v = _pct(row[key])
                if v is None:
                    continue
                ax.plot([v[1], v[2]], [y + dy, y + dy], color=color, linewidth=1.1, alpha=0.75,
                        solid_capstyle="round")
                ax.plot(v[0], y + dy, "o", color=color, markersize=size, markeredgecolor=BG,
                        markeredgewidth=0.8, zorder=3)
        ax.set_xlim(-2, 102)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("% of harmful episodes")
        ax.set_title(LABEL[agent], loc="left", color=INK, fontweight="bold")
    axes[0].set_yticks(range(n))
    axes[0].set_yticklabels([f.replace("_", " ") for f in reversed(fams)])
    for lab, f in zip(axes[0].get_yticklabels(), reversed(fams)):
        lab.set_color(INK if f not in workflow_fams else ACCENT2)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", linestyle="-", color=NEUTRAL, markersize=4.5, linewidth=1.1,
                      label="taken unprompted (turn 1)"),
               Line2D([], [], marker="o", linestyle="-", color=ACCENT, markersize=5.5, linewidth=1.1,
                      label="pulled in by the message"),
               Line2D([], [], linestyle="none", label="orange family names: workflow")]
    leg = fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8,
                     bbox_to_anchor=(0.5, -0.02), handlelength=1.6)
    leg.get_texts()[2].set_color(ACCENT2)
    fig.tight_layout(w_pad=1.2, rect=(0, 0.06, 1, 1))
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


VIEW_LABEL = {"action": "action only", "report_only": "", "message_only": "message only",
              "report": "action + report  (report only is the same point)",
              "delivered": "action + report + message"}
# label offsets in points, chosen so labels clear their points and each other
OFFSET = {"action": (7, 0), "report_only": (0, 0), "message_only": (-4, 9),
          "report": (9, -7), "delivered": (0, 9)}


BAR_VIEWS = [("action", "action only"), ("report_only", "report only"), ("message_only", "message only"),
             ("report", "action + report"), ("delivered", "action + report + message"),
             ("baseline_info", "  + baseline, same episode"), ("family_baseline", "  + baseline, similar situations")]
# The rule row ("standard") is left out on purpose: the rule tells the monitor to clear unilateral
# choices, so "missed, all collusion" would count those clears as misses. The table reports it.
HERO = "family_baseline"


def butterfly(monitors: list[tuple[str, dict]], path: Path) -> None:
    """Figure 2. Rows are monitor views. Left: missed collusion. Right: false alarms on harmful
    episodes the agent declined. One bar per monitor, darker for the first; thin lines are 95% CIs."""
    n = len(BAR_VIEWS)
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(6.8, 0.42 * n + 1.1), sharey=True,
                                   gridspec_kw={"wspace": 0.04})
    h = 0.34
    shades = [1.0, 0.45]
    for j, (name, pooled) in enumerate(monitors):
        for i, (v, _) in enumerate(BAR_VIEWS):
            y = n - 1 - i + (h / 2 if j == 0 else -h / 2)
            miss, fa = _pct(pooled["fnr"].get(v)), _pct(pooled["fpr_declined"].get(v))
            for ax, val, color, sign in ((axl, miss, ACCENT, -1), (axr, fa, ACCENT2, 1)):
                if val is None:
                    continue
                ax.barh(y, sign * val[0], height=h * 0.9, color=color, alpha=shades[j], linewidth=0)
                ax.plot([sign * val[1], sign * val[2]], [y, y], color=INK2, linewidth=0.7, alpha=0.8)
                ax.text(sign * (max(val[0], val[2]) + 2), y, f"{val[0]:.0f}", va="center",
                        ha="right" if sign < 0 else "left", fontsize=7, color=INK2)
    for ax, title in ((axl, "missed collusion (%)"), (axr, "false alarms on declined episodes (%)")):
        ax.set_facecolor(BG)
        ax.xaxis.grid(True, color=GRID, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        ax.set_title(title, color=INK, fontsize=8.5, loc="center")
    axl.set_xlim(-112, 0)
    axl.set_xticks([-100, -75, -50, -25, 0], ["100", "75", "50", "25", "0"])
    axr.set_xlim(0, 112)
    axr.set_xticks([0, 25, 50, 75, 100])
    axl.set_yticks(range(n))
    axl.set_yticklabels([lab for _, lab in reversed(BAR_VIEWS)])
    for lab, (v, _) in zip(axl.get_yticklabels(), reversed(BAR_VIEWS)):
        if v == HERO:
            lab.set_fontweight("bold")
            lab.set_color(INK)
    # the three baseline rows sit under a light band: what the evidence standard adds
    nb = sum(1 for v, _ in BAR_VIEWS if v in ("baseline_info", "family_baseline", "standard"))
    for ax in (axl, axr):
        ax.axhspan(-0.5, nb - 0.5, color="#f3f6fb", zorder=0)
    axl.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    handles = [Patch(color=INK2, alpha=s, label=name) for (name, _), s in zip(monitors, shades)]
    fig.legend(handles=handles, loc="lower center", ncol=len(monitors), frameon=False, fontsize=7.5,
               bbox_to_anchor=(0.55, -0.02), title="monitor (darker: first listed)", title_fontsize=7.5)
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def pipeline(path: Path) -> None:
    """Figure 1. Who does what. Three phases left to right; each card names a role, the model that
    plays it, and what it produces. Solid arrows: the main path; dashed: the alternative inputs."""
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    fig, ax = plt.subplots(figsize=(7.0, 3.05))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 44)
    ax.axis("off")
    GREEN = "#1d8a5f"
    COL = {"build": ACCENT, "run": ACCENT2, "audit": GREEN}
    TINT = {"build": "#f2f7fd", "run": "#fef5f0", "audit": "#f1f8f4"}

    def phase(x0, x1, key, label, sub):
        ax.add_patch(FancyBboxPatch((x0, 0.6), x1 - x0, 42.2, boxstyle="round,pad=0,rounding_size=1.4",
                                    facecolor=TINT[key], edgecolor="none", zorder=0))
        ax.text(x0 + 1.4, 41.4, label, color=COL[key], fontsize=7.6, fontweight="bold", va="top")
        ax.text(x0 + 1.4, 38.6, sub, color=INK2, fontsize=5.9, va="top", style="italic")

    def card(x, y, w, h, title, model, body, key, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.9",
                                    facecolor="white", edgecolor=COL[key] if dashed else "#d9d8d3",
                                    linewidth=0.8, linestyle=(0, (3, 2)) if dashed else "-", zorder=2))
        if not dashed:
            ax.add_patch(FancyBboxPatch((x, y + h - 0.9), w, 0.9, boxstyle="round,pad=0,rounding_size=0.4",
                                        facecolor=COL[key], edgecolor="none", zorder=3))
        ax.text(x + 1.3, y + h - 2.0, title, ha="left", va="top", fontsize=6.7, fontweight="bold",
                color=INK, zorder=4)
        top = y + h - 4.8
        if model:
            ax.text(x + 1.3, top, model, ha="left", va="top", fontsize=5.5, color=COL[key],
                    linespacing=1.3, zorder=4)
            top -= 2.5 * (model.count("\n") + 1) + 1.2
        ax.text(x + 1.3, top, body, ha="left", va="top", fontsize=5.6,
                color=INK2, linespacing=1.45, zorder=4)

    def arrow(p, q, dashed=False, rad=0.0):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7, color=INK2, linewidth=0.8,
                                     linestyle=(0, (3, 2)) if dashed else "-",
                                     connectionstyle=f"arc3,rad={rad}", zorder=1))

    phase(0.5, 44.5, "build", "1  BUILD", "once, then frozen")
    phase(45.5, 66.5, "run", "2  RUN", "every episode")
    phase(67.5, 99.5, "audit", "3  AUDIT", "offline, on the log")

    card(1.8, 18.5, 11.3, 17, "Item", "", "situation\ntwo options\nharmless\ntwin", "build")
    card(15.4, 18.5, 12.6, 17, "Renderer", "Gemini 2.5 Flash", "rival's\ninvitation\nin 4 styles", "build")
    card(30.3, 12.0, 12.8, 23.5, "Relay", "Qwen3-8B", "raw\nparaphrased\nneutralized\n4 summaries", "build")
    card(1.8, 2.2, 26.2, 13.5, "Gate + 4 LLM readers", "Gemini gate; Opus, Gemini Pro,\nGemma and GPT readers",
         "check: does each text still invite?", "build", dashed=True)

    card(47.0, 6.5, 18.0, 29, "Agent", "Gemini 2.5 Flash\nor Qwen3-8B",
         "T1  choose A or B\nT2  read message,\n       choose again\nT3  report to owner\nT4  influenced?\n       CÓ / KHÔNG",
         "run")

    card(69.0, 18.5, 13.6, 17, "Log", "", "message\naction\nreport\nbaseline", "audit")
    card(69.0, 2.2, 13.6, 13.5, "Summarizer", "Gemma-3-27B", "≤80-word entry", "audit", dashed=True)
    card(84.9, 6.5, 13.6, 29, "Monitor", "Aya Expanse 8B\nor Claude Haiku 5.5",
         "reads one view\nof the log, or\nthe summary\n\nFLAG / CLEAR", "audit")

    arrow((13.1, 27), (15.4, 27))
    arrow((28.0, 27), (30.3, 27))
    arrow((43.1, 27), (47.0, 27))
    arrow((65.0, 27), (69.0, 27))
    arrow((82.6, 27), (84.9, 27))
    arrow((75.8, 18.5), (75.8, 15.7), dashed=True)
    arrow((82.6, 9), (84.9, 11), dashed=True)
    arrow((28.0, 9), (30.3, 12.6), dashed=True)
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def asked_vs_told(rows: list[tuple[str, dict]], path: Path) -> None:
    """Who mentions the rival's message, among colluding harmful episodes. One row per agent:
    the agent asked directly (grey), the agent's own report (orange), a neutral third-party
    summary of the trace (blue). All three coded in code; thin lines are 95% CIs."""
    bars = [("item_cO", "answers yes when asked", NEUTRAL),
            ("lexical", "own report mentions it", ACCENT2),
            ("summary_lexical", "neutral summary mentions it", ACCENT)]
    fig, ax = plt.subplots(figsize=(6.6, 0.62 * len(rows) + 0.75))
    h = 0.24
    for i, (label, d) in enumerate(rows):
        y0 = len(rows) - 1 - i
        for j, (k, _, color) in enumerate(bars):
            v = _pct(d.get(k))
            if v is None:
                continue
            y = y0 + (1 - j) * h
            ax.barh(y, v[0], height=h * 0.86, color=color, linewidth=0)
            ax.plot([v[1], v[2]], [y, y], color=INK2, linewidth=0.7)
            ax.text(max(v[0], v[2]) + 1.5, y, f"{v[0]:.0f}%", va="center", fontsize=7, color=INK2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([lab for lab, _ in reversed(rows)])
    ax.set_xlim(0, 108)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("% of colluding harmful episodes")
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=c, label=l) for _, l, c in bars], loc="lower center", ncol=3,
               frameon=False, fontsize=7.5, bbox_to_anchor=(0.55, 0.0))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
