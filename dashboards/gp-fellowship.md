# Dashboard — GP Fellowship

RNZCGP Fellowship application and assessment. College ID: 66153. Requirements completed: 16 Feb 2026.

---

## Quick links

| | |
|--|--|
| **Project** | [[dashboards/gp-fellowship]] |
| **Assessment guide** | [[fellowship-assessment-guide]] |

---

## Open tasks

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
    ths.forEach((th) => {
      th.dataset.sortLabel = stripArrows(th.textContent);
    });
    ths.forEach((th, colIndex) => {
      th.style.cursor = 'pointer';
      th.title = 'Sort column';
      th.classList.add('vault-dash-sortable-th');
      th.addEventListener('click', (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const nextDir = state.col === colIndex && state.dir === 'asc' ? 'desc' : 'asc';
        state.col = colIndex;
        state.dir = nextDir;
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
            for (const f of fmts) {
              const d = L.fromFormat(raw, f, { locale: 'en-NZ' });
              if (d.isValid) return d.toMillis();
            }
            const ms = Date.parse(raw);
            if (!isNaN(ms)) return ms;
            return raw.toLowerCase();
          }
          const sel = cell.querySelector('select');
          if (sel) {
            const opt = sel.options[sel.selectedIndex];
            const t = (opt?.textContent ?? opt?.innerText ?? sel.value ?? '').trim();
            return t.toLowerCase();
          }
          return (cell.innerText?.trim() ?? '').toLowerCase();
        };
        const tb = table.tBodies[0] ?? table.querySelector('tbody');
        if (!tb) return;
        const rows = Array.from(tb.rows);
        rows.sort((a, b) => {
          const ka = sortKey(a);
          const kb = sortKey(b);
          let cmp = 0;
          if (typeof ka === 'number' && typeof kb === 'number') cmp = ka - kb;
          else cmp = String(ka).localeCompare(String(kb), undefined, { numeric: true, sensitivity: 'base' });
          return nextDir === 'asc' ? cmp : -cmp;
        });
        rows.forEach((r) => tb.appendChild(r));
        ths.forEach((h, i) => {
          const base = h.dataset.sortLabel || stripArrows(h.textContent);
          h.textContent = base + (i === colIndex ? (nextDir === 'asc' ? ' \u25B2' : ' \u25BC') : '');
        });
      });
    });
  };
  const tryBind = () => {
    const table = dv.container.querySelector('table');
    if (!table) return false;
    const tbody = table.tBodies[0] ?? table.querySelector('tbody');
    if (!tbody || tbody.rows.length === 0) return false;
    bind(table);
    return true;
  };
  if (tryBind()) return;
  const obs = new MutationObserver(() => {
    if (tryBind()) obs.disconnect();
  });
  obs.observe(dv.container, { childList: true, subtree: true });
  setTimeout(() => obs.disconnect(), 8000);
}

const pages = dv.pages('"tasks/open"')
  .where(p => p.repo === "gp-fellowship" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers,
  pages.map(p => [
    dv.fileLink(p.file.path, false, p.title || p.file.name),
    statusSelect(p.file.path), prioritySelect(p.file.path), p.due
  ])
);
scheduleDashboardColumnSort(dv, headers);
```

## Overdue

```dataviewjs
const mb = app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api;
const lifecycle = this.component;
const priorityOpts = [
  { name: 'option', value: ['high'] },
  { name: 'option', value: ['medium'] },
  { name: 'option', value: ['low'] }
];
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
    ths.forEach((th) => {
      th.dataset.sortLabel = stripArrows(th.textContent);
    });
    ths.forEach((th, colIndex) => {
      th.style.cursor = 'pointer';
      th.title = 'Sort column';
      th.classList.add('vault-dash-sortable-th');
      th.addEventListener('click', (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const nextDir = state.col === colIndex && state.dir === 'asc' ? 'desc' : 'asc';
        state.col = colIndex;
        state.dir = nextDir;
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
            for (const f of fmts) {
              const d = L.fromFormat(raw, f, { locale: 'en-NZ' });
              if (d.isValid) return d.toMillis();
            }
            const ms = Date.parse(raw);
            if (!isNaN(ms)) return ms;
            return raw.toLowerCase();
          }
          const sel = cell.querySelector('select');
          if (sel) {
            const opt = sel.options[sel.selectedIndex];
            const t = (opt?.textContent ?? opt?.innerText ?? sel.value ?? '').trim();
            return t.toLowerCase();
          }
          return (cell.innerText?.trim() ?? '').toLowerCase();
        };
        const tb = table.tBodies[0] ?? table.querySelector('tbody');
        if (!tb) return;
        const rows = Array.from(tb.rows);
        rows.sort((a, b) => {
          const ka = sortKey(a);
          const kb = sortKey(b);
          let cmp = 0;
          if (typeof ka === 'number' && typeof kb === 'number') cmp = ka - kb;
          else cmp = String(ka).localeCompare(String(kb), undefined, { numeric: true, sensitivity: 'base' });
          return nextDir === 'asc' ? cmp : -cmp;
        });
        rows.forEach((r) => tb.appendChild(r));
        ths.forEach((h, i) => {
          const base = h.dataset.sortLabel || stripArrows(h.textContent);
          h.textContent = base + (i === colIndex ? (nextDir === 'asc' ? ' \u25B2' : ' \u25BC') : '');
        });
      });
    });
  };
  const tryBind = () => {
    const table = dv.container.querySelector('table');
    if (!table) return false;
    const tbody = table.tBodies[0] ?? table.querySelector('tbody');
    if (!tbody || tbody.rows.length === 0) return false;
    bind(table);
    return true;
  };
  if (tryBind()) return;
  const obs = new MutationObserver(() => {
    if (tryBind()) obs.disconnect();
  });
  obs.observe(dv.container, { childList: true, subtree: true });
  setTimeout(() => obs.disconnect(), 8000);
}

const pages = dv.pages('"tasks/open"')
  .where(p => p.repo === "gp-fellowship" && p.due && p.due < dv.date("today") && p.status !== "done")
  .sort(p => p.due);
const headers = ['Task', 'Priority', 'Due'];
dv.table(headers,
  pages.map(p => [
    dv.fileLink(p.file.path, false, p.title || p.file.name),
    prioritySelect(p.file.path), p.due
  ])
);
scheduleDashboardColumnSort(dv, headers);
```

---

## Weekly Progress Log

### Week of 2026-04-07

- AMP enrolment confirmed: auto-enrolled 17 February 2026; active engagement is a hard gate for receiving Fellowship Assessment outcome
- AMP goal-setting identified as overdue (required at enrolment start Feb 17); to be completed this weekend
- First AMP collegial relationship meeting due by 17 April (2 months from enrolment); scheduled for next week — task gpf-20260413-001
- Fellowship Assessment Visit forms located in obsidian/temp/ and emailed to ryo@clinicpro.co.nz: Clinical Record Review Audit Checklist and Details for Fellowship Assessment Visit Form
- CRR Module 1 and Module 2 task deadlines rescheduled to 18 April
- gpf-20260330-001 (financial standing) and gpf-20260330-011 (AI scribe policy) deprioritised to Apr 30 — not on critical path for submission
