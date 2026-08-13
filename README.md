# sdd-toolkit

A spec-driven development toolkit for Claude Code. It adds an **artifact
contract** — feature folders, template-rendered documents, trace IDs, and
machine-checked gates — on top of the "thinking" skills (grilling, domain
modelling, TDD, review). Consistency stops being a model behaviour and becomes a
property of templates + scripts, the way GitHub's Spec Kit does it.

Installed the same way as Spec Kit: a `uv`-run CLI that scaffolds itself into an
existing repo.

## Install into an existing repo

```bash
uvx --from git+https://github.com/kklasing/sdd-toolkit sdd init --here
```

This scaffolds (idempotently — re-runs preserve your edits):

```
.sdd/
  memory/constitution.md          # your machine-checked rules (edit this first)
  templates/                      # spec / plan / tasks / research / data-model / decisions / evidence
  sdd.manifest.json               # hash manifest for safe upgrades
.claude/skills/
  sdd-grill-with-docs/  sdd-domain-modeling/  sdd-to-spec/  sdd-tdd/  sdd-review/   # thinking skills
  sdd-specify/  sdd-plan/  sdd-tasks/  sdd-implement/                             # artifact orchestration
.github/
  workflows/sdd.yml               # runs `sdd lint` + `sdd trace-check`
  pull_request_template.md        # human-reviewer attestation
docs/agents/issue-tracker.md      # config consumed by sdd-review
specs/                            # feature folders land here
```

## The loop

```bash
sdd new "User login"     # → specs/001-user-login/ (from templates) + branch 001-user-login
```

Then, inside Claude Code, drive each phase with a skill (each grills/thinks, then
fills a strict template):

| Skill          | Reads            | Writes                          |
|----------------|------------------|---------------------------------|
| `sdd-specify`  | your idea        | `spec.md` (`FR-###` requirements)|
| ↳ `sdd-to-spec`| shared understanding | `spec.md` — explores the repo, fixes the testing seams, writes + validates it |
| `sdd-plan`     | `spec.md`, constitution | `plan.md` (+ Constitution Check) |
| `sdd-tasks`    | `plan.md`        | `tasks.md` (`T###` → `FR-###`)  |
| `sdd-implement`| `tasks.md`, constitution | code + `T###:` commits, ticked tasks |

`sdd-specify` composes two component skills: `sdd-grill-with-docs` (the
interview) then `sdd-to-spec` (repo exploration, testing-seam identification, and
writing + validating the spec). You can also invoke `sdd-to-spec` on its own to
turn a design conversation you've already had into a spec, skipping the grilling.

`sdd-implement` runs the build loop: it works through `tasks.md` task by task,
dispatching subagents that build TDD-first (`sdd-tdd`) at agreed seams and
committing each task as `T###:`, then fans out `sdd-review` subagents across the
Standards (constitution) and Spec (`FR-###`) axes.

## The gates

```bash
sdd lint          # required files exist · every FR covered by ≥1 task · no open [NEEDS CLARIFICATION]
sdd trace-check   # every branch commit is prefixed with its task id (T###:)
```

Both run in CI via `.github/workflows/sdd.yml`. They are the enforcement layer —
skills only bias, gates decide.

## The trace

`FR-###` (spec) → `T###` (task, with file paths) → `T###:` commit prefix →
branch = feature folder. An auditor asking "where was requirement X specified,
implemented, tested and reviewed?" gets a grep, not a story.

## Two-tier decisions

- `docs/adr/NNNN-slug.md` — repo-wide architectural decisions (via `sdd-domain-modeling`).
- `specs/NNN-slug/decisions.md` — feature-local deviations from the plan;
  anything architecturally significant is promoted to an ADR and linked.

## Roadmap (v2)

- `sdd sync` — generate GitHub issues from `tasks.md`, write issue numbers back.
- `sdd evidence` — generate `evidence.md` from git + CI metadata at review time.
- A `handoff` skill; multi-agent support (`AGENTS.md`) beyond Claude Code.

## Development

```bash
uv venv && uv pip install -e ".[test]"
uv run pytest
```

Assets live in `assets/` and are bundled into the wheel at
`sdd_toolkit/core_pack/` (see `pyproject.toml`). The CLI resolves the bundled
pack when installed, or `assets/` when run from a source checkout.
