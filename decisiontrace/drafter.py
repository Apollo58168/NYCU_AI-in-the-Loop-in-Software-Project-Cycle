"""Draft a decision card from pasted text (module D).

With ANTHROPIC_API_KEY set, Claude drafts the card (see llm.py). Without a
key, the MOCK drafter runs: keyword rules, no AI. It looks for the first
sentence with a decision marker and a reason marker in that sentence or the
next one, and takes the quote straight from the text, so the quote is always
verbatim. Both go through the same card building and check_quote().
"""

from __future__ import annotations

import re

from . import llm
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


NEXT_SENTENCE_REASON = (
    "The reason comes from the sentence after the decision; check that it is "
    "about this decision."
)


def _reason_for(sentences: list[str], index: int) -> tuple[str | None, bool]:
    """The reason for the decision at `index`, and whether it is the next sentence.

    Only the decision sentence itself, or the sentence right after it, can
    hold the reason. The next sentence counts only if it does not state a
    decision of its own, so a reason for another decision, or a "because"
    earlier in the text, is never attached to this one (#17). Keywords cannot
    tell whether the next sentence is really about the decision ("Lunch was
    late because..."), so the caller lowers confidence and warns.
    """
    if _REASON.search(sentences[index]):
        return sentences[index], False
    if index + 1 < len(sentences):
        following = sentences[index + 1]
        if _REASON.search(following) and not _DECISION.search(following):
            return following, True
    return None, False


def _alternatives(text: str) -> list[str]:
    found: list[str] = []
    for match in _ALTERNATIVE.finditer(text):
        alt = match.group(1).strip()
        if alt and alt not in found:
            found.append(alt)
    return found


def _mock_fields(text: str, warnings: list[str]) -> dict:
    """The card fields the keyword rules find in `text`."""
    sentences = split_sentences(text)
    decision_indexes = [i for i, s in enumerate(sentences) if _DECISION.search(s)]
    if not decision_indexes:
        return {
            "decision": UNKNOWN,
            "reason": UNKNOWN,
            "verbatim_quote": UNKNOWN,
            "alternatives": [],
            "confidence": "low",
        }
    decision = sentences[decision_indexes[0]]
    reason, from_next = _reason_for(sentences, decision_indexes[0])
    if from_next:
        warnings.append(NEXT_SENTENCE_REASON)
    if len(decision_indexes) > 1:
        warnings.append(
            f"The text states {len(decision_indexes)} decisions; only the first was "
            "drafted. Paste one discussion per decision."
        )
    return {
        "decision": decision,
        "reason": reason or UNKNOWN,
        "verbatim_quote": reason or decision,
        "alternatives": _alternatives(text),
        "confidence": "medium" if reason and not from_next else "low",
    }


def _is_unknown(value: str) -> bool:
    # Claude may write "Unknown" or "UNKNOWN"; all of them mean the field is empty.
    return value.strip().casefold() == UNKNOWN


def _to_card(fields: dict, author: str, source: str, drafted_by: str, warnings: list[str]) -> Card:
    """Build the card the same way for the MOCK and for Claude."""
    fields = {
        **fields,
        **{k: UNKNOWN for k in ("decision", "reason", "verbatim_quote") if _is_unknown(fields[k])},
    }
    if fields["decision"] == UNKNOWN:
        # The form from #26: review() refuses to approve a card whose decision is UNKNOWN.
        warnings.append(NO_DECISION)
        return Card(
            decision=UNKNOWN,
            reason=UNKNOWN,
            verbatim_quote=UNKNOWN,
            alternatives=[],
            confidence="low",
            source=source,
            author=author,
            drafted_by=drafted_by,
            warnings=warnings,
        )
    # A card without a stated reason is never more than low confidence.
    confidence = "low" if fields["reason"] == UNKNOWN else fields["confidence"]
    return Card(
        decision=fields["decision"],
        reason=fields["reason"],
        verbatim_quote=fields["verbatim_quote"],
        alternatives=fields["alternatives"],
        confidence=confidence,
        source=source,
        author=author,
        drafted_by=drafted_by,
        warnings=warnings,
    )


def draft_card(source_text: str, author: str, source: str = "pasted text") -> Card:
    """Return a draft card for the discussion in `source_text`.

    Raises ValueError for empty text, and llm.DraftError when Claude is set up
    but fails (timeout, rate limit, invalid answer); then no card is made.
    Text longer than MAX_CHARS is cut and the card gets a warning. With no
    decision the decision is UNKNOWN, the card has low confidence and a
    NO_DECISION warning; review() will not approve it. More than one decision
    adds a warning. check_quote() always runs last.
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

    if llm.is_configured():
        fields, drafted_by = llm.draft_fields(text)
        if fields.pop("more_decisions"):
            warnings.append(
                "The text states more than one decision; only the first was "
                "drafted. Paste one discussion per decision."
            )
    else:
        fields, drafted_by = _mock_fields(text, warnings), MOCK
    card = check_quote(_to_card(fields, author, source, drafted_by, warnings), text)
    return _drop_unsupported_reason(card)


def _drop_unsupported_reason(card: Card) -> Card:
    """A reason whose quote is not in the text has no support, so it goes too.

    The MOCK's reason is its quote, but Claude writes the reason in its own
    words; without this, an invented reason could survive check_quote() and be
    approved (CP1 §4: no approved card may have an unsupported reason).
    """
    if card.verbatim_quote == UNKNOWN and card.reason != UNKNOWN:
        card.reason = UNKNOWN
        card.confidence = "low"
        card.warnings.append(
            "The reason was removed because no quote from the source supports it."
        )
    return card
