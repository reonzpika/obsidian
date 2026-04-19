# Dashboard — ClinicPro SaaS

Products: referral-images, ai-scribe, 12-month-prescription, acc, openmailer

---

## Weekly Progress Log

### Week of 2026-04-14

- GP profile photo regenerated (saas-20260409-008 closed): two editorial images via Nano Banana Pro with reference-image refinement — v1d (desk/office, lived-in background) replaces `DrRyoEguchiProfilePicMain.jpg` for homepage hero + all avatar uses; alt-v2a (consultation room, candid off-camera gaze) saved as `DrRyoEguchiProfilePicClinic.jpg` for FounderSection + product pages
- AI Scribe § 05 "Why I built this" redesigned: single-column text → two-column editorial layout with clinic portrait (left 2/5) and story text (right 3/5); copy edit removed "and iterate when something breaks"
- Referral Images page: founder trust strip added between § 03 "Honest about everything" and § 04 "Privacy by design" — clinic portrait + founder quote ("I built this because I kept emailing clinical photos to myself")
- `FounderSection.tsx` and `clinicpro-landing.ts` updated to reference clinic image; AI Scribe and Referral Images small avatars remain on main (desk) image
- Prompt sidecar files created: `scripts/prompts/gp-profile-main.prompt.md`, `scripts/prompts/gp-profile-alt.prompt.md`
- Homepage copy rewrite (Option B) completed: hero subline updated to "15-minute slots, four active problems" NZ GP specificity; AI Scribe card Heidi reference removed and replaced with multi-problem consult positioning; principles cards replaced with "GP-built / NZ-tested / Privacy-first" falsifiable claims; "Clinical Orchestration — Vision" removed from roadmap
- Both homepage stats cited: "11.5 hours outside the consult room" (RNZCGP Workforce Survey, 2022) and "92% rate increasing patient complexity as overwhelming" (RNZCGP Burnout Survey, 2021)
- Proof strip updated: "Built by a practising GP · Auckland, NZ · Shipping weekly" → "GP-built · NZ-tested · Privacy-first"
- Full homepage visual redesign inspired by Maven Clinic (GSAP/ScrollTrigger patterns) and Hers (CSS-only easing):
  - Hero: staggered entrance animation (CSS `lg-hero-enter` with variable delays, 0s–0.48s); portrait continuous float (6s `translateY` bob)
  - NEW evidence section: dark forest green `#0c2820` full-bleed with grain texture; two animated counters (11.5 and 92%) count up on scroll via `requestAnimationFrame`
  - Tools: reverted to single column `max-w-3xl`; Referral Images hero card gets dark green bg with grain overlay; AI Scribe trimmed to 1 paragraph
  - Story section: flipped to dark navy `#0f172a` (slate-900) with grain and amber glow
  - FAQ: bouncy accordion via `grid-template-rows` animation (0fr ↔ 1fr) with `cubic-bezier(0.33, 0, 0, 1)` at 0.35s
  - Signature easing: all marketing transitions updated from `ease` to `cubic-bezier(0.33, 0, 0, 1)`; Reveal duration 0.55s → 0.7s; scroll trigger rootMargin for ~85% viewport trigger
  - `prefers-reduced-motion` safety net added for hero entrance and portrait float
- `ReferralImagesHomeCard` dark variant added (`dark` prop: white text, amber-400 label, inverted CTA)
- Story section paragraph 2 rewritten: removed self-deprecating "little tools" / "just me" / "coding in spare time"; replaced with belief-driven narrative ("GPs have accepted bad software as a fact of life. We work around it, build workarounds for the workarounds...")
- Design system updated (`context/clinicpro-context/clinicpro-design-system.md`): §2 new dark bg colours (`#0c2820` forest green, `#0f172a` navy); §6 full animation rewrite (signature easing, all patterns documented); §7 section rhythm map and dark section rules
- `colour-options.md` shared elements updated: old `#0c1628` replaced with two new dark backgrounds

