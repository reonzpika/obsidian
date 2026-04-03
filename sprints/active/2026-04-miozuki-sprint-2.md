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
