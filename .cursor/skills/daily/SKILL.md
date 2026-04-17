---
name: daily
description: Create today's daily note and run morning, midday, or evening routines. Surfaces active sprint tasks, blocked items, project priorities, and Gmail highlights for Ryo's founder/GP workflow.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet, mcp__claude_ai_Gmail__gmail_search_messages, mcp__claude_ai_Gmail__gmail_read_message
user-invocable: true
---

# Daily Workflow Skill

Creates daily notes and runs structured morning, midday, and evening routines tailored for Ryo's NexWave/ClinicPro workflow.

## Usage

```
/daily            # Create today's note + morning routine
/daily midday     # Midday check-in
/daily evening    # Evening shutdown
```

## Vault paths

- Daily notes: `daily/YYYY-MM-DD.md`
- Active tasks: `tasks/open/*.md` (frontmatter: id, title, project, repo, sprint, status, priority, due)
- Done tasks: `tasks/done/*.md`
- Active sprints: `sprints/active/*.md` (frontmatter: id, status, start, end, repos, projects, goal)
- Projects: `projects/*.md` (frontmatter: id, status, type, repo)
- Inbox: `inbox/`

## Repos

| repo field | product |
|---|---|
| clinicpro-saas | Main web app |
| clinicpro-medtech | Capture PWA + BFF |
| nexwave-rd | MBIE R&D (isolated) |
| gp-fellowship | Fellowship training |

## Core rule: no inline tasks

**The daily note is a focus layer, not a task layer.**

- All action items live in `tasks/open/` as task files — that is the single source of truth
- The daily note references task IDs; it never owns them
- Never write `- [ ]` checkboxes or freeform action items into a daily note
- If an action item surfaces during any daily routine step (Gmail, reflection, conversation), create the task file in `tasks/open/` first, then reference the task ID in the daily note
- This rule applies to Claude and to the user — if the user writes inline tasks, flag it and offer to convert them to task files

## Morning Routine

### Step 1: Create today's note

Check if `daily/YYYY-MM-DD.md` exists. If yes, open it. If no, create from template below.

### Step 2: Carry forward from yesterday

Read yesterday's daily note at `daily/YYYY-MM-DD-1.md` (subtract 1 day from today).

If it exists, extract:
- `## Evening Reflection > Tomorrow's priority` — surface this prominently at the top of today's briefing
- `## Notes` — scan for any observations, decisions, or open questions worth carrying forward

Display as a brief block before the sprint context:

```
From yesterday:
  Priority: [tomorrow's priority text]
  Notes: [any observations worth surfacing — skip if nothing meaningful]
```

If yesterday's note doesn't exist, skip silently.

**Do not carry forward task references** — those are managed by `tasks/open/` and will surface correctly in Step 3.

### Step 4: Surface sprint context

Read all files in `sprints/active/`. For each sprint where today falls between `start` and `end`:
- Extract `id`, `goal`, `end`, `repos`
- Calculate days remaining to `end`
- Flag sprints ending within 3 days

Display as:

```
Active sprints:
  2026-04-sprint-1 — Referral Images paid model (ends Apr 18, 6 days)
  2026-04-rd-sprint-2 — [goal] (ends [date], N days)
```

### Step 5: Surface today's tasks

Read all files in `tasks/open/`. Filter where `due = today` OR `status: in-progress`. Group by repo. Exclude `status: done`.

These are **references** to task files — display the task ID and title only. The daily note does not own these tasks.

Display as:

```
Today's tasks (from tasks/open/):
  clinicpro-saas:
    - saas-20260407-001 — Referral Images landing page copy
  nexwave-rd:
    - rd-20260329-020 — Find Indici contact (overdue)
```

