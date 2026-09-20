# Method Decisions

## Research question

> How much and at what cost does alias-aware matching improve the precision, recall, and F1 score of a lexicon-based technical-skill extractor compared with strict canonical matching?

## Scope

The task is document-level extraction of a fixed inventory of 20 canonical technical concepts explicitly mentioned or unambiguously represented anywhere in the complete job-description text. It is not applicant-requirement extraction, candidate ranking, exhaustive skill discovery, or a trained NER/transformer/LLM comparison.

## Controlled systems

| System | Matching rule | Output |
|---|---|---|
| System A | 20 canonical forms only | Canonical labels |
| System B | The same canonical forms plus 13 reviewed aliases | The same canonical labels |

Both systems share full-description input, Unicode/case/whitespace normalisation, regex boundary policy, extraction framework, held-out documents, gold labels, and scoring logic. The only intended difference is alias inclusion.

## Frozen inventory

The final inventory contains 20 canonical labels. System B adds the following 13 reviewed aliases:

```text
aws → amazon web services
gcp → google cloud platform
postgres → postgresql
mongo → mongodb
spark → apache spark
pyspark → apache spark
kafka → apache kafka
airflow → apache airflow
k8s → kubernetes
powerbi → power bi
sklearn → scikit-learn
ml → machine learning
nlp → natural language processing
```

Candidate aliases were identified and audited using only the development subset. Coverage counts and reviewed contexts informed decisions about technical equivalence, extraction value, ambiguity, and redundancy. The accepted alias set was frozen before held-out scoring.

## Matching policy

The matcher normalises Unicode/case/whitespace and uses safe regex boundaries. Ordinary hyphens are preserved. Candidate strings directly attached to an ordinary hyphen are blocked under the frozen conservative policy. This prevents some false positives but also explains a small number of documented residual false negatives.

## Evaluation

Gold labels and predictions are compared as sets for each document. Metrics are pooled across all document-label decisions:

- Micro precision: TP / (TP + FP)
- Micro recall: TP / (TP + FN)
- Micro F1: 2TP / (2TP + FP + FN)
- Exact-set-match rate: documents for which the predicted label set exactly equals the gold label set

The final analysis uses a paired non-parametric document bootstrap with 10,000 replicates, seed `20260918`, and percentile 95% confidence intervals.

## Methodological boundaries

The final lexicon, final gold annotations, source evaluation set, matching policy, and published results are frozen artifacts. The normal public reproduction workflow may validate and read them, but must not overwrite them.
