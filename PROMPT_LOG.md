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
