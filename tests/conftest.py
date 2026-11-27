import pytest


@pytest.fixture(autouse=True)
def no_claude_key(monkeypatch):
    """Tests never call the real API: a key in a developer's .env is removed,
    so the MOCK drafts unless a test sets a key and a fake client itself."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
