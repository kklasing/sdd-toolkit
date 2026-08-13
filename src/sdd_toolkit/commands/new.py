"""`sdd new` — create a numbered feature folder from templates + a matching branch."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer
from rich.console import Console

from sdd_toolkit import _repo

console = Console()

# template filename in .sdd/templates -> rendered filename in the feature folder.
# evidence.md is intentionally absent: it is generated at review time, never
# hand-authored.
TEMPLATE_MAP: dict[str, str] = {
    "spec-template.md": "spec.md",
    "plan-template.md": "plan.md",
    "tasks-template.md": "tasks.md",
    "research-template.md": "research.md",
    "data-model-template.md": "data-model.md",
    "decisions-template.md": "decisions.md",
}


def _render(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(key, value)
    return text


def new(
    title: str = typer.Argument(..., help='Feature title, e.g. "User login".'),
    no_branch: bool = typer.Option(
        False, "--no-branch", help="Do not create/checkout a git branch."
    ),
) -> None:
    """Allocate the next NNN, scaffold `specs/NNN-slug/`, and create the branch."""
    root = _repo.repo_root()
    templates_dir = root / ".sdd" / "templates"
    if not templates_dir.is_dir():
        raise typer.Exit(
            _fail("No .sdd/templates found — run `sdd init` first.")
        )

    number = _repo.next_feature_number(root)
    slug = _repo.slugify(title)
    folder_name = f"{number:03d}-{slug}"
    dest = _repo.specs_dir(root) / folder_name
    if dest.exists():
        raise typer.Exit(_fail(f"{dest} already exists."))

    tokens = {
        "{{NUMBER}}": f"{number:03d}",
        "{{SLUG}}": slug,
        "{{TITLE}}": title,
        "{{BRANCH}}": folder_name,
        "{{DATE}}": date.today().isoformat(),
    }

    dest.mkdir(parents=True)
    (dest / "contracts").mkdir()
    (dest / "contracts" / ".gitkeep").touch()

    created: list[str] = []
    for template_name, out_name in TEMPLATE_MAP.items():
        src = templates_dir / template_name
        if not src.is_file():
            continue
        (dest / out_name).write_text(_render(src.read_text(), tokens))
        created.append(out_name)

    console.print(f"[bold green]Created[/] specs/{folder_name}/")
    for name in created:
        console.print(f"  • {name}")

    if no_branch:
        return
    if not _repo.is_git_repo(root):
        console.print("[yellow]Not a git repo — skipped branch creation.[/]")
        return
    existing = _repo.git(root, "rev-parse", "--verify", folder_name)
    if existing.returncode == 0:
        _repo.git(root, "checkout", folder_name)
        console.print(f"[dim]Checked out existing branch[/] {folder_name}")
    else:
        result = _repo.git(root, "checkout", "-b", folder_name)
        if result.returncode == 0:
            console.print(f"[bold]Branch[/] {folder_name} created and checked out")
        else:
            console.print(f"[yellow]Could not create branch:[/] {result.stderr.strip()}")


def _fail(message: str) -> int:
    console.print(f"[bold red]error:[/] {message}")
    return 1
