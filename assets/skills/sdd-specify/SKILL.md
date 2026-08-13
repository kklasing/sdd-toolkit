---
name: sdd-specify
description: Turns a rough feature idea into a complete spec.md. Use when authoring or writing a feature specification, when the user has a fuzzy idea that needs pinning down into requirements, or when starting a new feature in specs/NNN-slug/.
---

# Specify

Turn a rough feature idea into a complete `spec.md` — one whose requirements are precise enough to plan against and to pass `sdd lint`.

## Prerequisites

The feature folder must already exist. If `specs/NNN-slug/` (with a rendered `spec.md` from the template) is not there, tell the user to run `sdd new "<title>"` first, then continue. The branch name matches the folder name.

## Process

### 1. Grill the idea first

Before writing anything, invoke the `sdd-grill-with-docs` skill to interrogate the idea and surface unknowns. Do not skip this — the grilling is what separates real requirements from guesses. Work the frontier until the user confirms a shared understanding.

### 2. Fill the spec

Fill `specs/NNN-slug/spec.md` from the template. Write each functional requirement as:

```
- **FR-001**: <requirement text>
```

Number them sequentially, zero-padded to three digits.

Rules:

- **Do not invent requirements.** Every FR must trace to something the user actually said or confirmed during grilling.
- **Mark genuine unknowns, don't guess.** Where the grilling left a real open question, write it inline as `[NEEDS CLARIFICATION: <specific question>]` rather than inventing an answer.
- Keep the spec about *what* and *why*, not *how* — implementation belongs in `plan.md`.

### 3. Hand off

Tell the user to resolve every `[NEEDS CLARIFICATION: ...]` marker before running `sdd lint` — unresolved markers fail the gate. Once clarifications are resolved, the spec is ready for `sdd-plan`.
