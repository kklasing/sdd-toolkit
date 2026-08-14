---
name: sdd-constitution
description: Create or amend the project's constitution (.sdd/memory/constitution.md) — the machine-checked rules sdd-plan gates every plan against. Use when setting up the toolkit's guardrails for the first time, tailoring the placeholder rules to this project, or amending and versioning them later. Also triggers on "define our principles/rules", "set up the constitution".
---

# Constitution

Author or amend `.sdd/memory/constitution.md` — the project's non-negotiable rules. This is the one artifact that isn't per-feature: every `plan.md` records a **Constitution Check** against it (`sdd-plan`), and deviations are justified in `decisions.md` / promoted to an ADR. Ship it before the first `sdd-plan`; amend it as the project's rules evolve.

## Scope guard

This skill changes **governance only** — the rules in the constitution and their version. It does not implement features, write specs/plans/tasks, or touch code. If the conversation raises non-governance work (a feature to build, a spec to write), record it as a deferred next action and hand off to the skill that owns it (`sdd-specify`, `sdd-plan`, …) — never do it here.

## Pre-Execution Checks

- **Toolkit installed.** Confirm `.sdd/memory/constitution.md` exists. If not, run `sdd init` first — it renders the placeholder template. This skill *fills* that template; it doesn't create the file from nothing.
- **Read what's there.** Load the current constitution. A fresh install is the placeholder template (HTML-comment `<!-- … -->` guidance, `## Governance` at version `0.0.0`); an established one carries real rules and a version — preserve both. This is an **edit in place**, never a rewrite from scratch.
- **Gather sources.** Skim the repo for rules it already implies — `README`, `docs/adr/`, `CONTEXT.md`, the CI workflow, lockfile/allowlist conventions, the PR template's attestation, and any `docs/coding-standards.md` / Semgrep baseline set up by `sdd-setup-tooling-node`. These seed the rules so you interview the user about the *gaps*, not the obvious.

## Outline

1. **Establish each rule from three sources, in priority order:** (1) what the user tells you, (2) what the repo already implies (the Pre-Execution sources), (3) a sensible default left as a `TODO(constitution): …` marker when neither settles it. Never invent a constraint the project hasn't agreed to — an unknown rule is a TODO, not a guess.
2. **Fill the six sections** the template defines — module boundaries, secrets handling, dependency policy, data-classes → model endpoints, review requirements, change management — replacing every `<!-- … -->` placeholder with a concrete rule. Add project-specific sections as the project warrants; keep the existing numbering stable so `sdd-plan`'s per-rule check stays legible.
3. **Make each rule declarative and testable.** "The API layer MUST NOT import from the persistence layer" — not "keep the code clean". A rule `sdd-plan` cannot return a PASS/DEVIATION verdict against isn't a constitution rule; either sharpen it or drop it.
4. **Interview for the gaps only.** Ask the user about the rules the repo and defaults couldn't settle — the real trade-offs: which data classes may reach which model endpoints, the dependency `minimumReleaseAge`, the reviewer count. Don't re-ask what a source already answered.
5. **Version the change** (see *Versioning*), refresh the *Sync Impact Report*, and set the governance dates.

## Versioning

The `## Governance` block carries a semantic version; bump it on every ratified change:

- **MAJOR** — a rule removed, or redefined so that plans/code which previously passed could now fail.
- **MINOR** — a new rule or section, or a material expansion of an existing one.
- **PATCH** — wording, clarification, or typo fixes with no change in what passes.

Dates are ISO `YYYY-MM-DD`. `Ratified` is the original adoption date and never changes once set; `Last amended` moves to today on any ratified change.

## Sync Impact Report

Prepend (or refresh) an HTML comment at the very top of the file recording the change, so amendments are auditable from the file itself:

```
<!-- Sync Impact Report
  Version: 1.1.0 → 1.2.0 (MINOR: added §7 Observability)
  Added:    §7 Observability
  Modified: §3 Dependency policy (minimumReleaseAge 7 → 14 days)
  Removed:  —
  Deferred: TODO(constitution): confirm reviewer count for hotfix branches
-->
```

## Mandatory Post-Execution

- **No stray placeholders.** No `<!-- … -->` template comments and no unexplained `[TOKENS]` remain — only `TODO(constitution): …` markers, each surfaced to the user as unresolved.
- **Version consistent.** The `## Governance` version matches the Sync Impact Report; dates are `YYYY-MM-DD`; `Ratified` is set.
- **Rules are testable.** Every rule reads as something `sdd-plan` can return PASS/DEVIATION on. Re-read section by section and fix any that don't.
- **Downstream still aligns.** If a rule changed what plans must obey, flag that open plans may need re-checking against the new version, and confirm the PR template's attestation still matches the review rules (§5).

## Completion Report

Report to the user:

- the constitution path and its new version + one-line bump rationale,
- any `TODO(constitution): …` markers left unresolved,
- a suggested commit message (e.g. `docs(constitution): ratify v1.0.0`),
- deferred non-governance next actions and the skill that owns each,
- readiness for `sdd-plan` (which now gates against this version).

## Done When

- [ ] Every template placeholder is replaced with a concrete, testable rule (or an explicit `TODO(constitution):` marker surfaced to the user).
- [ ] `## Governance` carries a bumped version, ISO dates, and a `Ratified` date; a Sync Impact Report records the change.
- [ ] Scope stayed governance-only; any non-governance intents were handed off, not executed.
- [ ] Completion reported with path, version, rationale, open TODOs, and readiness for `sdd-plan`.
