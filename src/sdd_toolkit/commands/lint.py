"""`sdd lint` — the spec-lint gate.

Checks, per feature folder:
  * required files exist (spec.md, plan.md, tasks.md)
  * plan.md carries a `## Constitution Check` section
  * no unresolved `[NEEDS CLARIFICATION]` markers remain
  * every `**FR-###**` defined in spec.md is referenced by >=1 task in tasks.md
"""

from __future__ import annotations

import re
from pathlib import Path

import typer
from rich.console import Console

from sdd_toolkit import _repo

console = Console()

REQUIRED_FILES = ("spec.md", "plan.md", "tasks.md")
FR_DEFINITION_RE = re.compile(r"\*\*(FR-\d+)\*\*")
FR_REFERENCE_RE = re.compile(r"\b(FR-\d+)\b")
CLARIFICATION_MARKER = "[NEEDS CLARIFICATION"
CONSTITUTION_HEADING_RE = re.compile(r"^##+\s+Constitution Check", re.MULTILINE)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _content(text: str) -> str:
    """Drop HTML comments — they are template scaffolding, never real content."""
    return HTML_COMMENT_RE.sub("", text)


def lint_feature(feature: Path) -> list[str]:
    """Return a list of human-readable problems for one feature folder."""
    problems: list[str] = []

    for name in REQUIRED_FILES:
        if not (feature / name).is_file():
            problems.append(f"missing required file: {name}")

    spec = feature / "spec.md"
    plan = feature / "plan.md"
    tasks = feature / "tasks.md"

    spec_text = _content(spec.read_text()) if spec.is_file() else ""
    plan_text = _content(plan.read_text()) if plan.is_file() else ""
    tasks_text = _content(tasks.read_text()) if tasks.is_file() else ""

    for name, text in (("spec.md", spec_text), ("plan.md", plan_text)):
        count = text.count(CLARIFICATION_MARKER)
        if count:
            problems.append(f"{name}: {count} unresolved [NEEDS CLARIFICATION] marker(s)")

    if plan_text and not CONSTITUTION_HEADING_RE.search(plan_text):
        problems.append("plan.md: missing a '## Constitution Check' section")

    if spec_text and tasks_text:
        defined = set(FR_DEFINITION_RE.findall(spec_text))
        referenced = set(FR_REFERENCE_RE.findall(tasks_text))
        uncovered = sorted(defined - referenced)
        if uncovered:
            problems.append(
                "requirements not covered by any task: " + ", ".join(uncovered)
            )

    return problems


def _features_to_lint(root: Path, target: str | None, all_: bool) -> list[Path]:
    if target:
        candidate = _repo.specs_dir(root) / target
        if candidate.is_dir():
            return [candidate]
        as_path = Path(target)
        if as_path.is_dir():
            return [as_path]
        raise typer.BadParameter(f"no such feature folder: {target}")

    everything = _repo.feature_dirs(root)
    if all_:
        return everything

    branch = _repo.current_branch(root)
    if branch:
        on_branch = _repo.specs_dir(root) / branch
        if on_branch.is_dir():
            return [on_branch]
    return everything


def lint(
    feature: str = typer.Argument(
        None, help="Feature folder name or path (default: current branch, else all)."
    ),
    all_: bool = typer.Option(False, "--all", help="Lint every feature folder."),
) -> None:
    """Run the spec-lint gate. Exits non-zero if any feature has problems."""
    root = _repo.repo_root()
    features = _features_to_lint(root, feature, all_)

    if not features:
        console.print("[yellow]No feature folders found under specs/.[/] Nothing to lint.")
        return

    total_problems = 0
    for feature_dir in features:
        problems = lint_feature(feature_dir)
        rel = feature_dir.relative_to(root) if feature_dir.is_relative_to(root) else feature_dir
        if problems:
            total_problems += len(problems)
            console.print(f"[bold red]✗[/] {rel}")
            for problem in problems:
                console.print(f"    [red]•[/] {problem}")
        else:
            console.print(f"[bold green]✓[/] {rel}")

    if total_problems:
        console.print(f"\n[bold red]spec-lint failed[/] — {total_problems} problem(s).")
        raise typer.Exit(1)
    console.print("\n[bold green]spec-lint passed.[/]")
