---
name: vault-audit
description: Structural audit of the Obsidian vault — counts tasks, sprints, and projects per dashboard area, flags schema violations, identifies orphaned files and broken references. Use when planning a vault restructure, diagnosing why a Dataview query is missing items, or auditing vault health before a sprint or weekly review. Trigger on "audit the vault", "check vault structure", "what tasks are where", "why isn't this showing in Dataview".
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# /vault-audit — Obsidian Vault Structural Audit

Reads all task, sprint, and project files and produces a violation summary and health report.

---

## Step 1: Collect all files

Read in parallel:
- Glob `tasks/open/*.md` — all open tasks
- Glob `tasks/done/*.md` — all done tasks (count only, do not read)
- Glob `projects/*.md` — all projects
- Glob `sprints/active/*.md` — active sprints
- Glob `sprints/archive/*.md` — archived sprints (count only)
- Glob `dashboards/*.md` — all dashboards

---

## Step 2: Parse frontmatter

For each open task, extract: `id`, `title`, `project`, `repo`, `status`, `priority`, `due`, `milestone`.
For each project, extract: `id`, `title`, `status`, `dashboard`, `repo`.

---

## Step 3: Run violation checks

Check each open task for:
- [ ] Missing `project:` field — task is orphaned
- [ ] `project:` value not matching any file in `projects/` (typo or stale ref)
- [ ] Missing `status:` field
- [ ] `status: done` but file still in `tasks/open/` — should be in `tasks/done/`
- [ ] `due:` field quoted (should be unquoted ISO 8601)
- [ ] `milestone:` contains a colon without quoting

Check each project for:
- [ ] Missing `dashboard:` field
- [ ] `status: active` with zero open tasks (possibly stale)
- [ ] `dashboard:` value not in the known set (clinicpro-saas, clinicpro-medtech, nexwave-rd, gp-fellowship, side-projects, partnerships)

---

## Step 4: Produce report

```
## Vault Audit — YYYY-MM-DD

### Counts
| Area | Open tasks | Projects | Active sprints |
|------|-----------|----------|----------------|

### Violations
| File | Issue | Severity |
|------|-------|----------|

### Summary
- Total open tasks: N
- Orphaned tasks (no valid project): N
- Stale active projects (no tasks): N
- Schema violations: N
```

---

## Step 5: Propose fixes

For each violation, propose a one-line fix (do not apply without user approval):
- Orphaned task: "Set project: to X based on ID prefix"
- Done task in open: "Move to tasks/done/"
- Stale project: "Set status: parked"

Ask: "Apply all fixes? (yes / selective / no)"
