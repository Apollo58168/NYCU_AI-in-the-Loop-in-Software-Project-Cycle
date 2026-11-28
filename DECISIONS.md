# Decisions Log

**Current code steward:** 林彥宇 ([**Apollo58168**](https://github.com/Apollo58168), @Apollo58168), since 2026-11-28 (see the entry *2026-11-28 — Steward handover: 蔡尚融 → 林彥宇* below).

## 2026-09-21 — Initial code steward
**What:** [**Apollo**](https://github.com/Apollo58168) is the initial code steward for the team.  
**Why:** Apollo volunteered and has the most Git experience so far.

## 2026-10-25 — CP1 evaluation thresholds replace the Week 3 plan
**What:** CP1 §4 replaces the Week 3 `EVALUATION_PLAN.md` thresholds. The 80% accuracy and 30% faster-median criteria stay. The median usefulness rating of at least 4/5 is now a diagnostic, not pass/fail. New pass/fail criteria: reviewers accept at least 60% of AI cards at a median of at most 2 min per card, and no approved card has an unsupported reason. The time criterion also requires every DecisionTrace participant to be faster than every manual participant, and the "not recorded" question is reported separately.  
**Why:** A usefulness rating from participants we recruit through our own contacts is the measure most open to politeness bias. Review cost and unsupported reasons are the risks our two interviews (R1, R2) raised.  
**Alternative rejected:** Keeping the Week 3 thresholds unchanged, which left review cost and hallucinated reasons unmeasured.  
**Led by:** 周廷威 (CP1 draft); accepted by the team through the review of the CP1 PR

## 2026-11-23 — 周廷威 and 蔡尚融 swap their remaining work
**What:** 周廷威 and 蔡尚融 swap every assignment still open in our prototype split plan. Work already merged keeps its author: #8 project setup (周廷威), #9 Ask tab (蔡尚融) and #12 Approved cards tab (周廷威).
- Module A's PR 2 (prompt test suite) and the 11/27 merge-day steward turn go to 蔡尚融.
- Module C PR 2 (sources and ranking, Q&A tests, sample data, demo steps), the design rationale and user tests, and the 11/24–25 steward turn go to 周廷威.
- Steward reviews swap with the roles: 周廷威 reviews module B's PRs, and 蔡尚融 reviews module D's PR 2.

**Why:** 周廷威 had already done two pieces of module A (#8 setup before the session and #12 in it), while 蔡尚融's module C still had its larger PR 2 ahead. Swapping the remaining work evens out the load between the two before the 11/29 CP2 deadline. Proposed by 林彥宇 after the walking-skeleton session.  
**Led by:** 林彥宇

## 2026-11-23 — Steward handover: 林彥宇 → 周廷威
**What:** 林彥宇 hands the code steward role to 周廷威 after the walking-skeleton session. 周廷威 is steward on 11/24–25.  
**Done in 林彥宇's turn:** reviewed and merged #13 (walking skeleton → main). It covers #9 Ask, #10 Draft, #11 Review and #12 Approved cards; 61 tests pass, and the main flow runs end to end.  
**Handed over:**
- [#14](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/14) is open: restore the module C and D entries in `PROMPT_LOG.md` (assigned to 蔡凱旭, due 11/26). 周廷威 reviews and merges the fix.
- This handover PR itself, which 林彥宇 cannot merge.
- Module B's PR 2 (林彥宇) will be reviewed by 周廷威.
- #9, #10 and #11 were merged into `walking-skeleton` without a recorded approval. From now on, every PR needs a steward approval with a substantive comment before it is merged.

**Next handover:** 周廷威 → 蔡凱旭 on 11/26.

## 2026-11-23 — Walking skeleton fakes the drafter with a keyword MOCK
**What:** In the walking-skeleton session the AI step is a keyword-rule MOCK drafter, labelled "MOCK draft, not AI" in every tab. It keeps the real `draft_card(source_text, author, source)` signature, so module D's PR 2 (#21) can put Claude behind it without changing the other tabs.  
**Why:** The session was about the four pieces connecting. The Claude API key had not been granted yet, and waiting for it would have blocked Review, Ask and Approved cards.  
**Alternative rejected:** Waiting for the API key before connecting the pieces.  
**Led by:** whole team, in the session (decision section of #13). Recorded here late, on 2026-11-25, with `docs/walking_skeleton.md`.

## 2026-11-24 — Three AI usage rules become checkable from a PR
**What:** Three rules in `AI_GUIDELINES.md` now name what a teammate can see in a PR:
- the "AI assistance" section lists the tool and model, the generated files, the instruction and what the author changed;
- every merge needs a non-author approval with a comment that asks a question or names a file, line or case, and "LGTM" does not count;
- AI-written code shows one deliberate break with the number of failing tests, plus one input tried by hand in the app.

**Why:** In our last seven PRs (#8–#13, #15), all were mostly AI-generated. Only #9 and #10 named the files the AI wrote. #9–#11 were merged without an approval, and #10 and #12 got only "LGTM". Group 11's review (#16) found three drafter bugs (F1–F3) that the 15 drafter tests did not catch.

**Alternative rejected:** Keeping the Week 3 wording ("states whether AI was used", "a teammate can explain the result"), which every one of those PRs already met on paper.

**Led by:** 林彥宇 (proposed in this PR); accepted through the steward's review.

## 2026-11-24 — Prompt test suite checks key words, and runs against any drafter
**What:** The CP2 prompt test suite (`docs/prompt_test_suite.md`, 15 cases) checks the draft card by key words and rules (quote is verbatim, no reason from an unrelated sentence, chit-chat gives no decision), not by exact text, and takes the drafter as a parameter. The same cases run against the keyword MOCK now and against the Claude drafter after #21. Known MOCK failures run as strict xfail.  
**Why:** Claude will word decisions and reasons differently from the MOCK, so exact-text cases would all break when #21 merges and would have to be rewritten right before CP2. Run 1 also found that "undecided" and "disagreed" were drafted as decisions; the MOCK now matches English markers as whole words, because the MOCK stays the fallback whenever no API key is set.  
**Alternative rejected:** A PromptFoo config like the Week 10 lab. It can only test a prompt and an API, and we have neither until #21; the Python runner tests the MOCK today and can still call the Claude drafter later.  
**Led by:** 蔡尚融 (module A PR 2).

## 2026-11-25 — Steward turns and PR timing until CP2
**What:**
- Steward turns until the 11/29 deadline. Each steward approves the listed PRs with a substantive comment:

  | Turn | Steward | Reviews and merges |
  | --- | --- | --- |
  | 11/24–25 | 周廷威 | #24 (README status), #27 (this schedule), #28 (interim evaluation report) |
  | 11/26 | 蔡凱旭 | #25 (prompt suite), #26 (#18/#19), #29 (module C PR 2: cited answers) |
  | 11/27 (merge day) | 蔡尚融 | the fix for #14, the PR for #17, #30 (walking-skeleton worksheet); writes the merge plan |
  | 11/28–29 | 林彥宇 | the PR for #21 (Claude drafter); final CP2 check of `main` |

- 蔡凱旭 opens the PRs for #17 and #21 by 11/26, as drafts if they are not finished, so that they appear in the merge plan.
- Anything merged after merge day (expected: #21) is a follow-up merge on 11/28. It is recorded under the merge-plan entry, with the same check: someone other than the steward clones `main` fresh and runs the main task.

**Why:** 蔡尚融 pointed out two problems. First, #17 and #21 are due 11/28, after the 11/27 merge day. Second, nobody was steward on 11/28–29. Every member needs two steward approvals with a substantive comment for CP2. 周廷威 already has them (#22, #23). The table gives 蔡凱旭 and 蔡尚融 two each, and gives 林彥宇 the second one (the first was #13).

**Alternative rejected:** Moving merge day to 11/28, which leaves no buffer before the 11/29 deadline. Also rejected: one steward for all remaining days, which would leave the other two short of approvals.

**Led by:** 林彥宇, after 蔡尚融 raised the timing problem; accepted through the steward's review of this PR.

## 2026-11-25 — Steward handover: 周廷威 → 蔡凱旭
**What:** 周廷威 hands the code steward role to 蔡凱旭 at the end of the 11/24–25 turn. 蔡凱旭 is steward on 11/26.  
**Done in 周廷威's turn:**
- Reviewed and merged #15 (role swap and handover), #22 (Week 12 PR template), #23 (three checkable AI rules), #24 (README status line) and #28 (interim evaluation report), each with a substantive approval comment.
- Approved #27 (steward turns until CP2); its author 林彥宇 merged it after adding the rows I asked for.
- Approved #25 (prompt test suite) with a question on how known failures will be kept per drafter; 蔡尚融 answered in the PR. It stays for 蔡凱旭 to merge, as #27 says.
- `main` passes `uv run pytest` (61 passed) after #28.

**Handed over:**
- #25 (prompt test suite), #26 (module B PR 2: #18, #19) and #29 (module C PR 2, 周廷威): review and merge on 11/26. #25 and #26 both add to the end of `PROMPT_LOG.md`; keep both entries when resolving.
- [#14](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/14): restore the module C and D entries in `PROMPT_LOG.md` (蔡凱旭, due 11/26).
- #17 and #21: open the PRs on 11/26 (as drafts if not finished), so that the merge plan lists them.
- This handover PR itself, which 周廷威 cannot merge.

**Next handover:** 蔡凱旭 → 蔡尚融 at the end of 11/26.

## 2026-11-25 — Ask matching changed after user testing
**What:** In Ask, the word "use" is ignored, and a question of four or more keywords needs at least two keywords in common with a card (#29, 98291db). This replaces the rule that a card must share a third of the question's keywords.  
**Why:** In the user-testing sessions (P1, P2; `docs/design_rationale.md`), "What do we use to track bugs?" cited the unrelated polling card only because both contain "use", and the long Chinese question "為什麼即時看板用 polling，不用 WebSockets？" found nothing, because a Chinese sentence turns into many character pairs and the real match fell below a third. The new rule still rejects the earlier false match, where only "server" was shared.  
**Alternative rejected:** Matching with embeddings or Claude, which needs the API key from #21 and a new evaluation; keeping the one-third rule, which fails on Chinese.  
**Led by:** 周廷威

## 2026-11-26 — Steward handover: 蔡凱旭 → 蔡尚融
**What:** 蔡凱旭 hands the code steward role to 蔡尚融 at the end of the 11/26 turn. 蔡尚融 is steward on 11/27 (merge day). Recorded by 蔡尚融 from the PR history; times are Taiwan time.  
**Done in 蔡凱旭's turn:**
- Merged #25 (prompt test suite) and #31 (handover 周廷威 → 蔡凱旭) on 11/26. Both were approved on 11/25 with a question: on #25, whether `alternatives` should use keyword matching like decision and reason (蔡尚融 answered to keep it strict); on #31, whether the entry should link #34–#36 (周廷威 answered to keep it as it stood on 11/25).
- Merged #26 (#18, #19) on 11/26, after checking 林彥宇's follow-up commit a59a811, which was the answer to his 11/25 question about cards saved with the old "No decision found" text.
- #29: approved on 11/25 with a question about replaced decisions in `rank()`; 周廷威 answered in d9baeb8 (cited cards show their draft date), and 蔡凱旭 checked it on 11/26. 周廷威 rebased #29 onto `main` in 210f059 late on 11/26; it was not merged in this turn.
- Approved #32 and #33 on 11/25; not merged in this turn (both wait for #29).
- Opened #34 (#14), #35 (#17) and #36 (#21) on 11/25, and marked #35 and #36 ready for review on 11/26, as #27 asked.
- `uv run pytest` on `main` after the merges: not recorded.

**Handed over:**
- #29 → #32 → #33: approved by 蔡凱旭, to merge in that order on merge day.
- #34 (#14) and #35 (#17): steward approval with a substantive comment, then merge (as #27 lists for 11/27).
- #30 (walking-skeleton worksheet, 蔡尚融): approved by 林彥宇 on 11/25; the steward merges it.
- #36 (#21, Claude drafter): planned for 11/28 in #27; see the merge plan below.
- The merge plan below, and this handover entry.

**Next handover:** 蔡尚融 → 林彥宇 at the end of 11/27.

## 2026-11-27 — Merge plan (steward: 蔡尚融)
**Open PRs** (from `gh pr list` on the morning of 11/27):

| # | PR / branch | What it does | Author | Ready? | Touches the same files as… |
| --- | --- | --- | --- | --- | --- |
| 1 | #29 `c-ask-sources` | Cited ranked answers, sample data, five-step demo in the README | 周廷威 | yes (approved by 蔡凱旭; rebased in 210f059) | README.md: #36; PROMPT_LOG.md: #34, #35, #36 |
| 2 | #32 `docs/design-rationale` | Design rationale with two user-testing sessions | 周廷威 | yes (approved by 蔡凱旭 on 11/25; new commits on 11/27, read them on screen before merging) | DECISIONS.md: #30 |
| 3 | #33 `docs/eval-user-testing` | User-testing results in the evaluation report | 周廷威 | yes (approved by 蔡凱旭 on 11/25; new commits on 11/27, read them on screen before merging) | `docs/evaluation_report.md` only |
| 4 | #30 `docs/walking-skeleton-worksheet` | Walking-skeleton worksheet | 蔡尚融 | yes (approved by 林彥宇) | DECISIONS.md: #32 |
| 5 | #34 `fix/14-restore-prompt-log` | Restore the module C and D entries in PROMPT_LOG.md (Closes #14) | 蔡凱旭 | yes, needs the steward approval | PROMPT_LOG.md: #29, #35, #36 |
| 6 | #35 `fix/17-reason-same-decision` | Reason only from the decision's sentence or the next one (Closes #17) | 蔡凱旭 | yes, needs the steward approval | drafter.py, test_drafter.py, cases.json: #36 |
| 7 | #36 `d-claude-drafter` | Claude drafter, MOCK without a key (#21) | 蔡凱旭 | yes, needs a non-author approval | README.md: #29; drafter.py and more: #35 (#36 contains #35's commits) |

**Merge order and why:** #29 → #32 → #33 → #30 → #34 → #35 → #36.

> 1. #29 first: #32 and #33 cite its commits (for example 98291db), so it goes in before the documents that describe it.
> 2. #32, #33 and #30: documents only.
> 3. #34: PROMPT_LOG.md only; it inserts in the middle of the file.
> 4. #35, then #36: #36 is built on #35's drafter and contains its commits, so it goes last.

#36 moves from 11/28 (#27) to today, because it is ready and the trial merge below passes; this leaves 11/28–29 as a buffer.

**Conflicts we expect** (trial merge of all seven PRs in this order on top of `main` at e2689ed, on 11/27):

> - `DECISIONS.md`, when #32 goes in after this merge plan: both add an entry at the end of the file (found by 周廷威 in the review of #37; my trial merge started from `main` without the merge plan). 周廷威 rebases #32 before the session and keeps date order: #32's 2026-11-25 entry goes before the 2026-11-26 handover. #30 still merges cleanly, because it inserts in the middle of the file.
> - `README.md`, when #36 goes in: #29 adds two rows (`app/sidebar.py`, `decisiontrace/sample_data.py`) and the "Try it in five steps" section after the prompt-suite row of the Code layout table, and #36 adds one row (drafter / llm / prompt) at the same place. Keep all three rows, with no blank line between them: #36's row, then sidebar, then sample_data, then the five steps. 蔡凱旭 merges `main` into `d-claude-drafter`, resolves it, runs the tests and pushes before #36 is merged.
> - `PROMPT_LOG.md` merges cleanly every time, but 37d14fa once lost two entries in a conflict, so check `grep -c '^## ' PROMPT_LOG.md` after each merge: 6 now, then 7 after #29, 9 after #34, 10 after #35 and 12 after #36.
> - Result after all seven: `uv run pytest` 155 passed, 4 xfailed; MOCK prompt suite 15 of 19 (T3, E11, E12, E13 are the known MOCK failures).

**Who drives each merge** (at least three drivers):

| PR | Driver | Approval |
| --- | --- | --- |
| #29, #32, #33 | 蔡凱旭 | 蔡凱旭 (11/25) |
| #30 | 蔡尚融 | 林彥宇 (11/25) |
| #34, #35 | 蔡尚融 | 蔡尚融 (steward), with a substantive comment |
| #36 | 林彥宇 | 林彥宇, with a substantive comment |

**What "done" means today:** every open PR is merged or closed with a reason; `uv run pytest` passes on `main` after each merge; and someone other than the steward (林彥宇) clones `main` into a new folder and, following only the README, does the main task with no API key: Draft → Review → Ask, with the card in Approved cards.

**PRs we will close without merging:** none.

**Outcome (2026-11-27 to 11-28):** merged all seven open PRs and closed none: #29, #32, #33 (driven by 蔡凱旭), #30, #34, #35 (蔡尚融) and #36 (approved and merged by 林彥宇, 11/28 00:17). #34 and #35 closed #14 and #17. The merge plan itself went in first as #37.

Conflicts, and how they were resolved:
- `DECISIONS.md`, #32 after #37: both added an entry at the end. Found by 周廷威 in the review of #37 (the steward's trial merge had started from `main` without #37). 周廷威 rebased #32 in date order before it was merged.
- `README.md`, #36 after #29: as planned. 蔡凱旭 merged `main` into `d-claude-drafter` (6d3d161) and kept all three Code layout rows in the plan's order.
- #36 after #35: GitHub marked #36 as conflicting, but merging `main` (e629316) into it locally was clean, with 155 passed, 4 xfailed. #36 already contained #35's commits and had `main` merged in, so the two branches had two merge bases (35af3c8 and 26b412a). 蔡凱旭 merged `main` into the branch again (f8adce2); GitHub then showed it as mergeable, with only #36's 18 files in the diff.

`main` after each merge (`uv run pytest`; `grep -c '^## ' PROMPT_LOG.md`): after #33, 116 passed, 3 xfailed, 7 entries; after #30, the same; after #34, 116 passed, 3 xfailed, 9 entries; after #35, 126 passed, 3 xfailed, 10 entries; after #36, 155 passed, 4 xfailed, 12 entries. The app started on `main` after #33, #30, #34 and #35. After #29 and #32: not recorded separately (蔡凱旭 trial-merged each one locally before merging).

Fresh-clone test by 林彥宇 (run with Claude Code, see `docs/merge_day.md`) at af98de2, right after #36 merged, with no API key (MOCK): worked. `uv sync` OK, 155 passed, 4 xfailed, and all five README steps worked in the browser (details in `docs/merge_day.md`). README's clone command uses the SSH URL, so someone without an SSH key would stop there; the run used HTTPS. The run with an API key was not done.

`main` is green: 155 passed, 4 xfailed; MOCK prompt suite 15 of 19 (T3, E11, E12, E13 are the known MOCK failures).

Absent: nobody. All four took part, in an online meeting.

Left for after merge day: README clone URL to HTTPS (林彥宇, small PR on 11/28); #38 (MOCK puts the speaker's name in the decision; 蔡凱旭, due 12/7) and #39 (the sample discussion repeats the s-poll decision; 周廷威, due 12/7), from the fresh-clone test notes; a Draft run with an API key on a fresh clone.

## 2026-11-28 — Steward handover: 蔡尚融 → 林彥宇
**What:** 蔡尚融 hands the code steward role to 林彥宇 at the end of merge day, after #36 was merged (11/28 00:17) and the fresh-clone test was done. 林彥宇 is steward on 11/28–29, until CP2 is handed in, as #27 planned. Recorded by 林彥宇 from the PR history; times are Taiwan time.  
**Taken over:** merge day is recorded under the 2026-11-27 merge plan above (#40). From that turn: #40 itself, the README clone URL (林彥宇), #38 and #39 (Phase 3), and the follow-up PRs for the evaluation report and `CLAUDE.md`.

**Done in 林彥宇's turn:**
- #41 (evaluation report after merge day, 周廷威): commented that "MOCK label visible in every tab" was still there and that the criterion 5 cell should say how many cases were repeated. 周廷威 changed both in aedb140. Approved and merged on 11/28 at 02:21. This also covers the #28 wording that 林彥宇 had promised to fix.
- #42 (README clones with the HTTPS URL, 林彥宇): approved by 周廷威, who checked that the URL works without credentials. Merged on 11/28 at 02:22.
- #43 (`CLAUDE.md`, 蔡凱旭): checked its "How it fails" claims against `main`, and checked that changing one word of `prompts/draft_card.md` fails the drift test. Suggested adding that only four cases were repeated. Approved and merged on 11/28 at 17:06.
- #40 (merge-day outcome and `docs/merge_day.md`, 蔡尚融): asked for the Outcome to say that the fresh-clone test was run with Claude Code. 蔡尚融 changed it in b83f444; approved and merged by 林彥宇 on 11/28 at 17:11.
- Final check of `main` on a fresh HTTPS clone at 4864a55, with no API key:
  - `uv run pytest`: 156 passed, 4 xfailed.
  - MOCK prompt suite: 15 of 19 (T3, E11, E12, E13 are the known failures).
  - The app starts.
  - No `.env`, `data/cards.json` or API key is committed.

**Left after CP2:**
- [#38](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/38) (蔡凱旭) and [#39](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/issues/39) (周廷威), both due 12/7.
- Optional: in `CLAUDE.md`, add "only four cases repeated" next to "run 7 passed 19 of 19" (suggested in #43).
- A Draft run with an API key on a fresh clone (not done on merge day).

**Next handover:** the Phase 3 steward schedule is not decided yet; the team agrees it after CP2.
