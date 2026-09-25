# The grading rubric

Six criteria, 1/3/5 each, max 30. Published so people know what good looks
like before they start building. This is the rubric `.claude/skills/propose/SKILL.md`
grades every proposal against.

## Scoring rules

- **Max 30.** Six criteria, 1/3/5 anchors each (no 2s or 4s — force a real
  call between the anchors below).
- **Advisory only.** The machine's score is a first pass for a human, never
  a verdict. Only a named owner decides.
- **Missing evidence is a question, not a penalty.** If a criterion can't be
  scored because the evidence doesn't exist yet, score it `?` and write the
  question that would resolve it, instead of scoring it low. An idea with no
  data yet may just need a week of collecting it.
- **Confidence travels with the score.** Every score (including `?`) carries
  a confidence — high / medium / low — so a 5/5 on thin evidence doesn't read
  the same as a 5/5 on strong evidence.

## The six criteria

| # | Criterion | 1 | 3 | 5 |
|---|---|---|---|---|
| 1 | **Named user & problem** | No named person or team has this problem | A named team has this problem, described generally | A named person, with a specific recurring instance of the problem, described |
| 2 | **Evidence** | No data, only a hunch | Some examples or anecdotal data, no baseline | Measured baseline + samples of the problem occurring |
| 3 | **Feasibility** | Needs new systems/access that don't exist | Works with some integration effort | Works today on data/systems already available |
| 4 | **Cost & risk** | Touches production, external sends, or irreversible actions | Read-only but touches sensitive data | Read-only, reversible, no external sends |
| 5 | **Reuse** | One-off, no obvious second use | Could plausibly extend to one adjacent case | Pattern clearly reusable across multiple named cases |
| 6 | **Strategic fit** | Unrelated to any live bet | Adjacent to a live bet | Maps directly to a live bet in BETS-REGISTER.md |

## Decision outcomes

- **PROMOTED** — the named owner accepts it. It goes into the backlog (see
  `BETS-REGISTER.md` / Backlog task tooling) as a properly scoped build.
  **Promoted means backlog, never deployed.** Nothing goes to production off
  the strength of a graded proposal alone.
- **PARKED** — not accepted now, usually because of an evidence question.
  Stays visible; can come back once the question is answered.
- **COMPOSTED** — closed, not going forward. The reason becomes a lesson in
  `LEARNING-LOOP.md`, not a silent deletion.

## Owner decision block (required on every graded proposal)

```
Decision: PROMOTED | PARKED | COMPOSTED
Owner: <named person>
Date: <date>
Why: <one line>
```
