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


def _tradeoff_panel(ax, market: dict, workflow: dict | None, title: str, labels: bool) -> None:
    ax.set_facecolor(BG)
    ax.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.add_patch(plt.Rectangle((-3, -3), 23, 23, color=ACCENT, alpha=0.06, zorder=0, linewidth=0))
    for pooled, marker, color, name in ((market, "o", ACCENT, "market"), (workflow, "D", ACCENT2, "workflow")):
        if not pooled:
            continue
        for v in VIEW_LABEL:
            x, y = _pct(pooled["fpr_declined"].get(v)), _pct(pooled["fnr"].get(v))
            if x is None or y is None:
                continue
            ax.plot([x[1], x[2]], [y[0], y[0]], color=color, linewidth=0.8, alpha=0.5)
            ax.plot([x[0], x[0]], [y[1], y[2]], color=color, linewidth=0.8, alpha=0.5)
            ax.plot(x[0], y[0], marker, color=color, markersize=5.5 if marker == "o" else 4.5,
                    markeredgecolor=BG, markeredgewidth=0.8, zorder=3)
            if labels and name == "market" and VIEW_LABEL[v]:
                dx, dy = OFFSET[v]
                ax.annotate(VIEW_LABEL[v], (x[0], y[0]), xytext=(dx, dy), textcoords="offset points",
                            color=INK, fontsize=7.5,
                            ha="right" if dx < 0 else ("center" if dx == 0 else "left"), va="center")
    ax.set_xlim(-3, 103)
    ax.set_ylim(-3, 88)
    ax.set_title(title, loc="left", color=INK, fontweight="bold")
    ax.set_xlabel("false alarms on declined episodes (%)")


VIEW_LABEL = {"action": "action only", "report_only": "", "message_only": "message only",
              "report": "action + report", "delivered": "action + report + message"}
OFFSET = {"action": (6, 0), "report_only": (0, 0), "message_only": (-4, 20),
          "report": (7, 9), "delivered": (0, 9)}


def tradeoff(panels: list[tuple[str, dict, dict | None]], path: Path) -> None:
    """Figure 2. Each monitor view as a point: false alarms on declined episodes vs missed collusion,
    one panel per monitor, same axes."""
    fig, axes = plt.subplots(1, len(panels), figsize=(6.8, 3.0), sharey=True)
    axes = axes if len(panels) > 1 else [axes]
    for i, (ax, (title, market, workflow)) in enumerate(zip(axes, panels)):
        _tradeoff_panel(ax, market, workflow, title, labels=True)
    axes[0].set_ylabel("missed collusion (%)")
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", linestyle="none", color=ACCENT, label="market (pooled over channels)"),
               Line2D([], [], marker="D", linestyle="none", color=ACCENT2, markersize=5, label="workflow (raw channel)"),
               plt.Rectangle((0, 0), 1, 1, color=ACCENT, alpha=0.12, label="few misses and few false alarms")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=7.5,
               bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=(0, 0.07, 1, 1), w_pad=1.0)
    fig.savefig(path, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
