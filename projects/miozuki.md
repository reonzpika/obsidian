---
id: miozuki
status: active
type: side-project
owner: ting
repo: miozuki-web
stack: Next.js, TypeScript, Tailwind, Vercel, Shopify Storefront API
---
## Quick Links ##
- [Shopify](https://admin.shopify.com/store/miozuki/)
## Description
Fine jewellery ecommerce brand (NZ) specialising in moissanite and pearl pieces. Migrating the Shopify-native storefront to a custom Next.js frontend using the Shopify Storefront API. Hosted on Vercel at miozuki.co.nz.

## Notes
- Shopify store: nassuu-px.myshopify.com (live, products loaded)
- Brand palette: deep burgundy `#7B1E22` + cream `#F5F0E9`, Playfair serif
- Repo: github.com/reonzpika/miozuki-web (scaffolded sprint 1)
- No sales yet; ads running, conversion optimisation needed post-launch
- NZD / NZ market, DTC model

## Klaviyo Integration Notes

- Endpoint: `POST https://a.klaviyo.com/api/profile-subscription-bulk-create-jobs/`
- Revision header: `2024-02-15`
- Auth: `Authorization: Klaviyo-API-Key {KLAVIYO_PRIVATE_KEY}`
- `POST /api/lists/{id}/relationships/profiles` is deprecated — do not use
- Profile attributes: `email`, `first_name` (optional), `subscriptions.email.marketing.consent: SUBSCRIBED`
- List ID goes in `relationships.list.data.id` — get from Klaviyo URL when viewing the list, not from the forms page
- Returns 202 Accepted on success
- Env vars: `KLAVIYO_PRIVATE_KEY`, `KLAVIYO_LIST_ID` — must be set in both `.env.local` and Vercel project settings

## Weekly Progress Log

### Week of 2026-04-13

- Two-track collaboration workflow set up: Ting works directly on master (no branching); Ryo uses feature branches with Vercel preview URLs for approval before merging
- `.vscode/tasks.json` — dev server auto-starts when project opens in Cursor (no terminal for Ting)
- `.vscode/settings.json` — one-click commit auto-pushes to master
- `TING-GUIDE.md` — plain-English workflow guide for Ting
- `CLAUDE.md` updated with two-track workflow note so AI agents know not to suggest branches/terminal to Ting
- `Ctrl+Alt+P` keyboard shortcut — one-keypress publish with timestamped commit message
- `.env.example` committed; `.gitignore` updated to track it
- `docs/ting-laptop-setup.md` — in-person setup checklist ready to follow on Ting's machine
- Next: complete setup on Ting's laptop (miozuki-20260415-001)

### Week of 2026-04-07

- Implemented Miozuki 2.0 UI/UX on branch `feat/ui-animations-2.0` — 13 files, 778 insertions: scroll-reveal animations, staggered grids, hero line-by-line reveal, animated FAQ accordion, mobile snap-scroll product rail, luxury hover overlay, CSS marquee announcement bar, nav restructure with animated dropdowns, homepage reorder, differentiator strip, stone stats bar, email capture section, section diamond dividers
- Created `miozuki-web/docs/context/miozuki-2.0-proposal-for-ting.md` — standalone approval doc covering Phase 1 (7 quick wins) and Phase 2 (7 investment items) with evidence citations; awaiting Ting sign-off
- Wired Klaviyo email subscribe via `/api/subscribe` — uses `profile-subscription-bulk-create-jobs` endpoint (revision 2024-02-15); name + email captured, `first_name` mapped in Klaviyo profile
- Built site-wide email popup (`email-popup.tsx`) — 4s trigger on first visit, 7-day suppression on dismiss, permanent suppression on subscribe; uses same API route

### Week of 2026-04-06

- Completed full UI/UX and brand audit of miozuki-web — saved to `miozuki-web/brand-audit-2026.md`
- Identified 15 prioritised findings across brand identity, visual design, copy, navigation, and product UX
- Critical gaps flagged: no logomark exists, hero headline is SEO copy not brand copy, AI-generated image in Accessible Luxury section, dual brand voice register not unified
- Created deep research prompt (industry standards and best practices for fine jewellery DTC brands)
- Identified 3 additional research tracks before implementing updates: competitor live sites, NZ market specifics, moissanite positioning landscape
- Created detailed deep research prompts for all 3 research tracks — ready to run in Claude.ai
- Identified zero-reviews trust gap as primary conversion blocker at launch; researched trust signal priority stack for new DTC fine jewellery (NZ market)
- Trust tier-1 (implement immediately, no research needed): returns policy visible on PDPs, NZ identity signals (NZBN in footer, NZ address, Afterpay badge), craftsmanship warranty statement
- Trust tier-2 (pre-launch): founder story above fold on homepage (not About page), moissanite provenance/certification page, micro-influencer seeding (15-20 NZ creators, gifted)
- Mapped moissanite-specific credibility problem ("fake diamond" perception) as requiring separate trust framing beyond standard DTC tactics — certification detail and lab-stone narrative are the key levers
- Added fourth deep research track: trust signals for zero-review DTC fine jewellery launch — structured prompt ready to run in Claude.ai

## Sprints

```dataviewjs
const active = dv.pages('"sprints/active"')
  .where(p => p.projects && p.projects.includes("miozuki"));
const archived = dv.pages('"sprints/archive"')
  .where(p => p.projects && p.projects.includes("miozuki"));
const pages = active.concat(archived).sort(p => p.start);
const headers = ['Sprint', 'Goal', 'Start', 'End', 'Status'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.id), p.goal, p.start, p.end, p.status
]));
```

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
  .where(p => p.project === "miozuki" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
