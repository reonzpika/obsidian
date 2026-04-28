---
id: founder-os
title: "Founder OS"
status: active
type: side-project
description: "Personal tooling, Claude Code setup, workflow systems, and automation."
phase: "Vault OS redesign: sprint plan complete, execution ready"
dashboard: founder-os
---

## Description

The meta-layer of how the business runs. Claude Code configuration, MCP servers, hooks, skills, keyboard shortcuts, and workflow systems that make everything else faster.

## Architectural decisions (2026-04-28): Vault OS redesign

Sprint plan: `context/vault-os-redesign-sprint-plan.md`

- Vault structure: area-based under `areas/` folder. Each area has index.md, tasks/open, tasks/done, inbox, context, projects, logs, weekly.
- Shared root: daily/, templates/, home.md, weekly.md (master index), reference/ (cross-area docs), archives/.
- dashboards/ folder removed: replaced by per-area index.md files.
- Memory Level 2: subfolders domain/, tools/, product/, project/. SessionStart hook injects MEMORY.md index. Level 3 (memsearch) deferred until index exceeds 50 entries.
- CLAUDE.md architecture: behavioral rules stay inline in global CLAUDE.md (~40-50 lines). me.md for identity narrative (on demand). vault-map.md, skill-map.md, area CLAUDE.md files for navigation and area context (on demand or cwd-based).
- Skills self-improvement: assertion-only loop (Option B), overnight cron, suggestions staged for human review before apply.
- PreCompact hook: captures current objective, uncommitted decisions, active constraints, open questions. session-state.md rejected.
- session-update skill needs updating after Task 1: write to weekly.md (master) and areas/{project}/weekly/.

## Architectural decisions (2026-04-27)

- Skills with disable-model-invocation: evolve, board, handoff, evolve-queue. Prevents model from auto-triggering high-risk/interactive skills mid-task.
- CLAUDE_CODE_SUBAGENT_MODEL set to haiku globally. Sonnet was running for every fork subagent; unnecessary cost.
- clinicpro-medtech/.claude/settings.json: deny rules for rm -rf, rm -r, curl DELETE, dropdb, psql DROP. No deny rules existed despite PHI + FHIR exposure.
- nexwave-rd/.claude/settings.json: deny rules for Write/Edit on docs/*/output/*. Protects MBIE deliverables from accidental overwrite.
- 3 hooks active as of 2026-04-27: em-dash detector (PostToolUse Write+Edit), bash audit log (PreToolUse Bash to ~/.claude/logs/), session stats (Stop, outputs systemMessage). Scripts in C:/Users/reonz/Cursor/hooks/.

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
  .where(p => p.project === "founder-os" && p.status !== "done")
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
