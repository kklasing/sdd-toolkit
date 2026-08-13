from pathlib import Path

from sdd_toolkit import _repo


def test_slugify():
    assert _repo.slugify("User Login") == "user-login"
    assert _repo.slugify("  Add   OAuth2!! ") == "add-oauth2"
    assert _repo.slugify("###") == "feature"


def test_feature_dir_regex():
    assert _repo.FEATURE_DIR_RE.match("001-user-login")
    assert _repo.FEATURE_DIR_RE.match("042-a")
    assert not _repo.FEATURE_DIR_RE.match("1-user-login")  # not zero-padded
    assert not _repo.FEATURE_DIR_RE.match("001_user_login")  # underscores
    assert not _repo.FEATURE_DIR_RE.match("abc-user")


def test_parse_repo_slug():
    assert _repo.parse_repo_slug("git@github.com:acme/widgets.git") == "acme/widgets"
    assert _repo.parse_repo_slug("https://github.com/acme/widgets.git") == "acme/widgets"
    assert _repo.parse_repo_slug("https://github.com/acme/widgets") == "acme/widgets"
    assert _repo.parse_repo_slug("ssh://git@github.com/acme/widgets.git") == "acme/widgets"
    assert _repo.parse_repo_slug("https://github.com/acme/widgets/") == "acme/widgets"
    assert _repo.parse_repo_slug("not-a-url") is None


def test_next_feature_number(tmp_path: Path):
    specs = tmp_path / "specs"
    specs.mkdir()
    assert _repo.next_feature_number(tmp_path) == 1
    (specs / "001-alpha").mkdir()
    (specs / "004-beta").mkdir()
    (specs / "not-a-feature").mkdir()
    assert _repo.next_feature_number(tmp_path) == 5
