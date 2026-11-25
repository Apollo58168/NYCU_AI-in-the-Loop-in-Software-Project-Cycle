"""Draft a decision card from pasted text (module D).

This is the MOCK drafter: keyword rules, no AI. It looks for the first
sentence with a decision marker and a reason marker in that sentence or the
next one, and takes the quote straight from the text, so the quote is always
verbatim. Module D's
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


def _marker_pattern(markers: tuple[str, ...]) -> re.Pattern[str]:
    """Match English markers as whole words, so "undecided" and "disagreed"
    do not count as "decided" and "agreed". Chinese has no spaces between
    words, so Chinese markers still match anywhere."""
    parts = [
        rf"(?<![a-z]){re.escape(m)}(?![a-z])" if m.isascii() else re.escape(m)
        for m in markers
    ]
    return re.compile("|".join(parts), re.IGNORECASE)


_DECISION = _marker_pattern(DECISION_MARKERS)
_REASON = _marker_pattern(REASON_MARKERS)


def _reason_for(sentences: list[str], index: int) -> str | None:
    """The reason for the decision at `index`, or None if the text gives none.

    Only the decision sentence itself, or the sentence right after it, can
    hold the reason. The next sentence counts only if it does not state a
    decision of its own, so a reason for another decision, or a "because"
    earlier in the text, is never attached to this one (#17).
    """
    if _REASON.search(sentences[index]):
        return sentences[index]
    if index + 1 < len(sentences):
        following = sentences[index + 1]
        if _REASON.search(following) and not _DECISION.search(following):
            return following
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
    has low confidence and a NO_DECISION warning; review() will not approve it.
    The reason comes only from the decision's own sentence or the one right
    after it; more than one decision adds a warning. check_quote() always runs
    last.
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
    decision_indexes = [i for i, s in enumerate(sentences) if _DECISION.search(s)]
    decision = sentences[decision_indexes[0]] if decision_indexes else None
    reason = _reason_for(sentences, decision_indexes[0]) if decision_indexes else None
    if len(decision_indexes) > 1:
        warnings.append(
            f"The text states {len(decision_indexes)} decisions; only the first was "
            "drafted. Paste one discussion per decision."
        )

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
