"""Table-driven Ask cases on the fixed sample history.

Each row is a question a teammate might ask and the cards the answer must cite,
best first, or [] when the answer must be "No approved decision found.".
The same table can be reused for the evaluation report.
"""

import pytest

from decisiontrace.ask import NO_ANSWER, answer
from decisiontrace.sample_data import sample_cards

CASES = [
    # question, expected card ids (best first)
    ("Why do we use polling?", ["s-poll"]),
    ("Why not WebSockets for the live board?", ["s-poll"]),
    ("Which database do we store data in?", ["s-sqlite"]),
    ("Why not PostgreSQL?", ["s-sqlite"]),
    ("為什麼改用 Streamlit？", ["s-ui"]),
    ("為什麼不用 React？", ["s-ui"]),
    ("When do we freeze features?", ["s-deadline"]),
    # s-sse was rejected and s-auth is still a draft: neither may answer.
    ("Did we switch to server-sent events?", []),
    ("How do users log in with GitHub?", []),
    ("What colour is the logo?", []),
    # Asked by user-testing participants (P1, P2) on 2026-11-25.
    ("What do we use to track bugs?", []),
    ("為什麼即時看板用 polling，不用 WebSockets？", ["s-poll"]),
    ("當初為什麼即時看板用 polling，不用 WebSockets？", ["s-poll"]),
    ("為什麼用 polling 不用 WebSockets？", ["s-poll"]),
]


@pytest.mark.parametrize("question, expected", CASES)
def test_sample_question(question, expected):
    result = answer(question, sample_cards())
    assert result.card_ids == expected
    if not expected:
        assert result.text == NO_ANSWER


def test_every_cited_card_shows_its_id_and_quote():
    cards = {c.id: c for c in sample_cards()}
    result = answer("Why polling instead of WebSockets?", list(cards.values()))
    for card_id in result.card_ids:
        assert f"[{card_id}]" in result.text
        assert f'Quote: "{cards[card_id].verbatim_quote}"' in result.text


def test_unknown_reason_stays_unknown():
    result = answer("When do we freeze features?", sample_cards())
    assert "Reason: unknown" in result.text
    assert 'Quote: "unknown"' in result.text


def test_at_most_three_sources():
    cards = sample_cards()
    for card in cards:
        card.status = "approved"
        card.decision = f"{card.decision} for the live board"
    assert len(answer("live board", cards).card_ids) == 3


def test_one_shared_word_does_not_pull_in_a_weak_match():
    # "board" is in s-poll (best, 3 shared tokens) and nowhere else strong;
    # s-sqlite shares only "data" and must not be cited.
    result = answer("polling live board data", sample_cards())
    assert result.card_ids == ["s-poll"]


def test_cited_cards_show_when_they_were_drafted():
    # Two approved cards can match the same question when one replaced the
    # other; the date lets the reader see which one is newer.
    result = answer("Why do we use polling?", sample_cards())
    assert "[s-poll] Use polling every 10 seconds for the live board (drafted 2026-10-02)" in result.text

