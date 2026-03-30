#!/usr/bin/env python3
"""Move task files from tasks/open to tasks/done when frontmatter status is done."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def vault_root() -> Path:
    ws = os.environ.get("GITHUB_WORKSPACE")
    if ws:
        return Path(ws)
    return Path(__file__).resolve().parent.parent


def frontmatter_status(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    block = parts[1]
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("status:"):
            continue
        val = s.split(":", 1)[1].strip()
        return val.strip('"').strip("'")
    return None


def main() -> int:
    root = vault_root()
    open_dir = root / "tasks" / "open"
    done_dir = root / "tasks" / "done"
    if not open_dir.is_dir():
        print("tasks/open missing; skipping", file=sys.stderr)
        return 0
    done_dir.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    for path in sorted(open_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"skip read {path}: {e}", file=sys.stderr)
            continue
        status = frontmatter_status(text)
        if status != "done":
            continue
        dest = done_dir / path.name
        if dest.exists():
            print(
                f"SKIP collision (already in done): {path.name}",
                file=sys.stderr,
            )
            continue
        subprocess.run(
            ["git", "mv", str(path), str(dest)],
            cwd=root,
            check=True,
        )
        moved.append(path.name)
    print(f"Moved {len(moved)} files: {', '.join(moved) if moved else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
