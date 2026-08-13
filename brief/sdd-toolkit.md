The gap you're feeling isn't prompt quality — it's that Pocock's skills have no *artifact contract*. SpecKit's tickets are consistent because they're rendered from a template with a fixed schema, not because the model was asked nicely. Copy that mechanic; keep his skills for the thinking parts.

**1. Feature folder as the unit of record**
Adopt SpecKit's layout even if you skip the CLI: `specs/NNN-slug/` containing spec.md, research.md, data-model.md, contracts/, plan.md and tasks.md. Add two of your own: `decisions.md` (ADR-lite, deviations from plan) and `evidence.md` (generated, never hand-written).

**2. Trace IDs in everything — this is what actually buys the audit**

* Requirements in spec.md get `FR-001`…
* Tasks carry `T012 → FR-001, FR-003` plus exact file paths
* Commits prefixed `T012:`, branch = folder name, MR links the folder

When an auditor asks "show me where requirement X was specified, implemented, tested and reviewed," it's a grep, not a story.

**3. Generate tickets, don't prompt for them**
tasks.md is the source; a sync script pushes to Github via API with a fixed title format and writes the issue IID back into tasks.md so it's idempotent. The model fills a strict template; the script creates. Consistency stops being a model behaviour.

**4. Constitution = your ISO controls, machine-checked**
`constitution.md` holds module boundaries, secrets handling, dependency policy (`minimumReleaseAge`, allowlists), which data classes may reach which model endpoint, review requirements. SpecKit's plan step already reads the constitution, so make "Constitution check" a mandatory plan.md section. That's your hook into A.8.25/8.27/8.28 and change management A.8.32.

**5. Where Pocock's skills land**
Keep `grill-me`/`grill-with-docs` (pre-specify), `domain-modeling` (feeds data-model.md), `tdd`, `review` (pointed at the constitution), `handoff`. Drop `to-spec` and `to-tickets` — those are precisely what's producing your inconsistency.

**6. Gates, since skills only bias**
CI jobs: `spec-lint` (required files exist, every FR referenced by ≥1 task, no unresolved `[NEEDS CLARIFICATION]`), `trace-check` (commits carry task IDs), plus your existing boundaries/dependency-cruiser/test stages. MR template with explicit human-reviewer attestation.

**7. Evidence must be generated, not narrated**
At MR time, build evidence.md from git and pipeline metadata: model + version, skills directory commit SHA, constitution check result, pipeline run ID, approver, deviations pulled from decisions.md. Auditors accept machine-generated records; they don't accept an agent's recollection of what it did.

Rollout: one pilot repo for two sprints, then freeze it as a template repo and publish the phase skills as an internal package so Claude Code and Codex read the same `skills/` dir via AGENTS.md.
