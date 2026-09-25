# Operating layer

Harness-neutral copy of `CLAUDE.md`, for coding agents that read `AGENTS.md`
instead of (or alongside) `CLAUDE.md` (Codex and others). Same content,
plain references instead of Claude Code's `@` import syntax — read these
four files yourself before doing anything else in this repo:

- operating-layer/COMPANY-BRAIN.md — who we are, what we know, what we've learned
- operating-layer/OPERATING-RULES.md — what you may do alone, what needs a person, who that person is
- operating-layer/BETS-REGISTER.md — what we're trying right now, who owns it, what success means
- operating-layer/LEARNING-LOOP.md — how this layer has changed, and why

## The loop

idea → prototype (in `sandbox/`) → proposal (`proposals/`) → graded review
(`rubric.md`, advisory) → named-owner decision → `PROMOTED` (backlog, never
deployed) / `PARKED` / `COMPOSTED` → lessons back into the four files above.

If your harness supports skills or an equivalent, the fuller versions of
this loop live in `.claude/skills/map-process/`, `.claude/skills/propose/`
and `.claude/skills/learn/` — read their `SKILL.md` files directly; they are
plain markdown and don't require Claude Code to be useful as instructions.

## The one rule that holds all of this together

**You never approve your own work.** Draft, prototype, grade (advisory),
open a proposal or a pull request — a named person accepts it. `PROMOTED`
means backlog, never deployed. `guardrails.json` is the machine-readable
source of the rules that matter; if your harness supports hooks or
pre-action checks, wire them the way `.claude/hooks/` does for Claude Code
(see `README.md`, "Harness-neutral by design").
