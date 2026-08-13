# Evidence — {{TITLE}}

> **Generated, never hand-written.** This template documents the shape the v2
> `sdd evidence` generator fills at review time from git + CI metadata. `sdd new`
> deliberately does not create an `evidence.md`; a hand-authored one is not
> evidence. Auditors accept machine-generated records, not an agent's recollection.

- **Feature**: {{NUMBER}}-{{SLUG}}
- **Generated at**: <!-- pipeline timestamp -->
- **Pipeline run**: <!-- CI run id / URL -->

## Provenance

- **Model + version**: <!-- e.g. claude-opus-4-8 -->
- **Skills dir commit SHA**: <!-- SHA of .claude/skills at build time -->
- **Toolkit version**: <!-- sdd-toolkit version from the manifest -->

## Gate results

- **spec-lint**: <!-- pass/fail -->
- **trace-check**: <!-- pass/fail -->
- **Constitution check**: <!-- pass / deviations -->

## Traceability

<!-- FR-### → tasks → commits → issue, harvested from spec.md/tasks.md/git. -->

## Deviations

<!-- Pulled from decisions.md. -->

## Approval

- **Approver**: <!-- human reviewer, from the merged PR -->
- **PR**: <!-- URL -->
