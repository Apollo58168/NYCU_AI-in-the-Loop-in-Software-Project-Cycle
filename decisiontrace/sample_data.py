"""A fixed sample team history for demos and user-testing sessions (module C).

Every session can start from the same known state: a few approved decisions to
ask about, one draft waiting for review, and one rejected card that must never
be used as an answer. The discussion text is the kind of thread a team would
paste into the Draft tab.
"""

from __future__ import annotations

from .cards import Card

SAMPLE_DISCUSSION = (
    "Alice: The live board keeps freezing behind the school proxy.\n"
    "Bob: We decided to use polling every 10 seconds instead of WebSockets. "
    "Because WebSockets kept dropping behind the school reverse proxy.\n"
    "Carol: OK, and the TA said polling is fine for the demo."
)


def _card(card_id, decision, reason, quote, alternatives, status, author, reviewer, created_at):
    return Card(
        id=card_id,
        decision=decision,
        reason=reason,
        verbatim_quote=quote,
        alternatives=alternatives,
        confidence="medium",
        source="sample team history",
        author=author,
        drafted_by="sample",
        status=status,
        reviewer=reviewer,
        created_at=created_at,
    )


def sample_cards() -> list[Card]:
    """Fresh copies of the sample cards (callers may change them)."""
    return [
        _card(
            "s-poll", "Use polling every 10 seconds for the live board",
            "WebSockets kept dropping behind the school reverse proxy",
            "Because WebSockets kept dropping behind the school reverse proxy.",
            ["WebSockets"], "approved", "Bob", "Alice", "2026-10-02T09:00:00+00:00",
        ),
        _card(
            "s-sqlite", "Store the data in SQLite",
            "No database server to run for a class project",
            "SQLite means no database server to run for a class project.",
            ["PostgreSQL"], "approved", "Carol", "Bob", "2026-10-05T09:00:00+00:00",
        ),
        _card(
            "s-ui", "改用 Streamlit 做介面",
            "因為四個人都會 Python",
            "因為四個人都會 Python，不用再學前端框架。",
            ["React"], "approved", "Dave", "Carol", "2026-10-09T09:00:00+00:00",
        ),
        _card(
            "s-deadline", "Freeze features one week before the demo",
            "unknown",
            "unknown",
            [], "approved", "Alice", "Dave", "2026-10-20T09:00:00+00:00",
        ),
        _card(
            "s-sse", "Switch the live board from polling to server-sent events",
            "Polling every 10 seconds made the board feel slow",
            "Polling every 10 seconds made the board feel slow in the demo.",
            ["Polling", "WebSockets"], "rejected", "Bob", "Carol", "2026-11-01T09:00:00+00:00",
        ),
        _card(
            "s-auth", "Log in with GitHub accounts",
            "Everyone already has a GitHub account",
            "Everyone already has a GitHub account.",
            ["Email and password"], "draft", "Carol", None, "2026-11-10T09:00:00+00:00",
        ),
    ]
