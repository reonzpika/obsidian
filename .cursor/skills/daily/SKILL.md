---
name: daily
description: Morning routine and midday check-in for Ryo's NexWave/ClinicPro workflow. Reads last 3 days of context in parallel (daily notes, Gmail, projects, tasks), presents a tight briefing with project status, urgent tasks, and quick wins, waits for focus declaration, then writes a minimal focused daily note. Use whenever the user says /daily, "morning routine", "daily note", "start my day", "what's on today", "daily briefing", or wants a snapshot of project status and priorities. Do NOT use for: evening review, day retrospective, tomorrow planning, session wrap-up. Use /daily-review for those.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet
user-invocable: true
---

# Daily Workflow Skill

Tight morning briefing and midday check-in for Ryo's NexWave/ClinicPro workflow. Parallel reads → concise report → focus declaration → minimal daily note.

## Usage

```
/daily            # morning routine
/daily midday     # midday check-in
```

Evening review and tomorrow planning is handled by `/daily-review`.

---

## Vault paths

- Weekly planning file: `weekly.md`
- Logs: `logs/YYYY-WNN.md`
- Active tasks: `tasks/open/*.md` (frontmatter: id, title, project, repo, milestone, status, priority, due — `project` always set; `milestone` optional grouping label)
- Done tasks: `tasks/done/*.md`
- Projects: `projects/*.md` (frontmatter: id, title, status, type, repo, description, phase, dashboard — `phase` is current focus area)
- Inbox: `inbox/`

## Dashboard areas

| dashboard value | display name |
|---|---|
| clinicpro-saas | ClinicPro SaaS |
| clinicpro-medtech | ClinicPro Medtech |
| nexwave-rd | Nexwave R&D |
| gp-os | GP OS |
| personal | Personal |
| linkedin | LinkedIn |
| miozuki | Miozuki |
| other-projects | Other Projects |
| partnerships | Partnerships |

## Repos

| repo field | product |
|---|---|
| clinicpro-saas | Main web app |
| clinicpro-medtech | Capture PWA + BFF |
| nexwave-rd | MBIE R&D (isolated) |
| gp-fellowship | Fellowship training |

## Core rule: no inline tasks

The daily note is a focus layer, not a task layer. All action items live in `tasks/open/` as task files — the daily note references their IDs only. Never write `- [ ]` checkboxes or freeform action items into a daily note. If an action item surfaces during any step, create the task file first, then wikilink it.

---

## Morning Routine

**Time-of-day check:** If the current hour is 17:00 or later, emit one line: "It's evening. Did you mean `/daily-review` for an end-of-day review and tomorrow planning?" and wait before proceeding.

### Setup

Create 3 session tasks:
- `TaskCreate "Read context"`, activeForm: `"Reading notes, projects, tasks, Gmail..."`
- `TaskCreate "Build briefing report"`, activeForm: `"Building today's briefing..."`
- `TaskCreate "Write daily note"`, activeForm: `"Writing daily note..."`

Mark "Read context" in_progress.

---

### Phase 1: Parallel reads

Fire all of the following tool calls in a single message. Do not wait between them.

**Weekly planning file:**
Read `weekly.md`. Extract the briefing section (stream status per line), this week's focus, and any day sections already written this week for context.

**Recent logs and monthly review:**
Glob `logs/*.md` — read the most recent file (highest name) for weekly context. Glob `reviews/monthly/*.md` — read the file matching the current month (YYYY-MM.md), or the most recent if none matches.

If neither exists or is empty, note this as a flag: emit one line in Phase 3 after the Projects table: `**No logs/monthly review found** — consider running /weekly or /monthly`

Extract from weekly review: the daily plan for today and adjacent days, deferred items, open blockers, upcoming external deadlines within 7 days.
Extract from monthly review: the month's focus headline per stream, external deadline table.

**Gmail (last 3 days):**
Run these three gws searches simultaneously:
- `gws gmail users threads list --params '{"userId":"me","q":"newer_than:3d"}'` — received
- `gws gmail users threads list --params '{"userId":"me","q":"newer_than:3d in:sent"}'` — sent
- `gws gmail users threads list --params '{"userId":"me","q":"in:drafts newer_than:3d"}'` — drafts

Then read any actionable threads using `gws gmail users threads get --params '{"userId":"me","id":"<THREAD_ID>"}'`: replies from external contacts, anything unread, anything from key contacts (see Key Contacts section).

**Projects:**
Glob `projects/*.md`, read all project files. Note `id`, `title`, `phase`, `status`, `dashboard` for each active project.

**Tasks:**
Glob `tasks/open/*.md`, read all task files. Note `id`, `title`, `status`, `priority`, `due`, `milestone`, `project`, `repo`, and approximate body length for each.

Mark "Read context" completed.

---

### Phase 2: Background processing

Run these in parallel. Do not print verbose output — this all happens silently.

**Google Alerts (news feed):**
Search Gmail using gws: `gws gmail users messages list --params '{"userId":"me","q":"from:googlealerts-noreply@google.com is:unread"}'`. Process all unread alerts regardless of age (Ryo may skip /daily for several days — the queue is the source of truth).

