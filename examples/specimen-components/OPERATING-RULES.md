<!-- governance-tag: GUARDRAILS -->
<!-- FICTIONAL SPECIMEN — Specimen Components Ltd is not a real company.
     This is a filled example of operating-layer/OPERATING-RULES.md. -->
# Operating rules — Specimen Components Ltd (fictional specimen)

## Agents may

- Draft, refactor in a branch, run tests
- Prototype supplier-query triage in `sandbox/` using anonymised sample queries
- Draft replies to routine supplier queries for a human to send

## Agents may not

- Push to `main`, or force-push anywhere (enforced: `guard_commands.py`)
- Approve or merge their own proposal or pull request (enforced: `guard_commands.py`)
- Edit CI/deploy config directly (enforced: `guard_paths.py`)
- Send a reply to a supplier without a named handler's sign-off
- Deploy anything — `PROMOTED` means backlog, never deployed

## Escalate to a person

- Any query involving a price quote, a contract term, or a complaint
- Any query the agent can't classify with confidence

## Who approves what (named roles)

| Decision | Approver |
|---|---|
| Engineering PR merge | Head of Engineering |
| Proposal → PROMOTED/PARKED/COMPOSTED | Head of Sales Ops |
| Operating-layer change | Head of Sales Ops (this repo's owner) |
| Infra / deploy / CI change | Head of Engineering |

## Which rules are enforced in code

See `guardrails.json`, `guard_commands.py`, `guard_paths.py`,
`layer_budget.py` — same enforcement as the top-level template, just filled
in for this fictional specimen.
