# sdd-toolkit

A spec-driven development toolkit for Claude Code. It adds an **artifact
contract** — feature folders, template-rendered documents, trace IDs, and
machine-checked gates — on top of a set of reusable reasoning skills (grilling,
domain modelling, TDD, review). Consistency stops being a model behaviour and becomes a
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
  memory/constitution.md          # your machine-checked rules (author via sdd-constitution)
  templates/                      # spec / plan / tasks / research / data-model / decisions / evidence
  sdd.manifest.json               # hash manifest for safe upgrades
.claude/skills/
  sdd-grill-with-docs/  sdd-domain-modeling/  sdd-to-spec/                          # thinking skills
  sdd-constitution/  sdd-specify/  sdd-plan/  sdd-tasks/                            # artifact orchestration
  sdd-tdd/  sdd-review/  sdd-implement/                                             # implementation
  sdd-setup-tooling-node/                                                          # optional · Node.js project bootstrap
.github/
  workflows/sdd.yml               # runs `sdd lint` + `sdd trace-check`
  pull_request_template.md        # human-reviewer attestation
docs/agents/issue-tracker.md      # config consumed by sdd-review
specs/                            # feature folders land here
```

## Set up once: the constitution

`sdd init` drops a **placeholder** `constitution.md` — the machine-checked rules
`sdd-plan` gates every plan against. Before your first feature, author it with the
`sdd-constitution` skill: it fills the placeholders from you and the repo, makes
each rule declarative and testable, and stamps a semantic version + Sync Impact
Report into the `## Governance` block. Re-run it whenever the rules change — it
versions amendments (MAJOR/MINOR/PATCH) rather than silently editing law. This is
a project-level step, not per-feature; the per-feature loop below assumes it's done.

**Node.js projects (optional):** `sdd-setup-tooling-node` bootstraps the baseline
dev tooling — ESLint (flat config) + Prettier, Husky hooks, commitlint, release-please,
GitHub CI, Dependabot, Semgrep and a coding-standards index against the Sunbytes
`engineering-standards` baseline, `fallow` codebase intelligence, and a Vitest +
Playwright test stack. It's language-specific (the rest of the toolkit is
language-agnostic) and orthogonal to the loop — run it once when bootstrapping a
Node.js repo, or skip it entirely.

## The loop

One feature runs top-to-bottom through `specs/NNN-slug/`. The **happy path** is the
solid arrows; the **dashed arrows** are the step-backs — when a later phase exposes
a gap, you return to the phase that owns the fix and the trace IDs keep everything
aligned.

Each box is the skill you invoke; the label on each **solid** arrow is what that
phase produces and the next one reads — usually the `.md` it writes. **Dashed**
arrows are the step-backs, each labelled with what triggers it.

```mermaid
flowchart TD
    new(["sdd new"])
    specify["1 · sdd-specify"]
    plan["2 · sdd-plan"]
    tasks["3 · sdd-tasks"]
    implement["4 · sdd-implement"]
    gates{"5 · gates"}
    pr(["PR — review &amp; merge"])

    new -->|folder + branch| specify
    specify -->|spec.md| plan
    plan -->|plan.md| tasks
    tasks -->|tasks.md| implement
    implement -->|code + T### commits| gates
    gates -->|pass| pr

    plan -. spec gap .-> specify
    tasks -. plan insufficient .-> plan
    implement -. task mis-sliced .-> tasks
    implement -. missing requirement .-> specify
    gates -. FR uncovered .-> tasks
    gates -. open clarification .-> specify
    gates -. untraced commit .-> implement
    pr -. changes requested .-> implement
```

### `sdd new "<title>"` — start a feature

The one CLI step. Allocates the next `NNN`, slugifies the title, renders the
templates into `specs/NNN-slug/`, and creates + checks out the branch (branch ==
folder). Everything after this is driven by skills inside Claude Code.

### 1. `sdd-specify` — write the spec

Composes two component skills: `sdd-grill-with-docs` (a relentless interview that
also captures ADRs and glossary terms) then `sdd-to-spec` (explores the repo,
fixes the testing seams, writes the `FR-###` requirements into `spec.md`, and
validates them). Genuine unknowns become `[NEEDS CLARIFICATION]` markers (max 3)
you resolve before moving on. You can also run `sdd-to-spec` on its own to
synthesise a spec from a conversation you've already had, skipping the grilling.

### 2. `sdd-plan` — design the approach

Reads `spec.md` and the constitution and produces `plan.md` with a mandatory
**Constitution Check** (PASS/DEVIATION per rule). It dispatches research subagents
into `research.md` and sharpens the domain (`sdd-domain-modeling`) into
`data-model.md` / `contracts/` as the feature warrants. Deviations are logged in
`decisions.md`.

### 3. `sdd-tasks` — break it into tasks

Turns `plan.md` into `tasks.md`: dependency-ordered, MVP-first, **every `FR-###`
covered by ≥1 task**, each task a **vertical slice** (one behaviour through its
layers, with its test) in the `T### → Traces/Files` format.

### 4. `sdd-implement` — build it

Works `tasks.md` task by task, dispatching subagents that build TDD-first
(`sdd-tdd`) at the agreed seams and committing each as `T###:`, then fans out
`sdd-review` subagents across the Standards (constitution) and Spec (`FR-###`)
axes.

### 5. Gates & PR

`sdd lint` and `sdd trace-check` run locally and in CI (see [The gates](#the-gates)).
A green run plus human review on the PR — with the constitution attestation in the
PR template — closes the loop.

### Stepping back

The dashed edges above: planning can send you back to the spec (`spec gap`); a
mis-sliced task back to `sdd-tasks`; a **missing requirement** surfaced during the
build all the way back to `sdd-specify`; and a **failing gate** back to whichever
phase owns the fix — an uncovered FR to `sdd-tasks`, an open clarification to
`sdd-specify`, an untraced commit to `sdd-implement`. Because every artifact is
traced, stepping back is cheap: edit the earlier file and re-run forward.

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
