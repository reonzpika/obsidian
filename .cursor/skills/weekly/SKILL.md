---
name: weekly
description: Weekly sprint review and planning for NexWave/ClinicPro. Rolls up sprint progress, surfaces wins/blockers, and plans the next sprint. Run on Fridays or at end of a sprint cycle. Keeps R&D and commercial streams separate.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
user-invocable: true
---

# Weekly Review Skill

Facilitates Ryo's weekly sprint review. Rolls up task progress across all active sprints, identifies blockers, surfaces wins, and plans the next sprint cycle.

## Usage

```
/weekly        # Full review for current week
/weekly rd     # R&D stream only
/weekly saas   # Commercial stream only
```

## Vault paths

- Active sprints: `sprints/active/*.md`
- Archived sprints: `sprints/archive/*.md`
- Open tasks: `tasks/open/*.md`
- Done tasks: `tasks/done/*.md`
- Projects: `projects/*.md`
- Daily notes: `daily/*.md`
- Review output: `reviews/weekly/YYYY-MM-DD.md`

## R&D isolation rule

**Critical:** `nexwave-rd` tasks and sprints must always be reviewed in a separate section from commercial tasks. MBIE audits R&D activity independently. Never mix R&D progress with clinicpro-saas or clinicpro-medtech in the same summary table.

## Review Process

### Phase 1: Collect (read-only)

**Tasks — open:**
- Read all `tasks/open/*.md`
- Group by `repo`
- Note `status` (open / in-progress / blocked) and `due`

**Tasks — done this week:**
- Read `tasks/done/*.md`
- Filter where `created` or file mtime is within last 7 days

**Sprints:**
- Read all `sprints/active/*.md`
- For each: extract `id`, `goal`, `start`, `end`, `repos`, `projects`
- Calculate % of sprint elapsed (days elapsed / total days)
- Flag sprints ending within 3 days

**Daily notes:**
- Read `daily/*.md` for the past 7 days (if they exist)
- Extract any notes under "Wins", "Challenges", or "Tomorrow's priority"

Create session tasks:
```
TaskCreate: "Phase 1: Collect" — activeForm: "Reading tasks, sprints, and daily notes..."
```

### Phase 2: Reflect

**Per sprint, compute:**
- Tasks done this week (count)
- Tasks still open (count)
- Tasks blocked (count + reason)
- Sprint % time elapsed vs tasks remaining — flag if misaligned

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

1. Review sprints ending soon — does the sprint need closing or extending?
2. Check `projects/*.md` for each active project: any status changes?
3. Identify tasks to carry forward, tasks to drop
4. Ask: "What sprint or tasks should we create for next week?"

For each new task identified, create it via `/obsidian-task-table` or note it in the review output.

Create session task:
```
TaskCreate: "Phase 3: Plan" — blocked by Phase 2
```

## Output Format

Save to `reviews/weekly/YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
week: YYYY-WNN
---

# Weekly Review: YYYY-MM-DD

## Sprint Status

### Commercial
| Sprint | Goal | Elapsed | Tasks done | Open | Blocked |
|--------|------|---------|------------|------|---------|
| [id] | [goal] | N% | N | N | N |

### R&D (nexwave-rd — MBIE isolated)
| Sprint | Goal | Elapsed | Tasks done | Open | Blocked |
|--------|------|---------|------------|------|---------|
| [id] | [goal] | N% | N | N | N |

## Wins
1. 
2. 
3. 

## Blockers
| Blocker | Sprint | Owner | Next action |
|---------|--------|-------|-------------|

## Decisions Made
- 

## Next Week

### ONE Big Thing
> 

### Key tasks to create or carry forward
- 

### Sprints to close or extend
- 
```

## Best Practices

- Run every Friday or at sprint boundary
- R&D review must stay isolated — never merge into commercial summary
- If a sprint is > 80% elapsed with > 50% tasks open, flag it explicitly
- Wins should be specific and concrete — not "made progress on X"

## Integration

- `/daily` — daily notes feed Phase 1 context
- `/monthly` — weekly reviews feed monthly rollup
- `/session-update` — use during the week to log session progress
- `/obsidian-task-table` — create new tasks identified during planning
- `/calendar-sync` — sync sprint timelines after any sprint changes
