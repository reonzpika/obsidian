# ClinicPro SaaS — Design System

> **Canonical reference for all UI/UX work on `clinicpro-saas` (clinicpro.co.nz, AI Scribe, Referral Images, 12-Month Prescription).**
> Read this file before any frontend work. Tokens are authoritative. Prose rationale is included to support judgment calls.

---

## Contents
1. Brand philosophy
2. Colour tokens
3. Typography tokens
4. Spacing and layout tokens
5. Component patterns
6. Animation spec
7. Dark section patterns
8. Voice and copy rules
9. Accessibility baseline
10. DO-NOT list

---

## 1. Brand philosophy

Built by a practising GP, for GPs under time pressure. Three simultaneous signals:

| Signal | What it means in practice |
|---|---|
| Clinical seriousness | Professional tool, not a consumer app. No gamification, no playfulness. |
| Practical trustworthiness | Does what it says, transparently. Honest about limitations in copy. |
| Warm directness | NZ/AU professionals: clear, respectful, no-nonsense. Not corporate formal. |

**The single design test:** Would a GP trust this with patient data? If the UI feels playful, flashy, or consumer-grade — no.

---

## 2. Colour tokens

### Primary (SaaS brand)

| Role | Token name | Hex | Tailwind class |
|---|---|---|---|
| Primary action | `brand-primary` | `#15803d` | `nz-green-700` |
| Primary hover | `brand-primary-hover` | `#166534` | `nz-green-800` |
| Primary glow (shadows) | `brand-primary-glow` | `#16a34a` | `nz-green-600` |
| Primary tint (bg) | `brand-primary-tint` | `#dcfce7` | `nz-green-100` |
| Primary soft (borders, chips) | `brand-primary-soft` | `#bbf7d0` | `nz-green-200` |

**Rationale:** Forest green (not lime, not mint) reads as serious and grounded. NZ cultural resonance (native bush). Stands out in a healthcare landscape dominated by blue (60% adoption) while remaining clinically credible.

### Semantic (shared across all products)

| Role | Hex | Tailwind class | Notes |
|---|---|---|---|
| Success | `#16a34a` | `green-600` | Positive outcomes, completed actions |
| Warning | `#d97706` | `amber-600` | Use amber, NOT red. Red elevates anxiety. |
| Error / destructive | `#dc2626` | `red-600` | Errors and destructive actions only |
| Accent / highlight | `#f59e0b` | `amber-400` | GP quotes, callouts, human moments |

### Backgrounds

| Role | Hex | Tailwind / inline | Use |
|---|---|---|---|
| Page cream | `#fafaf7` | inline style | Main page background |
| Neutral base | `#f8fafc` | `slate-50` | Light section backgrounds |
| Neutral surface | `#f1f5f9` | `slate-100` | Cards on light background |
| Dark forest green | `#0c2820` | inline style | Evidence/stats sections, featured cards |
| Dark navy | `#0f172a` | `slate-900` | Story/narrative dark sections |

### Text

| Role | Hex | Tailwind class |
|---|---|---|
| Primary text | `#0f172a` | `slate-900` |
| Secondary text | `#475569` | `slate-600` |
| Tertiary text (captions, metadata) | `#94a3b8` | `slate-400` |

### Borders

| Role | Hex | Tailwind class |
|---|---|---|
| Default border | `#e2e8f0` | `slate-200` |

### Contrast rule
- Minimum 4.5:1 (WCAG AA) all text.
- Target 7:1 for clinical data display.
- Never use colour as sole information carrier.

---

## 3. Typography tokens

### Font stack

| Font | Variable | Role | Where |
|---|---|---|---|
| Newsreader | `--font-newsreader` | Serif display: hero headlines, pull-quotes, section headings | Marketing/landing pages only |
| Caveat | `--font-caveat` | Handwritten sign-off and P.S. accents | Marketing sign-offs only. One or two instances per page. |
| JetBrains Mono | `--font-mono-jb` | Section markers (§ 01), marginalia rails, captions | Marketing pages, letter grammar structural labels |
| Inter | body default | All body text, all in-app UI | Everywhere including clinical tool UIs |
| ~~Oswald~~ | — | Legacy marketing display | Do not use for new work. Newsreader is the replacement. |
| ~~Open Sans~~ | — | Deprecated | Do not use. |

