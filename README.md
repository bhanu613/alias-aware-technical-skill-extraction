# <img width="3755" height="297" alt="image" src="https://github.com/user-attachments/assets/84882ccd-c467-4f0b-8929-7ce35d942f48" />


A reproducible NLP study of whether an alias-aware lexicon improves extraction of canonical technical-skill mentions from English data-related IT job postings.

The project compares two deterministic, rule-based systems on the same independently annotated held-out corpus:

- **System A** matches 20 canonical technical-skill forms only.
- **System B** uses the same matcher, normalisation, and boundary policy, but also recognises 13 approved aliases and maps them back to the same canonical labels.

The central research question is:

> <img width="3027" height="105" alt="image" src="https://github.com/user-attachments/assets/c4b9c25f-6877-472f-a4b4-8db0e6f76a4c" />


## Headline results

Evaluation uses 100 held-out job descriptions, 379 gold label instances, and document-level paired bootstrap resampling with 10,000 replicates. System B increased recall, micro F1, and exact-set-match rate while retaining perfect micro precision on this fixed corpus.


<img width="1426" height="385" alt="image" src="https://github.com/user-attachments/assets/02fe9840-6cb5-4132-9cab-af32ca966d5a" />

| Metric | System A | System B | System B − System A |
|---|---:|---:|---:|
| True positives | 287 | 367 | +80 |
| False positives | 0 | 0 | 0 |
| False negatives | 92 | 12 | −80 |

The paired document-level bootstrap confidence intervals for the System B minus System A difference were:

| Metric difference | Point estimate | 95% percentile confidence interval |
|---|---:|---:|
| Micro recall | +0.2111 | +0.1730 to +0.2494 |
| Micro F1 | +0.1221 | +0.0979 to +0.1473 |
| Exact-set-match rate | +0.4800 | +0.3800 to +0.5800 |

All three intervals are above zero for resampling of this held-out 100-document corpus. They describe uncertainty under document-level resampling of this study corpus; they do not establish performance on every external job-posting dataset.

## Project structure

```text
alias-aware-technical-skill-extraction/
├── README.md
├── requirements.txt
├── matcher.py
│
├── notebooks/
│   ├── 01 Data Preparation and Lexicon Design.ipynb
│   ├── 02 System Implementation and Testing.ipynb
│   ├── 03 Gold Annotation Workflow.ipynb
│   └── 04 Final Evaluation and Results.ipynb
│
├── config/
│   └── LexiconList20_final.json
│
├── data/
│   ├── evaluation100.csv
│   ├── goldAnnotationFinal.csv
│   ├── SafetyTestCases.csv
│   └── IntegrationTestCases.csv
│
└── results/
    ├── SystemAPredictions.csv
    ├── SystemBPredictions.csv
    ├── DocumentEvaluation.csv
    ├── MetricSummary.csv
    ├── PerLabelMetrics.csv
    ├── RecoveryAudit.csv
    ├── ResidualErrorDecisions.csv
    ├── BootstrapResults.csv
    └── figures/
        ├── MainPerformanceComparison.png
        ├── AliasRecoveryByLabel.png
        └── ResidualErrorPatterns.png
```

## Method overview

The study follows a staged design that separates lexicon development, implementation testing, human annotation, and final evaluation.

1. **Data preparation and lexicon design.** Notebook 1 downloads a pinned revision of the public source dataset, applies deterministic filtering, and produces a 200-document development subset and an employer-disjoint 100-document held-out evaluation subset. Only development documents are used to construct the candidate inventory, audit candidate forms, and decide canonical labels and aliases.

2. **Frozen lexicon.** The final lexicon contains 20 canonical technical-skill labels and 13 approved aliases. System A searches canonical forms only. System B searches canonical forms plus approved aliases, but always returns canonical labels.

3. **Implementation and testing.** Notebook 2 imports the shared matcher and validates it against 41 single-target safety tests and 6 multi-skill integration tests. All 47 tests pass.

4. **Independent gold annotation.** Notebook 3 documents the full-document, explicit-evidence annotation protocol used to create the frozen gold labels for the 100 held-out documents. The released gold file is structurally validated and is not modified by the public workflow.

5. **Final evaluation.** Notebook 4 generates both systems' predictions, performs document-level TP/FP/FN scoring, reports aggregate and per-label metrics, audits alias recovery, analyses the 12 residual System B false-negative instances, and estimates uncertainty with a paired bootstrap.

<img width="1512" height="907" alt="image" src="https://github.com/user-attachments/assets/4009e2ed-b6b4-4522-ae24-a73fb5f6ac0b" />


## Reproduce the results

### Requirements

- Python 3
- Git
- Packages listed in [`requirements.txt`](requirements.txt)
- Internet access for the pinned Hugging Face source download in Notebook 1

No Google Drive connection, personal credentials, or editable author files are required for the standard public workflow.

### Option 1: Run locally

```bash
git clone https://github.com/bhanu613/alias-aware-technical-skill-extraction.git
cd alias-aware-technical-skill-extraction
python -m pip install -r requirements.txt
```

Open the notebooks in the following order:

