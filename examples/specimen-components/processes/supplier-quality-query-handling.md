<!-- FICTIONAL SPECIMEN — Specimen Components Ltd is not a real company. -->
# Supplier quality query handling

**Interviewed:** Sales Ops Lead (fictional specimen) · 2026-07-14

## Trigger

An inbound email from a supplier or Tier 1 customer asking about order
status, a quality deviation, a spec clarification, or a price query.

## Steps

1. Query lands in the shared Sales Ops inbox.
2. One of three handlers reads it and classifies it: status / quality /
   spec / price / other.
3. Status and spec queries: handler checks the order system, replies
   directly, usually same day.
4. Quality queries: handler pulls the batch record, may loop in QA.
5. Price queries: handler drafts a quote; anything over £50k goes to Finance
   for sign-off before it's sent.
6. Reply sent, query logged in the CRM.

## Handoffs

- Quality queries → QA (batch records, deviation reports)
- Price queries over £50k → Finance (sign-off)

## Decisions

- Is this a status/spec query a handler can answer alone, or does it need
  QA or Finance? Handlers weigh: does it touch a price or a quality claim?

## Waits

- Price queries over £50k wait on Finance — historically 1-3 days, the
  single biggest source of slow first response.

## Repeats

- Status and spec queries are the majority (roughly 70% of volume,
  handler's estimate) and follow an almost identical pattern each time.

## Systems touched

- Shared inbox, order system, CRM, (for quality queries) the batch-record
  system, (for price queries) the quoting tool.

## What goes wrong

- Status queries sit unread over a weekend and read as "slow" even when
  the actual answer takes 30 seconds once seen.
- A handler on leave means their queries wait for someone else to notice.

## Candidate agent opportunities

1. **Draft a first-pass reply to status/spec queries from the order system**
   — reversible/read-only. The agent drafts, a handler sends. Covers the
   70% majority and the weekend-lag problem.
2. **Flag quality queries with the right batch record pre-attached** —
   reversible/read-only. Speeds up the QA handoff without answering on
   QA's behalf.
3. **Auto-draft a price quote for Finance to approve, never to send** —
   **not** reversible/read-only by default (touches a customer-facing
   price) — would need the Finance sign-off gate to stay a hard stop.
