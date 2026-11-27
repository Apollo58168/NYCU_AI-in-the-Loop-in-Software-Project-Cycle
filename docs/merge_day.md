# Merge Day: Team Worksheet

Group 07 (DecisionTrace). Merge day 2026-11-27, last merge and fresh-clone test just after midnight on 11/28. Steward: 蔡尚融. Times are Taiwan time.

Who was there: all four (蔡尚融, 蔡凱旭, 周廷威, 林彥宇), in an online meeting.

---

## Part 0 | The steward's merge plan

Written by 蔡尚融 as the entry *2026-11-27 — Merge plan (steward: 蔡尚融)* in [`DECISIONS.md`](../DECISIONS.md), opened as #37 and merged on 11/27 at 16:24, before the first PR merge (21:44). 周廷威 reviewed it and found one conflict it had missed (#32 after #37, see Part 2).

| # | Branch / PR | What it does (one line) | Author | Ready? | Touches the same files as… |
|---|---|---|---|---|---|
| 1 | #29 `c-ask-sources` | Cited ranked answers, sample data, five-step demo in the README | 周廷威 | yes | README.md: #36; PROMPT_LOG.md: #34, #35, #36 |
| 2 | #32 `docs/design-rationale` | Design rationale with two user-testing sessions | 周廷威 | yes | DECISIONS.md: #30, #37 |
| 3 | #33 `docs/eval-user-testing` | User-testing results in the evaluation report | 周廷威 | yes | `docs/evaluation_report.md` only |
| 4 | #30 `docs/walking-skeleton-worksheet` | Walking-skeleton worksheet | 蔡尚融 | yes | DECISIONS.md: #32 |
| 5 | #34 `fix/14-restore-prompt-log` | Restore the module C and D entries in PROMPT_LOG.md | 蔡凱旭 | yes | PROMPT_LOG.md: #29, #35, #36 |
| 6 | #35 `fix/17-reason-same-decision` | Reason only from the decision's sentence or the next one | 蔡凱旭 | yes | drafter.py, test_drafter.py, cases.json: #36 |
| 7 | #36 `d-claude-drafter` | Claude drafter, MOCK without a key (#21) | 蔡凱旭 | yes | README.md: #29; drafter.py and more: #35 |

**Merge order:** #29 → #32 → #33 → #30 → #34 → #35 → #36. #32 and #33 cite #29's commits; #36 is built on #35 and contains its commits, so it goes last.

**Conflicts we expected:** `README.md` when #36 goes in (keep all three Code layout rows); added after 周廷威's review: `DECISIONS.md` when #32 goes in after #37.

**What "done" means:** every open PR merged or closed with a reason; `uv run pytest` passes on `main` after each merge; someone other than the steward clones `main` into a new folder and, following only the README, does the main task with no API key.

**PRs we will close without merging:** none.

---

## Part 1 | Agree the plan

| Merge # | PR | Driver | Approval |
|---|---|---|---|
| 1–3 | #29, #32, #33 | 蔡凱旭 | 蔡凱旭 (11/25) |
| 4 | #30 | 蔡尚融 | 林彥宇 (11/25) |
| 5–6 | #34, #35 | 蔡尚融 | 蔡尚融 (steward, 11/27) |
| 7 | #36 | 林彥宇 | 林彥宇 (11/28) |

