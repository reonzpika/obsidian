# Dashboard — Personal

Personal life projects: wedding, family, home, travel.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "personal" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "personal" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

**2026-04-27:** Wedding -- reconstructed full vendor picture from Gmail. Venue confirmed (高良大社, 14 Sep 2026). Styling vendor undecided: re-engaged Wedding Select (¥88,000) and sent pricing enquiry to JUNO (¥187,000, campaign TBC). 7 tasks created. gws personal auth fixed.

