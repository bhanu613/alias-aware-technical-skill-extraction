"""Print read-only diagnostics for public-result reproduction."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation import parse_labels
from src.matcher import SkillMatcher, load_lexicon
from src.paths import CONFIG_DIR, DATA_DIR


def counts(gold_values, prediction_lists):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    mismatches = []
    for row_number, (gold_value, predictions) in enumerate(zip(gold_values, prediction_lists), start=1):
        gold = parse_labels(gold_value)
        predicted = set(predictions)
        true_positives += len(gold & predicted)
        false_positives += len(predicted - gold)
        false_negatives += len(gold - predicted)
        if gold != predicted:
            mismatches.append((row_number, gold, predicted, gold - predicted, predicted - gold))
    return true_positives, false_positives, false_negatives, mismatches


def main() -> None:
    lexicon = load_lexicon(CONFIG_DIR / "lexicon_final_20.json")
    matcher = SkillMatcher(lexicon)
    evaluation = pd.read_csv(DATA_DIR / "evaluation_100.csv")
    gold = pd.read_csv(DATA_DIR / "gold_annotation_final.csv")

    print("Evaluation columns:", evaluation.columns.tolist())
    print("Gold columns:", gold.columns.tolist())
    print("Evaluation rows:", len(evaluation))
    print("Gold rows:", len(gold))
    print("IDs aligned:", evaluation["id"].tolist() == gold["id"].tolist())
    print("Canonical labels:", len(matcher.canonical_labels))
    print("Approved aliases:", sum(len(item["aliases"]) for item in lexicon["skills"].values()))
    print("Annotation statuses:", gold["Annotation status"].value_counts(dropna=False).to_dict())

    predictions_a = evaluation["Long Description"].apply(matcher.extract_system_a).tolist()
    predictions_b = evaluation["Long Description"].apply(matcher.extract_system_b).tolist()
    for system_name, predictions in (("System A", predictions_a), ("System B", predictions_b)):
        tp, fp, fn, mismatches = counts(gold["Gold skills"], predictions)
        print(f"{system_name} counts: TP={tp}, FP={fp}, FN={fn}")
        print(f"{system_name} exact matches: {len(gold) - len(mismatches)}")
        for row_number, gold_set, predicted_set, missed, extra in mismatches[:10]:
            annotation_order = int(gold.iloc[row_number - 1]["Annotation order"])
            print(
                f"{system_name} mismatch at annotation order {annotation_order}: "
                f"missed={sorted(missed)} extra={sorted(extra)} "
                f"gold={sorted(gold_set)} predicted={sorted(predicted_set)}"
            )


if __name__ == "__main__":
    main()
