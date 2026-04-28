---
id: personal-admin
title: "Personal Admin"
status: active
type: side-project
description: "Household bills, vehicle, insurance, and personal financial obligations for 7A Vienna Place, Birkenhead."
phase: "Clearing backlog: rego, MyACC, Pulse Energy overdue, ASB activation."
dashboard: personal
---

## Description

Admin for Ryo's personal life: property bills at 7A Vienna Place, Birkenhead, vehicle, insurance, and government obligations.

**Property: 7A Vienna Place, Birkenhead**
- Electricity: Pulse Energy, account 9088881339
- Water: Watercare, account 5514389-01
- Broadband: Skinny
- Electricity also: Electric Kiwi (check if this is a separate meter or switching context)

**Vehicle**
- Toyota, plate QZC52
- Insurance: AA Insurance, policy AMV800207045 (Comprehensive Car, from 21 Jan 2026)

**Key contacts**
- NZTA: nzta.govt.nz (rego renewal online)
- MyACC for Business: myacc.co.nz/business (NexWave invitation expires 21 May 2026)
- RNZCGP credit control: creditcontrol@rnzcgp.org.nz (Training Boost Refund)
- ASB: asb.co.nz (new account opened 22 Apr 2026, needs activation)

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
const all = dv.pages('"areas/personal/tasks/open"')
  .where(p => p.project === "personal-admin" && p.status !== "done")
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
