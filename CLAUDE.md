# CLAUDE.md

Obsidian vault for NexWave / ClinicPro project management. Planning, tasks, projects, and daily notes live here. No application code.

Full structure reference: `vault-map.md` (area layout, file placement rules, Dataview patterns, frontmatter schemas).

## Plugins the vault depends on

If any of these are disabled, dashboards and task tables break silently. Never replace their output with plain markdown.

- **Dataview** drives every task table and area index query.
- **Meta-bind** drives the interactive filter selects in `areas/{area}/index.md`. The `dataviewjs` blocks call `app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api`. Preserve that pattern. Never convert to plain Dataview TABLE.
- **Templater** drives the `/complete-task` macro. It moves a task file from `areas/{area}/tasks/open/` to `areas/{area}/tasks/done/` and updates frontmatter. Editing `status: done` manually leaves the file in the wrong folder.
- **Obsidian-git** auto-commits changes. Every edit becomes a commit.

## Vault layout

```
areas/             9 work stream areas (nexwave-rd, clinicpro-saas, clinicpro-medtech,
                   gp-os, founder-os, linkedin, miozuki, other-projects, personal)
  {area}/
    index.md       area dashboard — Dataview-powered
    CLAUDE.md      area-specific context (auto-loaded by Claude Code)
    tasks/open/    active task files
    tasks/done/    completed task files
    inbox/         AI drafts pending review; quick capture
    context/       supporting docs: proposals, research, briefings
    projects/      ONE metadata file per project
    logs/          session logs — YYYY-WNN.md
    weekly/        per-area weekly planning
home.md            Dataview project overview (do not edit manually)
weekly.md          master briefing index (read by /daily)
daily/             one note per day (YYYY-MM-DD.md)
templates/         Templater templates, including complete-task
reference/         non-area reference docs: tools, people, Claude Code docs
archives/          historical files
system/            meta-documentation: decisions-log.md, etc.
.obsidian/         Obsidian config, never edit
```

## Workflow rituals

- **Daily note.** `daily/YYYY-MM-DD.md` holds Focus, Projects, Today's Plan. Read today's note at the start of any vault session.
- **Area indexes are Dataview-powered.** The project list and task counts in `areas/{area}/index.md` are auto-generated. Do not edit them manually.
- **Task completion.** Use the `/complete-task` Templater macro. Do not manually move files or edit `status: done` alone.
- **Email trashing.** Before trashing emails, emit a single-line confirmation listing message IDs and senders, then wait for explicit yes.

## Information hierarchy

**Area index** (`areas/{area}/index.md`)
- Represents one independent work stream
- Shows project list with phase and task counts (Dataview-generated)

**Project** (`areas/{area}/projects/{id}.md`)
- Belongs to exactly one area (via `dashboard:` field)
- ONE metadata file per project — no task lists, no prose beyond frontmatter
- Supporting docs go in `areas/{area}/context/`, not here

**Task** (`areas/{area}/tasks/open/{id}.md`)
- Always has `project:` set (no exceptions)
- `milestone:` is optional: a human-readable grouping label
- Never attached directly to an area index

## Task prefix routing

| Prefix | Area |
|---|---|
| `rd-*` | nexwave-rd |
| `saas-*` | clinicpro-saas |
| `medtech-*` | clinicpro-medtech |
| `gpf-*` | gp-os |
| `fo-*` | founder-os |
| `linkedin-*` | linkedin |
| `miozuki-*` | miozuki |
| `heron-*` | other-projects |
| `personal-*`, `wedding-*` | personal |

## Frontmatter schemas

**Task** (`areas/{area}/tasks/open/*.md`):
```yaml
id: {prefix}-{YYYYMMDD}-{NNN}
title: Short human-readable description
project: {project-id}        # must match filename in areas/{area}/projects/ (no .md)
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | ...
milestone: "text label"      # optional grouping label
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

R&D tasks add: `objective: obj-1|obj-2|obj-3|obj-4|capability` and `owner: ryo|ting|both`.

**Project** (`areas/{area}/projects/*.md`):
```yaml
id: {project-id}
title: "Human-readable name"
status: active | parked | production
type: product | rd | training | side-project | partnership
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | ...   # omit if no repo
stack: [...]
description: "One-line description."
phase: "Current focus — one line"
dashboard: nexwave-rd | clinicpro-saas | clinicpro-medtech | gp-os | founder-os | linkedin | miozuki | other-projects | personal
```

## Advanced Obsidian syntax

For callouts, embeds, block references, mermaid, footnotes, or any Obsidian syntax beyond frontmatter and basic wikilinks: invoke the `/obsidian-markdown` skill before writing.

## Vault rules

- **Project scope check.** One project file = one coherent thing. If a project starts covering multiple workstreams, suggest splitting. Flag proactively.
- **No code in the vault.** Implementation lives in the task's `repo:`.
- **No inline checkbox tasks** (`- [ ]`). Workflow state lives in frontmatter.
- **No task lists inside project files.** Use Dataview embeds only.
- **R&D research output lives in `../nexwave-rd/docs/`.** Vault holds task files only.
- **Never edit anything inside `.obsidian/`.**
- **`home.md` is Dataview-powered.** Update project frontmatter fields, not home.md directly.
- **`reference/portfolio-map.canvas` is the visual portfolio map.** Update when projects are added or archived.
- **All AI-generated output goes to `areas/{area}/inbox/` first.** Move to final location only after Ryo approves.

## Gotchas

- **Colons in frontmatter:** quote any value containing `: ` (e.g. `title: "Review: Q2 plan"`). Dataview silently drops unquoted values with colons.
- **Project references:** `project:` in a task must match an actual filename in `areas/{area}/projects/` without `.md`. Typos produce no error; the task silently disappears from Dataview.
- **Milestone values:** free-text, must exactly match the label used in the project's grouping.
- **Due dates:** ISO 8601, unquoted. e.g. `due: 2026-04-06`.

## Writing style

No em dashes in code, comments, markdown, commits, or generated output. Use commas, colons, or restructure.

## Change discipline

Every changed line must trace directly to the user's request.

- Do not tidy adjacent frontmatter, Dataview queries, or task tables you were not asked to touch. Small edits silently break dashboards.
- Do not rewrite task descriptions, milestone labels, or project notes the user wrote. Those are the user's words.
- Match existing patterns. Do not introduce a new Dataview or dataviewjs form into one file.
- If you notice a broken query or stale status, mention it. Do not fix it without being asked.
