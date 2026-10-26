#!/usr/bin/env python3
"""Optional staged-change check for local ticket files (not a content verifier).

Usage: python3 .agents/skills/project-readme-keeper/scripts/check_project_memory_sync.py [--strict-code]

Default: staged local issue file changes require staged docs/PROGRESS.md.
Strict: staged non-doc code/config changes also require staged docs/PROGRESS.md.
Does not detect ignored .scratch files, remote issues, or chat-only proposals.
"""
from __future__ import annotations

import re
import subprocess
import sys


def main() -> int:
    strict = "--strict-code" in sys.argv[1:]
    if any(arg != "--strict-code" for arg in sys.argv[1:]):
        print("Usage: check_project_memory_sync.py [--strict-code]", file=sys.stderr)
        return 2
    try:
        raw = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRD", "-z"],
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ERROR: Cannot read git staged files", file=sys.stderr)
        return 2
    changed = {s.decode("utf-8") for s in raw.split(b"\0") if s}
    if not changed:
        print("PASS — no staged files")
        return 0
    local_ticket_changes = {
        path for path in changed
        if re.match(r"^\.scratch/[^/]+/issues/[^/]+\.md$", path)
    }
    code_changes = {
        path for path in changed
        if not (path.endswith(".md") or path.startswith((".agents/", ".cursor/", "docs/", ".scratch/")))
    }
    needs_progress = bool(local_ticket_changes or (strict and code_changes))
    if needs_progress and "docs/PROGRESS.md" not in changed:
        print("FAIL — stage docs/PROGRESS.md alongside the ticket/code changes:", file=sys.stderr)
        for path in sorted(local_ticket_changes | (code_changes if strict else set())):
            print(f"  {path}", file=sys.stderr)
        return 1
    print("PASS — staged change sync check (does not prove status consistency)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
