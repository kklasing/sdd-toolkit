from sdd_toolkit.commands.trace_check import commit_task_id


def test_commit_task_id_bare_prefix():
    assert commit_task_id("T001: add login form") == "T001"
    assert commit_task_id("  T042: indented") == "T042"


def test_commit_task_id_conventional_scope():
    assert commit_task_id("feat(T012): wire up login") == "T012"
    assert commit_task_id("fix(T012): handle null") == "T012"
    assert commit_task_id("fix(T012)!: breaking change") == "T012"
    assert commit_task_id("chore(auth,T099): mixed scope") == "T099"
    assert commit_task_id("REFACTOR(T007): case-insensitive type") == "T007"


def test_commit_task_id_rejects_missing_id():
    assert commit_task_id("fix a typo") is None
    assert commit_task_id("T1 no colon") is None
    assert commit_task_id("chore: bump deps") is None
    assert commit_task_id("feat: no task id") is None
    assert commit_task_id("feat(auth): scope without task id") is None
