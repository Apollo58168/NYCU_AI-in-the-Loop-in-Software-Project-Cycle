import pytest
from streamlit.testing.v1 import AppTest

from decisiontrace import store
from decisiontrace.cards import UNKNOWN, Card
from decisiontrace.drafter import NO_DECISION, draft_card
from decisiontrace.review import review


def _card(status="draft", author="Alice"):
    return Card(
        decision="Use uv", reason="It is fast", verbatim_quote="It is fast",
        alternatives=["pip"], confidence="high", source="chat", author=author,
        drafted_by="mock", status=status, id="c1",
    )


@pytest.mark.parametrize("action, status", [("approve", "approved"), ("reject", "rejected")])
def test_review_sets_status_and_reviewer(action, status):
    card = review(_card(), "  Bob ", action)
    assert (card.status, card.reviewer) == (status, "Bob")


@pytest.mark.parametrize("reviewer", ["Alice", " alice ", "ALICE"])
def test_author_cannot_review_own_card(reviewer):
    with pytest.raises(ValueError, match="teammate"):
        review(_card(), reviewer, "approve")


@pytest.mark.parametrize("reviewer", ["", "   ", None])
def test_reviewer_name_required(reviewer):
    with pytest.raises(ValueError, match="reviewer"):
        review(_card(), reviewer, "approve")


@pytest.mark.parametrize("status", ["approved", "rejected", "needs_author"])
def test_only_drafts_can_be_reviewed(status):
    with pytest.raises(ValueError, match="Only draft"):
        review(_card(status=status), "Bob", "approve")


def test_unknown_action_and_edits_refused():
    with pytest.raises(ValueError, match="Unknown"):
        review(_card(), "Bob", "delete")
    with pytest.raises(ValueError, match="not supported"):
        review(_card(), "Bob", "approve", edits={"reason": "x"})


def test_refused_review_leaves_card_unchanged():
    card = _card()
    with pytest.raises(ValueError):
        review(card, "alice", "approve")
    assert (card.status, card.reviewer) == ("draft", None)


def _tab(tmp_path, monkeypatch, reviewer):
    path = tmp_path / "cards.json"
    store.save([_card()], path)
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="review_reviewer").input(reviewer)
    at.button(key="review_approve_c1").click().run()
    assert not at.exception
    return at, path


def test_tab_approves_and_saves(tmp_path, monkeypatch):
    at, path = _tab(tmp_path, monkeypatch, "Bob")
    saved = store.load(path)[0]
    assert (saved.status, saved.reviewer) == ("approved", "Bob")
    assert "approved by Bob" in at.tabs[1].success[0].value


def test_tab_shows_error_when_author_reviews(tmp_path, monkeypatch):
    at, path = _tab(tmp_path, monkeypatch, "alice")
    assert "teammate" in at.tabs[1].error[0].value
    assert store.load(path)[0].status == "draft"


def test_card_without_a_decision_cannot_be_approved_but_can_be_rejected():
    # Group 11 review (#16, F2): chit-chat reached Approved cards.
    card = draft_card("今天午餐好吃", "Alice")
    assert card.decision == UNKNOWN
    with pytest.raises(ValueError, match="no decision"):
        review(card, "Bob", "approve")
    assert card.status == "draft"
    assert review(card, "Bob", "reject").status == "rejected"


def test_card_saved_before_the_fix_with_the_old_no_decision_text_cannot_be_approved():
    # Cards in an existing data/cards.json still carry the old text as their decision.
    card = _card()
    card.decision = NO_DECISION
    with pytest.raises(ValueError, match="no decision"):
        review(card, "Bob", "approve")


def test_tab_reject_message_says_how_to_fix(tmp_path, monkeypatch):
    path = tmp_path / "cards.json"
    store.save([_card()], path)
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="review_reviewer").input("Bob")
    at.button(key="review_reject_c1").click().run()
    assert not at.exception
    message = at.tabs[1].success[0].value
    assert "rejected by Bob" in message
    assert "Draft tab" in message and "another teammate" in message


def test_tab_approve_message_has_no_fix_hint(tmp_path, monkeypatch):
    at, _ = _tab(tmp_path, monkeypatch, "Bob")
    assert "Draft tab" not in at.tabs[1].success[0].value
