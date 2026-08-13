<!-- sdd-toolkit PR template. Keep the attestation section. -->

## Feature

- **Feature folder**: `specs/NNN-slug/`
- **Requirements covered**: FR-...

## Summary

<!-- What changed and why. Link the spec. -->

## Traceability

- [ ] Every commit is prefixed with its task id (`T###:`) — `sdd trace-check` passes
- [ ] `sdd lint` passes (required files present, all FRs covered, no open clarifications)
- [ ] Deviations from the plan are recorded in `decisions.md`

## Reviewer attestation

> The reviewer — who is **not** the sole author — confirms:

- [ ] The change matches the spec's functional requirements
- [ ] The plan's **Constitution Check** holds; any deviations are justified in `decisions.md` (and an ADR where significant)
- [ ] Secrets handling, dependency policy and module boundaries follow the constitution

**Reviewer**: @<!-- github handle -->
