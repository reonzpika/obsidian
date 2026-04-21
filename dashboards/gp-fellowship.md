# Dashboard — GP Fellowship

RNZCGP Fellowship application and assessment. College ID: 66153. Requirements completed: 16 Feb 2026.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "gp-fellowship" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
```

---

## Quick Links

| | |
|--|--|
| **Project** | [[gp-fellowship]] |
| **Assessment guide** | [[fellowship-assessment-guide]] |

---

## Weekly Progress Log

### Week of 2026-04-07

- AMP enrolment confirmed: auto-enrolled 17 February 2026; active engagement is a hard gate for receiving Fellowship Assessment outcome
- AMP goal-setting identified as overdue (required at enrolment start Feb 17); to be completed this weekend
- First AMP collegial relationship meeting due by 17 April (2 months from enrolment); scheduled for next week — task gpf-20260413-001
- Fellowship Assessment Visit forms located in obsidian/temp/ and emailed to ryo@clinicpro.co.nz: Clinical Record Review Audit Checklist and Details for Fellowship Assessment Visit Form
- CRR Module 1 and Module 2 task deadlines rescheduled to 18 April
- gpf-20260330-001 (financial standing) and gpf-20260330-011 (AI scribe policy) deprioritised to Apr 30 — not on critical path for submission
