---
title: "Miozuki: Strategy Action Plan"
created: 2026-04-26
status: draft
tags: [miozuki, strategy, action-plan]
---

# Miozuki: Strategy Action Plan

**Compiled:** 2026-04-26
**Source:** Selective review of 10 strategy documents across SEO, content, backlinks, tooling, community, and commercial themes.
**Status:** First draft. Requires Ryo's review before creating tasks or acting.

This document is the single authoritative output of the strategy review session. All source documents in `inbox/miozuki/` can be deleted once this is approved.

---

## Constraints (always apply)

- Solo founder (Ryo). Limited weekly hours on Miozuki.
- Pre-revenue: no confirmed marketing budget.
- Stack: Next.js + Shopify Storefront API + Vercel. Developer available but not full-time.
- NZ market is small. Low-volume, high-intent plays beat broad reach.
- All output is first draft only. Human review required before any content goes live.

---

## Phase 0: This Week (Urgent, Time-Sensitive)

Mother's Day NZ is 10 May 2026. Fourteen days away. Editorial decisions are being made now.

### 0.1 Pitch Viva (NZ Herald) for Mother's Day

**What:** Email Viva pitching Miozuki's pearl jewellery range as a Mother's Day gift feature.
**Pitch angles:**
- "Pearl jewellery as a Mother's Day gift" -- pearl is the traditional gift for mothers, directly on-brief
- "Ethical gifting for Mum -- why moissanite and pearl are gaining ground in NZ"
- "NZ fine jewellery under $500 for Mother's Day"

**Contact:** viva@nzherald.co.nz (verify before sending)
**Prereq:** miozuki.co.nz must have a live pearl product page and a credible About/brand page before pitching. Verify hi-res product photography is available -- Viva editorial requires it.
**Effort:** Medium (2-3 hours including writing the pitch)

### 0.2 Submit to Fashion Quarterly

**What:** Submit via the FQ Living project submission form at fq.co.nz/fq-living-project-submission/
**Why:** Lowest-risk editorial entry point for a new NZ brand. Quarterly publication, accessible submission process.
**Effort:** Low (30 minutes)

### 0.3 Register on SourceBottle

**What:** Register at sourcebottle.com (free, 10 minutes). Set category alerts for: jewellery, weddings, engagement, ethical shopping, sustainable fashion, consumer trends NZ.
**Why:** NZ's primary journalist query platform (HARO equivalent). Live queries only visible inside a registered account. Every day unregistered is a missed opportunity. One Stuff or Viva placement from SourceBottle is worth 20 directory backlinks in SEO authority.
**Effort:** 10 minutes to register; ongoing async (respond to queries as they arrive)

### 0.4 Submit to NZ Business Directories

**What:** Submit to all five directories in a single session. Combined effort under 2 hours.

| Directory | URL | Cost |
|---|---|---|
| Finda.co.nz | finda.co.nz | Free |
| Yellow NZ | yellow.co.nz | Free |
| Google Business Profile | business.google.com | Free |
| Green Directory NZ | greendirectory.co.nz | Free basic |
| Hotfrog NZ | hotfrog.co.nz | Free |

**Why:** Establishes NAP (Name/Address/Phone) consistency across NZ directories. Google cross-references these for local trust signals. Backlinks go live within days.
**Effort:** Under 2 hours combined

### 0.5 Inquire: Wild Hearts Wedding Fairs

**What:** Email hello@wildhearts.co.nz asking about 2026 event dates and jewellery exhibitor availability. Even if 2026 is booked, request to be on the 2027 waitlist and in their vendor database.
**Why:** Premium Auckland wedding fair series. Exhibitors listed on wildhearts.co.nz; backlink potential within 4-8 weeks if a 2026 slot is available.
**Effort:** 5 minutes

### 0.6 Register: WeddingWise and My Wedding Guide

