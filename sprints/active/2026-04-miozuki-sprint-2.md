---
id: 2026-04-miozuki-sprint-2
status: active
start: 2026-04-04
end: 2026-04-10
repos:
  - miozuki-web
projects:
  - miozuki
goal: Content migration — replicate all existing Shopify storefront content in the Next.js frontend
dashboard: side-projects
---

## Context

Sprint 1 delivered the technical foundation (Shopify API client, all core pages, cart, checkout).
Sprint 2 is about fidelity — the new frontend must match or improve on the existing
miozuki.co.nz content. Products and collections pull from Shopify automatically, but several
content layers are not yet reflected:

- **Hero image** on the home page (currently text-only)
- **Custom home page sections** (brand story, USPs, testimonials — if any)
- **Collection images and descriptions** (may exist in Shopify but not showing, or need updating)
- **Product descriptions / rich HTML** (may be plain or missing on some products)
- **About page** (`/about` currently 404s)
- **Static / policy pages** (shipping, returns, FAQ — if they exist on the current site)

## Approach

Start with a full content audit (task 001) by scraping the existing site page by page.
The audit output drives all subsequent tasks. Do not skip the audit — it defines the scope.

## Tasks

```dataview
TABLE title, status, priority, due
FROM "tasks"
WHERE sprint = "2026-04-miozuki-sprint-2"
SORT priority DESC
```

## Gap Report

Full audit output: `C:\Users\reonz\Cursor\scraper\miozuki\gap-report.md`

Key findings:

**Global (all tasks):**
- Announcement bar missing: "NZ Flat Shipping $8 | $1 ring sizer"
- Header nav links are wrong — correct handles documented in gap report
- Footer is sparse — missing Help/About columns, social links, payment icons

**Task 002 — Home page:**
- Hero image URL confirmed from scrape (hero-image.webp on Shopify CDN)
- 3 sections missing: brand story, Accessible Luxury editorial block, home FAQ (5 Q&As)

**Task 003 — Collections:**
- Collection images + descriptions come from API; confirm query includes `image` and `description`
- Key collection handles: `all-moissanite-pearl-nz`, `best-sellers`, `moissanite-ear-rings`, `bridal-jewellery`

**Task 004 — Product pages (HIGH complexity):**
- Structured sections (What's Included, Details, Materials) are almost certainly Shopify metafields — need to confirm field names in Shopify admin before building
- Engraving field (4-char text input) → needs `customAttributes` in `cartLinesAdd`
- Ring size guide modal (static content + size chart image)
- Shipping accordion (static, same on all products)

**Task 005 — About pages:**
- `/pages/about-us` and `/pages/our-founder` — full content captured in scrape
- Founder image URL confirmed: PXL_20241230... on Shopify CDN

**Task 006 — Policy pages:**
- 7 pages to build: moissanite-faq, jewellery-care, warranty, returns, size-guide, contact, shipping
- Contact form needs a solution (Formspree or simple mailto)
- Shipping policy is also at `/policies/shipping-policy` (Shopify built-in)

**Open questions before Task 004:**
1. What are the metafield namespace/key names for What's Included / Details / Materials?
2. Contact form: **decided** — mailto approach implemented
3. Blogs: **in scope — Task 004** — Storefront API dynamic routes, ISR, 23 existing posts + auto-updates for new posts

## Progress (2026-04-04)

**Done (code complete):**
- Task 001: Content audit ✓
- Task 002: Home page — hero, brand story, collections grid, best sellers, accessible luxury, FAQ accordion ✓
- Task 005: About pages — `/pages/about-us`, `/pages/our-founder` ✓
- Task 006: Policy pages — moissanite-faq, jewellery-care-guide, warranty-cover, returns-refunds-policy, size-guide, contact, shipping-policy ✓
- Global: Announcement bar, header nav fix, footer rewrite ✓
- Product page: Engraving field (cart customAttributes), ring size guide modal, shipping accordion, Judge.me reviews (Option C — server component, graceful empty state) ✓

**Blocked — needs Shopify admin input from Ting:**
- Task 003: Upload collection images + write collection descriptions in Shopify admin
- Task 004: Product page metafields (What's Included / Details / Materials) — need namespace/key names from Shopify admin → any ring product → Metafields section
- Judge.me private API token — add to `.env.local` as `JUDGE_ME_PRIVATE_TOKEN=`
