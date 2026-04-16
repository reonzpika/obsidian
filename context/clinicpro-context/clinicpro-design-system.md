# ClinicPro Design System

> Authoritative reference for all frontend work across ClinicPro products.
> Every decision here is research-backed. Rationale is included so you can apply judgment — not just rules.
> When in doubt: precision and clarity over delight.

---

## 1. Brand Philosophy

ClinicPro tools are built by a practising GP, for GPs under time pressure. The design must signal three things simultaneously: **clinical seriousness** (this is a professional tool, not a consumer app), **practical trustworthiness** (it does what it says, transparently), and **warm directness** (NZ/AU professionals expect clear, respectful, no-nonsense communication — not corporate formality).

**The single design test:** Would a GP trust this with patient data? If the UI feels playful, flashy, or consumer-grade, the answer is no.

---

## 2. Two-Product Colour System

ClinicPro has two distinct product lines that should be visually differentiable. Everything else (typography, spacing, component patterns, tone) is shared.

### Rationale for colour split
Research basis: 60% of healthcare software uses blue as primary (neurophysiological — blue demonstrably lowers heart rate and creates calming parasympathetic response, building trust). Teal signals clinical precision and a clean aesthetic that mimics clinical lighting — appropriate for tools deeply embedded in clinical workflow.

### ClinicPro SaaS (clinicpro.co.nz)
*Products: Referral Images, 12-month Prescriptions, AI Scribe, ACC tools*

**Primary: Deep forest green** *(Option 1 Native — decided 2026-04-08)*
- Green carries health associations (22% adoption vs 60% blue — stands out while remaining clinically credible)
- Deep forest green (not lime, not mint) reads as serious, grounded, authoritative — not wellness
- NZ cultural resonance: native bush, DOC green, natural landscape — culturally authentic without being cliché
- Amber shared accent adds warmth and anchors the editorial/letter-grammar design language

| Role | Name | Hex | Tailwind |
|------|------|-----|----------|
| Primary action | Forest Green | `#15803d` | `nz-green-700` |
| Primary hover | — | `#166534` | `nz-green-800` |
| Primary light (bg tints) | — | `#dcfce7` | `nz-green-100` |
| Primary soft (borders, chips) | — | `#bbf7d0` | `nz-green-200` |
| Primary glow (shadows, accents) | — | `#16a34a` | `nz-green-600` |

### ClinicPro Medtech (clinicpro-medtech)
*Products: ClinicPro Capture (ALEX integration PWA)*

**Primary: Clinical teal**
- Deeply embedded in clinical workflow (NHI lookup, image commit to Medtech Evolution)
- Requires institutional trust, not commercial warmth
- Teal = clinical precision, data clarity, technical authority
- Visually distinct from SaaS at a glance — GPs switching contexts see a different product

| Role | Name | Hex | Tailwind |
|------|------|-----|----------|
| Primary action | Clinical Teal | `#0d9488` | `teal-600` |
| Primary hover | — | `#0f766e` | `teal-700` |
| Primary light (bg tints) | — | `#ccfbf1` | `teal-100` |
| Primary soft (borders, chips) | — | `#99f6e4` | `teal-200` |
| Primary glow (shadows, accents) | — | `#14b8a6` | `teal-500` |

> **Tailwind note:** SaaS uses `nz-green` as primary. Medtech uses `teal` (or chosen Option 1 charcoal — see `colour-options.md`). Do not cross-pollinate — SaaS never uses teal as primary; Medtech never uses nz-green as primary.

### Shared semantic colours (both products)

Research basis: Colour must never be the sole information carrier (WCAG 2.2, 1.4.1 — 300M people globally are colour-blind). All states use colour + icon + label.

| Role | Hex | Tailwind | Notes |
|------|-----|----------|-------|
| Success / confirmed | `#16a34a` | `green-600` | Positive outcomes, completed actions |
| Warning / caution | `#d97706` | `amber-600` | Use amber, NOT red — red elevates anxiety |
| Error / destructive | `#dc2626` | `red-600` | Errors only; never as primary accent |
| Quote / highlight accent | `#f59e0b` | `amber-400` | For GP quotes, callouts, human moments |
| Dark forest green bg | `#0c2820` | inline style | Evidence sections, featured product cards |
| Dark navy bg | `#0f172a` | `slate-900` | Story/narrative dark sections |
| Cream page bg | `#fafaf7` | inline style | Main page background |
| Neutral base | `#f8fafc` | `slate-50` | Page backgrounds, light sections |
| Neutral surface | `#f1f5f9` | `slate-100` | Cards on light bg |
| Text primary | `#0f172a` | `slate-900` | All primary text |
| Text secondary | `#475569` | `slate-600` | Supporting text |
| Text tertiary | `#94a3b8` | `slate-400` | Labels, captions, metadata |
| Border | `#e2e8f0` | `slate-200` | Cards, dividers |

