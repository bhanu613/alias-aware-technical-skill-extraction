"""Reproduce the final System A versus System B analysis from frozen files."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation import micro_metrics, paired_bootstrap, parse_labels, score_predictions
from src.figures import plot_recovery_by_label, plot_residual_errors, plot_system_comparison
from src.matcher import SkillMatcher, load_lexicon, run_safety_tests
from src.paths import CONFIG_DIR, DATA_DIR, FIGURE_OUTPUT_DIR, RESULTS_DIR, RUNTIME_OUTPUT_DIR, ensure_runtime_directories


def prediction_table(evaluation_data: pd.DataFrame, predictions: list[list[str]], column_name: str) -> pd.DataFrame:
    table = evaluation_data[["Annotation order", "id", "Position"]].copy()
    table[column_name] = [";".join(labels) if labels else "none" for labels in predictions]
    table[f"{column_name} count"] = [len(labels) for labels in predictions]
    return table


def per_label_table(document_results: pd.DataFrame, canonical_labels: set[str]) -> pd.DataFrame:
    rows = []
    for label in sorted(canonical_labels):
        counts = {}
        for system in ("System A", "System B"):
            for outcome in ("TP", "FP", "FN"):
                counts[f"{system} {outcome}"] = sum(
                    label in parse_labels(value)
                    for value in document_results[f"{system} {outcome} labels"]
                )
        support = counts["System A TP"] + counts["System A FN"]
        recovered = counts["System A FN"] - counts["System B FN"]
        rows.append(
            {
                "Canonical label": label,
                "Gold support": support,
                "System A TP": counts["System A TP"],
                "System A FP": counts["System A FP"],
                "System A FN": counts["System A FN"],
                "System B TP": counts["System B TP"],
                "System B FP": counts["System B FP"],
                "System B FN": counts["System B FN"],
                "Recovered by System B": recovered,
            }
        )
    return pd.DataFrame(rows)


def metric_summary(document_results: pd.DataFrame, gold_annotations: pd.DataFrame, system_a: pd.DataFrame, system_b: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    gold_instances = sum(len(parse_labels(value)) for value in gold_annotations["Gold skills"])
    for system_name, scores, predictions in (
        ("System A", micro_metrics(document_results, "System A "), system_a),
        ("System B", micro_metrics(document_results, "System B "), system_b),
    ):
        prediction_column = f"{system_name} predictions"
        predicted_instances = sum(len(parse_labels(value)) for value in predictions[prediction_column])
        summary_rows.append(
            {
                "System": system_name,
                "Documents": scores["Documents"],
                "Gold label instances": gold_instances,
                "Predicted label instances": predicted_instances,
                **scores,
            }
        )
    return pd.DataFrame(summary_rows)


def main() -> None:
    ensure_runtime_directories()

    lexicon = load_lexicon(CONFIG_DIR / "lexicon_final_20.json")
    matcher = SkillMatcher(lexicon)
    canonical_labels = matcher.canonical_labels

    evaluation_data = pd.read_csv(DATA_DIR / "evaluation_100.csv")
    gold_annotations = pd.read_csv(DATA_DIR / "gold_annotation_final.csv")
    safety_cases = pd.read_csv(DATA_DIR / "safety_test_cases.csv")
    integration_results = pd.read_csv(DATA_DIR / "integration_test_results.csv")
    residual_record = pd.read_csv(RESULTS_DIR / "residual_error_decisions.csv")

    assert len(evaluation_data) == 100
    assert len(gold_annotations) == 100
    assert evaluation_data["id"].tolist() == gold_annotations["id"].tolist()
    assert gold_annotations["Annotation status"].eq("complete").all()
    assert canonical_labels == set(lexicon["skills"])

    safety_results = run_safety_tests(matcher, safety_cases)
    assert len(safety_results) == 41
    assert safety_results["Test passes"].all()
    assert len(integration_results) == 6
    assert integration_results["Test passes"].all()

    system_a_lists = evaluation_data["Long Description"].apply(matcher.extract_system_a).tolist()
    system_b_lists = evaluation_data["Long Description"].apply(matcher.extract_system_b).tolist()
    assert all(set(a).issubset(set(b)) for a, b in zip(system_a_lists, system_b_lists))

    system_a = prediction_table(evaluation_data, system_a_lists, "System A predictions")
    system_b = prediction_table(evaluation_data, system_b_lists, "System B predictions")
    assert system_a["id"].tolist() == gold_annotations["id"].tolist()
    assert system_b["id"].tolist() == gold_annotations["id"].tolist()

    scored_a = score_predictions(gold_annotations, system_a, "System A predictions", "System A ")
    scored_b = score_predictions(gold_annotations, system_b, "System B predictions", "System B ")
    document_results = pd.concat(
        [gold_annotations[["Annotation order", "id", "Gold skills"]], system_a[["System A predictions"]], system_b[["System B predictions"]], scored_a, scored_b],
        axis=1,
    )

    summary = metric_summary(document_results, gold_annotations, system_a, system_b)
    expected = {
        "System A": (287, 0, 92, 0.7573, 0.8619, 41, 0.4100),
        "System B": (367, 0, 12, 0.9683, 0.9839, 89, 0.8900),
    }
    for _, row in summary.iterrows():
        true_positives, false_positives, false_negatives, recall, f1, exact_documents, exact_rate = expected[row["System"]]
        assert int(row["True positives"]) == true_positives
        assert int(row["False positives"]) == false_positives
        assert int(row["False negatives"]) == false_negatives
        assert round(row["Micro recall"], 4) == recall
        assert round(row["Micro F1"], 4) == f1
        assert int(row["Exact-set-match documents"]) == exact_documents
        assert round(row["Exact-set-match rate"], 4) == exact_rate

    per_label = per_label_table(document_results, canonical_labels)
    assert int(per_label["Gold support"].sum()) == 379
    assert int(per_label["Recovered by System B"].sum()) == 80
    assert int(residual_record.shape[0]) == 12

    bootstrap = paired_bootstrap(document_results)
    points = {
        "Micro recall difference": 0.9683 - 0.7573,
        "Micro F1 difference": 0.9839 - 0.8619,
        "Exact-set-match-rate difference": 0.8900 - 0.4100,
    }
    bootstrap["Point estimate"] = bootstrap["Metric difference"].map(points)

    system_a.to_csv(RUNTIME_OUTPUT_DIR / "system_a_predictions.csv", index=False)
    system_b.to_csv(RUNTIME_OUTPUT_DIR / "system_b_predictions.csv", index=False)
    safety_results.to_csv(RUNTIME_OUTPUT_DIR / "safety_test_results.csv", index=False)
    document_results.to_csv(RUNTIME_OUTPUT_DIR / "document_level_results.csv", index=False)
    summary.to_csv(RUNTIME_OUTPUT_DIR / "metric_summary.csv", index=False)
    per_label.to_csv(RUNTIME_OUTPUT_DIR / "per_label_metrics.csv", index=False)
    bootstrap.to_csv(RUNTIME_OUTPUT_DIR / "bootstrap_results.csv", index=False)

    plot_system_comparison(summary, FIGURE_OUTPUT_DIR / "figure_1_main_performance_comparison")
    plot_recovery_by_label(per_label, FIGURE_OUTPUT_DIR / "figure_2_alias_recovery_by_label")
    plot_residual_errors(residual_record, FIGURE_OUTPUT_DIR / "figure_3_residual_error_patterns")

    print("Final reproduction completed successfully.")
    print(summary.round(4).to_string(index=False))
    print(f"Runtime outputs: {RUNTIME_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
