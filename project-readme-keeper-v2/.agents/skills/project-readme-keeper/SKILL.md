---
name: project-readme-keeper
description: Initialize and continuously sync a concise README (one-sentence goal, extensible project stages, possible features, link to Progress) and docs/PROGRESS.md (all ticket statuses) with Matt Pocock's configured issue tracker. Use when starting a repo, discussing new features, deciding scope, publishing tickets, implementing, or verifying completion.
---

# Project README Keeper v2

Keep `README.md` as the **project overview** and `docs/PROGRESS.md` as the **ticket dashboard**. The configured issue tracker remains the **sole canonical record for tickets**. Read the repo's `AGENTS.md` hard rules and `references/matt-pocock-integration.md` when relevant.

## Start of every project task

1. Read current `README.md`, `docs/PROGRESS.md`, and `docs/agents/issue-tracker.md` (if they exist). Read the specific canonical tickets involved, not only cached progress rows.
2. Determine whether this is a feature proposal, feature decision, ticket publication, lifecycle change, verified completion, stage milestone, or an ordinary question with no project change.
3. Apply only the triggered updates; keep the two files short and preserve all unrelated existing content. A new concrete feature discussion qualifies **even if there are no code edits**.
4. Before finishing, re-read changes and compare ticket rows with the canonical tracker; report sync status truthfully. If file/issue writes are unavailable, supply an exact patch and say `Not synced`.

## Initialization / migration

- If README absent: use `assets/README.template.md` as a starting point. If present: *merge* missing sections without replacing existing helpful content, links, setup instructions, or custom sections. Prefer the `<!-- project-readme-keeper:start/end -->` block if it doesn't duplicate existing equivalent headings.
- Project Goal must be **one confirmed sentence** describing intended user and desired outcome. If unclear, run `/grill-me` if installed; otherwise one focused question at a time. Leave `Needs clarification` until confirmed. No fabricated goal.
- Create/merge README `Project Stages` rows **POC → MVP → Production Ready** (in that order), preserving additional stages. Tailor observable exit criteria when the user or evidence supports them; initial template criteria are suggestions, not proof of achievement.
- Create/merge README `Possible Features` table. Use the compact columns below; keep existing features, including deferred/rejected.
- Add README `## Progress` with **only** the link `[View all tickets and progress](docs/PROGRESS.md)` (a short explanatory line is allowed). Create/merge `docs/PROGRESS.md` from `assets/PROGRESS.template.md`, respecting existing contents.
- **v1 migration:** stop maintaining README `Recent Progress` and `Current Focus`. Preserve verified historical entries in `docs/PROGRESS.md` under `Untracked Work (Needs Linking)` or a linked history archive (e.g. `docs/project-history.md`); do not convert historic work to invented tickets. Preserve meaningful focus decisions elsewhere if still relevant. Replace only obsolete *skill-owned* sections, not unrelated user-written content.
- If `docs/agents/issue-tracker.md` does not exist, do **not** silently select a tracker or auto-run user-invoked setup; tell user to run `/setup-matt-pocock-skills`. Leave dashboard explicitly `Not yet synced`, with no fabricated IDs.

## README content contract

### `## Project Goal`
A single declarative sentence. Until confirmed: `Needs clarification — run /grill-me`.

### `## Project Stages`

`| Stage | Status | Exit Criteria | Evidence / Notes |`

- Initial stages: `POC`, `MVP`, `Production Ready`; more may be appended indefinitely.
- Allowed statuses: `Not Started`, `In Progress`, `Blocked`, `Achieved`.
- Exit criteria must be observable; evidence must be genuine (test results, release checks, user acceptance). No inferred Production Ready.

### `## Possible Features`

`| Feature | Description | Importance | Urgency | Status |`

- Importance = lasting value; urgency = timing. Each: `High`, `Medium`, `Low`, `TBD`.
- Feature status: `Proposed`, `Planned`, `In Progress`, `Done`, `Deferred`, `Rejected`.
- New concrete discussion -> one row `Proposed` (unless user already approved it). No implied authorization to build or ticket it. Merge duplicates instead of creating similar rows.
- Feature `Done` needs verification, and linked ticket work Done when applicable. A single completed ticket does not mean a whole feature is Done.
- Avoid stuffing ticket-level details into this table.

