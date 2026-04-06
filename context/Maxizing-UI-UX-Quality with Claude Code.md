# Maximizing UI/UX Quality with Claude Code: Complete Technical Reference

Claude produces generic UI because of **distributional convergence** — it samples from the statistical center of its training data, which is dominated by Tailwind tutorials circa 2019–2024. The fix is a layered system of CLAUDE.md configuration, skills, MCP servers, and targeted prompting that steers output toward distinctive, production-grade design. This report provides every concrete technique, command, snippet, and tool needed to build that system, organized into the two target file structures.

---

# PART 1: CLAUDE-UI-GENERIC.md — Universal Best Practices

## 1. Why Claude defaults to generic UI

Anthropic officially names the root cause as **distributional convergence** (source: claude.com/blog/improving-frontend-design-through-skills, Nov 2025). During token prediction, statistically dominant patterns win. For UI, the "center of distribution" produces Inter or Roboto fonts, purple-to-blue gradients on white backgrounds, rounded card grids, and flat layouts. Claude *has* strong design knowledge — typography, color theory, spatial composition — but convergence obscures it without explicit guidance.

The critical insight is that even with anti-generic instructions, Claude can **converge to a different local maximum**. Anthropic's own blog notes: "Even with explicit instructions to avoid certain patterns, the model can default to other common choices (like Space Grotesk for typography)." This means single-layer interventions fail; you need the full stack described below.

### The altitude framework for prompting

Anthropic's engineering blog (Sep 2025) introduces the **"right altitude"** concept — the Goldilocks zone between two failure modes. **Too low altitude** means hardcoding brittle specifics like exact hex codes, which creates fragility. **Too high altitude** means vague directives like "make it professional" that assume shared context. The optimal altitude for UI guidance is specific enough to constrain behavior ("avoid Inter; prefer editorial typefaces like Playfair Display") yet flexible enough for Claude to apply judgment. Every technique in this document targets this altitude.

## 2. The CLAUDE.md foundation

CLAUDE.md is loaded into Claude's context at the start of **every session** as system prompt. It follows a hierarchical priority system where content closer to the working directory takes precedence (source: Official Anthropic docs, code.claude.com/docs/en/settings).

**Loading order (lowest to highest priority):**
1. `/etc/claude-code/CLAUDE.md` — global admin policy (always loaded)
2. `~/.claude/CLAUDE.md` — personal global instructions
3. `CLAUDE.md` or `.claude/CLAUDE.md` — project root (version-controlled)
4. `.claude/rules/*.md` — scoped rules with path-based frontmatter
5. `CLAUDE.local.md` — personal project overrides (gitignored)

The official test for inclusion: **"Would removing this line cause Claude to make a mistake on your codebase? If not, cut it."**

### Complete CLAUDE.md template for UI projects

```markdown
# Project: [Name] — [Type]

## Stack
- Framework: Next.js 15 (App Router)
- Language: TypeScript 5.x (strict mode)
- Styling: Tailwind CSS v4 + shadcn/ui
- Animation: motion/react (v12)
- Testing: Vitest (unit) + Playwright (e2e with screenshots)
- Linting: `pnpm lint` (Biome)

## Commands
- `pnpm dev` — start dev server
- `pnpm test` — run unit tests
- `pnpm test:e2e` — run Playwright (set SCREENSHOTS=1 for captures)
- `pnpm lint` — run linter

## Design System
This project uses design tokens defined in `src/styles/tokens.css`.
Always reference tokens when generating or modifying UI. Never invent
new values or use framework defaults.

@./docs/design-system.md

## Design Principles
Design is first-class. Working is not enough — it must look intentional.

### Banned Patterns (AI Slop):
- Fonts: Never use Inter, Roboto, Open Sans, Arial, Lato, Space Grotesk
- Colors: No purple gradients on white. No rainbow gradients. No pure grays
- Layout: No generic 3-card grids. No cookie-cutter hero sections
- Icons: No emojis in UI. Minimal generic icon usage
- Effects: No meaningless animations, heavy drop shadows, over-rounded cards

### Required Aesthetic:
- Typography: [Font] for headings, [Font] for body. Weight extremes (200/800)
- Color: [Direction]. Dominant color + sharp accent. Max 2 accent colors
- References: Linear, Stripe, Vercel — restrained, hierarchy through typography
- Depth: Subtle borders, no box shadows. Surface elevation via token lightness
- Motion: Intentional only. One orchestrated page-load > scattered micro-interactions

## Accessibility (WCAG 2.2 AA)
- Color contrast: 4.5:1 normal text, 3:1 large text and UI components
- All interactive elements: keyboard accessible with visible focus indicators
- All animations: behind prefers-reduced-motion media query
- All forms: labeled inputs, aria-describedby for help, aria-live for errors
- Native HTML first. ARIA only when HTML semantics are insufficient

## UI Workflow
1. Before implementing UI, describe the design direction in plan mode
2. Implement, then verify with embedded browser or `/screenshot-test`
3. Compare output against design system. Iterate 2-3 times minimum
4. Check responsive (375px, 768px, 1440px), dark mode, and a11y
5. Only commit when visual output matches design intent

## Architecture
- Components: src/components/
- Pages: src/app/
- Design tokens: src/styles/tokens.css
- Tests alongside source with .test.ts extension
```

