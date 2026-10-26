---
description: Initialize or sync project documentation using the project-readme-keeper skill
---

Use the installed project-readme-keeper skill for the current project. Find it in the available skills or at `.agents/skills/project-readme-keeper/SKILL.md`, and read its instructions before acting. If it is unavailable, explain that the skill must be installed using the package's INSTALL.md and stop; do not substitute a separate workflow.

Follow the user's accompanying request. If no task was supplied, initialize or reconcile README.md and docs/PROGRESS.md with the project's existing documentation and configured tracker. Preserve existing content, ask only for missing decisions required by the skill, and report the verified sync state. This shortcut alone does not authorize creating tickets, closing issues, committing, pushing, or deploying.