1. [Notebook 1 Data Preparation and Lexicon Design](notebooks/01%20Data%20Preparation%20and%20Lexicon%20Design.ipynb)
2. [Notebook 2 System Implementation and Testing](notebooks/02%20System%20Implementation%20and%20Testing.ipynb)
3. [Notebook 3 Gold Annotation Workflow](notebooks/03%20Gold%20Annotation%20Workflow.ipynb)
4. [Notebook 4 Final Evaluation and Results](notebooks/04%20Final%20Evaluation%20and%20Results.ipynb)

For a quick reproduction of the published results, Notebook 4 is the main evaluation notebook. It independently loads the committed frozen evaluation data, gold annotations, lexicon, and matcher.

### Option 2: Run in Google Colab

Open any notebook in Colab and run it from top to bottom. Each public notebook clones this repository into the temporary Colab runtime when necessary and writes generated files only to a temporary runtime output directory.

The standard workflow does not mount Google Drive and does not write over repository inputs such as `goldAnnotationFinal.csv` or `LexiconList20_final.json`.

## Data provenance

The source corpus is the English job-descriptions component of the [Djinni Recruitment Dataset on Hugging Face](https://huggingface.co/datasets/lang-uk/recruitment-dataset-job-descriptions-english). Notebook 1 uses the pinned dataset revision:

```text
b56a6054c10f1266a141e37c8df66c79ff2863af
```

The deterministic filtering policy retains English postings in the Data Science, Data Analyst, Data Engineer, and Python role families. The procedure produces a filtered corpus of 9,222 postings, a 200-document development subset, and a 100-document held-out evaluation subset.

Please consult the source dataset page for its access conditions, licence information, and citation guidance before reusing source data.

## Frozen artifacts

The following artifacts define the reported experiment and should be treated as read-only:

| Artifact | Role |
|---|---|
| [`config/LexiconList20_final.json`](config/LexiconList20_final.json) | Frozen 20-label inventory, 13 aliases, normalisation policy, and boundary policy |
| [`data/evaluation100.csv`](data/evaluation100.csv) | Fixed held-out 100-document evaluation corpus |
| [`data/goldAnnotationFinal.csv`](data/goldAnnotationFinal.csv) | Human-created frozen gold annotations used for reported scoring |
| [`matcher.py`](matcher.py) | Shared implementation used by both systems |
| [`data/SafetyTestCases.csv`](data/SafetyTestCases.csv) | Fixed single-target safety tests |
| [`data/IntegrationTestCases.csv`](data/IntegrationTestCases.csv) | Fixed multi-skill integration tests |

The normal public workflow may create temporary outputs, but it does not modify these frozen artifacts.

## Result artifacts

The `results/` folder contains the committed outputs produced by the final evaluation workflow:

| File | Contents |
|---|---|
| [`SystemAPredictions.csv`](results/SystemAPredictions.csv) | Canonical predictions from System A |
| [`SystemBPredictions.csv`](results/SystemBPredictions.csv) | Canonical predictions from System B |
| [`DocumentEvaluation.csv`](results/DocumentEvaluation.csv) | Document-level gold/prediction comparison with TP, FP, and FN labels |
| [`MetricSummary.csv`](results/MetricSummary.csv) | Aggregate micro metrics and exact-set-match results |
| [`PerLabelMetrics.csv`](results/PerLabelMetrics.csv) | Per-label support, precision, recall, and F1 |
| [`RecoveryAudit.csv`](results/RecoveryAudit.csv) | System A misses recovered by System B and residual misses |
| [`ResidualErrorDecisions.csv`](results/ResidualErrorDecisions.csv) | Descriptive review of the 12 remaining System B false-negative instances |
| [`BootstrapResults.csv`](results/BootstrapResults.csv) | Paired 10,000-replicate bootstrap metric-difference intervals |

The three figures in [`results/figures/`](results/figures/) summarize main performance, alias recovery, and remaining residual error patterns.

## Interpretation

System B adds aliases without changing the canonical-label inventory, normalisation policy, or boundary policy used by System A. In this corpus, the alias-aware system recovered 80 of System A's 92 false-negative label instances, leaving 12 residual System B false-negative instances across 11 documents.

The residual error analysis is descriptive. It documents limitations of the frozen system, including unapproved lexical variants, conservative hyphen-boundary blocking, indirect related-technology references, and compound or slash-separated expressions. It does not modify the lexicon, matcher, gold labels, or reported metrics.

## Limitations

- The study uses a bounded inventory of 20 technical concepts rather than an open-ended skills taxonomy.
- The gold labels were produced by one annotator; the study does not estimate inter-annotator agreement.
- The evaluation corpus contains 100 held-out English data-related IT job postings, so conclusions should not be generalized automatically to other job markets, languages, role families, or datasets.
- Per-label metrics for sparse labels should be interpreted cautiously.
- The conservative hyphen policy intentionally blocks some attached forms, such as `ML-based`, to reduce overly broad matching risk.
- The study evaluates deterministic lexicon matching, not a learned named-entity-recognition or large-language-model extraction system.

## Reuse and citation

If you reuse or extend this project, retain the provenance of the frozen artifacts and distinguish any changed lexicon, annotation scheme, data split, or matcher policy as a new experiment.

For the source corpus, follow the citation guidance supplied by the original Hugging Face dataset maintainers.
