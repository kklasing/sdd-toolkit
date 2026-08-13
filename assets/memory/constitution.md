# Constitution

> The project's non-negotiable rules. `sdd-plan` reads this file and records a
> **Constitution Check** in every `plan.md`; deviations must be justified in
> `decisions.md` and, when architecturally significant, an ADR under `docs/adr/`.
>
> These are your machine-checkable controls — the hooks for ISO/IEC 27001
> Annex A change-management and secure-development controls (e.g. A.8.25,
> A.8.27, A.8.28, A.8.32). **Edit this file to fit your project** before relying
> on it; the placeholders below are a starting point, not law handed down.

## 1. Module boundaries

- <!-- Which modules/packages may depend on which. State the allowed direction
     of dependencies and any forbidden edges. -->
- Cross-boundary calls go through published interfaces only — no reaching into
  another module's internals.

## 2. Secrets handling

- No secrets in source, specs, logs, or evidence files.
- Secrets are read from <!-- your secret store / env mechanism --> only.

## 3. Dependency policy

- **minimumReleaseAge**: a new third-party dependency version must be at least
  <!-- N --> days old before it may be adopted.
- **Allowlist**: new runtime dependencies must be on the approved allowlist, or
  added to it via an ADR.
- Lockfiles are committed and reviewed.

## 4. Data classes → model endpoints

- Define your data classes (e.g. `public`, `internal`, `confidential`,
  `regulated`).
- <!-- Which data classes may be sent to which model/LLM endpoints. State the
     forbidden combinations explicitly. -->

## 5. Review requirements

- Every change merges via PR with at least <!-- N --> human reviewer(s).
- The PR author may not be the sole approver.
- Reviewers attest against this constitution (see the PR template).

## 6. Change management

- Every change traces to a feature folder (`specs/NNN-slug/`) and its
  requirements (`FR-###`).
- Commits carry their task id (`T###:`); the branch is the feature folder name.
