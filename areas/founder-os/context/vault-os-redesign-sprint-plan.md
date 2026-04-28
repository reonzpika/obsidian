# Sprint Plan: Vault OS Redesign
**Date:** 2026-04-28 | Tasks: fo-20260427-001 to fo-20260427-005

## Dependency map

```
Task 1 (folder structure) ──► Task 3 steps 4-6 (area CLAUDE.md, vault-map.md)
Task 2 (memory reorg) ───────► Task 5 (hooks point to memory files)
Task 4 (skills) ─────────────► independent, any time
```

Execution order: 1 → 2 → 3 → 4 → 5. Tasks 3 steps 1-3 (me.md, skill-map.md) can start before Task 1 completes.

---

## Task 1: Vault folder structure (fo-20260427-001)

**Key decisions:**
- Migration: bash only, single atomic operation, no git branch
- Container folder: `areas/`
- Each area dashboard becomes `areas/{area}/index.md`
- `weekly.md` at root: master index; per-area `weekly/` inside each area
- Root `context/` renamed to `reference/`
- `zArchives/` renamed to `archives/`
- `dashboards/` folder removed entirely

**Target structure:**
```
areas/
  nexwave-rd/
    index.md
    tasks/open/, tasks/done/
    inbox/, context/, projects/, logs/, weekly/
    CLAUDE.md   (created in Task 3)
  clinicpro-saas/   (same)
  clinicpro-medtech/  (same)
  gp-fellowship/  (same)
  founder-os/  (same)
home.md
daily/, templates/, weekly.md, reference/, archives/, system/, reviews/
CLAUDE.md, vault-config.json
```

**Steps:**
1. Pre-read: `ls tasks/open/`, `tasks/done/`, `inbox/`, `logs/`, `projects/` to list all files
2. Pre-read: read all dashboard and project files to capture every Dataview query string
3. Pre-read: read `system/` contents (currently untracked, purpose unclear)
4. Create all target directories under `areas/`
5. Move tasks by prefix: `rd-*` → nexwave-rd, `saas-*` → clinicpro-saas, `medtech-*` → clinicpro-medtech, `gpf-*` → gp-fellowship, `fo-*` → founder-os (both open and done)
6. Move inbox: `inbox/{area}/` → `areas/{area}/inbox/`
7. Move context (area-specific):
   - `context/nexwave-rd/` + `context/rd-context/` → `areas/nexwave-rd/context/` (merge)
   - `context/clinicpro-context/` → `areas/clinicpro-saas/context/`
   - `context/medtech-context/` → `areas/clinicpro-medtech/context/`
   - `context/gpf-context/` → `areas/gp-fellowship/context/`
   - `context/vault-audits/` → `areas/founder-os/context/vault-audits/`
   - Remaining context files (tools/, people.md, Claude Code references) → `reference/`
