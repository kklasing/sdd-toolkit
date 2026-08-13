"""sdd — spec-driven development toolkit CLI.

Subcommands:
    sdd init          scaffold the toolkit into a repo
    sdd new "<title>" create a numbered feature folder + branch
    sdd lint          gate: required files, FR coverage, no open clarifications
    sdd trace-check   gate: branch commits carry T### task IDs
"""

from __future__ import annotations

import typer

from sdd_toolkit.commands import init as init_cmd
from sdd_toolkit.commands import lint as lint_cmd
from sdd_toolkit.commands import new as new_cmd
from sdd_toolkit.commands import trace_check as trace_cmd

app = typer.Typer(
    help="Spec-driven development toolkit.",
    no_args_is_help=True,
    add_completion=False,
)

app.command("init")(init_cmd.init)
app.command("new")(new_cmd.new)
app.command("lint")(lint_cmd.lint)
app.command("trace-check")(trace_cmd.trace_check)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
