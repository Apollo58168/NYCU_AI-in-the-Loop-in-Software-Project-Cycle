Drafter: `decisiontrace.drafter:draft_card`. Passed 10 of 15.

| Case | Kind | Result | What was wrong |
| --- | --- | --- | --- |
| T1-english-chat | typical | pass |  |
| T2-chinese-chat | typical | pass |  |
| T3-one-sentence-all-fields | typical | FAIL | alternatives should be ['MongoDB'], got ['MongoDB because our data is relational'] |
| T4-chinese-one-sentence | typical | pass |  |
| T5-meeting-notes | typical | pass |  |
| T6-decision-without-reason | typical | pass |  |
| E1-reason-from-other-decision | edge | FAIL | reason 'We decided to use React because the team knows it.' does not support the PostgreSQL decision; expected a warning on the card |
| E2-unrelated-reason | edge | FAIL | reason should be 'unknown', got 'Lunch was late because the cafe was busy.'; confidence should be at most 'low', got 'medium'; reason 'Lunch was late because the cafe was busy.' does not support the PostgreSQL decision |
| E3-chinese-chit-chat | edge | pass |  |
| E4-english-question | edge | pass |  |
| E5-undecided | edge | FAIL | expected no decision, got decision 'We are still undecided about the database because nobody has benchmarked it.' |
| E6-disagreed | edge | FAIL | expected no decision, got decision 'I disagreed with switching to Rust because the deadline is close.' |
| E7-prompt-injection | edge | pass |  |
| E8-too-long | edge | pass |  |
| E9-empty | edge | pass |  |
