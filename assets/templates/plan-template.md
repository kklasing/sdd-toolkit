# Plan — {{TITLE}}

- **Feature**: {{NUMBER}}-{{SLUG}}
- **Branch**: `{{BRANCH}}`
- **Created**: {{DATE}}
- **Spec**: [spec.md](./spec.md)

> Written by `sdd-plan`. Turn the approved spec into an implementation approach.
> The **Constitution Check** section below is mandatory — `sdd lint` fails if it
> is missing.

## Approach

<!-- The shape of the implementation: components touched, data flow, sequencing. -->

## Architecture & interfaces

<!-- Key modules/boundaries, public interfaces (the "seams" sdd-tdd will test at),
     and how they map onto the functional requirements. -->

## Data model

<!-- Summarise or link to data-model.md. Reference domain terms from .sdd/memory/context.md. -->

## Research

<!-- Summarise or link to research.md for anything that needed investigation. -->

## Constitution Check

<!--
Check this plan against every rule in .sdd/memory/constitution.md. For each,
record PASS or DEVIATION. Every DEVIATION MUST be logged in decisions.md with a
justification, and promoted to a docs/adr/ ADR if architecturally significant.
-->

| Constitution rule | Verdict | Note |
|---|---|---|
| Module boundaries | PASS / DEVIATION | |
| Secrets handling | PASS / DEVIATION | |
| Dependency policy (minimumReleaseAge, allowlist) | PASS / DEVIATION | |
| Data-class → model-endpoint routing | PASS / DEVIATION | |
| Review requirements | PASS / DEVIATION | |

**Deviations**: <!-- none | see decisions.md#… -->

## Risks & mitigations

- <!-- risk → mitigation -->
