"""`sdd token-report` — per-run token & model usage from Claude Code transcripts.

Claude Code records every subagent it spawns under
`~/.claude/projects/<encoded-repo-path>/<session>/subagents/` as a pair of files:
an `agent-*.jsonl` transcript (real per-message `usage` and `model`) and an
`agent-*.meta.json` sidecar (the `description` the orchestrator dispatched it
with, plus its `agentType`). This command rolls those up into a CSV — one row
per subagent — of tokens-per-task and which model ran each task, plus a final
orchestrator row for the main session's own (not-per-task) tokens, attributed to
the spec. The CSV opens natively in Excel / Sheets.

Attribution to a task relies on each implementation subagent being dispatched
with a `T###`-prefixed description, which the `sdd-implement` skill instructs.
Subagents whose description carries no task id are still reported, grouped under
their raw description.
"""

from __future__ import annotations

import csv
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from sdd_toolkit import _repo

console = Console()

TASK_RE = re.compile(r"\b(T\d+)\b")

CSV_COLUMNS = (
    "task",
    "description",
    "agent_type",
    "model",
    "input_tokens",
    "cache_creation_tokens",
    "cache_read_tokens",
    "output_tokens",
    "total_tokens",
    "started",
    "agent_id",
)


@dataclass
class AgentUsage:
    """Rolled-up token usage for a single dispatched subagent."""

    agent_id: str
    task: str
    description: str
    agent_type: str
    model: str
    input_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0
    output_tokens: int = 0
    started: str = ""

    @property
    def total_tokens(self) -> int:
        return (
            self.input_tokens
            + self.cache_creation_tokens
            + self.cache_read_tokens
            + self.output_tokens
        )

    def as_row(self) -> dict[str, object]:
        return {
            "task": self.task,
            "description": self.description,
            "agent_type": self.agent_type,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "cache_creation_tokens": self.cache_creation_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "started": self.started,
            "agent_id": self.agent_id,
        }


def task_of(description: str) -> str:
    """The `T###` id embedded in a subagent description, or '' if none."""
    match = TASK_RE.search(description or "")
    return match.group(1) if match else ""


def encode_project_path(path: Path) -> str:
    """Claude Code's on-disk name for a project: non-alphanumerics become '-'.

    e.g. /Users/a/workspace/sdd-toolkit -> -Users-a-workspace-sdd-toolkit
    """
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def _projects_root() -> Path:
    override = os.environ.get("CLAUDE_CONFIG_DIR")
    base = Path(override) if override else Path.home() / ".claude"
    return base / "projects"


def aggregate_agent(jsonl_lines: list[str], meta: dict) -> AgentUsage | None:
    """Sum a subagent transcript's per-message usage into one record.

    Returns None if the transcript carries no token usage at all (e.g. an agent
    that died before its first assistant turn).
    """
    inp = cc = cr = out = 0
    models: list[str] = []
    started = ""
    for line in jsonl_lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        if not started:
            started = str(obj.get("timestamp", ""))
        message = obj.get("message") or {}
        usage = message.get("usage") or {}
        inp += usage.get("input_tokens") or 0
        cc += usage.get("cache_creation_input_tokens") or 0
        cr += usage.get("cache_read_input_tokens") or 0
        out += usage.get("output_tokens") or 0
        model = message.get("model")
        if model and model not in models:
            models.append(model)

    if not (inp or cc or cr or out):
        return None

    description = str(meta.get("description", "")).strip()
    return AgentUsage(
        agent_id=str(meta.get("agent_id", "")),
        task=task_of(description),
        description=description,
        agent_type=str(meta.get("agentType", "")),
        model=", ".join(models),
        input_tokens=inp,
        cache_creation_tokens=cc,
        cache_read_tokens=cr,
        output_tokens=out,
        started=started,
    )


def aggregate_orchestrator(
    jsonl_lines: list[str], session_id: str, reference: str
) -> AgentUsage | None:
    """Roll up the orchestrator's own (main-session) usage into one record.

    The main-session transcript holds only main-loop turns in current Claude Code
    (subagents live in their own files), but older transcripts inlined subagent
    turns as `isSidechain` lines — drop those so we never double-count.

    Orchestrator work isn't per-task, so it's attributed to the spec as a whole:
    the `task` column carries `reference` (the feature folder / branch).
    """
    main_lines = [
        line
        for line in jsonl_lines
        if line.strip() and not _is_sidechain(line)
    ]
    record = aggregate_agent(
        main_lines,
        {
            "description": "orchestrator (main session)",
            "agentType": "orchestrator",
            "agent_id": session_id,
        },
    )
    if record is None:
        return None
    record.task = reference
    return record


def _is_sidechain(line: str) -> bool:
    try:
        return bool(json.loads(line).get("isSidechain"))
    except json.JSONDecodeError:
        return False