### Contrast requirement
Minimum 4.5:1 (WCAG AA) for all text. Target WCAG AAA (7:1) for clinical data. Readability in clinical settings increases 60% with proper contrast — this is patient safety, not aesthetics.

---

## 3. Typography

### Rationale
Research finding: sans-serif fonts are the universal standard for clinical software. They reduce misreading risk, improve scanning speed under time pressure, and outperform serif on screens. Inter is specifically research-validated for clinical software: it is a humanist sans-serif designed for screen rendering at small sizes, balancing clinical precision with human warmth. It outperforms Roboto and Open Sans for readability at 12-16px. Oswald (condensed display) is appropriate for marketing headings where visual hierarchy and authority matter — not for in-app clinical UI.

### Font stack

| Font | Role | Loading | Where |
|------|------|---------|-------|
| **Newsreader** | Marketing serif display (hero headlines, pull-quotes, section headings) | `next/font/google` via root layout (`--font-newsreader`) | Marketing/landing pages only — never in clinical app UI |
| **Caveat** | Handwritten sign-off and P.S. accents only | `next/font/google` via root layout (`--font-caveat`) | Marketing sign-offs only — one or two instances per page |
| **JetBrains Mono** | Section markers (§ 01), marginalia rails, captions | `next/font/google` via root layout (`--font-mono-jb`) | Marketing pages — letter grammar structural labels |
| **Oswald** | Legacy marketing display headings | Google Fonts (loaded in SaaS) | Avoid for new work — Newsreader is preferred for new marketing pages |
| **Inter** | All body text; all in-app UI | Google Fonts (already loaded in SaaS) | Everywhere, including all clinical tool UIs |
| ~~Open Sans~~ | Deprecated | — | Do not use for new work |

> **Medtech repo:** Add Inter via `next/font/google`. Remove system font default.

### Font role rules

**Oswald** (marketing headings only):
- Use for: section headings, hero headlines on marketing/landing pages
- Class: `font-oswald`
- Weight: `font-bold` (700) only — Oswald at 400 looks weak
- Transform: normal (no uppercase — it reads as shouting)
- Never use for: body text, UI labels, buttons, form elements, any clinical route

**Inter** (everything else):
- Use for: all body copy, all UI elements, all clinical tool pages, all button labels
- Class: `font-inter` or no class (set as body default in globals.css)
- Weights in use: 400 (body), 500 (medium, UI labels), 600 (semibold, emphasis), 700 (bold, headings in-app)

### Type scale

| Size | Tailwind | Use |
|------|----------|-----|
| 48–72px | `text-5xl`–`text-7xl` | Marketing hero headlines (Oswald only) |
| 36–44px | `text-4xl` | Marketing section headings (Oswald) |
| 24–30px | `text-2xl`–`text-3xl` | In-app page headings (Inter bold) |
| 18–20px | `text-lg`–`text-xl` | In-app subheadings, card titles |
| 16px | `text-base` | Body text, form labels |
| 14px | `text-sm` | Supporting text, descriptions |
| 12px | `text-xs` | Metadata, captions, fine print |

### Readability specs (clinical standard)
- **Minimum body font:** 16px (14px only for secondary/supporting text)
- **Line height:** 1.5–1.6 (`leading-relaxed`) — reduces cognitive load
- **Letter spacing:** Normal to slightly open; never tight for body text
- **Avoid:** Light weights (300) in clinical UI — poor contrast in clinical lighting conditions

---

## 4. Spacing and Layout

### Rationale
GPs use rapid glance-and-verify patterns (5–10 second screen bursts). Information must be retrievable without scrolling within a single visual field. Generous spacing improves scan speed and reduces eye strain.

### Max-widths

| Context | Max-width | Tailwind |
|---------|-----------|----------|
| Marketing page content | 1280px | `max-w-7xl` |
| Marketing section content | 1024px | `max-w-5xl` or `max-w-4xl` |
| Single-focus content (pricing, forms) | 672px | `max-w-2xl` |
| Reading columns | 768px | `max-w-3xl` |
| Narrow cards | 512px | `max-w-xl` |

