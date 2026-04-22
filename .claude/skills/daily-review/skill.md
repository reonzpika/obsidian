---
name: daily-review
description: Evening day review — reconstructs today's work across multiple sessions from git history and task state, plans tomorrow's focus, appends Evening Review and Tomorrow sections to today's daily note, then spawns parallel session-update agents for projects with detectable activity.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /daily-review — Evening Day Review

Reconstructs today's work (git history + task state, not conversation context), plans tomorrow's focus, appends results to today's daily note, then spawns parallel session-update agents for projects with detectable activity.

**Vault root:** `C:/Users/reonz/cursor/obsidian/`

---

## Phase 1: Read context (all in parallel)

Fire all reads in a single message. Do not wait between them.

**Today's daily note:**
Read `daily/YYYY-MM-DD.md`. Extract: Focus, Today section (projects, urgent, quick wins), Blockers. If it does not exist, note this and proceed anyway.

**Tasks:**
- Glob `tasks/done/*.md` — read all files. Note id, title, project, status.
- Glob `tasks/open/*.md` — read all files. Note id, title, status, priority, due, project, milestone.

**Git history (today's commits across active repos):**
Run all four git commands in a single Bash call, substituting today's date for `YYYY-MM-DD`:
```bash
git -C C:/Users/reonz/cursor/clinicpro-saas log --after="YYYY-MM-DD 00:00" --oneline 2>/dev/null || echo "clinicpro-saas: no repo"
git -C C:/Users/reonz/cursor/clinicpro-medtech log --after="YYYY-MM-DD 00:00" --oneline 2>/dev/null || echo "clinicpro-medtech: no repo"
git -C C:/Users/reonz/cursor/nexwave-rd log --after="YYYY-MM-DD 00:00" --oneline 2>/dev/null || echo "nexwave-rd: no repo"
git -C C:/Users/reonz/cursor/gp-fellowship log --after="YYYY-MM-DD 00:00" --oneline 2>/dev/null || echo "gp-fellowship: no repo"
```
Also check the vault itself for task file moves:
```bash
git -C C:/Users/reonz/cursor/obsidian log --after="YYYY-MM-DD 00:00" --name-status --format="" -- "tasks/done/*.md" "tasks/open/*.md" 2>/dev/null
```

**Session-update pending queue:**
```bash
cat ~/.claude/session-update-pending.jsonl 2>/dev/null || echo "(empty)"
```
Extract: project IDs and session durations from entries.

**Gmail (received today + sent today):**
```bash
gws gmail users messages list --params '{"userId":"me","q":"newer_than:1d","maxResults":20}'
gws gmail users messages list --params '{"userId":"me","q":"newer_than:1d in:sent","maxResults":10}'
```
Read threads that look actionable: replies from key contacts, unread threads, anything requiring a follow-up. Skip newsletters, Google Alerts, and automated notifications.

**Projects:**
Glob `projects/*.md` — read all. Note id, title, phase, status, dashboard.

---

## Phase 2: Reconstruct the day (silent)

Do not print output. Synthesise from Phase 1 into these buckets:

- **Shipped:** git commits in product repos + task files newly present in `tasks/done/` today. One entry per distinct deliverable or decision.
- **Advanced:** tasks in `tasks/open/` with `status: in-progress` whose project had git commits or pending-queue entries today.
- **Not reached:** task IDs listed in today's daily note Focus/Urgent/Quick wins that have no matching git activity and remain `open`.
- **Comms:** Gmail threads where a reply was sent or a decision was made today.
- **Projects with activity:** union of repos with commits today + project IDs from pending queue + projects whose task files changed in the vault log.

---

## Phase 3: Present day summary

No preamble. No greeting. Format:

```
## [Day], [Date] — Evening Review

**Shipped:**
- [one bullet per deliverable or decision]

**Advanced:**
- [task ID and title, one line each]

**Not reached:**
- [[task-id]] — title

**Comms:**
- [sender, topic, action taken — one line each]
```

Omit **Advanced** if nothing was progressed without shipping. Omit **Not reached** if the day's plan was fully executed. Omit **Comms** if nothing actionable.

End with:
> Anything to add or correct?

Wait for response before proceeding.

---

## Phase 4: Tomorrow planning

After user confirms the summary, surface suggested focus for tomorrow.

Pull from `tasks/open/`:
1. Tasks with `due` = tomorrow or already overdue (highest priority)
2. Tasks with `status: blocked` that have a realistic chance of unblocking
3. `priority: high` open tasks for projects that had activity today

Format:
```
**Suggested focus for tomorrow:**
| Priority | Task | Project | Note |
|----------|------|---------|------|
| high | [[task-id]] title | project-id | due tomorrow |
| high | [[task-id]] title | project-id | overdue |
| medium | [[task-id]] title | project-id | high-priority open |
```

Limit to 5 rows. If the list is longer, truncate and note how many were omitted.

End with:
> What's your focus for tomorrow?

Wait for response.

---

## Phase 5: Append to today's daily note

If `daily/YYYY-MM-DD.md` does not exist, skip silently — do not create it.

Append to the end of the file:

```markdown
## Evening Review

### Today
- [one bullet per shipped item from the confirmed summary]

### Not reached
- [[task-id]] — title

### Tomorrow
- [user's stated focus — verbatim or lightly cleaned, one bullet per distinct goal]
```

Rules:
- Omit the **Not reached** block entirely if nothing was missed.
- Tomorrow bullets: use `[[task-id]]` wikilinks where the user names a specific task. Plain text otherwise.
- No checkboxes (`- [ ]`) anywhere.
- Do not create task files here. Task creation is session-update's job.
- Do not rewrite anything already in the file.

---

## Phase 6: Identify projects for session-update

Collect the union of:
- Repos with git commits today (from Phase 1 git log)
- Project IDs from the pending session queue (from Phase 1 queue read)
- Projects whose task files changed in the vault git log today

Map repo to project ID:
| Repo | Project ID |
|------|------------|
| clinicpro-saas | clinicpro-saas |
| clinicpro-medtech | clinicpro-medtech |
| nexwave-rd | nexwave-rd |
| gp-fellowship | gp-fellowship |

Dedupe. Exclude projects with no detectable activity.

Present:
```
Session-update needed: clinicpro-medtech, clinicpro-saas
Spawn agents for both? (yes / skip / name specific ones)
```

Wait for confirmation.

---

## Phase 7: Spawn session-update agents (parallel)

On confirmation, spawn one Agent per project in a **single message** — all Agent tool calls together, not sequentially.

For each project, use this prompt:

```
Run the session-update skill for [project-id].

Read the skill at: C:/Users/reonz/.claude/skills/session-update/SKILL.md
Follow it exactly. Do not ask which project — it is [project-id]. Start from Step 2.

Context for this project today:
- Git commits: [paste commit lines for this repo from Phase 1]
- Vault task changes: [list task IDs that moved to done or changed status, from Phase 1 vault log]
- Pending queue: [duration and edit count for this project from Phase 1 queue read, or "(none)" if absent]

Vault root: C:/Users/reonz/cursor/obsidian/
```

Wait for all agents to complete, then summarise:
```
session-update complete:
- clinicpro-medtech: tasks done [IDs] | tasks created [IDs] | dashboard updated
- clinicpro-saas: tasks done [IDs] | tasks created [IDs] | dashboard updated
```

---

## Phase 8: Clear the pending queue

After agents complete:
```bash
> ~/.claude/session-update-pending.jsonl
```

Do this silently. Skip if the file does not exist.

---

## Key contacts

| Name / email | Role |
|---|---|
| Ting / tingchou1988@gmail.com | R&D Programme Manager |
| Lisa Pritchard / Lisa.Pritchard@mbie.govt.nz | MBIE Innovation Services |
| Lawrence Peterson / LPeterson@medtechglobal.com | AU market opportunity |
| Alex Cauble-Chantrenne / AChantrenne@medtechglobal.com | Medtech NZ partnership |
| Defne Arzanoglu / alexsupport@medtechglobal.com | Medtech ALEX support |
