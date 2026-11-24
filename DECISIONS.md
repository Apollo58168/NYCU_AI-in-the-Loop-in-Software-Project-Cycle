# Decisions Log

**Current code steward:** 周廷威 ([**gainsborouo**](https://github.com/gainsborouo), @gainsborouo), since 2026-11-23 (see the entry *2026-11-23 — Steward handover: 林彥宇 → 周廷威* below).

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

## 2026-11-24 — Three AI usage rules become checkable from a PR
**What:** Three rules in `AI_GUIDELINES.md` now name what a teammate can see in a PR:
- the "AI assistance" section lists the tool and model, the generated files, the instruction and what the author changed;
- every merge needs a non-author approval with a comment that asks a question or names a file, line or case, and "LGTM" does not count;
- AI-written code shows one deliberate break with the number of failing tests, plus one input tried by hand in the app.

**Why:** In our last seven PRs (#8–#13, #15), all were mostly AI-generated. Only #9 and #10 named the files the AI wrote. #9–#11 were merged without an approval, and #10 and #12 got only "LGTM". Group 11's review (#16) found three drafter bugs (F1–F3) that the 15 drafter tests did not catch.

**Alternative rejected:** Keeping the Week 3 wording ("states whether AI was used", "a teammate can explain the result"), which every one of those PRs already met on paper.

**Led by:** 林彥宇 (proposed in this PR); accepted through the steward's review.

## 2026-11-25 — Steward turns and PR timing until CP2
**What:**
- Steward turns until the 11/29 deadline. Each steward approves the listed PRs with a substantive comment:

  | Turn | Steward | Reviews and merges |
  | --- | --- | --- |
  | 11/24–25 | 周廷威 | #24 (README status) |
  | 11/26 | 蔡凱旭 | #25 (prompt suite), #26 (#18/#19) |
  | 11/27 (merge day) | 蔡尚融 | the fix for #14, the PR for #17; writes the merge plan |
  | 11/28–29 | 林彥宇 | the PR for #21 (Claude drafter); final CP2 check of `main` |

- 蔡凱旭 opens the PRs for #17 and #21 by 11/26, as drafts if they are not finished, so that they appear in the merge plan.
- Anything merged after merge day (expected: #21) is a follow-up merge on 11/28. It is recorded under the merge-plan entry, with the same check: someone other than the steward clones `main` fresh and runs the main task.

**Why:** 蔡尚融 pointed out two problems. First, #17 and #21 are due 11/28, after the 11/27 merge day. Second, nobody was steward on 11/28–29. Every member needs two steward approvals with a substantive comment for CP2. 周廷威 already has them (#22, #23). The table gives 蔡凱旭 and 蔡尚融 two each, and gives 林彥宇 the second one (the first was #13).

**Alternative rejected:** Moving merge day to 11/28, which leaves no buffer before the 11/29 deadline. Also rejected: one steward for all remaining days, which would leave the other two short of approvals.

**Led by:** 林彥宇, after 蔡尚融 raised the timing problem; accepted through the steward's review of this PR.
