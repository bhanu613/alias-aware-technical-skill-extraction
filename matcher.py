"""Frozen lexicon matcher used by System A and System B."""

from pathlib import Path

import json
import re
import unicodedata


def loadLexicon(lexiconPath):
    """Load the frozen lexicon JSON file."""

    with Path(lexiconPath).open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def validateLexicon(finalLexicon):
    """Verify the frozen 20-label and 13-alias specification."""

    skills = finalLexicon["skills"]

    canonicalLabels = set(
        skills.keys()
    )

    aliasCount = sum(
        len(details["aliases"])
        for details in skills.values()
    )

    assert len(canonicalLabels) == 20, (
        f"Expected 20 canonical labels, "
        f"found {len(canonicalLabels)}."
    )

    assert aliasCount == 13, (
        f"Expected 13 approved aliases, "
        f"found {aliasCount}."
    )

    return skills, canonicalLabels, aliasCount


def normaliseText(text):
    """Apply the frozen text normalisation policy."""

    text = unicodedata.normalize(
        "NFKC",
        str(text)
    )

    text = text.lower()

    text = text.replace(
        "’",
        "'"
    ).replace(
        "‘",
        "'"
    )

    text = re.sub(
        r"[–—]", 
        "-", 
        text
    )
  
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def termPattern(term):
    """Build the frozen boundary-safe pattern for one form."""

    escapedTerm = re.escape(
        term.lower().strip()
    )

    escapedTerm = escapedTerm.replace(
        r"\ ",
        r"\s+"
    )

    leftBoundary = r"(?<![A-Za-z0-9+#&_.\-])"

    rightBoundary = r"(?![A-Za-z0-9+#&_\-])"

    return re.compile(
        leftBoundary
        + escapedTerm
        + rightBoundary
    )


def extractSkills(
    text,
    skills,
    includeAliases=False
):
    """Return sorted canonical labels found in one text."""

    normalisedText = normaliseText(
        text
    )

    foundLabels = set()

    for canonicalLabel, details in skills.items():

        formsToSearch = [
            canonicalLabel
        ]

        if includeAliases:
            formsToSearch.extend(
                details["aliases"]
            )

        for form in formsToSearch:

            pattern = termPattern(
                form
            )

            if pattern.search(
                normalisedText
            ):
                foundLabels.add(
                    canonicalLabel
                )

                break

    return sorted(
        foundLabels
    )


def extractSystemA(
    text,
    skills
):
    """System A: canonical forms only."""

    return extractSkills(
        text,
        skills,
        includeAliases=False
    )


def extractSystemB(
    text,
    skills
):
    """System B: canonical forms plus approved aliases."""

    return extractSkills(
        text,
        skills,
        includeAliases=True
    )
