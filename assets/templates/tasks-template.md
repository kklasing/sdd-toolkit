# Tasks — {{TITLE}}

- **Feature**: {{NUMBER}}-{{SLUG}}
- **Branch**: `{{BRANCH}}`
- **Created**: {{DATE}}
- **Plan**: [plan.md](./plan.md)

> Written by `sdd-tasks`. A dependency-ordered task list. **Every `FR-###` in
> spec.md must appear in at least one task's `Traces:` line** — `sdd lint`
> enforces this. Keep task IDs stable; commits reference them (`T001: …`).
>
> Task format (do not change the shape — the gates parse it):
>
> ```
> - [ ] **T001** — <short imperative description>
>   - Traces: FR-001, FR-003
>   - Files: `path/to/file`, `path/to/test`
>   - Issue: #—
> ```
>
> `Issue: #—` is a placeholder; ticket-sync (a later step) fills the real number.

## Tasks

- [ ] **T001** — <!-- e.g. write a failing test for the login form -->
  - Traces: FR-001
  - Files: `path/to/test`
  - Issue: #—

- [ ] **T002** — <!-- … -->
  - Traces: FR-002
  - Files: `path/to/file`
  - Issue: #—

## Coverage check

<!-- Sanity list: FR-001 → T001; FR-002 → T002; … every FR must map to a task. -->
