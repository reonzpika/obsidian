---
title: "Claude Code for Social Media Content Workflows"
created: 2026-04-25
status: draft
tags: [miozuki, claude-code, social-media, tools, workflow]
---

# Claude Code for Social Media Content Workflows

**Research date:** 2026-04-25
**Scope:** Claude Code CLI (Max plan) workflows, MCP servers, and community tooling for social media content creation and publishing. Relevance: Miozuki DTC jewellery brand using Next.js + Shopify.
**Status:** First draft for human review.

---

## 1. MCP Servers for Social Media Publishing

### Instagram MCP

Multiple providers now offer Instagram MCP servers:

- **Composio Instagram MCP**: Read posts and comments, publish content, analytics, DM automation. Composio acts as the auth middleware, handles OAuth. Part of their 250+ tool MCP ecosystem. Free tier available; paid plans for higher volume. Most actively maintained of the available options.
- **Inrō Instagram MCP**: Focused on DM automation and audience engagement. Suited for responding to comment threads and DMs at scale. Less useful for publishing.
- **CData Connect AI**: Full CRUD over Instagram Graph API through a normalised SQL-like interface. More developer-oriented; overkill for content publishing unless you need data extraction and reporting.

**Relevant to Miozuki**: Composio is the practical choice. Publish posts, read engagement data, respond to DMs from inside a Claude Code session. Combine with Midjourney output (already in the tools stack) for a draft-to-publish workflow.

### Pinterest MCP

Pinterest itself deployed MCP internally (confirmed InfoQ, April 2026). External tooling:

- **CData Connect AI**: Free GitHub version is read-only (boards, pins, analytics). Full CRUD available through the commercial CData MCP Server for Pinterest (paid).
- **Ayrshare MCP** (see below): Includes Pinterest among its 13+ platforms. Best route for publishing.

**Note on headless Pinterest**: Pinterest Rich Pins require server-rendered Open Graph meta tags. Miozuki's Next.js stack already supports this, but it needs explicit verification that the `og:type`, `og:title`, `og:image`, and `product:price:amount` tags are being rendered at the page level, not injected client-side. If they are not, Rich Pins will not validate. This is a prerequisite for any Pinterest publishing workflow to carry full SEO and product discovery value.

### Ayrshare MCP

**Best option for multi-platform publishing.** GitHub: `vanman2024/ayrshare-mcp`.

- 75+ tools, 13+ platforms: Instagram, Pinterest, TikTok, Facebook, X, LinkedIn, Threads, YouTube, and more.
- Bulk scheduling, post drafting, analytics pull, image attachment.
- Pricing: Free tier (20 posts, images only) / $149/month Premium / $499/month Business. API key-based auth; no per-platform OAuth complexity once Ayrshare is connected.
- Claude Code workflow: connect Ayrshare MCP, draft posts in session, schedule or publish directly. No switching between apps.

**This is the most production-ready social MCP currently available.** For Miozuki's volume (small, curated), the Free tier may suffice initially; Premium at $149/month is needed for video, scheduling, and analytics. Verify current tier limits at ayrshare.com before committing.

### Canva MCP

Official Canva MCP integration. Available now.

- Generate designs from text prompts.
- Fill templates with product data (name, price, image URL).
- Export to PNG, PDF, MP4.
- Canva Design Engine is now integrated into Claude Design (Anthropic Labs product). The MCP exposes the same engine to Claude Code sessions.

**Workflow pattern for Miozuki**: Feed Canva MCP a product name, stone type, price, and lifestyle image path. Canva generates a carousel or story template. Export to PNG. Pass to Ayrshare MCP to schedule. Full draft-to-schedule without leaving the terminal.

**Limitation**: Template quality depends on your Canva Pro template library. Generic templates look generic. Miozuki's brand palette (deep burgundy, cream, dark velvet) needs to be pre-built into saved Canva templates for the MCP to use them consistently.

---

## 2. Shopify MCP (Official, April 2026)

Shopify released the **AI Toolkit** on April 9, 2026. Four official MCP servers:

| Server | What it exposes |
|---|---|
| Shopify Dev MCP | Store configuration, theme, app setup (developer-facing) |
| Shopify Storefront MCP | Product catalogue, collections, pricing, inventory (customer-facing data) |
| Shopify Customer Account MCP | Order history, account data, loyalty |
| Shopify Checkout MCP | Checkout configuration, discount codes, shipping (preview only, not GA) |

**Every Shopify store gets a free Storefront MCP endpoint.** No third-party proxy needed.

**Docs**: `shopify.dev/docs/apps/build/devmcp`

**Relevant to Miozuki content workflows**:

- Pull live product data (name, price, image URL, stone type, in-stock status) directly into a Claude Code session via Storefront MCP.
- Use that data to generate caption copy, product comparison tables, FAQ content, or social posts with accurate, real-time pricing.
- Eliminates the manual step of copy-pasting product details into prompts. Reduces errors when prices or availability change.

**Example workflow**: In a Claude Code session, call Storefront MCP to pull all in-stock rings under $2,000 NZD. Feed results to a prompt: "Draft five Instagram captions for these products in Miozuki's brand voice (NZ English, warm but not fluffy, ethical sourcing angle)." Review, edit, pass to Ayrshare.

