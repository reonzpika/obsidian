# ClinicPro Colour Palette Options

> Status: **DECIDED 2026-04-08** — Option 1 Native chosen. See `clinicpro-design-system.md` for live values. This document retained as decision record.

---

## Decision criteria (from research)

Before reviewing options, these are the constraints that any colour choice must satisfy:

1. **Clinically credible** — cannot read as consumer app, wellness/spa, or lifestyle brand
2. **WCAG AA minimum** — 4.5:1 contrast ratio on all text; 7:1 target for clinical data
3. **Original** — blue and teal are what 60-80% of healthcare apps use; dismissed
4. **Differentiable** — SaaS and Medtech must be visually distinct from each other
5. **NZ/AU appropriate** — no colour that carries a wrong cultural association in either market
6. **Semantic separation** — whatever colour is chosen as primary cannot be amber (reserved for quotes/highlights) or red (reserved for errors only)

---

## Option 1 — Native

> **Concept:** Rooted in NZ. Grounded in health. Not like any other GP software.

| Product | Colour | Hex | Tailwind |
|---------|--------|-----|----------|
| ClinicPro SaaS | Deep forest green | `#15803d` | `green-700` |
| ClinicPro Medtech | Charcoal slate | `#1e293b` | `slate-800` |
| Shared accent | Warm amber | `#f59e0b` | `amber-400` |

**Why this works:**
- Green carries health associations (used by 22% of healthcare apps vs 60% blue — stands out while still being clinically legible)
- Deep forest green (not lime, not mint) removes the wellness/spa connotation. Reads as serious, grounded, authoritative
- NZ cultural resonance: native bush, DOC green, natural landscape — culturally authentic without being cliché
- Charcoal slate for Medtech signals clinical precision and institutional seriousness — completely different feel from SaaS
- The contrast between warm forest green and cool charcoal creates strong differentiation

**Risks:**
- Green can still tip into "alternative health" if implementation is not disciplined (avoid: light greens, lime, mint)
- In AU market, green doesn't carry the same NZ cultural resonance — ensure it's used as a brand colour, not a "NZ flag" moment

**Implementation notes:**
- SaaS: Add `forest` palette to Tailwind (or use existing `green-700` range, ensuring deep values only)
- Medtech: Replace all placeholder blues with slate-800 as primary; no change to neutral base
- Amber stays as shared accent (quotes, highlights, callouts only — never warning, which becomes orange-600)

---

## Option 2 — Indigo Authority

> **Concept:** The GP who built this thought harder about design than every other tool in the market.

| Product | Colour | Hex | Tailwind |
|---------|--------|-----|----------|
| ClinicPro SaaS | Deep indigo | `#3730a3` | `indigo-700` |
| ClinicPro Medtech | Deep forest green | `#166534` | `green-800` |
| Shared accent | Warm amber | `#f59e0b` | `amber-400` |

**Why this works:**
- Indigo is spectrally adjacent to blue — so it carries residual trust/calm associations without being generic healthcare blue
- Indigo is used by premium professional services (legal, financial, insurance) — signals authority and considered design, never used in healthcare = completely original
- Psychologically: indigo signals depth, contemplation, precision — appropriate for a product built by a clinician who thought carefully about the problem
- Forest green for Medtech: health, clinical, grounded — works in the deeper shade as institutional rather than wellness

**Risks:**
- Indigo can edge toward purple at lower saturations — must stay at `indigo-700` or `indigo-800`, never lighter
- Some research flags purple family as potentially "overwhelming in clinical environments with high cognitive load" — but deep indigo is far from the vivid purples the research references

**Implementation notes:**
- SaaS: Add `indigo` palette to Tailwind if not present; primary = `indigo-700`, hover = `indigo-800`
- Medtech: Deep green `green-800` as primary — very dark, very serious
- Test both at WCAG AAA contrast levels before finalising

---

## Option 3 — Editorial Slate

> **Concept:** Looks like no healthcare product that exists. Signals: we thought about this from first principles.

