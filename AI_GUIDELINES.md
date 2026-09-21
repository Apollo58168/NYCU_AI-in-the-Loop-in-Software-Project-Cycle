# AI Usage Guidelines

Status: Reviewed and ready for Week 3 submission.

## 1. Tools, Uses, and Boundaries

- We will use OpenAI Codex for repository-scoped work such as generating boilerplate, suggesting small refactors, drafting unit-test skeletons, and updating documentation. We will not merge its output without a human reading the diff, understanding the implementation, and running the relevant checks.
- We will use ChatGPT for brainstorming requirements, comparing design alternatives, explaining unfamiliar concepts, and drafting non-final documentation. ChatGPT may propose options, but the team makes final product and architecture decisions and records significant choices in `DECISIONS.md`.
- We may use Claude or Gemini for a second opinion on requirements, designs, or debugging when the first model's answer is uncertain. A second model's agreement is not treated as proof of correctness; claims that affect the project must still be checked against source documentation, code, or tests.
- AI tools may draft tests, but a human must add missing edge cases and confirm that the tests can fail when the implementation is wrong. Passing AI-generated tests alone is not enough evidence to merge.
- Authentication, authorization, secrets, privacy-sensitive data handling, destructive data operations, and other security-critical behavior must be designed and reviewed by humans. Real credentials, personal information, or confidential data must never be pasted into an AI tool.
- In DecisionTrace, AI may extract, summarize, and suggest a decision candidate from GitHub pull requests, issues, commits, and meeting notes. Each candidate contains a decision, reason, source references, alternatives, confidence, and review status.
- DecisionTrace's AI must not publish a candidate as an official team decision or write it directly to the official decision log. A human reviewer must approve, edit, or reject every candidate; only an approved or human-edited candidate may become official.
- DecisionTrace must not present an inferred reason as a fact. When the source material does not support a field, the AI must mark it as unknown or lower its confidence instead of inventing missing context. Confidence is a review signal, not proof that the candidate is correct.

## 2. Documenting AI Interactions

- An entry is required in the prompt engineering log whenever an AI interaction produces code, text, an evaluation method, or a design recommendation that is retained in the repository. Each entry records the date, tool and model when known, prompt or concise prompt summary, output summary, what was retained or changed, and the reason for that decision.
- One-off syntax lookups, explanations, or debugging questions do not require a log entry when their output is not copied into the repository and does not change a project decision.
- Every pull request description states whether AI was used and points to the relevant prompt-log entry when one exists. The PR description summarizes the contribution; it does not duplicate the full interaction transcript.
- If an AI suggestion changes the team's requirements, architecture, data model, evaluation method, or another significant approach, the team records the decision and its reasoning in `DECISIONS.md`. The prompt log records the interaction, while `DECISIONS.md` records the team's decision.
- The collaboration log records human coordination: who contributed or reviewed, important handoffs, unresolved disagreements, and how the team resolved them. It does not repeat prompts or routine Git activity that is already visible in commits and pull requests.
- During collaboration, the contributor who used AI must be able to explain the retained output to another teammate. Review comments and resulting changes remain in the pull request and may be linked from the collaboration log rather than copied into it.

## 3. Resolving Disagreements About AI Output

- Correctness and safety are decided using evidence: the relevant tests pass, the change satisfies the agreed requirements, authoritative documentation supports external claims, and at least one teammate other than the contributor can explain the result.
- Style disagreements are resolved using the repository's formatter, linter, and documented conventions rather than personal preference.
- If evidence reveals a defect or unresolved risk, the AI-generated output is revised or rejected even when most teammates prefer it. A vote is not a substitute for evidence.
- If the available evidence does not resolve the disagreement, the code steward makes the final merge decision after hearing both positions. The team records a one-sentence explanation in `DECISIONS.md` when the decision is significant.
- The person who wrote the prompt does not receive special authority over the output. The same review and acceptance criteria apply to human-written and AI-assisted work.
