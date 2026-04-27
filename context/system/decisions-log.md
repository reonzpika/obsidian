# Decisions Log

Running record of system decisions. Prevents relitigating. One entry per decision, newest first.

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

## 2026-04-27: Single weekly.md, not stream-specific weekly files

What: One `weekly.md` for all streams. No per-stream weekly files.
Why: Stream-specific weekly files would require opening 4 files each morning to reconstruct the full picture. One file preserves the single-entry orientation goal.
Considered: `dashboards/{stream}/weekly.md` with a linking index. Rejected.

---

## 2026-04-27: inbox/ as default landing zone for AI output

What: All AI-generated content lands in `inbox/{project}/` before review. Moves to final location only after explicit Ryo approval.
Why: Prevents unreviewed content entering the system as final.
Replaces: AI writing directly to final file location.

---

## 2026-04-27: Five core system documents in context/system/

What: Created `context/system/` with system-map.md, file-structure.md, workflow-reference.md, decisions-log.md. Techstack remains at `context/stack.md`. Skills remain at `context/skills-index.md`.
Why: System knowledge was fragmented across CLAUDE.md files and Ryo's head. Central reference docs reduce reconstruction cost each session.
