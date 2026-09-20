"""Document-level, micro-averaged, and bootstrap evaluation helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def parse_labels(value: object) -> set[str]:
    """Parse semicolon-separated labels; `none` represents an empty set."""
    if pd.isna(value):
        return set()
    cleaned = str(value).strip()
    if cleaned in {"", "none"}:
        return set()
    return {label.strip() for label in cleaned.split(";") if label.strip()}


def serialise_labels(labels: set[str]) -> str:
    """Store label sets deterministically for CSV output."""
    return ";".join(sorted(labels)) if labels else "none"


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def score_document(gold_labels: set[str], predicted_labels: set[str]) -> dict[str, object]:
    """Return set-based TP, FP, FN, and exact-match values for one document."""
    true_positives = gold_labels & predicted_labels
    false_positives = predicted_labels - gold_labels
    false_negatives = gold_labels - predicted_labels
    return {
        "TP labels": serialise_labels(true_positives),
        "FP labels": serialise_labels(false_positives),
        "FN labels": serialise_labels(false_negatives),
        "TP": len(true_positives),
        "FP": len(false_positives),
        "FN": len(false_negatives),
        "Exact set match": gold_labels == predicted_labels,
    }


def score_predictions(gold: pd.DataFrame, predictions: pd.DataFrame, prediction_column: str, prefix: str) -> pd.DataFrame:
    """Score aligned document-level predictions against frozen gold labels."""
    required_gold = {"Annotation order", "id", "Gold skills"}
    assert required_gold.issubset(gold.columns)
    assert {"Annotation order", "id", prediction_column}.issubset(predictions.columns)
    assert len(gold) == len(predictions)
    assert gold["id"].tolist() == predictions["id"].tolist()
    scored = [
        score_document(parse_labels(gold_value), parse_labels(prediction_value))
        for gold_value, prediction_value in zip(gold["Gold skills"], predictions[prediction_column])
    ]
    return pd.DataFrame(scored).add_prefix(prefix)


def micro_metrics(document_scores: pd.DataFrame, prefix: str) -> dict[str, float | int]:
    """Pool TP/FP/FN across documents and calculate micro metrics."""
    true_positives = int(document_scores[f"{prefix}TP"].sum())
    false_positives = int(document_scores[f"{prefix}FP"].sum())
    false_negatives = int(document_scores[f"{prefix}FN"].sum())
    documents = len(document_scores)
    exact_documents = int(document_scores[f"{prefix}Exact set match"].sum())
    return {
        "Documents": documents,
        "True positives": true_positives,
        "False positives": false_positives,
        "False negatives": false_negatives,
        "Micro precision": safe_divide(true_positives, true_positives + false_positives),
        "Micro recall": safe_divide(true_positives, true_positives + false_negatives),
        "Micro F1": safe_divide(2 * true_positives, 2 * true_positives + false_positives + false_negatives),
        "Exact-set-match documents": exact_documents,
        "Exact-set-match rate": safe_divide(exact_documents, documents),
    }


def paired_bootstrap(document_results: pd.DataFrame, replicates: int = 10_000, seed: int = 20260918) -> pd.DataFrame:
    """Calculate paired document-bootstrap differences for B minus A."""
    rng = np.random.default_rng(seed)
    metric_rows = []
    for _ in range(replicates):
        sample = document_results.iloc[rng.integers(0, len(document_results), len(document_results))]
        system_a = micro_metrics(sample, "System A ")
        system_b = micro_metrics(sample, "System B ")
        metric_rows.append({
            "Micro recall difference": system_b["Micro recall"] - system_a["Micro recall"],
            "Micro F1 difference": system_b["Micro F1"] - system_a["Micro F1"],
            "Exact-set-match-rate difference": system_b["Exact-set-match rate"] - system_a["Exact-set-match rate"],
        })
    differences = pd.DataFrame(metric_rows)
    summary = pd.DataFrame({
        "Metric difference": differences.columns,
        "Point estimate": [None] * len(differences.columns),
        "95% CI lower": differences.quantile(0.025).to_numpy(),
        "95% CI upper": differences.quantile(0.975).to_numpy(),
    })
    return summary
