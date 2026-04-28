# Vault Map

Obsidian vault for NexWave / ClinicPro project management. Area-based structure as of 2026-04-28.

---

## Root layout

```
areas/             9 work stream areas (see below)
daily/             daily notes — YYYY-MM-DD.md
templates/         Templater templates
weekly.md          master briefing index (read by /daily)
home.md            Dataview project overview (do not edit manually)
reference/         non-area reference docs: tools, people, Claude Code docs
archives/          historical files (formerly zArchives/)
system/            meta-documentation: decisions-log.md, file-structure.md, etc.
CLAUDE.md          vault-wide rules and plugin info
vault-config.json  machine-readable vault config
```

---

## Area structure

Each of 9 areas follows this pattern:

```
areas/{area}/
  index.md           area dashboard — Dataview-powered, do not edit project list manually
  CLAUDE.md          area-specific context for Claude Code (auto-loaded when cwd is here)
  tasks/open/        active task files (one per task, prefix-routed)
  tasks/done/        completed task files
  inbox/             AI-generated drafts pending review; quick capture
  context/           supporting docs: proposals, research, briefings, design systems
  projects/          ONE metadata file per project (id, status, type, repo, stack)
  logs/              session logs — YYYY-WNN.md per project
  weekly/            per-area weekly planning file
```

**9 areas:** nexwave-rd, clinicpro-saas, clinicpro-medtech, gp-os, founder-os, linkedin, miozuki, other-projects, personal

---

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

---

## File placement rules

1. **New task** → `areas/{area}/tasks/open/{prefix}-YYYYMMDD-NNN.md`
2. **Project metadata** → `areas/{area}/projects/{project-id}.md` — ONE file per project, required frontmatter only
3. **Supporting doc** (proposal, research, briefing) → `ls areas/{area}/context/` first, find or name a subfolder
4. **AI-generated draft** (pending review) → `areas/{area}/inbox/`
5. **General reference** (tools, people, Claude Code docs) → `reference/`
6. **Unsure** → `areas/{area}/inbox/` and flag for Ryo to route

Never put supporting docs in `areas/{area}/projects/`. Never put project metadata in `context/`.

---

## Dataview patterns

Area task table:
```
FROM "areas/{area}/tasks/open"
WHERE status != "done"
```

Area project list:
```
FROM "areas/{area}/projects"
WHERE dashboard == "{area}"
```

Global project overview (home.md only):
```javascript
dv.pages('"areas"')
  .where(p => p.dashboard && p.status != "parked")
```

---

## Frontmatter schemas

**Task:**
```yaml
id: {prefix}-YYYYMMDD-NNN
title: Short description
project: {project-id}       # must match filename in areas/{area}/projects/ (no .md)
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | ...
milestone: "text label"     # optional, free-text
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

**Project:**
```yaml
id: {project-id}
title: "Human-readable name"
status: active | parked | production
type: product | rd | training | side-project | partnership
repo: ...                   # omit if no repo
stack: [...]
description: "One-line description."
phase: "Current focus"
dashboard: {area}           # controls which area's index.md shows this project
```

---

## Key rules

- **No inline checkbox tasks** (`- [ ]`) — state lives in frontmatter
- **No task lists in project files** — use Dataview embeds
- **Colons in frontmatter** — quote values containing `: `
- **home.md is Dataview-powered** — never manually edit project entries
- **R&D research output** → `../nexwave-rd/docs/` (not vault)
- **All AI output goes to inbox/ first** — move to final location only after Ryo approves
