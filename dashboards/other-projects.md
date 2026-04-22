---
id: other-projects
status: active
type: side-project
---

# Other Projects

Personal, family, and training projects outside of ClinicPro and NexWave R&D. Maintained by Ryo and Ting.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "other-projects" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "other-projects" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

### Week of 2026-04-14

**miozuki**
- Two-track collaboration workflow shipped: Ting works direct on master, Ryo on feature branches with Vercel previews. `.vscode/tasks.json` (dev server auto-start), `.vscode/settings.json` (one-click auto-push commit), `Ctrl+Alt+P` publish shortcut, `TING-GUIDE.md`, `CLAUDE.md` workflow note, `docs/ting-laptop-setup.md` checklist
- In-person setup on Ting's laptop completed 15 Apr — miozuki-20260415-001 closed
- Site audit cycle run: first audit results filed, audit scripts added to repo, Instagram proxy, Klaviyo subscribe + email popup a11y + contact form fixes shipped
- LCP image perf pass: priority + responsive `sizes` added; audit re-run against fixes

**linkedin (automation go-live, Apr 19)**
- First post on new strategy scheduled: ManageMyHealth patient portal login UX (Pillar A, text), publishes Tue 21 Apr 10:00 NZST
- Golden Hour Windows automation shipped and verified: wake timers enabled on AC + DC; auth session valid; schedule registry + task actions verified end-to-end
- Bug fixed: `scripts/ensure_claude_desktop.bat` Claude Desktop MSIX/UWP package path resolved

**linkedin (strategy pivot, Apr 16-17)**
- Full LinkedIn strategy overhaul: Pillar A "What Works in NZ Primary Care" (55%) + Pillar B "What's Changing in NZ Primary Care" (40%)
- Cadence: 3x/week (1 carousel Tue + 2 text Thu/Sat) + fortnightly "The GP Builder" newsletter
- Knowledge files updated to v4.0; Golden Hour system redesigned with core_targets.json

### Week of 2026-04-21

**vault restructure**
- Sprint layer eliminated: `sprints/active/` removed from vault, replaced with `phase:` on projects and `milestone:` on tasks
- GP Fellowship wikilink ambiguity resolved: `projects/gp-fellowship.md` renamed to `projects/fellowship-application.md` (`id: fellowship-application`); 15 gpf-* task files updated
- `dashboards/gp-fellowship.md` deleted; GP Fellowship project absorbed into Other Projects dashboard
- `dashboards/side-projects.md` renamed to `dashboards/other-projects.md`; all Dataview queries and project frontmatter updated
- Heron project moved from Partnerships to Other Projects (`dashboard: other-projects`)
- `home.md` nav and section headers updated: GP Fellowship removed, Side Projects → Other Projects
- All skill files updated (daily, weekly, monthly, obsidian, obsidian-task-table, adopt): sprint references removed, project/phase/milestone pattern adopted throughout
- Vault `CLAUDE.md` updated: hierarchy rules, task schema, project schema, gotchas