Three drivers. Reviewer on screen: the PR's author watched the driver's shared screen (周廷威 for #29, #32, #33; 蔡尚融 for #30; 蔡凱旭 for #34, #35, #36).

---

## Part 2 | Merge one at a time

| # | PR | Conflicts? (where) | How we resolved them | Tests after merge | App runs on `main`? |
|---|---|---|---|---|---|
| 1 | #29 | none | — | not recorded separately (trial-merged locally first) | not recorded |
| 2 | #32 | `DECISIONS.md`, with #37 (both append at the end) | 周廷威 rebased #32 before it was merged, entries in date order | not recorded separately | not recorded |
| 3 | #33 | none | — | 116 passed, 3 xfailed; PROMPT_LOG 7 entries | yes |
| 4 | #30 | none | — | 116 passed, 3 xfailed; PROMPT_LOG 7 | yes |
| 5 | #34 | none | — | 116 passed, 3 xfailed; PROMPT_LOG 9 | yes |
| 6 | #35 | none | — | 126 passed, 3 xfailed; PROMPT_LOG 10 | yes |
| 7 | #36 | `README.md`, with #29 (Code layout table); then GitHub marked it conflicting after #35 merged | 蔡凱旭 merged `main` into the branch and kept all three rows (6d3d161). The second time, the local merge was clean; the branches had two merge bases (35af3c8, 26b412a) because #36 already contained #35. 蔡凱旭 merged `main` again (f8adce2) and GitHub showed it as mergeable | 155 passed, 4 xfailed; PROMPT_LOG 12 | yes (fresh-clone test) |

Nothing broke on `main`, so nothing was reverted.

---

## Part 3 | The fresh-clone test

Run by 林彥宇 with Claude Code on his laptop (macOS), at `main` af98de2, right after #36 merged. Claude Code ran the commands and clicked through the app in the browser; 林彥宇 watched. No `ANTHROPIC_API_KEY`, so Draft used the MOCK.

- Cloned into an empty folder, with no `.venv` and no `data/`. README's clone command uses the SSH URL (`git@github.com:…`); the run used the HTTPS URL.
- `uv sync`: OK. `uv run pytest`: 155 passed, 4 xfailed.
- `uv run streamlit run app/main.py`: the app opened, with "No ANTHROPIC_API_KEY set, so the keyword MOCK drafts the card."
- Step 1, Load sample data: "Loaded 6 sample cards: 4 approved, 1 rejected, 1 draft."
- Step 2, Ask: "Why do we use polling?" cited card s-poll with its quote. "Did we switch to server-sent events?" gave "No approved decision found." Both match the README.
- Step 3, Draft (author Alice, sample discussion from the sidebar): MOCK card labelled "MOCK draft, not AI - needs human review", confidence low, with the warning that the reason comes from the next sentence. Save as draft showed "Saved as draft. It now waits in the Review tab: ask a teammate…". The copy icon on the sample block did not put the text on the clipboard in this run (unclear whether the click missed), so the text was typed in.
- Step 4, Review: Alice approving her own card gave "You wrote this card, so a teammate has to review it." Bob approving gave "Card 2fb0aa41 approved by Bob."
- Step 5, Approved cards: the new card is listed first, "drafted by MOCK (not AI)". Reset data (after ticking the box) gave "All cards deleted." and "No approved cards yet."

| | |
|---|---|
| Who did it | 林彥宇 |
| Did the README work without help? (yes / partly / no) | partly: everything worked, but the clone step uses the SSH URL |
| What was missing from the README? | An HTTPS clone URL, for anyone without an SSH key |
| Did the main task work end to end? | yes, with the MOCK (no API key) |
| Any API key or setup step that only one person knows? | The run with an API key was not done. The README says to copy `.env.example` to `.env` and fill in the key |

Not blocking, noted during the test:
1. README step 2 uses the SSH clone URL; HTTPS works for anyone. 林彥宇 fixes it in a small PR.
2. ([#38](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/38)) The MOCK copies the speaker into the decision: "Bob: We decided to use polling every 10 seconds instead of WebSockets."
3. ([#39](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/39)) The sample discussion drafts the same decision as the approved sample card s-poll, so after the five steps Approved cards shows polling twice.

---

## Part 4 | Record the outcome

The outcome is written under the merge plan in [`DECISIONS.md`](../DECISIONS.md).

**Team check:**

1. What made merging harder than it needed to be? Many PRs add an entry at the end of the same files (`DECISIONS.md`, `PROMPT_LOG.md`). That is how #32 conflicted with #37, and how 37d14fa once dropped two `PROMPT_LOG.md` entries while resolving such a conflict.
2. One habit we will change for Phase 3: a branch built on someone else's open PR waits until that PR is merged, then rebases onto `main`. #36 merged `main` in early while #35 was still open, which left two merge bases and made GitHub mark it as conflicting.
3. Could each of us run the prototype and do the main task without help? Yes, all four of us.

---

## Quick checklist

- [x] The merge plan was in `DECISIONS.md` before the session started (#37, merged 16:24; first PR merge 21:44)
- [x] All four of us were there (online meeting)
- [x] Every open PR was merged or closed with a reason (all seven merged)
- [ ] Tests and the app were run on `main` after each merge: tests and app for #33, #30, #34, #35 and #36; after #29 and #32, not recorded
- [x] Someone other than the steward ran the fresh-clone test (林彥宇)
- [x] The outcome is written under the merge plan
- [x] This worksheet is saved as `docs/merge_day.md`
