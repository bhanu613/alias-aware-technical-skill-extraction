## Terminology

* **Document / Job Posting:** A single text unit, in this case, an IT job advertisement.
* **Djinni Recruitment Dataset:** The specific public dataset of IT job descriptions used as raw data.
* **UUID-hash bucket allocation:** A deterministic method for assigning data records to subsets using their unique ID hashes.
* **Development set:** Data used for designing the lexicon and rules, not for final evaluation.
* **Held-out evaluation subset:** Unseen data used only for final, unbiased performance evaluation.
* **Lexicon-based technical-skill extraction:** Identifying skills in text using a predefined list of terms.
* **Rule-based system:** An extraction method that uses explicit, predefined linguistic rules.
* **Canonical forms:** The standardized, official names for technical skills (e.g., 'machine learning').
* **Aliases:** Alternate names or abbreviations for canonical forms (e.g., 'ML' for 'machine learning').
* **Normalisation policy:** Rules for standardizing text (e.g., lowercasing) before skill extraction.
* **Boundary policy:** Rules defining exact word boundaries for skill matching (e.g., 'git' not matching 'github').
* **Candidate pool:** An initial, provisional list of potential technical skills and their observed forms.
* **Lexicon freeze:** The process of finalizing the set of canonical forms, accepted aliases, and matching rules.
* **System A:** The baseline extractor that identifies only canonical forms.
* **System B:** The alias-aware extractor that identifies canonical forms and their accepted aliases.
* **Safety-test specification / Safety cases:** Fixed examples used to verify that the extraction systems behave as expected.
* **Multi-skill integration safety tests:** Specific tests to ensure extractors correctly handle multiple skills within a single text.
* **Gold annotation / Gold labels:** Human-created, ground-truth labels indicating the presence of skills in evaluation data.
* **Prediction files:** Output files containing the skills extracted by System A and System B for the evaluation dataset.
* **Micro-averaged scoring:** An evaluation approach where metrics (TP, FP, FN) are summed across all documents before calculating overall precision, recall, and F1.
* **True Positives (TP):** Skill instances correctly identified by the system that are also in the gold labels.
* **False Positives (FP):** Skill instances identified by the system that are not present in the gold labels.
* **False Negatives (FN):** Skill instances present in the gold labels that were missed by the system.
* **Micro precision:** The proportion of correctly identified skills among all skills identified by the system.
* **Micro recall:** The proportion of correctly identified skills among all actual skills in the gold data.
* **Micro F1:** The harmonic mean of micro precision and micro recall, balancing both metrics.
* **Exact-set-match rate:** The percentage of documents where the system's predicted set of skills precisely matches the gold set.
* **Per-label performance analysis:** A breakdown of evaluation metrics (TP, FP, FN, P, R, F1) for each individual canonical skill label.
* **System A miss, System B recovery:** Analysis tracking gold labels missed by System A that System B successfully identified due to alias expansion.
* **Residual false negatives:** Gold labels that remain unidentified even after System B's alias expansion.
* **Paired bootstrap confidence intervals:** A statistical technique for estimating the uncertainty range of performance differences between two systems on the same dataset.
* **Bootstrap replicates:** Multiple resamples with replacement of the original dataset used to generate a distribution of a statistic (e.g., performance difference) for confidence interval estimation.
