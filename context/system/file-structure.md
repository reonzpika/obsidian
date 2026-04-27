# File Structure Spec

What goes in each file type. What does not. Authoritative reference.

---

## home.md

**Purpose:** Portfolio index. Single starting point for Ryo and AI.

**Contains:**
- Dataview-generated project table (title, status, phase, dashboard)
- Active task count per stream
- Quick links to stream dashboards

**Does not contain:** task tables, history, daily notes, project detail, manual entries.

**Rule:** Everything is Dataview-generated from frontmatter. Never add manual content.

---

## dashboards/{stream}.md

**Purpose:** Stream-level index. Current state only.

**Contains:**
- Project list with phase and status (Dataview)
- Current focus (one line, manually maintained)
- Key contacts for the stream
- Links to projects

**Does not contain:** task tables, progress history, weekly logs, context docs, planning.

**Rule:** If this file is growing over time, something is in the wrong place. History goes to `logs/`. Planning goes to `weekly.md`.

---

## projects/{project}.md

**Purpose:** Project detail and task table.

**Contains:**
- Frontmatter (id, title, status, type, repo, stack, phase, dashboard)
- Current focus (one line)
- Milestone-grouped task table (Dataview embed)
- Links to relevant context docs

**Does not contain:** history logs, stream-level information, inline checkbox tasks, session notes.

**Rule:** Body is notes and Dataview embeds only. Workflow state lives in task frontmatter. Tasks are grouped by `milestone:` label within the Dataview query.

---

## tasks/open/{id}.md

**Purpose:** Single task with full context.

**Contains:**
- Frontmatter only (id, title, project, repo, milestone, status, priority, created, due)
- Notes section (free text, blockers, links to inbox items)

**Does not contain:** inline checkbox tasks, code, lengthy context (link to `context/` instead).

**Rule:** `project:` must match an actual filename in `projects/` without `.md`. `milestone:` must exactly match the label used in the project's Dataview grouping.

---

## tasks/done/{id}.md

**Purpose:** Completed task archive.

**Rule:** Moved here by `/complete-task` Templater macro. Never manually move or edit `status: done` in place.

---

## weekly.md

**Purpose:** Rolling weekly planning file. Forward-looking only. Reset each Monday.

**Structure:**
```
## Briefing
{stream}: {one-line status} | {urgent item} | {open decision}
(4 lines, one per stream — updated by /session-update at session end)

## Focus this week
- ClinicPro SaaS:
- ClinicPro Medtech:
- NexWave R&D:
- GP Fellowship:

## Monday YYYY-MM-DD
**Plan:**
**Done:**
**Blocked:**

## Tuesday ...
(repeat for each day worked)
```

**Does not contain:** session logs, project detail, task tables, history beyond the current week.

**Rule:** `/daily` updates this file. It does not create new `daily/YYYY-MM-DD.md` files. At end of week, `/weekly` archives this file to `logs/` and resets it.

---

## monthly.md

**Purpose:** Monthly review and forward plan. Written once per month.

**Structure:**
- What shipped this month (per stream)
- What stalled and why
- Decisions made
- Next month priorities (per stream)

**Does not contain:** task tables, daily detail, running logs.

**Rule:** Written by `/monthly` skill. Not a running log. Previous months archived to `logs/`.

---

## logs/YYYY-WNN.md

**Purpose:** Session and weekly log records. Grows freely.

**Contains:** Session summaries (written by `/session-update`), archived weekly files (moved by `/weekly`).

**Rule:** Never read for orientation. This is a write-only sink except for retrospective lookups.

---

## context/system/

**Purpose:** System reference docs for Ryo and AI.

**Contains:** system-map.md, file-structure.md, workflow-reference.md, decisions-log.md only.

**Rule:** No project content here.

---

## context/{stream}-context/

**Purpose:** Stream-specific reference material.

**Contains:** research docs, briefings, proposals, API references, strategy docs for that stream.

**Rule:** Linked from relevant `projects/*.md` or `dashboards/*.md`. Not embedded inline.

---

## inbox/

**Purpose:** Landing zone for all unreviewed AI output.

**Rule:** Every AI-generated file lands here first. Nothing moves to its final location without explicit Ryo approval.
