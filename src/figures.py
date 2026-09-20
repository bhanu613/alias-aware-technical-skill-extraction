"""Data-derived figures used in the repository and research poster."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

SYSTEM_A_COLOR = "#6B7280"
SYSTEM_B_COLOR = "#173B5F"
RECOVERY_COLOR = "#0F766E"
ERROR_COLORS = ["#C2410C", "#7C3AED", "#B45309", "#2563EB"]


def _save(figure, output_stem: Path) -> None:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_stem.with_suffix(".png"), dpi=400, bbox_inches="tight", facecolor="white")
    figure.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(figure)


def plot_system_comparison(metric_summary: pd.DataFrame, output_stem: Path) -> None:
    """Create the main System A versus System B performance figure."""
    metrics = ["Micro precision", "Micro recall", "Micro F1", "Exact-set-match rate"]
    labels = ["Precision", "Recall", "Micro F1", "Exact-set\nmatch rate"]
    indexed = metric_summary.set_index("System")
    figure, axis = plt.subplots(figsize=(12, 7))
    positions = list(range(len(metrics)))
    width = 0.34
    bars_a = axis.bar([p - width / 2 for p in positions], indexed.loc["System A", metrics], width, color=SYSTEM_A_COLOR, label="System A: canonical forms only")
    bars_b = axis.bar([p + width / 2 for p in positions], indexed.loc["System B", metrics], width, color=SYSTEM_B_COLOR, label="System B: canonical forms + aliases")
    axis.set_ylim(0, 1.10)
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Score")
    axis.set_title("Held-Out Performance: System A vs System B", weight="bold", pad=16)
    axis.grid(axis="y", linestyle="--", alpha=0.4)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="lower left")
    for bar in list(bars_a) + list(bars_b):
        axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.025, f"{bar.get_height():.3f}", ha="center", va="bottom")
    figure.tight_layout()
    _save(figure, output_stem)


def plot_recovery_by_label(per_label_metrics: pd.DataFrame, output_stem: Path) -> None:
    """Create recovery counts by canonical label."""
    recovery = per_label_metrics[["Canonical label", "Recovered by System B"]].copy()
    recovery = recovery[recovery["Recovered by System B"] > 0].sort_values("Recovered by System B")
    figure, axis = plt.subplots(figsize=(12, 8))
    bars = axis.barh(recovery["Canonical label"], recovery["Recovered by System B"], color=RECOVERY_COLOR)
    axis.set_xlabel("Gold-label instances recovered by System B")
    axis.set_title("Where Alias-Aware Matching Recovered System A Misses", weight="bold", pad=16)
    axis.grid(axis="x", linestyle="--", alpha=0.4)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    for bar in bars:
        axis.text(bar.get_width() + 0.35, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va="center", weight="bold")
    axis.text(0.99, 0.02, f"Total recovered instances: {int(recovery['Recovered by System B'].sum())}", transform=axis.transAxes, ha="right", va="bottom")
    figure.tight_layout()
    _save(figure, output_stem)


def plot_residual_errors(decision_record: pd.DataFrame, output_stem: Path) -> None:
    """Create residual System B false-negative categories from the decision record."""
    names = {
        "Unapproved lexical variant or abbreviation": "Unapproved variants\nor abbreviations",
        "Conservative hyphen/boundary-policy block": "Hyphen/boundary\npolicy effects",
        "Indirect related-technology reference": "Indirect related-\ntechnology reference",
        "Compound or slash-separated expression": "Compound or slash-\nseparated expression",
    }
    summary = decision_record["Error family"].value_counts().rename_axis("Error family").reset_index(name="Residual FN instances")
    summary["Display label"] = summary["Error family"].map(names)
    assert summary["Display label"].notna().all()
    summary = summary.sort_values("Residual FN instances")
    figure, axis = plt.subplots(figsize=(12, 7))
    bars = axis.barh(summary["Display label"], summary["Residual FN instances"], color=ERROR_COLORS[:len(summary)])
    axis.set_xlabel("Residual System B false-negative instances")
    axis.set_title("Residual Error Patterns After Alias Expansion", weight="bold", pad=16)
    axis.grid(axis="x", linestyle="--", alpha=0.4)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    for bar in bars:
        axis.text(bar.get_width() + 0.10, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va="center", weight="bold")
    axis.text(0.99, 0.02, f"{int(summary['Residual FN instances'].sum())} instances", transform=axis.transAxes, ha="right", va="bottom")
    figure.tight_layout()
    _save(figure, output_stem)
