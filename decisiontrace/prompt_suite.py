"""Prompt test suite runner for the drafter (module A).

The cases live in `tests/prompt_suite/cases.json`. Each case is a pasted
discussion and what the draft card must (or must not) contain. The checks use
key words instead of exact text, so the same cases work for the keyword MOCK
today and for the Claude drafter once module D's PR 2 connects it.

Run it and save a results table:

    uv run python -m decisiontrace.prompt_suite --out docs/prompt_suite_results/mock.md

Any function with the `draft_card(source_text, author)` signature can be
tested with `--drafter package.module:function`.
"""

from __future__ import annotations

import argparse
import importlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .cards import CONFIDENCE_LEVELS, UNKNOWN, Card
from .drafter import NO_DECISION

CASES_PATH = Path(__file__).resolve().parent.parent / "tests" / "prompt_suite" / "cases.json"
DEFAULT_DRAFTER = "decisiontrace.drafter:draft_card"
AUTHOR = "prompt-suite"

Drafter = Callable[[str, str], Card]


@dataclass
class Result:
    case_id: str
    kind: str
    failures: list[str] = field(default_factory=list)
    card: Card | None = None

    @property
    def passed(self) -> bool:
        return not self.failures


def load_cases(path: Path = CASES_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def case_input(case: dict) -> str:
    """The text to paste. A dict input builds long text without storing it."""
    raw = case["input"]
    if isinstance(raw, str):
        return raw
    return raw["text"] + raw["pad_with"] * raw["pad_times"]


def _has_all(text: str, words: list[str]) -> bool:
    lower = text.lower()
    return all(w.lower() in lower for w in words)


def is_no_decision(card: Card) -> bool:
    return card.decision in (NO_DECISION, UNKNOWN)


def check(case: dict, card: Card | None, error: Exception | None = None) -> list[str]:
    """Return what is wrong with `card` for `case`; an empty list is a pass."""
    expect = case["expect"]
    text = case_input(case)

    if expect.get("refused"):
        return [] if isinstance(error, ValueError) else ["expected the input to be refused"]
    if error is not None:
        return [f"drafter raised {type(error).__name__}: {error}"]
    assert card is not None

    if expect.get("no_decision"):
        if not is_no_decision(card):
            return [f"expected no decision, got decision {card.decision!r}"]
        return []

    failures: list[str] = []
    if is_no_decision(card):
        return [f"expected a decision, got {card.decision!r}"]

    if card.verbatim_quote != UNKNOWN and card.verbatim_quote not in text:
        failures.append("quote is not verbatim in the input")

    words = expect.get("decision_contains")
    if words and not _has_all(card.decision, words):
        failures.append(f"decision {card.decision!r} should mention {words}")

    words = expect.get("reason_contains")
    if words and not _has_all(card.reason, words):
        failures.append(f"reason {card.reason!r} should mention {words}")

    if "reason" in expect and card.reason != expect["reason"]:
        failures.append(f"reason should be {expect['reason']!r}, got {card.reason!r}")

    if "alternatives" in expect:
        got = [a.strip() for a in card.alternatives]
        if got != expect["alternatives"]:
            failures.append(f"alternatives should be {expect['alternatives']}, got {got}")

    limit = expect.get("confidence_at_most")
    if limit and CONFIDENCE_LEVELS.index(card.confidence) > CONFIDENCE_LEVELS.index(limit):
        failures.append(f"confidence should be at most {limit!r}, got {card.confidence!r}")

    for decision_word, reason_word in expect.get("forbidden_pairs", []):
        if _has_all(card.decision, [decision_word]) and _has_all(card.reason, [reason_word]):
            failures.append(
                f"reason {card.reason!r} does not support the {decision_word} decision"
            )

    if expect.get("warns") and not card.warnings:
        failures.append("expected a warning on the card")

    if "status" in expect and card.status != expect["status"]:
        failures.append(f"status should be {expect['status']!r}, got {card.status!r}")

    return failures


def run_case(case: dict, drafter: Drafter) -> Result:
    card, error = None, None
    try:
        card = drafter(case_input(case), AUTHOR)
    except Exception as exc:  # the suite reports drafter crashes as failures
        error = exc
    return Result(case["id"], case["kind"], check(case, card, error), card)


def run(drafter: Drafter, cases: list[dict] | None = None) -> list[Result]:
    return [run_case(c, drafter) for c in (cases if cases is not None else load_cases())]


def load_drafter(spec: str) -> Drafter:
    module, _, name = spec.partition(":")
    return getattr(importlib.import_module(module), name)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def to_markdown(results: list[Result], drafter_spec: str) -> str:
    passed = sum(r.passed for r in results)
    lines = [
        f"Drafter: `{drafter_spec}`. Passed {passed} of {len(results)}.",
        "",
        "| Case | Kind | Result | What was wrong |",
        "| --- | --- | --- | --- |",
    ]
    for r in results:
        result = "pass" if r.passed else "FAIL"
        lines.append(f"| {r.case_id} | {r.kind} | {result} | {_cell('; '.join(r.failures))} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--drafter", default=DEFAULT_DRAFTER, help="module:function to test")
    parser.add_argument("--out", type=Path, help="also write the results table to this file")
    args = parser.parse_args(argv)

    results = run(load_drafter(args.drafter))
    table = to_markdown(results, args.drafter)
    print(table, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(table, encoding="utf-8")
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
