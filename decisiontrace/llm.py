"""Claude drafter (module D, PR 2).

draft_fields() sends the pasted discussion to Claude with the system prompt in
prompts/draft_card.md and gets back the card fields as JSON. drafter.py builds
the card from them, so the MOCK and Claude share the same card rules and the
same check_quote().

Settings come from the environment, or from a local .env file (gitignored):
ANTHROPIC_API_KEY (without it the MOCK runs) and ANTHROPIC_MODEL (optional).
The key is never printed or logged.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from .cards import CONFIDENCE_LEVELS

load_dotenv()  # a real environment variable wins over the .env file

DEFAULT_MODEL = "claude-opus-5-5"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "draft_card.md"
TIMEOUT_SECONDS = 30.0
MAX_TOKENS = 16000

# If Claude's safety checks decline a request, the API retries it on a
# fallback model in the same call. Only these models accept the parameter.
_FALLBACK_BETA = "server-side-fallback-2026-07-01"
_FALLBACK_MODELS = {"claude-opus-5-5", "claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5"}

CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string"},
        "reason": {"type": "string"},
        "verbatim_quote": {"type": "string"},
        "alternatives": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "string", "enum": list(CONFIDENCE_LEVELS)},
        "more_decisions": {"type": "boolean"},
    },
    "required": [
        "decision", "reason", "verbatim_quote", "alternatives", "confidence", "more_decisions",
    ],
    "additionalProperties": False,
}


class DraftError(Exception):
    """Claude could not draft a card. The message is safe to show to the user."""


def is_configured() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def model_name() -> str:
    return os.environ.get("ANTHROPIC_MODEL", "").strip() or DEFAULT_MODEL


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic(timeout=TIMEOUT_SECONDS, max_retries=1)


def _call(client, system: str, text: str):
    model = model_name()
    extra = {}
    if model in _FALLBACK_MODELS:
        extra = {"betas": [_FALLBACK_BETA], "fallbacks": "default"}
    try:
        response = client.beta.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": f"<discussion>\n{text}\n</discussion>"}],
            output_config={
                "effort": "low",
                "format": {"type": "json_schema", "schema": CARD_SCHEMA},
            },
            **extra,
        )
    # Most specific first: APITimeoutError is a kind of APIConnectionError.
    except anthropic.APITimeoutError:
        raise DraftError(
            f"Claude did not answer within {TIMEOUT_SECONDS:.0f} seconds. "
            "Your text is kept; press Draft card to try again."
        ) from None
    except anthropic.RateLimitError:
        raise DraftError(
            "Claude's rate limit was reached. Wait a minute, then press Draft card again."
        ) from None
    except anthropic.AuthenticationError:
        raise DraftError(
            "Claude rejected the API key. Check ANTHROPIC_API_KEY in your .env file."
        ) from None
    except anthropic.APIStatusError as exc:
        raise DraftError(
            f"Claude returned an error (HTTP {exc.status_code}). Press Draft card to try again."
        ) from None
    except anthropic.APIConnectionError:
        raise DraftError(
            "Could not reach Claude. Check your network, then press Draft card again."
        ) from None
    if response.stop_reason == "refusal":
        raise DraftError("Claude declined to draft a card from this text.")
    return response


def parse_fields(response) -> dict:
    """The card fields from Claude's JSON answer; ValueError if it is not valid."""
    if response.stop_reason == "max_tokens":
        raise ValueError("answer was cut off")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise ValueError("no text in the answer")
    data = json.loads(text)  # json.JSONDecodeError is a ValueError
    if not isinstance(data, dict) or set(data) != set(CARD_SCHEMA["required"]):
        raise ValueError("wrong fields")
    strings = ("decision", "reason", "verbatim_quote")
    if not all(isinstance(data[k], str) and data[k].strip() for k in strings):
        raise ValueError("empty or non-text field")
    alternatives = data["alternatives"]
    if not isinstance(alternatives, list) or not all(isinstance(a, str) for a in alternatives):
        raise ValueError("alternatives is not a list of text")
    if data["confidence"] not in CONFIDENCE_LEVELS or not isinstance(data["more_decisions"], bool):
        raise ValueError("bad confidence or more_decisions")
    return {
        **{k: data[k].strip() for k in strings},
        "alternatives": [a.strip() for a in alternatives if a.strip()],
        "confidence": data["confidence"],
        "more_decisions": data["more_decisions"],
    }


def draft_fields(text: str, client=None) -> tuple[dict, str]:
    """Ask Claude for the card fields. Returns (fields, model that answered).

    An answer that is not valid JSON in the expected shape is asked for once
    more; a second bad answer raises DraftError, so no incomplete card is made.
    """
    client = client or _client()
    system = PROMPT_PATH.read_text(encoding="utf-8")
    for _ in range(2):
        response = _call(client, system, text)
        try:
            return parse_fields(response), response.model
        except ValueError:
            continue
    raise DraftError(
        "Claude's answer was not a valid card twice in a row. Your text is kept; "
        "press Draft card to try again."
    )
