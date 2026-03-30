# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

This is an **Obsidian vault** — a task/project management workspace for NexWave / ClinicPro. It holds planning, sprints, tasks, and strategy notes. It does **not** contain application code.

- Implementation code lives in the three product repos (see below)
- The vault holds **what to do**; product repos hold **how it is built**
- Full rules: `context/llm-workspace-guide.md` — read before editing anything when given Obsidian context

## Product repos (where code lives)

| `repo` field | Path on this machine | Purpose |
|---|---|---|
| `clinicpro-saas` | `C:\Users\reonz\Cursor\clinicpro-saas` | Main web app — Next.js, Clerk, Drizzle/Neon, Vercel |
| `clinicpro-medtech` | `C:\Users\reonz\Cursor\clinicpro-medtech` | ClinicPro Capture PWA + Medtech BFF — Next.js, Supabase OTP, AWS Lightsail |
| `nexwave-rd` | `C:\Users\reonz\Cursor\nexwave-rd` | MBIE R&D — isolated from commercial code, AWS Bedrock |

**Choosing a repo:** use the `repo:` frontmatter field in a task file, or infer from the task ID prefix (`saas-*`, `medtech-*`, `rd-*`). Ask the user if ambiguous.

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
title: Short human-readable description
project: {project-id}                  # must match a filename in projects/ (no .md)
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd
sprint: {sprint-id}                    # must match a filename in sprints/ (no .md)
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

R&D tasks add: `objective: obj-1|obj-2|obj-3|obj-4|capability` and `owner: ryo|ting|both`

**Project** (`projects/*.md`): `id`, `status`, `type: product|rd`, `repo`, `stack`

**Sprint** (`sprints/active/*.md`): `id: YYYY-MM-sprint-N`, `status`, `start`, `end`, `repos`, `projects`, `goal`

## Rules

- **No code in the vault.** If a task has `repo: clinicpro-saas`, implementation goes in `C:\Users\reonz\Cursor\clinicpro-saas`, not here.
- **No inline checkbox tasks** (`- [ ]`) anywhere in vault files. Tasks must be rows in `tasks/open/`.
- **No task lists inside project files.** Use Dataview embeds only.
- Check existing files in `tasks/open/` before creating a new task to avoid ID collisions.
- Sprint files move to `sprints/archive/` on completion — never deleted.
- Never create or edit anything inside `.obsidian/`.
- **R&D isolation:** `nexwave-rd` work must not import ClinicPro commercial code unless the user explicitly allows it.
- Due dates: ISO 8601, no quotes — e.g. `due: 2026-04-06`
