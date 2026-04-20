# CLAUDE.md

Obsidian vault for NexWave / ClinicPro project management. Planning, tasks, sprints, dashboards, and daily notes live here. No application code.

## Plugins the vault depends on

If any of these are disabled, dashboards and task tables break silently. Never replace their output with plain markdown.

- **Dataview** drives every task table, sprint table, and dashboard query.
- **Meta-bind** drives the interactive filter selects in `dashboards/*.md`. The `dataviewjs` blocks call `app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api`. Preserve that pattern. Never convert to plain Dataview TABLE.
- **Templater** drives the `/complete-task` macro. It moves a task file from `tasks/open/` to `tasks/done/` and updates frontmatter. Editing `status: done` manually leaves the file in the wrong folder.
- **Obsidian-git** auto-commits changes. Every edit becomes a commit.

## Vault layout

```
tasks/open/       active tasks (one file per task)
tasks/done/       completed tasks
projects/         project metadata (one file per project)
sprints/active/   current sprints
sprints/archive/  completed sprints, never deleted
dashboards/       manual progress logs with Dataview tables
daily/            one note per day (YYYY-MM-DD.md)
templates/        Templater templates, including complete-task
context/          reference docs (repos.md, llm-workspace-guide.md)
inbox/            quick capture
.obsidian/        Obsidian config, never edit
```

## Workflow rituals

- **Daily note.** `daily/YYYY-MM-DD.md` holds Focus, From Yesterday, Active Sprints, Today's Plan, Today's Focus. Read today's note at the start of any vault session.
- **Dashboards are manual.** The weekly progress log in each dashboard is written by hand after work ships. Do not auto-generate.
- **Task completion.** Use the `/complete-task` Templater macro. Do not manually move files or edit `status: done` alone.
- **Sprint IDs.** `YYYY-MM-sprint-N` for cross-repo sprints. `YYYY-MM-{repo-tag}-sprint-N` for single-repo (e.g. `2026-04-rd-sprint-1`, `2026-04-gpf-sprint-1`). Mismatched IDs break Dataview filters silently.

## Information hierarchy rules

**Dashboard** (`dashboards/*.md`)
- Represents an independent area of work
- Must wikilink to every project in the area
- Must wikilink to every area-level sprint (sprints not tied to a specific project)

**Project** (`projects/*.md`)
- Belongs to exactly one dashboard
- Must wikilink to every sprint associated with it

**Sprint** (`sprints/active/*.md` or `sprints/archive/*.md`)
- Belongs to either a dashboard (area-level) or a project (scoped), never both, never neither

**Task** (`tasks/open/*.md`)
- Links to either a `project:` OR a `sprint:`, never both
- Area-level sprint tasks (no project) are valid
- Never attached directly to a dashboard

## Choosing the repo for a task

Priority order:
1. Task frontmatter `repo:` field (authoritative)
2. Task ID prefix: `saas-*` → `clinicpro-saas`; `medtech-*` → `clinicpro-medtech`; `rd-*` → `nexwave-rd`; `gpf-*` → `gp-fellowship`
3. Project file (`projects/*.md`) `repo:` field
4. If still ambiguous, ask

## Frontmatter schemas

**Task** (`tasks/open/*.md`):
```yaml
id: {repo-prefix}-{YYYYMMDD}-{NNN}
title: Short human-readable description
project: {project-id}                    # must match filename in projects/ (no .md) — set OR sprint, never both
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship
sprint: {sprint-id}                      # must match filename in sprints/ (no .md) — set OR project, never both
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

R&D tasks add: `objective: obj-1|obj-2|obj-3|obj-4|capability` and `owner: ryo|ting|both`.

**Project** (`projects/*.md`):
```yaml
id: {project-id}
title: "Human-readable name"
status: active | parked | production
type: product | rd | training | side-project | partnership
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship | miozuki-web   # omit if no repo
stack: [...]
description: "One-line description for home.md display."
dashboard: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship | side-projects | partnerships
```

**Sprint** (`sprints/active/*.md`):
```yaml
id: {sprint-id}
status: active
start: YYYY-MM-DD
end: YYYY-MM-DD
repos: [repo-name, ...]
projects: [project-id, ...]
goal: "One-line sprint goal"
dashboard: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship | side-projects | partnerships
```

## Advanced Obsidian syntax

For callouts, embeds, block references, mermaid, footnotes, or any Obsidian syntax beyond frontmatter and basic wikilinks: invoke the `/obsidian-markdown` skill before writing. The skill has the full syntax reference.

## Vault rules

- **No code in the vault.** Implementation lives in the task's `repo:`, not here.
- **No inline checkbox tasks** (`- [ ]`). Workflow state lives in frontmatter. Body is notes only.
- **No task lists inside project files.** Use Dataview embeds only.
- **R&D research output lives in `../nexwave-rd/docs/`.** The vault holds task files and sprint plans for R&D; research reports, specs, and architecture decisions go in the product repo under `docs/obj-N/research/` or `docs/obj-N/output/`.
- **Sprint files are append-only.** Move to `sprints/archive/` on completion. Never delete.
- **Never edit anything inside `.obsidian/`.**
- **`dashboards/home.md` is Dataview-powered.** Project lists, sprint lists, and active counts are generated from frontmatter. Do not manually add or edit project or sprint entries in home.md. To update what appears there, update the relevant project or sprint frontmatter fields (`title`, `description`, `status`, `dashboard`).
- **`dashboards/portfolio-map.canvas` is the visual portfolio map.** Update it when projects are added or archived.

## Gotchas

- **Colons in frontmatter:** quote any value containing `: ` (e.g. `title: "Review: Q2 plan"`). Dataview silently drops unquoted values with colons.
- **Sprint and project references:** `sprint:` and `project:` fields in a task must match actual filenames without `.md`. Typos produce no error; the task just fails to appear in the Dataview query.
- **Due dates:** ISO 8601, unquoted. e.g. `due: 2026-04-06`.

## Writing style

No em dashes in code, comments, markdown, commits, or generated output. Use commas, colons, or restructure.

## Change discipline

Every changed line must trace directly to the user's request.

- Do not tidy adjacent frontmatter, Dataview queries, or task tables you were not asked to touch. Small edits silently break dashboards.
- Do not rewrite task descriptions, sprint goals, or project notes the user wrote. Those are the user's words.
- Match existing patterns. Do not introduce a new Dataview or dataviewjs form into one file.
- If you notice a broken query or stale status, mention it. Do not fix it without being asked.
- For non-trivial edits (new dashboard, sprint restructure, bulk task updates), state a brief plan before editing.
