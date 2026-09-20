# Annotation Guidelines

## Purpose

This document describes the protocol used to create the frozen gold labels for the 100-document held-out evaluation set.

## Annotation unit

Each row represents one complete English job description. The annotation target is the set of in-scope canonical technical concepts explicitly mentioned or unambiguously represented anywhere in the full description.

## Label inventory

The final gold inventory is closed: annotations may use only the 20 canonical labels in `config/lexicon_final_20.json`.

## Evidence rule

Assign a canonical label when the full job-description text contains explicit evidence for that in-scope technical concept or an unambiguous accepted representation of it. Read the whole description rather than relying on job title, section heading, or a single local fragment.

## Important exclusions

Do not annotate:

- A skill inferred only from the job title.
- A technology merely implied by a related role or product.
- An out-of-scope concept not in the frozen 20-label inventory.
- A concept based only on a vague, ambiguous, or non-technical word.

The project does not distinguish whether a technical concept is required, preferred, used internally, or mentioned as contextual background. The criterion is full-document technical mention within the fixed inventory.

## `none` policy

Use `none` only when no in-scope canonical concept is supported anywhere in the complete description. It does not mean that the job description has no technical content; it means that none of the 20 selected labels is supported under this protocol.

## Uncertainty policy

Flag an item for review when the annotator cannot determine whether the evidence supports a canonical label under the frozen scope. Resolve flagged cases before final freeze. The released final file must contain only complete annotations with no unresolved review-needed rows.

## Process summary

1. A 10-document pilot was annotated and reviewed.
2. The final held-out set of 100 documents was annotated one document at a time using a custom interface.
3. Structural checks verified identifier alignment, allowed labels, label uniqueness, status consistency, and completion.
4. The final gold file was frozen before final system scoring.

## Limitation

The final gold set was created by one annotator. Inter-annotator agreement is therefore not available and is reported as a limitation.

## Public repository behavior

The standard reproduction workflow reads `data/gold_annotation_final.csv` as a frozen reference. It does not expose a public action that can overwrite this official file. Any future practice-mode annotation writes only to a separate user-owned output file and represents a new annotation exercise, not the published gold standard.
