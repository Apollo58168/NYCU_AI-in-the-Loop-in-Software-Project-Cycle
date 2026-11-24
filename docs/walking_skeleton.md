# Walking Skeleton: Team Worksheet

> **Filled in after the session.** The session took place on 2026-11-23, 20:44–21:49 (Asia/Taipei), and nobody typed into the worksheet during it. As the course FAQ allows, 蔡尚融 filled this in on 2026-11-25 from the PR history (#8–#13), commit times and review comments. Rows marked **TODO (team)** need what only the four of us remember: our own sentences and the team check. Each of us adds or corrects their own line before CP2.
>
> Merged PR from the session: [#13 — walking skeleton runs end to end](https://github.com/Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle/pull/13)

Present: 周廷威, 林彥宇, 蔡凱旭, 蔡尚融 (all four opened and merged a PR during the session).

---

## Part 1 ★ | Say what the tool does in one sentence

| | Sentence |
|---|---|
| 周廷威 | Our tool helps a project team to remember why decisions were made by turning discussions into AI-drafted decision cards that a teammate must approve before anyone can rely on them. |
| 林彥宇 | TODO (team) |
| 蔡凱旭 | TODO (team) |
| 蔡尚融 | Our tool helps team members to keep a trusted record of decisions by letting AI draft a card from a discussion and requiring someone else to approve it. |
| **Agreed sentence** (written down on 11/25, closest to what we said; TODO (team): confirm) | Our tool helps **team members** to **keep a trusted record of decisions** by **letting AI draft a card from a discussion and requiring someone else to approve it**. |

**Did all four sentences match?** 周廷威: mine matches the agreed sentence; only the wording differs. TODO (team): others

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
| Ask (#9) | 蔡尚融 | 21:07 (蔡凱旭) | 林彥宇, on the shared screen | yes | 蔡凱旭 asked why we use Streamlit. 蔡尚融 answered that it is the stack from #8 and added a docstring on how Streamlit reruns the tab (9776a10). |
| Draft (#10) | 蔡凱旭 | 21:24 (林彥宇) | TODO (team) | with a fix later | Commit 37d14fa removed the PROMPT_LOG entries for #9 and #10 while fixing a conflict. Found in the #13 review and tracked in #14. |
| Review (#11) | 林彥宇 | 21:35 (周廷威) | TODO (team) | yes | 周廷威 noted that the reviewer name is free text, so an author could approve their own card under a different spelling. Kept as a known limitation. |
| Approved cards (#12) | 周廷威 | 21:41 (林彥宇) | not recorded (connected last, right before #13) | yes | none |

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

Answers so far are 蔡尚融's. The other three add their own view under each one (**TODO (team)**), or write "agree".

1. **What worked well in how we worked together today?**

   > 蔡尚融: All four of us built and merged our own piece within about an hour. Because #8 fixed the `Card` contract and the function signatures first, no piece had to change its hand-off when it was connected.
   >
   > 周廷威: Agree. Because the `Card` contract and function signatures were fixed in #8 before the session, all four tabs could be built in parallel and none of them changed its hand-off when connected.
   >
   > TODO (team): others

2. **What was hard or awkward?**

   > 蔡尚融: We merged too fast to review properly. #9–#11 went in without an approval, and I left only "LGTM" on #10 without reading it closely. A PROMPT_LOG conflict silently removed two entries, and nobody noticed until the steward reviewed #13.
   >
   > 周廷威: The end of the session was rushed. #12 was the last piece and went in two minutes after it was opened, with only "LGTM". I opened the setup (#8), the last piece (#12) and the integration PR (#13), so the start and the end of the integration both sat on one person.
   >
   > TODO (team): others

3. **Who had the least chance to contribute, and what would help next time?**

   > 蔡尚融: It was fairly even: each person owned one tab. The weakest part was review, not building. Reviewers had little time, so comments were short.
   >
   > 周廷威: Building was even, one tab each, and merging into `walking-skeleton` rotated. But the setup and the final integration PR both came from me, so the others had less chance to drive the integration. Next time setup and final integration go to different people, and we rotate who drives while connecting.
   >
   > TODO (team): others

4. **What is the one thing we will do differently in the next team session (merge day)?**

   > 蔡尚融: No PR is merged without a steward approval that has a real comment (a question, or a specific file, line or case). Conflicts are read aloud by the driver before resolving.
   >
   > The first half was already written down after the session (DECISIONS.md, 2026-11-23 handover; AI_GUIDELINES rules from 2026-11-24).
   >
   > 周廷威: Agree with the steward-approval rule. I'd add: the last piece still gets explained by a non-author before it is connected, even when we are short on time, and setup and final integration go to different people.
   >
   > TODO (team): others

5. **Blockers we found, and who follows up:**

   > - PROMPT_LOG entries for #9 and #10 were removed → #14, 蔡凱旭.
   > - No Claude API key yet, so the drafter is MOCK → #21, 蔡凱旭.
   > - Reviewer name is free text → listed as a known limitation in #13; to be covered in the design rationale (周廷威).

---

## Quick checklist

- [x] All four of us were present for the session
- [ ] All four of us built a piece, and each piece was explained by someone who did not write it: built yes; "explained by" filled in for Ask so far (TODO in Part 3 for the other three)
- [x] We have one agreed sentence about what the tool does (written down afterwards; the team confirms it)
- [x] The pieces connected and something ran from input to output, with the drafter faked
- [x] The PR was reviewed by the steward with at least one real comment, and merged (#13)
- [x] We saved this worksheet as `docs/walking_skeleton.md` and added a line to `DECISIONS.md` (both late, on 2026-11-25)
