"""Draft a decision card from pasted text (module D).

This is the MOCK drafter: keyword rules, no AI. It looks for the first
sentence with a decision marker and the first with a reason marker, and takes
the quote straight from the text, so the quote is always verbatim. Module D's
second PR replaces the body with a Claude API call behind the same signature.
"""

from __future__ import annotations

import re

from .cards import UNKNOWN, Card, check_quote

MOCK = "mock"
MAX_CHARS = 8000
NO_DECISION = "No decision found in the text."

DECISION_MARKERS = (
    "decided", "we will", "we'll", "let's", "going with", "agreed",
    "決定", "改用", "就用",
)
REASON_MARKERS = ("because", "since", "so that", "因為", "由於")
ALTERNATIVE_MARKERS = ("instead of", "rather than", "而不是")

# A sentence ends at . ! ? ; (ASCII or full-width) or a line break.
_SENTENCE_END = re.compile(r"(?<=[.!?;。！？；])\s*|\n+")
# An alternative runs from its marker to the next comma or sentence end.
_ALTERNATIVE = re.compile(
    "(?:" + "|".join(re.escape(m) for m in ALTERNATIVE_MARKERS) + r")\s*([^,，、.!?;。！？；\n]+)",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    """Split on English and Chinese sentence punctuation and line breaks."""
    return [s.strip() for s in _SENTENCE_END.split(text) if s.strip()]


def _first_with(sentences: list[str], markers: tuple[str, ...]) -> str | None:
    for sentence in sentences:
        lower = sentence.lower()
        if any(m in lower for m in markers):
            return sentence
    return None


def _alternatives(text: str) -> list[str]:
    found: list[str] = []
    for match in _ALTERNATIVE.finditer(text):
        alt = match.group(1).strip()
        if alt and alt not in found:
            found.append(alt)
    return found


def draft_card(source_text: str, author: str, source: str = "pasted text") -> Card:
    """Return a draft card for the discussion in `source_text`.

    Raises ValueError for empty text. Text longer than MAX_CHARS is cut and the
    card gets a warning. With no decision marker the decision is UNKNOWN, the card
    has low confidence and a NO_DECISION warning; review() will not approve it. check_quote() always runs last.
    """
    text = (source_text or "").strip()
    if not text:
        raise ValueError("Please paste the discussion to draft from.")

    warnings: list[str] = []
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
        warnings.append(
            f"The text was longer than {MAX_CHARS} characters; only the first "
            f"{MAX_CHARS} were used."
        )

    sentences = split_sentences(text)
    decision = _first_with(sentences, DECISION_MARKERS)
    reason = _first_with(sentences, REASON_MARKERS)

    if decision is None:
        warnings.append(NO_DECISION)
        card = Card(
            decision=UNKNOWN,
            reason=UNKNOWN,
            verbatim_quote=UNKNOWN,
            alternatives=[],
            confidence="low",
            source=source,
            author=author,
            drafted_by=MOCK,
            warnings=warnings,
        )
    else:
        card = Card(
            decision=decision,
            reason=reason or UNKNOWN,
            verbatim_quote=reason or decision,
            alternatives=_alternatives(text),
            confidence="medium" if reason else "low",
            source=source,
            author=author,
            drafted_by=MOCK,
            warnings=warnings,
        )
    return check_quote(card, text)
