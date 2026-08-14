# Templates

File bodies for `sb-setup-tooling`. Adapt the package manager (examples use **pnpm**) and drop React/Playwright pieces the user opted out of. Pin to the latest stable major when installing.

## Dependencies

Install as devDependencies.

**Core (always):**

```
eslint @eslint/js typescript-eslint eslint-config-prettier eslint-plugin-import-x
prettier
husky lint-staged
@commitlint/cli @commitlint/config-conventional
typescript
```

**React (if React project):** add to ESLint deps

```
eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
```

**Vitest + Testing Library:**

```
vitest @vitest/coverage-istanbul jsdom
@testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**Playwright (if e2e):**

```
@playwright/test
```

Then `pnpm exec playwright install` to fetch browsers.

**fallow (if codebase intelligence chosen):** a normal devDependency (TypeScript/JavaScript only).

```
fallow
```

The GitHub Action installs the version pinned here (or `latest` if absent), so the same fallow runs locally, in the `pre-push` hook, and in CI.

**Semgrep (if security scan chosen):** not an npm dependency — it's a system tool the developer and CI install separately.

```
pipx install semgrep   # or: pip install semgrep
```

Rules are **not installed into the repo**; they're referenced from the Sunbytes `engineering-standards` baseline at a pinned tag `<BASELINE_REF>` (see § Semgrep baseline). CI installs Semgrep via pip in its own workflow.

## package.json scripts

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "audit": "pnpm audit",
    "semgrep": "semgrep scan --error --metrics=off --config https://raw.githubusercontent.com/Sunbytes-Development/engineering-standards/<BASELINE_REF>/semgrep/baseline.yaml --config https://raw.githubusercontent.com/Sunbytes-Development/engineering-standards/<BASELINE_REF>/semgrep/rules/javascript-typescript.yaml",
    "fallow": "fallow",
    "fallow:audit": "fallow audit",
    "prepare": "husky"
  }
}
```

Replace `<BASELINE_REF>` with the resolved tag. Append a `--config .../rules/nextjs.yaml` and/or `.../rules/nestjs.yaml` URL for those stacks. Drop the `semgrep` script entirely if the scan wasn't chosen. Drop the `fallow` and `fallow:audit` scripts if codebase intelligence wasn't chosen. `fallow` runs the full local pipeline; `fallow:audit` is the changed-file gate used by CI and `pre-push`.

## eslint.config.mjs

Full flat config. Remove the `react`, `react-hooks`, `jsx-a11y` blocks for non-React projects. `eslint-config-prettier` must be **last** so it wins.

```js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import importX from 'eslint-plugin-import-x';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import prettier from 'eslint-config-prettier';

export default tseslint.config(
  { ignores: ['dist', 'build', 'coverage', 'node_modules', '.next', 'playwright-report'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  importX.flatConfigs.recommended,
  importX.flatConfigs.typescript,
  // --- React block (drop for non-React) ---
  {
    files: ['**/*.{jsx,tsx}'],
    ...react.configs.flat.recommended,
    settings: { react: { version: 'detect' } },
  },
  {
    files: ['**/*.{jsx,tsx}'],
    plugins: { 'react-hooks': reactHooks },
    rules: reactHooks.configs.recommended.rules,
  },
  jsxA11y.flatConfigs.recommended,
  // --- end React block ---
  {
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      'import-x/order': [
        'warn',
        { 'newlines-between': 'always', alphabetize: { order: 'asc' } },
      ],
    },
  },
  prettier,
);
```

## .prettierrc

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 100,
  "singleQuote": true,
  "trailingComma": "all",
  "semi": true,
  "arrowParens": "always"
}
```

## .prettierignore

```
dist
build
coverage
node_modules
.next
pnpm-lock.yaml
playwright-report
```

## .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

## .lintstagedrc.json

```json
{
  "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml,css}": ["prettier --write"],
  "*": "prettier --ignore-unknown --write"
}
```

## commitlint.config.js

```js
export default { extends: ['@commitlint/config-conventional'] };
```

## Husky hooks

No shebang needed (Husky v9+). Swap `pnpm` for the detected manager.

`.husky/pre-commit`

```sh
pnpm typecheck
pnpm exec lint-staged
```

`.husky/commit-msg`

```sh
pnpm exec commitlint --edit "$1"
```

`.husky/pre-push`

```sh
pnpm typecheck
pnpm test
pnpm semgrep
pnpm fallow:audit
```

Drop the `pnpm semgrep` line if the scan wasn't chosen, or if the user wants CI-only scanning (no local `semgrep` dependency). Drop the `pnpm fallow:audit` line if codebase intelligence wasn't chosen, or if the user wants the fallow gate in CI only.

## vitest.config.ts

```ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    exclude: ['e2e/**', 'node_modules/**'],
    coverage: {
      provider: 'istanbul',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**'],
      exclude: ['**/*.test.{ts,tsx}', '**/*.d.ts'],
    },
  },
});
```

For a non-React project, set `environment: 'node'` and drop the setup file.

## vitest.setup.ts

```ts
import '@testing-library/jest-dom/vitest';
```

## playwright.config.ts

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  testMatch: '**/*.spec.ts',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: { trace: 'on-first-retry' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
```

