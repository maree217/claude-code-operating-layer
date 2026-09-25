---
name: map-process
description: Interview one person about how a piece of work actually flows, then write processes/<slug>.md and list 1-3 candidate agent opportunities. Use when someone wants to document a real process (not the org-chart version) before deciding where agents could help.
---

# Map a process

Interview **one person** about **one piece of work**, one question at a
time. Don't batch questions — their answer to one shapes the next. Cover, in
this rough order:

1. **Trigger** — what starts this? An email, a date, another process finishing?
2. **Steps** — walk it start to finish. Who touches it, in what order?
3. **Handoffs** — where does it move between people or teams? What's passed?
4. **Decisions** — where does a human choose between options? What do they
   weigh?
5. **Waits** — where does it sit idle? Waiting on whom, for what, how long?
6. **Repeats** — what part of this happens over and over, roughly the same way?
7. **Systems touched** — every tool, spreadsheet, inbox, database involved.
8. **What goes wrong** — the exceptions, the workarounds, the thing everyone
   quietly does that isn't in the manual.

Push past the tidy version. "It goes to finance for approval" is not an
answer — ask who, how, and what happens when they're on leave.

## Write it up

Create `processes/<slug>.md` using this fixed template:

```markdown
# <Process name>

**Interviewed:** <name/role> · <date>

## Trigger
## Steps
1. ...
## Handoffs
## Decisions
## Waits
## Repeats
## Systems touched
## What goes wrong
```

## End with opportunities

List **1-3 candidate agent opportunities**, each tagged:

- **reversible/read-only** — safe to let an agent try today
- **not** — needs a person in the loop before it's safe to automate

Each opportunity should point at the specific step number(s) above it comes
from. Don't invent opportunities the interview didn't surface.

## Then what

A promising opportunity becomes an idea for `.claude/skills/propose/SKILL.md`
— this skill maps the terrain, it doesn't decide anything itself.