All fonts loaded via `next/font/google` in root `app/layout.tsx`.

### Type scale

| Size | Tailwind | Font | Use |
|---|---|---|---|
| 48–72px | `text-5xl`–`text-7xl` | Newsreader | Marketing hero headlines |
| 36–44px | `text-4xl` | Newsreader | Marketing section headings |
| 24–30px | `text-2xl`–`text-3xl` | Inter bold | In-app page headings |
| 18–20px | `text-lg`–`text-xl` | Inter semibold | In-app subheadings, card titles |
| 16px | `text-base` | Inter | Body text, form labels |
| 14px | `text-sm` | Inter | Supporting text, descriptions |
| 12px | `text-xs` | Inter | Metadata, captions, fine print only |

### Readability rules

| Rule | Value |
|---|---|
| Minimum body font | 16px (`text-base`). 14px only for secondary text. |
| Line height | `leading-relaxed` (1.5–1.6) |
| Letter spacing | Normal to slightly open. Never tight for body. |
| Minimum weight | 400 in clinical UI. Never 300 (fails clinical lighting conditions). |

---

## 4. Spacing and layout tokens

### Max-widths

| Context | Max-width | Tailwind |
|---|---|---|
| Marketing page container | 1280px | `max-w-7xl` |
| Marketing section content | 1024px | `max-w-5xl` or `max-w-4xl` |
| Reading columns | 768px | `max-w-3xl` |
| Single-focus (pricing, forms) | 672px | `max-w-2xl` |
| Narrow cards | 512px | `max-w-xl` |

### Section padding

| Context | Classes |
|---|---|
| Marketing sections | `py-16 sm:py-24` |
| Dense in-app sections | `py-8 sm:py-12` |
| Horizontal padding | `px-4 sm:px-6` |

### Grid rules

| Rule | Value |
|---|---|
| Default column progression | 1 col (mobile) → 2 col (sm) → 3 col (lg) |
| Gap | `gap-4` tight / `gap-5`–`gap-6` breathing room |
| Maximum columns for content | 3. Use 4 only for icon-only cards. |

### Touch targets

Minimum 44×44px on all interactive elements.

### Mobile-first principles

- Forms: full-width inputs, large tap areas.
- Marketing CTAs: full-width or near-full-width on mobile.
- No horizontal scroll at any viewport.

---

## 5. Component patterns

Copy these class strings directly. Do not approximate.

### Buttons

**Primary (main action):**
```
bg-nz-green-700 text-white rounded-full px-8 py-3 font-semibold
hover:bg-nz-green-800 shadow-sm hover:shadow-[0_0_0_3px_rgba(22,163,74,0.3)]
transition-all duration-250 cubic-bezier(0.33,0,0,1)
```

**Secondary (alternative action):**
```
border border-slate-200 bg-white text-slate-800 rounded-full px-6 py-3 font-medium
hover:bg-slate-50 transition-colors duration-200
```

**Ghost / low emphasis:**
```
text-nz-green-700 font-medium hover:bg-nz-green-700/5 transition-colors duration-200
```

**Destructive:**
```
bg-red-600 text-white rounded-lg px-6 py-3 font-semibold
```

**Button rules:**
- One primary button per view. Never two primary buttons competing.
- `rounded-full` on marketing pages. `rounded-lg` acceptable in dense in-app UI.
- Never `rounded-full` on data table row actions.

### Cards

**Standard card:**
```
rounded-2xl border border-slate-200 bg-white p-5 shadow-sm
```

**Clickable card (add hover):**
```
rounded-2xl border border-slate-200 bg-white p-5 shadow-sm
hover:shadow-md transition-shadow duration-250
```

**Dark card (inside dark sections):**
```
rounded-2xl border border-white/10 bg-white/5 p-5
```

Use `shadow-sm` not `shadow-lg`. Clinical tools feel precise, not dramatic.

### Forms and inputs (clinical UI)

