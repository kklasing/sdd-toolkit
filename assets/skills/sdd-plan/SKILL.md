---
name: sdd-plan
description: Turns an approved spec.md into an implementation plan.md with a mandatory Constitution Check, plus research.md/data-model.md/contracts as the feature warrants. Use when planning the implementation of a spec, producing plan.md, or working out how a specified feature will be built.
---

# Plan

Turn an approved `spec.md` into a `plan.md` — *how* the feature will be built, checked against the project's constitution. This phase produces **design artifacts** (`research.md`, `data-model.md`, `contracts/`); it writes **no code**. The spec says *what*; the plan says *how*; the constitution says what the *how* must obey.

## Pre-Execution Checks

- **Feature folder exists.** Determine it from the current branch (`specs/NNN-slug/`; branch == folder). If it isn't there, run `sdd new "<title>"` first.
- **Spec is approved.** Read `spec.md`. If it still contains unresolved `[NEEDS CLARIFICATION]` markers, stop and route back to `sdd-specify` — you cannot plan against an unsettled spec.
- **Constitution available and authored.** Confirm `.sdd/memory/constitution.md` exists (run `sdd init` if the toolkit isn't installed). If it's still the untouched placeholder template (`<!-- … -->` comments, `## Governance` at `0.0.0`), route to the `sdd-constitution` skill to author it first — the Constitution Check below is mandatory and can't gate against placeholders.

## Outline

1. **Setup.** Identify the feature directory and the files `sdd new` rendered into it: `SPEC_FILE` (`spec.md`), `PLAN_FILE` (`plan.md`), and the sibling artifacts `research.md`, `data-model.md`, `contracts/`.
2. **Load context.** Read `spec.md` (its `FR-###` requirements, user scenarios, key entities, and the agreed testing seams) and `.sdd/memory/constitution.md`. Load the `plan.md` template to learn the required sections.
3. **Technical context.** Fill the plan's **Approach** and **Architecture & interfaces**. Reuse the testing seams already agreed in the spec — don't renegotiate them. Mark genuine unknowns inline as `[NEEDS CLARIFICATION: …]`; they get resolved in Phase 0.
4. **Initial Constitution Check (gate).** Before designing, evaluate the intended approach against **each** constitution rule. Record PASS/DEVIATION. An unjustified violation is a hard stop — resolve or justify it before continuing. See *Constitution gate*.
5. **Phase 0 — Research.** Resolve the unknowns (see *Phases*).
6. **Phase 1 — Design.** Produce `data-model.md` and `contracts/`, sharpening the domain first via `sdd-domain-modeling` (see *Phases*).
7. **Post-Design Constitution Check (gate).** Re-evaluate against the constitution now that the design is concrete. If the design introduced a deviation, log it.
8. **Write the plan.** Fill every `plan.md` section in order, including the completed `## Constitution Check` table. Keep it traceable to the spec — cover its requirements, invent none.

## Phases

### Phase 0 — Research

For each unknown in the technical context, each remaining `[NEEDS CLARIFICATION]`, and each dependency or integration that needs investigation, **dispatch a research subagent** ("Research `<unknown>` for this feature"). Consolidate the findings into `research.md` in this shape:

- **Decision**: what was chosen
- **Rationale**: why
- **Alternatives considered**: what else was evaluated

**Output**: `research.md` with all unknowns resolved. Anything unresolved must be surfaced, not buried.

### Phase 1 — Design & contracts

**Prerequisite**: `research.md` complete.

- **Sharpen the domain first.** If the feature introduces or reshapes domain terminology, invoke `sdd-domain-modeling` to pin down the ubiquitous language in `.sdd/memory/context.md` and record any hard, surprising trade-off as an ADR — *before* writing the data model.
- **Entities → `data-model.md`.** Fields, relationships, validation rules from the requirements, state transitions, and the data class per the constitution — named with `.sdd/memory/context.md` terms.
- **Interfaces → `contracts/`.** If the feature exposes an interface (API endpoints, CLI commands, a library surface), document the contract there. Skip if the feature is purely internal.

**Output**: `data-model.md`, `contracts/*` (as warranted).

## Mandatory Post-Execution

Complete before reporting done:

- **Constitution resolved.** Every rule is PASS, or each DEVIATION is logged in `decisions.md` (from `decisions-template.md`) with a justification and referenced from the check. Promote anything architecturally significant to a `docs/adr/` ADR via `sdd-domain-modeling`.
- **No open clarifications** remain in `plan.md`.
- **Hand off** to `sdd-tasks`.

## Completion Report

Report to the user:

- the feature directory and the `plan.md` path,
- the design artifacts generated (`research.md`, `data-model.md`, `contracts/`),
- the Constitution Check result (all PASS / deviations logged),
- readiness for the next phase (`sdd-tasks`).

## Constitution gate

- Check the plan against **each** rule in `.sdd/memory/constitution.md`.
- Record **PASS** or **DEVIATION** per rule in the plan's `## Constitution Check` table.
- Every **DEVIATION** is logged in `decisions.md` with its justification, referenced from the check, and promoted to an ADR when architecturally significant.
- An unjustified violation is a **hard stop**, not a warning.

## Done When

- [ ] `plan.md` written with all sections and a completed Constitution Check (initial + post-design).
- [ ] Design artifacts generated as warranted (`research.md`, `data-model.md`, `contracts/`).
- [ ] Every deviation logged in `decisions.md`; no open clarifications.
- [ ] Completion reported with the plan path, artifacts, and readiness for `sdd-tasks`.
