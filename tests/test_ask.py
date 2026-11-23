import pytest
from streamlit.testing.v1 import AppTest

from decisiontrace import store
from decisiontrace.ask import NO_ANSWER, answer, tokens
from decisiontrace.cards import Card


def make_card(decision, reason, status="approved", alternatives=(), created_at="2026-11-20T00:00:00+00:00"):
    return Card(
        decision=decision,
        reason=reason,
        verbatim_quote="unknown",
        alternatives=list(alternatives),
        confidence="medium",
        source="pasted text",
        author="alice",
        drafted_by="mock",
        status=status,
        reviewer="bob" if status == "approved" else None,
        created_at=created_at,
    )


POLLING = make_card("Use polling for live updates", "WebSockets kept dropping behind the proxy", alternatives=["WebSockets"])
SQLITE = make_card("Store data in SQLite", "No server to run for a class project")
CHINESE = make_card("改用 Streamlit 做介面", "因為四個人都會 Python")


def test_tokens_split_words_and_chinese_bigrams():
    assert tokens("Why did we pick WebSockets?") == {"pick", "websockets"}
    assert tokens("改用輪詢") == {"改用", "用輪", "輪詢"}


def test_best_matching_approved_card_answers():
    result = answer("Why polling instead of WebSockets?", [SQLITE, POLLING])
    assert result.card_ids == [POLLING.id]
    assert "Use polling for live updates" in result.text
    assert "WebSockets kept dropping behind the proxy" in result.text


def test_chinese_question_matches_chinese_card():
    result = answer("我們為什麼改用 Streamlit？", [POLLING, CHINESE])
    assert result.card_ids == [CHINESE.id]


@pytest.mark.parametrize("status", ["draft", "rejected", "needs_author"])
def test_cards_that_are_not_approved_are_never_used(status):
    unapproved = make_card("Use polling for live updates", "proxy drops sockets", status=status)
    result = answer("polling", [unapproved])
    assert result.text == NO_ANSWER
    assert result.card_ids == []


def test_no_match_gives_exact_fallback():
    result = answer("What colour is the logo?", [POLLING, SQLITE, CHINESE])
    assert result.text == "No approved decision found."
    assert result.card_ids == []


def test_question_of_only_common_words_gives_fallback():
    assert answer("What did we decide?", [POLLING]).text == NO_ANSWER


def test_no_cards_gives_fallback():
    assert answer("polling", []).text == NO_ANSWER


@pytest.mark.parametrize("question", ["", "   ", "\n"])
def test_empty_question_raises(question):
    with pytest.raises(ValueError):
        answer(question, [POLLING])


def test_tie_goes_to_newer_card():
    old = make_card("Use polling", "simple", created_at="2026-11-01T00:00:00+00:00")
    new = make_card("Stop polling, use SSE", "polling was slow", created_at="2026-11-20T00:00:00+00:00")
    assert answer("polling", [old, new]).card_ids == [new.id]


def test_unknown_reason_is_shown_as_unknown():
    card = make_card("Use polling", "unknown")
    assert "Reason: unknown" in answer("polling", [card]).text


def _ask(tmp_path, monkeypatch, question, cards):
    path = tmp_path / "cards.json"
    store.save(cards, path)
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="ask_question").input(question)
    at.button(key="ask_button").click().run()
    assert not at.exception
    return at


def test_tab_shows_answer_and_source_card(tmp_path, monkeypatch):
    at = _ask(tmp_path, monkeypatch, "Why polling?", [POLLING, SQLITE])
    shown = " ".join(m.value for m in at.markdown)
    assert "Use polling for live updates" in shown
    assert "Source card" in shown
    assert any("approved by bob" in c.value for c in at.caption)


def test_tab_shows_error_for_empty_question(tmp_path, monkeypatch):
    at = _ask(tmp_path, monkeypatch, "   ", [POLLING])
    assert at.error
    assert "Source card" not in " ".join(m.value for m in at.markdown)


def test_tab_shows_error_for_broken_data_file(tmp_path, monkeypatch):
    path = tmp_path / "cards.json"
    path.write_text("not json", encoding="utf-8")
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="ask_question").input("polling")
    at.button(key="ask_button").click().run()
    assert not at.exception
    assert at.error
