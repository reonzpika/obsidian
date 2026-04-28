# Decisions Log

Running record of system decisions. Prevents relitigating. One entry per decision, newest first.

---

## 2026-04-28: Area-based vault structure (Vault OS Redesign — Task 1)

What: Vault migrated from flat global structure to per-area structure under `areas/`. 9 areas: nexwave-rd, clinicpro-saas, clinicpro-medtech, gp-os, founder-os, linkedin, miozuki, other-projects, personal. Each area is self-contained: `areas/{area}/{tasks/open, tasks/done, inbox, context, projects, logs, weekly, index.md}`.
Why: Global tasks/ and projects/ caused Dataview to scan all streams for every view. Area isolation eliminates cross-stream noise and enables per-area CLAUDE.md context files.
Key moves: dashboards/ removed (each became areas/{area}/index.md), projects/ removed (distributed to areas/{area}/projects/), logs/ removed (distributed to areas/{area}/logs/), context/ replaced by reference/ for non-area files, weekly/ replaced by root weekly.md + areas/{area}/weekly/, zArchives/ renamed archives/.
Dataview: All FROM "tasks/open" and FROM "projects" queries updated to area-specific paths. home.md uses FROM "areas" with dashboard: filter.
Prerequisite for: Task 3 (area CLAUDE.md files, vault-map.md), Task 5 (/session-update path update).
Sprint plan: context/vault-os-redesign-sprint-plan.md (now at areas/founder-os/context/).

---

## 2026-04-27: Modular weekly/ and logs/ structure (Option A)

What: `weekly/` directory with `briefing.md` + per-project files. `logs/` directory with per-project subdirectories.
Why: Monolithic `weekly.md` and `logs/YYYY-WNN.md` caused token cost problem: per-project skill sessions loaded all streams. Per-project files allow scoped reads with zero cross-stream noise.
Structure: `weekly/briefing.md` (4 lines), `weekly/{project-id}.md`, `logs/{project-id}/YYYY-WNN.md`, `logs/{project-id}/YYYY-WNN-review.md`.
Skills updated: `/daily`, `/session-update`, `/weekly`, `/monthly`.

---

## 2026-04-27: weekly.md replaces daily files

What: `/daily` updates `weekly.md` instead of creating `daily/YYYY-MM-DD.md` files.
Why: Daily files fragment context across the week. Weekly file keeps the full week in one place for AI orientation and Ryo's planning.
Replaces: `daily/YYYY-MM-DD.md` pattern.

---

## 2026-04-27: weekly.md and monthly.md are planning files only

What: `weekly.md` and `monthly.md` are forward-looking planning documents. No session logs or history inside them.
Why: Mixing planning with logging causes both to grow unboundedly and become hard to navigate.
Replaces: Weekly progress log sections that lived inside dashboard files and weekly notes.

---

## 2026-04-27: Logs move to logs/YYYY-WNN.md

What: Session records and archived weekly files go to `logs/YYYY-WNN.md`. Not inside dashboards.
Why: Dashboards were growing every week and becoming too large to scan quickly.
Replaces: Weekly progress log sections inside `dashboards/*.md`.

---

## 2026-04-27: No sprint concept

What: Sprints removed from the system. Tasks are grouped within projects by `milestone:` label.
Why: Sprint structure added overhead without benefit for a solo founder. Milestone grouping inside projects is sufficient.
Replaces: `sprints/active/` and `sprints/archive/` workflow.

---

## 2026-04-27 (revised same day): Per-project weekly files, not single weekly.md

What: `weekly/briefing.md` (4 lines, always-on) + `weekly/{project-id}.md` (per-project focus and day sections). Replaces single `weekly.md`.
Why: Single `weekly.md` caused token cost problem: every per-project skill session had to load all four streams. Per-project files allow scoped reads. Briefing.md preserves single-file morning orientation at 4 lines.
Replaces: Earlier same-day decision to use single `weekly.md`. That decision was reversed after testing surfaced the token cost problem.
MBIE benefit: `weekly/nexwave-rd.md` isolates R&D planning by structure, not just convention.

---

## 2026-04-27: inbox/ as default landing zone for AI output

What: All AI-generated content lands in `inbox/{project}/` before review. Moves to final location only after explicit Ryo approval.
Why: Prevents unreviewed content entering the system as final.
Replaces: AI writing directly to final file location.

---

## 2026-04-27: Five core system documents in context/system/

What: Created `context/system/` with system-map.md, file-structure.md, workflow-reference.md, decisions-log.md. Techstack remains at `context/stack.md`. Skills remain at `context/skills-index.md`.
Why: System knowledge was fragmented across CLAUDE.md files and Ryo's head. Central reference docs reduce reconstruction cost each session.
