<!-- governance-tag: GUARDRAILS -->
# Operating rules

**Purpose:** decision authority. What an agent may do alone, what needs a
person, and who that person is. This is where most rollouts stay silent —
don't leave it silent here.

> Guidance — what good looks like: "may" and "may not" as short, concrete
> verbs an agent can check itself against ("run tests" not "be helpful").
> A preference stays in prose; a rule that matters gets a matching line in
> guardrails.json and one of the hooks below enforces it — see "Which rules
> are enforced in code". Size budget: ~80 lines (`layer_budget.py`). Section
> headers below are read by `session_brief.py` at session start — keep the
> exact `## Agents may not` heading so that hook keeps working.

## Agents may

- Draft, refactor in a branch, run tests
- Prototype in `sandbox/` (see propose skill) — never in a production code path
- Propose changes to this operating layer itself (via a proposal, not a
  silent edit)

## Agents may not

- Push to a protected branch, or force-push anywhere (enforced: `guard_commands.py`)
- Approve or merge their own pull request / proposal (enforced: `guard_commands.py`)
- Edit protected paths directly — infra, deploy, CI config (enforced: `guard_paths.py`)
- Send anything external (email, message, webhook) without a named person's sign-off
- Deploy anything. `PROMOTED` means backlog, never deployed — see rubric.md.

## Escalate to a person

- Anything irreversible, anything touching real customer data, anything the
  agent is unsure counts as "may" above.
- <!-- name the escalation contact for this repo/org -->

## Who approves what (named roles)

| Decision | Approver |
|---|---|
| Engineering PR merge | <!-- named role --> |
| Proposal → PROMOTED/PARKED/COMPOSTED | <!-- named role, see BETS-REGISTER.md --> |
| Operating-layer change (this file, the other 3 sheets) | <!-- named role --> |
| Infra / deploy / CI change | <!-- named role --> |

## Which rules are enforced in code

See `guardrails.json` for the machine-readable source of truth, and:
- `guard_commands.py` — blocked_command_patterns, protected_branches
- `guard_paths.py` — protected_paths
- `layer_budget.py` — operating_layer_line_budget

Everything above that has no matching hook is a preference, not a
guarantee — treat it as advisory until someone enforces it.
