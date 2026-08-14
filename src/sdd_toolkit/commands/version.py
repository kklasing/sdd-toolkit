"""`sdd version` — report the CLI version and the contract installed in this repo."""

from __future__ import annotations

from rich.console import Console

from sdd_toolkit import _assets
from sdd_toolkit._repo import repo_root as find_repo_root
from sdd_toolkit.manifest import Manifest

console = Console()


def version() -> None:
    """Show the installed CLI version and the `.sdd` contract version in this repo.

    The CLI version is the toolkit you are running. The contract version is what
    `sdd init` last stamped into this repo's manifest. When they differ, a newer
    (or older) CLI is available and re-running `sdd init` will bring the contract
    into line.
    """
    cli = _assets.version()
    console.print(f"sdd-toolkit [bold]{cli}[/] (CLI)")

    root = find_repo_root()
    installed = Manifest.load(root).version
    if not installed:
        console.print(
            "[dim]No .sdd contract installed here — run "
            "[bold]sdd init[/] to scaffold one.[/]"
        )
        return

    if installed == cli:
        console.print(f"contract in [cyan]{root}[/]: [bold]{installed}[/] (up to date)")
    else:
        console.print(
            f"contract in [cyan]{root}[/]: [bold]{installed}[/] — CLI is "
            f"[bold]{cli}[/]; re-run [bold]sdd init[/] to update."
        )
