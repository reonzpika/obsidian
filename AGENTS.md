# Obsidian Vault — Schema and Rules

## For AI assistants (read first)

### What this vault is

This is an **Obsidian vault**: task and project management for NexWave / ClinicPro (planning, sprints, tasks, strategy). It does **not** contain application code.

- The vault holds **what to do**; product repos hold **how it is built**
- Implementation work belongs in **product git repos**, not here. Task files only **point** to a repo via the `repo` field
- **Full rules:** [[context/llm-workspace-guide.md]]
- **Route / folder map (detailed):** [[context/repos.md]]

### Product repos (where code lives)

Quick reference; feature-level detail is in [[context/repos.md]].

| `repo` field | Path on this machine | Purpose |
|---|---|---|
| `clinicpro-saas` | `C:\Users\reonz\Cursor\clinicpro-saas` | Main web app — Next.js, Clerk, Drizzle/Neon, Vercel |
| `clinicpro-medtech` | `C:\Users\reonz\Cursor\clinicpro-medtech` | ClinicPro Capture PWA + Medtech BFF — Next.js, Supabase OTP, AWS Lightsail |
| `nexwave-rd` | `C:\Users\reonz\Cursor\nexwave-rd` | MBIE R&D — isolated from commercial code, AWS Bedrock |

**Choosing a repo:** use the `repo:` frontmatter field in the task file, or infer from the task ID prefix (`saas-*`, `medtech-*`, `rd-*`). If the user shares Obsidian context without naming a repo, infer `repo` from the task file or ask before editing code.

### Vault structure

```
obsidian/
├── AGENTS.md              # This file — schema + rules (read first)
├── context/               # Reference docs — repos.md, stack.md, llm-workspace-guide.md
├── tasks/open/            # Active tasks (one file per task, frontmatter-driven)
├── tasks/done/            # Completed tasks
├── projects/              # Project metadata files
├── sprints/active/        # Current sprint files
├── sprints/archive/       # Completed sprints (never deleted)
├── dashboards/            # Dataview-powered dashboards
├── templates/             # Obsidian Templater templates
└── inbox/                 # Quick capture / brain dump
```

## Vault root
Cursor/obsidian/

## Frontmatter schema

### Task files (tasks/open/ and tasks/done/)
---
id: {repo-prefix}-{YYYYMMDD}-{NNN}
title: One-line description shown on dashboards (required)
project: {project-id}
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd
sprint: {sprint-id}
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
---

### R&D task files — additional fields
objective: obj-1 | obj-2 | obj-3 | obj-4 | capability
owner: ryo | ting | both

### Project files (projects/)
---
id: {project-id}
status: active | paused | complete
type: product | rd
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd
stack: [list]
---

### Sprint files (sprints/active/ and sprints/archive/)
---
id: YYYY-MM-sprint-N
status: active | planning | complete
start: YYYY-MM-DD
end: YYYY-MM-DD
repos: [list]
projects: [list]
goal: one-line goal
---

## Rules

- **title** must be a short, human-readable line (same idea as the first line of body text). Dashboards use `title`, not the filename, so you can scan work at a glance.
- Due date format: ISO 8601, no quotes. Example: due: 2026-04-06
- project field must match a filename in projects/ without .md
- sprint field must match a filename in sprints/active/ or sprints/archive/ without .md
- repo must be one of the three allowed values exactly
- **No code in the vault.** If a task has `repo: clinicpro-saas`, implementation goes in `C:\Users\reonz\Cursor\clinicpro-saas`, not here.
- No task lists inside project files. Use Dataview embeds only.
- No inline checkbox tasks (`- [ ]`) anywhere in the vault. Tasks must be rows in `tasks/open/`.
- Always list existing files in `tasks/open/` before creating a new task to avoid ID collision.
- Sprint files are never deleted. Move to `sprints/archive/` on completion.
- Never create or edit anything inside `.obsidian/`.
- **R&D isolation:** `nexwave-rd` work must not import ClinicPro commercial code unless the user explicitly allows it.