For each alert:
1. Read the thread with `gws gmail users threads get --params '{"userId":"me","id":"<THREAD_ID>"}'`
2. Extract article titles, sources, and URLs
3. Filter for NZ health / primary care / GP / AI-in-healthcare relevance — skip generic global AI hype and non-health items
4. Dedupe against existing URLs in `C:/Users/reonz/cursor/LinkedIn/knowledge/news_feed.md`
5. Append new items under a dated heading `## YYYY-MM-DD` inserted at the top of that file (after the intro block, before existing dated sections). Format: `- [Article Title](URL), Source`
6. Trash each processed alert: `gws gmail users messages trash --params '{"userId":"me","id":"<MSG_ID>"}'` — one call per message, not batched
7. Track: N items added, M alerts trashed

**Tool tips:**
Search Gmail using gws: `gws gmail users messages list --params '{"userId":"me","q":"from:reonzpika@gmail.com is:unread"}'`. Ryo forwards tools, YouTube videos, and tech resources from his personal address.

For each email:
1. Read the thread with `gws gmail users threads get --params '{"userId":"me","id":"<THREAD_ID>"}'`
2. Extract URL and tool/resource name (usually clear from subject)
3. Skip non-tool emails: Zoom invites, own app links, Vercel logs, meeting forwards, shopping
4. Classify: `claude-code` / `rag` / `ai-memory` / `ai-research` / `ai-scraping` / `ai-image` / `ai-workflow` / `document-parsing` / `directory` / `claude-code-tips` / `industry-news` / `other`
5. If `context/tools/<kebab-name>.md` already exists: append the new source to `additional-sources` in frontmatter
6. If not: create a skeleton file (schema below)
7. Trash only emails where a file was created or updated: `gws gmail users messages trash --params '{"userId":"me","id":"<MSG_ID>"}'`
8. Track: N created, M duplicates, K trashed

Tool tip skeleton schema:
```yaml
---
name: Tool or resource name
category: [category]
status: new
source-email-date: YYYY-MM-DD
source-email-id: GMAIL_MSG_ID
source-url: URL
added: YYYY-MM-DD
researched: false
---
# Tool name
Video/source title: "..."
## Summary
TBD, pending research
## Relevance
TBD, pending research
## Links
- Source URL
- GitHub/Docs: TBD
```

**Auto-task creation from Gmail:**
Identify Gmail threads containing actionable items (reply required, decision needed, unblocks a task) that have no corresponding task file in `tasks/open/`. For each new action item:

Additionally, if any task in `tasks/open/` has `status: blocked` and its body references specific email contacts, search Gmail for threads involving those contacts (both sent and received) and summarise the thread status in the task body. Do not create a new task — annotate the existing one.

**Factual-only rule:** Task files must contain only information directly present in the source email. Specifically:
- `title`: the action required, stated as a plain fact (e.g. "Reply to Anna Bell, Kerikeri Medical")
- Task body: quote or paraphrase the email content only — sender, subject, date, what they asked or said
- Cross-references: link to existing task IDs where the email is clearly related (e.g. `Related: [[medtech-20260414-001]]`)
- Never add: reply guidance, suggested wording, how-to steps, technical recommendations, "Next steps", or any context not in the source email. If in doubt, omit it.
- If you don't know something, leave it blank or omit it — do not invent it

1. Create a task file in `tasks/open/` using the Task Schema below
2. Track: K tasks created

These new task IDs will appear in the Urgent table in Phase 3.

---

### Phase 3: Briefing report

Mark "Build briefing report" in_progress.

Present the following structure — nothing else, no preamble, no "good morning":

---

```
## [Day], [Date]

**This week's recap:**
- [most significant thing that shipped, moved, or landed this week]
- [second most significant]
- [third — only include if genuinely distinct]

**Projects:**
| Project | Phase | Open tasks |
|---------|-------|------------|

**Urgent:**
| Project | Task | Note |
|---------|------|------|

**Quick wins:**
| Project | Task | Note |
|---------|------|------|

Background: [summary line]
```

---

**Timeline cue (from weekly/monthly reviews):**
After the Off-radar line (or Projects table if no off-radar areas), add one line listing external deadlines due within 7 days that are not already surfaced in the Urgent table. Format:
`**Upcoming:** 25 Apr — AMP collegial meeting | 27 Apr — Bell Gully reply deadline`
Pull from the monthly review's external deadline table and the weekly review's day plans. If nothing new, omit this line.

**Off-radar logic:**
After computing the projects table, identify which dashboard areas are off radar:
1. Collect `dashboard` values from all active projects (status != "parked"). These are on radar.
2. Any of the 6 areas (clinicpro-saas, clinicpro-medtech, nexwave-rd, gp-fellowship, side-projects, partnerships) not in that set = off radar.
3. If any off-radar areas exist, add one line immediately after the Projects table:
   `**Off radar** (no active project): ClinicPro SaaS, Partnerships`
   Use the display name from the Dashboard areas table, not the dashboard value.
4. If all areas have active projects, omit this line entirely.