### Scoped rules for component-level enforcement

Create `.claude/rules/ui-components.md` with path frontmatter:

```yaml
---
paths:
  - "src/components/**"
  - "*.tsx"
---
# UI Component Rules
- Use ONLY design tokens for colors, spacing, typography
- No inline hex colors. No magic pixel values
- Every interactive element needs hover, focus, active, and disabled states
- Wrap conditional renders in AnimatePresence with unique keys
- Import from motion/react, never framer-motion
- Include prefers-reduced-motion handling on all animated components
- Use cn() utility for conditional Tailwind classes
- Check existing components before creating new ones
```

**Source classification:** CLAUDE.md hierarchy and loading are **official Anthropic documentation**. The template synthesizes official guidance with community-proven patterns from DEV Community, MindStudio, and production deployments.

## 3. The essential skills stack

Skills are modular instruction packages (SKILL.md files) that Claude loads **on demand** when it detects a matching task — unlike CLAUDE.md which loads every session. They follow the open Agent Skills specification (agentskills.io, Dec 2025) adopted by both Anthropic and OpenAI.

### Minimum viable skill set (install these first)

```bash
# 1. Design quality — Official Anthropic (277K+ installs)
npx skills add anthropics/skills@frontend-design -g -y

# 2. Design linting — Official Vercel (22K stars, 133K weekly installs)
npx skills add vercel-labs/agent-skills@web-design-guidelines -g -y

# 3. Component library — Official shadcn
npx shadcn@latest add skill

# 4. Accessibility — Community (well-tested)
npx skills add supercent-io/skills-template@web-accessibility -g -y
```

### Advanced skill set (for strong brand identity)

```bash
# 5. Comprehensive design intelligence — 50+ styles, 97 palettes, 57 font pairings
npx skills add nextlevelbuilder/ui-ux-pro-max-skill@ui-ux-pro-max -g -y

# 6. Animation polish
npx skills add mblode/agent-skills@ui-animation -g -y

# 7. Google Stitch design system management
npx skills add google-labs-code/stitch-skills@shadcn-ui -g -y
```

### Multi-skill pipeline for component creation

From the Claude Code Frontend Design Toolkit (wilwaldon):
```
1. /frontend-design → Generate the component
2. /baseline-ui → Fix spacing, typography, states
3. /fixing-accessibility → Keyboard, labels, focus, semantics
4. /fixing-motion-performance → Reduced-motion, perf budgets
```

### Writing a custom SKILL.md for your design system

```yaml
---
name: my-design-system
description: |
  Enforce project design system tokens, component patterns, and WCAG AA
  standards when building frontend code. Activate when creating, modifying,
  or reviewing React components, pages, layouts, or any UI. Also activate
  for terms: "component", "button", "card", "modal", "theme", "dark mode",
  "responsive", "design system", "tokens", or any styling task.
---

# [Project] Design System

## Tokens
Load `references/tokens.md` for complete definitions.

## Typography
- Display: [Font] (700, 800)
- Body: [Font] (300, 400)
- Scale: text-xs through text-6xl, rem-based

## Component Patterns
- Use shadcn/ui as the component base
- Compose with Radix UI primitives
- Use cn() for conditional classes
- Every interactive element needs focus-visible state

## Animation
- Use motion/react for React animations
- Restrict to transform and opacity (compositor properties)
- Respect prefers-reduced-motion
- Entry: fade + slight translateY (200-300ms, ease-out)

## Accessibility
- Contrast ratio ≥ 4.5:1 (AA)
- Keyboard navigable, focus indicators visible
- ARIA labels on icon-only buttons
```

**Key optimization for auto-activation:** Descriptions should be "pushy" — Claude tends to under-trigger skills. Front-load keywords in the first **250 characters** (the budget cap). Use third-person perspective. List specific trigger phrases including common synonyms.

**Skill architecture principle:** Process goes in SKILL.md, context goes in `references/` files. Keep SKILL.md under 500 lines. This improves consistency because Claude's working memory is limited and top-of-file instructions receive more attention.

### Skill registries overview

| Registry | URL | Size | Quality Signal |
|----------|-----|------|----------------|
| **skills.sh** | skills.sh | Showcase for `npx skills` CLI | Used by official CLI |
| **playbooks.com** | playbooks.com/skills | Skills + bundles | Curated collections |
| **fastmcp.me** | fastmcp.me / mcp.directory | 3,000+ MCP + skills | Largest directory |
| **awesomeskill.ai** | awesomeskill.ai | 50,000+ skills | Min 2-star filter |
| **mcpmarket.com** | mcpmarket.com | Skills + MCP marketplace | Detailed skill pages |
| **tessl.io** | tessl.io/registry/skills | Scored skills | Validation/Review scores |
| **awesome-skills.com** | awesome-skills.com | 146+ curated | Security review badges |

