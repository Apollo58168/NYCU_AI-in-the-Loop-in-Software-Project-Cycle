# Interim Evaluation Report (CP2)

Status: interim, 2026-11-27 (after merge day). Plan: CP1 §4, which replaced the Week 3 `EVALUATION_PLAN.md` thresholds (`DECISIONS.md`, 2026-10-25). This report lists what we have measured so far and, just as important, what we have **not** measured yet.

## Summary

None of the five CP1 pass/fail criteria has been tested yet. The prototype runs end to end. Draft uses Claude when `ANTHROPIC_API_KEY` is set and the keyword MOCK otherwise (#36, #21); so far Claude has run only through the prompt test suite, and no participant has reviewed a Claude-drafted card. The CP1 participant study has not been run, and no ground truth has been committed; two shorter user-testing sessions with students outside the team have (see below). So far we have evidence about **safety rules** (who can approve what, and that quotes are verbatim). We have no evidence yet about **effect** (speed, accuracy, acceptance).

## CP1 §4 criteria

| # | Criterion (CP1 §4) | Status | Evidence so far |
|---|---|---|---|
| 1 | ≥ 6 retrieval participants (≥ 3 per group), ≥ 2 reviewer participants | **Not tested** | 0 participants. The ground-truth list and the 3 "why" questions are not committed yet. |
| 2 | DecisionTrace group ≥ 80% correct on the 2 scored questions, no lower than manual | **Not tested** | No retrieval study yet. |
| 3 | DecisionTrace median time ≥ 30% lower, and full separation of participant medians | **Not tested** | No retrieval study yet. |
| 4 | Reviewers approve or edit ≥ 60% of AI cards, median ≤ 2 min per card | **Not tested** | Every card a person has reviewed so far (Group 11, P1, P2) came from the MOCK, so its acceptance rate says nothing about Claude's drafts. Review time is not recorded yet (no `reviewed_at`). |
| 5 | No approved card has a reason its sources do not support (hard rule) | **Risk found, partly guarded** | See "What we have tested". The MOCK attached a verbatim but unrelated reason (Group 11, #16 F1); #35 narrows this, but an unrelated "because" right after the decision still gets through, marked confidence `low` with a warning. Claude passed these cases in the prompt suite (19/19 in run 7; only E1, E2, E10 and E11 were repeated), which is not evidence that it never attaches an unrelated reason. A reviewer can still approve such a card. |

## What we have tested

**Automated tests.** `uv run pytest` on `main` gives 155 passed, 4 xfailed (the xfails are the MOCK's known prompt-suite failures). These cover the verbatim-quote check (`check_quote`), the "author cannot review" rule, "Ask uses approved cards only", and the four tabs through Streamlit `AppTest`.

**Cross-team review by Group 11 (#16, 2026-11-24).** This is our first look from outside the team. They ran the app from the README and tried to make the drafter fail:
- **Unsupported reasons (criterion 5).** With two decisions in one text, the Reason and Quote came from the other decision. A lunch sentence was given as the reason for choosing PostgreSQL (F1). The quote was verbatim, so `check_quote` passed, but it did not support the decision. **A verbatim quote is not enough to meet criterion 5.** Fixed for the MOCK in #35: the reason now comes only from the decision's own sentence or the one right after it. An unrelated "because" in that next sentence still gets through, with confidence `low` and a warning (prompt-suite cases E12, E13).
- **No-decision cards could be approved (F2).** Chit-chat produced a card that a reviewer could approve into the decision log. Fixed in #26 (#18): such a card cannot be saved or approved.
- **Alternatives included the reason text (F3).** Not fixed in the MOCK. The sentence is a prompt-suite case.
- **Next step unclear after Reject (F4).** Fixed in #26 (#19).
- **What held:** a card's author could not approve it, rejected cards never reached Ask, and the MOCK label was visible in the Draft, Review and Approved cards tabs.

**User testing with two students outside the team (P1, P2, 2026-11-25).** Both are 4th-year Computer Science students; each ran the app from the README (branch `c-ask-sources`, #29) with the sample history and did five tasks. Details are in `docs/design_rationale.md`.
- **Reviewer gate (criterion 5).** Both rejected the card whose reason belonged to a different decision (PostgreSQL decision, React reason), and both checked the quote against the decision before trusting a card. This is the check `check_quote` cannot make. It was one planted card each, so it shows the gate can work, not how often reviewers catch such cards.
- **Ask.** Both hit two matching bugs: "What do we use to track bugs?" cited the unrelated polling card (shared word "use"), and a long Chinese question found nothing. Both are fixed in #29 (98291db) and kept as test cases.
- **Not found.** Both read "No approved decision found." as "no such decision", although one card was waiting for review and another had been rejected. Not fixed yet.
- **Limits.** Two friendly participants, the MOCK drafter, a fixed sample history and no timing: these sessions do not count toward criteria 1–4.

**Prompt test suite (#25, extended in #35 and #36; `docs/prompt_test_suite.md`).** 19 cases that check key words and rules rather than exact text, so the same cases run against both drafters.
- **MOCK:** 10/15 on the first run, 12/15 after fixing marker matching (#25), 14/17 after #35. Now 15/19: T3, E11, E12 and E13 fail and run as strict xfail.
- **Claude (#36):** 16/16 on the first run, so we added E11 (a decision later replaced by another). It failed: Claude drafted the outdated decision. After a prompt fix, 17/17, and 19/19 after rebasing on #35. Only E1, E2, E10 and E11 were repeated (3 runs each), so run-to-run variation is not measured for the other cases.

## What we have not tested, and when we will

| Gap | Why not yet | Plan |
|---|---|---|
| Any criterion with Claude-drafted cards | Claude is connected (#36), but only the prompt suite has run on it | Run the review task with Claude-drafted cards in Phase 3 |
| Retrieval study (criteria 1–3) | No ground truth, no participants | Commit the ground truth and the 3 questions before any card is drafted (CP1 §4), then recruit ≥ 6 students outside the team in Phase 3 |
| Review cost (criterion 4) | No review timestamps | Record `reviewed_at` (module B) before the review task |
| Unsupported-reason audit (criterion 5) | No approved cards from a real artifact set. `check_quote` only checks that the quote is verbatim, so a Claude card whose quote does not support its reason also passes | Two members audit every approved card, as in CP1 §4; the inputs from #16 F1 stay in the prompt suite as a regression check |
| Users outside the team | Two sessions done (P1, P2), but with the MOCK, a fixed sample history and no timing | In Phase 3 (CP3), with Claude connected (#36): 周廷威 repeats the same tasks with Claude-drafted cards as part of the retrieval study above. P1 and P2 are not counted among its ≥ 6 participants, because they have already seen the sample cards. |

## What this changes for Phase 3

Group 11 could only test the MOCK, and they still found ways to produce an unsupported reason. So we will keep their inputs as a fixed adversarial set, run it on both the MOCK and the Claude drafter, and use it as the first check of criterion 5. Claude is now connected, but the 80% accuracy and the 60% acceptance criteria stay marked **not tested** until the Phase 3 studies. We will not report MOCK results in their place.
