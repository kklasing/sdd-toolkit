"""Hash manifest for safe, repeatable installs.

The manifest records the sha256 of every file the installer wrote. On a re-run
this lets us tell three cases apart for each managed file:

* **missing**   – not on disk       → write it.
* **pristine**  – on disk, hash matches the manifest (unmodified toolkit file)
                                     → safe to refresh with the newer version.
* **modified**  – on disk, hash differs from the manifest (user edited it)
                                     → leave it alone unless ``--force``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

MANIFEST_RELPATH = Path(".sdd/sdd.manifest.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


@dataclass
class Manifest:
    version: str
    files: dict[str, str]  # repo-relative posix path -> sha256

    @classmethod
    def load(cls, repo_root: Path) -> "Manifest":
        path = repo_root / MANIFEST_RELPATH
        if not path.is_file():
            return cls(version="", files={})
        data = json.loads(path.read_text())
        return cls(version=data.get("version", ""), files=data.get("files", {}))

    def save(self, repo_root: Path, version: str) -> None:
        path = repo_root / MANIFEST_RELPATH
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": version, "files": dict(sorted(self.files.items()))}
        path.write_text(json.dumps(payload, indent=2) + "\n")

    def status(self, repo_root: Path, relpath: str) -> str:
        """Return 'missing' | 'pristine' | 'modified' for a managed relpath."""
        dest = repo_root / relpath
        if not dest.is_file():
            return "missing"
        recorded = self.files.get(relpath)
        if recorded is None:
            # Present but never installed by us — treat as user-owned.
            return "modified"
        return "pristine" if sha256(dest) == recorded else "modified"