### Section padding rhythm
- **Marketing sections:** `py-16 sm:py-24` (64px → 96px) — generous breathing room
- **Dense in-app sections:** `py-8 sm:py-12` (32px → 48px)
- **Horizontal padding:** `px-4 sm:px-6` — mobile first, expand on larger screens

### Grid
- Default: 1 column (mobile) → 2 columns (sm) → 3 columns (lg) where appropriate
- Gap: `gap-4` (tight cards) or `gap-5` to `gap-6` (breathing room)
- Never go beyond 3 columns for content; 4 only for icon-only cards

### Mobile-first principles
Research finding: Clinicians prefer mobile for in-consultation quick reference; desktop for documentation. Design for mobile completion first — not just "it works on mobile."
- Touch targets: minimum 44×44px
- Forms on mobile: full-width inputs, large tap areas
- Marketing CTAs on mobile: full-width button or near-full-width
- No horizontal scroll at any viewport

---

## 5. Component Patterns

### Buttons

**Primary button** (main action):
```
bg-[product-primary] text-white rounded-full px-6–8 py-3–4 font-semibold
hover: slightly lighter shade, shadow glow
```
- Always rounded-full on marketing pages
- `rounded-lg` acceptable in dense in-app UI
- Never: square corners (too institutional), rounded-full in data tables (too consumer-app)

**Secondary button** (alternative action):
```
border border-slate-200 bg-white text-slate-800 rounded-full/lg px-6 py-2–3 font-medium
hover: bg-slate-50
```

**Ghost/text button** (low emphasis):
```
text-[product-primary] font-medium
hover: bg-primary/5
```

**Destructive:**
```
bg-red-600 text-white
```
Reserve for genuinely destructive actions (delete, revoke). Never use for warnings.

**Button hierarchy rule:** One primary button per view. Never two primary buttons competing.

### Cards

```
rounded-2xl border border-slate-200 bg-white p-5–6 shadow-sm
```
- Use `shadow-sm` not `shadow-lg` — clinical tools should feel precise, not dramatic
- Hover state on clickable cards: `hover:shadow-md transition-shadow`
- Dark cards (inside dark sections): `bg-white/5 border-white/10`

### Forms and inputs (clinical UI)

```
border border-slate-200 rounded-lg px-4 py-3 text-base text-slate-900
focus: ring-2 ring-[product-primary]/30 border-[product-primary]
```
- Always use `text-base` (16px) for inputs — never `text-sm`
- Error state: red border + red text label + error icon (never red alone)
- Labels above inputs, never placeholder-only (accessibility + clinical precision)

### Alert / status badges

Always use colour + icon + text label. Never colour alone.
```
Success: bg-green-50 border-green-200 text-green-800 + CheckCircle icon
Warning: bg-amber-50 border-amber-200 text-amber-800 + AlertTriangle icon
Error: bg-red-50 border-red-200 text-red-800 + XCircle icon
Info: bg-blue-50 border-blue-200 text-blue-800 + Info icon
```

---

## 6. Animation Principles

### Rationale
Research finding: Excessive animation in clinical software reduces trust scores and signals "not serious." Clinicians don't want delight — they want clarity and speed. Marketing pages are an exception: scroll-triggered reveals, staggered entrances, and subtle continuous motion create a modern editorial feel (inspired by Maven Clinic and Hers). All marketing animations must respect `prefers-reduced-motion`.

### Signature easing curve
All marketing page transitions use `cubic-bezier(0.33, 0, 0, 1)` (smooth deceleration, inspired by Hers). This replaces generic `ease` across the codebase. In-app clinical UI continues to use `ease` or `ease-out`.

### What to animate

