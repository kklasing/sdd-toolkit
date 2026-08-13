---
name: sdd-to-spec
description: Synthesises an existing shared understanding into a feature spec.md — no interview, just repo exploration, testing-seam identification, and filling the spec template. Use after a design discussion or grilling session, or when sdd-specify needs to turn agreed understanding into FR-### requirements.
disable-model-invocation: true
---

# To spec

Turn an already-shared understanding — the outcome of a grilling session or a substantive prior design conversation — into `specs/NNN-slug/spec.md`. This skill does **not** interview; it *synthesises* what is already known. For the interview, run `sdd-grill-with-docs` first; `sdd-specify` chains the two.

## Prerequisites

- A feature folder `specs/NNN-slug/` with a rendered `spec.md` (run `sdd new "<title>"` if it isn't there).
- Enough shared understanding to synthesise from — a completed grilling, or a substantive conversation and codebase you can draw on. If the idea is still fuzzy, stop and grill first (`sdd-grill-with-docs`).

## Process

### 1. Explore the repository

Examine the current codebase state relevant to this feature. Apply the ubiquitous language from `CONTEXT.md`, and respect any ADRs under `docs/adr/` that touch this area. The spec must fit the system that exists, not an imagined one.

### 2. Identify the testing seams

Map where this feature will be tested. Prefer **existing** seams over new ones, at the **highest** sensible level. Minimise seams that cut across the codebase — ideally one. **Validate the seam choices with the user.** Record them in the spec's user-scenarios / notes so `sdd-tdd` and `sdd-implement` reuse the agreed boundaries rather than renegotiating them.

### 3. Synthesise the spec

Write into `spec.md` using the template's section order (Summary, Goals, Non-goals, Functional requirements, Non-functional requirements, User scenarios, Assumptions, Open questions):

- Each functional requirement is `- **FR-001**: <testable requirement>`, numbered sequentially and zero-padded to three digits. Every FR must trace to something actually discussed — **invent nothing**.
- Fill **User scenarios** (Given/When/Then). Identify **key entities** (using `CONTEXT.md` terms) for `data-model.md` downstream.
- **Make informed guesses** for minor unspecified details and record them under **Assumptions** rather than asking. Reserve `[NEEDS CLARIFICATION: <specific question>]` for genuine forks only — **maximum 3 markers**, prioritised by impact: scope > security/privacy > user experience > technical detail.
- Keep the spec about *what* and *why*, never *how*. Remove template sections that don't apply.

### 4. Validate the spec

After writing the draft, review it against this checklist and fix what fails (re-run up to 3 times):

- **Content quality**: no implementation details; focused on user value; readable by a non-technical stakeholder; all mandatory sections completed.
- **Requirement completeness**: requirements testable and unambiguous; Goals are measurable success criteria (see below); user scenarios cover the primary flows; edge cases identified; scope clearly bounded; assumptions recorded; ≤3 `[NEEDS CLARIFICATION]` markers.

For each remaining `[NEEDS CLARIFICATION]`, present it to the user as a numbered question with a small options table so it's cheap to answer:

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

## Success criteria

The spec's **Goals** (and any quantitative **NFRs**) are its success criteria. Each must be:

1. **Measurable** — a specific metric (time, percentage, count, rate).
2. **Technology-agnostic** — no frameworks, languages, databases, or tools.
3. **User-focused** — an outcome from the user/business perspective, not a system internal.
4. **Verifiable** — testable without knowing the implementation.

**Good**: "Users can complete checkout in under 3 minutes" · "95% of searches return results in under 1 second" · "Task completion rate improves by 40%".

**Bad** (implementation-focused): "API response time under 200ms" (say "users see results instantly") · "Database handles 1000 TPS" · "React components render efficiently".

## Note

Publishing the spec to an issue tracker (the final step of Matt Pocock's original `to-spec`) is handled by ticket-sync, a future `sdd` step — not here.

## Done when

- [ ] Repository explored; the spec fits existing terms and ADRs.
- [ ] Testing seams identified and validated with the user.
- [ ] `spec.md` filled with `FR-###` requirements, assumptions recorded, and ≤3 clarification markers.
- [ ] Spec validated against the quality checklist; each remaining clarification surfaced to the user.
