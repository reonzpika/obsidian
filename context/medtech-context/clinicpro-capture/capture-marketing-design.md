---
title: ClinicPro Capture — marketing design source of truth
status: v0.1 (2026-04-16) — locked direction, first build pending user review
related:
  - ../clinicpro-context/clinicpro-design-system.md
  - ./capture-overview.md
  - ./capture-pricing.md
  - ./capture-problem-statement.md
meta-guide: ../Maxizing-UI-UX-Quality with Claude Code.md
---

# ClinicPro Capture — marketing design source of truth

> Authoritative for every public-facing Capture marketing page (`/medtech/capture`, `/refer-a-practice`, and any future Capture marketing touch).
> Extends the global design system in `clinicpro-design-system.md`. When this doc and the global doc conflict, this one wins for marketing-only contexts. In-app clinical UI still follows the global doc.

---

## 0. For the LLM building from this doc

Before touching any component in a Capture marketing page, invoke the following skills. Claude under-triggers skills by default; this is a hard instruction, not a suggestion.

**On starting work, invoke in this order:**

1. `superpowers:frontend-design` — Anthropic-official design discipline, anti-slop typography, motion guidance.
2. `web-design-guidelines` (if installed, Vercel-official) — design linting against common AI-slop anti-patterns.
3. `web-accessibility` (if installed) — WCAG 2.2 AA checks.
4. `ui-animation` (if installed) — motion polish for any animated element.

**During the session:**

- If editing a component, re-invoke `frontend-design` at the start of that edit block.
- If running into a layout dead-end, ask for the `frontend-design` skill's layout anti-patterns list.
- Before committing, verify against `web-accessibility` for focus rings, labels, contrast.

**Anti-generic prompting baseline (from the Maximizing UI/UX Quality reference doc):**

- Inter, Roboto, Open Sans, Lato, Arial, Space Grotesk, and system font stacks are BANNED in marketing. This doc's typography stack below overrides any default.
- Purple-to-blue gradients on white are BANNED. Use the discipline in §3 below.
- Three-equal-cards-in-a-row is a convergence pattern. Prefer asymmetric splits, paired rows, tariff tables, editorial rhythm.
- Never ship UI after a single generation. Visual verification + 2-3 iterations minimum (see §10).

**When in doubt, use the right altitude:**
- Too low altitude = hardcoded hex codes, brittle values.
- Too high altitude = "make it look clinical", vague.
- Right altitude = "Newsreader serif display, IBM Plex Sans body, 800 weight for headline, asymmetric 40/55 column split, teal-600 used exactly four times in this section".

---

## 1. Audience and tone

**Primary audience:** NZ practice managers and owner GPs evaluating clinical software. Time-pressured (5-10 second attention bursts), institutionally sceptical, reject consumer-app salesmanship, respect craftsmanship and restraint.

**Secondary audience:** champion GPs forwarding the page to their PM; digital/IT leads and PHO procurement evaluating framework alignment and data residency.

**Tone targets:** clinical seriousness, practical trustworthiness, warm directness. Not corporate formal, not consumer casual. Direct imperatives are acceptable; flowery language is not.

**Single design test:** would a GP trust this with patient data? If the UI feels playful, flashy, or consumer-grade, it fails.

---

## 2. Typography

### Marketing typography stack (this doc)

| Role | Font | Weights | Loading |
|------|------|---------|---------|
| Display / hero / section leads | **Newsreader** (serif) | 400, 600, 700 | `next/font/google` as `--font-newsreader` |
| Body / UI / buttons | **IBM Plex Sans** | 400, 500, 600, 700 | `next/font/google` as `--font-body` |
| Section markers, regulatory framework labels, captions | **JetBrains Mono** | 400, 500 | `next/font/google` as `--font-mono` |

**Why this stack:**

- **Newsreader** (editorial serif, distinctive). Signals "this is a serious publication, not a product brochure". Research-validated for screen rendering.
- **IBM Plex Sans** (institutional, clean, clinical-adjacent). Replaces Inter for marketing contexts. IBM Plex reads as technical-institutional rather than tech-bro-startup. Not in the AI-slop banned list.
- **JetBrains Mono** (monospace). For `§ 02` section markers, framework name highlights (`HIPC 2020`, `HISO 10029`), and small captions. Gives the page a quiet editorial precision.

