"""Locate the bundled asset pack.

Assets (constitution, templates, skills, github, docs) are bundled into the
wheel at ``sdd_toolkit/core_pack/`` via hatchling ``force-include``. When run
from a source checkout (editable install / ``uvx --from .``) that directory does
not exist, so we fall back to the repo's top-level ``assets/`` dir.
"""

from __future__ import annotations

from importlib import metadata
from pathlib import Path


def core_pack() -> Path:
    """Return the directory holding the toolkit's asset pack.

    Prefers the wheel-bundled ``core_pack/`` next to this module; falls back to
    ``<repo-root>/assets`` for source checkouts.
    """
    bundled = Path(__file__).parent / "core_pack"
    if bundled.is_dir():
        return bundled

    repo_assets = Path(__file__).resolve().parents[2] / "assets"
    if repo_assets.is_dir():
        return repo_assets

    raise FileNotFoundError(
        "Could not locate the sdd-toolkit asset pack (neither the bundled "
        "'core_pack/' nor a source 'assets/' directory was found)."
    )


def version() -> str:
    """Best-effort package version, for stamping the manifest."""
    try:
        return metadata.version("sdd-toolkit")
    except metadata.PackageNotFoundError:  # source checkout without install
        return "0.0.0+source"
