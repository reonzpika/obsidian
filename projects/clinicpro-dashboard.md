---
id: clinicpro-dashboard
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
---

## Description

GP clinical dashboard centralising three problems that cause GPs to miss critical actions:

1. **Clinical todos** — NLP extracts action items (labs, referrals, radiology) from free-text consult notes. Extracted items written back to ALEX as native tasks via `POST /FHIR/Task`.
2. **Billing completeness** — Detects unbilled ACC procedure codes, nurse involvement, and CSC/HUHC rate mismatches from consult note content and patient demographics.
3. **Inbox triage** — Prioritises lab results, radiology reports, and clinical correspondence by urgency. Radiology NLP (free-text PDF) for abnormality detection; structured Observation interpretation codes for labs.

**Research**: [[Clinical-Dashboard for NZ General Practice]]
**API reference**: [[alex-api-docs]]

## Build order

Billing first, action items second, inbox triage third.

Billing is the simplest NLP problem, generates immediate measurable revenue, and builds clinical trust for the higher-complexity modules.

## Key decisions

- All ALEX calls via BFF (api.clinicpro.co.nz) — never direct from Vercel
- Consult notes are RTF-encoded base64 — decode step required before LLM processing
- Task write-back is bidirectional: extracted action items land in ALEX as native tasks
- Unfiled inbox queue via `GET /FHIR/V2/DiagnosticReport?attentionto={hpi-cpn}` (v2.10)
- Human-in-the-loop required for all AI outputs — NZ regulatory + patient safety
- Dashboard-owned state tracks billing review status (Invoice query scope TBC pending Medtech role grant)

## API status

| Resource | Access | Notes |
|---|---|---|
| Patient + Coverage | Confirmed | CSC and HUHC via `_include=Coverage:patient` |
| DocumentReference | Confirmed | Consult notes — RTF base64 |
| DiagnosticReport (V2) | Confirmed | Labs + radiology; unfiled inbox via `attentionto` |
| Task | Confirmed (docs) | Pending role test |
| Communication | Confirmed (docs) | Inbox messages; pending role test |
| Invoice | Pending | 403 on all queries — awaiting Medtech role grant |
| ChargeItem | Pending | Billing catalogue — awaiting Medtech role grant |
| ExplanationOfBenefit | Pending | ACC claim details — awaiting Medtech role grant |

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
  .where(p => p.project === "clinicpro-dashboard" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
