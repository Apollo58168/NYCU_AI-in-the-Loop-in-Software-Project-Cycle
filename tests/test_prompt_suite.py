"""Run the prompt test suite against the MOCK drafter, and test the checker.

Cases the MOCK is known to fail carry a `known_failure.mock` note in
cases.json and run as strict xfail: when a fix (for example #17) makes one
pass, this test fails until the note is removed, so the list stays honest.
"""

import pytest

from decisiontrace import prompt_suite
from decisiontrace.cards import UNKNOWN, Card
from decisiontrace.drafter import draft_card

CASES = prompt_suite.load_cases()


def _param(case):
    note = case.get("known_failure", {}).get("mock")
    marks = [pytest.mark.xfail(reason=note, strict=True)] if note else []
    return pytest.param(case, id=case["id"], marks=marks)


@pytest.mark.parametrize("case", [_param(c) for c in CASES])
def test_mock_drafter(case):
    result = prompt_suite.run_case(case, draft_card)
    assert result.passed, result.failures


def test_suite_has_ten_cases_with_typical_and_edge_inputs():
    assert len(CASES) >= 10
    assert {c["kind"] for c in CASES} == {"typical", "edge"}
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids))


def test_long_input_is_built_past_the_limit():
    case = next(c for c in CASES if c["id"] == "E8-too-long")
    assert len(prompt_suite.case_input(case)) > 8000


# The checker itself: a wrong card must be reported, not waved through.

def _card(**overrides):
    fields = dict(
        decision="We decided to use PostgreSQL.",
        reason="Because our data is relational.",
        verbatim_quote="Because our data is relational.",
        alternatives=["MongoDB"],
        confidence="medium",
        source="test",
        author="alice",
        drafted_by="test",
    )
    fields.update(overrides)
    return Card(**fields)


CASE = {
    "id": "x",
    "kind": "typical",
    "input": "We decided to use PostgreSQL. Because our data is relational.",
    "expect": {
        "decision_contains": ["postgresql"],
        "reason_contains": ["relational"],
        "alternatives": ["MongoDB"],
        "confidence_at_most": "medium",
        "status": "draft",
    },
}


def test_checker_passes_a_matching_card():
    assert prompt_suite.check(CASE, _card()) == []


@pytest.mark.parametrize(
    "overrides, problem",
    [
        ({"decision": "We decided to use MySQL."}, "decision"),
        ({"reason": "Because it is fast."}, "reason"),
        ({"alternatives": ["MongoDB because"]}, "alternatives"),
        ({"confidence": "high"}, "confidence"),
        ({"status": "approved"}, "status"),
        ({"verbatim_quote": "made up"}, "verbatim"),
        ({"decision": UNKNOWN}, "expected a decision"),
    ],
)
def test_checker_reports_each_kind_of_mistake(overrides, problem):
    failures = prompt_suite.check(CASE, _card(**overrides))
    assert any(problem in f for f in failures), failures


def test_checker_reports_forbidden_pair_and_missing_warning():
    case = {"id": "x", "kind": "edge", "input": CASE["input"],
            "expect": {"forbidden_pairs": [["PostgreSQL", "relational"]], "warns": True}}
    failures = prompt_suite.check(case, _card())
    assert len(failures) == 2, failures


def test_checker_handles_refusal_and_crashes():
    refused = {"id": "x", "kind": "edge", "input": "", "expect": {"refused": True}}
    assert prompt_suite.check(refused, None, ValueError("empty")) == []
    assert prompt_suite.check(refused, _card()) != []
    assert prompt_suite.check(CASE, None, TimeoutError("slow")) != []


def test_cli_writes_the_table(tmp_path, capsys):
    out = tmp_path / "results.md"
    code = prompt_suite.main(["--out", str(out)])
    table = out.read_text(encoding="utf-8")
    assert "| T1-english-chat | typical | pass |" in table
    assert table == capsys.readouterr().out
    assert code == 1  # the MOCK still has known failures