| Animation | Use case | Spec |
|-----------|----------|------|
| Scroll reveal (fade + translate) | Marketing page sections | `0.7s cubic-bezier(0.33, 0, 0, 1)`, 28px translateY, IntersectionObserver with `rootMargin: '0px 0px -15% 0px'` (triggers at ~85% viewport), fires once |
| Hero entrance stagger | Marketing page hero only | CSS `lg-hero-enter` class with `--hero-delay` CSS variable per element (0s portrait, 0.05s marginalia, 0.1s eyebrow, 0.18s headline, 0.32s subline, 0.48s CTAs) |
| Portrait float | Hero portrait image only | `translateY(0 → -8px → 0)`, 6s infinite `ease-in-out`. Subtle continuous motion that makes the static photo feel alive |
| Counter count-up | Evidence section stat numbers | `requestAnimationFrame` counter, 1.5s duration, ease-out cubic, triggers on scroll via IntersectionObserver |
| Header glass effect | Sticky header on scroll | `backdrop-blur(12px)`, transition 300ms |
| Button hover glow | Primary CTA buttons only | `box-shadow` ring, 250ms `cubic-bezier(0.33, 0, 0, 1)` |
| Card lift hover | Marketing product cards | `translateY(-2px)` + shadow, 250ms `cubic-bezier(0.33, 0, 0, 1)` |
| Accordion expand | FAQ, collapsible panels | `grid-template-rows: 0fr → 1fr`, 0.35s `cubic-bezier(0.33, 0, 0, 1)`. ChevronDown rotate 180°, 300ms same easing |
| Loading spinner | Async states only | `animate-spin` |
| Error/success state | Form feedback | Fade in, no translate |

### What not to animate
- Page transitions (jarring in clinical context)
- Hover animations on non-interactive elements
- Any animation that delays access to information
- In-app clinical UI (loading states only)

### Timing rules
- Fast interactions (hover, toggle, card lift): 200–300ms
- Reveals (scroll, modal open): 600–900ms
- Hero entrance sequence: 0.9s per element, staggered 0.05–0.48s
- Continuous ambient (portrait float): 6s
- Nothing above 600ms in clinical UI

### Reduced motion
All marketing animations wrapped in `@media (prefers-reduced-motion: reduce)` safety net. `lg-hero-enter` and `lg-float` classes set `animation: none; opacity: 1` when reduced motion is preferred.

---

## 7. Dark Sections

### Section rhythm
The homepage uses dark/light alternation to create visual rhythm (inspired by Maven Clinic). Two dark sections break up the otherwise cream page:

```
CREAM #fafaf7   ████████  Hero
WHITE/60        ██        Proof strip
DARK GREEN      ████      Evidence section (#0c2820)
CREAM           ████████  Tools (hero card also uses #0c2820)
DARK NAVY       ████      Story section (#0f172a / slate-900)
CREAM           ████████  Principles, CTA, Roadmap, FAQ, Footer
```

### Two dark background colours

| Name | Hex | Use |
|------|-----|-----|
| Dark forest green | `#0c2820` | Evidence/stats sections, featured product cards. Carries the nz-green brand into dark contexts |
| Dark navy | `#0f172a` (slate-900) | Narrative/story sections. Neutral dark that lets amber accents and white text breathe |

Do not mix these in the same section. Do not introduce additional dark colours.

### When to use dark backgrounds
- **Evidence/stats sections:** Dark forest green — signals weight and authority for data
- **Story/narrative sections:** Dark navy — creates immersive reading context
- **Featured product cards:** Dark forest green — differentiates the hero product from other cards
- **Security/compliance sections:** Either dark colour appropriate
- **In-app clinical UI:** Never — dark is for marketing only

### Dark section rules
- Text on dark: `text-white` for headings, `text-white/60–70` for body, `text-white/30–40` for supporting/citations
- Borders: `border-white/20` for corner brackets, `border-white/10` for card edges
- Grain texture: `lg-grain-dark` class — `rgba(255,255,255,0.04)` dot grid at 22px, opacity 20–30%
- Subtle glow: `bg-nz-green-700/10 blur-3xl` (green sections) or `bg-amber-500/5 blur-3xl` (navy sections)
- Section marker labels on dark: `text-amber-400/70` (not amber-700, which is invisible on dark)
- Blockquote accent line: `bg-amber-400` (same as cream sections — the amber reads well on both)

---

## 8. Voice and Tone

### Rationale
NZ professionals expect: direct, warm, respectful. Not corporate-formal, not consumer-casual. AU professionals expect: no-nonsense, competence-led, evidence-based. Both markets reject jargon and flowery language. GPs trust software that is honest about what it does and doesn't do.

### Copy rules

**Lead with the outcome, not the feature:**
- ✓ "Clinical photos on your desktop in 30 seconds"
- ✗ "Our innovative image transfer technology enables clinicians to..."

**Be honest about limitations:**
- ✓ "You still attach the JPEG to your referral manually"
- ✗ Hiding the fact that it's not fully automated

