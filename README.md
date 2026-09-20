# Alias-Aware Technical-Skill Extraction

Reproducible evaluation of alias-aware lexicon matching for technical-skill extraction from English job descriptions.

## Project status

This repository is being prepared as the public reproducibility companion to an NLP research poster. The final release will provide a clean, repository-relative workflow that reproduces the reported comparison between:

- **System A:** canonical-form matching only
- **System B:** the same canonical forms plus 13 reviewed aliases

The default reproduction route will use frozen, version-controlled artifacts and will not require Google Drive or manual re-annotation.

## Planned quick start

The final public release will identify `notebooks/04_final_evaluation_and_results.ipynb` as the one-click notebook for reproducing predictions, metrics, tables, and figures.

## Repository status

The repository structure is initialized. Source notebooks, frozen artifacts, results, and final documentation will be added only after they are cleaned, checked, and tested in a fresh Colab runtime.

## Research scope

The project evaluates document-level extraction of a fixed 20-label inventory of technical concepts from selected English data-related IT job descriptions. It is a transparent lexicon-based comparison, not a trained NER, transformer, or LLM benchmark.

## Licence and data

Code and repository documentation will be released under a stated licence. Dataset-derived files will include source, licence, provenance, and redistribution notes before the repository is made public.