**Security warning:** Skills can execute arbitrary code. Treat community skills like open-source dependencies — read SKILL.md and all scripts before installing. awesome-skills.com provides security badges for code execution, network access, and credential usage.

## 4. MCP server integrations

Configure MCP servers in `.mcp.json` at project root (shared via git) or via `claude mcp add` CLI.

### The complete UI/UX MCP stack

```json
{
  "mcpServers": {
    "figma": {
      "url": "https://mcp.figma.com/mcp",
      "type": "http"
    },
    "shadcn": {
      "command": "pnpm",
      "args": ["dlx", "shadcn@latest", "mcp", "serve"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "accesslint": {
      "command": "npx",
      "args": ["-y", "@accesslint/mcp"]
    },
    "motion": {
      "command": "npx",
      "args": ["-y", "https://api.motion.dev/registry.tgz?package=motion-studio-mcp&version=latest"]
    },
    "storybook": {
      "transport": "http",
      "url": "http://localhost:6006/mcp"
    }
  }
}
```

**Figma MCP** (Official, production): Design-to-code via frame selection or link pasting. Code-to-canvas capture for review. Write-to-canvas in beta. Rate limits: free seats get **6 calls/month**; paid Dev/Full seats get per-minute limits. Remote server recommended over desktop.

**shadcn MCP** (Official, v3.0): Real-time component specs, proper TypeScript interfaces, accurate install commands. Without it, Claude hallucinates component props. Setup: `pnpm dlx shadcn@latest mcp init --client claude`. Add a GitHub PAT to avoid 60/hr rate limit (→ 5,000/hr).

**Playwright MCP** (Official Microsoft, production): Navigate, click, fill, screenshot, generate PDFs, accessibility snapshots. **Recommended over deprecated Puppeteer MCP**. Cross-browser (Chromium, Firefox, WebKit).

**AccessLint MCP** (Official AccessLint, production): Three tools — `contrast_ratio`, `analyze_color_pair`, `suggest_accessible_color`. 92 rules covering 23 WCAG 2.1 success criteria. Single-digit millisecond audits, purpose-built for agentic loops.

**Motion Studio MCP** (Official Motion, production): AI context for full Motion docs, 330+ examples codex, CSS spring generation, transition visualization. Premium features require Motion+ membership. Free `/motion` and `/motion-audit` skills included.

**Storybook MCP** (Official Storybook, experimental): `@storybook/addon-mcp` runs MCP server within Storybook dev server. Requires Node.js 24+. APIs may change.

**Verification:** Run `/mcp` inside Claude Code to check server status. Always restart Claude Code after config changes — MCP connections initialize at startup.

## 5. The anti-generic prompting system

### The official ~400-token aesthetics prompt

This is the canonical anti-slop prompt from Anthropic's cookbook (platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics). Append it to CLAUDE.md or use via the `frontend-design` skill:

```xml
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend
design, this creates what users call the "AI slop" aesthetic. Avoid this:
make creative, distinctive frontends that surprise and delight. Focus on:

Typography: Choose fonts that are beautiful, unique, and interesting. Never
use Inter, Roboto, Open Sans, Lato, default system fonts. Impact choices:
Code aesthetic (JetBrains Mono, Fira Code), Editorial (Playfair Display,
Crimson Pro, Fraunces), Startup (Clash Display, Satoshi, Cabinet Grotesk),
Technical (IBM Plex family), Distinctive (Bricolage Grotesque, Newsreader).
Use weight extremes: 100/200 vs 800/900. Size jumps of 3x+.

Color & Theme: Use CSS variables for consistency. Dominant colors with sharp
accents outperform timid, evenly-distributed palettes. Draw from IDE themes
and cultural aesthetics for inspiration.

Motion: Prioritize CSS-only solutions for HTML. Use Motion library for React.
One well-orchestrated page load with staggered reveals > scattered micro-interactions.

Backgrounds: Create atmosphere and depth. Layer CSS gradients, geometric
patterns, or contextual effects. Never default to solid colors.

Avoid: Overused fonts, purple gradients on white, predictable layouts,
cookie-cutter design. You still converge on common choices (Space Grotesk)
across generations. Think outside the box!
</frontend_aesthetics>
```

### Typography ban list and recommendations

**Permanently ban** (in CLAUDE.md): Inter, Roboto, Open Sans, Lato, Arial, Space Grotesk, system font stacks.

**Recommended by category** (from official cookbook):

- **Code/Technical:** JetBrains Mono, Fira Code, IBM Plex Mono
- **Editorial:** Playfair Display, Crimson Pro, Fraunces, Newsreader
- **Startup/Modern:** Clash Display, Satoshi, Cabinet Grotesk
- **Technical/Corporate:** IBM Plex Sans, IBM Plex Serif, Source Sans 3
- **Distinctive:** Bricolage Grotesque, Obviously

**Weight extremes technique:** Use 100/200 for light text and 800/900 for bold — never the default 400/600/700 middle ground. Size jumps should be **3x+** (e.g., 48px heading / 14px body), not 1.5x. Load from Google Fonts; never rely on system font stacks.

### Color system architecture