**Global design system conflict note.** The global `clinicpro-design-system.md` specifies Inter for all body text, including in-app and marketing. For **marketing only**, this doc overrides that choice to IBM Plex Sans. In-app clinical UI (inside `/app/medtech/capture/*`) still uses Inter per the global system. Rationale: clinical UI values research-validated legibility at small sizes in clinical lighting; marketing values distinctiveness and institutional register.

### Weight discipline

Use weight extremes, not middle ground.

- Hero headline: Newsreader 700 (or 600 if 700 reads too heavy).
- Section headings: Newsreader 600 or IBM Plex Sans 700.
- Body: IBM Plex Sans 400.
- UI labels and buttons: IBM Plex Sans 500 or 600.
- Fine print, captions, mono markers: IBM Plex Sans 400 or JetBrains Mono 400.

Size jumps between tiers should be meaningful (ideally 1.5x+). Hero headline is 3-4x body size.

### Type scale (marketing)

| Size | Tailwind | Use |
|------|----------|-----|
| 60–72px | `text-6xl`–`text-7xl` | Hero headline desktop (Newsreader) |
| 48px | `text-5xl` | Hero headline mobile; Trust lead 1 desktop |
| 36px | `text-4xl` | Section leads, Trust lead 2 |
| 24–30px | `text-2xl`–`text-3xl` | Section subheads, fix headings, FinalCTA headline |
| 18–20px | `text-lg`–`text-xl` | Body lead lines, summary copy |
| 16px | `text-base` | Body text, inclusions, FAQ answers |
| 14px | `text-sm` | Footer lines, trust line under hero CTAs |
| 12px | `text-xs` | Section markers (`§ 02`), captions |

### NZ English and copywriting rules

Apply to every word that ends up on the rendered page.

- NZ spelling: organise, behaviour, programme, colour, centre.
- **No em dashes in rendered copy.** Use full stops, commas, or colons. Restructure sentences to avoid them.
- Telegraph style: short sentences, no preamble, no padding.
- Lead with the outcome, never the feature.
- Pricing copy must match `capture-pricing.md` source of truth. No "30-day free trial", "no credit card", "cancel anytime", or FTE-tier language.
- Certification claims: "ALEX API integration", "Medtech partnership agreement in final stages". Never "Medtech Global certified partner" until that is factually true.
- Competitors (MedImage, QuickShot) are NOT named on public pages. Reference categories and architectural constraints instead.
- Every word must be intentional. When cutting doesn't reduce meaning, cut.

---

## 3. Colour

### Palette

Base comes from the global design system (`clinicpro-design-system.md` §2 Medtech), with marketing-specific applications below.

| Role | Token | Hex | Tailwind | Use |
|------|-------|-----|----------|-----|
| Primary accent | Clinical Teal | `#0d9488` | `teal-600` | Single accent across the page. Used sparingly. |
| Primary hover | — | `#0f766e` | `teal-700` | Button hover, link hover. |
| Primary soft | — | `#ccfbf1` | `teal-100` | Pricing-table header row. |
| Canvas | White | `#ffffff` | `white` | Default page background. |
| Surface | Slate 50 | `#f8fafc` | `slate-50` | Cards on light sections (avoid on this page unless needed). |
| Text primary | Slate 900 | `#0f172a` | `slate-900` | All primary text. |
| Text secondary | Slate 700 | `#334155` | `slate-700` | Body copy. |
| Text muted | Slate 600 | `#475569` | `slate-600` | Pain quotes, consequence lines, footers. |
| Text tertiary | Slate 500 | `#64748b` | `slate-500` | Pain quote display, trust line. |
| Border | Slate 200 | `#e2e8f0` | `slate-200` | Table borders, subtle dividers. |
| Dark hero bg | Navy | `#0c1628` | inline | Trust section dark band only. |

### Discipline rules

1. **Teal-600 is scarce.** It appears at specific, counted moments:
   - Primary CTA button background.
   - PainFix fix-heading underlines (2-3px, 4 instances).
   - HowItWorks step numbers and left vertical rule.
   - Pricing table header row background (teal-100, not teal-600).
   - FinalCTA button background.
   That is roughly 8-10 appearances across the whole page. Scarcity creates salience. If teal ever appears more, audit.

