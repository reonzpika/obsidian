---
name: monthly
description: Monthly review and planning for NexWave/ClinicPro. Rolls up weekly reviews, checks project health across all streams, and plans next month's focus. Keeps R&D stream (MBIE reporting) separate from commercial. Run at end of month.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
user-invocable: true
---

# Monthly Review Skill

Facilitates Ryo's monthly review. Rolls up task progress across all projects, assesses project health across all repos, identifies patterns, and sets next month's focus. Keeps R&D and commercial streams strictly separated for MBIE reporting.

## Usage

```
/monthly         # Full monthly review
/monthly rd      # R&D stream only (MBIE reporting)
/monthly saas    # Commercial stream only
```

## Vault paths

- Open tasks: `tasks/open/*.md`
- Done tasks: `tasks/done/*.md`
- Projects: `projects/*.md`
- Logs: `logs/*.md` (weekly reviews at `logs/YYYY-WNN-review.md`, session logs at `logs/YYYY-WNN.md`)
- Review output: `reviews/monthly/YYYY-MM.md`

## R&D isolation rule

**Critical:** `nexwave-rd` tasks and outputs must be reviewed in a fully separate section. MBIE audits R&D activity independently of commercial work. The R&D section of the monthly review is a source of truth for programme progress reporting to Lisa (MBIE) and Ting (Programme Manager).

## Review Process

### Phase 1: Collect monthly data

**Projects:**
- Read `projects/*.md`
- Note `id`, `title`, `status`, `phase`, `dashboard`, `type` for each

**Tasks done this month:**
- Read `tasks/done/*.md`, filter by file mtime or `created` within the month

**Weekly reviews:**
- Glob `logs/*-review.md` — read all weekly review files from this month
- Also read session log files `logs/YYYY-WNN.md` for supplementary context
- Extract: wins, blockers, decisions

**Projects:**
- Read all `projects/*.md`
- Note `status` and `type` (product / rd / training)

Create session task:
```
TaskCreate: "Phase 1: Collect", activeForm: "Collecting project and task data for the month..."
```

### Phase 2: Reflect

**Commercial stream (clinicpro-saas + clinicpro-medtech):**
- Sprints completed: goals met or not?
- Tasks done vs tasks left open at month end
- Key decisions made
- Blockers that recurred across multiple weeks
- Project status changes

**R&D stream (nexwave-rd, MBIE isolated):**
- Sprints completed against R&D objectives (Obj 1-4)
- Research outputs: reports, datasets, experiments, findings
- Programme timeline health: are we on track for the MBIE reporting schedule?
- Ting coordination: any blockers or items needing escalation to Ting?
- Any items to surface to Lisa (MBIE)?

**gp-fellowship:**
- Fellowship task progress against milestones
- Any assessments due or completed

**Patterns across the month:**
- Recurring blockers (flag systemic issues)
- Repos that stalled (no tasks completed)
- Over-committed projects (too many tasks, no completions)

**Ask Ryo (one at a time):**
1. "What were the 3 biggest wins this month?"
2. "What kept recurring as a blocker?"
3. "Which project needs the most attention next month?"
4. "Any R&D programme risks to flag for Ting or MBIE?"

Create session task:
```
TaskCreate: "Phase 2: Reflect", blocked by Phase 1
```

### Phase 3: Plan next month

1. For each project in `projects/*.md`: does the `phase:` field need updating for next month?
2. Identify tasks to carry forward or create for next month's focus
3. Set next month's ONE focus per stream (commercial / R&D)
4. Flag any external deadlines: MBIE reports, Ting check-ins, medtech partner reviews

**Ask Ryo:**
- "What's the ONE commercial focus for next month?"
- "What's the ONE R&D focus for next month?"
- "Any project phases to update or tasks to carry forward?"

Create session task:
```
TaskCreate: "Phase 3: Plan", blocked by Phase 2
```

## Output Format

Save to `reviews/monthly/YYYY-MM.md`:

```markdown
---
month: YYYY-MM
---

# Monthly Review: [Month YYYY]

## Summary
- Tasks completed: N (commercial), N (R&D)
- Projects active: N

---

## Commercial Stream

### Projects
| Project | Phase | Tasks done | Status | Notes |
|---------|-------|------------|--------|-------|

### Wins
1. 
2. 
3. 

### Blockers / Patterns
- 

### Decisions
- 

---

## R&D Stream (nexwave-rd, MBIE isolated)

### Projects
| Project | Phase | Tasks done | Status | Notes |
|---------|-------|------------|--------|-------|

### Research Outputs
- Reports/documents produced:
- Datasets or experiments run:
- Key findings:

### Programme Timeline Health
- On track: yes / at risk
- Notes for Ting:
- Notes for MBIE/Lisa:

---

## GP Fellowship

### Progress
- 

---

## Next Month

### Commercial focus
> 

### R&D focus
> 

### Project phase updates
- 

### External deadlines
| Date | Item | Owner |
|------|------|-------|
```

## Integration

- `/weekly`: weekly reviews feed this rollup
- `/obsidian-task-table`: create tasks for next month's priorities
- `/session-update`: log the review session itself
