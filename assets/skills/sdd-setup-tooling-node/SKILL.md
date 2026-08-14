---
name: sdd-setup-tooling-node
description: Bootstrap the baseline tooling for a Node.js project — ESLint (flat config) with Prettier, import-x, jsx-a11y, react, react-hooks; Husky hooks (pre-commit typecheck + lint-staged, commit-msg commitlint, pre-push typecheck + tests + Semgrep); commitlint conventional commits; release-please; GitHub CI workflow; Dependabot; Prettier; EditorConfig; pnpm audit; Semgrep security scan against the pinned Sunbytes engineering-standards baseline; a coding-standards index that references the Sunbytes engineering-standards docs for the detected stack (plus a project-specific section); fallow codebase intelligence (dead code, circular dependencies, duplication, complexity, architecture drift) for TypeScript/JavaScript; and Vitest (Istanbul coverage + Testing Library jsdom/React) plus Playwright; and, when the sdd-toolkit is installed, wiring the coding and security standards into the constitution (`.sdd/memory/constitution.md`) as gated rules. Use when the user wants to set up, scaffold, or bootstrap project tooling, linting, formatting, git hooks, conventional commits, releases, CI, coding standards, or a test stack for a Node.js/TypeScript/React repo.
disable-model-invocation: true
---

# Setup project tooling

Bootstrap the baseline dev tooling for a Node.js project. File contents live in [TEMPLATES.md](TEMPLATES.md) — read it before writing files.

## What this sets up