**What:** Register free vendor listings at weddingwise.co.nz and myweddingguide.co.nz.
**Why:** Free, topically relevant, low-DA but builds out the wedding vendor directory presence. 30 minutes combined.
**Effort:** Low

### 0.7 Verify: Shopify Agentic Storefronts NZ Eligibility

**What:** Check shopify.com/editions/winter2026 and the Shopify partner portal to confirm whether Agentic Storefronts (product discovery in ChatGPT, Perplexity, Google AI Mode) is live for NZ merchants. March 2026 rollout was US-only.
**Why:** If available, this is free AI discovery channel exposure at zero ongoing cost. Enable immediately if eligible.
**Effort:** 10 minutes

### 0.8 Enable Shopify Inbox AI

**What:** Enable Shopify Inbox in the Miozuki Shopify admin. Activate AI suggested replies.
**Why:** Zero cost. Handles basic inbound support queries (delivery, returns). Does not replace the Claude API advisor but removes low-effort support volume.
**Effort:** 15 minutes

---

## Phase 1: Developer Setup Sprint (Before/At Launch)

All items in this phase are one-time technical setup tasks. Group them into a single developer sprint.

### 1.1 Technical SEO Baseline

These are non-negotiable for a headless Next.js build. None will rank without them.

**Rendering:**
- Verify all product and collection pages are SSG (static generation with revalidation) or SSR. Client-rendered pages will not index reliably. This is the most critical item to verify.

**Structured data (JSON-LD):**
- `Product` schema on every product page: name, image, description, brand, offers (price, availability, currency, URL). Include `aggregateRating` once reviews exist. Missing `brand` significantly reduces AI-assisted search discovery.
- `FAQPage` schema on the existing "Moissanite vs Diamond NZ" article and the moissanite FAQ page.
- `BreadcrumbList` on all pages.
- `Organization` schema on homepage.

**Canonical tags:**
- Shopify's default myshopify.com URLs must not be indexed. Set canonical to miozuki.co.nz equivalents on all pages. Handle collection filter variants with canonical pointing to the unfiltered collection URL.

**XML sitemap and robots.txt:**
- Auto-generate sitemap via Next.js sitemap package. Submit to Google Search Console on launch day. Block /admin, /cart, /checkout, and internal API routes in robots.txt.

**Core Web Vitals:**
- Use next/image with `priority` flag on all above-the-fold product images. WebP format. Correct `sizes` attribute. Target LCP under 2.5 seconds.

**Metadata:**
- Unique `title` and `meta description` on every page. Format: `[Product Name] | Miozuki NZ` for product pages; `[Category] NZ | Miozuki` for collections. No duplicate titles across collection variants.

**Open Graph meta tags:**
- Add `og:title`, `og:description`, `og:image`, `og:price:amount`, `og:price:currency`, `og:availability` to the Next.js `<Head>` component on every product page, populated from Shopify Storefront API data. Required for how links display when shared on any platform.

**Internal linking discipline:**
- Every blog/education article links to at least one relevant product collection. Every product collection links to relevant educational content. Build this into the article template from the start.

### 1.2 Architecture Decision: Subdirectory for Content Hub

**What:** Confirm that the moissanite education hub and any future content hub is built at `miozuki.co.nz/learn` or `miozuki.co.nz/moissanite-guide` as a subdirectory, never as `learn.miozuki.co.nz` or `guide.miozuki.co.nz` (subdomains).
**Why:** Subdomains are treated as separate sites by Google and split domain authority. A new domain with zero backlinks cannot afford to dilute authority. Subdirectory consolidates every piece of content under miozuki.co.nz's growing authority.
**Action required:** This is an architecture decision, not a build task. Confirm with developer before any content hub work begins.

### 1.3 Shopify Dev MCP

**What:** Install the official Shopify Dev MCP in the miozuki-web repo.
```bash
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
```
Verify with `claude mcp list`.
**Why:** Gives Claude Code direct access to Shopify Admin API, GraphQL schema, and Storefront API documentation. Eliminates manual copy-pasting of product specs and API docs into prompts. Used for the chatbot build, content generation, and metafield work.
**Effort:** 5 minutes