### `## Progress`
Only a relative link to `docs/PROGRESS.md`. Do not include a second table of ticket status in README. **No mandatory `Recent Progress` / `Current Focus` sections.**

## `docs/PROGRESS.md` content contract

- Heading `# Progress`.
- Tracker/config reference and a truthful sync state (`Synced` or `Not yet synced` / `Needs reconciliation`), with optional last-verified date only if known.
- Ticket table: `| Ticket | Description | Stage | Status |`.
- Ticket cell **links to the canonical issue** (or exact local file), and uses a unique identifier. Descriptions are short. Stage is the related project stage or `TBD` when unknown; never invent mappings.
- Normalized dashboard statuses: `Backlog`, `Todo`, `In Progress`, `Blocked`, `Done`, `Cancelled`, `Unknown`. Map only from observed tracker state. No guessed Done.
- **Include all existing tickets** (open, blocked, completed and cancelled); don't silently prune finished entries. For large workspaces, group tables by feature or stage while preserving all tickets and the columns.
- If there is verified untracked work, optionally add a separate `## Untracked Work (Needs Linking)` table; label it `Untracked` rather than fake IDs.
- This file is a **mirror/index**. The tracker owns ticket descriptions, detailed specifications, blockers, acceptance criteria, status, and closure evidence. When records disagree, tracker wins; repair the dashboard.

## Update triggers and order

| What happened | Canonical change | Mirror / overview change |
|---|---|---|
| Concrete new feature discussed | No ticket (discussion ≠ approval) | Add/update README feature as Proposed; importance/urgency TBD unless stated |
| Feature approved/reprioritized/rejected | Record approved decision in existing project conventions | Update README feature status/description/priorities |
| `/to-tickets` breakdown is discussed but not approved | No ticket publication yet | Do not fabricate published tickets; README may reflect agreed feature scope |
| Tickets **published** after user approval | `/to-tickets` publishes to configured tracker | Add/update actual linked ticket rows in PROGRESS, from observed data |
| Ticket started/blocked/resumed | Update issue status/notes in canonical tracker | Mirror ticket row status in PROGRESS; adjust feature if applicable |
| Ticket completion verified | Confirm criteria/tests and update tracker to Done using its conventions | Mirror Done, review README feature/stage; only mark feature Done if entire scope complete |
| Stage criteria met | Preserve verification artifacts | Update stage status and evidence in README |
| No tracker access / conflicting facts | Do not silently modify source of truth | Show Needs reconciliation / Unknown and explain blocker |

After a terminal outcome, report exactly which repo files or issue states changed. Never auto-invoke `/to-tickets`, publish tickets, close unrelated issues, commit, push, deploy, or claim background syncing solely because this skill is installed.

## Safe edit / multi-agent protocol

1. Inspect latest file and tracker state immediately before writing, even if read earlier.
2. Edit minimally, preserving established headings/links, meaningful history and unrelated agent changes. Stable ticket IDs prevent duplicate rows.
3. Reconcile concurrent changes and review diff. If genuine conflict or unavailable tracker, stop the disputed update; label mirror stale instead of overriding someone else's work.
4. Verify links (README -> `docs/PROGRESS.md`; Progress -> actual local ticket files or known issue URLs), headings/tables, stage order, status mapping and honest evidence.
5. Optionally run `python3 .agents/skills/project-readme-keeper/scripts/validate_project_memory.py` from repo root. It checks shape/relative paths, not remote truth.
6. Report concise sync results: `README synced: ...; PROGRESS synced: ...` or `Not synced: ...`.

## Examples

- User: “What about an export-to-CSV feature?” -> add a README `Proposed` row; **no ticket**.
- User: “Let's implement CSV export; run /to-tickets.” -> use upstream quiz/approval; **after** publication mirror actual IDs in PROGRESS.
- Agent implements ticket `<id>` and tests pass -> update/close canonical issue per configured tracker, then set its dashboard status `Done`, then review README feature/stage evidence.
- User: “How many tickets are blocked?” -> read canonical tracker and summarize; fix dashboard only if write access exists and its state is stale.
