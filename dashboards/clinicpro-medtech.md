# Dashboard — ClinicPro Medtech

Products: ClinicPro Capture (and future Medtech ALEX products)

---

## Quick links

| | |
|--|--|
| **Products** | [[clinicpro-capture]], [[clinicpro-dashboard]] |
| **API reference** | [[alex-api-docs]] |
| **Glossary** | [Medtech / ALEX Glossary](context/medtech-context/glossary.md) |
| **Active sprint** | [[2026-04-medtech-sprint-1]] |
| **Repo map** | [[repos]] |

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
  .where(p => p.repo === "clinicpro-medtech")
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

---

## Weekly Progress Log

### Week of 2026-04-07

- Defne (Medtech) confirmed all five FHIR roles granted: Invoice R/W, ChargeItem R, ExplanationOfBenefit R, Task R/W, Communication R/W
- Tested Invoice endpoint via SSH on Lightsail BFF — discovered patient/date search not supported; only `GET /Invoice?_id=` works (confirmed against ALEX API docs)
- ChargeItem confirmed working — returns practice billing catalogue for facility F2N060-E
- Diagnosed billing completeness architectural constraint: cannot retroactively audit invoices by patient; redesigned as appointment-driven billing prompt (see clinicpro-dashboard.md)
- Updated clinicpro-dashboard.md with API status findings and new billing completeness architecture
- Sent follow-up to Alex Cauble-Chantrenne re Medtech partnership agreement (OOO until 10 April)
- Sent feature request to Defne requesting patient-based Invoice search (`Invoice?subject=Patient/{id}`)
- Confirmed invoice patient search not supported by design (Prashanth/ALEX Support 8 Apr): invoice retrieval is vendor-scoped only; can only GET by invoice ID created by same vendor — billing completeness module architectural constraint resolved
- Lawrence Peterson replied 12 April with AU deal proposal: Medtech seeking to purchase ClinicPro licenses to bundle into AU G2M product for May; image capture + post feature only as starting point; asked for per-license pricing; two other integration partners already confirmed for AU launch
- Alex Cauble-Chantrenne: partnership agreement draft promised 7 April but not yet received
- Lawrence Peterson: follow-up sent 13 April asking who covers infrastructure running costs under proposed license bundle model — answer needed before pricing proposal can be completed

### Week of 2026-04-14

- Received partnership agreement draft from Alex (13 Apr): reviewed in full including Schedule 1 (fee table extracted via python-docx)
- Schedule 1 confirmed: Commencement Date 18 Mar 2026, Initial Term 36 months, fee structure $10–$60/month per Active Facility by enrolment tier
- Identified three issues with draft: (1) flat fee model not commission-based as verbally agreed, (2) no NZ-only geographic scope, (3) PIA/pentest timeline 3 months vs 6 months Alex stated in January
- Replied to Alex 14 April: requested commission model (10% self-referred / 15% Medtech-referred), explicit NZ-only scope, and correction of PIA/pentest timeline to 6 months — awaiting response
- Lawrence Peterson AU thread reviewed: all five commercial questions sent (12–13 Apr); awaiting reply before pricing proposal can proceed

## Active sprint tasks

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
  .where(p => p.repo === "clinicpro-medtech" && p.sprint && p.status !== "done")
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
