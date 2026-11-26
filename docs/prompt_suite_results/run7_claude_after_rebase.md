Claude run 4, 2026-11-26: `claude-opus-5-5`, after rebasing on #26 (no-decision card form) and #35 (E12, E13 added from 蔡尚融's review).

Drafter: `decisiontrace.drafter:draft_card`. Passed 19 of 19.

| Case | Kind | Result | What was wrong |
| --- | --- | --- | --- |
| T1-english-chat | typical | pass |  |
| T2-chinese-chat | typical | pass |  |
| T3-one-sentence-all-fields | typical | pass |  |
| T4-chinese-one-sentence | typical | pass |  |
| T5-meeting-notes | typical | pass |  |
| T6-decision-without-reason | typical | pass |  |
| E1-reason-from-other-decision | edge | pass |  |
| E2-unrelated-reason | edge | pass |  |
| E3-chinese-chit-chat | edge | pass |  |
| E4-english-question | edge | pass |  |
| E5-undecided | edge | pass |  |
| E6-disagreed | edge | pass |  |
| E7-prompt-injection | edge | pass |  |
| E8-too-long | edge | pass |  |
| E9-empty | edge | pass |  |
| E10-reason-not-in-text | edge | pass |  |
| E11-reversed-decision | edge | pass |  |
| E12-unrelated-reason-after | edge | pass |  |
| E13-objection-after | edge | pass |  |