**Input:**
```
border border-slate-200 rounded-lg px-4 py-3 text-base text-slate-900 w-full
focus:outline-none focus:ring-2 focus:ring-nz-green-700/30 focus:border-nz-green-700
```

**Error state:**
```
border-red-500 focus:ring-red-500/30 focus:border-red-500
```

**Rules:**
- Always `text-base` (16px) for inputs.
- Labels above inputs always. Never placeholder-only.
- Error state: red border + red text label + error icon. Never colour alone.

### Alert / status badges

Always colour + icon + text label. Never colour alone.

| State | Classes |
|---|---|
| Success | `bg-green-50 border border-green-200 text-green-800` + CheckCircle icon |
| Warning | `bg-amber-50 border border-amber-200 text-amber-800` + AlertTriangle icon |
| Error | `bg-red-50 border border-red-200 text-red-800` + XCircle icon |
| Info | `bg-blue-50 border border-blue-200 text-blue-800` + Info icon |

---

## 6. Animation spec

### Library
**Framer Motion** — the sole animation library for `clinicpro-saas`. Do not use GSAP, AOS, or custom IntersectionObserver scroll logic. All animation goes through Framer Motion.

Install: `pnpm add framer-motion`

| Pattern | Framer Motion API |
|---|---|
| Scroll reveal | `whileInView` + `viewport={{ once: true, margin: "-15%" }}` |
| Hero entrance stagger | `variants` with `staggerChildren` on the parent |
| Hover lift / glow | `whileHover` on the element |
| Accordion | `AnimatePresence` + `motion.div` with `height: "auto"` / `0` |
| Counter count-up | `useMotionValue` + `useTransform` or `animate()` imperative |
| Ambient float | CSS keyframe (`@keyframes float`) — keep outside Framer for perf |
| Reduced motion | Wrap with `useReducedMotion()` hook — set all durations to `0` |
| Line mask reveal | `overflow: hidden` parent + `motion.div` animating `y: '110%' → 0` |
| Character stagger | `useInView` + per-char `overflow: hidden` span + `motion.span` animating `y: '105%' → 0` |
| Scramble rotate | `useInView` + `setInterval` at 33ms, random chars revealed left-to-right over 650ms, auto-cycles |
| Scroll-linked draw | `useEffect` scroll listener + `getBoundingClientRect()` + `useMotionValue.set()` + `useTransform` → `clipPath: inset()` |

### Signature easing curve
All marketing transitions: `cubic-bezier(0.33, 0, 0, 1)`. Pass as `ease: [0.33, 0, 0, 1]` in Framer Motion. In-app clinical UI: `"easeOut"`.

### Timing

| Category | Duration |
|---|---|
| Hover, toggle, card lift | 200–300ms |
| Scroll reveals, modal open | 600–900ms |
| Hero entrance per element | 0.9s, staggered 0.05–0.48s |
| Ambient (portrait float) | 6s |
| In-app clinical UI max | 600ms (loading states only) |

### Animation catalogue

