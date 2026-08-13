"""`sdd trace-check` — the trace gate.

Every non-merge commit on the feature branch (base..HEAD) must be prefixed with
its task id, e.g. `T012: wire up the login form`. When the branch matches a
feature folder, referenced task ids are also checked against tasks.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import typer
from rich.console import Console

from sdd_toolkit import _repo

console = Console()

COMMIT_TASK_RE = re.compile(r"^(T\d+):")
TASK_DEFINITION_RE = re.compile(r"\*\*(T\d+)\*\*")


def commit_task_id(subject: str) -> str | None:
    match = COMMIT_TASK_RE.match(subject.strip())
    return match.group(1) if match else None


def _resolve_base(root: Path, base: str | None) -> str | None:
    candidates = [base] if base else ["origin/main", "main", "origin/master", "master"]
    for ref in candidates:
        if ref and _repo.git(root, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return None


def trace_check(
    base: str = typer.Option(
        None, "--base", help="Base ref to diff against (default: origin/main, main…)."
    ),
) -> None:
    """Verify branch commits carry T### task ids. Exits non-zero on violations."""
    root = _repo.repo_root()
    if not _repo.is_git_repo(root):
        console.print("[bold red]error:[/] not a git repository.")
        raise typer.Exit(1)

    base_ref = _resolve_base(root, base)
    if base_ref is None:
        console.print(
            "[yellow]No base ref found[/] (looked for origin/main, main…). "
            "Pass --base to specify one."
        )
        raise typer.Exit(1)

    log = _repo.git(
        root, "log", f"{base_ref}..HEAD", "--no-merges", "--format=%H%x1f%s"
    )
    if log.returncode != 0:
        console.print(f"[bold red]error:[/] git log failed: {log.stderr.strip()}")
        raise typer.Exit(1)

    lines = [ln for ln in log.stdout.splitlines() if ln.strip()]
    if not lines:
        console.print(f"[green]No commits in {base_ref}..HEAD[/] — nothing to check.")
        return

    # Known task ids for the current feature, if we can find them.
    known_tasks: set[str] = set()
    branch = _repo.current_branch(root)
    if branch:
        tasks_md = _repo.specs_dir(root) / branch / "tasks.md"
        if tasks_md.is_file():
            known_tasks = set(TASK_DEFINITION_RE.findall(tasks_md.read_text()))

    violations: list[str] = []
    unknown: list[str] = []
    for line in lines:
        sha, _, subject = line.partition("\x1f")
        task_id = commit_task_id(subject)
        if task_id is None:
            violations.append(f"{sha[:8]}  {subject}")
        elif known_tasks and task_id not in known_tasks:
            unknown.append(f"{sha[:8]}  {task_id} not defined in tasks.md — {subject}")

    if violations:
        console.print(f"[bold red]✗ commits missing a T### prefix[/] (base {base_ref}):")
        for item in violations:
            console.print(f"    [red]•[/] {item}")
    for item in unknown:
        console.print(f"    [yellow]•[/] {item}")

    if violations:
        console.print(
            f"\n[bold red]trace-check failed[/] — {len(violations)} commit(s) "
            "without a task id."
        )
        raise typer.Exit(1)
    console.print(f"[bold green]trace-check passed[/] — {len(lines)} commit(s) traced.")
