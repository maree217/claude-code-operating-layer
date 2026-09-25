---
name: learn
description: Weekly review of the operating layer itself - read the audit log, blocked actions, and decided proposals, then propose (never apply) rule changes to the four sheets. Use for a periodic operating-layer health check, not for day-to-day work.
---

# Learning loop — weekly review

This skill **proposes**, it never **applies**. Every output below is a draft
for the named owner of the operating layer (see `OPERATING-RULES.md`, "Who
approves what") to accept or reject — same discipline as any other proposal.

## 1. Read the sources

- `.claude/audit/actions.jsonl` — what actually happened (tool calls,
  summaries only — see `audit_log.py`).
- Any blocked-action messages from this week (the hook stderr messages from
  `guard_commands.py`, `guard_paths.py`, `layer_budget.py` — pull these from
  session transcripts or wherever they were surfaced).
- Decided proposals in `proposals/` with a filled-in `Decision:` block.

## 2. Look for patterns

- **Repeated fixes → new rule.** The same mistake blocked, or corrected by a
  person, more than once → draft a new line for `OPERATING-RULES.md` or a
  new pattern for `guardrails.json`.
- **Stale rules → retire.** A rule in `OPERATING-RULES.md` or a pattern in
  `guardrails.json` that never fired, or that no longer matches how work
  actually happens → draft its removal.
- **Over-budget sheets → prune.** Any operating-layer sheet near or over its
  line budget (`layer_budget.py` will have been blocking edits to it) → draft
  which lines to cut, oldest/lowest-value first.
- **Decided proposals → lessons.** Every `PROMOTED`/`PARKED`/`COMPOSTED`
  proposal this cycle → one line each into `LEARNING-LOOP.md`'s "Lessons
  from decided proposals".

## 3. Write the review

Produce a short review for the owner, in this shape:

```markdown
## Learning-loop review — <date>

### Proposed new rules
- <rule text> — evidence: <what repeated> — target sheet: <which>

### Proposed retirements
- <rule text> — why stale

### Sheets over budget
- <sheet> — <N> lines over — proposed cuts: <what>

### Lessons to record
- <proposal> — <outcome> — <one-line lesson>
```

Hand this to the owner. Do not edit `COMPANY-BRAIN.md`, `OPERATING-RULES.md`,
`BETS-REGISTER.md`, or `LEARNING-LOOP.md` directly — the owner applies (or
rejects) each line, the same as any other proposal.
