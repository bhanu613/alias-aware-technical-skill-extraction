# Data Card

## Source dataset

This project uses the English job-description portion of the Djinni Recruitment Dataset, distributed through Hugging Face as `lang-uk/recruitment-dataset-job-descriptions-english`.

- Source snapshot used in the private research workflow: commit `b56a6054c10f1266a141e37c8df66c79ff2863af`
- Dataset scope: anonymized English IT job descriptions from the Djinni platform
- Dataset licence reported by the source repository: MIT
- Dataset paper: *Introducing the Djinni Recruitment Dataset: A Corpus of Anonymized Candidate Profiles and Job Descriptions* (2024)

The raw upstream dataset is not copied into this repository. The final repository will include only the project-specific, documented subsets needed for transparent method review and exact final-result reproduction.

## Target population

The study restricts the source corpus to selected English data-related IT job postings in four role families:

- Data Science
- Data Analyst
- Data Engineer
- Python

This is a bounded study population, not a claim about every job advertisement, occupation, language, or labour market.

## Data preparation

The private master workflow applied deterministic filtering and splitting:

1. Keep the four target role families.
2. Keep declared English records.
3. Remove records with missing identifiers or text.
4. Remove substantially non-English/bilingual records using a Cyrillic-character-ratio check.
5. Retain descriptions between 500 and 4,000 characters.
6. Remove exact duplicate text.
7. Sort by stable identifier and assign deterministic MD5 buckets.
8. Build development and evaluation subsets with employer-disjointness safeguards.

The resulting filtered pool contained 9,222 postings. The final research subsets contain 200 development documents and 100 held-out evaluation documents. Employer overlap between these subsets was zero.

## Repository data policy

| Item | Planned location | Purpose |
|---|---|---|
| `development_200.csv` | `data/` | Evidence for lexicon-development documentation |
| `development_review_32_ids.csv` | `data/` | Manifest for balanced structured review |
| `evaluation_100.csv` | `data/` | Fixed held-out input for exact final-result reproduction |
| `gold_annotation_final.csv` | `data/` | Frozen gold labels used for published scoring |
| Final lexicon | `config/` | Frozen labels and aliases used by both systems |

## Privacy and responsible use

The dataset is described by its provider as anonymized. This project concerns technical-concept mentions in job-description text; it does not infer applicant suitability, person-level attributes, or hiring decisions.

## Citation

The final public README and appendix will provide the complete bibliographic citation, dataset URL, licence information, and pinned-revision retrieval instructions.
