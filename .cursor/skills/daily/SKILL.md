---
name: daily
description: Morning routine and midday check-in for Ryo's NexWave/ClinicPro workflow. Reads last 3 days of context in parallel (daily notes, Gmail, sprints, tasks), presents a tight briefing with sprint status, urgent tasks, and quick wins, waits for focus declaration, then writes a minimal focused daily note. Use whenever the user says /daily, "morning routine", "daily note", "start my day", "what's on today", "daily briefing", or wants a snapshot of sprint status and priorities.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, mcp__claude_ai_Gmail__search_threads, mcp__claude_ai_Gmail__get_thread
user-invocable: true
---

# Daily Workflow Skill

Tight morning briefing and midday check-in for Ryo's NexWave/ClinicPro workflow. Parallel reads → concise report → focus declaration → minimal daily note.

## Usage

```
/daily            # morning routine
/daily midday     # midday check-in
```

Evening shutdown is handled by `/session-update`.

---

## Vault paths

- Daily notes: `daily/YYYY-MM-DD.md`
- Active tasks: `tasks/open/*.md` (frontmatter: id, title, project, repo, sprint, status, priority, due — `project` OR `sprint` set, never both)
- Done tasks: `tasks/done/*.md`
- Active sprints: `sprints/active/*.md` (frontmatter: id, status, start, end, repos, projects, goal, dashboard)
- Projects: `projects/*.md` (frontmatter: id, title, status, type, repo, description, dashboard)
- Inbox: `inbox/`

## Dashboard areas

| dashboard value | display name |
|---|---|
| clinicpro-saas | ClinicPro SaaS |
| clinicpro-medtech | ClinicPro Medtech |
| nexwave-rd | Nexwave R&D |
| gp-fellowship | GP Fellowship |
| side-projects | Side Projects |
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

### Setup

Create 3 session tasks:
- `TaskCreate "Read context"`, activeForm: `"Reading notes, sprints, tasks, Gmail..."`
- `TaskCreate "Build briefing report"`, activeForm: `"Building today's briefing..."`
- `TaskCreate "Write daily note"`, activeForm: `"Writing daily note..."`

Mark "Read context" in_progress.

---

### Phase 1: Parallel reads

Fire all of the following tool calls in a single message. Do not wait between them.

**Daily notes (last 3 days):**
Read `daily/YYYY-MM-DD.md`, `daily/YYYY-MM-DD-1.md`, `daily/YYYY-MM-DD-2.md`. Skip silently if a file doesn't exist.

**Gmail (last 3 days):**
Run these three searches simultaneously:
- `newer_than:3d` — received
- `newer_than:3d in:sent` — sent
- `in:drafts newer_than:3d` — drafts

Then read any threads that look actionable: replies from external contacts, anything unread, anything from key contacts (see Key Contacts section).

**Sprints:**
Glob `sprints/active/*.md`, read all sprint files. Extract `id`, `goal`, `start`, `end`, `repos`, `dashboard` for each.

**Tasks:**
Glob `tasks/open/*.md`, read all task files. Note `id`, `title`, `status`, `priority`, `due`, `sprint`, `repo`, and approximate body length for each.

Mark "Read context" completed.

---

### Phase 2: Background processing

Run these in parallel. Do not print verbose output — this all happens silently.

**Google Alerts (news feed):**
Search Gmail: `from:googlealerts-noreply@google.com is:unread`. Process all unread alerts regardless of age (Ryo may skip /daily for several days — the queue is the source of truth).

For each alert:
1. Read the message with `get_thread`
2. Extract article titles, sources, and URLs
3. Filter for NZ health / primary care / GP / AI-in-healthcare relevance — skip generic global AI hype and non-health items
4. Dedupe against existing URLs in `C:/Users/reonz/cursor/LinkedIn/knowledge/news_feed.md`
5. Append new items under a dated heading `## YYYY-MM-DD` inserted at the top of that file (after the intro block, before existing dated sections). Format: `- [Article Title](URL), Source`
6. Trash each processed alert: `gws gmail users messages trash --params '{"userId":"me","id":"<MSG_ID>"}'` — one call per message, not batched
7. Track: N items added, M alerts trashed

**Tool tips:**
Search Gmail: `from:reonzpika@gmail.com is:unread`. Ryo forwards tools, YouTube videos, and tech resources from his personal address.

For each email:
1. Read the message with `get_thread`
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
1. Create a task file in `tasks/open/` using the Task Schema below
2. Track: K tasks created

**Factual-only rule:** Task files must contain only information directly present in the source email. Specifically:
- `title`: the action required, stated as a plain fact (e.g. "Reply to Anna Bell, Kerikeri Medical")
- Task body: quote or paraphrase the email content only — sender, subject, date, what they asked or said
- Cross-references: link to existing task or sprint IDs where the email is clearly related (e.g. `Related: [[medtech-20260414-001]]`)
- Never add reply guidance, suggested wording, how-to advice, "Next steps", or any context not present in the source email
- If you don't know something, leave it blank or omit it — do not invent it

These new task IDs will appear in the Urgent table in Phase 3.

---

### Phase 3: Briefing report

Mark "Build briefing report" in_progress.

Present the following structure — nothing else, no preamble, no "good morning":

