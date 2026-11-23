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

## 2026-11-23 — Ask tab for the walking skeleton (module C)

- **Tool and model:** Claude Code (Claude Opus 5.5)
- **Prompt summary:** I gave Claude Code our team prompt for module C: implement `answer(question, cards)` from approved cards only, scored by keyword overlap (English words, Chinese character bigrams), returning exactly "No approved decision found." when nothing matches, plus the Ask tab and tests.
- **Output:** `decisiontrace/ask.py`, `app/tab_ask.py` and `tests/test_ask.py` (17 tests, including three that drive the Ask tab with Streamlit's `AppTest`).
- **What I retained:** All of it, after reading the diff and running `uv run pytest` (27 passed). To check that the tests can fail, I removed the approved-only filter and three tests failed.
- **What I changed:** Added stop words (question words and "decide"/"決定"), so a question like "What did we decide?" gets the fallback instead of matching any card that contains "we". On a tie the newer card wins, because a later decision may replace an earlier one.
- **Human decision and reason:** Keyword overlap is enough for the walking skeleton; ranking up to three cards with cited quotes is planned for module C's second PR.
- **Repository result:** [PR #9 — Ask tab from approved cards](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/9)
