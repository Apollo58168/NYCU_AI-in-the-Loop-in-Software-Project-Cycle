# Walking Skeleton: Team Worksheet

> **Filled in after the session.** The session took place on 2026-11-23, 20:44–21:49 (Asia/Taipei), and nobody typed into the worksheet during it. As the course FAQ allows, 蔡尚融 filled this in on 2026-11-25 from the PR history (#8–#13), commit times and review comments. Rows marked **TODO (team)** need what only the four of us remember: our own sentences and the team check. Each of us adds or corrects their own line before CP2.
>
> Merged PR from the session: [#13 — walking skeleton runs end to end](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/13)

Present: 周廷威, 林彥宇, 蔡凱旭, 蔡尚融 (all four opened and merged a PR during the session).

---

## Part 1 ★ | Say what the tool does in one sentence

| | Sentence |
|---|---|
| 周廷威 | TODO (team) |
| 林彥宇 | TODO (team) |
| 蔡凱旭 | TODO (team) |
| 蔡尚融 | TODO (team) |
| **Agreed sentence** (written down on 11/25; TODO (team): confirm or replace with the one we said) | Our tool helps **student software teams** to **find out later why they made a decision** by **drafting decision cards from pasted discussions, which a teammate must approve before Ask answers from them**. (The app header says it shorter: "Draft decision cards from team discussions; a teammate reviews every card.") |

**Did all four sentences match?** TODO (team)

---

## Part 2 ★ | Draw the path and split the work

**1. The path**

```
[Pasted discussion] -> [Draft: draft_card(), MOCK] -> [Save as draft: data/cards.json]
      -> [Review: a different teammate approves or rejects] -> [Ask / Approved cards: answer from approved cards only, with the source card]
```

**2. Where we were.** **Route 1.** Before the session only the project setup and the shared `Card` contract existed (#8, merged at 20:50), with one placeholder file per tab. Nothing ran from input to output.

**Our goal for today:** one pasted discussion ("We decided to use polling instead of WebSockets. Because WebSockets kept dropping behind the school proxy.") goes in as a draft card, Bob approves it, and it comes out as the answer to "Why do we use polling?" in Ask, with the source card shown.

**3. The split and the hand-offs.** The hand-offs are the function signatures in the shared contract from #8, so each tab could be built in its own file.

| Person | Building task | Receives | Returns | Branch |
|---|---|---|---|---|
| 周廷威 | Setup and shared contract (before the session); Approved cards tab | `list[Card]` | `approved_cards(cards)`: approved only, newest first | `a-setup` (#8), `a-cards` (#12) |
| 蔡凱旭 | Draft tab and MOCK drafter (module D) | pasted text, author | `draft_card(source_text, author, source) -> Card` with status `draft` | `d-draft` (#10) |
| 林彥宇 | Review tab (module B) | a draft `Card`, reviewer name, action | `review(card, reviewer, action) -> Card`, approved or rejected; the author cannot approve their own card | `b-review` (#11) |
| 蔡尚融 | Ask tab (module C) | a question, `list[Card]` | `answer(question, cards) -> Answer` built only from approved cards, with the source card | `c-ask` (#9) |

**Things we left out on purpose today:**

> The real Claude call (the API key had not been granted yet), editing a card during review, export, ranking several sources in Ask, and logins (the reviewer name is free text).

---

## Part 3 ★ | Build your piece, then connect them together

Each piece was opened as its own PR into `walking-skeleton` and merged by a teammate who did not write it. The tabs are independent files, so each one rendered as soon as it was merged. The full example could run only once all four were in.

| Piece | Built by | Merged into `walking-skeleton` (by) | Explained by | Connected? | What came up at the connection |
|---|---|---|---|---|---|
| Ask (#9) | 蔡尚融 | 21:07 (蔡凱旭) | TODO (team) | yes | 蔡凱旭 asked why we use Streamlit. 蔡尚融 answered that it is the stack from #8 and added a docstring on how Streamlit reruns the tab (9776a10). |
| Draft (#10) | 蔡凱旭 | 21:24 (林彥宇) | TODO (team) | with a fix later | Commit 37d14fa removed the PROMPT_LOG entries for #9 and #10 while fixing a conflict. Found in the #13 review and tracked in #14. |
| Review (#11) | 林彥宇 | 21:35 (周廷威) | TODO (team) | yes | 周廷威 noted that the reviewer name is free text, so an author could approve their own card under a different spelling. Kept as a known limitation. |
| Approved cards (#12) | 周廷威 | 21:41 (林彥宇) | TODO (team) | yes | none |

**Where did it first run end to end?** 21:41, after #12 was merged. The steward then reran it on screen for #13: Alice drafts, Alice's own approve is refused, Bob approves, Ask answers from the card, and Approved cards lists it. 61 tests passed.

**What did we fake or stub?**

> The drafter is a keyword-rule MOCK, not AI. Every tab labels it "MOCK draft, not AI". It keeps the `draft_card()` signature so module D's PR 2 (#21) can put Claude behind it. Reviewer identity is a free-text name.

---

## Part 4 ★ | Open the pull request together

| | |
|---|---|
| Link to the merged PR | [#13](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/13) (`walking-skeleton` → `main`, opened 21:42, merged 21:49) |
| Steward who reviewed | 林彥宇 |
| Steward's comment (copy it here) | "PROMPT_LOG.md is missing the entries for #9 (Ask, module C) and #10 (Draft, module D). They were added on their branches but removed by 37d14fa ("modify propmt_log.md"), so this PR only adds the A and B entries to main. Our AI_GUIDELINES require a log entry for every AI-generated piece, and CP2 checks it. Could 蔡凱旭 restore the two entries from c906b7e / cffc668 before we merge?" |
| How the author answered | No reply in the PR. The steward wrote "Merging now so main has the working skeleton; the PROMPT_LOG fix is tracked in #14" (蔡凱旭, due 11/26), then approved and merged. |

**The line in `DECISIONS.md`:** the walking skeleton fakes the AI step with a keyword MOCK drafter behind the real `draft_card()` signature (entry *2026-11-23 — Walking skeleton fakes the drafter with a keyword MOCK*, added with this worksheet).

---

## Part 5 | Team check

Facts from the PR history are already filled in. The answers themselves are **TODO (team)**.

1. **What worked well in how we worked together today?**

   > TODO (team). From the history: all four built and merged a piece within an hour, and the shared contract from #8 meant no piece had to change its hand-off when it was connected.

2. **What was hard or awkward?**

   > TODO (team). From the history: #9, #10 and #11 were merged without a recorded approval, and #10 and #12 got only "LGTM". The PROMPT_LOG conflict removed two entries without anyone noticing until the #13 review.

3. **Who had the least chance to contribute, and what would help next time?**

   > TODO (team)

4. **What is the one thing we will do differently in the next team session (merge day)?**

   > TODO (team). Already decided after the session: every PR needs a steward approval with a substantive comment before it is merged (DECISIONS.md, 2026-11-23 handover, and the AI_GUIDELINES rules from 2026-11-24).

5. **Blockers we found, and who follows up:**

   > - PROMPT_LOG entries for #9 and #10 were removed → #14, 蔡凱旭.
   > - No Claude API key yet, so the drafter is MOCK → #21, 蔡凱旭.
   > - Reviewer name is free text → listed as a known limitation in #13; to be covered in the design rationale (周廷威).

---

## Quick checklist

- [x] All four of us were present for the session
- [ ] All four of us built a piece, and each piece was explained by someone who did not write it: built yes; "explained by" not recorded (TODO in Part 3)
- [x] We have one agreed sentence about what the tool does (written down afterwards; the team confirms it)
- [x] The pieces connected and something ran from input to output, with the drafter faked
- [x] The PR was reviewed by the steward with at least one real comment, and merged (#13)
- [x] We saved this worksheet as `docs/walking_skeleton.md` and added a line to `DECISIONS.md` (both late, on 2026-11-25)