### 1.4 Vercel Plugin for Claude Code

**What:** Install the Vercel Claude Code plugin. Check vercel.com/docs/integrations/claude-code for current install method.
**Commands added:** /deploy, /env, /status, /marketplace
**Why:** Deployment, environment variable management, and log checking without leaving Claude Code. Practical for the build-deploy-review loop on the Next.js frontend.
**Effort:** 10 minutes

### 1.5 miozuki-web CLAUDE.md

**What:** Create or update the CLAUDE.md in the miozuki-web repo with:
- Shopify Storefront API version in use
- Product metafield schema
- Vercel project name and environment names (production, preview, development)
- NZ English spelling conventions (jewellery, colour, organise, etc.)
- Brand voice rules: editorial, warm but not fluffy, ethical sourcing angle. Never: "stunning", "gorgeous", "perfect", "unique"
- Canonical pattern for collection and product pages
- Internal linking convention (articles link to collections and vice versa)
**Why:** Every Claude Code session in this repo inherits these conventions without re-prompting. One-time setup, compounding benefit.
**Effort:** 1-2 hours

### 1.6 Claude Code Hooks

Install all three hooks in `.claude/settings.json` for the miozuki-web repo:

**Auto-commit hook (PostToolUse on Write):**
Automatically commits every file written by Claude Code. Creates an audit trail of all AI-generated draft content without manual commit steps.

**Vale prose linter hook (PostToolUse on Write):**
Runs Vale prose linter on every markdown file written. Catches NZ English violations, passive voice, and style errors before content reaches review. Requires Vale installed: `scoop install vale` (Windows) or `brew install vale` (Mac).

**PreToolUse gate for git push and Shopify deployment:**
Blocks any `git push` or Shopify deployment from inside a Claude Code session until a custom condition is met. Safety rail for the production repo.
**Effort:** 1 hour combined

### 1.7 Custom Slash Commands

Build the following in `.claude/commands/` (or `.claude/skills/<name>/SKILL.md` per current Claude Code convention):

| Command | What it generates |
|---|---|
| `/product-description [product]` | Miozuki brand-voice product copy, 150-200 words, NZ English, ethical sourcing angle |
| `/seo-meta [page]` | title tag, meta description, OG tags for a given page |
| `/blog-outline [topic]` | Structured moissanite or pearl education article outline with H2/H3 hierarchy and FAQ section |
| `/faq-entry [question]` | FAQ schema-ready Q&A pair (JSON-LD `FAQPage` format) |

Note: `/pin-caption` is deferred until Pinterest becomes an active channel.
**Effort:** 2-3 hours combined

---

## Phase 2: Brand Positioning (Before Launch, No Code Required)

These are copy and positioning decisions, not builds. They should be locked in before any content is published.

### 2.1 Adopt "Heirloom Ethics" as the Primary Brand Narrative

**What:** Reframe the brand story away from "moissanite instead of a diamond" toward "jewellery designed to be passed down, not replaced." The narrative is not the cheaper, greener substitute. It is the stone that earns its place in the family without the extraction story.

**Where to apply:**
- About page (primary home for this narrative)
- Homepage hero copy
- Product descriptions (subtle; not every line, but the framing underpins the voice)
- Every PR pitch and journalist angle
- The Mother's Day pitch already in flight (pearl as heirloom, not just gift)

**Key copy points:**
- Moissanite: 9.25 Mohs hardness, second only to diamond. Built to last generations.
- Pearl: coastal heritage. Natural, timeless, not manufactured for trend.
- Ethical sourcing becomes more meaningful over time, not less.
- "Jewellery for the family, not the occasion."

### 2.2 Adopt Dual-Category Positioning Explicitly

