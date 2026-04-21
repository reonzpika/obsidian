---
id: gp-fellowship
status: active
type: training
repo: gp-fellowship
stack: [rnzcgp, gpep3, amp]
title: "GP Fellowship"
description: "RNZCGP Fellowship application. Final stage: Assessment Visit."
phase: "Fellowship audit and application submission"
dashboard: gp-fellowship
---

## Description

RNZCGP Fellowship application and assessment process for Dr Ryotaro Eguchi (College ID: 66153). GPEP 3+ training requirements completed 16 Feb 2026. Now at final stage: submit application package to obtain Fellowship Assessment Visit allocation.

## Key details

- MCNZ number: 69327
- College ID: 66153

## Key contacts

- Fellowship enquiries: fellowship@rnzcgp.org.nz
- GPEP programme: gpep2@rnzcgp.org.nz
- Accounts (fees): via College main line +64 4 496 5999

## Submission package required

All three items must be received before an assessor is allocated:

1. Fellowship Application Form (fillable PDF — 7 pages, must be returned as PDF not printed/scanned)
2. Clinical Record Review (Module 1 check + Module 2 audit of 10 records)
3. Up-to-date CV
4. Hauora Māori Reflection (highly recommended — submit with the above)

## Key requirements to meet

- Practice must hold Foundation Standard accreditation (minimum Cornerstone Bronze, or pre-approved by College)
- Must have worked at the practice for minimum 3 months FTE in the 9 months preceding the visit
- Clinical Record Review must be completed within 6 months of the Fellowship visit date
- Must be in good financial standing with the College (no outstanding fees)
- Must be actively participating in AMP (CPD team will enrol separately)

## AMP (Te Whanake Annual Maintenance Programme)

- **Enrolled:** 17 February 2026 (auto-enrolled by College; email from Aimee, CPD@rnzcgp.org.nz)
- **Duration:** 6 months from enrolment (to ~17 August 2026)
- **Hard gate:** "Fellowship candidates must be actively engaged in their recertification programme to receive their Fellowship Assessment outcome" — non-compliance blocks result
- **Components required** (pro-rated to time enrolled): CME 4cr, PO 4cr, RP 4cr, CSE 4cr, CR (collegial meetings every 2 months)
- **Goal-setting:** required at enrolment start (Feb 17); overdue as of Apr 13 — complete via Te Whanake AMP dashboard this weekend
- **Collegial relationship:** first meeting due by 17 April 2026; subsequent meetings every 2 months — task gpf-20260413-001
- **Dashboard:** Te Whanake AMP (separate from Te Ara platform)

## Tasks

```dataviewjs
const mb = app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api;
const lifecycle = this.component;
const statusOpts = [
  { name: 'option', value: ['open'] },
  { name: 'option', value: ['in-progress'] },
  { name: 'option', value: ['blocked'] },
  { name: 'option', value: ['done'] }
];
const priorityOpts = [
  { name: 'option', value: ['high'] },
  { name: 'option', value: ['medium'] },
  { name: 'option', value: ['low'] }
];
function statusSelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('status', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--status'] }, ...statusOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function prioritySelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('priority', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--priority'] }, ...priorityOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
const all = dv.pages('"tasks/open"')
  .where(p => p.project === "gp-fellowship" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const groups = {};
const unassigned = [];
for (let p of all) {
  const m = p.milestone ?? "";
  if (m) {
    if (!groups[m]) groups[m] = [];
    groups[m].push(p);
  } else {
    unassigned.push(p);
  }
}
const render = (tasks) => dv.table(
  ['Task', 'Status', 'Priority', 'Due'],
  tasks.map(p => [dv.fileLink(p.file.path, false, p.title || p.file.name), statusSelect(p.file.path), prioritySelect(p.file.path), p.due])
);
for (const [m, tasks] of Object.entries(groups)) {
  dv.paragraph(`**${m}**`);
  render(tasks);
}
if (unassigned.length > 0) {
  if (Object.keys(groups).length > 0) dv.paragraph("**Backlog**");
  render(unassigned);
}
```
