# Reproducibility

## Goal

The repository supports two complementary goals:

1. **Method transparency:** readers can inspect data preparation, lexicon design, matcher testing, annotation protocol, and evaluation logic.
2. **Result reproducibility:** readers can reproduce the reported System A versus System B results without mounting the author's Google Drive or repeating manual annotation.

## Primary reproduction route

The final public release will identify:

```text
notebooks/04_final_evaluation_and_results.ipynb
```

as the main result-reproduction notebook.

It will load repository-controlled frozen inputs:

```text
data/evaluation_100.csv
data/gold_annotation_final.csv
config/lexicon_final_20.json
src/ matcher and evaluation code
```

It will regenerate predictions, metrics, audits, and figures into a runtime output directory. The default workflow will not write to `data/`, `config/`, or `results/`.

## Colab use

The final README will provide an Open in Colab link for each notebook. A bootstrap cell will clone the repository into the temporary Colab runtime and install dependencies. Readers will not need to upload CSV files manually or mount the author's Drive.

## Notebook roles

| Notebook | Purpose |
|---|---|
| `01_data_preparation_and_lexicon_design.ipynb` | Data provenance, deterministic subset selection, and lexicon-decision evidence |
| `02_system_implementation_and_testing.ipynb` | Matcher implementation plus safety and integration tests |
| `03_gold_annotation_workflow.ipynb` | Annotation protocol, validation, final-freeze explanation, and optional safe demonstration |
| `04_final_evaluation_and_results.ipynb` | One-click reproduction of published results |

Each notebook will load the files it needs and will not rely on variables left in memory by another notebook.

## Expected final metrics

The released reproduction notebook must regenerate the following values from the frozen artifacts:

| Metric | System A | System B |
|---|---:|---:|
| Micro precision | 1.0000 | 1.0000 |
| Micro recall | 0.7573 | 0.9683 |
| Micro F1 | 0.8619 | 0.9839 |
| Exact-set-match rate | 0.4100 | 0.8900 |

The notebook must also reconcile the final counts: 379 gold label instances; 287 System A true positives and 92 false negatives; 367 System B true positives and 12 false negatives.

## Clean-runtime release test

Before public release, test from a fresh Colab runtime:

1. Clone the public repository.
2. Run Notebook 4 top to bottom.
3. Confirm the expected metrics and figures are reproduced.
4. Confirm no frozen artifact changed.
5. Test all README commands and Colab links.
