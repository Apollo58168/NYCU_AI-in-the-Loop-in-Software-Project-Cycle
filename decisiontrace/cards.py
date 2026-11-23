"""Decision card model and the deterministic verbatim-quote check.

This file is the shared contract between modules A-D. Change it only through a
PR that the whole team has agreed on.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

UNKNOWN = "unknown"

CONFIDENCE_LEVELS = ("low", "medium", "high")
STATUSES = ("draft", "approved", "rejected", "needs_author")


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Card:
    decision: str
    reason: str
    verbatim_quote: str
    alternatives: list[str]
    confidence: str  # one of CONFIDENCE_LEVELS
    source: str
    author: str
    drafted_by: str  # "mock" or the LLM model name
    status: str = "draft"  # one of STATUSES
    reviewer: str | None = None
    warnings: list[str] = field(default_factory=list)
    id: str = field(default_factory=_new_id)
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Card:
        return cls(**data)


def check_quote(card: Card, source_text: str) -> Card:
    """Make sure the card's quote really appears in the source.

    A quote that is not an exact substring of `source_text` is replaced with
    UNKNOWN, a warning is added, and confidence drops to "low". An empty quote
    becomes UNKNOWN. This runs in plain code after every draft, so neither the
    mock nor an LLM can attach an invented quote to a card.
    """
    quote = card.verbatim_quote.strip()
    if not quote:
        card.verbatim_quote = UNKNOWN
    elif quote != UNKNOWN and quote not in source_text:
        card.verbatim_quote = UNKNOWN
        card.confidence = "low"
        card.warnings.append(
            "The drafted quote was not found word for word in the source, "
            "so it was replaced with 'unknown'."
        )
    return card
