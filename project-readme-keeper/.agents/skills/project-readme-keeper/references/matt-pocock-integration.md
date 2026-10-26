# Matt Pocock Skills integration — tracker is authoritative

Verified against the upstream docs:
- https://github.com/mattpocock/skills/blob/main/docs/engineering/setup-matt-pocock-skills.md
- https://github.com/mattpocock/skills/blob/main/docs/engineering/to-tickets.md

## Recommended order per repo

1. Run `/setup-matt-pocock-skills` to choose the repo's issue tracker. It records the policy in `docs/agents/issue-tracker.md` (plus other relevant `docs/agents/` files).
2. Run `project-readme-keeper` to merge README sections and initialize `docs/PROGRESS.md`.
3. Discuss features freely. A concrete proposal goes into the README. This is not yet a ticket.
4. When user wants execution planning, invoke `/to-tickets` explicitly (the skill is user-invoked), review its proposed slices/blocking edges and **approve publication**.
5. After confirmed publication in the configured tracker, mirror all created ticket IDs/links and statuses in `docs/PROGRESS.md`.
6. When starting work or closing it with `/implement` or another implementation workflow, reconcile the canonical tracker status **first**, then the progress index; additionally adjust README feature status and stage evidence if applicable.

## Tracker layouts

- **Local Markdown:** one file per ticket, generally `.scratch/<feature-slug>/issues/<NN>-<slug>.md`; the `<NN>` is local to its feature folder. A bare `03` may be ambiguous across multiple features: display ticket as `[feature/03](../.scratch/feature/issues/03-name.md)` (or another unique clear label). Verify that actual files/paths exist; don't hardcode feature names or assume `.scratch` is committed.
- **GitHub / GitLab:** issue's URL and ID, e.g. `[#123](https://...)`. The configured tracker decides statuses, relations and closure method. Never claim native blocker links where the tracker doesn't have them.
- **Other (e.g. Linear / Jira):** use exact ticket ID+URL and status from that tracker via the configured integration; no guessed URLs.
- **Unconfigured:** no ticket IDs, no invented table rows. Show `Not yet synced` and state that `/setup-matt-pocock-skills` is required.

## Common pitfalls

- `/to-tickets` only publishes planning artifacts; **it doesn't implement the tickets**. Do not mark them Done after ticket creation.
- Different trackers use different native statuses. Map to the dashboard's normalized `Backlog`, `Todo`, `In Progress`, `Blocked`, `Done`, `Cancelled`, or `Unknown` conservatively. Keep the exact source in the tracker, not in the dashboard.
- Do not infer a status from code being present or a PR existing. If tracker cannot be read/updated, mark `Unknown` in the mirror with a Sync status warning; never contradict tracker silently.
- For new local issue files, update progress in the same change when possible. For remote tracker workflows, update the dashboard as part of closeout even when no repository files changed otherwise.
- Upstream issue-tracker instructions may change between Matt Pocock Skills releases; prefer the **repo's current** `docs/agents/issue-tracker.md` over this guide.
