# Operating layer

This repo's operating layer — the durable part, independent of harness or
model. Read on arrival (Claude Code loads these `@` imports at launch):

@operating-layer/COMPANY-BRAIN.md
@operating-layer/OPERATING-RULES.md
@operating-layer/BETS-REGISTER.md
@operating-layer/LEARNING-LOOP.md

## The loop

idea → prototype (in `sandbox/`) → proposal (`proposals/`) → graded review
(`rubric.md`, advisory) → named-owner decision → `PROMOTED` (backlog, never
deployed) / `PARKED` / `COMPOSTED` → lessons back into the sheets above.

Use `.claude/skills/map-process/SKILL.md` to map how work actually flows,
`.claude/skills/propose/SKILL.md` to turn an idea into a graded proposal, and
`.claude/skills/learn/SKILL.md` for the weekly review of this layer itself.

## The one rule that holds all of this together

**You never approve your own work.** You can draft, prototype, grade
(advisory), and open a proposal or a PR. A named person accepts it. Nothing
you touch gets deployed on the strength of your own judgement alone —
`PROMOTED` means backlog, never deployed. `OPERATING-RULES.md` above is the
detail; `guardrails.json` and `.claude/hooks/` enforce the parts that
matter, in code — see "Which rules are enforced in code" in that file.
