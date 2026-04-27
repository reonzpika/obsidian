---
name: weekly
description: Weekly project review and planning for NexWave/ClinicPro. Rolls up task progress across projects and milestones, surfaces wins/blockers, and plans the next week. Run on Fridays. Keeps R&D and commercial streams separate.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
user-invocable: true
---

# Weekly Review Skill

Facilitates Ryo's weekly project review. Rolls up task progress across all active projects, identifies blockers, surfaces wins, and plans the next week.

## Usage

```
/weekly        # Full review for current week
/weekly rd     # R&D stream only
/weekly saas   # Commercial stream only
```

## Vault paths

- Projects: `projects/*.md` (includes `phase:` field for current focus area)
- Open tasks: `tasks/open/*.md`
- Done tasks: `tasks/done/*.md`
- Weekly planning file: `weekly.md`
- Logs: `logs/*.md`
- Review output: `logs/YYYY-WNN-review.md`

## R&D isolation rule

**Critical:** `nexwave-rd` tasks must always be reviewed in a separate section from commercial tasks. MBIE audits R&D activity independently. Never mix R&D progress with clinicpro-saas or clinicpro-medtech in the same summary table.

## Review Process

### Phase 1: Collect (read-only)

**Tasks — open:**
- Read all `tasks/open/*.md`
- Group by `repo`
- Note `status` (open / in-progress / blocked) and `due`

**Tasks — done this week:**
- Read `tasks/done/*.md`
- Filter where `created` or file mtime is within last 7 days

**Weekly planning file:**
- Read `weekly.md`
- Extract: briefing (stream status), week focus, day sections (focus, urgent, blockers per day)

Create session tasks:
```
TaskCreate: "Phase 1: Collect" — activeForm: "Reading projects, tasks, and daily notes..."
```

### Phase 2: Reflect

**Per project, compute:**
- Tasks done this week (count)
- Tasks still open (count), grouped by milestone
- Tasks blocked (count + reason)

**Per repo stream:**

Commercial (clinicpro-saas + clinicpro-medtech + gp-fellowship):
- What shipped or progressed this week?
- What's blocked and needs unblocking?
- Any key decisions made?

R&D (nexwave-rd only):
- Sprint progress against R&D objective
- MBIE-relevant outputs: reports, data, experiments
- Any blockers impacting the programme timeline?

**Ask Ryo (one at a time):**
1. "What were your top 3 wins this week?" (commercial and R&D separately if needed)
2. "What were the main blockers or frustrations?"
3. "What's the ONE big thing for next week?"

Create session task:
```
TaskCreate: "Phase 2: Reflect" — blocked by Phase 1
```

### Phase 3: Plan

1. Review each active project's `phase:` field — does it need updating?
2. Check `projects/*.md` for each active project: any status changes?
3. Identify tasks to carry forward, tasks to drop, and new milestones to set
4. Ask: "What tasks or milestones should we create for next week?"

For each new task identified, create it via `/obsidian-task-table` or note it in the review output.

Create session task:
```
TaskCreate: "Phase 3: Plan" — blocked by Phase 2
```

## Output Format

Save to `logs/YYYY-WNN-review.md`:

```markdown
---
date: YYYY-MM-DD
week: YYYY-WNN
---

# Weekly Review: YYYY-MM-DD

## Project Status

### Commercial
| Project | Phase | Tasks done | Open | Blocked |
|---------|-------|------------|------|---------|
| [name] | [phase] | N | N | N |

### R&D (nexwave-rd — MBIE isolated)
| Project | Phase | Tasks done | Open | Blocked |
|---------|-------|------------|------|---------|
| [name] | [phase] | N | N | N |

## Wins
1. 
2. 
3. 

## Blockers
| Blocker | Project | Owner | Next action |
|---------|---------|-------|-------------|

## Decisions Made
- 

## Next Week

### ONE Big Thing
> 

### Key tasks to create or carry forward
- 

### Project phases to update
- 
```

## Best Practices

- Run every Friday
- R&D review must stay isolated — never merge into commercial summary
- If a project has > 50% tasks open from the previous week, flag it explicitly
- Wins should be specific and concrete — not "made progress on X"

## Archive and Reset weekly.md

After saving the review to `logs/YYYY-WNN-review.md`:

1. Read current `weekly.md`.
2. Append the day sections from `weekly.md` (everything after `## Focus this week`) to `logs/YYYY-WNN.md` under a heading `## Weekly planning archive`.
3. Reset `weekly.md` for the new week — overwrite with a blank template:

```markdown
## Briefing
ClinicPro SaaS: — | — | —
ClinicPro Medtech: — | — | —
NexWave R&D: — | — | —
GP Fellowship: — | — | —

## Focus this week
- ClinicPro SaaS:
- ClinicPro Medtech:
- NexWave R&D:
- GP Fellowship:
```

Confirm: `weekly.md reset for week YYYY-WNN+1`

---

## Integration

- `/daily` — updates weekly.md; Phase 1 reads it for context
- `/monthly` — reads logs/ for weekly review context
- `/session-update` — use during the week to log session progress
- `/obsidian-task-table` — create new tasks identified during planning
