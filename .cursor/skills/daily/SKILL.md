---
name: daily
description: Create today's daily note and run morning, midday, or evening routines. Surfaces active sprint tasks, blocked items, and project priorities for Ryo's founder/GP workflow.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
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

## Morning Routine

### Step 1: Create today's note

Check if `daily/YYYY-MM-DD.md` exists. If yes, open it. If no, create from template below.

### Step 2: Surface sprint context

Read all files in `sprints/active/`. For each sprint where `status: active`:
- Extract `id`, `goal`, `end`, `repos`
- Calculate days remaining to `end`
- Flag sprints ending within 3 days

Display as:

```
Active sprints:
  2026-04-sprint-1 — Referral Images paid model (ends Apr 18, 6 days)
  2026-04-rd-sprint-1 — [goal] (ends [date], N days)
```

### Step 3: Surface today's tasks

Read all files in `tasks/open/`. Filter where `due = today` OR `status: in-progress`. Group by repo. Exclude `status: done`.

Display as:

```
Today's tasks:
  clinicpro-saas:
    - [title] (saas-20260407-001) — due today
  nexwave-rd:
    - [title] (rd-20260401-002) — in-progress
```

### Step 4: Surface blockers

Read `tasks/open/`. Filter where `status: blocked`. List them.

### Step 5: Interactive prompts

Ask (one at a time):
- "What's the ONE thing that would make today successful?"
- "Any meetings or commitments to block time for?"
- "Anything blocked that needs unblocking today?"

## Daily Note Template

```markdown
---
date: YYYY-MM-DD
day: Monday
---

# YYYY-MM-DD

## Focus
> 

## Active Sprints
| Sprint | Goal | Ends | Days left |
|--------|------|------|-----------|

## Today's Tasks
### clinicpro-saas
- 

### clinicpro-medtech
- 

### nexwave-rd
- 

### gp-fellowship
- 

## Blockers
- 

## Notes

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
2. For each task marked done today, confirm task file in `tasks/open/` has `status: done`
3. Scan `inbox/` for unprocessed items — flag for tomorrow
4. Prompt: "Any decisions or learnings worth capturing?"

## Task-Based Progress Tracking

Create session tasks at skill start:

```
TaskCreate: "Create daily note" — activeForm: "Creating today's note..."
TaskCreate: "Surface sprint context" — activeForm: "Reading active sprints..."
TaskCreate: "Surface today's tasks" — activeForm: "Scanning tasks/open/..."
TaskCreate: "Morning prompts" — activeForm: "Running morning prompts..."
```

Run sequentially. Mark each `in_progress` then `completed` as you go.

## Integration

- `/weekly` — reads daily notes to compile sprint summary
- `/session-update` — end-of-session log (use instead of /daily evening for coding sessions)
- `/obsidian-task-table` — create new tasks surfaced during daily review
