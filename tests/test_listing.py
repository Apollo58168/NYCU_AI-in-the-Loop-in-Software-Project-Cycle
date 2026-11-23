from streamlit.testing.v1 import AppTest

from decisiontrace import store
from decisiontrace.cards import Card
from decisiontrace.listing import approved_cards


def _card(card_id, status, created_at):
    return Card(
        decision=f"Decision {card_id}", reason="unknown", verbatim_quote="unknown",
        alternatives=[], confidence="low", source="chat", author="Alice",
        drafted_by="mock", status=status, reviewer="Bob", id=card_id,
        created_at=created_at,
    )


CARDS = [
    _card("old", "approved", "2026-11-20T10:00:00+00:00"),
    _card("draft", "draft", "2026-11-23T10:00:00+00:00"),
    _card("new", "approved", "2026-11-22T10:00:00+00:00"),
    _card("rejected", "rejected", "2026-11-23T11:00:00+00:00"),
    _card("needs", "needs_author", "2026-11-23T12:00:00+00:00"),
]


def test_only_approved_cards_newest_first():
    assert [c.id for c in approved_cards(CARDS)] == ["new", "old"]


def test_no_cards():
    assert approved_cards([]) == []


def _cards_tab(tmp_path, monkeypatch, cards):
    path = tmp_path / "cards.json"
    store.save(cards, path)
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    assert not at.exception
    return at.tabs[3]


def test_tab_lists_only_approved_cards(tmp_path, monkeypatch):
    tab = _cards_tab(tmp_path, monkeypatch, CARDS)
    text = " ".join(m.value for m in tab.markdown)
    assert "Decision new" in text and "Decision old" in text
    assert "Decision draft" not in text and "Decision rejected" not in text


def test_tab_empty_state(tmp_path, monkeypatch):
    tab = _cards_tab(tmp_path, monkeypatch, [_card("draft", "draft", "2026-11-23T10:00:00+00:00")])
    assert tab.info[0].value == "No approved cards yet."
