#!/usr/bin/env python3
"""Validate project-memory Markdown structure offline (not remote ticket truth).

Usage:
  python3 .agents/skills/project-readme-keeper/scripts/validate_project_memory.py [repo_path]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASELINE_STAGES = ("POC", "MVP", "Production Ready")
STAGE_STATUSES = {"Not Started", "In Progress", "Blocked", "Achieved"}
PRIORITIES = {"High", "Medium", "Low", "TBD"}
FEATURE_STATUSES = {"Proposed", "Planned", "In Progress", "Done", "Deferred", "Rejected"}
TICKET_STATUSES = {"Backlog", "Todo", "In Progress", "Blocked", "Done", "Cancelled", "Unknown"}


def section(doc: str, heading: str) -> str | None:
    match = re.search(r"^## " + re.escape(heading) + r"\s*$", doc, re.M)
    if not match:
        return None
    tail = doc[match.end():]
    end = re.search(r"^##?\s+", tail, re.M)
    return tail[:end.start()] if end else tail


def parse_table(section_text: str, required: list[str]) -> list[list[str]] | None:
    # Only the *first contiguous table* belongs to this contract. A section may
    # also contain an optional second table for untracked historical work.
    lines = []
    for source_line in section_text.splitlines():
        line = source_line.strip()
        if line.startswith("|"):
            lines.append(line)
        elif lines:
            break
    if len(lines) < 3:
        return None
    head = [s.strip() for s in lines[0].strip("|").split("|")]
    if head != required:
        return None
    sep = [s.strip() for s in lines[1].strip("|").split("|")]
    if len(sep) != len(head) or not all(re.fullmatch(r":?-{3,}:?", s) for s in sep):
        return None
    rows = []
    for line in lines[2:]:
        cells = [s.strip() for s in line.strip("|").split("|")]
        if len(cells) != len(head):
            return None
        rows.append(cells)
    return rows


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    readme = root / "README.md"
    progress = root / "docs" / "PROGRESS.md"
    if not readme.is_file():
        return (["Missing README.md"], warnings)
    if not progress.is_file():
        return (["Missing docs/PROGRESS.md"], warnings)

    rtext = readme.read_text(encoding="utf-8")
    ptext = progress.read_text(encoding="utf-8")
    for header in ("Project Goal", "Project Stages", "Possible Features", "Progress"):
        if len(re.findall(r"^## " + re.escape(header) + r"\s*$", rtext, re.M)) != 1:
            errors.append(f"README must have exactly one ## {header} section")

    goal = section(rtext, "Project Goal")
    if goal and "Needs clarification" in goal:
        warnings.append("Project goal is unconfirmed; run /grill-me")
    if goal and not goal.strip():
        errors.append("Project Goal is empty")

    stage_rows = parse_table(section(rtext, "Project Stages") or "", ["Stage", "Status", "Exit Criteria", "Evidence / Notes"])
    if stage_rows is None:
        errors.append("Project Stages table must use Stage | Status | Exit Criteria | Evidence / Notes")
    else:
        named = [r[0] for r in stage_rows]
        if named[:3] != list(BASELINE_STAGES):
            errors.append("First three Project Stages must be POC, MVP, Production Ready")
        for row in stage_rows:
            if row[1] not in STAGE_STATUSES:
                errors.append(f"Invalid stage status {row[0]}: {row[1]}")
            if not row[2] or row[2] == "—":
                errors.append(f"Stage {row[0]} is missing exit criteria")
            if row[1] == "Achieved" and (not row[3] or row[3] in {"—", "TBD"}):
                errors.append(f"Achieved stage {row[0]} has no evidence")

    feature_rows = parse_table(section(rtext, "Possible Features") or "", ["Feature", "Description", "Importance", "Urgency", "Status"])
    if feature_rows is None:
        errors.append("Possible Features table missing/invalid")
    else:
        seen: set[str] = set()
        for row in feature_rows:
            if row[0] == "—":
                continue
            if row[0].casefold() in seen:
                errors.append(f"Duplicate Possible Feature: {row[0]}")
            seen.add(row[0].casefold())
            if row[2] not in PRIORITIES or row[3] not in PRIORITIES:
                errors.append(f"Invalid importance/urgency for {row[0]}")
            if row[4] not in FEATURE_STATUSES:
                errors.append(f"Invalid feature status for {row[0]}: {row[4]}")

    progress_block = section(rtext, "Progress") or ""
    if "(docs/PROGRESS.md)" not in progress_block:
        errors.append("README Progress must link to docs/PROGRESS.md")
    if re.search(r"^\|\s*Ticket\s*\|", progress_block, re.M):
        errors.append("README Progress should contain link, not duplicate ticket table")
    if not re.search(r"^# Progress\s*$", ptext, re.M):
        errors.append("docs/PROGRESS.md must start with # Progress")
    ticket_rows = parse_table(ptext, ["Ticket", "Description", "Stage", "Status"])
    if ticket_rows is None:
        errors.append("Progress ticket table must use Ticket | Description | Stage | Status")
    else:
        seen_tickets: set[str] = set()
        for row in ticket_rows:
            if row[0] == "—":
                continue
            if row[0] in seen_tickets:
                errors.append(f"Duplicate ticket row: {row[0]}")
            seen_tickets.add(row[0])
            if row[3] not in TICKET_STATUSES:
                errors.append(f"Invalid ticket status {row[0]}: {row[3]}")
            link = re.search(r"\]\(([^)]+)\)", row[0])
            if not link:
                errors.append(f"Ticket row lacks canonical link: {row[0]}")
            elif not urlsplit(link.group(1)).scheme:
                linked = (progress.parent / unquote(link.group(1).split("#", 1)[0])).resolve()
                if not linked.is_file():
                    warnings.append(f"Local ticket link not available in checkout: {row[0]}")
    if "Sync status:" not in ptext:
        warnings.append("Progress should have an explicit Sync status")
    return errors, warnings


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: validate_project_memory.py [repo_path]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
    errors, warnings = validate(root)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAIL — {len(errors)} errors, {len(warnings)} warnings")
        return 1
    print(f"PASS — README/PROGRESS structure valid ({len(warnings)} warnings; remote status not verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