2. **One dark band only.** The Trust section uses navy `#0c1628`. No other section uses a dark background. FinalCTA can use teal-600 as a distinct punctuation colour, or stay light; do not reuse the Trust navy.

3. **Slate is the default text spectrum.** Slate 500, 600, 700, 900 in decreasing mutedness. Pain-side copy is muted (500-600). Fix-side and primary body copy are full ink (700-900).

4. **No gradients on marketing.** No purple-to-blue, no green-to-teal, no fade-to-anything. The page is flat colour or solid dark. Gradients trigger AI-slop recognition instantly.

5. **WCAG 2.2 AA minimum.** Every text/background pair meets 4.5:1 contrast for normal text and 3:1 for large text and UI components. Slate-500 on white sits near the AA boundary for body size; use slate-600 if any reviewer finds slate-500 borderline.

---

## 4. Spatial composition

### Max-widths

| Context | Max-width | Tailwind |
|---------|-----------|----------|
| Marketing page content | 1280px | `max-w-7xl` |
| Section content (hero, pain↔fix, trust) | 1024px | `max-w-5xl` |
| Single-focus sections (HowItWorks, FAQ) | 768px | `max-w-3xl` |
| Reading columns (inclusions list items) | 672px | `max-w-2xl` |

### Vertical rhythm

- Section padding: `py-24 sm:py-32` (96px mobile → 128px desktop). Non-negotiable. Airy layout is a credibility signal.
- Between PainFix rows: 80-96px padding.
- Between Pricing inclusions: `gap-3` (12px) within the two-column grid.
- Hero: `py-24 sm:py-32` with generous internal breathing room.

### Grid preferences

- Avoid three-equal-cards-in-a-row. Convergence pattern.
- Preferred patterns: asymmetric 40/55 split (PainFix), single tariff table (Pricing), two-column grid 2x2 (Trust supporting blocks), single centred column with vertical rule (HowItWorks).
- Maximum 3 columns for content. 2 is stronger for this page.

### Mobile-first baseline

- Every section must be fully legible and navigable at 360px width.
- Asymmetric columns stack vertically at `<640px`. PainFix: pain above fix, same order.
- Touch targets minimum 44×44px (WCAG 2.5.8). FAQ `<summary>` and all CTAs must meet this.
- No horizontal scroll at any viewport.
- Hero headline size steps down cleanly: `text-5xl` mobile → `text-7xl` desktop.

---

## 5. Section patterns (Capture marketing pages)

Each pattern below is the canonical recipe. Extending or deviating must be justified, documented here, and reviewed.

### 5.1 Hero

- Headline: Newsreader serif, two-sentence structure where the second sentence is the payoff beat, rendered on its own line.
- Body: IBM Plex Sans, `text-lg`, slate-700, max-w ~48ch.
- Primary CTA: teal-600 rounded-full button, white text, `px-8 py-4`.
- Secondary CTA: plain text link, underline on hover.
- Trust line: `text-sm` slate-500, beneath the CTAs.
- Optional Loom embed slot: below CTAs, 16:9, thin slate-200 frame.
- Background: white. Generous top/bottom padding.

### 5.2 Pain↔Fix paired rows

The signature pattern for Capture marketing.

- Section marker: JetBrains Mono `§ 02` (or equivalent) top-left, `text-xs` slate-500. No section heading.
- Four paired rows, alignment baseline-aligned across columns.
- Desktop: asymmetric 40% (pain) / 55% (fix) with 5% gutter.
- Pain column (left): Newsreader italic, `text-xl` sm `text-2xl` md, slate-500. Real curly quotes rendered oversize (2-3x text size) in slate-300. Consequence line below in IBM Plex Sans `text-base`, slate-600.
- Fix column (right): IBM Plex Sans bold, `text-2xl` sm `text-3xl` md, slate-900. Trailing full stop is a design element. Underline beneath heading: 2-3px teal-600, width of heading. Supporting line in IBM Plex Sans `text-base`, slate-700.
- Optional hanging-margin offset on pain side (8-12%, no rotation). If it reads as gimmicky, fall back to tidy aligned column.
- Mobile: single column. Pain above fix. Same row order. Drop hanging-margin offset.
- Motion: IntersectionObserver fade-in per row, 0.55s ease, 28px translateY, fires once.

