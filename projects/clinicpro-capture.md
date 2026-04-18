---
id: clinicpro-capture
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
---

## Description
Mobile web app that photographs clinical images and commits them to patient records in Medtech Evolution via the ALEX API. All ALEX calls route through BFF at api.clinicpro.co.nz.

**API reference**: [[alex-api-docs]]

## Current goals
- Ship Phase 1 marketing (landing page, refer-a-practice, in-app banner, champion email, demo Loom) by 2026-04-21
- Warm-list blitz targeting ~60 NZ GP champions starts 2026-04-20
- Await Medtech production sign-off
- Onboard first paying practices after sign-off
- Success gate: 3+ practices paying or trialling by end of week 4

## Key decisions
- URL architecture (decided 2026-04-16): marketing at `/medtech/{product}` (public, `(marketing)` route group), app at `/app/medtech/{product}/*` (authenticated, `(clinical)` route group)
- Marketing typography: Newsreader (serif display), IBM Plex Sans (body), JetBrains Mono (mono). Inter stays in-app only.
- Auth: Supabase OTP (6-digit code, no magic link)
- Pricing (decided 2026-04-15): annual per practice by enrolled patient count ($299 / $799 / $1,500 / contact). No self-serve trial. Concierge trial via ryo@clinicpro.co.nz.
- BFF mandatory: never call ALEX directly from Vercel
- Phase 1 plan: `clinicpro-medtech/docs/superpowers/plans/2026-04-15-capture-marketing-phase1.md`

## AU market — Lawrence Peterson (Medtech Global)

**Execution sprint**: [[2026-04-medtech-sprint-2]] (21 Apr - 16 May 2026)
**Strategy and pricing analysis**: [[clinicpro-capture-au-strategy]]
**External proposal one-pager**: [[clinicpro-capture-au-proposal]]

**Proposal received 12 April 2026:** Lawrence proposes Medtech purchases ClinicPro Capture licenses to bundle as a value-add for AU G2M in May. Scope: image capture + post only as starting point. Two other integration partners already confirmed for AU launch.

**Open questions (as of 14 April 2026):**

| # | Question | Status |
|---|---|---|
| Q1 | Who covers infrastructure running costs under the license bundle model — baked into per-license fee or separate? | Awaiting reply (sent 13 Apr) |
| Q2 | Which AU product specifically — Medtech Evolution AU or other? | Awaiting reply |
| Q3 | How many practices in scope for May G2M, and rollout over 12 months? | Awaiting reply |
| Q4 | Fully Medtech-branded or ClinicPro visible to practices? | Awaiting reply |
| Q5 | Support routing — through Medtech or ClinicPro directly? | Awaiting reply |

All five questions sent to Lawrence in two emails (12 Apr + 13 Apr). AU deal must be structured under a separate agreement from the NZ partnership. Pricing proposal to be prepared once answers received. Tracked in task medtech-20260414-002.

## NZ Partnership Agreement — status (14 April 2026)

Draft received from Alex Cauble-Chantrenne 13 April. Schedule 1 confirmed:

- Commencement Date: 18 March 2026
- Initial Term: 36 months (expires 18 March 2029)
- Fee structure: $10–$60/month per Active Facility by enrolment tier
- Permitted Purposes: direct image service only (Base + Portal without Confidential Scope + ALEX Apps)
- Software: Medtech Artia and Medtech Evolution

Three issues raised with Alex in reply (sent 14 April), tracked in task medtech-20260414-001:

1. **Fee model**: flat per-facility fee not commission-based as discussed. Counter-proposal: 10% self-referred / 15% Medtech-referred of Gross Revenue
2. **Geographic scope**: no NZ-only language; requested explicit restriction — AU market to be handled separately
3. **PIA/pentest timeline**: draft says 3 months; Alex said 6 months in January — requested correction

Awaiting Alex response before signing.

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
  .where(p => p.project === "clinicpro-capture" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
