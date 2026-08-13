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
7. **Synthesise the spec.** Invoke the `sdd-to-spec` skill to turn that shared understanding into `spec.md`. It explores the repository (applying `CONTEXT.md` and the relevant `docs/adr/` ADRs), identifies and validates the testing seams with the user (so `sdd-tdd`/`sdd-implement` reuse them), and writes the `FR-###` requirements into the template — every FR traced to the grilling, informed guesses recorded under **Assumptions**, and genuine forks marked `[NEEDS CLARIFICATION]` (max 3, prioritised scope > security/privacy > UX > technical). If no clear user flow exists, ERROR — you cannot determine scenarios.
8. **Specification quality validation.** After writing the draft, review it against this checklist and fix what fails (re-run up to 3 times):
   - **Content quality**: no implementation details; focused on user value; readable by a non-technical stakeholder; all mandatory sections completed.
   - **Requirement completeness**: requirements testable and unambiguous; Goals are measurable success criteria (see *Success Criteria Guidelines*); user scenarios cover the primary flows; edge cases identified; scope clearly bounded; assumptions recorded; ≤3 `[NEEDS CLARIFICATION]` markers.
   - For each remaining `[NEEDS CLARIFICATION]`, present it to the user as a numbered question with a small options table so it's cheap to answer:

     ```markdown
     ## Question 1: <topic>

     **Context**: <quote the relevant spec section>
     **What we need to know**: <the specific question>

     | Option | Answer | Implications |
     |--------|--------|--------------|
     | A      | …      | …            |
     | B      | …      | …            |
     | Custom | your own answer | … |
     ```

     Present all questions together (max 3), wait for the answers, then replace each marker with the resolved decision and re-validate.

## Mandatory Post-Execution

Complete this before reporting done:

- **Resolve clarifications.** Every `[NEEDS CLARIFICATION]` marker must be resolved (unresolved markers fail `sdd lint`). If the user defers one, that's their call — flag it explicitly as blocking the gate.
- **Confirm lint-readiness.** The spec should be ready for `sdd lint` once tasks exist (lint checks: required files present, no open clarifications, every FR later covered by a task). Note that FR→task coverage is enforced after `sdd-tasks` runs.
- **Hand off.** The next phase is `sdd-plan` (or `sdd-tasks` after planning). Point the user there.

## Completion Report

Report to the user:

- the feature directory (`specs/NNN-slug/`) and the `spec.md` path,
- a one-line quality summary (checklist passed / issues remaining),
- any unresolved clarifications that will block the gate,
- readiness for the next phase (`sdd-plan`).

## Success Criteria Guidelines

The spec's **Goals** (and any quantitative **NFRs**) are its success criteria. Each must be:

1. **Measurable** — a specific metric (time, percentage, count, rate).
2. **Technology-agnostic** — no frameworks, languages, databases, or tools.
3. **User-focused** — an outcome from the user/business perspective, not a system internal.
4. **Verifiable** — testable without knowing the implementation.

**Good**: "Users can complete checkout in under 3 minutes" · "95% of searches return results in under 1 second" · "Task completion rate improves by 40%".

**Bad** (implementation-focused): "API response time under 200ms" (say "users see results instantly") · "Database handles 1000 TPS" · "React components render efficiently".

## Done When

- [ ] `spec.md` written using the template's sections, with `FR-###` requirements traced to the grilling.
- [ ] Testing seams identified and validated with the user.
- [ ] Spec validated against the quality checklist; ≤3 clarifications, each surfaced to the user.
- [ ] Completion reported with the feature directory, spec path, quality summary, and readiness for `sdd-plan`.