### 5.3 Trust

- Full-bleed dark band, navy `#0c1628`.
- Two lead moments + supporting grid.
- Lead 1 (data handling, plain English): Newsreader serif, `text-4xl` sm `text-5xl` md, white. Body `text-lg` white/70.
- Thin white/10 horizontal rule.
- Lead 2 (regulatory posture): IBM Plex Sans bold, `text-2xl` sm `text-3xl` md, white. Body `text-base` white/70. Framework names (`HIPC 2020`, `HISO 10029`) highlighted inline in JetBrains Mono or teal-500 to give scanners visual anchors.
- Thin white/10 horizontal rule.
- Supporting blocks: 2x2 grid desktop, single column mobile. Each block: IBM Plex Sans semibold `text-lg` white heading, `text-sm` white/60 body, `leading-relaxed`.
- No decorative icons. Visual styling alone.
- Content in `max-w-5xl mx-auto`.
- Section padding `py-24 sm:py-32`.
- Language discipline: "built to meet", "designed against", "aligned with". Never "certified against" unless factually true.

### 5.4 How it works

- Centred, `max-w-2xl mx-auto`.
- Small section heading ("How it works.") in Newsreader or IBM Plex Sans, restrained.
- Five-step numbered list. Numbers in teal-600, IBM Plex Sans semibold. Step text in slate-900.
- Ultra-thin teal-600 vertical rule (2px) running the height of the list, positioned left of the numbers, connecting the steps.
- Background-process footer line below the list: IBM Plex Sans `text-base`, slate-600.
- Motion: fade-in on entry, 0.55s. Optional 80ms stagger per step.
- Simplicity is the argument. Do not pad this section.

### 5.5 Pricing

- White background, `max-w-4xl mx-auto`.
- Section heading: IBM Plex Sans bold, `text-3xl`, slate-900.
- Sub-line: IBM Plex Sans `text-base`, slate-600.
- Tariff table: subtle teal-100 header-row background, slate-200 borders. Rendered as a clinical fee schedule, not a pricing-card grid.
- Inclusions list: two-column grid desktop (`md:grid-cols-2`), single column mobile. Small teal-600 check glyph (`✓`) preceding each item. IBM Plex Sans `text-base`.
- Concierge trial line: plain text, `text-sm` slate-600, optionally italic. Not a button.
- Primary CTA at bottom: same teal-600 button as hero.
- Copy discipline: match `capture-pricing.md` word for word. No stale trial or FTE language.

### 5.6 FAQ

- White background, `max-w-3xl mx-auto`.
- Native `<details>` elements. Each `<summary>`: IBM Plex Sans medium `text-lg` slate-900, chevron on right (CSS rotation on `[open]`).
- Each answer: IBM Plex Sans `text-base` slate-700, `leading-relaxed`.
- No decorative dividers. Vertical spacing via `py-4`.
- Hover state: slight teal-600 left-border accent (2px) on `<summary>`.
- Touch target: `<summary>` minimum 44×44px (padding adjusted accordingly).
- Chevron `aria-hidden="true"`.

### 5.7 Final CTA

- Single closing band.
- Teal-600 background OR light (slate-50) background — pick whichever contrasts best with the preceding Trust section.
- Centred, `max-w-3xl mx-auto`.
- Headline: Newsreader serif, `text-3xl` sm `text-4xl` md. White on teal/dark, slate-900 on light.
- Single button: "Book a 15-minute demo" mailto.
- Trust line beneath: IBM Plex Sans `text-sm` with reduced opacity.
- Does not restate features. One sentence, one button, one line of credit.

---

## 6. Motion discipline

