import json
from pathlib import Path

from typer.testing import CliRunner

from sdd_toolkit import _assets, app

runner = CliRunner()

MANIFEST = ".sdd/sdd.manifest.json"


def test_version_without_contract(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0, result.output
    assert _assets.version() in result.output
    assert "No .sdd contract installed" in result.output


def test_version_reports_installed_contract(tmp_path: Path, monkeypatch):
    runner.invoke(app, ["init", str(tmp_path)])
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0, result.output
    assert _assets.version() in result.output
    assert "up to date" in result.output


def test_version_flags_mismatched_contract(tmp_path: Path, monkeypatch):
    runner.invoke(app, ["init", str(tmp_path)])
    # Simulate a repo scaffolded by an older CLI.
    manifest_path = tmp_path / MANIFEST
    data = json.loads(manifest_path.read_text())
    data["version"] = "0.0.1"
    manifest_path.write_text(json.dumps(data))

    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0, result.output
    assert "0.0.1" in result.output
    assert "re-run" in result.output


def test_init_reports_version_transition(tmp_path: Path):
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert _assets.version() in result.output

    # Downgrade the recorded version, then re-run: init reports the transition.
    manifest_path = tmp_path / MANIFEST
    data = json.loads(manifest_path.read_text())
    data["version"] = "0.0.1"
    manifest_path.write_text(json.dumps(data))

    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "0.0.1" in result.output
    assert _assets.version() in result.output