**What:** Every brand touchpoint (About, homepage, editorial pitches, PR) should explicitly call out the moissanite and pearl combination. No NZ competitor combines both categories. This is a structural differentiator.

**Where to apply:** Same list as 2.1. The dual-category fact is also the correct PR angle for SourceBottle responses and editorial pitches.

### 2.3 Develop a Specific NZ Provenance Narrative

**What:** "NZ-owned" is generic -- every small NZ brand says it. Develop a specific story about what NZ means to Miozuki's aesthetic. What landscape, what coast, what cultural reference is the brand actually rooted in? This should be one clear, specific paragraph, not a generic "proudly NZ" statement.

**Why this matters for PR:** It is the NZ story that gives Viva and Stuff a reason to cover Miozuki over an AU brand. Journalists need an angle, not a product listing.

### 2.4 Curate an Explicit Gifting Collection ($300-$1,200 Tier)

**What:** Create a clearly labelled gifting collection on the site -- pearl studs, moissanite pendants, stacking rings -- priced between $300 and $1,200 NZD. The collection should feel curated and intentional, not "entry-level." Frame it as fine gifting, not budget.

**Why:** Four Words starts at $2,300 with a consultation gate. No NZ competitor serves the considered gifting sweet spot with a fine jewellery brand voice. This is an open lane that Miozuki's current price range ($318-$458 sterling silver) already occupies.

---

## Phase 3: Month 1-2 (Post-Launch Foundation)

### 3.1 Audit and Optimise "Moissanite vs Diamond NZ" for Featured Snippet

**What:** The page is already live and ranking. This is the single highest-leverage SEO action available with almost no new content needed.

**Changes required:**
- Direct answer to "is moissanite better than diamond?" in the first 100 words
- Comparison table with clear column headers (Cost, Hardness, Fire, Brilliance, Ethical sourcing)
- FAQ section at the bottom with 6-8 specific questions
- Add `FAQPage` JSON-LD schema markup to the page (covered in Phase 1 but applied here)

**Why:** The featured snippet for "moissanite vs diamond NZ" is currently uncontested. A well-structured page can take position 1-3. This drives more qualified traffic than any other single content change.
**Effort:** 2-3 hours (copywriting + dev for schema)

### 3.2 Collection Page Copy

**What:** Add 200-300 words of descriptive copy above the product grid on each major collection page (moissanite rings, moissanite engagement rings, pearl jewellery).
**Why:** Thin collection pages (product grid only) will not rank against established players. Descriptive copy with target keywords above the fold is the minimum for collection page organic ranking.
**Effort:** 1-2 hours per collection page

### 3.3 Moissanite Grades and Brands Guide NZ

**What:** A comprehensive NZ-focused guide covering moissanite quality grades, the difference between Forever One (Charles and Colvard), Harro Gem, NEO moissanite, and unbranded stones. What to look for, what the grades mean, which to buy at which price point.
**Why:** No NZ-specific resource covers this. US brands (Brilliant Earth, IGS) have exhaustive guides; NZ has nothing. First-mover advantage on this topic is available now. This is foundational content for the /moissanite-guide hub.
**Target keyword cluster:** "moissanite grades NZ," "Forever One moissanite NZ," "best moissanite brand NZ"
**Effort:** 4-6 hours (research, draft, Ryo review)
**Note:** Human editorial review required before publishing. AI draft is a starting point, not final copy.

### 3.4 Claude API Chatbot MVP

**What:** Build a minimal viable jewellery advisor using the Claude API. Open conversation only (no structured quiz flow at this stage). Architecture:

```
Browser (React component)
  --> POST /api/chat (Next.js API route)
      --> Anthropic SDK (claude-haiku-4-5 for cost; claude-sonnet-4-6 for nuance)
          --> system prompt: Miozuki product knowledge, brand voice, guardrails
          --> streaming via Server-Sent Events
  <-- token stream to UI
```

