---
name: sdd-implement
description: Implement a feature's tasks from tasks.md — TDD-first, subagent-driven, then reviewed. Combines sdd-tdd and sdd-review into one orchestrated build loop. Use when the spec, plan and tasks already exist and the user wants to build the feature.
disable-model-invocation: true
---

Implement the tasks in the current feature's `tasks.md`, one traceable slice at a time, using subagents for development and review wherever the work can run in parallel.

## Orient

1. Determine the feature folder from the current branch (`specs/NNN-slug/`; branch name == folder name). If you can't, ask which feature to build.
2. Read the contract before writing code: `spec.md` (the `FR-###` requirements), `plan.md` (approach + the Constitution Check), `tasks.md` (the `T###` tasks with their `Traces:` and `Files:`), `.sdd/memory/constitution.md`, and `CONTEXT.md` if it exists (use its ubiquitous language).
3. **Confirm the TDD seams with the user before any tests are written.** The `sdd-tdd` skill only tests at pre-agreed public boundaries — agree them once, up front, so the subagents don't each stop to re-ask.

## Implement, task by task

Work tasks in the order listed; respect dependencies. Independent tasks may run concurrently.

For each task `T###`:

- **Dispatch a subagent** to implement just that task, scoped to its `Files:` and the requirements named in its `Traces:`. Tell it to follow the `sdd-tdd` skill (red → green at the agreed seams, one vertical slice at a time) and to not expand scope beyond the task.
- **Guard the slice.** A well-formed task is already a vertical slice (one behaviour through its layers, with its test). If you find a task that is actually a horizontal layer or splits tests from implementation, stop and fix `tasks.md` (re-slice it) before building — don't let the subagent build it flat.
- **Fan out where it's safe:** tasks whose `Files:` don't overlap can run in parallel subagents; tasks that touch the same files run sequentially to avoid conflicts.
- **On return, verify locally:** run typechecking and the task's relevant test file. If it's red, fix it or bounce it back to the subagent until green.
- **Commit on the current branch** with the task id as the subject prefix: `T###: <subject>`. This is exactly what `sdd trace-check` verifies.
- **Update state:** tick the task in `tasks.md` (`- [ ]` → `- [x]`). If you deviated from the plan, record it in the feature's `decisions.md` (and promote it to an ADR via `sdd-domain-modeling` if it's architecturally significant).

## Verify the whole

- Run the **full test suite once** at the end — it must pass.
- Run `sdd lint` and `sdd trace-check`: every `FR-###` covered by a task, no open `[NEEDS CLARIFICATION]`, every commit traced to a task.

## Review

- Invoke the `sdd-review` skill on this branch's changes. It fans out parallel review subagents across two axes — **Standards** (point it at `.sdd/memory/constitution.md` and any repo coding standards) and **Spec** (does the code actually satisfy the `FR-###` its tasks trace to).
- Triage the findings: fix what's real as further `T###`-prefixed commits (or a follow-up task), and record anything consciously deferred in `decisions.md`.

The feature is done when the full suite passes, both gates pass, and every review finding is either fixed or deliberately deferred with a note.
