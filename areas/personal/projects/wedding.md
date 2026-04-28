---
id: wedding
status: active
type: side-project
title: "Wedding"
description: "Shinto shrine wedding, Kora Taisha, Kurume, 14 Sep 2026."
phase: "Both vendors confirmed availability. Schedule meetings with JUNO and Wedding Select."
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
- Plan table sent by Matsushita on 6 Mar 2026.
- 27 Apr 2026: Ryo re-engaged with date (14 Sep), outfit preferences (白無垢/紋付袴), and asked about ¥99,000 Fukuoka campaign.
- 27 Apr 2026: Matsushita accepted and requested online or in-person meeting (JUNO Tenjin store), approx 1.5 hrs. ¥99,000 campaign question to be discussed in meeting.

**Also contacting: Wedding Select (門井)**
- Contact: 門井, info@wedding-select.wedding, tel 092-522-1110
- Plan: 挙式撮影付き神社挙式プラン, ¥88,000 (kimono, H&M, dressing, photographer 150+ shots, attendant)
- Kora Taisha experience: confirmed
- No weekend surcharge
- Previously declined 18 Mar 2026, re-engaged 27 Apr 2026.
- 27 Apr 2026: 門井 confirmed availability for 14 Sep. Requested online meeting (Zoom/Google Meet). Hours 10:30-19:00 JST, flexible outside hours if needed.

## Open questions / blockers

| Question | Sent | Waiting on |
|---|---|---|
| Written booking confirmation for 14 Sep slot | 26 Mar 2026 | 高良大社 (Tanaka) |
| Schedule meeting: JUNO online or in-person (1.5 hrs) | -- | Ryo to propose times |
| Schedule meeting: Wedding Select online (Zoom/Google Meet) | -- | Ryo to propose times |
| Does ¥99,000 Fukuoka campaign apply? | 27 Apr 2026 | Discuss at JUNO meeting |
| Dressing venue near Kora Taisha (no on-site changing rooms) | -- | After vendor confirmed |

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
