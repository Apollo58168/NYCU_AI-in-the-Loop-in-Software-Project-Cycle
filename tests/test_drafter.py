import pytest
from streamlit.testing.v1 import AppTest

from decisiontrace import store
from decisiontrace.prompt_suite import is_no_decision
from decisiontrace.cards import UNKNOWN
from decisiontrace.drafter import MAX_CHARS, MOCK, NO_DECISION, draft_card, split_sentences

ENGLISH = (
    "Alice: the WebSocket demo dropped again on the school VM.\n"
    "Bob: We decided to use polling every 10 seconds instead of WebSockets.\n"
    "Alice: OK, because WebSockets kept dropping behind the reverse proxy."
)
CHINESE = "我們討論了很久。最後決定改用 SQLite 而不是 MongoDB。因為不用另外架伺服器。"


def test_english_discussion():
    card = draft_card(ENGLISH, "bob")
    assert card.decision == "Bob: We decided to use polling every 10 seconds instead of WebSockets."
    assert card.reason == "Alice: OK, because WebSockets kept dropping behind the reverse proxy."
    assert card.verbatim_quote == card.reason
    assert card.alternatives == ["WebSockets"]
    assert card.confidence == "medium"
    assert card.drafted_by == MOCK
    assert card.status == "draft"
    assert card.author == "bob"
    assert card.source == "pasted text"
    assert card.warnings == []


def test_chinese_discussion():
    card = draft_card(CHINESE, "凱旭", source="Discord #decisions")
    assert card.decision == "最後決定改用 SQLite 而不是 MongoDB。"
    assert card.reason == "因為不用另外架伺服器。"
    assert card.verbatim_quote == "因為不用另外架伺服器。"
    assert card.alternatives == ["MongoDB"]
    assert card.source == "Discord #decisions"


def test_quote_is_always_verbatim_in_the_source():
    for text in (ENGLISH, CHINESE):
        card = draft_card(text, "bob")
        assert card.verbatim_quote in text


def test_decision_without_reason_quotes_the_decision():
    card = draft_card("Let's go with uv for packaging.", "alice")
    assert card.decision == "Let's go with uv for packaging."
    assert card.reason == UNKNOWN
    assert card.verbatim_quote == card.decision
    assert card.confidence == "low"


def test_markers_are_case_insensitive():
    card = draft_card("AGREED: we ship on Friday. Since the demo is Monday.", "alice")
    assert card.decision == "AGREED: we ship on Friday."
    assert card.reason == "Since the demo is Monday."


@pytest.mark.parametrize(
    "text",
    [
        "We are still undecided about the database because nobody has benchmarked it.",
        "I disagreed with switching to Rust because the deadline is close.",
    ],
)
def test_markers_inside_other_words_are_not_decisions(text):
    # is_no_decision, not the exact NO_DECISION text: #18 changes how a
    # no-decision card looks, and the Claude drafter (#21) may differ again.
    assert is_no_decision(draft_card(text, "alice"))


def test_whole_word_markers_still_match_next_to_punctuation():
    card = draft_card("Decided: we'll use uv, since it is fast.", "alice")
    assert card.decision == "Decided: we'll use uv, since it is fast."
    assert card.reason == card.decision


def test_reason_of_another_decision_is_not_attached():
    # Group 11 review F1, first example (#17).
    card = draft_card(
        "We decided to use PostgreSQL. We decided to use React because the team knows it.",
        "alice",
    )
    assert card.decision == "We decided to use PostgreSQL."
    assert card.reason == UNKNOWN
    assert card.verbatim_quote == card.decision
    assert card.confidence == "low"
    assert any("2 decisions" in w for w in card.warnings)


def test_reason_before_the_decision_is_not_attached():
    # Group 11 review F1, second example (#17).
    card = draft_card("Lunch was late because the cafe was busy. We decided to use PostgreSQL.", "alice")
    assert card.decision == "We decided to use PostgreSQL."
    assert card.reason == UNKNOWN
    assert "cafe" not in card.verbatim_quote
    assert card.confidence == "low"


