"""Frozen lexicon-based matching used by Systems A and B."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def normalise_text(text: object) -> str:
    """Apply the frozen Unicode, case, hyphen, and whitespace policy."""
    normalised = unicodedata.normalize("NFKC", str(text))
    normalised = normalised.lower()
    normalised = normalised.replace("’", "'").replace("`", "'")
    normalised = re.sub(r"\s*-\s*", "-", normalised)
    normalised = re.sub(r"\s+", " ", normalised)
    return normalised.strip()


def term_pattern(term: str) -> re.Pattern[str]:
    """Build the frozen safe boundary pattern for one form or alias."""
    escaped_term = re.escape(term.lower().strip())
    escaped_term = escaped_term.replace(r"\-", r"[- ]")
    left_boundary = r"(?<![A-Za-z0-9.-])"
    right_boundary = r"(?![A-Za-z0-9-])"
    return re.compile(left_boundary + escaped_term + right_boundary)


def load_lexicon(path: str | Path) -> dict[str, Any]:
    """Load and validate the frozen 20-label / 13-alias lexicon."""
    with Path(path).open("r", encoding="utf-8") as file:
        lexicon = json.load(file)
    skills = lexicon["skills"]
    alias_count = sum(len(details["aliases"]) for details in skills.values())
    assert len(skills) == 20, "The frozen lexicon must contain 20 canonical labels."
    assert alias_count == 13, "The frozen lexicon must contain 13 approved aliases."
    return lexicon


class SkillMatcher:
    """Shared extractor: System A excludes aliases; System B includes them."""

    def __init__(self, lexicon: dict[str, Any]):
        self.lexicon = lexicon
        self.skills = lexicon["skills"]
        self.canonical_labels = set(self.skills)

    def extract(self, text: object, include_aliases: bool = False) -> list[str]:
        normalised = normalise_text(text)
        found_labels: set[str] = set()
        for canonical_label, details in self.skills.items():
            forms = [canonical_label]
            if include_aliases:
                forms.extend(details["aliases"])
            for form in forms:
                if term_pattern(form).search(normalised):
                    found_labels.add(canonical_label)
                    break
        return sorted(found_labels)

    def extract_system_a(self, text: object) -> list[str]:
        """System A: strict canonical-form matching only."""
        return self.extract(text, include_aliases=False)

    def extract_system_b(self, text: object) -> list[str]:
        """System B: canonical forms plus approved aliases."""
        return self.extract(text, include_aliases=True)


def run_safety_tests(matcher: SkillMatcher, safety_cases):
    """Evaluate the frozen single-target safety-test table."""
    results = safety_cases.copy()
    results["System A predictions"] = results["text"].apply(matcher.extract_system_a)
    results["System B predictions"] = results["text"].apply(matcher.extract_system_b)
    results["System A observed"] = results.apply(
        lambda row: row["Canonical label"] in row["System A predictions"], axis=1
    )
    results["System B observed"] = results.apply(
        lambda row: row["Canonical label"] in row["System B predictions"], axis=1
    )
    results["System A passes"] = results["System A observed"] == results["Expected System A"]
    results["System B passes"] = results["System B observed"] == results["Expected System B"]
    results["Test passes"] = results["System A passes"] & results["System B passes"]
    return results
