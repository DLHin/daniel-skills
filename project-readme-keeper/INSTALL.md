# project-readme-keeper — installation

A repo-local Agent Skill + persistent rules for **Codex** and **Cursor**, designed to cooperate with **Matt Pocock's engineering skills**.

## Contents

```text
AGENTS.md                                  # merge into existing rules
.cursor/rules/project-memory.mdc            # Cursor Always Apply
.agents/skills/project-readme-keeper/
  SKILL.md                                  # agent procedure
  assets/README.template.md                 # template only; never blindly overwrite README
  assets/PROGRESS.template.md               # template only; never blindly overwrite docs/PROGRESS.md
  references/matt-pocock-integration.md     # tracker compatibility notes
  scripts/validate_project_memory.py        # optional offline document check
  scripts/check_project_memory_sync.py      # optional staged git guard
```

## Install safely (repo root)

1. Extract ZIP to a temporary folder. **Copy** `.agents/skills/project-readme-keeper/` to your repo's matching path.
2. **Merge** the rules from `AGENTS.md` into your existing `AGENTS.md`, and optionally copy `.cursor/rules/project-memory.mdc` for Cursor. Do **not** blindly overwrite existing rules.
3. If you haven't yet configured Matt Pocock skills, run **`/setup-matt-pocock-skills`** in the repo. Confirm your ticket tracker; it creates `docs/agents/issue-tracker.md`. If you're using a configured tracker already, keep it.
4. Run the initialization prompt below to merge/add README sections and create/merge `docs/PROGRESS.md`. The two `assets/*.template.md` are NOT project files and should stay in the skill folder.
5. Review the diff and the tracker mapping. Do not mark goals/stages/ticket statuses as known until verified.

### Initialization prompt (paste into Codex or Cursor)

```text
Use the project-readme-keeper skill in this repository. Read AGENTS.md, README.md and docs/agents/issue-tracker.md (if present). Preserve existing docs and rules. Initialize/migrate README.md with Project Goal (one sentence), Project Stages (POC, MVP, Production Ready, extendable), Possible Features, and a Progress link to docs/PROGRESS.md. Create/merge docs/PROGRESS.md as a ticket index of the canonical tracker, with Ticket | Description | Stage | Status. Don't create or publish tickets automatically. If goal is unclear, use /grill-me. If tracker isn't configured, mark progress not synced and tell me to run /setup-matt-pocock-skills. Inspect diff and verify before reporting success.
```

## Routine behavior

| Event | README | docs/PROGRESS.md | Canonical tracker |
|---|---|---|---|
| Discuss feature | Add/update Possible Features | No new ticket | No new ticket |
| Publish `/to-tickets` (after user approval) | Feature decision only | Index real published tickets | Create actual tickets |
| Start/block/complete ticket | Review relevant feature/stage only | Update status | Update **first** |
| Stage acceptance verified | Mark Achieved + evidence | No automatic change | Tickets as appropriate |

The README never duplicates the progress ticket table. The `docs/PROGRESS.md` status is a mirror and the tracker remains authoritative.

## Optional validation

After initialization, run from repo root:

```bash
python3 .agents/skills/project-readme-keeper/scripts/validate_project_memory.py
```

If you stage local Markdown tickets in `.scratch/`, optionally check the staged dashboard sync:

```bash
python3 .agents/skills/project-readme-keeper/scripts/check_project_memory_sync.py
```

Stricter check (requires dashboard to be staged for all code/config changes):

```bash
python3 .agents/skills/project-readme-keeper/scripts/check_project_memory_sync.py --strict-code
```

This is opt-in; the package **does not install a git hook**. These scripts cannot ensure ticket truth, detect remote tracker updates, detect untracked/ignored `.scratch` files, or detect feature discussions that only happen in chat. That requires agent compliance and repository/tracker access.

## Compatibility notes

- `/to-tickets` is user-invoked. It proposes a ticket breakdown and gets approval **before** publishing; don't auto-publish from a feature brainstorm.
- Local ticket files follow Matt Pocock's configured tracker and usually live at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`; do not create a competing `docs/tickets/` directory.
- On GitHub/GitLab/other trackers use real issue links and observed issue statuses.
- If you already used v1, migrate `Recent Progress` history without fabricating ticket identifiers; remove v1 `Current Focus` only if it is skill-owned and safely preserved where useful.

Sources: [Matt Pocock to-tickets](https://github.com/mattpocock/skills/blob/main/docs/engineering/to-tickets.md) · [Tracker setup](https://github.com/mattpocock/skills/blob/main/docs/engineering/setup-matt-pocock-skills.md)
