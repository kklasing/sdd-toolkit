# Issue tracker

> Configuration for skills that need to locate the originating issue/spec of a
> change (e.g. `sdd-review`). Edit for your repo.

- **Tracker**: GitHub Issues
- **Repo**: `kklasing/<repo>`
- **CLI**: `gh` (GitHub CLI) — e.g. `gh issue view <number>`
- **API**: `https://api.github.com/repos/kklasing/<repo>/issues/<number>`

## Conventions

- Issues are created from `tasks.md` (ticket-sync — a future `sdd` step). Each
  task's `Issue: #—` placeholder is replaced with the real issue number.
- The originating spec for a change is the feature folder `specs/NNN-slug/`,
  where `NNN-slug` is the branch name.
- Commit subjects carry the task id: `T012: <subject>`.

## Where specs live

- `specs/NNN-slug/spec.md` — functional requirements (`FR-###`)
- `specs/NNN-slug/tasks.md` — tasks (`T###`) tracing back to requirements
