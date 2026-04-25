---
id: miozuki
status: active
type: side-project
owner: ting
repo: miozuki-web
stack: Next.js, TypeScript, Tailwind, Vercel, Shopify Storefront API
title: "Miozuki"
description: "NZ fine jewellery ecommerce. Next.js headless frontend over Shopify."
phase: "Content migration to Next.js frontend"
dashboard: other-projects
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

## Decisions

### 2026-04-15 — Two-track collaboration model for non-dev collaborator
Ting works directly on `master` with zero git literacy; Ryo uses feature branches + Vercel preview URLs for approval before merge. The onboarding primitives are `.vscode/tasks.json` (dev server auto-start on folder open), `.vscode/settings.json` (one-click commit auto-pushes), a `Ctrl+Alt+P` publish shortcut, and a plain-English `TING-GUIDE.md`. Trade-off explicitly accepted: coordination risk in exchange for Ting's autonomy — she can edit content end-to-end without touching a terminal or understanding branches. Pattern is reusable for any future non-dev collaborator on any repo.

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
const all = dv.pages('"tasks/open"')
  .where(p => p.project === "miozuki" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const groups = {};
const unassigned = [];
for (let p of all) {
  const m = p.milestone ?? "";
  if (m) {
    if (!groups[m]) groups[m] = [];
    groups[m].push(p);
  } else {
    unassigned.push(p);
  }
}
const render = (tasks) => dv.table(
  ['Task', 'Status', 'Priority', 'Due'],
  tasks.map(p => [dv.fileLink(p.file.path, false, p.title || p.file.name), statusSelect(p.file.path), prioritySelect(p.file.path), p.due])
);
for (const [m, tasks] of Object.entries(groups)) {
  dv.paragraph(`**${m}**`);
  render(tasks);
}
if (unassigned.length > 0) {
  if (Object.keys(groups).length > 0) dv.paragraph("**Backlog**");
  render(unassigned);
}
```
