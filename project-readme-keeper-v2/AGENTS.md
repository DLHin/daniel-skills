# Project Memory — mandatory agent rules

> Installation: merge this section into the repository's existing `AGENTS.md`; never overwrite other rules. Applies to Codex and any agent that reads `AGENTS.md`.

## Read before project work

Before planning, proposing, implementing, closing tickets, or reporting project progress:
- Read `README.md` (goal, stages, possible features, progress link).
- Read `docs/PROGRESS.md` (ticket dashboard), if present.
- Read `docs/agents/issue-tracker.md` (Matt Pocock's configured tracker), if present, **before** reading/writing tickets.
- For detailed workflows, read `.agents/skills/project-readme-keeper/SKILL.md`.
- If documents are missing, initialize/merge them without overwriting existing project documentation.

## Write gates — mandatory in the same task

1. **Goal gate:** README must state exactly one confirmed, clear project-goal sentence. If unclear, run `/grill-me` if installed; otherwise interview the user one focused question at a time. Mark goal `Needs clarification` until confirmed. Do not invent it.
2. **Feature-discussion gate:** When a concrete new feature is discussed, add/update it in README `Possible Features` as `Proposed` (importance/urgency `TBD` unless confirmed). This applies even without code changes. A discussion is **not** authorization to implement or publish tickets.
3. **Decision gate:** When a feature is approved, reprioritized, deferred, rejected, rescoped, or verified complete, update its README row. Keep **importance** (value) distinct from **urgency** (time sensitivity). Do not silently erase features.
4. **Ticket gate:** When tickets are *actually published* using `/to-tickets` or another approved workflow, first write them to the configured tracker, then create/update corresponding `docs/PROGRESS.md` rows. Do not create tickets simply because a feature was discussed. Do not override `/to-tickets`'s approval/quiz step.
5. **Lifecycle gate:** Every ticket transition (including In Progress, Blocked, Done, Cancelled) must update the **canonical ticket/tracker first**, then mirror the status in `docs/PROGRESS.md` before saying the transition is complete. An implementation does not equal Done without its acceptance/verification. Never mark a tracker item Done based on stale dashboard data.
6. **Stage gate:** Keep **POC → MVP → Production Ready** as initial Project Stages in README. More stages can be added. Each must have observable Exit Criteria. Mark Achieved only upon verified evidence; do not infer Production Ready from deployment alone.
7. **Progress gate:** README's `## Progress` contains **a link to `docs/PROGRESS.md`**, not a duplicate ticket table, and no `Recent Progress` or `Current Focus` requirement. `docs/PROGRESS.md` is an **index**, NOT another source of truth. Never invent IDs, dates, tickets, tracker statuses, or stages. If the tracker is unavailable, mark the index potentially stale and report the blocker rather than asserting synchronized status.
8. **Verified-work gate:** On verified completion of task/bugfix/feature, update its canonical ticket and dashboard; review relevant README features and milestones. If work had no ticket, report it as untracked (without a fake ID), and request/link proper tracking when possible. Preserve historical evidence.
9. **Safe edits:** Re-read latest files before writing; preserve unrelated sections, existing decisions, and concurrent agents' work. No destructive rewrites. Do not commit, push, close issues, or deploy solely to satisfy documentation rules without the user's workflow/authority.
10. **Before replying:** Check which gates this task triggered, inspect the updated files and links, and briefly report `README synced` and/or `PROGRESS synced`. If edits were impossible, explicitly report `Not synced` with the exact remaining update. Never claim successful synchronization without verifying it.

**Status vocabularies** are defined in `.agents/skills/project-readme-keeper/SKILL.md`. Agent hard rules cannot force another tool or IDE to edit files during a chat with no repository access. In that case, supply a concrete patch instead of pretending to have edited the repository.
