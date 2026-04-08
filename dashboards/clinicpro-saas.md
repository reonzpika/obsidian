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
- Fixed user re-key duplicate email constraint: temp-email swap before INSERT in `ensure-links` and `clerk-user` webhook routes
- Fixed Stripe webhook product check (`referral_images_premium` → `referral_images`); added `customer.subscription.deleted` and `invoice.payment_failed` handlers
- Fixed Clerk middleware blocking Stripe webhook route (was returning 401 to Stripe on every event)
- Fixed success page redirect loop: was pushing to `/referral-images/capture` (requires `?u=` param); corrected to `/referral-images`; updated copy to subscription language
- Registered dedicated production Stripe webhook at `clinicpro.co.nz/api/referral-images/upgrade/webhook`; `STRIPE_REFERRAL_IMAGES_WEBHOOK_SECRET` updated in Vercel
- Deployed to production (commit 667a203); TypeScript error on `Invoice.subscription` field patched before deploy succeeded
- T5 verified in dev: payment flow completes, Premium badge appears; T6 (cancel → revert) pending production verification
- T5 and T6 completed locally: subscribe → `imageTier = premium` and cancel → `imageTier = free` both confirmed end-to-end
- Root cause of webhook failures identified: Stripe CLI was authenticated to NexWave account (`acct_1RhpQRP6R5CzSXa7`) but `.env` had test keys from a different account (`acct_1TJ6xV`); fixed by updating `.env` to NexWave test keys
- `.env` bug fixed: leading space in `STRIPE_REFERRAL_IMAGES_WEBHOOK_SECRET` was causing signature verification to fail silently (truthy value prevented fallback to `STRIPE_WEBHOOK_SECRET`)
- Local test environment now stable: NexWave test keys + CLI on NexWave account; correct webhook path is `/api/referral-images/upgrade/webhook` (route group `(clinical)` does not appear in URL)
- Vercel production env vars verified: all four live Stripe keys confirmed on NexWave account (`sk_live_`, `pk_live_`, live price ID, live webhook secret) — production deploy confirmed complete
- Landing page fully redesigned (`app/(marketing)/referral-images/page.tsx`): dark navy hero, scroll animations, GP quotes from "GPs for GPs" Facebook group, expanded security section, pricing section ($5/month, 1 month free trial), all "completely free" messaging removed, Oswald + Inter typography, mobile-first
- gws CLI confirmed installed globally (`npm` global) and authenticated — provides Google Drive/Docs access from Claude Code sessions
- ClinicPro design system created: `context/clinicpro-context/clinicpro-design-system.md` — brand philosophy, typography (Inter body, Oswald marketing display), spacing, component patterns, animation rules, voice/tone, do-not-do list — all research-backed
- Design research documented: `context/clinicpro-context/design-research.md` — colour psychology in healthcare, typography for clinical software, GP workflow UX, NZ/AU cultural context
- 4 colour palette options documented (decision pending): `context/clinicpro-context/colour-options.md` — Native (forest green + charcoal), Indigo Authority, Editorial Slate, Amber Earth — blue and teal dismissed as too generic
- Colour palette decision finalised: **Option 1 Native** chosen — forest green `nz-green-700` (`#15803d`) as SaaS primary with amber (`#f59e0b`) shared accent; replaces `nz-blue` across all marketing surfaces (`saas-20260408-001` closed)
- Referral Images landing page complete visual redesign (`app/(marketing)/referral-images/page.tsx`): light cream `#fafaf7` editorial hero (was dark navy), asymmetric headline-led layout with animated amber underline accent, forest green CTAs, dark `#0c1628` security anchor with green glow, structure compressed from 12 to 11 sections (merged "Honest about scope" + "Is this for you?" into single "Scope + Fit" 4-card section)
- Body font switched from Open Sans (deprecated per design system) to Inter (already loaded in `app/layout.tsx` — only required removing the `font-open-sans` wrapper class); Oswald preserved on display headings
- All landing page copy preserved verbatim; `useAuth`, `ensure-links` chain, `LOADING_MESSAGES`, `showLoading`, `showEnsureError`, and all redirect logic preserved byte-for-byte
- `nz-green` palette already existed in `clinicpro-saas/tailwind.config.ts:96-108` with full 50-950 range, so the redesign required zero Tailwind config changes — only class swaps in the page file
- Verification: `npx tsc --noEmit` exit 0; ESLint regression check confirmed net reduction in errors vs. original (14 → 3, where the remaining 3 `max-statements-per-line` warnings sit inside the preserved auth chain and predate the rewrite)
- Repo-wide migration of `tailwind.config.ts` `--primary` HSL + obsidian context doc updates (`clinicpro-design-system.md` §2, `colour-options.md`) deferred to `saas-20260408-002`
- Hero photograph generated with Nano Banana Pro (Gemini 3 Pro Image): editorial Leica Q2 / 28mm / f/2.0 / Kodak Portra 400 prompt; final asset saved at `public/images/referral-images/referral_images_hero_image_3.png` (2752×1536) and wired into the redesigned hero with `next/image` priority + responsive `sizes`
- Editorial typography stack added page-scoped via `next/font/google` for the referral-images landing page: Newsreader serif (display + body accents), Caveat handwritten (sign-off), JetBrains Mono (§ section markers); Inter retained for UI chrome and Oswald removed from this page
- "Letter grammar" structure applied across the page: `§ 01`–`§ 05` section markers, `P.S.` lead-in to the FAQ accordion, Caveat sign-off above the footer
- Visual identity primitives added as inline SVG: 4-position viewfinder corner brackets, `Logomark` (corner bracket framing a "RI" serif glyph), `HandUnderline` (Q-curve path) wrapped in a reusable `<Marked>` component, inline marginalia rail beside the hero
- Four post-rewrite polish fixes after side-by-side review: logomark bracket enlarged to fully frame the "RI" glyph; hand-drawn headline underline strength increased (`strokeWidth` 3→4.5, opacity /70→/90, height `h-2`→`h-3`); italic wrapper removed from "In 30 seconds." so all three headline lines render at equal weight; "How it works" dotted connector swapped from `h-px` @ 0.18 opacity to `h-1` @ 0.55 opacity in `nz-green-700` so the line between numbered chips is actually visible
- New vault reference doc created: `context/clinicpro-context/nano-banana-pro-research.md` — 12-section prompt-engineering guide for Google Nano Banana Pro (Gemini 3 Pro Image), including the 7-part prompt template, anti-AI-look techniques, hand-handling rules, and the verbatim Referral Images hero prompt (v1 + two backup variants)
- Final verification on the redesigned page after the polish pass: `npx tsc --noEmit` exit 0; ESLint clean with zero errors (14 cosmetic `tailwindcss/no-custom-classname` warnings remain on intentional `ri-*` keyframe utility classes)

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
