<!-- FICTIONAL SPECIMEN — Specimen Components Ltd is not a real company. -->
# Supplier-query triage

**Submitted by:** Sales Ops Lead (fictional specimen) · 2026-08-01

## What

An agent drafts a first-pass reply to routine status/spec supplier queries,
pulled from the order system, for a named handler to review and send.

## For whom

The three Sales Ops handlers who triage the shared inbox — named process:
see `processes/supplier-quality-query-handling.md`.

## Problem

70% of inbound queries are status/spec, answerable from data already in the
order system, but they queue behind whoever's free to read the inbox — worst
case, a whole weekend.

## Evidence

Two weeks of query samples collected (61 queries, 43 status/spec). No
measured baseline response time yet — the "30% faster" success line in
BETS-REGISTER.md is a target, not yet a measured improvement.

## Prototype

`sandbox/supplier-triage-draft/` — reads the order system, drafts a reply,
does not send.

## Risks

Read-only against the order system; no external send without a handler's
review. Risk is a wrong draft costing a handler more time than writing from
scratch, not a wrong action reaching a supplier.

## Ask

Sales Ops Lead to decide: promote this to a proper build, or wait for a
measured baseline first.

## Rubric (advisory — see rubric.md)

| # | Criterion | Score | Confidence | Note / question |
|---|---|---|---|---|
| 1 | Named user & problem | 5 | high | 3 named handlers, specific recurring query type |
| 2 | Evidence | 3 | medium | 2 weeks of samples; no baseline yet — **question:** what's current median first-response time? |
| 3 | Feasibility | 4 | high | Works on existing order-system data |
| 4 | Cost & risk | 4 | high | Read-only, no external send without sign-off |
| 5 | Reuse | 3 | medium | Pattern plausibly extends to customer (not just supplier) queries |
| 6 | Strategic fit | 5 | high | Maps directly to the live bet in BETS-REGISTER.md |

**Total: 24/30 (advisory)** — one question outstanding (baseline response
time), not a blocker to promotion, tracked as a follow-up measurement.

## Decision

```
Decision: PROMOTED
Owner: Head of Sales Ops
Date: 2026-08-01
Why: Read-only, clearly owned, strong strategic fit; baseline measurement
becomes the first task of the build rather than a precondition for starting.
```
