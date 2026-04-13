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

### Step 8: Interactive prompts

Ask (one at a time):
- "What's the ONE thing that would make today successful?"
- "Any meetings or commitments to block time for?"
- "Anything blocked that needs unblocking today?"

If any action items emerge from these answers, create task files in `tasks/open/` immediately, then note the task ID in `## Notes`.

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

## Today's Focus
<!-- Reference only — tasks live in tasks/open/. No inline checkboxes. -->
### clinicpro-saas
- 

### clinicpro-medtech
- 

### nexwave-rd
- 

### gp-fellowship
- 

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

1. Review morning task list — what's done, what's not
2. Identify anything to reschedule or drop
3. Check inbox for urgent items
4. Ask: "What's the most important thing for this afternoon?"

## Evening Shutdown

1. Update today's note: fill in Wins, Challenges, Tomorrow's priority
2. For each task completed today: update `status: done` in the task file in `tasks/open/`
3. Scan `inbox/` — for each item, either create a task file or discard. No inbox items should be copied inline into the daily note.
4. Prompt: "Any decisions or learnings worth capturing?" — capture in `## Notes` as free text only. If it creates an action item, make a task file.
5. Prompt: "Any new action items from today?" — for each: create a task file in `tasks/open/`, then note the ID in `## Notes`.

## Task-Based Progress Tracking

Create session tasks at skill start:

```
TaskCreate: "Create daily note" — activeForm: "Creating today's note..."
TaskCreate: "Surface sprint context" — activeForm: "Reading active sprints..."
TaskCreate: "Surface today's tasks" — activeForm: "Scanning tasks/open/..."
TaskCreate: "Surface Gmail highlights" — activeForm: "Scanning Gmail last 7 days..."
TaskCreate: "Morning prompts" — activeForm: "Running morning prompts..."
```

Run sequentially. Mark each `in_progress` then `completed` as you go.

## Integration

- `/weekly` — reads daily notes to compile sprint summary
- `/session-update` — end-of-session log (use instead of /daily evening for coding sessions)
- `/obsidian-task-table` — create new tasks surfaced during daily review