- **ESLint** flat config: typescript-eslint + Prettier (config), import-x, jsx-a11y, react, react-hooks
- **Prettier** + **EditorConfig**
- **Husky** hooks: `pre-commit` (typecheck + lint-staged), `commit-msg` (commitlint), `pre-push` (typecheck + all tests + Semgrep + fallow audit)
- **commitlint** with `config-conventional` (Conventional Commits only)
- **release-please** GitHub Action
- **GitHub CI** workflow (lint + typecheck + coverage + audit, plus an e2e job)
- **Dependabot** config for npm dependency and GitHub Actions updates (conventional-commit prefixes so release-please and commitlint stay happy)
- **pnpm audit** script
- **Semgrep** security scan against the Sunbytes [`engineering-standards`](https://github.com/Sunbytes-Development/engineering-standards) baseline — referenced by a pinned tag (not copied), wired into a dedicated CI workflow and the `pre-push` hook
- **Coding standards** — a `docs/coding-standards.md` index that references the Sunbytes [`engineering-standards`](https://github.com/Sunbytes-Development/engineering-standards) coding-standard docs for the detected stack (selected via that repo's `coding-standards/manifest.yaml`, referenced at the same pinned tag, not copied), plus a section for project-specific standards
- **fallow** codebase intelligence ([`fallow-rs/fallow`](https://github.com/fallow-rs/fallow)) — static analysis for dead code, circular dependencies, duplication, complexity/health scoring, and architecture drift; a full local pipeline plus a changed-file `audit` gate wired into a dedicated CI workflow and the `pre-push` hook (TypeScript/JavaScript only)
- **Vitest** with Istanbul coverage + Testing Library (jsdom, React, jest-dom, user-event)
- **Playwright** e2e
- **Constitution wiring** (when the sdd-toolkit is installed) — records the coding-standards index and the Semgrep security baseline as rules in `.sdd/memory/constitution.md` via the `sdd-constitution` skill, so `sdd-plan`'s Constitution Check and `sdd-review`'s Standards axis gate against the baseline instead of it sitting unreferenced in the repo

## Before you start — ask the user

Detect what you can, then ask only what's still unclear. Don't assume:

1. **Package manager** — detect the lockfile (`pnpm-lock.yaml` → pnpm, etc.). User's default is **pnpm**; confirm if no lockfile exists.
2. **React?** — if not a React project, drop `react`, `react-hooks`, `jsx-a11y` from ESLint and skip jsdom/RTL deps.
3. **Playwright e2e?** — skip if they don't want browser/e2e tests.
4. **release-please + CI** — only if the repo is hosted on GitHub. Ask the release type (default `node`) and whether it's a monorepo. The CI workflow's e2e job is included only if Playwright is set up.
5. **Dependabot?** — default **yes**, GitHub only. Adds `.github/dependabot.yml` with a weekly `npm` update job and a `github-actions` job (keeps the workflow action versions current). Uses conventional-commit prefixes (`chore(deps)` / `ci(deps)`) so commits pass commitlint and feed release-please. Ask the update cadence if `weekly` isn't wanted.
6. **Semgrep scan?** — default **yes**. Adds a pinned scan against the Sunbytes `engineering-standards` baseline via a dedicated CI workflow, and a step in the `pre-push` hook. The hook needs the `semgrep` binary installed locally (`pipx install semgrep`); offer to skip only the hook (keeping the CI scan, which runs in a clean environment) if they don't want that local dependency.
7. **Coding standards index?** — default **yes**. Writes `docs/coding-standards.md` referencing the Sunbytes `engineering-standards` coding-standard docs for the detected stack (at the same pinned tag as Semgrep) plus an empty project-specific section. Ask where the project keeps docs if it isn't `docs/`, and whether to link the index from the project's agent instructions (`CLAUDE.md`/`AGENTS.md`) and/or `README` so the coding and review skills pick it up (default: link from whichever of those already exists).
8. **fallow codebase intelligence?** — default **yes** for TypeScript/JavaScript projects. Adds the `fallow` devDependency, a scaffolded `.fallowrc.json`, `fallow` + `fallow:audit` scripts, a dedicated CI workflow (`.github/workflows/fallow.yml`, only if on GitHub), and a `fallow:audit` step in the `pre-push` hook. It's changed-file scoped, so a legacy backlog doesn't block day one. Offer to skip only the hook step (keeping the CI gate) if the user doesn't want it running on every push.
9. **Wire standards into the constitution?** — only when the sdd-toolkit is installed (`.sdd/memory/constitution.md` exists) *and* the coding-standards index and/or Semgrep are in scope. Default **yes**. Records those standards as gated rules in the constitution via the `sdd-constitution` skill (see Workflow). If the toolkit isn't installed, skip — the standards still live in `docs/coding-standards.md` + CI; mention that `sdd init` + the `sdd-constitution` skill would let plans and reviews gate against them.
10. **Existing config** — never clobber. If a config already exists (ESLint, Prettier, Vitest, etc.), show the user and ask whether to merge, replace, or skip that piece.
11. **Missing prerequisites** — if `typescript`, a `tsconfig.json`, or a `package.json` is missing, stop and ask before continuing.

## Workflow

1. **Detect** package manager, framework (React/Next), TypeScript, the project's Node version (`.nvmrc`, `.node-version`, or `engines.node`), and any existing tool configs. Report what's already present.
2. **Confirm scope** using the questions above. Skip pieces the user opts out of.
3. **Resolve the engineering-standards baseline tag** (if Semgrep and/or the coding-standards index is in scope — both reference the same repo at the same tag). Fetch the latest released tag and pin it — don't hardcode a stale value:
   ```sh
   gh api repos/Sunbytes-Development/engineering-standards/tags --jq '.[0].name'
   ```
   Use that tag everywhere `<BASELINE_REF>` appears in [TEMPLATES.md](TEMPLATES.md) (current latest: `v2.0.0`). For Semgrep, pick the rule configs from the detected stack: `baseline.yaml` + `rules/javascript-typescript.yaml` always, plus `rules/nextjs.yaml` (Next.js) and/or `rules/nestjs.yaml` (NestJS).
4. **Select the coding-standard docs** (if the index is in scope). Read `coding-standards/manifest.yaml` from the repo at the resolved tag and pick the `docs` for each detected stack — a framework stack pulls in its language baseline too, ordered baseline-first (e.g. Next.js → `typescript.md` + `frameworks/react.md` + `frameworks/nextjs.md`). Read it live rather than hardcoding, so new stacks and layering changes are picked up:
   ```sh
   gh api "repos/Sunbytes-Development/engineering-standards/contents/coding-standards/manifest.yaml?ref=<BASELINE_REF>" --jq '.content' | base64 -d
   ```
5. **Install devDependencies** for the agreed pieces (see [TEMPLATES.md](TEMPLATES.md) § Dependencies). Use the detected package manager. Semgrep itself is a system tool, not an npm dep — see § Semgrep. fallow is a normal devDependency — see § fallow.
6. **Write config files** from [TEMPLATES.md](TEMPLATES.md), adapting to package manager and React/no-React. Skip any the user chose not to replace. Include `.semgrepignore` and `.github/workflows/semgrep.yml` if Semgrep is in scope. Write `.github/dependabot.yml` if Dependabot is in scope (GitHub only). Write `docs/coding-standards.md` (§ Coding standards index) if the index is in scope, and link it from the agreed agent-instructions/README file. If fallow is in scope, scaffold `.fallowrc.json` (run `pnpm exec fallow init` to let it detect the stack, or write the starter from § fallow) and add `.github/workflows/fallow.yml` (if on GitHub).
7. **Add package.json scripts**: `lint`, `format`, `typecheck`, `test`, `test:coverage`, `test:e2e`, `audit`, `semgrep`, `fallow`, `fallow:audit`, `prepare`.
8. **Init Husky** (`pnpm dlx husky init` or pkg-manager equivalent) and write the three hook files. Husky v9+ needs no shebang.
9. **Wire standards into the constitution** (if in scope — question 9). When the coding-standards index and/or Semgrep are set up and `.sdd/memory/constitution.md` exists, invoke the `sdd-constitution` skill to amend the constitution — don't hand-edit it yourself (`sdd-constitution` owns the `## Governance` version and Sync Impact Report). Pass it the concrete references and the resolved `<BASELINE_REF>`, and have it record:
   - a **coding-standards** rule — code conforms to the standards indexed in `docs/coding-standards.md` (the engineering-standards baseline at the pinned `<BASELINE_REF>` plus the project-specific section); `sdd-review`'s Standards axis attests against it, deviations justified in `decisions.md`;
   - a **security** rule — every change passes the Semgrep scan against the pinned engineering-standards baseline (`<BASELINE_REF>`), enforced in CI and the `pre-push` hook; new findings block merge.
   Skip and note it if the toolkit isn't installed.
10. **Verify** (below), then tell the user what was set up and what they should review.

## Verify

- [ ] `pnpm lint`, `pnpm typecheck`, `pnpm test` run (or report which scripts are missing source to act on)
- [ ] `.husky/pre-commit`, `.husky/commit-msg`, `.husky/pre-push` exist; `prepare` script is `"husky"`
- [ ] A test commit with a non-conventional message is rejected by `commit-msg`
- [ ] `pnpm audit` runs
- [ ] ESLint, Prettier, EditorConfig, Vitest (and Playwright, if chosen) configs exist
- [ ] release-please and CI workflows exist under `.github/workflows/` (if on GitHub)
- [ ] If Dependabot chosen: `.github/dependabot.yml` exists with `npm` and `github-actions` update jobs and is valid YAML
- [ ] If Semgrep chosen: `.github/workflows/semgrep.yml` and `.semgrepignore` exist, `BASELINE_REF` is pinned to the resolved tag, and `pnpm semgrep` runs (needs the `semgrep` binary)
- [ ] If the coding-standards index chosen: `docs/coding-standards.md` exists, references the docs the manifest maps to the detected stack (baseline-first) at the pinned tag, has a project-specific section, and is linked from the agreed agent-instructions/README file; the standards links resolve
- [ ] If fallow chosen: `.fallowrc.json` exists, `pnpm fallow` and `pnpm fallow:audit` run, `.github/workflows/fallow.yml` exists (if on GitHub), and the `pre-push` hook runs `fallow:audit` (unless the user opted out of the hook step)
- [ ] If constitution wiring chosen: `.sdd/memory/constitution.md` carries the coding-standards and Semgrep rules (referencing `docs/coding-standards.md` and the pinned `<BASELINE_REF>`), its `## Governance` version was bumped, and a Sync Impact Report records the change

## Notes

- Run Prettier for formatting; use `eslint-config-prettier` to turn off conflicting ESLint rules (don't run Prettier _through_ ESLint).
- Vitest unit tests are `*.test.ts(x)`; Playwright e2e are `*.spec.ts` under `e2e/` — keep them separate so Vitest doesn't pick up Playwright specs.
- Semgrep rules are **referenced at a pinned tag, never copied** — projects pick up rule updates deliberately by bumping `BASELINE_REF`. The scan fetches configs over the network, so the `pre-push` hook needs `semgrep` installed locally and network access; CI installs it fresh each run.
- Coding standards work the same way: the `docs/coding-standards.md` index **links** the central docs at the pinned tag rather than copying them, so the whole org shares one baseline and updates are opt-in (bump `BASELINE_REF` and re-run). Semgrep enforces the mechanically-detectable rules in CI; these docs cover the rest (style, structure, design) and are enforced in code review. Keep only the project-specific section by hand — the referenced list is regenerated from the detected stack.
- fallow is **TypeScript/JavaScript only** and complements the other tools rather than overlapping: Semgrep finds security/pattern issues, ESLint finds style/correctness, fallow finds structural rot (dead code, cycles, duplication, complexity, architecture drift). `fallow` runs the full pipeline locally; `fallow audit` is changed-file scoped (pass/warn/fail on findings a change *introduces*), which is what CI and the `pre-push` hook run so a legacy backlog doesn't block work. Unlike Semgrep it's a normal devDependency, so the hook needs no extra system tool — the version in `package.json` is what CI and the hook use. Exit code 1 means findings (a real gate failure); exit 2 is a tool error.
- The **constitution** (`.sdd/memory/constitution.md`) is the machine-checked gate `sdd-plan` and `sdd-review` enforce; `docs/coding-standards.md` and the Semgrep baseline are the standards themselves. Wiring the two rules above into the constitution is what makes the sdd loop actually gate against the engineering-standards baseline — without it, the standards sit in the repo but nothing in the loop references them. The rules **link** the pinned baseline rather than restating it, so bumping `<BASELINE_REF>` and re-running updates both the docs index and the constitution's reference.
- Don't `git commit` for the user unless they ask; if you do, the new hooks act as a smoke test.
