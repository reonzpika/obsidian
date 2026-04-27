---
id: founder-os
status: active
type: side-project
---

# Founder OS

The meta-layer of how the business runs. Claude Code configuration, vault structure, memory systems, hooks, skills, and automation.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "founder-os" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "founder-os" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

### Week of 2026-04-27

- Board session: identified 5 structural issues for Vault OS redesign (folder structure, memory system, CLAUDE.md architecture, skills architecture, hooks/automation)
- Research base: 12 founder-os inbox reports reviewed (LYT, MemPalace, memory systems, GStack, agentic patterns, AutoResearch)
- Tasks created: fo-20260427-001 through fo-20260427-005
- Security quick wins: disable-model-invocation on 4 skills (evolve, board, handoff, evolve-queue); haiku subagent model; medtech PHI deny rules; nexwave-rd output dir protection
- Hook quick wins: 3 hooks registered (em-dash detector, bash audit log, session stats)
- Vault integrity: 10 rd-tasks rerouted to correct project IDs; 5 done-task statuses corrected
