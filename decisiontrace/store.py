"""Local JSON storage for decision cards."""

from __future__ import annotations

import json
from pathlib import Path

from .cards import Card

DEFAULT_PATH = Path("data/cards.json")


def load(path: Path = DEFAULT_PATH) -> list[Card]:
    """Return all stored cards; an absent file means no cards yet."""
    if not path.exists():
        return []
    return [Card.from_dict(d) for d in json.loads(path.read_text(encoding="utf-8"))]


def save(cards: list[Card], path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([c.to_dict() for c in cards], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def upsert(card: Card, path: Path = DEFAULT_PATH) -> None:
    """Insert the card, or replace the stored card with the same id."""
    cards = load(path)
    for i, existing in enumerate(cards):
        if existing.id == card.id:
            cards[i] = card
            break
    else:
        cards.append(card)
    save(cards, path)