| Product | Colour | Hex | Tailwind |
|---------|--------|-----|----------|
| ClinicPro SaaS | Rich slate | `#334155` | `slate-700` |
| ClinicPro Medtech | Deep indigo | `#4338ca` | `indigo-700` |
| Shared accent | Warm amber | `#f59e0b` | `amber-400` |

**Why this works:**
- Slate as a primary is almost unheard of in healthcare — immediately signals "this is different"
- Reads as editorial, premium, considered — like a premium professional tool (financial terminals, legal software, high-end SaaS)
- NZ/AU preference for no-nonsense professionalism aligns with slate's neutral authority
- Amber accent does the heavy lifting for warmth — prevents coldness
- Indigo for Medtech differentiates clearly from SaaS while adding depth and authority

**Risks:**
- Highest execution risk — "premium editorial" requires very precise typography and spacing to work; if the rest of the UI isn't equally intentional, slate reads as "unfinished" not "premium"
- Least immediately legible as healthcare — some GPs may not immediately identify it as a clinical tool
- Requires the amber accent to be used generously enough to add warmth

**Implementation notes:**
- This option requires the most disciplined implementation — typography, spacing, and contrast must all be impeccable
- Dark hero sections work extremely well with this palette (slate-700 primary + near-black hero)
- Amber accent should appear on CTAs and key highlights, not just quotes

---

## Option 4 — Amber Earth

> **Concept:** Boldest option. NZ earth tones. Nothing in healthcare looks like this.

| Product | Colour | Hex | Tailwind |
|---------|--------|-----|----------|
| ClinicPro SaaS | Deep amber | `#b45309` | `amber-700` |
| ClinicPro Medtech | Charcoal slate | `#1e293b` | `slate-800` |
| Shared accent | Forest green | `#15803d` | `green-700` |

**Requires special handling:**
- Amber-700 as brand primary is visually bold; amber as **warning/caution** must use a distinctly different treatment (border + icon + text, different shade — e.g., amber-50 bg with amber-600 text, never the same amber-700 used for brand)
- This requires explicit semantic separation in the design system: brand amber ≠ caution amber

**Why this works:**
- Deep amber/copper reads as: warm authority, grounded, human, NZ earth tones (the land, kauri, iron sand)
- Completely unlike any other GP software in the NZ/AU market — very memorable
- Charcoal for Medtech creates strong product differentiation and feels appropriately serious
- Forest green accent grounds the palette and adds health associations

**Risks:**
- Highest risk option. Amber-as-primary may trigger subconscious caution/warning associations for some users (since amber = warning in traffic lights and most UI systems)
- Requires the most implementation discipline to separate brand amber from warning amber
- Some GPs may find it unexpected to the point of seeming unprofessional — A/B testing would ideally validate before full roll-out

**Implementation notes:**
- Warning states must use orange-600 or amber with significantly different treatment (bg fill + border + icon)
- Brand amber (CTAs, headings) should always be at `amber-700` (`#b45309`) — dark enough to avoid "caution sign" connotation
- Test with a small group of GPs before committing

---

## Shared elements (all options)

These do not change regardless of which option is chosen:

| Role | Hex | Tailwind |
|------|-----|----------|
| Neutral bg (light sections) | `#f8fafc` | `slate-50` |
| Neutral surface (cards) | `#f1f5f9` | `slate-100` |
| Text primary | `#0f172a` | `slate-900` |
| Text secondary | `#475569` | `slate-600` |
| Text tertiary | `#94a3b8` | `slate-400` |
| Border | `#e2e8f0` | `slate-200` |
| Dark forest green bg | `#0c2820` | inline style |
| Dark navy bg | `#0f172a` | `slate-900` |
| Success | `#16a34a` | `green-600` |
| Warning | `#d97706` | `amber-600` |
| Error | `#dc2626` | `red-600` |

---

## Next step

Once Ryo selects an option (or defines a hybrid), update:
1. `clinicpro-design-system.md` section 2 — Two-Product Colour System
2. `clinicpro-saas` Tailwind config — update `primary` CSS variable and add relevant palette
3. `clinicpro-medtech` Tailwind config — add chosen primary palette
4. Replace `nz-blue` references on landing page with new primary
