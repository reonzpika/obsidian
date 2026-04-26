---
id: linkedin
status: active
type: side-project
---

# LinkedIn

LinkedIn content strategy and automation. Maintained by Ryo.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "linkedin" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "linkedin" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

