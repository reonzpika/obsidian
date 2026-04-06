# Dashboard — ClinicPro SaaS

Products: referral-images, ai-scribe, 12-month-prescription, acc, openmailer

---

## Weekly Progress Log

### Week of 2026-04-06

- Referral Images launched 6 April 2026 on $5/month subscription model
- Grandfathering migration applied: 78 pre-launch users set to `grandfatheredUntil = 2027-04-06`; new users get 1-month free trial via Clerk webhook
- `referral_images_users` table extracted from `users` (migration 0057) — holds `imageTier`, `grandfatheredUntil`, and referral-images-specific columns
- Tier resolver updated to query `referralImagesUsers` with `grandfatheredUntil > now()` logic
- Stripe checkout converted to subscription mode; webhook branched on `product: referral_images` to avoid AI Scribe cross-contamination
- Free tier fully blocked post-trial — removed 20-image limit, grace unlock system, and `sendLimitHitEmail`
- Paywall UI added to both capture and desktop pages; copy updated to "Already used by 100+ GPs across NZ. Billed monthly, cancel anytime."
- Stale code cleaned: removed `graceUnlocksRemaining`, `calculateLimit`, `canUseGraceUnlock`, `IMAGE_TOOL_FREE_MONTHLY_LIMIT`, `getImageToolUsage`, `unlock-grace` route; `sendMonthResetEmail` copy updated to $5/month
- FK re-key bug fixed in `ensure-links` and Clerk webhook routes — sequential child-table updates to work around neon-http no-transaction constraint
- Stripe CLI installed; test env configured; local webhook listener running

---

## Quick links

| | |
|--|--|
| **Products** | [[ai-scribe]] · [[referral-images]] · [[12-month-prescription]] |
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
  .where(p => p.repo === "clinicpro-saas")
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
  .where(p => p.repo === "clinicpro-saas" && p.due && p.due < dv.date("today") && p.status !== "done")
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
