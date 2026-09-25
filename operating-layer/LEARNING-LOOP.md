<!-- governance-tag: LEARNING -->
# Learning loop

**Purpose:** how the operating layer gets better after every piece of work.
When an agent (or a person) gets the same thing wrong twice, the fix becomes
a rule. When a rule goes stale, it retires.

> Guidance — what good looks like: short, dated entries, not a diary. This
> sheet is where the other three sheets earn their edits — a promotion here
> should point at the exact line it changed in COMPANY-BRAIN.md,
> OPERATING-RULES.md or BETS-REGISTER.md. Size budget: ~80 lines
> (`layer_budget.py`) — this sheet prunes hardest of the four, because its
> whole job is to feed conclusions into the other sheets and then let go of
> the raw log. Run `.claude/skills/learn/SKILL.md` weekly to draft this.

## Repeated mistakes → candidate new rules

- <!-- date · what went wrong twice · proposed rule · which sheet it belongs in -->

## Rules retired this cycle

- <!-- date · rule · why it's stale (superseded, never fired, no longer true) -->

## Sheets over budget

- <!-- date · sheet · lines over · what got pruned -->

## Lessons from decided proposals

- <!-- date · proposal · PROMOTED/PARKED/COMPOSTED · one-line lesson -->

## Source of truth for this loop

`.claude/audit/actions.jsonl` (blocked actions + tool history — gitignored,
local), decided proposals in `proposals/`, and this sheet's own history. The
`learn` skill reads all three and proposes changes here; it never edits the
other sheets directly — a named owner does that, same as any other proposal.
