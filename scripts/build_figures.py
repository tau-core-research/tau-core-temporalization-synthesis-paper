#!/usr/bin/env python3
"""Build the two claim-bounded synthesis figures."""

from pathlib import Path
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
SUB = ROOT / "temporalization_synthesis_submission_source" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
SUB.mkdir(parents=True, exist_ok=True)


COL = {
    "input": "#dbeafe",
    "owned": "#dcfce7",
    "conditional": "#fef3c7",
    "boundary": "#fee2e2",
    "ink": "#172554",
    "muted": "#475569",
}


def box(ax, x, y, w, h, text, color, fontsize=8.0, lw=1.1):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=lw, edgecolor=COL["ink"], facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=COL["ink"], wrap=True)
    return patch


def arrow(ax, x0, y0, x1, y1, style="-"):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=10,
        linewidth=1.05, linestyle=style, color=COL["muted"],
        shrinkA=2, shrinkB=2,
    ))


def save(fig, name):
    out = FIG / name
    fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    shutil.copy2(out, SUB / name)
    plt.close(fig)


def dependency_figure():
    fig, ax = plt.subplots(figsize=(10.4, 6.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.965, "Nonredundant dependency and ownership map",
            ha="center", va="center", fontsize=13, weight="bold", color=COL["ink"])

    labels = [
        ("Paper I\nAtemporal body\nand forward readout", 0.03),
        ("Paper II\nTyped source\nsignatures", 0.17),
        ("Paper III\nStable record\ntransport", 0.31),
        ("Paper IV\nParent-law and\nactuality boundary", 0.45),
        ("Paper V\nTemporal descent\nand process no-go", 0.59),
        ("Paper VI\nQuantizer, Choi\nand history fibers", 0.73),
        ("Paper VII\n4D terminal and\nenergy boundary", 0.87),
    ]
    for text, x in labels:
        box(ax, x, 0.72, 0.105, 0.155, text, COL["input"], 7.3)
        arrow(ax, x + 0.0525, 0.715, 0.5, 0.60)

    box(ax, 0.27, 0.46, 0.46, 0.145,
        "This paper: typed composition theorem + consolidated status ledger\n"
        "(component proofs remain owned by their canonical sources)",
        COL["owned"], 9.1, 1.4)

    outputs = [
        (0.06, "Temporalization fiber\n+ exact order cochain"),
        (0.27, "EOCC actuality\n+ progressive stabilization"),
        (0.48, "Observer time\n+ resolved records"),
        (0.69, "Operational no-go\n+ bounded discriminator"),
        (0.84, "Energy/dark-sector\nnon-entailment"),
    ]
    for x, text in outputs:
        box(ax, x, 0.20, 0.14, 0.13, text, COL["conditional"], 7.8)
        arrow(ax, 0.5, 0.455, x + 0.07, 0.335)

    box(ax, 0.16, 0.035, 0.68, 0.085,
        "Not obtained: Nature-level temporal occupation, absolute parent time, SI units,\n"
        "a unique dark sector, or empirical validation",
        COL["boundary"], 8.4, 1.25)
    arrow(ax, 0.5, 0.195, 0.5, 0.125, style="--")
    save(fig, "fig_dependency_ownership_map.pdf")


def temporalization_figure():
    fig, ax = plt.subplots(figsize=(10.2, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.965, "Temporalization, actuality and observer descent",
            ha="center", va="center", fontsize=13, weight="bold", color=COL["ink"])

    box(ax, 0.035, 0.68, 0.18, 0.17,
        "Atemporal carrier P\n"
        "simultaneous relations,\nnulls and morphology",
        COL["input"], 8.4)
    box(ax, 0.285, 0.68, 0.20, 0.17,
        "Temporalization fiber Temp(P)\n"
        "source-owned omega\n"
        "cycle periods = 0",
        COL["owned"], 8.2)
    box(ax, 0.555, 0.68, 0.19, 0.17,
        "EOCC actuality\n"
        "X = -Gamma^{-1} dA\n"
        "omega(X) > 0",
        COL["conditional"], 8.3)
    box(ax, 0.815, 0.68, 0.15, 0.17,
        "Stabilized body\n"
        "dA = 0\n"
        "no maintenance power",
        COL["conditional"], 8.1)
    arrow(ax, 0.215, 0.765, 0.285, 0.765)
    arrow(ax, 0.485, 0.765, 0.555, 0.765)
    arrow(ax, 0.745, 0.765, 0.815, 0.765)

    box(ax, 0.12, 0.40, 0.22, 0.145,
        "Nested persistent prefixes\n"
        "frozen past = restriction\n"
        "not a stored history",
        COL["owned"], 8.2)
    box(ax, 0.40, 0.40, 0.22, 0.145,
        "Body-conditioned\nobserver-source access\n"
        "+ outward record jet",
        COL["input"], 8.2)
    box(ax, 0.68, 0.40, 0.22, 0.145,
        "Stable quantizer Q_OS\n"
        "+ terminal calibration\n"
        "= observer time/records",
        COL["owned"], 8.2)
    arrow(ax, 0.65, 0.675, 0.23, 0.55)
    arrow(ax, 0.89, 0.675, 0.51, 0.55)
    arrow(ax, 0.34, 0.472, 0.40, 0.472)
    arrow(ax, 0.62, 0.472, 0.68, 0.472)

    box(ax, 0.075, 0.12, 0.37, 0.135,
        "Exact operational ceiling\n"
        "finite acyclic interventions can be represented by\n"
        "an atemporal simultaneous factor graph",
        COL["boundary"], 8.0)
    box(ax, 0.555, 0.12, 0.37, 0.135,
        "Lawful empirical target\n"
        "reject a source-frozen bounded comparator through\n"
        "nonfactorizing record/rank/capacity growth",
        COL["conditional"], 8.0)
    arrow(ax, 0.79, 0.395, 0.26, 0.26, style="--")
    arrow(ax, 0.79, 0.395, 0.74, 0.26, style="--")
    save(fig, "fig_temporalization_proof_spine.pdf")


if __name__ == "__main__":
    dependency_figure()
    temporalization_figure()
    print("TEMPORALIZATION_SYNTHESIS_FIGURES_BUILT")
