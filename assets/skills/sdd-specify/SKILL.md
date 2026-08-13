---
name: sdd-specify
description: Turns a rough feature idea into a complete, quality-checked spec.md. Use when authoring or writing a feature specification, when the user has a fuzzy idea that needs pinning down into FR-### requirements, or when starting a new feature in specs/NNN-slug/.
---

# Specify

Turn a rough feature idea into a complete `spec.md` — one whose requirements are precise enough to plan against and to pass `sdd lint`. Focus on **what** users need and **why**; never **how** (no tech stack, APIs, or code structure — that belongs in `plan.md`).

## Pre-Execution Checks

Before doing anything else, establish the workspace:

- **Feature description present.** The text the user gave you when invoking this skill *is* the feature description. If it is empty, ERROR and ask for one — do not proceed.
- **Feature folder exists.** Determine the feature folder from the current branch (`specs/NNN-slug/`; branch name == folder name). If it does not exist yet, run `sdd new "<short title>"` to create it (this allocates `NNN`, slugifies the title, renders the templates, and creates + checks out the branch). Only create **one** feature per invocation.
- **Templates & constitution available.** Confirm `.sdd/templates/spec-template.md` exists (it was rendered into the folder's `spec.md` by `sdd new`) and note whether `.sdd/memory/constitution.md` is present. If the toolkit isn't installed, tell the user to run `sdd init` first.

## Outline

Given the feature description, work these steps in order. Steps 1–3 are performed by `sdd new` (run it in Pre-Execution if the folder wasn't there already); do not re-implement them by hand.

1. **Short name** — `sdd new` derives a 2–4 word slug from the title (action-noun form, preserving technical terms/acronyms, e.g. "add user authentication" → `user-auth`). If you're running `sdd new` yourself, pass a title that yields a good slug.
2. **Branch** — `sdd new` creates and checks out the branch named after the folder (`NNN-slug`).
3. **Feature directory** — `sdd new` creates `specs/NNN-slug/` and renders `spec.md` (and the sibling templates) into it. This is your `SPEC_FILE`.
4. **Load the spec template.** Read `spec.md` (rendered from `.sdd/templates/spec-template.md`) to understand the required sections and their order: Summary, Goals, Non-goals, Functional requirements (`FR-###`), Non-functional requirements (`NFR-###`), User scenarios, Open questions.
5. **Load the constitution** (if it exists). Read `.sdd/memory/constitution.md` for principles and constraints the spec must respect (e.g. data classes, boundaries). Don't restate it in the spec — just don't contradict it.
6. **Interrogate the idea.** Invoke the `sdd-grill-with-docs` skill and work its rounds until the user confirms a shared understanding. This is where real requirements are separated from guesses, and where any hard, surprising trade-offs are captured as ADRs and any sharpened terms land in `CONTEXT.md`. Do not skip it.
7. **Synthesise and validate the spec.** Invoke the `sdd-to-spec` skill to turn that shared understanding into `spec.md`. It explores the repository (applying `CONTEXT.md` and the relevant `docs/adr/` ADRs), identifies and validates the testing seams with the user (so `sdd-tdd`/`sdd-implement` reuse them), writes the `FR-###` requirements into the template, and validates the result against its quality checklist — surfacing any `[NEEDS CLARIFICATION]` (max 3) to you for resolution. Every FR traces to the grilling; assumptions are recorded; the spec stays about *what* and *why*, never *how*.

## Mandatory Post-Execution

Complete this before reporting done:

- **Confirm clarifications resolved.** `sdd-to-spec` surfaces any `[NEEDS CLARIFICATION]` for resolution; confirm none remain (unresolved markers fail `sdd lint`). If the user deferred one, flag it explicitly as blocking the gate.
- **Confirm lint-readiness.** The spec should be ready for `sdd lint` once tasks exist (lint checks: required files present, no open clarifications, every FR later covered by a task). FR→task coverage is enforced after `sdd-tasks` runs.
- **Hand off.** The next phase is `sdd-plan` (or `sdd-tasks` after planning). Point the user there.

## Completion Report

Report to the user:

- the feature directory (`specs/NNN-slug/`) and the `spec.md` path,
- a one-line quality summary (checklist passed / issues remaining),
- any unresolved clarifications that will block the gate,
- readiness for the next phase (`sdd-plan`).

## Done When

- [ ] Spec produced and validated by `sdd-to-spec` — `FR-###` requirements traced to the grilling, testing seams validated with the user, ≤3 clarifications each surfaced for resolution.
- [ ] No unresolved `[NEEDS CLARIFICATION]` remain (or deferrals flagged as blocking the gate).
- [ ] Completion reported with the feature directory, spec path, quality summary, and readiness for `sdd-plan`.
