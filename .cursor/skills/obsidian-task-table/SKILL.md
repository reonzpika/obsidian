---
name: obsidian-task-table
description: Generate a correctly-structured Obsidian task table for the NexWave/ClinicPro vault (C:\Users\reonz\cursor\obsidian). Use whenever creating or updating a task table in ANY vault file — projects/, dashboards/, or context/. NEVER use plain dataview TABLE for task tables in this vault. Always use the dataviewjs pattern with meta-bind inline selects and sortable columns defined below.
user-invocable: true
argument-hint: [filter-type: project|repo|milestone] [filter-value] [optional: include-done]
allowed-tools:
  - Read
  - Edit
  - Write
---

# Obsidian Task Table — Canonical Pattern

This vault uses **dataviewjs** for ALL task tables. Never use plain `dataview` TABLE for tasks — it lacks sorting and inline editing.

## When to use which filter

| File location | Filter field | Example |
|--------------|--------------|---------|
| `projects/*.md` | `p.project === "project-id"` | `p.project === "gp-fellowship"` |
| `dashboards/*.md` | `p.repo === "repo-name"` | `p.repo === "clinicpro-saas"` |
| milestone grouping | `p.milestone === "label"` | `p.milestone === "Phase 1 marketing"` |

Always exclude done tasks unless the user asks to show them: add `&& p.status !== "done"` to the where clause.

## Default columns

Standard: `['Task', 'Status', 'Priority', 'Due']`

For dashboards that span multiple projects/repos, add a Project or Repo column:
`['Task', 'Repo', 'Project', 'Priority', 'Due', 'Status']`

For R&D files, add Owner: `['Task', 'Owner', 'Status', 'Priority', 'Due']`

## Full boilerplate (copy and substitute FILTER_LINE and HEADERS)

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
function scheduleDashboardColumnSort(dv, headerNames) {
  const bind = (table) => {
    if (table.dataset.vaultDashSortBound) return;
    const thead = table.querySelector('thead');
    const tbody = table.tBodies[0] ?? table.querySelector('tbody');
    if (!thead || !tbody || tbody.rows.length === 0) return;
    table.dataset.vaultDashSortBound = '1';
    const ths = thead.querySelectorAll('th');
    const stripArrows = (s) => String(s).replace(/\s*[\u25B2\u25BC]\s*$/, '').trim();
    const state = { col: -1, dir: 'asc' };
    ths.forEach((th) => { th.dataset.sortLabel = stripArrows(th.textContent); });
    ths.forEach((th, colIndex) => {
      th.style.cursor = 'pointer';
      th.title = 'Sort column';
      th.classList.add('vault-dash-sortable-th');
      th.addEventListener('click', (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        const nextDir = state.col === colIndex && state.dir === 'asc' ? 'desc' : 'asc';
        state.col = colIndex; state.dir = nextDir;
        const headerName = headerNames[colIndex] ?? '';
        const sortKey = (row) => {
          const cell = row.cells[colIndex];
          if (!cell) return '';
          if (/due/i.test(headerName)) {
            const raw = cell.innerText?.trim() ?? '';
            const L = dv.luxon.DateTime;
            const iso = L.fromISO(raw);
            if (iso.isValid) return iso.toMillis();
            const fmts = ['MMMM d, yyyy', 'd MMMM yyyy', 'yyyy-MM-dd', 'dd/MM/yyyy', 'd/MM/yyyy'];
            for (const f of fmts) { const d = L.fromFormat(raw, f, { locale: 'en-NZ' }); if (d.isValid) return d.toMillis(); }
            const ms = Date.parse(raw);
            if (!isNaN(ms)) return ms;
            return raw.toLowerCase();
          }
          const sel = cell.querySelector('select');
          if (sel) { const opt = sel.options[sel.selectedIndex]; return (opt?.textContent ?? opt?.innerText ?? sel.value ?? '').trim().toLowerCase(); }
          return (cell.innerText?.trim() ?? '').toLowerCase();
        };
        const tb = table.tBodies[0] ?? table.querySelector('tbody');
        if (!tb) return;
        const rows = Array.from(tb.rows);
        rows.sort((a, b) => { const ka = sortKey(a), kb = sortKey(b); let cmp = (typeof ka === 'number' && typeof kb === 'number') ? ka - kb : String(ka).localeCompare(String(kb), undefined, { numeric: true, sensitivity: 'base' }); return nextDir === 'asc' ? cmp : -cmp; });
        rows.forEach((r) => tb.appendChild(r));
        ths.forEach((h, i) => { const base = h.dataset.sortLabel || stripArrows(h.textContent); h.textContent = base + (i === colIndex ? (nextDir === 'asc' ? ' ▲' : ' ▼') : ''); });
      });
    });
  };
  const tryBind = () => { const table = dv.container.querySelector('table'); if (!table) return false; const tbody = table.tBodies[0] ?? table.querySelector('tbody'); if (!tbody || tbody.rows.length === 0) return false; bind(table); return true; };
  if (tryBind()) return;
  const obs = new MutationObserver(() => { if (tryBind()) obs.disconnect(); });
  obs.observe(dv.container, { childList: true, subtree: true });
  setTimeout(() => obs.disconnect(), 8000);
}
// SUBSTITUTE: change the .where() filter and headers for context
const pages = dv.pages('"tasks/open"')
  .where(p => FILTER_LINE)
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = HEADERS;
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```

## Substitution examples

**Project file** (`projects/my-project.md`):
```javascript
.where(p => p.project === "my-project" && p.status !== "done")
const headers = ['Task', 'Status', 'Priority', 'Due'];
```

**Repo dashboard** (`dashboards/clinicpro-saas.md`):
```javascript
.where(p => p.repo === "clinicpro-saas" && p.status !== "done")
const headers = ['Task', 'Status', 'Priority', 'Due'];
```

**Overdue section** (always by repo or all):
```javascript
.where(p => p.repo === "my-repo" && p.due && p.due < dv.date("today") && p.status !== "done")
.sort(p => p.due);
const headers = ['Task', 'Priority', 'Due'];
// map: dv.fileLink(...), prioritySelect(...), p.due  — no statusSelect in overdue
```

## Hard rules

1. ALWAYS use `dataviewjs` — never plain `dataview` TABLE for tasks in this vault
2. ALWAYS include `scheduleDashboardColumnSort` — sortable columns are required everywhere
3. ALWAYS include meta-bind selects for status and priority
4. ALWAYS exclude done tasks by default (`p.status !== "done"`) unless user asks otherwise
5. Default sort: priority (high→medium→low), then due date ascending
6. When adding a column, also add the value to the `.map()` array in matching position
7. After writing any project file, check it doesn't still have a plain `dataview` block — replace it
