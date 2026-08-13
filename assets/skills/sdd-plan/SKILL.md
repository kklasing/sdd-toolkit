---
name: sdd-plan
description: Turns an approved spec.md into an implementation plan.md (and optionally research.md and data-model.md). Use when planning the implementation of a spec, producing plan.md, or working out how a specified feature will be built.
---

# Plan

Turn an approved `spec.md` into a `plan.md` — how the feature will be built, checked against the project's constitution.

## Prerequisites

Work inside an existing `specs/NNN-slug/` folder with a rendered `plan.md` from the template. If it is missing, tell the user to run `sdd new "<title>"` first. The spec should be approved and free of unresolved `[NEEDS CLARIFICATION]` markers.

## Process

### 1. Read the inputs

Read `specs/NNN-slug/spec.md` and `.sdd/memory/constitution.md`. The spec defines *what*; the constitution defines the rules the *how* must obey.

### 2. Optionally sharpen the domain

If the feature introduces or reshapes domain terminology that will feed `data-model.md`, invoke the `sdd-domain-modeling` skill to pin down the ubiquitous language first. Fill `data-model.md` (and `research.md` for open technical questions) from their templates only when the feature warrants them.

### 3. Fill the plan

Fill `plan.md` from the template. It MUST include a completed `## Constitution Check` section:

- Check the plan against **each** rule in `.sdd/memory/constitution.md`.
- Record **PASS** or **DEVIATION** per rule.
- For every DEVIATION, log the decision and its justification in `decisions.md` (from `decisions-template.md`) and reference it from the check.

Keep the plan traceable to the spec — the approach should cover the spec's requirements without inventing new ones.

### 4. Hand off

Once the Constitution Check passes (or all deviations are logged), the plan is ready for `sdd-tasks`.