def test_reason_in_the_next_sentence_is_kept():
    card = draft_card(
        "We decided to use polling instead of WebSockets. Because WebSockets kept dropping.",
        "alice",
    )
    assert card.reason == "Because WebSockets kept dropping."
    assert card.confidence == "medium"


def test_reason_two_sentences_later_is_not_attached():
    card = draft_card("We decided to use uv. The lab is on Monday. Since pip is slow.", "alice")
    assert card.reason == UNKNOWN


def test_one_decision_gives_no_split_warning():
    assert draft_card(ENGLISH, "bob").warnings == []


def test_no_decision_found():
    card = draft_card("Has anyone seen the lab slides? I can't find them.", "alice")
    assert card.decision == UNKNOWN
    assert NO_DECISION in card.warnings
    assert card.reason == UNKNOWN
    assert card.verbatim_quote == UNKNOWN
    assert card.alternatives == []
    assert card.confidence == "low"


@pytest.mark.parametrize("text", ["", "   \n\t ", None])
def test_empty_input_is_refused(text):
    with pytest.raises(ValueError):
        draft_card(text, "alice")


def test_very_long_input_is_cut_with_a_warning():
    text = "We decided to use Streamlit. " + "x" * (MAX_CHARS * 2)
    card = draft_card(text, "alice")
    assert card.decision == "We decided to use Streamlit."
    assert len(card.warnings) == 1
    assert str(MAX_CHARS) in card.warnings[0]


def test_decision_past_the_limit_is_not_seen():
    text = "x" * MAX_CHARS + " We decided to use Streamlit."
    assert draft_card(text, "alice").decision == UNKNOWN


def test_split_sentences_handles_both_languages():
    assert split_sentences("One. Two!\n三。四？五；") == ["One.", "Two!", "三。", "四？", "五；"]


# The Draft tab, driven through the whole app as in tests/test_app.py.

def _draft(tmp_path, monkeypatch, author, text):
    path = tmp_path / "cards.json"
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="draft_author").input(author)
    at.text_area(key="draft_text").input(text)
    at.button(key="draft_button").click().run()
    assert not at.exception
    return at, path


def test_tab_shows_mock_label_and_saves_draft(tmp_path, monkeypatch):
    at, path = _draft(tmp_path, monkeypatch, "bob", ENGLISH)
    assert any("MOCK" in w.value for w in at.warning)
    assert any("use polling" in m.value for m in at.markdown)
    assert store.load(path) == []

    at.button(key="draft_save").click().run()
    assert not at.exception
    saved = store.load(path)
    assert len(saved) == 1
    assert saved[0].status == "draft"
    assert saved[0].drafted_by == MOCK
    assert at.success


def test_tab_shows_error_for_empty_text(tmp_path, monkeypatch):
    at, _ = _draft(tmp_path, monkeypatch, "bob", "  ")
    assert at.error
    assert not any("MOCK" in w.value for w in at.warning)


def test_tab_shows_error_without_author(tmp_path, monkeypatch):
    at, _ = _draft(tmp_path, monkeypatch, " ", ENGLISH)
    assert at.error


def test_tab_save_message_says_who_reviews_next(tmp_path, monkeypatch):
    at, _ = _draft(tmp_path, monkeypatch, "bob", ENGLISH)
    at.button(key="draft_save").click().run()
    assert "enter their own name as reviewer" in at.success[0].value


def test_tab_offers_no_save_without_a_decision(tmp_path, monkeypatch):
    # Group 11 review (#16, F2): chit-chat must not become a saved draft.
    at, path = _draft(tmp_path, monkeypatch, "bob", "今天午餐好吃")
    assert "No decision found" in at.info[0].value
    assert not [b for b in at.button if b.key == "draft_save"]
    assert store.load(path) == []
