"""`sdd init` — scaffold the toolkit into a repo (idempotent, manifest-guarded)."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from sdd_toolkit import _assets, _repo
from sdd_toolkit._repo import repo_root as find_repo_root
from sdd_toolkit.manifest import Manifest, sha256_bytes

console = Console()

# (asset-pack subdir, destination prefix relative to the repo root)
LAYOUT: list[tuple[str, str]] = [
    ("memory", ".sdd/memory"),
    ("templates", ".sdd/templates"),
    ("skills", ".claude/skills"),
    ("github", ".github"),
    ("docs", "docs"),
]

# Destination paths (repo-relative) whose {{TOKENS}} are rendered at install time.
RENDERED_FILES = {"docs/agents/issue-tracker.md"}
REPO_SLUG_FALLBACK = "<owner>/<repo>"


def _iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def init(
    here: bool = typer.Option(
        False, "--here", help="Scaffold into the current directory (default)."
    ),
    force: bool = typer.Option(
        False, "--force", help="Overwrite files you have modified."
    ),
    path: Path = typer.Argument(
        None, help="Target repo (defaults to the current git root / cwd)."
    ),
) -> None:
    """Install the sdd-toolkit contract into a repo.

    Copies the constitution, templates, phase skills, CI workflow and PR
    template into the target repo. Re-runs refresh unmodified toolkit files and
    leave your edits alone (use --force to overwrite edits).
    """
    target = (path or Path.cwd()).resolve()
    root = find_repo_root(target)
    pack = _assets.core_pack()

    manifest = Manifest.load(root)
    new_files = dict(manifest.files)

    # Detect the target repo's remote so token-rendered files point at it, not
    # at the toolkit's own repo. Falls back to a generic placeholder.
    slug = _repo.remote_slug(root) or REPO_SLUG_FALLBACK
    tokens = {"{{REPO_SLUG}}": slug}

    wrote: list[str] = []
    refreshed: list[str] = []
    skipped: list[str] = []

    for subdir, dest_prefix in LAYOUT:
        src_root = pack / subdir
        if not src_root.is_dir():
            continue
        for src_file in _iter_files(src_root):
            rel_within = src_file.relative_to(src_root)
            rel = str(Path(dest_prefix) / rel_within)
            dest = root / rel

            data = src_file.read_bytes()
            if rel in RENDERED_FILES:
                text = data.decode()
                for key, value in tokens.items():
                    text = text.replace(key, value)
                data = text.encode()
            content_hash = sha256_bytes(data)
            status = manifest.status(root, rel)

            if status == "modified" and not force:
                skipped.append(rel)
                continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            new_files[rel] = content_hash
            (refreshed if status == "pristine" else wrote).append(rel)

    # Ensure a place for feature folders to land.
    specs = root / "specs"
    specs.mkdir(exist_ok=True)
    gitkeep = specs / ".gitkeep"
    if not any(specs.iterdir()):
        gitkeep.touch()

    manifest.files = new_files
    manifest.save(root, _assets.version())

    console.print(f"[bold green]sdd-toolkit[/] installed into [cyan]{root}[/]")
    console.print(
        f"  {len(wrote)} written, {len(refreshed)} refreshed, "
        f"{len(skipped)} skipped (locally modified)"
    )
    if skipped and not force:
        console.print(
            "  [yellow]Skipped your edits[/] — re-run with [bold]--force[/] to overwrite."
        )
    console.print("\nNext: [bold]sdd new \"<feature title>\"[/] to start a feature.")
