---
name: sdd-implement
description: Implement a feature's tasks from tasks.md — TDD-first, subagent-driven, then reviewed. Combines sdd-tdd and sdd-review into one orchestrated build loop. Use when the spec, plan and tasks already exist and the user wants to build the feature.
disable-model-invocation: true
---

Implement the tasks in the current feature's `tasks.md`, one traceable slice at a time. Development and review are always delegated to subagents — a **senior software developer** writes the code, a **senior code reviewer** reviews it. Fan the work out in parallel wherever it's safe, running **at most 5 subagents concurrently**.

## Orient

1. Determine the feature folder from the current branch (`specs/NNN-slug/`; branch name == folder name). If you can't, ask which feature to build.
2. Read the contract before writing code: `spec.md` (the `FR-###` requirements), `plan.md` (approach + the Constitution Check), `tasks.md` (the `T###` tasks with their `Traces:` and `Files:`), `.sdd/memory/constitution.md`, and `.sdd/memory/context.md` if it exists (use its ubiquitous language).
3. **Confirm the TDD seams with the user before any tests are written.** The `sdd-tdd` skill only tests at pre-agreed public boundaries — agree them once, up front, so the subagents don't each stop to re-ask.

## Implement, task by task

Work tasks in the order listed; respect dependencies. Independent tasks may run concurrently.

For each task `T###`:

- **Dispatch a subagent — briefed as a senior software developer** — to implement just that task, scoped to its `Files:` and the requirements named in its `Traces:`. Tell it to follow the `sdd-tdd` skill (red → green at the agreed seams, one vertical slice at a time) and to not expand scope beyond the task. **Prefix the subagent's description with the task id** — e.g. `T012: implement the login form` — so token usage can later be attributed back to the task (see _Report token usage_).
- **Guard the slice.** A well-formed task is already a vertical slice (one behaviour through its layers, with its test). If you find a task that is actually a horizontal layer or splits tests from implementation, stop and fix `tasks.md` (re-slice it) before building — don't let the subagent build it flat.
- **Fan out where it's safe:** tasks whose `Files:` don't overlap can run in parallel subagents; tasks that touch the same files run sequentially to avoid conflicts. Keep **no more than 5 subagents running at once** — queue the rest and dispatch them as slots free up.
- **On return, verify locally:** run typechecking and the task's relevant test file. If it's red, fix it or bounce it back to the subagent until green.
- **Commit on the current branch** with the task id as the subject prefix: `T###: <subject>`. This is exactly what `sdd trace-check` verifies.
- **Update state:** tick the task in `tasks.md` (`- [ ]` → `- [x]`). If you deviated from the plan, record it in the feature's `decisions.md` (and promote it to an ADR via `sdd-domain-modeling` if it's architecturally significant).

## Verify the whole

- Run the **full test suite once** at the end — it must pass.
- Run `sdd lint` and `sdd trace-check`: every `FR-###` covered by a task, no open `[NEEDS CLARIFICATION]`, every commit traced to a task.

## Report token usage

Give the run a cost record: how many tokens each task burned and which model did the work.

- Run `sdd token-report` once the implementation subagents have finished (before or after review — reviews count too). It reads Claude Code's own transcripts for this session, rolls up **real** `usage` and `model`, adds an **estimated USD cost** per task (list prices; cache writes 1.25× input, reads 0.1×), and writes `specs/NNN-slug/token-usage.csv` (opens directly in Excel). It also prints a per-task summary table. Costs are estimates — models with no known rate are left uncosted rather than guessed.
- The CSV has one row per subagent plus a final **orchestrator** row — the main-session (your own) tokens, which aren't per-task, attributed to the spec as a whole (the `task` column carries the feature reference). Pass `--no-orchestrator` to report subagents only.
- Per-task attribution depends on the `T###`-prefixed descriptions you dispatched with — subagents without a task id in their description are still reported, grouped under their raw description. Don't hand-estimate token counts; the numbers come from the transcript, not from you.
- If the report lands in the wrong feature folder or session, scope it explicitly: `sdd token-report --feature NNN-slug --session <id> --out <path>`.

## Review

- Invoke the `sdd-review` skill on this branch's changes. It fans out parallel review subagents — each briefed as a **senior code reviewer** — across two axes — **Standards** (point it at `.sdd/memory/constitution.md` and any repo coding standards) and **Spec** (does the code actually satisfy the `FR-###` its tasks trace to). Hold to the same **5-subagent concurrency cap**.
- Triage the findings: fix what's real as further `T###`-prefixed commits (or a follow-up task), and record anything consciously deferred in `decisions.md`.

The feature is done when the full suite passes, both gates pass, and every review finding is either fixed or deliberately deferred with a note.
