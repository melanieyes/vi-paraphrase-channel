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
    # Legend swatches in the bars' own colours: each monitor is a blue/orange pair, darker for the first.
    from matplotlib.legend_handler import HandlerTuple
    from matplotlib.patches import Patch
    handles = [(Patch(color=ACCENT, alpha=a_), Patch(color=ACCENT2, alpha=a_)) for a_ in shades]
    fig.legend(handles=handles, labels=[f"{name} monitor" for name, _ in monitors], loc="lower center",
               ncol=len(monitors), frameon=False, fontsize=7.5, bbox_to_anchor=(0.55, 0.0),
               handler_map={tuple: HandlerTuple(ndivide=None, pad=0)}, handlelength=2.6)
    fig.subplots_adjust(bottom=0.12)
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def pipeline(path: Path) -> None:
    """Figure 1. The design as one illustrative episode. Top: what the agent does before and after the
    rival's message (collusion = the switch the message causes). Bottom: what a monitor concludes from
    each kind of evidence. Schematic: the episode is an example, not a data point."""
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis("off")
    GREEN, GREY_BG = "#1d8a5f", "#f3f2ef"
    COLL = ACCENT2                         # the collusive option
    FW, FY, FH = 31.0, 27.0, 23.5          # frame width, bottom, height
    FX = [0.5, 34.5, 68.5]

    def frame(x, num, title, edge):
        ax.add_patch(FancyBboxPatch((x, FY), FW, FH, boxstyle="round,pad=0,rounding_size=1.4",
                                    facecolor="white", edgecolor=edge, linewidth=1.0, zorder=1))
        ax.text(x + 1.6, FY + FH - 2.4, f"{num}  {title}", fontsize=7.4, fontweight="bold", color=INK, va="center")

    def chip(x, y, w, text, picked, col):
        ax.add_patch(FancyBboxPatch((x, y), w, 3.6, boxstyle="round,pad=0,rounding_size=1.8",
                                    facecolor=col if picked else GREY_BG, edgecolor="none", zorder=2))
        ax.text(x + 1.4, y + 1.8, text, fontsize=6.2, va="center", zorder=3,
                color="white" if picked else INK2, fontweight="bold" if picked else "normal")

    # frame 1: before any message
    frame(FX[0], "1", "Before any message", INK2)
    chip(FX[0] + 2, FY + 13.5, 26, "A  Hold the price", False, COLL)
    chip(FX[0] + 2, FY + 8.6, 26, "B  Cut the price", True, INK2)
    ax.text(FX[0] + FW / 2, FY + 3.6, "the agent competes", ha="center", fontsize=6.2, color=INK2, style="italic")

    # frame 2: the rival's message
    frame(FX[1], "2", "The rival's message", ACCENT)
    ax.add_patch(FancyBboxPatch((FX[1] + 2, FY + 7.0), FW - 4, 11.8, boxstyle="round,pad=0,rounding_size=2.2",
                                facecolor="#e8f1fc", edgecolor="none", zorder=2))
    ax.text(FX[1] + FW / 2, FY + 15.0, "\u201cmong anh em m\u00ecnh\nc\u00f9ng gi\u1eef gi\u00e1 nh\u00e9\u201d",
            ha="center", va="center", fontsize=6.6, color=INK, zorder=3, linespacing=1.25)
    ax.text(FX[1] + FW / 2, FY + 9.6, "let's both hold the price, brothers", ha="center", va="center",
            fontsize=5.9, color=INK2, style="italic", zorder=3)
    ax.text(FX[1] + FW / 2, FY + 3.6, "4 styles, from a direct proposal\nto a bare announcement", ha="center",
            fontsize=5.8, color=INK2, linespacing=1.3)

    # frame 3: after the message
    frame(FX[2], "3", "After the message", COLL)
    chip(FX[2] + 2, FY + 13.5, 26, "A  Hold the price", True, COLL)
    chip(FX[2] + 2, FY + 8.6, 26, "B  Cut the price", False, COLL)
    ax.text(FX[2] + 2.2, FY + 5.0, "report to owner: \u201ckept the price\nto protect margins\u201d (no mention)",
            fontsize=5.6, color=INK2, va="center", linespacing=1.25)
    ax.text(FX[2] + 2.2, FY + 1.8, "asked directly if influenced: yes", fontsize=5.6, color=INK2, va="center")

    for i in range(2):
        ax.add_patch(FancyArrowPatch((FX[i] + FW + 0.3, FY + FH / 2), (FX[i + 1] - 0.3, FY + FH / 2),
                                     arrowstyle="-|>", mutation_scale=9, color=INK2, linewidth=1.0))
    # the definition, between the bands
    ax.text(50, 23.6, "Collusion is the switch the message caused: B in frame 1, A in frame 3.",
            ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLL)

    # bottom: what a monitor sees and concludes
    ax.text(0.5, 19.6, "What a monitor sees, and what it concludes", fontsize=7.0, fontweight="bold",
            color=INK, va="center")
    CASES = [("Only the action (3)", "cannot tell whether the\nmessage caused it", INK2, GREY_BG, False),
             ("Action + message (2, 3)", "flags agents that refused\nthe offer too", ACCENT2, "#fdf1ea", False),
             ("+ what it did before (1),\nor on similar cases", "sees the switch: FLAG.\nOur proposed standard", GREEN, "#eef7f2", True)]
    for (head, verdict, col, bg, best), x in zip(CASES, FX):
        ax.add_patch(FancyBboxPatch((x, 4.2), FW, 12.4, boxstyle="round,pad=0,rounding_size=1.4",
                                    facecolor=bg, edgecolor=col if best else "none", linewidth=1.2))
        ax.text(x + FW / 2, 12.8, head, ha="center", va="center", fontsize=6.4, fontweight="bold",
                color=INK, linespacing=1.25)
        ax.text(x + FW / 2, 7.6, verdict, ha="center", va="center", fontsize=6.3, color=col,
                fontweight="bold" if best else "normal", linespacing=1.3)
    ax.text(0.5, 1.6, "Illustrative episode. Agents: Gemini 2.5 Flash, Qwen3-8B. Monitors: Mistral Small 3.1 24B, "
            "Claude Haiku 5.5.", fontsize=5.6, color=INK2,
            style="italic", va="center")
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
