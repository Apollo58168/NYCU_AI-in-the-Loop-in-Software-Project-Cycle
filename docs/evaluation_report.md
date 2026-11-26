# Interim Evaluation Report (CP2)

Status: interim, 2026-11-25. Plan: CP1 §4, which replaced the Week 3 `EVALUATION_PLAN.md` thresholds (`DECISIONS.md`, 2026-10-25). This report lists what we have measured so far and, just as important, what we have **not** measured yet.

## Summary

None of the five CP1 pass/fail criteria has been tested yet. The prototype runs end to end, but card drafting is still a keyword MOCK (Claude is connected in #21). The CP1 participant study has not been run, and no ground truth has been committed; two shorter user-testing sessions with students outside the team have (see below). So far we have evidence about **safety rules** (who can approve what, and that quotes are verbatim). We have no evidence yet about **effect** (speed, accuracy, acceptance).

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
- **No-decision cards could be approved (F2).** Chit-chat produced a card that a reviewer could approve into the decision log. Fix in #26 (open, #18): such a card cannot be saved or approved.
- **Alternatives included the reason text (F3).** Not fixed in the MOCK. The sentence is a prompt-suite case.
- **Next step unclear after Reject (F4).** Fix in #26 (open, #19).
- **What held:** a card's author could not approve it, rejected cards never reached Ask, and the MOCK label was visible in every tab.

**User testing with two students outside the team (P1, P2, 2026-11-25).** Both are 4th-year Computer Science students; each ran the app from the README (branch `c-ask-sources`, #29) with the sample history and did five tasks. Details are in `docs/design_rationale.md`.
- **Reviewer gate (criterion 5).** Both rejected the card whose reason belonged to a different decision (PostgreSQL decision, React reason), and both checked the quote against the decision before trusting a card. This is the check `check_quote` cannot make. It was one planted card each, so it shows the gate can work, not how often reviewers catch such cards.
- **Ask.** Both hit two matching bugs: "What do we use to track bugs?" cited the unrelated polling card (shared word "use"), and a long Chinese question found nothing. Both are fixed in #29 (98291db) and kept as test cases.
- **Not found.** Both read "No approved decision found." as "no such decision", although one card was waiting for review and another had been rejected. Not fixed yet.
- **Limits.** Two friendly participants, the MOCK drafter, a fixed sample history and no timing: these sessions do not count toward criteria 1–4.

**Prompt test suite (module A PR 2, #25, open).** 15 cases, run against the MOCK: 10/15 on the first run, 12/15 after fixing marker matching. The 3 that still fail are F1 ×2 (#17) and F3. The cases check key words and rules rather than exact text, so the same suite will run against the Claude drafter from #21.

## What we have not tested, and when we will

| Gap | Why not yet | Plan |
|---|---|---|
| Any criterion with Claude-drafted cards | Claude not connected | Run the prompt suite against #21's drafter, then the review task |
| Retrieval study (criteria 1–3) | No ground truth, no participants | Commit the ground truth and the 3 questions before any card is drafted (CP1 §4), then recruit ≥ 6 students outside the team in Phase 3 |
| Review cost (criterion 4) | No review timestamps | Record `reviewed_at` (module B) before the review task |
| Unsupported-reason audit (criterion 5) | No approved cards from a real artifact set | Two members audit every approved card, as in CP1 §4; the inputs from #16 F1 stay in the prompt suite as a regression check |
| Users outside the team | Two sessions done (P1, P2), but with the MOCK, a fixed sample history and no timing | In Phase 3 (CP3), after #21 connects Claude: 周廷威 repeats the same tasks with Claude-drafted cards as part of the retrieval study above. P1 and P2 are not counted among its ≥ 6 participants, because they have already seen the sample cards. |

## What this changes for Phase 3

Group 11 could only test the MOCK, and they still found ways to produce an unsupported reason. So we will keep their inputs as a fixed adversarial set, run it on both the MOCK and the Claude drafter, and use it as the first check of criterion 5. Until #21 is merged, the 80% accuracy and the 60% acceptance criteria stay marked **not tested**. We will not report MOCK results in their place.