## GitHub CI

`.github/workflows/ci.yml` — runs on PRs and pushes to `main`. Swap `pnpm` and the setup steps for the detected package manager. Drop the e2e job if Playwright wasn't set up.

**Node version:** align CI with the project. Prefer `node-version-file: '.nvmrc'` (shown below) so there's one source of truth — if the repo has no `.nvmrc`/`.node-version`, create one from `engines.node` in `package.json` (or ask the user) and reference it. Only fall back to a pinned `node-version: '<major>'` if the user explicitly wants no version file.

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test:coverage
      - run: pnpm audit --audit-level high
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps
      - run: pnpm test:e2e
```

## Dependabot

`.github/dependabot.yml` — GitHub only. Keeps npm dependencies and the workflow
Action versions current. The `npm` ecosystem also covers pnpm and Yarn projects.
`commit-message.prefix` uses conventional-commit types so the PRs pass commitlint
and are classified correctly by release-please (`chore` → no release bump, `ci` for
Action updates). Dev dependencies are grouped into one PR to cut noise; production
dependencies stay separate so each is easy to review.

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
    commit-message:
      prefix: chore
      prefix-development: chore
      include: scope
    groups:
      dev-dependencies:
        dependency-type: development
        update-types: [minor, patch]
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    commit-message:
      prefix: ci
      include: scope
```

For a monorepo, add a `directory` (or `directories`) entry per package. Adjust
`interval` to `daily`/`monthly` if the user wants a different cadence. If the repo
vendors Docker images or other ecosystems, add matching `updates` entries.

## release-please

`.github/workflows/release-please.yml`

```yaml
name: release-please
on:
  push:
    branches: [main]
permissions:
  contents: write
  pull-requests: write
jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: node
```

`release-please-config.json`

```json
{
  "packages": {
    ".": { "release-type": "node" }
  },
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json"
}
```

`.release-please-manifest.json`

```json
{ ".": "0.0.0" }
```

Set the manifest version to the package's current version. For a monorepo, add each package path to both `packages` and the manifest.

## Semgrep baseline