- saas-20260409-003 closed: "full audit trail" claim softened on Referral Images marketing page (three instances at L700/L790/L871 replaced with accurate copy)
- saas-20260409-006 closed: editorial images generated for referral-images landing page (§ 01 problem section + § 02 workflow section)

### Week of 2026-04-07

- AI Scribe landing page (`app/(marketing)/ai-scribe/page.tsx`) fully rewritten — copy + letter-grammar visual migration
- Three-pillar positioning landed: (1) cognitive load not time (NASA Task Load Index, JAMIA Open 2025), (2) multi-problem NZ consults — each complaint in its own lane, (3) NZ GP provenance as trust, not feature
- Research citations embedded: JAMIA Open 2025 clinician pull-quote; PMC12492056 (263 physicians, 6 health systems, 2025)
- `scripts/gen-image.mjs` created: Nano Banana Pro (Gemini 3 Pro Image via laozhang.ai) image generation script; `gen-image` npm script added to `package.json`
- `scripts/prompts/ai-scribe-hero.prompt.md` created: full editorial 7-part GP consult hero prompt (Fujifilm X100V / Classic Chrome / 4500K venetian blind light)
- `public/generated/ai-scribe-hero.jpg` generated (2924 KB) and wired as page hero replacing placeholder
- Product screenshots wired: `ClinicProConsultation.jpg` in § 01 (post pull-quote); `ClinicProGenerateNote.jpg` in § 02 (pre 4-step card)
- Profile photo added: `DrRyoEguchiProfilePicMain.jpg` (48px circle) with Caveat "— Ryo Eguchi" + mono "GP · Auckland, NZ"
- Referral photos section: `referral_images_hero_image_3.png` replaces broken `mobile_recording_page` placeholder
- `saas-20260409-003` created: audit trail gap on Referral Images marketing page — three false "full audit trail" claims at L700/L790/L871
- Homepage copy analysis: Option B selected — keep "Hi, I'm Ryo" hero portrait, update subline/body with NZ specificity (15-min, 4-problem consult language); AI Scribe card and Principles section also flagged for rewrite; implementation deferred to next session

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
- Homepage (`app/page.tsx`) redesigned with letter grammar: § 00 hero with viewfinder-framed portrait, § 01 tools, § 02 story, § 03 principles, § 04 roadmap, P.S. FAQ, Caveat `— Ryo` sign-off; all copy verbatim; Inbox Intelligence waitlist form behaviour preserved
- Shared marketing primitives extracted to `src/shared/components/marketing/letter-grammar.tsx`: useInView, Reveal, Logomark (parameterised `letters` prop), CornerBracket, HandUnderline, Marked, LETTER_GRAMMAR_STYLES
- Referral Images landing page refactored to use shared primitives (visually byte-identical); page-scoped fonts replaced with Tailwind utilities (`font-newsreader` / `font-caveat` / `font-mono-jb`)
- `app/layout.tsx` updated: Newsreader, Caveat, JetBrains Mono loaded globally via `next/font/google` with CSS variables
- `tailwind.config.ts` updated: three new font families; `primary.dark` migrated to nz-green-800
- `app/globals.css`: `--primary` migrated from HSL blue (221 83% 53%) to forest green (142 72% 29%) — all `bg-primary`/`text-primary` across SaaS now render nz-green-700
- `clinicpro-design-system.md` sections 2, 3, and 11 updated to reflect Option 1 Native; `colour-options.md` status marked DECIDED
- `saas-20260408-002` closed (moved to done); `saas-20260409-002` created for clinicpro-medtech palette migration

---

## Quick links

| | |
|--|--|
| **Products** | [[ai-scribe]] · [[referral-images]] · [[12-month-prescription]] |
| **Repo map** | [[repos]] |
| **Finance & accounting** | Helen Yu (accountant, all entities) — see [people.md](../context/people.md#helen-yu) for scope |

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
