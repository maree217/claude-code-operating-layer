---
name: propose
description: Turn an idea (optionally with a prototype in sandbox/) into a graded proposal for a named owner to decide on. Use when someone wants to propose an agent-built idea for review, without needing to know git or engineering tooling. Never merges, never deploys.
---

# Propose an idea

For anyone — not just engineers. This skill hides git from the person using
it; describe every step in plain words, not git jargon.

## 1. Capture the idea

Ask, if not already given: what is it, who is it for (a named person or
team), what problem does it solve, and — if there's a prototype already in
`sandbox/` — where is it. A prototype is optional; an idea alone can still be
proposed.

## 2. Write the proposal

Create `proposals/<YYYY-MM-DD>-<slug>.md` from this fixed template:

```markdown
# <Title>

**Submitted by:** <name> · <date>

## What
## For whom
## Problem
## Evidence
## Prototype
<link to sandbox/... or "none yet">
## Risks
## Ask
<what you want the owner to decide>
```

## 3. Grade it — advisory, not a verdict

Score the proposal against every criterion in `rubric.md`. For each of the
six criteria, give a score (1/3/5, or `?` if the evidence to score it
doesn't exist yet), a **confidence** (high/medium/low), and — for any `?` —
the specific question that would resolve it. Missing evidence is a
question, not a penalty. Total the scorable criteria out of 30 and append
the scored rubric table to the proposal file, followed by an empty
**Decision** block (see `rubric.md`'s owner decision block) for the owner to
fill in.

Say the score out loud in plain words: "This machine-scored 22/30, advisory
— two criteria are questions because there's no baseline yet." Never call
the score a decision.

## 4. Only if they agree: open it for the owner

Ask first: "Do you want me to open this for <owner> to decide?" If yes:

1. Create a new branch for the proposal file.
2. Commit it.
3. Open a pull request (or your harness's equivalent) addressed to the named
   owner from `OPERATING-RULES.md`'s "Who approves what" table.

Explain what happened in plain words afterwards ("I've opened this for
<owner> to review — they'll see it as a pull request called ...") rather
than showing raw git output.

## What this skill never does

- Never merges its own pull request.
- Never deploys anything. `PROMOTED` means backlog, never deployed.
- Never treats its own grading as the decision — only the named owner's
  `Decision:` block in the proposal file does that.

Once decided, the outcome belongs in `BETS-REGISTER.md` (if `PROMOTED`) and
the reasoning belongs in `LEARNING-LOOP.md` either way — that's
`.claude/skills/learn/SKILL.md`'s job, not this one's.
