from pathlib import Path

from decisiontrace import llm

CLAUDE_MD = Path(__file__).resolve().parent.parent / "CLAUDE.md"


def test_claude_md_shows_the_system_prompt_the_code_uses():
    # CP2 submits CLAUDE.md as the system prompt, so its copy must not drift
    # from prompts/draft_card.md, which llm.py actually sends to Claude.
    prompt = llm.PROMPT_PATH.read_text(encoding="utf-8").strip()
    assert f"```text\n{prompt}\n```" in CLAUDE_MD.read_text(encoding="utf-8")
