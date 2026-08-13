---
name: sdd-tasks
description: Turns an approved plan.md into a dependency-ordered tasks.md where every FR is covered by at least one vertically-sliced task. Use when breaking a plan into tasks, generating tasks.md, or producing an implementation task list for a specified feature.
---

# Tasks

Turn `plan.md` into `tasks.md` — a dependency-ordered task list where **every** `FR-###` in `spec.md` is covered by at least one task, and each task is a **vertical slice** ready for `sdd-implement` to build and commit.

## Pre-Execution Checks

- **Feature folder exists.** Determine it from the current branch (`specs/NNN-slug/`; branch == folder). If it isn't there, run `sdd new "<title>"` first.
- **Inputs complete.** `plan.md` and `spec.md` must both be complete. If `plan.md` is missing or unfinished, route back to `sdd-plan`. Optional inputs — `data-model.md`, `contracts/`, `research.md` — are used when present.

## Outline

1. **Setup.** Identify the feature directory, the `TASKS_FILE` (`tasks.md`, rendered by `sdd new`), and which design docs are available under the folder.
2. **Load design documents.** Read the **required** `plan.md` (approach, structure) and `spec.md` (the `FR-###` requirements, user scenarios, entities, agreed testing seams); the **optional** `data-model.md`, `contracts/`, `research.md`; and `.sdd/memory/constitution.md` if present. Generate tasks from whatever is available.
3. **Generate tasks.** Derive the tasks that deliver the spec:
   - from **user scenarios / FRs** → the behaviour tasks (the primary organisation),
   - from **data-model entities** → folded into the behaviour task that needs them (a shared entity goes in the earliest task that needs it or a foundational task),
   - from **contracts** → the interface tasks,
   - from **setup / foundational** needs → early tasks that unblock the rest.

   Order by dependency (a task appears after anything it depends on). Identify which tasks can run in **parallel** (no shared files, no dependency on incomplete work). Keep an **MVP-first** ordering so the earliest tasks already deliver a usable slice.
4. **Write `tasks.md`** using the template's exact block format (below). Keep task IDs stable — commits reference them (`T001: …`) and `sdd trace-check` verifies it.

## Task format (required — the gates parse this)

```
- [ ] **T001** — <short imperative description>
  - Traces: FR-001, FR-003
  - Files: `path/to/file`, `path/to/test`
  - Issue: #—
```

- Number tasks sequentially (`T001`, `T002`, …).
- `Traces:` lists the `FR-###` requirements this task implements.
- `Files:` lists the source **and** test files the task creates or edits.
- Leave `Issue: #—` as a placeholder — ticket-sync is a later step.

## Slice vertically, not horizontally

Each task must be a **vertical slice**: a thin cut through every layer it needs to deliver one observable behaviour end-to-end, together with its test. This is what lets `sdd-implement` and `sdd-tdd` work a task red → green, one slice at a time. Getting this wrong here quietly defeats TDD downstream.

- Prefer **one task per behaviour** (usually one — occasionally a few closely related — `FR-###`). A task's `Files:` should therefore span the layers that behaviour touches (e.g. handler + model + test), not a single layer.
- **Do not slice by layer.** Tasks like "build all the models", "add every API endpoint", or "write the whole UI" are horizontal — reject them.
- **Do not split tests from implementation.** "Write all the tests" as one task and "implement" as another is the horizontal anti-pattern `sdd-tdd` warns against; each task carries its own test.
- Order by dependency, but keep each unit shippable on its own.

## Verify coverage

Every `FR-###` in `spec.md` must appear in at least one task's `Traces:` line. Walk the FR list and confirm each is covered; add tasks for any that are orphaned. `sdd lint` enforces this at the gate.

## Mandatory Post-Execution

Complete before reporting done:

- **Coverage complete** — every FR is traced by a task.
- **Format valid** — every task has a checkbox, a `T###` id, a `Traces:` line, and a `Files:` line.
- Suggest the user run `sdd lint` to confirm coverage and format.
- **Hand off** to `sdd-implement`.

## Completion Report

Report to the user:

- the `tasks.md` path and the total task count,
- FR coverage (each `FR-###` → the task(s) that cover it),
- the tasks that can run in parallel,
- the suggested **MVP scope** — the earliest vertical slice that is already usable,
- format validation: confirm all tasks follow the block format.

## Done When

- [ ] `tasks.md` generated in the exact block format, dependency-ordered, each task a vertical slice.
- [ ] Every `FR-###` in `spec.md` covered by ≥1 task.
- [ ] Completion reported with task count, coverage, parallel opportunities, and MVP scope.
