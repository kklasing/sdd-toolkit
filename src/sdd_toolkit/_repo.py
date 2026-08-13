"""Repo-level helpers: locating the project root, git plumbing, feature folders."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

FEATURE_DIR_RE = re.compile(r"^(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*$")


def git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def is_git_repo(path: Path) -> bool:
    return git(path, "rev-parse", "--git-dir").returncode == 0


def repo_root(start: Path | None = None) -> Path:
    """Return the git top-level, or the cwd if not inside a git repo."""
    start = start or Path.cwd()
    result = git(start, "rev-parse", "--show-toplevel")
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return start.resolve()


def current_branch(repo_root: Path) -> str | None:
    result = git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    if result.returncode != 0:
        return None
    branch = result.stdout.strip()
    return branch or None


def specs_dir(repo_root: Path) -> Path:
    return repo_root / "specs"


def feature_dirs(repo_root: Path) -> list[Path]:
    """All `specs/NNN-slug/` folders, sorted by number."""
    root = specs_dir(repo_root)
    if not root.is_dir():
        return []
    dirs = [p for p in root.iterdir() if p.is_dir() and FEATURE_DIR_RE.match(p.name)]
    return sorted(dirs, key=lambda p: p.name)


def next_feature_number(repo_root: Path) -> int:
    existing = feature_dirs(repo_root)
    if not existing:
        return 1
    return max(int(p.name[:3]) for p in existing) + 1


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "feature"
