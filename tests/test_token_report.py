import json
from pathlib import Path

from sdd_toolkit.commands.token_report import (
    aggregate_agent,
    aggregate_orchestrator,
    collect_records,
    encode_project_path,
    task_of,
    write_csv,
)


def test_task_of():
    assert task_of("T012: implement the login form") == "T012"
    assert task_of("review of T007 changes") == "T007"
    assert task_of("Standards review of #166") == ""
    assert task_of("") == ""


def test_encode_project_path():
    assert (
        encode_project_path(Path("/Users/a/workspace/sdd-toolkit"))
        == "-Users-a-workspace-sdd-toolkit"
    )
    # dots and underscores collapse to '-' too, matching Claude Code's encoding.
    assert encode_project_path(Path("/x/y.z_q")) == "-x-y-z-q"


def _assistant(model: str, **usage: int) -> str:
    return json.dumps(
        {"type": "assistant", "timestamp": "2026-08-13T10:00:00Z",
         "message": {"model": model, "usage": usage}}
    )


def test_aggregate_agent_sums_usage_and_captures_model():
    lines = [
        _assistant("claude-opus-4-8", input_tokens=2, output_tokens=9,
                   cache_creation_input_tokens=100, cache_read_input_tokens=50),
        _assistant("claude-opus-4-8", input_tokens=3, output_tokens=11,
                   cache_read_input_tokens=25),
        '{"type": "user", "message": {}}',  # non-assistant lines ignored
    ]
    rec = aggregate_agent(lines, {"description": "T012: build it", "agentType": "general-purpose"})
    assert rec is not None
    assert rec.task == "T012"
    assert rec.model == "claude-opus-4-8"
    assert rec.input_tokens == 5
    assert rec.output_tokens == 20
    assert rec.cache_creation_tokens == 100
    assert rec.cache_read_tokens == 75
    assert rec.total_tokens == 200


def test_aggregate_agent_returns_none_without_usage():
    assert aggregate_agent(['{"type": "user", "message": {}}'], {"description": "T1: x"}) is None
    assert aggregate_agent([], {}) is None


def test_aggregate_orchestrator_attributes_to_spec_and_skips_sidechains():
    lines = [
        _assistant("claude-opus-4-8", input_tokens=5, output_tokens=15),
        # a sidechain line must not be double-counted into the orchestrator total
        json.dumps({"type": "assistant", "isSidechain": True,
                    "message": {"model": "claude-opus-4-8",
                                "usage": {"input_tokens": 999, "output_tokens": 999}}}),
    ]
    rec = aggregate_orchestrator(lines, "sess-123", "007-login")
    assert rec is not None
    assert rec.task == "007-login"
    assert rec.agent_type == "orchestrator"
    assert rec.agent_id == "sess-123"
    assert rec.input_tokens == 5
    assert rec.output_tokens == 15
    assert rec.total_tokens == 20  # sidechain's 999s excluded


def test_collect_records_reads_pairs_and_writes_csv(tmp_path: Path):
    subagents = tmp_path / "subagents"
    subagents.mkdir()
    (subagents / "agent-aaa.jsonl").write_text(
        _assistant("claude-opus-4-8", input_tokens=10, output_tokens=20) + "\n"
    )
    (subagents / "agent-aaa.meta.json").write_text(
        json.dumps({"description": "T003: do the thing", "agentType": "general-purpose"})
    )
    # A meta with no matching jsonl is skipped without error.
    (subagents / "agent-orphan.meta.json").write_text(json.dumps({"description": "T999"}))

    records = collect_records(subagents)
    assert len(records) == 1
    assert records[0].task == "T003"
    assert records[0].agent_id == "agent-aaa"

    out = tmp_path / "token-usage.csv"
    write_csv(records, out)
    header, row = out.read_text().splitlines()[:2]
    assert header.startswith("task,description,agent_type,model")
    assert row.startswith("T003,")
    assert "30" in row  # total_tokens