- IntersectionObserver fade-in per section or per row, once, on viewport entry.
- Duration: 0.55s ease-out. Translate: 28px.
- Button hover: 200ms ease.
- FAQ accordion: native `<details>` disclosure, chevron 180deg rotation on `[open]`, 200ms.
- No parallax, no scroll-linked animations, no counter animations, no typewriter, no carousel.
- Loom embed lazy-loads.
- **Reduced motion safety net** in `app/globals.css`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0s !important;
  }
}
```

---

## 7. Accessibility baseline (WCAG 2.2 AA)

- Contrast: 4.5:1 normal text, 3:1 large text and UI components.
- Touch targets: 44×44px minimum (WCAG 2.5.8).
- Focus indicators visible on every interactive element. No `outline: none` without a replacement focus ring.
- Semantic HTML first. `<main>`, `<section>`, `<blockquote>`, `<h1>`-`<h3>`, `<details>`, `<summary>` used appropriately. ARIA only when HTML semantics are insufficient.
- Pain quotes in `<blockquote>`. Fix headings as `<h3>`.
- Real curly quotes (`"` `"`) in copy, not straight quotes.
- Alt text on any icon that conveys meaning. `aria-hidden="true"` on purely decorative icons.
- Forms (pricing concierge, refer-a-practice): labelled inputs, `aria-describedby` for help text, `aria-live` for errors.
- Keyboard navigation: tab order follows visual reading order. Skip link present if appropriate.
- Reduced-motion honoured everywhere (see §6).

---

## 8. Copywriting source of truth links

- Product capabilities, workflow, security model: `./capture-overview.md`
- Vendor landscape, structural gap analysis: `./capture-problem-statement.md`
- Pricing, inclusions, FAQ: `./capture-pricing.md` (authoritative — overrides any plan or email copy)

---

## 9. URL architecture for Capture marketing

Decided 2026-04-16. Option 2 from URL discussion.

- **Marketing:** `/medtech/{product}` (public, static, `(marketing)` route group).
- **App:** `/app/medtech/{product}/*` (authenticated, per-product entitlement required, `(clinical)` route group).

All Capture marketing pages are in `app/(marketing)/medtech/capture/...`. All Capture app pages are in `app/(clinical)/app/medtech/capture/...`. Middleware enforces `/app/*` as the single protected path prefix.

Future tools under `/medtech/` follow the same split. New tool = new marketing URL at `/medtech/{new-tool}` + app under `/app/medtech/{new-tool}/*`.

---

## 10. Build verification protocol

Every marketing page build, before declaring done:

1. **Visual check at three viewports.** Take screenshots at 360px (mobile), 768px (tablet), 1440px (desktop). Confirm no horizontal scroll, typography scales correctly, columns stack on mobile.
2. **Dark-mode check.** Reserved for future; Capture marketing is light-only at v0.1. If adding dark mode later, every section must be specified.
3. **Accessibility audit.** Run WCAG 2.2 AA checks: contrast, focus rings, keyboard navigation, screen reader tree (semantic HTML), target sizes.
4. **Copy audit.** Grep page source for banned terms: `30-day free trial`, `no credit card`, `FTE`, `certified partner`, em dash (`—`), `MedImage`, `QuickShot`.
5. **Motion check.** Toggle `prefers-reduced-motion`. All animations stop. Page still navigable.
6. **At least two iterations.** No UI ships after a single generation. First pass is always a draft.
7. **Skills re-invocation.** After first build, re-invoke `frontend-design` and `web-accessibility` for a second-pass review.

If any check fails, iterate. Do not commit.

---

## 11. Open questions and known risks

- **Typography stack reaction pending.** Newsreader + IBM Plex Sans + JetBrains Mono is the current direction. User review on the first build may revise this. If IBM Plex Sans reads as too institutional or starts clashing with the in-app Inter experience a prospect sees next at demo, reconsider.
- **Hanging-margin PainFix offset.** 8-12% horizontal offset on pain column is a distinctive design move. If user review says it reads as gimmicky rather than lived experience, fall back to tidy aligned column.
- **Teal scarcity.** If first build has teal appearing more than ~10 times across the page, audit and cut.
- **Final CTA background colour.** Teal-600 or slate-50 is a judgement call on first build. Pick the stronger contrast against the preceding Trust navy.
- **HISO 10029 claim language.** "Built to meet" and "designed against" are defensible. "Certified against" is not. If PHO digital lead pushes on this at demo, honest fallback is "designed to align with, happy to walk through specifics in the DPA".

---

## 12. Maintenance

- This doc updates when user review changes design direction.
- Section patterns (§5) update when a new marketing page introduces a new pattern that proves worth reusing.
- Copy source-of-truth doc references (§8) update when those docs change.
- Typography, colour, and accessibility baseline changes are treated as versioned decisions. Bump the version in frontmatter and note the change.

*v0.1 — 2026-04-16. Initial lock from design discussion. First build pending, review after first build will produce v0.2.*