---

```
## [Day], [Date]

**3-day recap:**
- [most significant thing that shipped, moved, or landed]
- [second most significant]
- [third — only include if genuinely distinct]

**Sprints:**
| Project | Goal | Current task | Days left |
|---------|------|-------------|-----------|

**Urgent:**
| Project | Task | Note |
|---------|------|------|

**Quick wins:**
| Project | Task | Note |
|---------|------|------|

Background: [summary line]
```

---

**Off-radar logic:**
After computing the sprint table, identify which dashboard areas are off radar:
1. Collect `dashboard` values from all active sprints (today between `start` and `end`). These are on radar.
2. Any of the 6 areas (clinicpro-saas, clinicpro-medtech, nexwave-rd, gp-fellowship, side-projects, partnerships) not in that set = off radar.
3. If any off-radar areas exist, add one line immediately after the Sprint table:
   `**Off radar** (no active sprint): ClinicPro SaaS, Partnerships`
   Use the display name from the Dashboard areas table, not the dashboard value.
4. If all areas have active sprints, omit this line entirely.

**Sprint table rules:**
- One row per sprint where today falls between `start` and `end`
- Project = sprint's `repos` value (or project name)
- Current task = title of the first `in-progress` or `due-today` task for that sprint. If none: `—`
- Flag sprints ending in ≤2 days with ⚠ in the Days left cell

**Urgent table rules — include a task if ANY of these are true:**
- `due` = today or tomorrow
- Sprint it belongs to ends in ≤2 days
- `status: in-progress` AND `status: blocked`
- Task was created in Phase 2 auto-creation (new from Gmail)

Note column = brief reason: `"due today"` / `"sprint ends tomorrow"` / `"blocked: waiting on X"` / `"new from Gmail"`

**Quick wins table rules — include a task if ALL of these are true:**
- Title contains any of: reply, review, check, confirm, read, await, send, ask
- OR body word count is under ~120 words
- AND `status` is not `blocked`
- AND title does NOT contain: build, implement, migrate, design, write (as in "write code/feature")

Note column = brief cue: `"reply needed"` / `"2-min review"` / `"quick confirm"`

**Background line:**
`Background: N news items added | M tool skeletons created | K tasks from Gmail`
If all zero: `Background: nothing new`

Mark "Build briefing report" completed.

End with exactly:
> What's your focus for today?

Wait. Do not suggest a plan. Do not ask follow-up questions.

---

### Phase 4: Write daily note

Once the user replies, mark "Write daily note" in_progress.

Write `daily/YYYY-MM-DD.md` using this template:

```markdown
---
date: YYYY-MM-DD
day: [Day name]
---

# YYYY-MM-DD

[[dashboards/home]] | [[daily/YYYY-MM-DD-1]]

## Focus
> [user's stated focus, verbatim or lightly cleaned]

## Today

### Sprints
| Project | Goal | Current task | Days left |
|---------|------|-------------|-----------|

### Urgent
- [[task-id]] — title

### Quick wins
- [[task-id]] — title

## Blockers
- [[task-id]] — waiting on X

---

[[dashboards/home]]
```

**Writing rules:**
- Sprint table: same as the report. If user narrowed scope (e.g. "only medtech today"), include only relevant sprints.
- Urgent and Quick wins: wikilinks `[[task-id]]`, no checkboxes, only tasks in scope of the user's stated focus.
- Blockers: up to 5, only tasks where `status: blocked` pulled from `tasks/open/`. Format: `[[task-id]] — waiting on X`
- If the user's reply surfaces a new action item: create the task file first, then wikilink it in the note.
- Always add `[[dashboards/home]] | [[daily/YYYY-MM-DD-1]]` (home link + previous day link) on the line immediately after the `# YYYY-MM-DD` title. No nav links at the bottom.
- Always add `[[daily/YYYY-MM-DD]]` on the line immediately after the `# Dashboard: All Projects` title in `dashboards/home.md`, replacing the previous date's link.
- Nothing else: no Gmail section, no From Yesterday, no Evening Reflection, no Notes section. Ephemeral notes belong in chat.

Mark "Write daily note" completed.

Confirm with one line: `Daily note written → daily/YYYY-MM-DD.md`

---

## Task Schema

```yaml
id: {repo-prefix}-{YYYYMMDD}-{NNN}
title: Short human-readable description
project: {project-id}
repo: clinicpro-saas | clinicpro-medtech | nexwave-rd | gp-fellowship
sprint: {sprint-id}
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

Read today's `daily/YYYY-MM-DD.md`. Identify tasks in `## Today` — what's done, in-progress, not started.

### Step 2: Update task statuses

For tasks completed since morning:
- Update `status: done` in the task file frontmatter
- Move file from `tasks/open/` to `tasks/done/`

For tasks that progressed but aren't done:
- Update `status: in-progress` if still `open`

### Step 3: Check Gmail for urgent items

Search Gmail for unread emails in the last 2 days. Read anything from key contacts or that looks actionable. Cross-reference against `tasks/open/` where `status: blocked` — if an email unblocks a task, note the task ID.

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
- `/weekly`: reads daily notes to compile sprint summary
- `/obsidian-task-table`: create new tasks surfaced during daily review
