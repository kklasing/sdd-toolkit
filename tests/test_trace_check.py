from sdd_toolkit.commands.trace_check import commit_task_id


def test_commit_task_id():
    assert commit_task_id("T001: add login form") == "T001"
    assert commit_task_id("  T042: indented") == "T042"
    assert commit_task_id("fix a typo") is None
    assert commit_task_id("T1 no colon") is None
    assert commit_task_id("chore: bump deps") is None
