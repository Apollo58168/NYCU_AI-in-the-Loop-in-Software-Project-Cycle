"""Which cards count as the team's approved decisions (module A)."""

from __future__ import annotations

from .cards import Card


def approved_cards(cards: list[Card]) -> list[Card]:
    """Approved cards only, newest first (by when the card was drafted)."""
    approved = [c for c in cards if c.status == "approved"]
    return sorted(approved, key=lambda c: c.created_at, reverse=True)