def collect_records(subagents_dir: Path) -> list[AgentUsage]:
    """Roll up every agent-*.jsonl/.meta.json pair in a subagents directory."""
    records: list[AgentUsage] = []
    for meta_path in sorted(subagents_dir.glob("*.meta.json")):
        jsonl = meta_path.parent / meta_path.name.replace(".meta.json", ".jsonl")
        if not jsonl.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            meta = {}
        meta.setdefault("agent_id", jsonl.stem)
        record = aggregate_agent(jsonl.read_text().splitlines(), meta)
        if record:
            records.append(record)
    records.sort(key=lambda r: (r.task or "~", r.started))
    return records


def _latest_session_dir(project_dir: Path, session: str | None) -> Path | None:
    if session:
        candidate = project_dir / session
        return candidate if (candidate / "subagents").is_dir() else None
    with_subagents = [
        p for p in project_dir.iterdir() if p.is_dir() and (p / "subagents").is_dir()
    ]
    if not with_subagents:
        return None
    return max(with_subagents, key=lambda p: (p / "subagents").stat().st_mtime)


def _resolve_feature_dir(root: Path, feature: str | None) -> Path | None:
    if feature:
        candidate = _repo.specs_dir(root) / feature
        if candidate.is_dir():
            return candidate
        as_path = Path(feature)
        return as_path if as_path.is_dir() else None
    branch = _repo.current_branch(root)
    if branch:
        on_branch = _repo.specs_dir(root) / branch
        if on_branch.is_dir():
            return on_branch
    return None


def write_csv(records: list[AgentUsage], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for record in records:
            writer.writerow(record.as_row())


def _print_summary(records: list[AgentUsage]) -> None:
    """A per-task rollup to the console (many subagents may share a task)."""
    table = Table(title="Token usage per task")
    table.add_column("Task", style="bold")
    table.add_column("Model")
    table.add_column("Agents", justify="right")
    table.add_column("Input", justify="right")
    table.add_column("Cache", justify="right")
    table.add_column("Output", justify="right")
    table.add_column("Total", justify="right")

    by_task: dict[str, list[AgentUsage]] = {}
    for record in records:
        by_task.setdefault(record.task or record.description or "(unlabelled)", []).append(record)

    grand = 0
    for label, group in by_task.items():
        models = sorted({m for g in group for m in g.model.split(", ") if m})
        inp = sum(g.input_tokens for g in group)
        cache = sum(g.cache_creation_tokens + g.cache_read_tokens for g in group)
        out = sum(g.output_tokens for g in group)
        total = sum(g.total_tokens for g in group)
        grand += total
        table.add_row(
            label,
            ", ".join(models),
            str(len(group)),
            f"{inp:,}",
            f"{cache:,}",
            f"{out:,}",
            f"{total:,}",
        )
    table.add_section()
    table.add_row("TOTAL", "", str(len(records)), "", "", "", f"{grand:,}")
    console.print(table)


def token_report(
    feature: str = typer.Option(
        None, "--feature", "-f", help="Feature folder (default: current branch)."
    ),
    session: str = typer.Option(
        None, "--session", help="Session id under the project dir (default: most recent)."
    ),
    out: Path = typer.Option(
        None, "--out", "-o", help="CSV output path (default: <feature>/token-usage.csv)."
    ),
    project_dir: Path = typer.Option(
        None,
        "--project-dir",
        help="Override the Claude Code projects/<encoded> directory.",
    ),
    no_orchestrator: bool = typer.Option(
        False,
        "--no-orchestrator",
        help="Omit the orchestrator (main-session) row; report subagents only.",
    ),
) -> None:
    """Roll subagent token/model usage from Claude Code transcripts into a CSV."""
    root = _repo.repo_root()

    if project_dir is None:
        project_dir = _projects_root() / encode_project_path(root)
    if not project_dir.is_dir():
        console.print(
            f"[bold red]error:[/] no Claude Code transcripts at {project_dir}.\n"
            "Pass --project-dir if your projects live elsewhere."
        )
        raise typer.Exit(1)

    session_dir = _latest_session_dir(project_dir, session)
    if session_dir is None:
        console.print(f"[yellow]No subagent transcripts found[/] under {project_dir}.")
        raise typer.Exit(1)

    feature_dir = _resolve_feature_dir(root, feature)
    records = collect_records(session_dir / "subagents")

    # The orchestrator's own turns aren't per-task; attribute them to the spec.
    if not no_orchestrator:
        main_jsonl = project_dir / f"{session_dir.name}.jsonl"
        if main_jsonl.is_file():
            reference = feature_dir.name if feature_dir else (
                _repo.current_branch(root) or "(session)"
            )
            orchestrator = aggregate_orchestrator(
                main_jsonl.read_text().splitlines(), session_dir.name, reference
            )
            if orchestrator:
                records.append(orchestrator)

    if not records:
        console.print(
            f"[yellow]No token usage recorded[/] for session {session_dir.name}."
        )
        raise typer.Exit(0)

    if out is None:
        out = (feature_dir or root) / "token-usage.csv"

    write_csv(records, out)
    _print_summary(records)
    rel = out.relative_to(root) if out.is_relative_to(root) else out
    console.print(
        f"\n[green]Wrote[/] {len(records)} row(s) → [bold]{rel}[/] "
        f"(session {session_dir.name})."
    )