**System prompt must include:**
- Full Miozuki product catalogue and pricing (embed directly; use prompt caching)
- NZ English conventions
- Moissanite education: grades, vs diamond, vs lab diamond, stone size vs carat, care
- Pearl education: types, quality grading, Tahitian vs freshwater vs Akoya
- Guardrails: no medical/legal claims, no competitor disparagement, stay on topic
- Brand voice: heirloom ethics framing, warm but not salesy

**Cost at under 1,000 chats/month:**
- claude-haiku-4-5: approximately USD $3-5/month with prompt caching
- claude-sonnet-4-6: approximately USD $8-12/month
Neither justifies any third-party platform at $100-700/month.

**Note on quiz/structured flow:** Defer to Month 3-4. Build the MVP first, collect visitor question data, then design the quiz flow around what people actually ask. The open conversation generates the research for the quiz design.

**Chatbot placement:** Embed on product pages and, later, inside /moissanite-guide education pages. The static page earns the ranking; the chatbot converts.

**Effort:** 10-15 hours for MVP (API route, chat UI component, system prompt)

### 3.5 Next.js Storefront MCP Proxy

**What:** Build a custom `/api/mcp` route in the Next.js app that exposes live Shopify product data (name, price, image, availability, stone type) as MCP context for Claude Code sessions.
**Why:** Enables accurate, real-time product data in every content generation task and in the chatbot context. Eliminates manual copy-pasting of product specs. Also feeds the Claude API advisor with live pricing.
**Effort:** 4-8 hours
**Note:** This is a developer task, not content work.

### 3.6 /content-draft Slash Command

**What:** Build a `/content-draft` slash command that:
- Accepts a product SKU or collection name
- Pulls live data via Shopify Storefront MCP
- Drafts Instagram and Pinterest captions in Miozuki's brand voice (NZ English, heirloom ethics framing)
- Saves drafts to `inbox/content-queue/YYYY-MM-DD.md` for review

**Human approval gate is mandatory** before any post is published. Fully automated publishing is not appropriate at this stage.
**Effort:** 2-3 hours

---

## Phase 4: Month 2-3

### 4.1 Pearl Jewellery Guide NZ

**What:** Comprehensive guide covering pearl types (freshwater, Akoya, Tahitian, South Sea), quality grading, lustre, care, price differences, and where to buy in NZ.
**Why:** No NZ-specific pearl education resource exists. PearlsOnly is price-led with no editorial content. Walker and Hall have product pages but no educational layer. Shahana Jewels covers Pacific Tahitian pearls but not the full category. This page becomes a reference resource that gift guides, bridal blogs, and lifestyle sites will link to.
**Target keyword cluster:** "pearl jewellery NZ," "pearl earrings NZ," "freshwater pearl guide NZ," "pearl engagement ring NZ"
**Effort:** 4-6 hours (research, draft, Ryo review)

### 4.2 Bride and Groom Magazine Pitch

**What:** Email Bride and Groom Magazine pitching Miozuki for an engagement ring feature.
**Contact:** production@brideandgroom.co.nz
**Pitch angle:** Moissanite as the ethical, NZ-designed alternative to mined diamonds. NZ brand, NZD pricing, delivered to NZ couples. Heirloom ethics framing.
**Why:** NZ's top-selling wedding magazine, in print since 1987. Engagement ring features are standard editorial. Highly relevant audience (engaged couples with high purchase intent). DA moderate but audience quality is exceptional.
**Lead time:** 4-8 weeks for editorial consideration.
**Effort:** Medium (pitch email + product photography required)

---

## Phase 5: Month 4-6 (Topical Depth)

### 5.1 Lab Diamond vs Moissanite NZ Comparison

**What:** A comparison article framing the choice for NZ buyers. Moissanite-favourable framing without being promotional. Cover: cost per carat, visual differences, ethical sourcing, resale value, availability in NZ.
**Why:** Lab diamond is a growing search cluster. A comparison article captures buyers researching lab diamonds who may convert to moissanite once educated. Novita Diamonds covers this from a lab diamond perspective; Miozuki covers it from the moissanite side.
**Target keywords:** "lab diamond vs moissanite NZ," "lab grown diamond vs moissanite NZ price"
**Effort:** 4-5 hours

