"""Human review of drafted decision cards (module B).

A card becomes part of the team's decision log only when a teammate other than
its author approves it here. This is plain code, no AI.
"""

from __future__ import annotations

from .cards import UNKNOWN, Card

# action -> the status the card gets
_ACTIONS = {"approve": "approved", "reject": "rejected"}


def review(card: Card, reviewer: str, action: str, edits: dict | None = None) -> Card:
    """Approve or reject a draft card; raise ValueError when that is not allowed.

    The card is changed in place and returned, like check_quote().
    """
    reviewer = (reviewer or "").strip()
    if not reviewer:
        raise ValueError("Please enter your name as the reviewer.")
    if reviewer.casefold() == card.author.strip().casefold():
        raise ValueError("You wrote this card, so a teammate has to review it.")
    if card.status != "draft":
        raise ValueError(f"Only draft cards can be reviewed; this card is '{card.status}'.")
    if action not in _ACTIONS:
        raise ValueError(f"Unknown review action: {action!r}.")
    if edits:
        # shortcut: edits arrive with "edit_approve" in module B's PR 2.
        raise ValueError("Editing a card during review is not supported yet.")

    if action == "approve" and card.decision.strip() in ("", UNKNOWN):
        raise ValueError("This card has no decision, so it cannot be approved. Reject it instead.")

    card.status = _ACTIONS[action]
    card.reviewer = reviewer
    return card