**Use OKLCH color space** for perceptually uniform palettes. Equal numerical changes produce equal visual changes across all hues — no hue drift when adjusting lightness (unlike HSL where blues shift purple).

```css
:root {
  /* Brand-tinted neutrals — add tiny chroma matching brand hue */
  --neutral-50: oklch(0.98 0.005 250);   /* slight cool tint */
  --neutral-100: oklch(0.95 0.01 250);
  --neutral-900: oklch(0.15 0.02 250);

  /* Dominant + sharp accent pattern */
  --color-primary: oklch(0.55 0.27 270);
  --color-accent: oklch(0.70 0.25 150);  /* different hue for contrast */
  --color-text: oklch(0.95 0.01 270);
  --color-muted: oklch(0.60 0.05 270);
}
```

The key principle from official sources: **"Dominant colors with sharp accents outperform timid, evenly-distributed palettes."** Pick one dominant color and one sharp accent on a different hue. Never distribute colors evenly.

### Layout anti-patterns and alternatives

The single most common AI UI pattern is three equal cards in a row. The official SKILL.md counters with: **"Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements."**

Prompt for specific layout types:
- "Bento grid with mixed-size tiles" instead of "card grid"
- "Asymmetric 60/40 split" instead of "two columns"
- "Editorial magazine layout with overlapping elements" for content pages
- "Use CSS Grid with named grid areas" to force intentional structure

### Named aesthetic themes

These descriptors produce reliably distinct output:

