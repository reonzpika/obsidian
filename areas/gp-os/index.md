# Dashboard — GP OS

Operating system for clinical work as a GP. Fellowship, recertification, clinical workflow, audits, CME.

---

## Projects

```dataviewjs
const active = dv.pages('"areas/gp-os/projects"')
  .where(p => p.dashboard == "gp-os" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"areas/gp-os/tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"areas/gp-os/projects"').where(p => p.dashboard == "gp-os" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

