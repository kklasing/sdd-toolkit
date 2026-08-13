from pathlib import Path

from sdd_toolkit.commands.lint import lint_feature

GOOD_SPEC = """# Spec
- **FR-001**: The system MUST do a thing.
- **FR-002**: The system MUST do another thing.
"""
GOOD_PLAN = """# Plan
## Constitution Check
| rule | verdict |
| boundaries | PASS |
"""
GOOD_TASKS = """# Tasks
- [ ] **T001** — first
  - Traces: FR-001
- [ ] **T002** — second
  - Traces: FR-002
"""


def _write(feature: Path, spec: str, plan: str, tasks: str) -> None:
    feature.mkdir(parents=True)
    (feature / "spec.md").write_text(spec)
    (feature / "plan.md").write_text(plan)
    (feature / "tasks.md").write_text(tasks)


def test_clean_feature_passes(tmp_path: Path):
    f = tmp_path / "001-ok"
    _write(f, GOOD_SPEC, GOOD_PLAN, GOOD_TASKS)
    assert lint_feature(f) == []


def test_missing_files(tmp_path: Path):
    f = tmp_path / "001-empty"
    f.mkdir()
    problems = lint_feature(f)
    assert any("spec.md" in p for p in problems)
    assert any("plan.md" in p for p in problems)
    assert any("tasks.md" in p for p in problems)


def test_uncovered_requirement(tmp_path: Path):
    f = tmp_path / "001-gap"
    tasks = "# Tasks\n- [ ] **T001** — first\n  - Traces: FR-001\n"
    _write(f, GOOD_SPEC, GOOD_PLAN, tasks)  # FR-002 uncovered
    problems = lint_feature(f)
    assert any("FR-002" in p for p in problems)


def test_open_clarification(tmp_path: Path):
    f = tmp_path / "001-fuzzy"
    spec = GOOD_SPEC + "\n[NEEDS CLARIFICATION: which auth provider?]\n"
    _write(f, spec, GOOD_PLAN, GOOD_TASKS)
    problems = lint_feature(f)
    assert any("CLARIFICATION" in p for p in problems)


def test_missing_constitution_check(tmp_path: Path):
    f = tmp_path / "001-noconst"
    _write(f, GOOD_SPEC, "# Plan\nno check here\n", GOOD_TASKS)
    problems = lint_feature(f)
    assert any("Constitution Check" in p for p in problems)