---

## 3. Blotato: Content Repurposing Workflow

**Blotato** is currently the most cited Claude Code + social media integration among non-developer users.

- $29/month. Platform-specific content (caption styles, hashtag norms, image ratios) vary by target.
- Blotato MCP: YouTube transcript scraper built in. Pulls transcript from any public video. Feed to Claude Code for repurposing.
- Community-reported workflow: one YouTube video generates around nine pieces of platform-specific content in a single session. Not a vendor benchmark.
- Works for any long-form input: a podcast transcript, a long-form blog post, a supplier product brief.

**Miozuki application**: Miozuki does not yet have video content, but the pattern applies to blog posts and product descriptions. A single long-form piece (e.g., "Moissanite vs Diamond Guide") can be sliced into Instagram carousels, Pinterest pin descriptions, TikTok script outlines, and Twitter/X thread drafts in one session.

---

## 4. Content Automation Hooks

Claude Code hooks run shell commands on events (before tool use, after tool use, on session start, etc.). For content workflows:

**Pre-commit hook pattern**: Trigger a content quality check before any markdown file is committed to the vault. Runs a Claude prompt against the draft: checks brand voice, NZ English spelling, em-dash rule, pricing accuracy against Shopify data.

**Post-write hook pattern**: After a content file is written, automatically log it to a `content-queue.csv` or push a notification. Enables async content review without manually tracking what was drafted.

**The `#1 non-developer Claude Code use case`** cited in the community is social media post creation. The pattern is:
1. Hooks trigger on new product images added to a watched folder.
2. Claude Code reads the image metadata and product SKU.
3. Calls Shopify Storefront MCP for live product data.
4. Drafts caption variants.
5. Saves drafts to a review queue.
6. Human reviews and approves.
7. Ayrshare MCP publishes on schedule.

This is not hypothetical: multiple solo operators are running this pattern as of early 2026. The missing piece for most is step 6 (structured human review before publish). For Miozuki at pre-revenue stage, manual review of every post is appropriate and low-volume enough to be practical.

---

## 5. Community Resources and Repos

**awesome-claude-code** (GitHub: `hesreallyhim/awesome-claude-code`): The primary community-maintained resource for Claude Code integrations. 21.6k+ stars, highly active. Lists MCP servers, skills, workflows, CLAUDE.md templates, and real use cases. Start here for any new integration research.

**Content Ops Skill**: A Claude Code skill pattern (slash command) that runs a full editorial pipeline. Researches a topic, drafts content for multiple platforms, applies brand voice, saves structured output. Not a specific repo, but a pattern that has been published in multiple forms in the awesome-claude-code community. Buildable as a custom skill for Miozuki.

---

## 6. Practical Workflow for Miozuki

**Minimum viable setup (start now):**

1. Connect Shopify Storefront MCP using the new official endpoint.
2. Install Ayrshare MCP (`vanman2024/ayrshare-mcp`) and connect Ayrshare (Free tier to start; Premium $149/month for video and scheduling -- verify at ayrshare.com).
3. Connect Ayrshare to Instagram and Pinterest.
4. Write a `content-draft` slash command in `.claude/commands/` that:
   - Accepts a product SKU or collection name as input.
   - Pulls live data via Storefront MCP.
   - Drafts captions for Instagram and Pinterest in Miozuki's brand voice.
   - Saves drafts to `inbox/content-queue/YYYY-MM-DD.md` for review.

**Next layer (months 1-3):**

5. Add Canva MCP for templated image generation. Pre-build 3-5 Canva templates in Miozuki's brand palette (burgundy + cream, dark velvet, coastal NZ).
6. Extend the slash command to trigger Canva template fill after caption draft.
7. Add hook: after content review approval (a manual flag in the queue file), auto-publish via Ayrshare.

**Future (months 3-6, post-revenue):**

8. Blotato for video repurposing once product video assets exist.
9. Content repurposing pipeline: long-form moissanite guide content sliced into social assets automatically.

---

## 7. Open Questions and Caveats

- **Pinterest Rich Pins on Next.js**: Verify that `og:type` and product meta tags are server-rendered (not client-injected) before investing in Pinterest MCP workflows. Failing this, Rich Pin validation will fail and product pins will have reduced reach.
- **Shopify Storefront MCP eligibility**: Confirm that the Miozuki store is on a Shopify plan that includes the Storefront MCP endpoint. Check `shopify.dev/docs/apps/build/devmcp` for plan requirements.
- **Ayrshare Instagram publish permissions**: Instagram's API requires a Business or Creator account. Verify Miozuki's Instagram account type before connecting Ayrshare.
- **Canva MCP template quality**: Canva MCP uses saved templates. If Miozuki's brand templates are not in the Canva account, the MCP will default to generic Canva styles.
- **Hook-based automation approval gate**: Any automated publish workflow should have an explicit human approval step before Ayrshare publishes. Fully automated publishing from a pre-revenue brand is a risk (errors, wrong pricing, off-brand tone). Build the approval gate in before scaling.

---

*Research compiled 2026-04-25. All tool pricing and availability subject to change. Verify at each vendor before committing. First draft for Ryo's review.*