Write these into the daily note's `## Today's Focus` section as a reference list — task IDs and titles only, no checkboxes.

### Step 6: Surface blockers

Read `tasks/open/`. Filter where `status: blocked`. List task IDs and titles. No checkboxes.

### Step 7: Surface Gmail highlights

Search Gmail for emails received in the last 7 days using `mcp__claude_ai_Gmail__gmail_search_messages` with query `newer_than:7d`.

Read the content of any email that looks actionable or is from a key contact using `mcp__claude_ai_Gmail__gmail_read_message`.

**Key contacts to prioritise:**

| Name | Role | Flag as |
|------|------|---------|
| Defne Arzanoglu / alexsupport@medtechglobal.com | Medtech ALEX support | Action — ALEX/API |
| Ting (tingchou1988@gmail.com) | R&D Programme Manager | Action — R&D programme |
| Lisa Pritchard | MBIE / Callaghan Innovation | Action — R&D/grant |
| Lawrence Peterson | AU market opportunity | Action — commercial |

**Triage rules:**

1. **Needs action** — reply required, decision needed, or unblocks a task (e.g. Defne responding on Invoice API)
2. **Waiting on them** — you sent something and they've responded or not yet
3. **FYI only** — read, no action

**Cross-reference against blockers:** If an email resolves or updates a blocked task in `tasks/open/`, note the task ID alongside the email entry.

**Display as:**

```
Gmail (last 7 days):

Needs action:
  - [Sender] — [Subject] (received Mon Apr 8) → unblocks medtech-20260408-003
  - [Sender] — [Subject] (received Wed Apr 10)

Waiting on:
  - Lawrence Peterson — no reply yet on AU market thread

FYI:
  - [Sender] — [Subject]
```

If no actionable emails found, display: "Gmail: nothing actionable in the last 7 days."

Add the Gmail section to today's daily note under a `## Gmail` heading.

### Step 8: Update LinkedIn news feed from Google Alerts

Scan Gmail for **all unread** Google Alerts, regardless of age: `from:googlealerts-noreply@google.com is:unread`. Ryo may skip /daily for several days at a time, so the queue is the source of truth, not a rolling window.

For each alert:
- Read the message with `mcp__claude_ai_Gmail__gmail_read_message`
- Extract article titles, sources, and URLs
- Filter for NZ health / primary care / GP / AI-in-healthcare relevance (skip generic global AI hype and non-health items)
- Dedupe against existing URLs in `C:/Users/reonz/cursor/LinkedIn/knowledge/news_feed.md`

Append new items under a dated heading `## YYYY-MM-DD` inserted at the top of the file (after the intro block, before the existing Tier sections). Format each entry as:

```
- [Article Title](URL) — Source
```

Use today's date in the heading, not the alert's original date.

**After all alerts have been read and processed**, move every processed alert message to Trash so the unread queue is cleared:

```bash
gws gmail users messages trash --params '{"userId":"me","id":"<MESSAGE_ID>"}'
```

Run one call per message — do not batch. Trash (not permanent delete) so the action is reversible for 30 days if anything is lost.

**List every entry added to `news_feed.md`** in the Step 9 briefing under a dedicated `News feed` block — title + source per line. Also report totals: `N new entries added, M alerts trashed`. If no alerts were unread, report `News feed: no unread alerts`.

Do not modify existing Tier sections — they are curated manually.

### Step 9: Process personal tool-tip emails

Scan Gmail for unread emails from Ryo's personal address: `from:reonzpika@gmail.com is:unread`.

Ryo forwards interesting tools, YouTube videos, and tech resources from his personal Gmail. This step captures them as skeleton files under `C:/Users/reonz/cursor/obsidian/context/tools/` for later research.

For each email:
- Read the message with `mcp__claude_ai_Gmail__gmail_read_message`
- Extract the URL and the resource name (usually clear from the subject, e.g. `docling`, `Scrapling`, `Claude Mem`)
- Classify as one of: `claude-code` / `rag` / `ai-memory` / `ai-research` / `ai-scraping` / `ai-image` / `ai-workflow` / `document-parsing` / `directory` / `claude-code-tips` / `industry-news` / `other`
- **Skip** non-tool emails (his own app links, Zoom invites, Vercel logs, meeting forwards, unrelated shopping) — do not create a file for these
- **Derive a kebab-case filename** from the tool name (e.g. `docling.md`, `rag-anything.md`)
- **If the file already exists** (same tool mentioned before), append the new source to `additional-sources` in the frontmatter instead of creating a duplicate
- **If not**, create a new skeleton file with this schema:

```yaml
---
name: Tool or resource name
category: one of the values above
status: new
source-email-date: YYYY-MM-DD
source-email-id: GMAIL_MSG_ID
source-url: URL
added: YYYY-MM-DD (today)
researched: false
---

# Tool name

Video/source title: "..."

## Summary
TBD — pending research

## Relevance
TBD — pending research (note any obvious tie-in to NexWave / ClinicPro / R&D workflow)

## Links
- Source URL
- GitHub/Docs: TBD
```