Rules live in [`Sunbytes-Development/engineering-standards`](https://github.com/Sunbytes-Development/engineering-standards) under `semgrep/` and are **referenced by raw URL at a pinned tag**, never copied into the project. Resolve the latest released tag at setup time and substitute it for `<BASELINE_REF>` everywhere (the `semgrep` npm script above, the `pre-push` hook, and the workflow below):

```sh
gh api repos/Sunbytes-Development/engineering-standards/tags --jq '.[0].name'   # current latest: v2.0.0
```

Every repo applies `baseline.yaml` + `rules/javascript-typescript.yaml`. Add `rules/nextjs.yaml` for Next.js and `rules/nestjs.yaml` for NestJS (the stack → rule map is `semgrep/manifest.yaml` in that repo). To bump rules later, change `BASELINE_REF` to a newer tag — updates are opt-in.

### .semgrepignore

Copy to the project root.

```
# Dependencies
node_modules/
vendor/
bower_components/

# Build output / generated
dist/
build/
out/
.next/
coverage/
*.min.js
*.bundle.js

# Misc
.git/
.venv/
*.snap
```

### .github/workflows/semgrep.yml

Copy verbatim, substituting the resolved tag for `<BASELINE_REF>` and keeping only the `--config` lines for stacks the repo actually uses.

```yaml
name: semgrep
on:
  pull_request:
  push:
    branches: [main, master]
permissions:
  contents: read
jobs:
  semgrep:
    runs-on: ubuntu-latest
    env:
      BASELINE_REF: <BASELINE_REF>
      BASE_URL: https://raw.githubusercontent.com/Sunbytes-Development/engineering-standards
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install Semgrep
        run: pip install --no-input semgrep
      - name: Run Semgrep (baseline + stack rules)
        run: |
          BASE="$BASE_URL/$BASELINE_REF/semgrep"
          semgrep scan --error --metrics=off \
            --config "$BASE/baseline.yaml" \
            --config "$BASE/rules/javascript-typescript.yaml" \
            --config "$BASE/rules/nextjs.yaml"
          #   --config "$BASE/rules/nestjs.yaml"   # add for NestJS
```

## Coding standards index

The human-facing companion to the Semgrep baseline. Coding-standard docs live in
[`Sunbytes-Development/engineering-standards`](https://github.com/Sunbytes-Development/engineering-standards)
under `coding-standards/` and are **referenced at a pinned tag, never copied** —
same model as the Semgrep rules, same `<BASELINE_REF>`. Which docs apply is driven
by `coding-standards/manifest.yaml`: pick the `docs` for each detected stack,
baseline-first, deduping across stacks. Common Node/TS cases:

| Detected stack | Docs (in order) |
|---|---|
| TypeScript (no framework) | `typescript.md` |
| React | `typescript.md`, `frameworks/react.md` |
| Next.js | `typescript.md`, `frameworks/react.md`, `frameworks/nextjs.md` |
| NestJS | `typescript.md`, `frameworks/nestjs.md` |

Read the manifest live (workflow step 4) rather than trusting this table — it's an
example, not the source of truth.

### docs/coding-standards.md

Write to the project's docs directory (default `docs/`). List **one bullet per doc
the manifest maps to the detected stack**, in order — the example below is a
Next.js repo. Link to the GitHub blob at the pinned tag (human-readable and
clickable); the raw URL under `raw.githubusercontent.com/.../<BASELINE_REF>/coding-standards/<PATH>`
serves the same file for tools that fetch it.

```markdown
# Coding standards

This project follows the Sunbytes engineering coding standards, referenced from
[`engineering-standards`](https://github.com/Sunbytes-Development/engineering-standards)
at a pinned tag (`<BASELINE_REF>`). They are the human-facing companion to the
Semgrep baseline: Semgrep enforces the mechanically-detectable rules in CI; these
docs cover style, structure, and design, and are enforced in code review.
Requirement levels are MUST / SHOULD / MAY (RFC 2119) — a MUST that can't be met
needs a reviewer-approved exception noted in the PR.

## Sunbytes standards (engineering-standards @ `<BASELINE_REF>`)

Selected for this repo's stack from the standards `manifest.yaml`. **Do not edit
this list by hand** — it's generated from the detected stack. To pick up updates,
bump the tag and re-run `/sb-setup-tooling`.

- [TypeScript](https://github.com/Sunbytes-Development/engineering-standards/blob/<BASELINE_REF>/coding-standards/typescript.md) — language baseline
- [React](https://github.com/Sunbytes-Development/engineering-standards/blob/<BASELINE_REF>/coding-standards/frameworks/react.md)
- [Next.js](https://github.com/Sunbytes-Development/engineering-standards/blob/<BASELINE_REF>/coding-standards/frameworks/nextjs.md)

## Project-specific standards

Standards that apply only to this repository — anything the central standards
don't cover, or a deliberate local deviation (record the reason). This section is
yours to maintain; `/sb-setup-tooling` never overwrites it.

- _None yet._
```

Then link the index from the project's agent-instructions file (`CLAUDE.md` or
`AGENTS.md`) and/or `README` so the coding and review skills find it — e.g. add
`- Coding standards: [docs/coding-standards.md](docs/coding-standards.md)` under
the relevant section. If neither file exists and the user wants a link, ask where
it should go rather than creating one unprompted.

## fallow

[`fallow-rs/fallow`](https://github.com/fallow-rs/fallow) is a TypeScript/JavaScript
codebase-intelligence tool: dead code, circular dependencies, duplication,
complexity/health scoring, and architecture drift. It works with zero config, so
prefer letting it detect the stack rather than hand-writing a config.

### .fallowrc.json

Scaffold with the tool so it detects the framework, workspace layout, test runner,
and package manager:

```sh
pnpm exec fallow init          # scaffold a starter config
# or: pnpm exec fallow recommend  # interactive — asks only subjective choices
```

If the project has a plain layout and you prefer a checked-in starter, this minimal
config is a safe default (fallow fills in the rest from its built-in framework
plugins):

```json
{
  "$schema": "https://fallow.rs/schema/fallowrc.json"
}
```

Keep it minimal — add `include`/`exclude`, architecture presets (e.g. `layered`,
`hexagonal`), or per-analysis tuning only when a run surfaces noise worth
suppressing.

### .github/workflows/fallow.yml

Uses the official Action, which auto-detects the base branch for the diff-scoped
`audit` and installs the fallow version pinned in `package.json`. `fetch-depth: 0`
is required so the diff base is available.

```yaml
name: fallow
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  id-token: write # lets the fallow bot author PR feedback; drop if not wanted
jobs:
  fallow:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: fallow-rs/fallow@v3
```

The Action gates the PR on findings a change introduces (`fail-on-issues` defaults
to true), so a legacy backlog doesn't block merges. Exit code 1 = findings
(gate fails); exit 2 = a real tool error.
