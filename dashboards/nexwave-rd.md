---
id: nexwave-rd
status: active
type: rd
repo: nexwave-rd
stack: [aws-bedrock, claude-haiku, claude-sonnet, python, nextjs]
---

# NexWave R&D

MBIE-funded R&D programme (N2RD grant CONT-109091-N2RD-NSIWKC). Developing NZ-sovereign clinical LLM for GP workflow. Managed with Ting (R&D Programme Manager).

---

## Programme at a Glance

| Field          | Detail                                      |
| -------------- | ------------------------------------------- |
| Contract ref   | CONT-109091-N2RD-NSIWKC                     |
| Total funding  | $716,926.00 (GST excl.)                     |
| First tranche  | $286,770.40                                 |
| Grant split    | 40% MBIE / 60% company                      |
| Contract start | 12 March 2026                               |
| Contract end   | 11 March 2028                               |
| MBIE contact   | Lisa Pritchard                              |
| Q1 claim due   | 31 May 2026 (PAYE evidence due 30 Apr 2026) |

---

## Active Objective — Obj 1

**Objective 1 — Foundation AI Architecture and Data Requirements**

Months 1–6 | January–June 2026

Core question: Which AI architecture and NZ data types achieve clinical-grade performance under sovereignty constraints?

Key deliverables by end of June:

- Medtech and Indici sandbox environments connected
- Architecture selected with documented evidence
- Data requirements documented (types and volumes)
- Prototypes hitting ≥90% triage accuracy and ≥95% CVDRA accuracy on synthetic data

---

## Objective Timeline

| Objective | Title | Period | Status |
|---|---|---|---|
| Obj 1 | Foundation AI Architecture | Months 1–6 | Active |
| Obj 2 | Real-World Inbox Data Handling | Months 4–12 | Not Started |
| Obj 3 | Care Gap Detection Validation | Months 7–16 | Not Started |
| Obj 4 | Real-World Deployment | Months 16–24 | Not Started |

---

## Budget by Objective

| Objective | Budget |
|---|---|
| Obj 1 — Foundation Architecture | $177,396 |
| Obj 2 — Inbox Data Handling | $178,562 |
| Obj 3 — Care Gap Detection | $179,410 |
| Obj 4 — Real-World Deployment | $145,558 |
| Capability Development | $36,000 |
| **Total** | **$716,926** |

---

## Hard Stops

- Safety metrics fail → halt all deployment immediately
- Clinical accuracy drops >10% → investigate before proceeding
- GP satisfaction <60% → re-evaluate workflow integration
- Co-funding falls below 60% → clawback risk

---

## Sprints

```dataviewjs
const pages = dv.pages('"sprints/active"')
  .where(p => p.projects && p.projects.includes("nexwave-rd"))
  .sort(p => p.start);
const headers = ['Sprint', 'Goal', 'Start', 'End', 'Status'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.id || p.file.name),
  p.goal, p.start, p.end, p.status
]));
```

---

## Unassigned Tasks

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
const ownerOpts = [
  { name: 'option', value: ['ryo'] },
  { name: 'option', value: ['ting'] },
  { name: 'option', value: ['both'] }
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
function ownerSelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('owner', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--owner'] }, ...ownerOpts] }
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
const pages = dv.pages('"tasks/open"')
  .where(p => p.project === "nexwave-rd" && (!p.sprint || p.sprint === ""))
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Objective', 'Owner', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  p.objective, ownerSelect(p.file.path),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
