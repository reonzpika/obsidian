---
id: clinicpro-capture-integration
status: active
type: partnership
repo: clinicpro-medtech
title: "ClinicPro Capture: Medtech Integration Contract"
description: "Commission-based integration agreement covering Capture direct sales via Medtech channel. NZ and AU."
phase: "Awaiting Medtech team decision on 15% commission"
dashboard: clinicpro-medtech
---

## Overview

Commission-based partnership with Medtech NZ. Alex Cauble-Chantrenne is the main contact. ClinicPro earns commission on Capture direct sales (D2C via Medtech channel), covering both NZ and AU markets.

Kept strictly separate from the AU bundle deal ([[clinicpro-capture-au-bundle]]). Medtech may attempt to link the two contracts; refuse linkage.

**Product context**: [[clinicpro-capture]]

## 22 April 2026 meeting outcomes

**Alex (NZ):** Clarified the 15% figure at the meeting (asked for the number, not a confirmation). Team decision still pending. NZ deal not agreed. PIA/pentest timeline and reporting cadence not confirmed.

## NZ + AU Integration Contract — Alex Cauble-Chantrenne (Medtech NZ)

**Strategy and pricing analysis**: [[clinicpro-capture-medtech-integration-strategy]]

Draft received from Alex 13 April 2026. Schedule 1 confirmed:

- Commencement Date: 18 March 2026
- Initial Term: 36 months (expires 18 March 2029)
- Fee structure (draft): $10–$60/month per Active Facility by enrolment tier — being renegotiated
- Permitted Purposes: direct image service only (Base + Portal without Confidential Scope + ALEX Apps)
- Software: Medtech Artia and Medtech Evolution

**Commercial position (confirmed 19 April 2026):**

- Opening ask: 15% flat commission on Gross Revenue. Simplified from earlier 10/15% self-referred / Medtech-referred split (14 April email), consolidated on 16 April call.
- Fallback: 20% flat commission.
- Walkaway: above 20%.
- Scope: both NZ and AU direct sales (revised from 14 April NZ-only position).
- PIA/pentest timeline: 6 months from go-live (not draft's 3 months).

Alex signalled personally on 16 April call that 30% was always "too much internally" and took 15% back to her team. Scope-revision email sent to Alex 19 April on existing thread (19cdf07cdcd3c13b) pulling back NZ-only line, keeping integration contract separate from AU bundle. 15% not re-mentioned in scope email — Alex already in team discussion.

Non-negotiables (full list in strategy doc):
1. Explicit NZ + AU geographic scope
2. Double-dipping carve-out (bundle practices excluded from commission until they convert to direct)
3. WHT on AU-sourced commission (services fee restructure, same as AU bundle)
4. Scope locked to ClinicPro Capture (future tools separate)
5. No exclusivity on ClinicPro side
6. Termination + integration IP with 6-month wind-down
7. PIA/pentest at 6 months from go-live

Tracked in task medtech-20260414-001.

## Open questions

| # | Question | Status |
|---|---|---|
| Q1 | Does Medtech team accept 15% flat commission on NZ + AU direct sales? | Alex asked for clarification on the figure at 22 Apr meeting; team decision still pending. |
| Q4 | Reporting cadence for commission (quarterly acceptable, monthly burdensome) | Not discussed 22 Apr. To confirm next meeting. |

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
const all = dv.pages('"areas/clinicpro-medtech/tasks/open"')
  .where(p => p.project === "clinicpro-capture-integration" && p.status !== "done")
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