| Animation | Spec | Trigger |
|---|---|---|
| Scroll reveal | Fade + 28px translateY, 0.7s signature easing | IntersectionObserver, `rootMargin: '0px 0px -15% 0px'`, fires once |
| Hero entrance stagger | `lg-hero-enter` class, `--hero-delay` CSS var per element: portrait 0s, marginalia 0.05s, eyebrow 0.1s, headline 0.18s, subline 0.32s, CTAs 0.48s | Page load |
| Portrait float | `translateY(0 → -8px → 0)`, 6s infinite `ease-in-out` | Continuous |
| Counter count-up | `requestAnimationFrame`, 1.5s ease-out cubic | IntersectionObserver |
| Header glass | `backdrop-blur(12px)`, 300ms | Scroll |
| Button glow | `box-shadow` ring, 250ms signature easing | Hover |
| Card lift | `translateY(-2px)` + shadow, 250ms signature easing | Hover |
| Accordion | `grid-template-rows: 0fr → 1fr`, 0.35s signature easing. ChevronDown rotate 180°, 300ms | Click |
| Line mask reveal | Per-line `overflow: hidden` div + `motion.div` with `y: '110%' → 0`, 0.85s signature easing, stagger 0.15s per line. Use for hero H1 only. | Page load |
| Character stagger (`CharStagger`) | Per-char `overflow: hidden` span + `motion.span` with `y: '105%' → 0`, 0.55s signature easing, 0.028s stagger per char. Spaces animate instantly. `useInView` triggered, fires once. Component in `letter-grammar.tsx`. | Scroll into view |
| Scramble rotate (`ScrambleRotate`) | Cycles through a `phrases` array. Each transition: random chars revealed left-to-right at 33ms tick over 650ms, then holds 2800ms before next phrase. `useInView` starts the loop. Reduced motion: plain crossfade at `holdMs` interval. Component in `letter-grammar.tsx`. | Scroll into view (loops indefinitely) |
| Scroll-linked connector | `useEffect` scroll listener (passive) reads `getBoundingClientRect().top`, maps to 0–1 progress via `useMotionValue.set()`, piped through `useTransform` to `clipPath: inset(0 X% 0 0)`. Do NOT use `useScroll` with a `target` ref — it uses `useLayoutEffect` internally and fails SSR hydration in Next.js App Router. | Scroll |

### Reusable animation components

`src/shared/components/marketing/letter-grammar.tsx` exports ready-to-use components. Use these; do not re-implement.

| Component | Purpose | Key props |
|---|---|---|
| `Reveal` | Scroll-triggered fade + translate wrapper | `delay`, `from: 'bottom' | 'left' | 'right' | 'none'` |
| `Marked` | Inline hand-underline SVG accent, draw-on-scroll | — |
| `CharStagger` | Character-by-character mask reveal | `children: string`, `delay` (ms) |
| `ScrambleRotate` | Cycling scramble/decode heading | `phrases: readonly string[]`, `holdMs`, `scrambleDurationMs` |
| `Logomark` | Viewfinder bracket + lettermark SVG | `size`, `letters` |
| `CornerBracket` | Single corner bracket SVG | `position: 'tl' | 'tr' | 'bl' | 'br'`, `size` |
| `HandUnderline` | Standalone hand-underline SVG | — |

### SSR gotcha: do not use `useScroll` with a target ref

`useScroll` uses `useLayoutEffect` internally. In Next.js App Router, `'use client'` components are still SSR'd, so `useLayoutEffect` fires before the ref is attached to the DOM — causing a hydration runtime error.

Use this pattern instead for scroll-linked animations tied to a specific element:

```tsx
const elRef = useRef<HTMLDivElement>(null);
const progress = useMotionValue(0);
useEffect(() => {
  const el = elRef.current;
  if (!el) return;
  const onScroll = () => {
    const { top } = el.getBoundingClientRect();
    const wh = window.innerHeight;
    const p = Math.max(0, Math.min(1, (wh * 0.7 - top) / (wh * 0.45)));
    progress.set(p);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  return () => window.removeEventListener('scroll', onScroll);
// eslint-disable-next-line react-hooks/exhaustive-deps
}, []);
```

Adjust the `0.7` and `0.45` constants to control when the animation starts and over what scroll distance it completes.

### Do not animate
- Page transitions
- Hover states on non-interactive elements
- Anything that delays access to information
- Any in-app clinical UI (loading states excepted)

### Reduced motion
All marketing animations use `@media (prefers-reduced-motion: reduce)`. `lg-hero-enter` and `lg-float` set `animation: none; opacity: 1`. All `letter-grammar.tsx` components respect `useReducedMotion()` — set duration to 0 or use plain crossfade.

---

## 7. Dark section patterns

### Section rhythm (homepage)

```
CREAM #fafaf7      Hero
WHITE/60           Proof strip
DARK GREEN #0c2820 Evidence section
CREAM              Tools
DARK NAVY #0f172a  Story section
CREAM              Principles, CTA, FAQ, Footer
```

### Dark background usage

| Background | Hex | Use |
|---|---|---|
| Dark forest green | `#0c2820` | Evidence/stats, featured product cards |
| Dark navy | `#0f172a` | Narrative/story sections |

Do not mix these in the same section. Do not introduce additional dark colours.

