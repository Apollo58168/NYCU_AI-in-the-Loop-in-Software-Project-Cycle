# Interim Evaluation Report (CP2)

Status: interim, 2026-11-25. Plan: CP1 §4, which replaced the Week 3 `EVALUATION_PLAN.md` thresholds (`DECISIONS.md`, 2026-10-25). This report lists what we have measured so far and, just as important, what we have **not** measured yet.

## Summary

None of the five CP1 pass/fail criteria has been tested yet. The prototype runs end to end, but card drafting is still a keyword MOCK (Claude is connected in #21). No participant study has been run, and no ground truth has been committed. So far we have evidence about **safety rules** (who can approve what, and that quotes are verbatim). We have no evidence yet about **effect** (speed, accuracy, acceptance).

## CP1 §4 criteria

| # | Criterion (CP1 §4) | Status | Evidence so far |
|---|---|---|---|
| 1 | ≥ 6 retrieval participants (≥ 3 per group), ≥ 2 reviewer participants | **Not tested** | 0 participants. The ground-truth list and the 3 "why" questions are not committed yet. |
| 2 | DecisionTrace group ≥ 80% correct on the 2 scored questions, no lower than manual | **Not tested** | No retrieval study yet. |
| 3 | DecisionTrace median time ≥ 30% lower, and full separation of participant medians | **Not tested** | No retrieval study yet. |
| 4 | Reviewers approve or edit ≥ 60% of AI cards, median ≤ 2 min per card | **Not tested** | Every card so far comes from the MOCK, not from AI, so its acceptance rate says nothing about Claude's drafts. Review time is not recorded yet (no `reviewed_at`). |
| 5 | No approved card has a reason its sources do not support (hard rule) | **Risk found, partly guarded** | See "What we have tested". The MOCK can attach a verbatim but unrelated reason (Group 11, #16 F1). A reviewer can still approve such a card. |

## What we have tested

**Automated tests.** `uv run pytest` on `main` gives 61 passed. These cover the verbatim-quote check (`check_quote`), the "author cannot review" rule, "Ask uses approved cards only", and the four tabs through Streamlit `AppTest`.

**Cross-team review by Group 11 (#16, 2026-11-24).** This is our first look from outside the team. They ran the app from the README and tried to make the drafter fail:
- **Unsupported reasons (criterion 5).** With two decisions in one text, the Reason and Quote came from the other decision. A lunch sentence was given as the reason for choosing PostgreSQL (F1). The quote was verbatim, so `check_quote` passed, but it did not support the decision. **A verbatim quote is not enough to meet criterion 5.** Tracked in #17.
- **No-decision cards could be approved (F2).** Chit-chat produced a card that a reviewer could approve into the decision log. Fixed in #26 (#18): such a card cannot be saved or approved.
- **Alternatives included the reason text (F3).** Not fixed in the MOCK. The sentence is a prompt-suite case.
- **Next step unclear after Reject (F4).** Fixed in #26 (#19).
- **What held:** a card's author could not approve it, rejected cards never reached Ask, and the MOCK label was visible in every tab.

**Prompt test suite (module A PR 2, #25, open).** 15 cases, run against the MOCK: 10/15 on the first run, 12/15 after fixing marker matching. The 3 that still fail are F1 ×2 (#17) and F3. The cases check key words and rules rather than exact text, so the same suite will run against the Claude drafter from #21.

## What we have not tested, and when we will

| Gap | Why not yet | Plan |
|---|---|---|
| Any criterion with Claude-drafted cards | Claude not connected | Run the prompt suite against #21's drafter, then the review task |
| Retrieval study (criteria 1–3) | No ground truth, no participants | Commit the ground truth and the 3 questions before any card is drafted (CP1 §4), then recruit ≥ 6 students outside the team in Phase 3 |
| Review cost (criterion 4) | No review timestamps | Record `reviewed_at` (module B) before the review task |
| Unsupported-reason audit (criterion 5) | No approved cards from a real artifact set | Two members audit every approved card, as in CP1 §4; the inputs from #16 F1 stay in the prompt suite as a regression check |
| Users outside the team | Design-rationale user tests are not done yet | At least two sessions before CP2 (design rationale owner: 周廷威) |

## What this changes for Phase 3

Group 11 could only test the MOCK, and they still found ways to produce an unsupported reason. So we will keep their inputs as a fixed adversarial set, run it on both the MOCK and the Claude drafter, and use it as the first check of criterion 5. Until #21 is merged, the 80% accuracy and the 60% acceptance criteria stay marked **not tested**. We will not report MOCK results in their place.
