# Evaluation Plan

Status: Reviewed and ready for Week 3 submission.

Project: **DecisionTrace — AI-Powered Decision Memory for Software Teams**

## Problem Grounding

### 1. Who has the collaboration problem?

Students working in multi-week software project teams have this problem, especially members who join after a decision was made or need to revisit an earlier technical choice. They need to understand not only what the team implemented, but why the team selected that approach and which alternatives it rejected.

### 2. What do they currently do instead of using our tool?

They manually search fragmented Discord or Slack messages, pull requests, issues, commits, and meeting notes, or ask a teammate to remember the discussion. This takes time, interrupts other members, and can produce an incomplete or incorrect explanation when the original reasoning was spread across several sources.

### 3. What would be observably different if the tool worked?

With DecisionTrace, team members would search one human-approved decision log and answer questions such as "Why did the team choose PostgreSQL?" faster and more accurately. They would rely less on interrupting teammates or reconstructing reasoning from raw project history, while still being able to follow every decision back to its original sources.

## Evaluation Design

### Success Definition

We will know DecisionTrace works if representative users can answer three project-decision questions with at least 80% accuracy and the DecisionTrace group has a median completion time at least 30% lower than the manual-search group, without reducing answer accuracy. DecisionTrace users should also give the tool a median usefulness rating of at least 4 out of 5.

DecisionTrace produces a structured candidate with these fields:

- **Decision:** the choice the team appears to have made;
- **Reason:** the source-supported reason for the choice;
- **Discussed in:** links or identifiers for the supporting pull requests, issues, commits, or meeting notes;
- **Alternatives:** other options explicitly considered in the sources;
- **Confidence:** the AI's estimate of how strongly the sources support the extraction; and
- **Review status:** Pending, Approved, Edited, or Rejected.

The human–AI boundary is explicit: AI extracts, summarizes, and suggests decision candidates, while a human reviewer approves, edits, or rejects each candidate. The AI does not decide whether a candidate is an official team decision. Only an approved or human-edited candidate may enter the official decision log.

### Target Users

We will recruit at least six university students who have worked on a team software project. We will recruit them from classmates and other student project teams, excluding the DecisionTrace developers so that prior knowledge of the test materials does not influence the results. Participants will be randomly assigned in equal numbers to a manual-search group and a DecisionTrace group.

### Method

We will use a controlled between-groups comparison with one fixed project-artifact set containing GitHub pull requests, issues, commits, and meeting notes. Before the study, the team will create a ground-truth set of significant decisions and verify every answer against the cited source material.

The evaluation has two stages:

1. **Candidate review:** DecisionTrace processes the artifact set. Human reviewers record whether each AI-generated candidate is approved unchanged, edited, or rejected. This measures whether the suggestions are useful enough to justify the review interruption.
2. **Decision retrieval:** Both participant groups answer the same three questions about why the project chose a particular approach. The manual-search group uses the raw artifacts, while the DecisionTrace group uses the human-approved Decision Log. We record completion time and score correctness against the ground truth. After each answer, participants rate their confidence from 1 to 5; DecisionTrace users also rate the tool's overall usefulness from 1 to 5.

We will run this formative evaluation after the first testable prototype can generate and display reviewable candidates, early enough to revise the extraction prompt, review workflow, and interface before the final evaluation.

### Minimum Evidence Threshold

The initial evidence threshold will be considered met when:

- at least six representative participants complete the evaluation, with at least three in each group;
- the DecisionTrace group answers the three questions with at least 80% accuracy and performs no worse than the manual-search group on accuracy;
- the DecisionTrace group's median completion time is at least 30% lower than the manual-search group's median;
- DecisionTrace users give the tool a median usefulness rating of at least 4 out of 5; and
- no candidate enters the official Decision Log without a recorded human approval or edit.

The team will also report participant confidence scores and the proportions of AI candidates that were approved, edited, and rejected. These are diagnostic measures for improving the design rather than additional pass/fail thresholds for this evaluation.
