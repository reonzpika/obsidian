---
name: monthly
description: Monthly review and planning for NexWave/ClinicPro. Rolls up weekly reviews and sprint completions, checks project health, and plans next month. Keeps R&D stream (MBIE reporting) separate from commercial. Run at end of month.
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
user-invocable: true
---

# Monthly Review Skill

Facilitates Ryo's monthly review. Rolls up sprints completed in the month, assesses project health across all repos, identifies patterns, and sets next month's focus. Keeps R&D and commercial streams strictly separated for MBIE reporting.

## Usage

```
/monthly         # Full monthly review
/monthly rd      # R&D stream only (MBIE reporting)
/monthly saas    # Commercial stream only
```

## Vault paths

- Sprints (active): `sprints/active/*.md`
- Sprints (archived): `sprints/archive/*.md`
- Open tasks: `tasks/open/*.md`
- Done tasks: `tasks/done/*.md`
- Projects: `projects/*.md`
- Weekly reviews: `reviews/weekly/*.md`
- Daily notes: `daily/*.md`
- Review output: `reviews/monthly/YYYY-MM.md`

## R&D isolation rule

**Critical:** `nexwave-rd` sprints, tasks, and outputs must be reviewed in a fully separate section. MBIE audits R&D activity independently of commercial work. The R&D section of the monthly review is a source of truth for programme progress reporting to Lisa (MBIE) and Ting (Programme Manager).

## Review Process

### Phase 1: Collect monthly data

**Sprints completed this month:**
- Read `sprints/archive/*.md`, filter where `end` is within this calendar month
- Read `sprints/active/*.md`, flag any that started this month but are still running

**Tasks done this month:**
- Read `tasks/done/*.md`, filter by file mtime or `created` within the month

**Weekly reviews:**
- Read all `reviews/weekly/*.md` from this month
- Extract: wins, blockers, decisions

**Projects:**
- Read all `projects/*.md`
- Note `status` and `type` (product / rd / training)

Create session task:
```
TaskCreate: "Phase 1: Collect", activeForm: "Collecting sprint and task data for the month..."
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
- Fellowship sprint progress
- Any assessments due or completed

**Patterns across the month:**
- Recurring blockers (flag systemic issues)
- Repos that stalled (no tasks completed)
- Over-committed sprints

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

1. Review sprints still active, do they carry over or need closing?
2. For each project in `projects/*.md`: set next month's focus (one line)
3. Identify any new sprints to create
4. Set next month's ONE focus per stream (commercial / R&D)
5. Flag any external deadlines: MBIE reports, Ting check-ins, medtech partner reviews

**Ask Ryo:**
- "What's the ONE commercial focus for next month?"
- "What's the ONE R&D focus for next month?"
- "Any sprints to close, extend, or create?"

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
- Sprints completed: N (commercial), N (R&D)
- Tasks completed: N (commercial), N (R&D)
- Projects active: N

---

## Commercial Stream

### Sprints
| Sprint | Goal | Outcome |
|--------|------|---------|

### Project Health
| Project | Repo | Status | Notes |
|---------|------|--------|-------|

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

### Sprints
| Sprint | Objective | Outcome |
|--------|-----------|---------|

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

### Sprint progress
- 

---

## Next Month

### Commercial focus
> 

### R&D focus
> 

### Sprints to create
- 

### External deadlines
| Date | Item | Owner |
|------|------|-------|
```

## Integration

- `/weekly`: weekly reviews feed this rollup
- `/calendar-sync`: sync new sprints to Google Calendar after planning
- `/obsidian-task-table`: create tasks for next month's priorities
- `/session-update`: log the review session itself