8. Move projects: `projects/{area}.md` → `areas/{area}/projects/`
9. Move logs: `logs/{area}/` → `areas/{area}/logs/`
10. Move dashboards: `dashboards/{area}.md` → `areas/{area}/index.md`; merge `dashboards/home.md` into root `home.md`; move `portfolio-map.canvas` → `reference/`
11. Rename `zArchives/` → `archives/`
12. Move `weekly/briefing.md` content into new root `weekly.md`; create per-area `weekly/` folders
13. Update all Dataview queries in index.md and projects/*.md files: `'"tasks/open"'` → `'"areas/{area}/tasks/open"'`, `'"projects"'` → `'"areas/{area}/projects"'`
14. Update vault CLAUDE.md vault layout section
15. Verify: open Obsidian, confirm all Dataview tables render

---

## Task 2: Memory Level 2 (fo-20260427-002)

**Key decisions:**
- Level 3 deferred (revisit trigger: index exceeds 50 entries OR AI misses context in 2+ sessions)
- Subfolders: `domain/`, `tools/`, `product/`, `project/`

**Steps:**
1. Read all files in `~/.claude/projects/C--Users-reonz-cursor-obsidian/memory/`
2. Create subfolders: `domain/`, `tools/`, `product/`, `project/`
3. Categorise and move each memory file:
   - `domain/`: GP knowledge, NZ health system, clinical context
   - `tools/`: Claude Code patterns, gws setup, hook configs
   - `product/`: ClinicPro/NexWave context, partner contacts
   - `project/`: per-project state, open questions, decisions
4. Update `MEMORY.md` index: correct all file paths, add subfolder section headers
5. Create `C:/Users/reonz/Cursor/hooks/hook_session_start_memory.py`: reads MEMORY.md, outputs `systemMessage` with index content, exit 0 always
6. Add to `~/.claude/settings.json` SessionStart array
7. Verify: start new session, confirm MEMORY.md index appears in context

**Deferred:** Level 3 memsearch (zilliztech/memsearch, Milvus-backed, installs via plugin marketplace). Revisit trigger: index exceeds 50 entries OR AI misses relevant context in 2+ consecutive sessions.

---

## Task 3: CLAUDE.md architecture (fo-20260427-003)

**Key decisions:**
- Behavioral rules stay inline in global CLAUDE.md: non-negotiable. Hooks can fail; CLAUDE.md cannot.
- me.md: identity narrative only, on-demand load
- Behavioral rules are NOT in me.md
- Area CLAUDE.md files depend on Task 1 completing first

**File/retrieval table:**

| File | Location | Retrieval |
|---|---|---|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | Auto: always loaded |
| Workspace CLAUDE.md | `cursor/CLAUDE.md` | Auto: cwd-based |
| Vault CLAUDE.md | `obsidian/CLAUDE.md` | Auto: cwd-based |
| Area CLAUDE.md | `areas/{area}/CLAUDE.md` | Auto: cwd-based |
| MEMORY.md index | `~/.claude/.../memory/MEMORY.md` | Auto: SessionStart hook |
| me.md | `~/.claude/me.md` | On demand |
| vault-map.md | `obsidian/vault-map.md` | On demand |
| skill-map.md | `~/.claude/skill-map.md` | On demand |
| Claude Code best-practice | `cursor/claude-code-best-practice/` | On demand |
| Individual memory files | `~/.claude/.../memory/{subfolders}/` | On demand |

**Steps (1-3 before Task 1; 4-6 after Task 1):**
1. Create `~/.claude/me.md`: identity narrative (GP, solo founder, Auckland), clinical and technical fluency, domain background. No behavioral rules.
2. List all skills in `~/.claude/commands/` and `~/.claude/skills/`
3. Create `~/.claude/skill-map.md`: name, path, trigger, when to use, when not to use for every skill
4. After Task 1: create `obsidian/vault-map.md`: area-based structure, path map, Dataview patterns, file placement rules
5. After Task 1: create `areas/{area}/CLAUDE.md` for each area: active objective, sprint focus, key files, area conventions. Max 20-30 lines each.
6. Trim global CLAUDE.md: remove content moved to me.md, add pointers. Target: 40-50 lines.

---

## Task 4: Skills architecture (fo-20260427-004)

**Key decisions:**
- Self-improvement: Option B (assertions against SKILL.md text, no headless Claude sessions)
- Overnight run via cron; suggestions staged for human review before any change applies
- Priority skills: daily, session-update, weekly, board, obsidian, evolve

**Steps:**
1. List all skills in `~/.claude/commands/` and `~/.claude/skills/`; read all SKILL.md frontmatters
2. Flag skills with vague, missing, or over-long trigger descriptions
3. Invoke `/skill-creator` for each priority skill to refine trigger descriptions
4. Create `evals/evals.json` inside each priority skill directory. Binary assertions only. Examples:
   - "trigger-description is under 200 characters"
   - "no em dashes present"
   - "contains explicit when-not-to-use section"
   - "no inline checkbox tasks in step instructions"
5. Create `C:/Users/reonz/Cursor/skill-evolver/run_eval_loop.py`:
   - Reads SKILL.md + evals.json for each priority skill
   - Scores current SKILL.md against assertions
   - Generates improved variant via model call
   - If score improves, writes to `~/.claude/skill-suggestions/{skill}/proposed-skill.md`
   - Never modifies actual SKILL.md directly
6. Schedule overnight via CronCreate
7. Add to SessionStart: check `~/.claude/skill-suggestions/` for pending items, notify if found
8. Extend `/evolve` skill to handle suggestion review (approve/decline/edit flow)

---

## Task 5: Hooks and automation (fo-20260427-005)

**Key decisions:**
- session-state.md: rejected (transcript + /resume is sufficient)
- PreCompact captures: current objective, uncommitted decisions, active constraints, open questions
- Depends on Task 2 completing first

**Steps:**
1. `hook_session_start_memory.py`: created in Task 2, no further work needed here
2. Create `C:/Users/reonz/Cursor/hooks/hook_precompact.py`: outputs systemMessage with working-memory snapshot (current objective, uncommitted decisions, active constraints, open questions)
3. Register in `~/.claude/settings.json` under PreCompact for both `auto` and `manual` matchers
4. Verify: run /compact with active work in session, confirm snapshot appears in compaction summary
5. Update `/session-update` skill: change `weekly/briefing.md` path to `weekly.md` (master index), add step to write per-area content to `areas/{project}/weekly/`

---

## Deferred decisions

- **Memory Level 3:** Plugin available (zilliztech/memsearch, Milvus-backed). Revisit when index exceeds 50 entries or AI misses context in 2+ consecutive sessions.
- **session-state.md:** Rejected. Not needed.
