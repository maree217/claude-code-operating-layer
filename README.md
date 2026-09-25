# Claude Code operating layer — a starter kit

This is a working starter kit for the "operating layer" described in
[The missing layer in every Claude Code rollout](ARTICLE_URL): the plain-language
account of how your organisation works — what you sell, who decides, what
agents may do alone, what needs a person, and what you've learned — that
every serious agent rollout eventually needs and almost none ship with. Copy
the files below into an existing repo, fill in the four sheets for your own
organisation, and the same loop that runs a specimen fictional company below
runs yours.

## The three layers

```
+-------------------------------------------------------------+
|  OPERATING LAYER   — yours. nobody ships it. (owned)         |
|  operating-layer/*.md, guardrails.json, .claude/hooks/       |
+-------------------------------------------------------------+
|  HARNESS            — Claude Code, Codex, Copilot agents...  |
|  swappable, converging fast on the same shape (swappable)    |
+-------------------------------------------------------------+
|  MODEL               — rented, changes every quarter          |
+-------------------------------------------------------------+
```

The harness debate is about the middle layer. The value sits in the top one.

## What's in the box

| Path | What it is |
|---|---|
| `operating-layer/*.md` | The four sheets: Company brain (policy), Operating rules (guardrails), Bets register (observability), Learning loop (learning) — empty templates, ready to fill |
| `guardrails.json` | Machine-readable rules the hooks below enforce |
| `.claude/hooks/*.py` | Enforcement: blocked commands, protected paths, the operating layer's own size cap, and an audit log — stdlib Python only |
| `.claude/skills/*` | `map-process`, `propose`, `learn` — the four-moves loop as something you can run |
| `CLAUDE.md` / `AGENTS.md` | Same operating layer, wired for Claude Code and for any other harness that reads `AGENTS.md` |
| `rubric.md` | The six-criterion grading rubric proposals are scored against |
| `processes/`, `proposals/`, `sandbox/` | Where the loop's output lives — empty, with a README each |
| `examples/specimen-components/` | A fully filled, fictional worked example (see below) |
| `.github/workflows/` | CI: hook tests, and an advisory PR-comment grader for proposals |
| `tests/` | Tests for every hook |

## 10-minute install

1. Copy these into an existing repo, at its root: `operating-layer/`,
   `guardrails.json`, `.claude/settings.json`, `.claude/hooks/`,
   `.claude/skills/`, `CLAUDE.md`, `AGENTS.md`, `rubric.md`, `processes/`,
   `proposals/`, `sandbox/`, `tests/`. (`examples/` and the two GitHub
   workflows are optional reference material — copy them if you want the
   worked example or the CI wiring.)
2. If the repo already has a `CLAUDE.md`, merge the `@` imports in rather
   than overwriting it. If it already has an `AGENTS.md`, merge similarly.
3. Fill in the four sheets in `operating-layer/` for your organisation —
   `examples/specimen-components/` shows what "filled in" looks like.
4. Run `python3 -m unittest discover -s tests -v` from the repo root. This
   proves the guardrails actually block what OPERATING-RULES.md says they
   block, on your machine, before you trust them in a real session.
5. Add an `ANTHROPIC_API_KEY` repository secret if you want the
   `grade-proposal.yml` workflow to comment on proposal pull requests.

## How to adopt it: the four moves

The article names four moves. Here's what in this kit serves each one.

1. **Map the processes** — `.claude/skills/map-process/SKILL.md`. Interviews
   one person about one piece of work and writes `processes/<slug>.md`,
   ending in 1-3 candidate agent opportunities.
2. **Write the operating layer** — the four files in `operating-layer/`,
   turned into rules by `OPERATING-RULES.md` and into enforcement by
   `guardrails.json` + `.claude/hooks/`.
3. **Find the opportunities** — score what `map-process` surfaced against
   `rubric.md`, the same rubric every proposal in this kit uses. Start with
   what's tagged reversible/read-only.
4. **Open the loop** — `.claude/skills/propose/SKILL.md` for anyone to
   submit an idea, `.claude/skills/learn/SKILL.md` to feed lessons back
   weekly. See `examples/specimen-components/` for the loop run end to end.

## Engineers vs everyone else: same loop, different interface

Software engineers already have the loop — it's called branches and pull
requests. An engineering change is a branch, a PR, tests, review, and a
named person's approval; nothing here changes that, it's what
`OPERATING-RULES.md`'s "Agents may" section assumes.

Everyone else gets the same loop through `.claude/skills/propose/SKILL.md`
instead: idea (and optionally a prototype in `sandbox/`) → a written
proposal → a graded, advisory rubric score → a named owner's decision.
Nobody outside engineering needs to see a branch or a diff — the skill
hides git and describes what happened in plain words.

Both paths end the same way: a named person decides, and `PROMOTED` means
backlog, never deployed.

## Harness-neutral by design

`operating-layer/*.md` and `guardrails.json` are plain markdown and JSON —
no Claude Code required to read or edit them. `CLAUDE.md` wires them into
Claude Code with `@` imports; `AGENTS.md` carries the same content in plain
references for Codex and any other harness that reads `AGENTS.md`. The
`.claude/hooks/` enforcement is Claude Code-specific (it's this harness's
hook mechanism); if you adopt a different harness, port the same rules —
read `guardrails.json`, block the same patterns — into whatever pre-action
mechanism it offers. Fig. 06 in the article is the test to run when you pick
one: does it read your operating layer on arrival, can it enforce your
guardrails in code, does it leave an audit trail, does it fit your review
process, what does it cost.

## What this kit deliberately does not do

- **No deploys.** Nothing here ships code to production. `PROMOTED` means a
  backlog entry, never a deployment.
- **No auto-merge.** `guard_commands.py` blocks `gh pr merge` and
  `gh pr review --approve` outright; the `propose` skill never merges its
  own pull request; the GitHub Action grader posts a comment and nothing
  else.
- **Machine grades are advisory, always.** `rubric.md`'s score is a first
  pass for a human. Only a named owner's `Decision:` block is a real
  decision — see rubric.md and `.claude/skills/propose/SKILL.md`.

## What the guardrails are — and aren't

`.claude/hooks/` catches mistakes and keeps an honest agent inside the
rules in `OPERATING-RULES.md`. It is pattern-based — it matches command
text and file paths, the way `guard_commands.py`'s own docstring explains
in detail for `git push` — and pattern matching is not a security boundary
against a determined adversary who's trying to get around it, only a
check against the agent's own straightforward attempt.

For something you actually need to hold under adversarial conditions —
"nothing merges to `main` without review", above all — the real control is
server-side: GitHub's own
[branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
and required reviews, enforced by GitHub itself, not by anything running
on the agent's own machine. This kit's hooks are the first layer of
defence in depth — the one that stops a mistake before it needs a second
layer to catch it — not the last one.

## Licence

MIT — see `LICENSE`.
