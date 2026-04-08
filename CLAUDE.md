# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

This is an **Obsidian vault** — a task/project management workspace for NexWave / ClinicPro. It holds planning, sprints, tasks, and strategy notes. It does **not** contain application code.

- The vault holds **what to do**; product repos hold **how it is built**
- `context/repos.md` — authoritative route/folder map for all repos
- `context/llm-workspace-guide.md` — full rules; read before editing anything when given Obsidian context
- `context/design-system.md` — **read before any frontend work** — colours, typography, animation, voice/tone for all ClinicPro products

## Product repos (where code lives)

| `repo` field | Path on this machine | Purpose |
|---|---|---|
| `clinicpro-saas` | `C:\Users\reonz\Cursor\clinicpro-saas` | Main web app — Next.js, Clerk, Drizzle/Neon, Vercel |
| `clinicpro-medtech` | `C:\Users\reonz\Cursor\clinicpro-medtech` | ClinicPro Capture PWA + Medtech BFF — Next.js, Supabase OTP, AWS Lightsail |
| `nexwave-rd` | `C:\Users\reonz\Cursor\nexwave-rd` | MBIE R&D — isolated from commercial code, AWS Bedrock |
| `gp-fellowship` | N/A (no code repo) | Personal training — RNZCGP Fellowship application and assessment |

**Choosing a repo — in priority order:**
1. Task frontmatter `repo:` field — authoritative
2. Task ID prefix: `saas-*` → clinicpro-saas; `medtech-*` → clinicpro-medtech; `rd-*` → nexwave-rd; `gpf-*` → gp-fellowship
3. Project file (`projects/*.md`) `repo:` field
4. If still ambiguous — ask the user before writing code

## Vault structure

```
obsidian/
├── AGENTS.md              # Frontmatter schema + vault rules (read this)
├── context/               # Reference docs — repos.md, stack.md, llm-workspace-guide.md
├── tasks/open/            # Active tasks (one file per task, frontmatter-driven)
├── tasks/done/            # Completed tasks
├── projects/              # Project metadata files
├── sprints/active/        # Current sprint files
├── sprints/archive/       # Completed sprints (never deleted)
├── dashboards/            # Dataview-powered dashboards (auto-generated views)
├── templates/             # Obsidian Templater templates
└── inbox/                 # Quick capture / brain dump
```

## Frontmatter schemas

**Task** (`tasks/open/*.md`):
```yaml
id: {repo-prefix}-{YYYYMMDD}-{NNN}   # e.g. saas-20260330-001
title: Short human-readable description  # dashboards display title, not filename
project: {project-id}                  # must match a filename in projects/ (no .md)
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship
sprint: {sprint-id}                    # must match a filename in sprints/ (no .md)
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

R&D tasks add: `objective: obj-1|obj-2|obj-3|obj-4|capability` and `owner: ryo|ting|both`

**Project** (`projects/*.md`): `id`, `status`, `type: product|rd|training`, `repo`, `stack`

**Sprint** (`sprints/active/*.md`): `id`, `status`, `start`, `end`, `repos`, `projects`, `goal`

Sprint IDs follow `YYYY-MM-sprint-N` for cross-repo sprints, or `YYYY-MM-{repo-tag}-sprint-N` for single-repo sprints (e.g. `2026-04-rd-sprint-1`, `2026-04-gpf-sprint-1`).

## Rules

- **No code in the vault.** If a task has `repo: clinicpro-saas`, implementation goes in `C:\Users\reonz\Cursor\clinicpro-saas`, not here.
- **No inline checkbox tasks** (`- [ ]`) anywhere in vault files. Tasks must be rows in `tasks/open/`.
- **No task lists inside project files.** Use Dataview embeds only.
- Check existing files in `tasks/open/` before creating a new task to avoid ID collisions.
- Sprint files move to `sprints/archive/` on completion — never deleted.
- Never create or edit anything inside `.obsidian/`.
- **R&D isolation:** `nexwave-rd` work must not import ClinicPro commercial code unless the user explicitly allows it.
- Due dates: ISO 8601, no quotes — e.g. `due: 2026-04-06`
- `title` must be short and human-readable — dashboards use `title`, not the filename.

## Available vault skills

These Claude Code skills are configured for vault work (invoke with `/skill-name`):

| Skill | Purpose |
|-------|---------|
| `/obsidian` | Orient for project management work — loads vault structure and key rules |
| `/obsidian-task-table` | Generate correctly-structured task tables for sprint/dashboard files |
| `/obsidian-markdown` | Create/edit Obsidian Flavored Markdown (wikilinks, callouts, properties) |
| `/obsidian-cli` | Interact with the vault via Obsidian CLI |
| `/obsidian-bases` | Create/edit Obsidian Bases (`.base` files) |
| `/calendar-sync` | Sync active sprint timelines to Google Calendar |
| `/session-update` | End-of-session update — progress log, new tasks, project step status |
| `/json-canvas` | Create/edit `.canvas` files |