**Do not deep-research each tool automatically** — that happens on-demand when Ryo asks ("research X"). Skeleton files are the queue.

**After processing all tool emails**, archive each from the inbox and mark read:

```bash
gws gmail users messages modify --params '{"userId":"me","id":"<MSG_ID>"}' --json '{"removeLabelIds":["UNREAD","INBOX"]}'
```

Archive (not trash) so the original email stays searchable. Run one call per message, including non-tool emails you skipped — they shouldn't stay unread indefinitely.

Report in the Step 10 briefing: `Tool tips: N new skeleton files created, M duplicates appended, K emails archived`. If nothing unread, report `Tool tips: inbox empty`.

### Step 10: Present overview with suggested plan

Present the briefing and a proposed plan for the day in chat. Use this structure:

```
Good morning. Here's today's picture.

From yesterday: [priority carried / notes — skip if blank]

Active sprints:
  [sprint table — flag anything ending within 3 days or overdue]

Gmail:
  Needs action: [...]
  Waiting on: [...]
  FYI: [...]

News feed (from Google Alerts):
  Added to LinkedIn/knowledge/news_feed.md:
    - [Title] — [Source]
    - [Title] — [Source]
  Totals: N new entries added, M alerts trashed
  (or: "News feed: no unread alerts")

Tool tips (from personal Gmail):
  New skeleton files in context/tools/:
    - [Tool name] — [category]
  Totals: N new, M duplicates appended, K emails archived
  (or: "Tool tips: inbox empty")

---

Suggested plan for today:

| # | Area | Goal |
|---|------|------|
| 1 | [highest priority area] | [what to achieve] |
| 2 | ...                     | ...               |

Parked: [tasks in scope but blocked or deferred — list task IDs]

---

Does this look right? What do you want to focus on or change?
```

**How to build the suggested plan:**
- Prioritise by: due today > overdue > sprint deadlines within 3 days > high priority in-progress > other open
- Respect repo isolation — don't mix R&D and commercial where they shouldn't cross
- Do not include blocked tasks unless unblocking them is the action
- Do not include tasks explicitly deferred by Ryo in prior notes
- Limit to 5-7 items — a full day, not a wishlist
- Show the task IDs + titles in the plan rows so Ryo can see exactly what's included

Keep the tone tight. Flag anything urgent but don't editorialize — let Ryo decide.

### Step 11: Ask one question

After the overview and suggested plan, ask exactly one question:

> "Does this look right? What do you want to focus on or change?"

Wait for the response. Do not ask follow-up questions — one pass is enough.

### Step 12: Write the plan

Once Ryo responds, incorporate any changes and write the final sections of the daily note.

**In the note, write:**

1. `## Focus` blockquote — one crisp sentence capturing the day's intent.

2. `## Today's Plan` — numbered priority table based on the confirmed plan:

```markdown
## Today's Plan
<!-- Ordered by priority. Parked items not in scope today. -->

| # | Area | Goal |
|---|------|------|
| 1 | miozuki-web | Finish content migration so Ting can work independently |
| 2 | nexwave-rd admin | Xero bank feeds + KiwiSaver — clear all admin today |
```

3. `## Today's Focus` — tasks grouped by the confirmed priorities, in order. Use named priority sections (e.g. `### 1. miozuki-web — finish handover for Ting`) rather than plain repo headings. Add a `### Parked today` section at the bottom for anything deferred — do not silently drop tasks.

**In chat, confirm the final plan** and flag anything urgent that wasn't included (e.g. "Note: gpf-20260330-008 is due today — parked as intended?").

If any action items surface from Ryo's response, create a task file in `tasks/open/` immediately and note the ID in `## Notes`.

## Daily Note Template

```markdown
---
date: YYYY-MM-DD
day: Monday
---

# YYYY-MM-DD

## Focus
> 

## From Yesterday
- Priority carried: 
- Notes: 

## Active Sprints
| Sprint | Goal | Ends | Days left |
|--------|------|------|-----------|

## Today's Plan
<!-- Ordered by priority as confirmed with Ryo. Parked items at bottom. -->

| # | Area | Goal |
|---|------|------|

## Today's Focus
<!-- Reference only — tasks live in tasks/open/. No inline checkboxes. -->
<!-- Grouped by Today's Plan priority order, not by repo. -->

## Blockers
<!-- Reference only — task IDs from tasks/open/ where status: blocked -->
- 

## Gmail
### Needs action
- 

### Waiting on
- 

### FYI
- 

## Notes
<!-- Free text only. If anything here needs action, create a task file and add the ID. -->

## Evening Reflection
- Wins:
- Challenges:
- Tomorrow's priority:
```