### 5.2 Moissanite Shape Guide NZ

**What:** Guide covering how different cuts (round, oval, cushion, pear, emerald, marquise) affect fire, brilliance, and face-up size on the hand. Include hand shape guidance (long fingers vs short, narrow vs wide bands).
**Why:** High purchase intent. Buyers in the shape-selection phase are close to converting. No NZ competitor has this guide. US analogues (Brilliant Earth, James Allen) have it and it drives significant long-tail traffic.
**Target keywords:** "moissanite shape guide NZ," "oval moissanite NZ," "cushion moissanite NZ"
**Effort:** 4-5 hours

### 5.3 Ethical Engagement Ring Guide NZ

**What:** A buying guide framing moissanite and pearl as the correct choice for ethically-minded NZ buyers. Cover: why mined diamonds have extraction issues, what makes a stone "ethical," moissanite and pearl credentials, what to ask a jeweller.
**Why:** Directly supports the heirloom ethics brand narrative. Low competition. Attracts links from ethical living blogs, sustainable shopping sites, and wedding blogs.
**Target keywords:** "ethical engagement ring NZ," "conflict-free engagement ring NZ," "sustainable jewellery NZ"
**Effort:** 4-5 hours

### 5.4 "Alternatives to Diamond Engagement Rings NZ" Roundup Post

**What:** Editorially neutral roundup covering moissanite, lab diamond, sapphire, pearl, morganite as diamond alternatives for NZ buyers. Miozuki covers moissanite and pearl; the article covers the full category landscape.
**Why:** Neutral roundup posts attract links from all sides: comparison sites, bridal forums, ethical shopping blogs, wedding photographers with educational content. This is a high-value link magnet asset once it ranks.
**Effort:** 5-6 hours (research, draft, Ryo review for accuracy)

### 5.5 Begin /moissanite-guide Content Hub

**What:** Launch the educational content hub at `miozuki.co.nz/moissanite-guide`. This is NZ's first standalone moissanite education resource. Structure:
- Hub page: overview of what moissanite is, Miozuki's perspective, links to all guide sections
- 10-15 NZ retailer profiles (original assessments, not copied blurbs)
- Educational articles: grades, shapes, care, resale value, vs diamond, vs lab diamond
- Honest comparison of NZ moissanite retailers including competitors

**Architecture:** subdirectory (not subdomain). Inherits miozuki.co.nz domain authority.
**Cadence:** 2-3 guide pages per month from Month 4 onward.
**Note on competitor listings:** Listing competitors honestly is a feature, not a risk. It builds the credibility that makes the hub citable and linkable. Miozuki controls the framing and highlights its own differentiators (pearl combination, NZD pricing, DTC, heirloom ethics narrative).
**Effort:** Ongoing. Initial hub setup: 1 developer sprint. Content: 2-3 hours per page with Ryo review.

### 5.6 Styled Shoot with NZ Wedding Photographer

**What:** Collaborate with 1-2 Auckland-based wedding photographers on a styled shoot featuring Miozuki pieces. Product on model, coastal NZ setting or editorial interior setting. Deep burgundy and cream palette.
**Outputs from a single shoot:**
- High-quality product photography for the site, social channels, and editorial pitches
- An editorial blog post on the photographer's site (backlink)
- Potential editorial placement in Bride and Groom Magazine if pitched alongside the shoot
- Social content for both photographer and Miozuki accounts

**Why now:** Product photography is a blocker for multiple other items (Viva pitch, product pages, chatbot system prompt images). Solving this in one styled shoot is highly efficient.
**Effort:** Medium (photography cost + coordination). Outreach to photographers begins in Month 3.