| Theme | Key Characteristics |
|-------|-------------------|
| **OLED Luxury** | Pure black (#000) bg, gold/champagne accents, spotlight effects |
| **Solarpunk** | Warm greens/golds, organic + technical, hopeful atmosphere |
| **Swiss Minimalism** | Black + white + one accent (red), massive typography, rigid grid |
| **Brutalism** | 3-4px borders, hard shadows, broken grids, limited palette |
| **Glassmorphism** | Translucent panels, backdrop-blur, mesh gradient backgrounds |
| **Editorial/Magazine** | Asymmetric columns, display serifs, overlapping images |

**Theme constraint prompt pattern** (from official cookbook):

```xml
<always_use_[theme]_theme>
Always design with [Theme] aesthetic:
- [Color palette specifics]
- [Shape/texture characteristics]
- [Typography direction]
- [Atmosphere/mood]
</always_use_[theme]_theme>
```

### Brand vocabulary that steers output

- "calm clinical" → clean whites, subtle blue accents, generous whitespace
- "premium monochrome" → black/white only, dramatic typography, high contrast
- "warm brutalist" → raw textures + warm earth tones, thick borders
- "industrial utilitarian" → monospace fonts, data-heavy, minimal decoration
- "luxury refined" → dark backgrounds, gold accents, thin fonts, generous spacing

## 6. Visual verification and iteration discipline

### The screenshot round-trip workflow

**Method 1 — Built-in browser (recommended):** Claude Code Desktop includes autoVerify, which is **on by default**. After editing files, Claude starts the dev server, screenshots the running app via embedded browser, identifies issues, and iterates automatically.

**Method 2 — Claude in Chrome extension** (Beta, paid plans): Start Claude Code with `claude --chrome`. Claude can navigate your running app, click buttons, fill forms, read console errors, and take screenshots using your browser's login state. Available for Chrome and Edge only.

**Method 3 — Playwright MCP:** For programmatic verification at specific viewports:
```
Open localhost:3000/dashboard at 375px width, take a screenshot,
then at 1440px width. Compare both against the design tokens and
report any spacing, typography, or contrast issues.
```

**Method 4 — Custom screenshot harness:** Add to CLAUDE.md:
```markdown
System tests support automatic screenshot capture via `SCREENSHOTS=1`.
Use the `/screenshot-test` skill to run system tests and visually examine
every captured screenshot.
```

### The 2-3 iteration protocol

Add this to CLAUDE.md to prevent "one-shot and done" UI:
```markdown
### UI Iteration Protocol
After any UI change:
1. Build the change
2. Verify visually (embedded browser, Chrome, or screenshot)
3. If issues found, fix and verify again
4. Minimum 2 iterations before declaring done
5. Final iteration: check responsive + dark mode + accessibility
Never ship UI after a single generation without visual verification.
```

**Reliability note:** autoVerify works well for layout and visual issues but may miss subtle contrast failures or motion timing problems. Supplement with AccessLint MCP for contrast and manual review for animation quality.

## 7. Accessibility integration

### WCAG 2.2 AA in Claude Code workflow

WCAG 2.2 (Oct 2023) adds 6 new AA criteria beyond 2.1's 50, including **Focus Not Obscured** (2.4.11), **Target Size Minimum of 24×24px** (2.5.8), **Consistent Help placement** (3.2.6), **Redundant Entry prevention** (3.3.7), and **Accessible Authentication** (3.3.8). Core ratios remain **4.5:1** for normal text and **3:1** for large text and UI components.

### Effective audit prompts

**Full audit:**
```
Run a WCAG 2.2 AA accessibility audit on [component/page]:
1. Semantic HTML (prefer native elements over ARIA)
2. Keyboard navigation and focus management
3. Color contrast ratios (4.5:1 text, 3:1 large text/UI)
4. ARIA attribute validity
5. Screen reader announcements for dynamic content
6. Focus not obscured by sticky elements (2.4.11)
7. Target sizes ≥24×24 CSS pixels (2.5.8)
8. Form labels and error messages
Group findings by pattern, not individual instances.
```

**Quick contrast check:**
```
Check all text colors in our design tokens against background colors.
Report any pair failing WCAG AA. For each failure, suggest the closest
passing color using oklch adjustments.
```

### Common AI-generated accessibility mistakes

The most frequent errors in Claude-generated code: using `<div>` with `role="button"` instead of `<button>`, modals without focus trapping, missing `aria-live` on dynamic content, `aria-hidden="true"` on functional elements, and missing keyboard event handlers on custom interactive elements. **The First Rule of ARIA: "No ARIA is better than bad ARIA."** Always prefer native HTML semantics.

### Reduced-motion as first-class constraint

```css
/* Global safety net — add to globals.css */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0s !important;
  }
}
```

For Motion library, wrap your app in `<MotionConfig reducedMotion="user">`. Prompt Claude: "Never remove all animation for reduced-motion — reduce or simplify it. Provide clear hover/focus indicators even without motion."

## 8. Recurring maintenance patterns

### Post-ship audit prompt

```
POST-SHIP UI AUDIT: Review UI changes in the last commit:
1. Visual consistency with existing patterns
2. Responsive at 375px, 768px, 1440px
3. Dark mode compatibility
4. Accessibility (keyboard, screen reader, contrast)
5. Loading, error, and empty states
Report issues by severity: blocking, should-fix, nice-to-have.
```

### Design drift detection prompt

```
DESIGN DRIFT CHECK: Scan codebase for design system violations:
1. HARDCODED COLORS: hex/rgb/hsl not from tokens
2. ROGUE SPACING: padding/margin not matching spacing scale
3. DUPLICATE COMPONENTS: multiple components serving same purpose
4. TOKEN OVERRIDES: !important declarations and inline styles
5. TYPOGRAPHY: text not using type scale, arbitrary font sizes
For each violation, show file:line and the correct token to use.
```

**Tool:** Buoy (buoy.design) — watches every PR for hardcoded colors, token violations, and rogue components. Deterministic (no LLMs), MIT licensed.

### Quarterly health check prompt

```
QUARTERLY UI HEALTH CHECK:
1. Design drift audit (tokens, spacing, colors, components)
2. Dependency audit (outdated UI libs, security vulnerabilities)
3. Dead code removal (unused CSS, orphaned components, unused assets)
4. Full WCAG 2.2 AA regression audit vs last quarter baseline
5. Component inventory: list all, flag any not in design system
```

---

# PART 2: CLAUDE-UI-TECHNIQUES.md — Advanced Techniques and Tools

## 1. Design token system with Tailwind v4

Tailwind v4 replaces `tailwind.config.js` with the CSS `@theme` directive. Variables declared in `@theme {}` **automatically generate utility classes** — `--color-primary` creates `bg-primary`, `text-primary`, etc.

### Complete token architecture

```css
/* src/styles/globals.css */
@import "tailwindcss";

@custom-variant dark (&:is(.dark *));

@theme inline {
  /* Colors — use @theme inline to keep var() references live */
  --color-background: var(--bg);
  --color-foreground: var(--fg);
  --color-primary: var(--primary);
  --color-surface: var(--surface);
  --color-muted: var(--muted);
  --color-border: var(--border);
  --color-accent: var(--accent);
  --color-destructive: var(--destructive);

  /* Typography */
  --font-display: "Satoshi", sans-serif;
  --font-body: "IBM Plex Sans", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Motion tokens */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-moderate: 350ms;
  --duration-slow: 500ms;

  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.2, 0, 0, 1.4);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}

@layer base {
  :root {
    --bg: oklch(0.98 0.005 250);
    --fg: oklch(0.15 0.02 250);
    --primary: oklch(0.55 0.27 270);
    --surface: oklch(0.96 0.008 250);
    --muted: oklch(0.55 0.03 250);
    --border: oklch(0.88 0.01 250);
    --accent: oklch(0.70 0.25 150);
    --destructive: oklch(0.55 0.22 25);
  }

  .dark {
    --bg: oklch(0.15 0.02 250);
    --fg: oklch(0.95 0.01 250);
    --primary: oklch(0.70 0.20 270);
    --surface: oklch(0.20 0.02 250);
    --muted: oklch(0.60 0.03 250);
    --border: oklch(0.30 0.02 250);
    --accent: oklch(0.75 0.22 150);
    --destructive: oklch(0.65 0.20 25);
  }
}

/* Reduced-motion safety net */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0s !important;
  }
}
```

### Three-tier token naming convention

**Tier 1 — Primitives** (raw values): `--color-blue-500: oklch(0.623 0.214 259.1)`
**Tier 2 — Semantic** (intent-based): `--color-surface-primary`, `--color-text-muted`, `--color-accent-hover`
**Tier 3 — Component** (optional, for large systems): `--button-bg`, `--card-border`, `--input-border-focus`

The semantic tier uses this naming pattern: `--color-{category}-{variant}` where categories are `surface`, `text`, `border`, `accent`, `status`. Components reference semantic tokens, never primitives directly.

### Tailwind v3 vs v4 migration notes

| Feature | v3 | v4 |
|---------|----|----|
| Config | `tailwind.config.js` (JS) | `@theme {}` in CSS |
| Dark mode | `darkMode: 'class'` in JS | `@custom-variant dark (&:is(.dark *))` in CSS |
| Custom colors | `theme.extend.colors` in JS | `--color-*` in `@theme {}` |
| Easing/duration | `theme.extend.transitionTimingFunction` | `--ease-*` / `--duration-*` in `@theme {}` |
| Content detection | Manual `content: [...]` | Automatic |
| Plugins | `plugins: [...]` in JS | `@plugin "package-name"` in CSS |

## 2. Dark mode architecture

### No-flash implementation with next-themes

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
"use client";
import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

// app/layout.tsx
import { Providers } from "./providers";

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

**Why `suppressHydrationWarning`:** next-themes injects a blocking `<script>` into `<head>` that adds the `dark` class before any content renders. This prevents flash-of-wrong-theme under all conditions — but causes a React hydration mismatch warning that `suppressHydrationWarning` silences.

**Theme toggle must check `mounted`:**
```tsx
"use client";
import { useState, useEffect } from "react";
import { useTheme } from "next-themes";

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const { setTheme, resolvedTheme } = useTheme();
  useEffect(() => setMounted(true), []);
  if (!mounted) return null; // Prevents hydration mismatch
  return (
    <button onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}>
      {resolvedTheme === "dark" ? "☀️" : "🌙"}
    </button>
  );
}
```

When using CSS variables with `@theme inline`, components don't need `dark:` prefixes — the same `bg-background text-foreground` classes automatically adapt.

## 3. Animation and motion patterns

### CSS-only vs Motion library decision

Use **CSS** for: simple transitions, hover states, single-property fades, anything without exit animations. Use **motion/react** when you need: exit animations (`AnimatePresence`), layout animations, spring physics, gesture tracking, scroll-linked animations, or coordinated parent-child sequences.

**Import change:** The package is now `motion` (not `framer-motion`). Import from `motion/react`:
```js
import { motion, AnimatePresence } from "motion/react";
```

### Key motion patterns

**Staggered children (the highest-impact pattern):**
```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08, delayChildren: 0.15 },
  },
};

const item = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((i) => <motion.li key={i} variants={item} />)}
</motion.ul>
```

**Spring physics presets:**
- **Snappy button:** `{ type: "spring", stiffness: 400, damping: 30 }`
- **Gentle entrance:** `{ type: "spring", stiffness: 100, damping: 20, mass: 0.5 }`
- **Bouncy:** `{ type: "spring", stiffness: 300, damping: 15 }`
- **No bounce (overdamped):** `{ type: "spring", stiffness: 200, damping: 40 }`

**Scroll-triggered reveal:**
```jsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
/>
```

**Page transitions (Next.js App Router):**
```tsx
// app/template.tsx
"use client";
import { motion, AnimatePresence } from "motion/react";

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### LazyMotion for production bundles

Full `motion` component is ~34kb. `LazyMotion` + `m` component reduces initial payload to **~4.6-6kb**:

```jsx
import { LazyMotion, domAnimation } from "motion/react";
import * as m from "motion/react-m";

<LazyMotion features={domAnimation} strict>
  <m.div animate={{ opacity: 1 }} />
</LazyMotion>
```

Use `domAnimation` (~15kb, covers animate/variants/exit/layout) for most apps. `domMax` adds drag and advanced layout. The `strict` prop throws errors if `motion.*` is accidentally used instead of `m.*`.

### GPU compositing tier list

**S-tier (compositor thread, 60-120fps):** `transform`, `opacity`, `filter`, `clip-path`
**C-tier (triggers paint):** `background-color`, `color`, `box-shadow`, CSS variables
**D-tier (triggers layout — avoid):** `width`, `height`, `padding`, `margin`, `top`, `left`

**Anti-patterns:** Never animate `width`/`height` directly (use `transform: scale()`). Don't apply `will-change` to more than 3-4 elements. Limit concurrent transform animations on mobile to 3-4.

### Motion audit prompt

```
MOTION AUDIT: Scan all animations in this project:
1. List every CSS animation, transition, and motion/react usage
2. Classify by GPU compositing tier (S/A/C/D/F from motion.dev)
3. Check: does every animation have reduced-motion handling?
4. Check: are durations using design tokens, not magic numbers?
5. Check: are spring configs shared via constants, not duplicated?
6. Check: does every AnimatePresence have exit matching entrance?
7. Generate performance improvement plan for any C-tier or below.
```

## 4. Background and atmosphere techniques

### Gradient layering (CSS-only, zero JS)

```css
.atmospheric-bg {
  background:
    radial-gradient(circle at 20% 50%, oklch(0.6 0.15 30 / 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, oklch(0.7 0.12 60 / 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, oklch(0.5 0.15 270 / 0.3) 0%, transparent 50%),
    var(--color-background);
}
```

### Noise texture overlay (SVG, lightweight)

```css
.noise-overlay::after {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.03;
  background: url("data:image/svg+xml,<svg viewBox='0 0 250 250' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.45' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  pointer-events: none;
}
```

### Glassmorphism

```css
.glass-card {
  background: oklch(1 0 0 / 0.15);
  backdrop-filter: blur(10px) saturate(150%);
  border: 1px solid oklch(1 0 0 / 0.2);
  border-radius: 16px;
}
```

**Performance note:** `backdrop-filter: blur()` is GPU-accelerated but expensive on large areas. Limit to card-sized elements. Test on mobile.

## 5. Figma MCP advanced workflow

### Design-to-code flow

```
1. Select a frame in Figma (or copy its URL)
2. In Claude Code: "Implement this Figma frame as a React component
   using our design tokens. Match the layout with CSS Grid."
3. Claude uses Figma MCP to extract layout, typography, colors, spacing
4. Verify output with Playwright MCP at the correct viewport
5. Iterate 2-3 times for accuracy
```

### Code-to-Figma capture

```
Start a local server for my app and capture the /dashboard page
into a new Figma file for design review.
```

This uses the remote MCP server's write-to-canvas capability (beta, free during beta period).

### Limitations to know

- Cannot surgically update existing code; often requires regeneration
- Complex multi-frame flows require per-frame conversion
- Free/View seats: **6 tool calls per month** (upgrade to Dev seat for per-minute limits)
- Write-to-canvas requires remote server and is beta only

## 6. AccessLint advanced integration

### Full plugin installation

```bash
claude plugin marketplace add accesslint/claude-marketplace
claude plugin install accesslint@accesslint
```

**Agents provided:**
- `accesslint:reviewer` — multi-step WCAG 2.1 A/AA code review
- `accesslint:fixer` — auto-fixes accessibility issues across files

**Skills provided:**
- `accesslint:contrast-checker` — interactive color contrast checking
- `accesslint:use-of-color` — WCAG 1.4.1 compliance checking

### Contrast validation in token generation

```
When generating design tokens, validate every foreground/background pair
against WCAG AA using the AccessLint MCP contrast_ratio tool. Reject any
body text combination below 4.5:1. For each rejection, use the
suggest_accessible_color tool to find the closest passing alternative.
```

### Supplementary accessibility tools

```bash
# axe-core-based page audit
claude mcp add a11y -- npx -y a11y-mcp

# Playwright + axe-core with visual annotations
claude mcp add mcp-accessibility-scanner -s user -- npx -y mcp-accessibility-scanner
```

## 7. The Taste Skill's parametric approach

The Taste Skill (6.6K stars, community) provides three adjustable dials:

- **DESIGN_VARIANCE (1-10):** 1 = clean centered layout → 10 = asymmetric modern
- **MOTION_INTENSITY (1-10):** 1 = simple hover → 10 = magnetic scroll-triggered
- **VISUAL_DENSITY (1-10):** 1 = luxury airy spacing → 10 = dense compact

Install: `npx skills add https://github.com/Leonxlnx/taste-skill`

This is **community/experimental** but widely referenced. Useful for rapid prototyping where you want to dial aesthetic parameters without writing full theme constraints.

## 8. Performance audit integration

### Core Web Vitals prompt

```
PERFORMANCE AUDIT — run against [page URLs]:
1. LCP target: <2.5s. Identify largest contentful paint element.
2. INP target: <200ms. Find slow event handlers.
3. CLS target: <0.1. Find layout shifts (missing dimensions, dynamic content).
4. Bundle analysis: total size, largest chunks, candidates for code-splitting.
5. Image optimization: lazy loading, explicit dimensions, modern formats.
6. Font loading: verify font-display: swap on all custom fonts.
For each issue, provide the specific fix with code.
```

### Available performance skills

- **Core Web Vitals Analyzer** (ccforseo): `cp -r seo-skills/core-web-vitals ~/.claude/skills/core-web-vitals`
- **react-nextjs-performance** (Vercel): Server Components optimization, bundle splitting
- **lighthouse-skills**: Framework-aware (Next.js, Vue/Nuxt, Svelte) performance auditing

## 9. Healthcare and SaaS-specific UI patterns

### Clinical accessibility requirements

Healthcare interfaces need stricter standards than WCAG minimums. Body text minimum **16px** (not 14px). Touch targets **≥44×44px** (not WCAG's 24px minimum). Test contrast in both bright clinical rooms and dim mobile screens. Support elderly users with motor impairments — generous click targets and forgiving input areas.

### PHI display rules for frontend

**Never display patient identifiers in:** URLs, page titles, browser tab names, error messages, debug logs, localStorage, or sessionStorage. Mask sensitive fields by default with click-to-reveal. Auto-lock sessions after inactivity with visible countdown and re-auth flow. Clear clipboard after copy of sensitive data. Log every PHI display event for audit trail.

### Trust signals in clinical interfaces

- **Red** = critical alerts only (never overuse — causes alert fatigue)
- **Amber/Yellow** = warnings requiring attention
- **Green** = normal/confirmed status
- **Blue** = informational content
- Never use red for primary action buttons
- Professional typography — no playful or casual styles
- Calming palette: soft blues, whites, light greys for primary UI
- Show encryption status, compliance badges, data sovereignty indicators

### Clinical form UX

```
CLINICAL FORM UX CHECKLIST:
1. Smart defaults based on clinical context
2. Real-time validation, not submit-time
3. Inline errors next to the field
4. Auto-save with explicit "Save as Draft" vs "Finalize"
5. Support clinical shortcuts ("T" for today's date)
6. Structured capture (dropdowns for ICD codes) + free text for notes
7. Undo capability for accidental changes
8. Tab order follows clinical workflow, not visual layout
9. Date pickers that allow manual entry
```

### CLAUDE.md section for healthcare projects

```markdown
## Healthcare Compliance
- Never display patient identifiers in URLs, page titles, or error messages
- Session timeout: visible countdown + accessible re-auth
- PHI display: minimum necessary, masked by default with click-to-reveal
- Critical alerts: role="alert", multi-modal (visual + text), require acknowledgment
- All clinical data entry: real-time validation, auto-save, undo support
- Touch targets: ≥44×44px (above WCAG 24px minimum)
- Font size: ≥16px body text, ≥14px labels
- Color never the only indicator — pair with icons + text labels
```

---

# SETUP RECOMMENDATIONS

## Minimum viable setup (new Next.js/TS/Tailwind/shadcn project)

```bash
# 1. Project init
npx create-next-app@latest --typescript --tailwind --app --src-dir

# 2. shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card input label

# 3. Dark mode
npm install next-themes

# 4. Essential skills
npx skills add anthropics/skills@frontend-design -g -y
npx skills add vercel-labs/agent-skills@web-design-guidelines -g -y
npx shadcn@latest add skill
npx skills add supercent-io/skills-template@web-accessibility -g -y

# 5. Essential MCP servers (add to .mcp.json)
pnpm dlx shadcn@latest mcp init --client claude
claude mcp add playwright npx @playwright/mcp@latest
claude mcp add accesslint -- npx -y @accesslint/mcp

# 6. Create CLAUDE.md with the template from Part 1, Section 2
# 7. Create globals.css with the token system from Part 2, Section 1
```

## Advanced setup (strong brand identity)

All of the above, plus:

```bash
# Additional skills
npx skills add nextlevelbuilder/ui-ux-pro-max-skill@ui-ux-pro-max -g -y
npx skills add mblode/agent-skills@ui-animation -g -y

# Motion library
npm install motion

# Additional MCP servers
# Add to .mcp.json: Figma MCP, Motion Studio MCP, Storybook MCP

# Custom design system skill
mkdir -p .claude/skills/design-system
# Create SKILL.md with project-specific tokens, components, patterns

# Scoped rules
mkdir -p .claude/rules
# Create ui-components.md with path frontmatter for src/components/**

# AccessLint full plugin
claude plugin marketplace add accesslint/claude-marketplace
claude plugin install accesslint@accesslint
```

---

# SOURCE CLASSIFICATION SUMMARY

| Category | Source | Reliability |
|----------|--------|-------------|
| Distributional convergence, altitude concept | **Official Anthropic** (blog + engineering) | Canonical |
| ~400-token aesthetics prompt | **Official Anthropic Cookbook** | Canonical |
| CLAUDE.md hierarchy, loading, rules | **Official Anthropic Docs** | Canonical |
| frontend-design skill | **Official Anthropic** (277K installs) | Canonical |
| web-design-guidelines skill | **Official Vercel** (22K stars) | High reliability |
| shadcn MCP v3.0 | **Official shadcn** | High reliability |
| Figma MCP (remote) | **Official Figma** | High reliability |
| Playwright MCP | **Official Microsoft** | High reliability |
| AccessLint MCP + plugin | **Official AccessLint** | High reliability |
| Motion Studio MCP | **Official Motion** | High reliability (commercial) |
| Storybook MCP addon | **Official Storybook** | Experimental — APIs may change |
| ui-ux-pro-max skill | **Community** (popular) | Medium-high |
| Taste Skill | **Community** (6.6K stars) | Experimental |
| Named aesthetic themes | **Mixed** (official cookbook + community demos) | Well-documented |
| OKLCH token architecture | **Web standards** + community patterns | Well-established |
| next-themes dark mode | **Community** (de facto standard) | Well-established |
| Screenshot round-trip | **Community** (multiple approaches) | Emerging |
| Design drift detection | **Community** (Buoy tool, emerging) | Emerging |
| Healthcare UI patterns | **Industry standard** (HIPAA/WCAG) | Well-established |

**Known unreliabilities:** Skill install numbers are community-reported and not independently verified. Space Grotesk convergence occurs even with anti-generic prompting — explicitly ban it. The Storybook MCP requires Node.js 24+ and has unstable APIs. Figma MCP free-tier rate limits (6 calls/month) make it impractical without a paid seat. autoVerify may miss subtle contrast and animation timing issues.