### Dark section token overrides

| Element | Class / value |
|---|---|
| Heading text | `text-white` |
| Body text | `text-white/60`–`text-white/70` |
| Supporting / citations | `text-white/30`–`text-white/40` |
| Borders | `border-white/20` (corner brackets), `border-white/10` (cards) |
| Grain texture | `lg-grain-dark` (`rgba(255,255,255,0.04)` dot grid, 22px, 20–30% opacity) |
| Glow (green sections) | `bg-nz-green-700/10 blur-3xl` |
| Glow (navy sections) | `bg-amber-500/5 blur-3xl` |
| Section marker labels | `text-amber-400/70` |
| Blockquote accent | `bg-amber-400` |

---

## 8. Voice and copy rules

### Framing

| Rule | Example |
|---|---|
| Lead with the outcome, not the feature | "Clinical photos on your desktop in 30 seconds" not "Our innovative image transfer technology..." |
| Honest about limitations | "You still attach the JPEG manually" not hiding incomplete automation |
| Use clinical language GPs know | NHI, ERMS, HealthLink, Medtech Evolution — no over-explanation |
| NZ framing | "Let's..." / "Consider..." — collaborative, not commanding |
| AU framing | Direct imperatives fine: "Start free trial" |
| No exclamation marks in clinical context | — |

### Heading style (marketing)
- Newsreader, sentence case (not uppercase, not title case)
- 3–7 words max for hero. Fragments acceptable.
- No clever wordplay. Directness is respect.

### Pricing copy
- Always state trial and ongoing price together: "1 month free · $5/month after"
- Never "completely free"
- Always include "Cancel any time" on pricing sections

---

## 9. Accessibility baseline

Non-negotiable. Clinical software accessibility has patient safety implications.

| Rule | Requirement |
|---|---|
| Contrast | 4.5:1 minimum (WCAG AA). 7:1 target for clinical data. |
| Colour redundancy | Every state uses colour + icon + text label. Never colour alone. |
| Touch targets | 44×44px minimum |
| Focus rings | Visible focus ring on all interactive elements |
| Screen reader | Semantic HTML. `aria-label` on icon-only buttons. `role` on custom components. |
| Body font size | 16px minimum. Never `text-xs` for primary content. |

---

## 10. DO-NOT list

| Anti-pattern | Reason |
|---|---|
| Purple as any accent | No clinical or NZ/AU cultural association. Looks startup-generic. |
| Gradient backgrounds (purple→pink, etc.) | Generic AI aesthetic. Signals consumer app. |
| Rounded pill on in-app data table actions | Too consumer. Use `rounded-lg`. |
| Animations that delay information access | GPs are time-pressed. |
| Gamification (streaks, badges, engagement bars) | Clinicians want reliability, not delight. |
| "Completely free" in copy | Inaccurate. Creates trust problems when pricing appears. |
| Pastel / low-saturation palette | Unserious. Healthcare needs clear contrast. |
| Stock photos of smiling doctors | NZ/AU professionals distrust stock imagery. |
| Shadcn defaults unmodified | Every component must be intentional. |
| Oswald in new marketing work | Newsreader is the replacement. |
| Oswald in clinical in-app UI | Too condensed for scanning under time pressure. |
| Inter for marketing display headings | Too neutral for impact. Use Newsreader for h1/h2. |
| Light font weights (300) in clinical data | Fails contrast in clinical lighting conditions. |
| Red as primary or accent colour | Elevates anxiety. Reserve for destructive actions only. |
| Horizontal scroll on any viewport | Breaks mobile clinical use. |
| More than one primary CTA per view | Kills decision clarity. |
| Feature tables with 10+ rows | Cognitive overload. Lead with the key benefit. |

---

*Last updated: 2026-04-22*
*Research basis: colour psychology in healthcare UI (JMIR, UXMatters, Naskay 2025), typography in clinical settings, GP workflow UX (AMA, PMC), NZ/AU cultural context. Animation patterns: Maven Clinic, Hers. New animation components (CharStagger, ScrambleRotate, scroll-linked connector) implemented on `/referral-images` landing page.*
