import subprocess
from pathlib import Path

from typer.testing import CliRunner

from sdd_toolkit import app

runner = CliRunner()

ISSUE_TRACKER = "docs/agents/issue-tracker.md"

EXPECTED = [
    ".sdd/memory/constitution.md",
    ".sdd/templates/spec-template.md",
    ".sdd/templates/tasks-template.md",
    ".claude/skills/sdd-grill-with-docs/SKILL.md",
    ".claude/skills/sdd-specify/SKILL.md",
    ".claude/skills/sdd-implement/SKILL.md",
    ".github/workflows/sdd.yml",
    ".github/pull_request_template.md",
    "docs/agents/issue-tracker.md",
    ".sdd/sdd.manifest.json",
]


def test_init_scaffolds_everything(tmp_path: Path):
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0, result.output
    for rel in EXPECTED:
        assert (tmp_path / rel).is_file(), f"missing {rel}"
    assert (tmp_path / "specs").is_dir()


def test_issue_tracker_falls_back_without_remote(tmp_path: Path):
    # tmp_path is not a git repo → no remote → generic placeholder.
    runner.invoke(app, ["init", str(tmp_path)])
    text = (tmp_path / ISSUE_TRACKER).read_text()
    assert "{{REPO_SLUG}}" not in text
    assert "<owner>/<repo>" in text
    assert "kklasing" not in text


def test_issue_tracker_uses_detected_remote(tmp_path: Path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "remote", "add", "origin", "git@github.com:acme/widgets.git"],
        cwd=tmp_path,
        check=True,
    )
    runner.invoke(app, ["init", str(tmp_path)])
    text = (tmp_path / ISSUE_TRACKER).read_text()
    assert "acme/widgets" in text
    assert "{{REPO_SLUG}}" not in text
    assert "<owner>/<repo>" not in text


def test_init_preserves_local_edits(tmp_path: Path):
    runner.invoke(app, ["init", str(tmp_path)])
    constitution = tmp_path / ".sdd/memory/constitution.md"
    constitution.write_text("# my edits\n")

    # Re-run without --force: our edit must survive.
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert constitution.read_text() == "# my edits\n"

    # Re-run with --force: our edit is overwritten by the template.
    result = runner.invoke(app, ["init", str(tmp_path), "--force"])
    assert result.exit_code == 0, result.output
    assert constitution.read_text() != "# my edits\n"
    assert "Constitution" in constitution.read_text()
