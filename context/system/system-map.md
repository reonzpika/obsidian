# System Map

Single reference for how the vault connects. For Ryo and AI equally.

---

## File hierarchy

```
home.md                     Starting point. Portfolio summary. No detail.
dashboards/*.md             Stream index. Project list, current sprint. No history.
projects/*.md               Project detail. Task table. Current focus.
tasks/open/*.md             Single task. Frontmatter + notes only.
tasks/done/*.md             Completed tasks. Archive only.
weekly.md                   Planning only. Reset each Monday.
monthly.md                  Planning only. Written once per month.
logs/YYYY-WNN.md            Session logs. Grows freely. Not for orientation.
context/system/             System reference docs (this folder).
context/{stream}-context/   Stream-specific reference material.
inbox/                      Unreviewed AI output. Nothing leaves without Ryo approval.
```

No sprints folder. Sprint concept removed 2026-04-27.

---

## Navigation rules

- Start at `home.md`. Always.
- AI reads `home.md` then the relevant `dashboards/*.md` to orient. No further unless needed.
- Detail lives in `projects/`. Never in `dashboards/` or `home.md`.
- History and session logs live in `logs/`. Never in `dashboards/`.
- AI output lands in `inbox/` first. Ryo reviews. Then moves to final location.
- Planning lives in `weekly.md` and `monthly.md`. These are forward-looking only.

---

## Entry points by task

| Task | Start here |
|---|---|
| Morning orientation | `weekly.md` briefing section |
| Strategic question | Run `/board` first |
| Project detail | `projects/{project}.md` |
| Finding a task | `tasks/open/` |
| Stream overview | `dashboards/{stream}.md` |
| System question | `context/system/` |
| Techstack | `context/stack.md` |
| Repos and folders | `context/repos.md` |
| Skills reference | `context/skills-index.md` |
| Workflow rituals | `context/system/workflow-reference.md` |
| Contacts | `context/people.md` |

---

## How files connect

```
home.md
  └── links to dashboards/*.md
        └── links to projects/*.md
              └── embeds tasks from tasks/open/ (Dataview)
                    └── links to context/{stream}-context/ as needed

weekly.md
  └── updated by /daily (planning sections)
  └── briefing section updated by /session-update

logs/YYYY-WNN.md
  └── session records written by /session-update
  └── not linked from dashboards or home
```

---

## Related docs

- File structural spec: `context/system/file-structure.md`
- Workflow rituals and skill triggers: `context/system/workflow-reference.md`
- System decisions: `context/system/decisions-log.md`
- Techstack: `context/stack.md`
- Skills: `context/skills-index.md`
