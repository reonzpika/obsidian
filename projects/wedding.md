---
id: wedding
status: active
type: side-project
title: "Wedding"
description: "Shinto shrine wedding, Kora Taisha, Kurume, 14 Sep 2026."
phase: "Venue booked. Awaiting replies from JUNO and Wedding Select on pricing."
dashboard: personal
---

## Description

Shinto shrine wedding (神前式) at 高良大社 (Kora Taisha), Kurume, Fukuoka. Ceremony only -- already legally married in NZ. Date: Monday 14 September 2026, 14:00.

**Venue: 高良大社**
- Contact: 田中友也 (Tanaka), 権禰宜, office@kourataisya.or.jp
- Ceremony fee: 50,000 yen cash on the day
- Duration: 30-40 min, main hall
- External photographer allowed
- No changing rooms or hair/makeup on site -- dressing venue needed nearby
- 19 guests (12 groom, 7 bride)
- Application form sent 26 Mar 2026. Awaiting written confirmation.

**Styling vendor: JUNO / Dress The Life (Fuchigami Fines)**
- Contact: 松下雪穂 (Matsushita Yukiho), y-matsushita@ffines.jp, +81-80-4922-5978
- Covers: kimono, dressing, hair/makeup, photographer, on-day planner (all-in-one)
- No weekend surcharge
- Plan table sent by Matsushita on 6 Mar 2026. Not yet reviewed or contracted.
- Last contact: 18 Mar 2026 (Ryo confirmed date, said would review plan)

**Also contacting: Wedding Select (門井)**
- Contact: 門井, info@wedding-select.wedding, tel 092-522-1110
- Plan: 挙式撮影付き神社挙式プラン, ¥88,000 (kimono, H&M, dressing, photographer 150+ shots, attendant)
- Kora Taisha experience: confirmed
- No weekend surcharge
- Previously declined 18 Mar 2026, re-engaged 27 Apr 2026. Awaiting reply.

## Open questions / blockers

| Question | Sent | Waiting on |
|---|---|---|
| Written booking confirmation for 14 Sep slot | 26 Mar 2026 | 高良大社 (Tanaka) |
| Does ¥99,000 Fukuoka campaign apply to our booking? | 27 Apr 2026 | JUNO (Matsushita) |
| Can Wedding Select accommodate 14 Sep, what are next steps? | 27 Apr 2026 | Wedding Select (門井) |
| Dressing venue near Kora Taisha (no on-site changing rooms) | -- | To be sourced once vendor confirmed |

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
  .where(p => p.project === "wedding" && p.status !== "done")
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