**Projects table rules:**
- One row per active project (status != "parked")
- Project = `[[projects/{project.id}|{project.title}]]`
- Phase = project's `phase` field, or "—" if empty
- Open tasks = count of `tasks/open/*.md` where `project` matches this project's `id`

**Urgent table rules — include a task if ANY of these are true:**
- `due` = today or tomorrow
- `status: in-progress` AND `status: blocked`
- Task was created in Phase 2 auto-creation (new from Gmail)

Note column = brief reason: `"due today"` / `"blocked: waiting on X"` / `"new from Gmail"`

**Quick wins table rules — include a task if ALL of these are true:**
- Title contains any of: reply, review, check, confirm, read, await, send, ask
- OR body word count is under ~120 words
- AND `status` is not `blocked`
- AND title does NOT contain: build, implement, migrate, design, write (as in "write code/feature")
- AND task does NOT already appear in the Urgent table

Note column = brief cue: `"reply needed"` / `"2-min review"` / `"quick confirm"`

**Background line:**
`Background: N news items added | M tool skeletons created | K tasks from Gmail`
If all zero: `Background: nothing new`

Mark "Build briefing report" completed.

End with exactly:
> What's your focus for today?

Wait. Do not suggest a plan. Do not ask follow-up questions.

---

### Phase 4: Update weekly.md

Once the user replies, mark "Write daily note" in_progress.

Read `weekly.md`. Check if a section for today already exists (e.g. `## Monday 2026-04-27`).

**If today's section does not exist:** append it after the last existing day section.

**If today's section exists:** update the Focus subsection in-place with the user's stated focus.

Today's section template:

```markdown
## [Day] YYYY-MM-DD

### Focus
- [user's stated focus — one bullet per distinct goal]

### Urgent
- [[task-id]] — title

### Quick wins
- [[task-id]] — title

### Blockers
- [[task-id]] — waiting on X
```

**Writing rules:**
- Focus: user's stated focus verbatim or lightly cleaned. One bullet per distinct goal.
- Urgent and Quick wins: wikilinks `[[task-id]]`, no checkboxes, only tasks in scope of the user's stated focus.
- Blockers: up to 5, only tasks where `status: blocked` pulled from `tasks/open/`. Format: `[[task-id]] — waiting on X`
- If the user's reply surfaces a new action item: create the task file first, then wikilink it.
- Do not create a new file. Always edit `weekly.md`.

Mark "Write daily note" completed.

Confirm with one line: `weekly.md updated → [Day] YYYY-MM-DD section written`

---

## Task Schema

```yaml
id: {repo-prefix}-{YYYYMMDD}-{NNN}
title: Short human-readable description
project: {project-id}
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship
milestone: "text label"             # optional grouping label
status: open | in-progress | blocked | done
priority: high | medium | low
created: YYYY-MM-DD
due: YYYY-MM-DD
```

R&D tasks add: `objective: obj-1|obj-2|obj-3|obj-4|capability` and `owner: ryo|ting|both`.

---

## Key Contacts

| Name / email | Role |
|---|---|
| Defne Arzanoglu / alexsupport@medtechglobal.com | Medtech ALEX support |
| Ting / tingchou1988@gmail.com | R&D Programme Manager |
| Lisa Pritchard / Lisa.Pritchard@mbie.govt.nz | MBIE Innovation Services |
| Lawrence Peterson / LPeterson@medtechglobal.com | AU market opportunity |
| Alex Cauble-Chantrenne / AChantrenne@medtechglobal.com | Medtech NZ partnership |

---

## Midday Check-in

### Step 1: Review morning plan

Read `weekly.md`. Find today's section (e.g. `## Monday 2026-04-27`). Identify tasks in `### Urgent` and `### Quick wins` — what's done, in-progress, not started.

### Step 2: Update task statuses

For tasks completed since morning:
- Update `status: done` in the task file frontmatter
- Move file from `tasks/open/` to `tasks/done/`

For tasks that progressed but aren't done:
- Update `status: in-progress` if still `open`

### Step 3: Check Gmail for urgent items

Search Gmail for unread emails in the last 2 days using gws: `gws gmail users threads list --params '{"userId":"me","q":"newer_than:2d is:unread"}'`. Read actionable threads with `gws gmail users threads get --params '{"userId":"me","id":"<THREAD_ID>"}'`. Cross-reference against `tasks/open/` where `status: blocked` — if an email unblocks a task, note the task ID.

### Step 4: Create task files for new action items

For every actionable item surfaced (email replies, new work, follow-ups), create a task file in `tasks/open/` immediately. Do not leave action items as prose.

### Step 5: Flag overdue or at-risk tasks

Note tasks that are overdue or unlikely to complete today.

### Step 6: Present and ask

```
Done: [task IDs completed]
Remaining: [task IDs still open from today's plan]
New tasks: [IDs created this check-in]
At risk: [IDs overdue or likely to slip]
```

Then ask: "What's the most important thing for this afternoon?"

---

## Integration

- `/session-update`: end-of-session log, replaces the old evening shutdown
- `/weekly`: reads weekly.md and logs/ to compile project and milestone summary
- `/obsidian-task-table`: create new tasks surfaced during daily review
