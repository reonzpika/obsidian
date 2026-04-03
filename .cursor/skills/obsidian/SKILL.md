---
name: obsidian
description: Orient agent for project management work in the Obsidian vault — no code repo involved. Loads vault structure and key rules.
user-invocable: true
argument-hint: (none required)
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

# /obsidian — Agent Orientation: Obsidian Vault (Project Management)

This session is for project management work in the Obsidian vault. There is no code repo involved.

**Vault root:** `C:/Users/reonz/Cursor/obsidian/`

## Vault structure

| Folder | Purpose |
|--------|---------|
| `projects/` | One page per product/initiative — description, goals, key decisions |
| `tasks/` | Task files (open, in-progress, done) — source of truth for all action items |
| `dashboards/` | Rollup views |
| `context/` | Standing reference material |
| `sprints/` | Sprint planning and tracking |
| `templates/` | Page templates |

## Key rules to follow

- **No inline checklists as tasks.** Never use `- [ ]` items on pages to represent action items. All tasks are rows in the Tasks database files under `tasks/`.
- When adding tasks, use the `/obsidian-task-table` skill to generate correctly-structured task tables.
- Reference pages contain standing knowledge only — not task lists.

## Orientation step

Read `C:/Users/reonz/Cursor/obsidian/projects/` directory listing to know which projects are active, then confirm:
> "Oriented on Obsidian vault. Ready for project management tasks."

Then wait for the user's first task.
