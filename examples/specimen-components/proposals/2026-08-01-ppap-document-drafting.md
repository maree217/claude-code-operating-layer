<!-- FICTIONAL SPECIMEN — Specimen Components Ltd is not a real company. -->
# AI-generated PPAP document drafting

**Submitted by:** Quality Engineer (fictional specimen) · 2026-08-01

## What

An agent drafts sections of a PPAP (Production Part Approval Process)
document set from part specs and batch data, for QA to review and complete.

## For whom

QA, ahead of new-part customer submissions.

## Problem

PPAP document sets are long and formulaic in places, but each one takes a
QA engineer most of a day to assemble.

## Evidence

None yet — no sample of past PPAP drafts has been assembled to check against
for accuracy or to learn the expected structure from.

## Prototype

None yet.

## Risks

A PPAP document is customer-facing and quality-critical; a wrong or
overconfident draft is worse than no draft if QA doesn't fully re-check it.

## Ask

Quality Engineer asks: should we invest in collecting sample data now, or is
this not worth pursuing yet?

## Rubric (advisory — see rubric.md)

| # | Criterion | Score | Confidence | Note / question |
|---|---|---|---|---|
| 1 | Named user & problem | 5 | high | Named team (QA), specific recurring document set |
| 2 | Evidence | ? | — | **Question:** no sample of past PPAP drafts collected yet — score this once a handful exist |
| 3 | Feasibility | ? | — | **Question:** unknown until we know how structured the source spec/batch data actually is |
| 4 | Cost & risk | 3 | medium | Customer-facing document, needs full QA review regardless |
| 5 | Reuse | 4 | medium | Same pattern likely applies across every new-part submission |
| 6 | Strategic fit | 3 | medium | Adjacent to quality/turnaround goals, not a named live bet yet |

**Total: not scored (two questions outstanding)** — advisory total withheld
rather than computed with placeholders, per rubric.md's rule that missing
evidence is a question, not a penalty.

## Decision

```
Decision: PARKED
Owner: Head of Sales Ops
Date: 2026-08-01
Why: Good idea, no evidence yet. Parked pending: (1) a sample of 5-10 past
PPAP drafts collected for QA to check draft accuracy against, (2) a look at
how structured the source spec/batch data is. Revisit once both exist.
```
