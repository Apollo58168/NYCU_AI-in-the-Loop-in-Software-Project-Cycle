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
**What:** 周廷威 and 蔡尚融 swap every assignment still open in our prototype split plan. Work already merged keeps its author: #8 project setup (周廷威) and #9 Ask tab (蔡尚融).
- Module A (prompt test suite, README) and the 11/27 merge-day steward turn go to 蔡尚融.
- Module C PR 2 (sources and ranking, Q&A tests, sample data, demo steps), the design rationale and user tests, and the 11/24–25 steward turn go to 周廷威.
- Steward reviews swap with the roles: 周廷威 reviews module B's PRs, and 蔡尚融 reviews module D's PR 2.

**Why:** Proposed by 林彥宇 after the walking-skeleton session. The plan allowed swapping the drawn assignments.  
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