**Use clinical language appropriately:**
- Refer to patients as patients (not "users" or "clients" in clinical context)
- Use NHI, ERMS, HealthLink, Medtech Evolution — GPs know these
- Don't over-explain clinical context you share with your audience

**Framing for NZ/AU:**
- NZ: "Let's..." / "Consider..." — collaborative, not commanding
- AU: Direct imperatives fine — "Start free trial" not "Why not start a free trial?"
- Both: Avoid exclamation marks in clinical context

**Pricing copy:**
- Always state trial and ongoing price together: "1 month free · $5/month after"
- Never "completely free" — it sets wrong expectations now that pricing exists
- "Cancel any time" — always include on pricing sections

### Heading style (marketing)
- Oswald bold, normal case (not uppercase)
- Short, concrete — 3–7 words max for hero
- Fragments acceptable: "Clinical photos. On your desktop. In 30 seconds."
- No clever wordplay — GPs are time-pressured, directness is respect

---

## 9. Do-Not-Do List

These are patterns that have been validated as wrong for this audience and context. Do not introduce them regardless of how they look.

| Anti-pattern | Why not |
|---|---|
| Purple as any accent | No clinical or NZ/AU cultural association; looks startup-generic |
| Gradient backgrounds (purple→pink, etc.) | Generic AI-generated aesthetic; signals consumer app |
| Rounded pill shape on in-app data tables | Too consumer-app; use rounded-lg |
| Animations that delay information access | GPs are time-pressed; never animate content into existence that was needed immediately |
| Gamification (streaks, badges, progress bars for engagement) | Clinicians don't want delight; they want reliability |
| "Completely free" in copy | Inaccurate; creates trust problems when pricing appears |
| Pastel / low-saturation colour palette | Signals unserious; healthcare needs clear contrast |
| Stock photography of smiling doctors | Inauthentic; NZ/AU professionals distrust stock imagery |
| Shadcn default patterns (default card + default button, unmodified) | Generic; every component must be intentional |
| Inter for marketing display headings | Too neutral for impact; use Oswald for marketing h1/h2 |
| Oswald in clinical in-app UI | Too condensed for scanning under time pressure |
| Light font weights (300) in clinical data | Fails contrast in clinical lighting conditions |
| Red as a primary or accent colour | Elevates anxiety; reserve for destructive actions only |
| Horizontal scroll on any viewport | Breaks mobile clinical use |
| More than one primary CTA per view | Kills decision clarity |
| Feature tables with 10+ rows | Cognitive overload; lead with the key benefit |

---

## 10. Accessibility Baseline

Non-negotiable. Clinical software with poor accessibility has patient safety implications.

- **Contrast:** Minimum 4.5:1 (WCAG AA) for all text. Target 7:1 for clinical data display.
- **Colour + redundancy:** Every status, alert, and state uses colour + icon + text label. Never colour alone.
- **Touch targets:** Minimum 44×44px for all interactive elements.
- **Focus states:** Visible focus ring on all interactive elements (keyboard navigation).
- **Screen reader:** Semantic HTML. `aria-label` on icon-only buttons. `role` attributes on custom components.
- **Font size:** Minimum 16px for body text. Never use `text-xs` for primary content.

---

## 11. Product Application Summary

| | ClinicPro SaaS | ClinicPro Medtech |
|---|---|---|
| **Primary colour** | nz-green-700 (`#15803d`) | teal-600 (`#0d9488`) |
| **Marketing display font** | Newsreader (serif) + JetBrains Mono (markers) + Caveat (sign-off) | — (no marketing pages) |
| **Body / UI font** | Inter | Inter |
| **Tone** | Warm professional, modern | Clinical, precise, institutional |
| **Dark hero** | Yes (marketing) | No |
| **Animation** | Scroll reveals + hero stagger | Minimal — loading states only |
| **Target context** | Desktop documentation + mobile quick-ref | Mobile in-room + desktop review |

---

*Last updated: 2026-04-16*
*Research basis: colour psychology in healthcare UI (JMIR, UXMatters, Naskay 2025), typography in clinical settings (Letter Hend, FontAlternatives), GP workflow UX (AMA, PMC), NZ/AU cultural context (Cultural Atlas, SBS). Animation patterns: Maven Clinic (GSAP ScrollTrigger, counter animations, dark/light rhythm), Hers (CSS-only, cubic-bezier easing, gentle float).*