## Midday Check-in

### Step 1: Review morning task list

Read all files in `tasks/open/` that appear in today's daily note `## Today's Focus`. Compare against the morning plan — what's done, what's in-progress, what hasn't started.

### Step 2: Update task statuses

For every task completed since the morning review:
- Update `status: done` in the task file frontmatter
- Move the file from `tasks/open/` to `tasks/done/`

For tasks that have progressed but aren't done:
- Update `status: in-progress` if still `open`

Do not wait for the user to ask — update statuses proactively based on what you can see in the daily note `## Notes` and conversation context.

### Step 3: Check for sprint status changes

Read `sprints/active/`. If a sprint's tasks are all done or the sprint end date has passed, flag it. Update sprint `status` frontmatter if appropriate (e.g. `active` → `completed`).

### Step 4: Check inbox for urgent items

Search Gmail for unread emails in the last 2 days. Read anything from key contacts or that looks actionable. Cross-reference against blocked tasks.

### Step 5: Create task files for new action items

For every actionable item surfaced during the review (emails needing replies, follow-ups, new work identified), create a task file in `tasks/open/` immediately. Do not leave action items as prose in the daily note or chat — they must become task files.

### Step 6: Identify anything to reschedule or drop

Flag tasks that are overdue, at risk, or should be deferred. Suggest reprioritisation if the afternoon looks overloaded.

### Step 7: Present and ask

Present the status update (done / remaining / new tasks created) and ask:

> "What's the most important thing for this afternoon?"

## Evening Shutdown

1. Update today's note: fill in Wins, Challenges, Tomorrow's priority
2. For each task completed today: update `status: done` in the task file in `tasks/open/` and move the file to `tasks/done/`
3. Scan `inbox/` — for each item, either create a task file or discard. No inbox items should be copied inline into the daily note.
4. Prompt: "Any decisions or learnings worth capturing?" — **do not write these into the daily note.** Route each item to its proper long-lived home:
   - **Project-specific decisions or design patterns** → `projects/{project-id}.md` under a `## Decisions` section, dated (e.g. `### YYYY-MM-DD — short title`)
   - **R&D operating rules, payroll/compliance procedures, grant-level learnings** → `dashboards/nexwave-rd.md` under the relevant section (e.g. Payroll → `### Operating rules (learnt)`)
   - **Cross-cutting engineering or workflow patterns** → the most relevant dashboard under a `## Decisions` or `## Rules` section
   - The daily `## Notes` section is **only for ephemeral session observations** (what I tried, what surprised me today) — anything a future agent or future-Ryo needs to find later belongs in a project or dashboard, not buried in a daily note.
   - If the decision creates an action item, make a task file as well.
5. Prompt: "Any new action items from today?" — for each: create a task file in `tasks/open/`. Do **not** duplicate the action into the daily note.

## Task-Based Progress Tracking

Create session tasks at skill start:

```
TaskCreate: "Create daily note" — activeForm: "Creating today's note..."
TaskCreate: "Surface sprint context" — activeForm: "Reading active sprints..."
TaskCreate: "Surface today's tasks" — activeForm: "Scanning tasks/open/..."
TaskCreate: "Surface Gmail highlights" — activeForm: "Scanning Gmail last 7 days..."
TaskCreate: "Update LinkedIn news feed" — activeForm: "Scanning Google Alerts..."
TaskCreate: "Process personal tool tips" — activeForm: "Scanning personal Gmail..."
TaskCreate: "Present overview and suggested plan" — activeForm: "Building today's briefing..."
TaskCreate: "Write confirmed plan to note" — activeForm: "Writing today's plan..."
```

Run sequentially. Mark each `in_progress` then `completed` as you go.

## Integration

- `/weekly` — reads daily notes to compile sprint summary
- `/session-update` — end-of-session log (use instead of /daily evening for coding sessions)
- `/obsidian-task-table` — create new tasks surfaced during daily review