### 5.7 Quiz/Structured Flow for Chatbot

**What:** Extend the Claude API chatbot MVP with a structured advisor flow. 3-4 qualifying questions before product recommendation:
1. "What is this for?" (self, partner, parent, friend)
2. "What is your budget?"
3. "Moissanite, pearl, or not sure?"
4. "Any style preference?" (classic, modern, minimal, statement)

Design the quiz questions based on real visitor conversation data from the MVP (3-4 months of open chat data).
**Why defer:** The quiz flow adds 20-30 hours of build time. Building it against real question data (from the MVP) is more efficient than building it blind.
**Effort:** 20-30 hours (beyond the MVP)

---

## Phase 6: Month 7-12 (Authority Building)

### 6.1 Moissanite Care and Cleaning Guide

**What:** Practical guide covering daily care, cleaning methods (ultrasonic vs soap and water), storage, repair, and whether moissanite scratches over time.
**Why:** Low competition in NZ, high utility. Attracts links from jewellery care blogs, gift guides, and new owners searching post-purchase. Also builds post-purchase trust.
**Effort:** 3-4 hours

### 6.2 Moissanite Resale Value NZ: Honest Assessment

**What:** An honest, unvarnished assessment of moissanite resale value in NZ. Cover the secondary market, price retention vs diamond, vs lab diamond. Do not oversell -- the honest answer is that resale value is low, but the purchase argument is not resale, it is the original price differential.
**Why:** This type of content earns disproportionate links precisely because it is unusual for a retailer to publish honestly. Journalists, comparison sites, and Reddit users link to it as a credible source. It also builds the E-E-A-T signals Google requires.
**Effort:** 3-4 hours plus Ryo review for accuracy

### 6.3 How to Choose a Pearl Engagement Ring NZ

**What:** Guide covering pearl types for engagement rings, setting options, durability considerations (pearl is softer than moissanite -- Mohs 2.5-4.5, requires more care), ring styles, and what to look for from an NZ supplier.
**Why:** Pearl engagement rings are a growing trend (45% Pinterest search increase confirmed). No NZ resource owns this topic. Directly supports Miozuki's pearl range and drives high-intent traffic.
**Effort:** 3-4 hours

### 6.4 Metro NZ Pitch

**What:** Pitch Metro NZ (quarterly Auckland lifestyle magazine) with a premium Auckland brand story. Frame around the heirloom ethics narrative and the NZ provenance story.
**Why:** Smaller than Viva but high credibility for a premium Auckland brand. The SourceBottle and Viva relationship built in Months 1-3 provides a reference point ("as featured in Viva") that strengthens the Metro pitch.
**Lead time:** Quarterly publication; start outreach in Month 5-6 to target a Month 7-9 placement.
**Effort:** Low (pitch email + existing brand assets)

### 6.5 Continue /moissanite-guide Content Hub

**Target:** 15-20 guide pages by end of Month 12. At 2-3 pages per month from Month 4, this is achievable without overcommitting.
**Priority order for remaining pages:**
1. Moissanite vs diamond (already live -- optimise)
2. Moissanite grades and brands (Phase 3)
3. Pearl jewellery guide (Phase 3/4)
4. Shape guide (Phase 5)
5. Care guide (Phase 6)
6. Resale value (Phase 6)
7. NZ retailer comparison profiles (build out gradually)
8. Setting guide (emerald cut settings, pavé, bezel, tension)
9. Moissanite sizing guide (carat vs mm face-up)
10. Pearl engagement ring guide (Phase 6)

---

## Deferred Backlog (Month 12+)

Review these at the 12-month mark. Do not act on them before then.

