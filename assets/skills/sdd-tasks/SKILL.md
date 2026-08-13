---
name: sdd-tasks
description: Turns an approved plan.md into a dependency-ordered tasks.md where every FR is covered by at least one task. Use when breaking a plan into tasks, generating tasks.md, or producing an implementation task list for a specified feature.
---

# Tasks

Turn `plan.md` into `tasks.md` — a dependency-ordered task list where **every** `FR-###` in `spec.md` is covered by at least one task.

## Prerequisites

Work inside an existing `specs/NNN-slug/` folder with a rendered `tasks.md` from the template. If it is missing, tell the user to run `sdd new "<title>"` first. `spec.md` and `plan.md` should both be complete.

## Process

### 1. Read the inputs

Read `specs/NNN-slug/spec.md` (for the full list of `FR-###`) and `plan.md` (for the approach that shapes the tasks).

### 2. Emit tasks

Write tasks in dependency order — a task must appear after anything it depends on. Use this exact block format:

```
- [ ] **T001** — <short imperative description>
  - Traces: FR-001, FR-003
  - Files: `path/to/file`, `path/to/test`
  - Issue: #—
```

- Number tasks sequentially (`T001`, `T002`, …).
- `Traces:` lists the `FR-###` requirements this task implements.
- `Files:` lists the files the task creates or edits (source and tests).
- Leave `Issue: #—` as a placeholder — ticket-sync is a later step.

### Slice vertically, not horizontally

Each task must be a **vertical slice**: a thin cut through every layer it needs
to deliver one observable behaviour end-to-end, together with its test. This is
what lets `sdd-implement` and `sdd-tdd` work a task red → green, one slice at a
time. Getting this wrong here quietly defeats TDD downstream.

- Prefer **one task per behaviour** (usually one — occasionally a few closely
  related — `FR-###`). A task's `Files:` should therefore span the layers that
  behaviour touches (e.g. handler + model + test), not a single layer.
- **Do not slice by layer.** Tasks like "build all the models", "add every API
  endpoint", or "write the whole UI" are horizontal — reject them.
- **Do not split tests from implementation.** "Write all the tests" as one task
  and "implement" as another is the horizontal anti-pattern `sdd-tdd` warns
  against; each task carries its own test.
- Order by dependency, but keep each unit shippable on its own.

### 3. Verify coverage

Every `FR-###` in `spec.md` must appear in at least one task's `Traces:` line. Walk the FR list and confirm each is covered; add tasks for any that are orphaned.

### 4. Hand off

Suggest the user run `sdd lint` to confirm coverage (every FR referenced by ≥1 task, required files present, no unresolved `[NEEDS CLARIFICATION]`).
