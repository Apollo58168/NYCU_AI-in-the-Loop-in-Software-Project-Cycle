Claude run 1 of the suite, 2026-11-26: `ANTHROPIC_API_KEY` set, so `draft_card` used Claude (`claude-opus-5-5`, effort low). 16 cases (before E11 was added).

Drafter: `decisiontrace.drafter:draft_card`. Passed 16 of 16.

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
