# Prompt Engineering Log

## 2026-09-21 — DecisionTrace Week 3 Documentation

- **Tool and model:** OpenAI Codex (GPT-5)
- **Prompt summary:** I asked Codex to review the Week 3 materials I had prepared, focusing on clarity, completeness, consistency with the specification, and whether the proposed evaluation was measurable.
- **Output:** Codex provided review feedback on my AI usage guidelines and DecisionTrace evaluation plan, including suggestions about the human–AI boundary, target users, evaluation method, and minimum evidence thresholds.
- **What I retained:** I kept the parts of the review that clarified how AI extracts and summarizes decision candidates while humans approve, edit, or reject them. I also kept the suggestion to make the evaluation measures explicit: accuracy, completion time, confidence, and usefulness.
- **What I changed:** Based on the review, I removed draft-status wording, renamed the repeated internal heading to `Evaluation Design`, cleared generic placeholders, and clarified that every official decision-log entry requires recorded human approval or editing.
- **Human decision and reason:** I authored the Week 3 materials and used Codex as a reviewer. I evaluated its suggestions individually and accepted only the changes that made the documents clearer and the evaluation more observable and measurable.
- **Repository result:** [PR #6 — Add Week 3 AI guidelines and evaluation plan](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/6)

## 2026-11-23 — Project setup for the walking skeleton (module A)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I asked Claude Code to set up the uv project, implement the shared `Card` contract with the verbatim-quote check and JSON storage, create an app shell with one placeholder file per tab, add tests, and document the run steps in the README.
- **Output:** `pyproject.toml`, `decisiontrace/cards.py`, `decisiontrace/store.py`, `app/main.py`, four placeholder tab files, 10 pytest tests, and the README run section.
- **What I retained:** All of it, after reading the diff and running `uv run pytest` and the app locally.
- **What I changed:** The scope was limited to what the other three modules need to start in the walking skeleton session; no tab is built here.
- **Human decision and reason:** The contract (fields, statuses, function signatures) follows our team's split plan, so that each module can be built in parallel in its own file.
- **Repository result:** [PR #8 — Project setup and shared Card contract](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/8)

## 2026-11-23 — Review tab for the walking skeleton (module B)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I gave Claude Code our team prompt for module B: implement `review(card, reviewer, action)` for "approve" and "reject" (reviewer name required, reviewer must differ from the author ignoring case and spaces, only draft cards), plus the Review tab and tests.
- **Output:** `decisiontrace/review.py`, `app/tab_review.py` and `tests/test_review.py` (15 tests, including two that drive the Review tab with Streamlit's `AppTest`).
- **What I retained:** All of it, after reading the diff and running `uv run pytest` (57 passed). To check that the tests can fail, I removed the author check and five tests failed.
- **What I changed:** Passing `edits` is refused with a clear error for now, so nobody can change a card's text before module B's PR 2 adds "edit_approve". MOCK cards keep the same "MOCK draft, not AI" label in the Review tab as in the Draft tab.
- **Human decision and reason:** The rule that the author cannot review their own card lives in `review()`, not only in the tab, so every future caller (export, PR 2 actions) gets it too.
- **Repository result:** [PR #11 — Review tab, approve or reject draft cards](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/11)

## 2026-11-23 — Approved cards tab for the walking skeleton (module A)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I gave Claude Code our team prompt for module A's session piece: `approved_cards(cards)` (approved only, newest first), the Approved cards tab with an empty state, and tests.
- **Output:** `decisiontrace/listing.py`, `app/tab_cards.py` and `tests/test_listing.py` (4 tests, two of them drive the tab with `AppTest`).
- **What I retained:** All of it, after reading the diff and running `uv run pytest` (61 passed). To check that the tests can fail, I let non-draft cards through the filter and two tests failed. I also ran the whole path once (draft as Alice, approve as Bob, ask, then the Approved cards tab).
- **What I changed:** MOCK cards are labelled "MOCK (not AI)" here too, like in the Draft and Review tabs.
- **Human decision and reason:** "Newest" uses the card's `created_at` (when it was drafted), because cards do not store a review time until module B's PR 2.
- **Repository result:** [PR #12 — Approved cards tab](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/12)

## 2026-11-24 — Prompt test suite for the drafter (module A, PR 2)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I asked Claude Code to build the CP2 prompt test suite for `draft_card()`: at least ten typical and edge cases including Group 11's three inputs, a runner whose checks also work for the Claude drafter, one failure-fix-re-run cycle, and a doc page.
- **Output:** `tests/prompt_suite/cases.json` (15 cases), `decisiontrace/prompt_suite.py`, `tests/test_prompt_suite.py`, `docs/prompt_test_suite.md`, two results tables, and a whole-word marker fix in `decisiontrace/drafter.py` with three drafter tests.
- **What I retained:** All of it, after reading the diff and running `uv run pytest` (89 passed, 3 xfailed). To check that the tests can fail, I put plain substring matching back and four tests failed.
- **What I changed:** Known MOCK failures (Group 11 F1 and F3) run as strict xfail instead of being left out, so the suite shows them and fails once #17 fixes them and the note is not removed.
- **Human decision and reason:** Run 1 found that "undecided" and "disagreed" were drafted as decisions. I fixed that in the MOCK even though Claude will replace it, because #21 keeps the MOCK whenever no API key is set, which is how a fresh clone runs.
- **Repository result:** this PR (module A PR 2).

## 2026-11-25 — Review guards and next-step messages (module B, PR 2)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I asked Claude Code to fix issues #18 and #19 from Group 11's review (#16): a card with no decision must not be saved or approved, and the Draft and Review tabs must tell the user the next step after Save and after Reject. Tests come from Group 11's inputs.
- **Output:** changes to `decisiontrace/review.py`, `decisiontrace/drafter.py`, `app/tab_draft.py`, `app/tab_review.py`; 5 new tests in `tests/test_review.py` and `tests/test_drafter.py`, and 2 updated drafter tests.
- **What I retained:** All of it, after reading the diff and running `uv run pytest` (66 passed). To check that the tests can fail, I broke each change once. Removing the approve guard, the Draft Save guard, or the Reject hint each made 1 test fail.
- **What I changed:** The no-decision card now uses `decision = UNKNOWN` with the old text as a warning, so `review()` checks a value, not an error string. It does not change the shared `Card` contract.
- **Human decision and reason:** The guard lives in `review()` as well as the Draft tab, so a no-decision card that is already saved (or arrives from another caller) still cannot be approved.
- **Repository result:** see the PR for #18 and #19.

## 2026-11-25 — Reason only from the decision's own sentence (module D, #17)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I asked Claude Code to fix issue #17 (Group 11 review F1): the MOCK drafter must not attach a reason from another sentence, must warn when the text has more than one decision, and the prompt suite's E1/E2 cases must pass.
- **Output:** `_reason_for()` and the multi-decision warning in `decisiontrace/drafter.py`, five tests in `tests/test_drafter.py`, the `known_failure` notes for E1/E2 removed from `tests/prompt_suite/cases.json`, run 3 of the prompt suite, and a "Revision cycle 2" section in `docs/prompt_test_suite.md`.
- **What I retained:** All of it, after reading the diff and running the tests (96 passed, 1 xfailed for T3). To check that the tests can fail, I put back "first reason sentence anywhere" and five tests failed.
- **What I changed:** The issue says "same sentence only". That would break the suite's T1/T2 cases and the walking-skeleton demo, where the reason is the next sentence ("…instead of WebSockets. Because WebSockets kept dropping…"). So the next sentence is also allowed, but only when it states no decision of its own.
- **Human decision and reason:** The rule stays narrow (own sentence or the next one) so that an unrelated "because" elsewhere in a long thread is never attached; a missing reason becomes `unknown`, which our CP1 criterion prefers to an unsupported one. After 蔡尚融's review, a reason from the next sentence gets confidence `low` and a warning, because keywords cannot tell it from an unrelated "because" (E12, E13 added as known MOCK failures).
- **Repository result:** [PR #35 — Reason only from the decision's own sentence](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/35)

## 2026-11-25 — Claude drafter behind draft_card (module D, PR 2, #21)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I gave Claude Code our module D PR 2 task and issue #21: call Claude from `draft_card()` when `ANTHROPIC_API_KEY` is set and keep the MOCK otherwise; on timeout, rate limit or invalid JSON keep the pasted text, show a retryable error and save no card; a system prompt that never invents a reason; tests with a stubbed client; a prompt card.
- **Output:** `decisiontrace/llm.py`, the shared card building in `decisiontrace/drafter.py`, `prompts/draft_card.md`, the Draft tab's error and AI label, `tests/test_llm.py` (22 tests, no network), `tests/conftest.py`, `.env.example`, `docs/PROMPT_CARD.md`, and the README status line.
- **What I retained:** All of it, after reading the diff and running the tests (118 passed, 1 xfailed). To check that the tests can fail, I removed the second try on invalid JSON and six tests failed.
- **What I changed:** Followed #21 instead of the older plan: when Claude fails, the app shows an error rather than silently falling back to the MOCK, so a MOCK card is never mistaken for a Claude card. Confidence is capped at "low" in code whenever the reason is unknown, for both drafters.
- **Human decision and reason:** Opened as a draft PR because the course API key has not arrived; the real-API run of the prompt suite and the failure → fix → re-run cycle come next.
- **Repository result:** PR link added after the PR is opened.
