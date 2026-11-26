# Design Rationale

DecisionTrace turns a pasted team discussion into a decision card, has a teammate other than the author approve or reject it, and answers "why did we decide this?" only from approved cards. Card drafting is still a keyword MOCK; Claude will be connected in #21 (open, PR #36).

The choices below were shaped by three sources:
- **CP1 interviews** (2026-10-23): R1, a late joiner who spent ~1.5 h looking for why timestamps were stored as text; R2, the "team memory" person whose own decision log died by week 7.
- **Group 11's cross-team review** (#16, 2026-11-24).
- **Two user-testing sessions** with students outside the team (P1, P2, 2026-11-25), described below.

## Key design decisions

| Decision | What shaped it | Rejected alternative | What testing showed |
| --- | --- | --- | --- |
| **A teammate other than the author approves every card** before it counts as a team decision (`review()` refuses the author). | R2's biggest fear was a plausible but wrong reason that looks authoritative. | Publishing AI drafts directly to the log. | Both P1 and P2 rejected the card whose reason belonged to a different decision (task 3), so the gate catches what the drafter gets wrong. The reviewer name is free text, so the author rule can be bypassed with another spelling (#11). |
| **A reason is a verbatim quote from the discussion, or `unknown`**; a quote not found word for word is replaced (`check_quote`). | R1: an AI turning a mundane reason into a smarter-sounding wrong one is worse than no reason. | Letting the drafter paraphrase the reason. | A verbatim quote can still belong to another decision (Group 11 F1, #17). P1 and P2 both judged the card by comparing the quote with the decision, but P1 could see only the extracted sentence, not the full discussion, so could not tell whether it was taken out of context. |
| **Ask answers only from approved cards and cites each card** by id and verbatim quote, up to three, best first (#29). | R1: source links matter most. R2 wanted teammates to ask the tool instead of interrupting R2. | Answering from drafts too; answering without the source card. | Both participants checked the quote before trusting an answer. Testing found two matching bugs, fixed in #29 (see below). Both said "No approved decision found." cannot tell "waiting for review", "rejected" and "never discussed" apart. |
| **The drafter is a keyword MOCK, labelled "MOCK draft, not AI" in Draft, Review and Approved cards**, behind the same `draft_card()` signature Claude will use. | The walking skeleton had to connect before the API key was granted (DECISIONS.md, 2026-11-23). | Waiting for the key before connecting the pieces. | Both participants noticed the label. Ask cites cards without it, which is where a reader decides whether to trust an answer. For a Chinese discussion the MOCK puts the same whole sentence into Decision, Reason and Quote, and the draft cannot be edited (P1, P2). |
| **Discussions are pasted in**, not read from Discord or LINE. | A bot needs server permissions, and v1 has no LINE integration (CP1 open question). | A Discord bot in v1. | Both participants named the extra paste-and-wait step as the main reason a team would stop using it; R2 had said the same in CP1. This remains the largest adoption risk. |

## User testing

**Participants.** Two 4th-year Computer Science students outside the team, recruited through personal contacts and cited by code with their consent. P1 has done about 5 team projects, P2 about 6. Both said their teams rarely record why a decision was made; they scroll back through LINE or Discord, or ask the person who proposed it.

**Setup.** Each participant installed the app from the README on their own machine and ran branch `c-ask-sources` (#29), then loaded the sample history (4 approved cards, 1 rejected, 1 draft). Each session had five tasks and five follow-up questions, run by 周廷威.

| Task | P1 | P2 |
| --- | --- | --- |
| 1. Find why the live board uses polling, not WebSockets | Found it in English on the first try. The same question in Chinese found nothing; a shorter Chinese question worked. | The Chinese question found nothing; the English one and a short Chinese one worked. |
| 2. Turn a Chinese discussion into a card for review | Done. Noticed the MOCK label and "It now waits in the Review tab"; did not know whom to notify. Wanted to edit the card (three identical fields) but could not. | Done. Same: noticed the label, no way to name a reviewer, no way to edit. |
| 3. Review a card drafted by "Tingwei" (PostgreSQL decision, React reason) | **Rejected**: the quote does not support the decision, and it conflicts with two approved cards. No way to give a reason. | **Rejected** for the same reasons. Had to open Approved cards to check for conflicts; Review does not show them. |
| 4. Answer "我們用什麼追蹤 bug？為什麼？" | "No approved decision found."; understood that the task-2 card is still waiting for review. Trying "What do we use to track bugs?" returned the unrelated polling card. | Same. Would trust a found card after checking its quote, but would not read "not found" as "nobody discussed it". |
| 5. Ask whether the team switched to server-sent events | "No approved decision found."; read it as "no such decision". Could not see that it had been proposed and rejected. | Same answer in Chinese, English and "SSE"; read it as "no such decision". |

**Findings**

| # | Finding | Seen by | Severity | Action |
| --- | --- | --- | --- | --- |
| 1 | `main` had no sidebar, so the README steps could not load the sample data | P1, P2 | blocks the main task | Fixed in #29 |
| 2 | "What do we use to track bugs?" cited the polling card only because both contain "use" | P1, P2 | will confuse users | Fixed in #29: "use" is ignored |
| 3 | A long Chinese question found nothing; a short one worked | P1, P2 | will confuse users | Fixed in #29: long questions need two shared keywords, not a share of all keywords |
| 4 | "No approved decision found." does not say whether a card is waiting for review or was rejected | P1, P2 | will confuse users | Phase 3 |
| 5 | Drafts cannot be edited; a Chinese discussion gives three identical fields | P1, P2 | will confuse users | Edit-then-approve: out of scope in #19; CP3 |
| 6 | Reject has no reason field; nothing tells the author whom to ask for review | P1, P2 | polish | Reviewer hint: fixed in #26 (#19); reject reason field: Phase 3 |
| 7 | Review does not flag conflicts with approved cards | P2 (P1 checked by hand) | polish | Phase 3 |

**What held.** Both participants caught the mismatched card in task 3, and both checked quotes before trusting an answer, which is the behaviour the design depends on.

## Known limitations

- The reviewer name is free text, so the "author cannot review" rule depends on honesty.
- The reviewer sees only the extracted sentence, not the whole pasted discussion.
- Ask matches keywords, so a question worded differently from the card (a synonym) is not found.
- Teams must paste discussions in by hand, which both participants and R2 named as a reason to stop using the tool.
- All results come from the MOCK drafter; none of them shows how Claude's drafts will be judged.
