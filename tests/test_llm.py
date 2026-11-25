"""The Claude drafter, with a stubbed client: these tests make no network calls."""

import json
from types import SimpleNamespace

import anthropic
import httpx2
import pytest
from streamlit.testing.v1 import AppTest

from decisiontrace import llm, store
from decisiontrace.cards import UNKNOWN
from decisiontrace.drafter import MOCK, NO_DECISION, draft_card

TEXT = "We decided to use polling instead of WebSockets. Because WebSockets kept dropping behind the proxy."
GOOD = {
    "decision": "Use polling instead of WebSockets",
    "reason": "WebSockets kept dropping behind the proxy",
    "verbatim_quote": "Because WebSockets kept dropping behind the proxy.",
    "alternatives": ["WebSockets"],
    "confidence": "high",
    "more_decisions": False,
}
REQUEST = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


def answer(data, stop_reason="end_turn", model="claude-opus-5-5"):
    text = data if isinstance(data, str) else json.dumps(data)
    return SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        model=model,
    )


class FakeClient:
    """Returns (or raises) the given outcomes in order and records each request."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.fixture
def claude(monkeypatch):
    """Set a fake key and return a function that installs a FakeClient."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    def install(*outcomes):
        client = FakeClient(*outcomes)
        monkeypatch.setattr(llm, "_client", lambda: client)
        return client

    return install


def test_without_a_key_the_mock_drafts():
    assert not llm.is_configured()
    assert draft_card(TEXT, "alice").drafted_by == MOCK


def test_claude_card(claude):
    client = claude(answer(GOOD))
    card = draft_card(TEXT, "alice", source="Discord")
    assert card.decision == GOOD["decision"]
    assert card.reason == GOOD["reason"]
    assert card.verbatim_quote == GOOD["verbatim_quote"]
    assert card.alternatives == ["WebSockets"]
    assert card.confidence == "high"
    assert card.drafted_by == "claude-opus-5-5"
    assert (card.author, card.source, card.status) == ("alice", "Discord", "draft")
    assert len(client.calls) == 1


def test_request_shape(claude):
    client = claude(answer(GOOD))
    draft_card(TEXT, "alice")
    call = client.calls[0]
    assert call["model"] == llm.DEFAULT_MODEL
    assert call["system"] == llm.PROMPT_PATH.read_text(encoding="utf-8")
    assert call["messages"][0]["content"] == f"<discussion>\n{TEXT}\n</discussion>"
    assert call["output_config"]["format"] == {"type": "json_schema", "schema": llm.CARD_SCHEMA}
    assert call["fallbacks"] == "default"


def test_model_from_env_without_fallbacks(claude, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-haiku-5-5")
    client = claude(answer(GOOD, model="claude-haiku-5-5"))
    assert draft_card(TEXT, "alice").drafted_by == "claude-haiku-5-5"
    assert client.calls[0]["model"] == "claude-haiku-5-5"
    assert "fallbacks" not in client.calls[0]


def test_invented_quote_is_still_replaced(claude):
    claude(answer({**GOOD, "verbatim_quote": "The TA told us to use polling."}))
    card = draft_card(TEXT, "alice")
    assert card.verbatim_quote == UNKNOWN
    assert card.confidence == "low"
    assert card.warnings


def test_unknown_reason_caps_confidence(claude):
    claude(answer({**GOOD, "reason": "unknown", "verbatim_quote": "We decided to use polling instead of WebSockets."}))
    card = draft_card(TEXT, "alice")
    assert card.reason == UNKNOWN
    assert card.confidence == "low"


def test_no_decision(claude):
    claude(answer({**GOOD, "decision": "unknown", "reason": "unknown", "verbatim_quote": "unknown", "alternatives": []}))
    card = draft_card("Has anyone seen the lab slides?", "alice")
    assert card.decision == NO_DECISION
    assert card.confidence == "low"


def test_more_decisions_warns(claude):
    claude(answer({**GOOD, "more_decisions": True}))
    assert any("more than one decision" in w for w in draft_card(TEXT, "alice").warnings)


def test_invalid_json_is_asked_again_once(claude):
    client = claude(answer("not json"), answer(GOOD))
    assert draft_card(TEXT, "alice").decision == GOOD["decision"]
    assert len(client.calls) == 2


@pytest.mark.parametrize(
    "bad",
    [
        answer("not json"),
        answer({**GOOD, "confidence": "very high"}),
        answer({key: value for key, value in GOOD.items() if key != "reason"}),
        answer({**GOOD, "decision": "  "}),
        answer(GOOD, stop_reason="max_tokens"),
    ],
)
def test_two_bad_answers_raise(claude, bad):
    client = claude(bad, bad)
    with pytest.raises(llm.DraftError, match="not a valid card"):
        draft_card(TEXT, "alice")
    assert len(client.calls) == 2


@pytest.mark.parametrize(
    "error, words",
    [
        (anthropic.APITimeoutError(request=REQUEST), "did not answer"),
        (anthropic.RateLimitError("slow down", response=httpx2.Response(429, request=REQUEST), body=None), "rate limit"),
        (anthropic.AuthenticationError("bad key", response=httpx2.Response(401, request=REQUEST), body=None), "API key"),
        (anthropic.InternalServerError("oops", response=httpx2.Response(500, request=REQUEST), body=None), "HTTP 500"),
        (anthropic.APIConnectionError(request=REQUEST), "Could not reach"),
    ],
)
def test_api_failures_raise_a_readable_error(claude, error, words):
    claude(error)
    with pytest.raises(llm.DraftError, match=words) as info:
        draft_card(TEXT, "alice")
    assert "test-key" not in str(info.value)


def test_refusal_raises(claude):
    claude(answer(GOOD, stop_reason="refusal"))
    with pytest.raises(llm.DraftError, match="declined"):
        draft_card(TEXT, "alice")


def test_tab_keeps_text_and_saves_nothing_when_claude_fails(claude, tmp_path, monkeypatch):
    path = tmp_path / "cards.json"
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    claude(anthropic.APITimeoutError(request=REQUEST))
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="draft_author").input("alice")
    at.text_area(key="draft_text").input(TEXT)
    at.button(key="draft_button").click().run()
    assert not at.exception
    assert any("did not answer" in e.value for e in at.error)
    assert at.text_area(key="draft_text").value == TEXT
    assert "draft_save" not in [b.key for b in at.button]
    assert store.load(path) == []


def test_tab_labels_a_claude_card(claude, tmp_path, monkeypatch):
    monkeypatch.setattr(store, "DEFAULT_PATH", tmp_path / "cards.json")
    claude(answer(GOOD))
    at = AppTest.from_file("../app/main.py").run()
    at.text_input(key="draft_author").input("alice")
    at.text_area(key="draft_text").input(TEXT)
    at.button(key="draft_button").click().run()
    assert any("AI draft by claude-opus-5-5" in w.value for w in at.warning)
    assert not any("MOCK draft" in w.value for w in at.warning)
