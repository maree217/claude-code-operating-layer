<!-- governance-tag: OBSERVABILITY -->
# Bets register

**Purpose:** what we're trying right now, who owns each bet, and what counts
as success. Stops agents (and people) optimising for the wrong thing.

> Guidance — what good looks like: one row per live bet, a named owner (a
> person, never "the team"), a measurable success line, and an explicit
> kill condition. A bet with no kill condition never dies. This section
> header (`## Live bets`) is read by `session_brief.py` at session start —
> keep the exact heading. Size budget: ~80 lines (`layer_budget.py`) —
> when a bet resolves, move its outcome into LEARNING-LOOP.md and delete
> the row here rather than letting the register only grow.

## Live bets

| Bet | Owner | Success | Kill if | Status |
|---|---|---|---|---|
| <!-- e.g. "supplier-query triage" --> | <!-- named person --> | <!-- e.g. "30% faster first response by Q1" --> | <!-- e.g. "no measurable change in 6 weeks" --> | <!-- proposed / promoted / running --> |

## Recently decided (last few cycles)

| Bet | Outcome | Date | Why |
|---|---|---|---|
| <!-- proposal name --> | PROMOTED / PARKED / COMPOSTED | <!-- date --> | <!-- one line --> |

## How a bet gets here

A bet enters this register when a proposal is graded (see `rubric.md`) and a
named owner decides `PROMOTED`. See `.claude/skills/propose/SKILL.md` for the
full idea → prototype → proposal → review → decision loop, and
`proposals/README.md` for where proposals themselves live.