| Item | Why Deferred |
|---|---|
| Reddit expert-participant programme | Requires consistent 20-30 min/day; not sustainable solo pre-revenue |
| Micro-influencer gifting campaign (~$1,500 NZD + product) | Pre-revenue budget constraint; revisit when first revenue arrives |
| Ahrefs MCP + programmatic SEO workflow (~$99 USD/month) | Keyword research for Year 1 already done; Ahrefs justified at higher content velocity |
| Ethical Jewellers NZ directory | Curation burden too high solo; revisit if /moissanite-guide establishes category authority |
| Pinterest as an active channel | Requires ongoing content pipeline; revisit when content system is running |
| Bay of Plenty Wedding Show (exhibitor) | Verify exhibitor fee and format first; commit only if budget justifies it |
| JWNZ membership | Assess ROI after first revenue |
| SBN (Sustainable Business Network) membership | Assess brand alignment separately |
| Ayrshare MCP ($149/month) | Social publishing at low volume doesn't justify cost pre-revenue |
| Canva MCP | Revisit when social content pipeline is active |
| Instagram MCP (Composio) | Revisit when Instagram is an active channel |
| Blotato ($29/month) | No video content yet; revisit Month 3-6 |
| Quiz/chatbot structured flow | Phase 5 (Month 3-4 after MVP data) |
| Ahrefs MCP | Month 6+ |
| claude-seo subagents | Evaluate at Month 4-6 when guide hub build begins |
| Feedspot NZ jewellery blog outreach | Month 3+ after higher-value links are established |
| NZFW exhibitor/sponsor | Month 4-6 after Viva relationship is built |
| "Affordable under $500" article | After brand voice is fully established |
| Curated ethical jeweller guide | Month 12-18 |
| Folder-watch content automation hooks | After photography workflow is established |
| /pin-caption slash command | When Pinterest becomes active |

---

## Skipped (Do Not Pursue)

| Item | Reason |
|---|---|
| All AI tools from ai-tools-dtc-2026.md (Flair, Pixora, PhotoRoom, Midjourney, Mokker, AdCreative, Creatify, HeyGen) | Entire category deferred by Ryo |
| Third-party chatbot platforms (Tidio, Intercom) | $100-700/month; Claude API direct is cheaper and better |
| Conscious Wedding Vendors NZ directory | Weak brand alignment; market too crowded |
| Fine jewellery NZ / "fine jewellery online NZ" head terms | Too competitive for Year 1 new domain |
| Engagement rings NZ head terms | Too competitive for Year 1 new domain |
| Pencil (video editing AI) | Requires existing video footage |
| Pinterest active channel | Ongoing content cadence unsustainable solo pre-revenue |

---

## Key Unresolved Prerequisite

**Product photography is a blocker.** The following items cannot proceed without hi-res product shots on a neutral background:
- Viva Mother's Day pitch (editorial requires images)
- Claude API chatbot system prompt (product images in context)
- Styled shoot (needs base product shots)
- Collection page copy (images drive the copy framing)

**Resolve this before any content or PR work begins.** If studio product shots do not exist, this is the first task -- not the second.

---

## Decision Reference: What We Are and Are Not Doing

**Brand:** Heirloom ethics framing. Dual-category (moissanite + pearl). NZ provenance story. Not "affordable alternative to diamonds."

**SEO:** Content-first, subdirectory architecture, editorial voice. Targeted long-tail NZ queries. Not chasing head terms in Year 1.

**Content:** 1-2 posts/month minimum, comparison and education queries first. /moissanite-guide hub from Month 4.

**Backlinks:** Earned via editorial pitches (Viva, Stuff, Bride and Groom), SourceBottle responses, directories, and styled shoot collaborations. Not paid links.

**Tooling:** Claude API chatbot (direct, not third-party). Shopify Dev MCP + Vercel Plugin + custom slash commands and hooks for developer efficiency. No SaaS tool subscriptions except where zero cost.

**Community:** Not actively pursuing Reddit or Pinterest at this stage. SourceBottle responses as the only active journalist outreach channel.

---

*First draft, compiled 2026-04-26. All recommendations require Ryo's review before task creation or execution. All contacts and URLs should be verified before acting. This is a planning document, not a final brief.*
