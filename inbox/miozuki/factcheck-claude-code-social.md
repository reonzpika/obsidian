---
title: "Fact-check: claude-code-social-media.md"
created: 2026-04-25
status: draft
tags: [miozuki, factcheck, claude-code, social-media]
---

# Fact-check: claude-code-social-media.md

Fact-check date: 2026-04-25. Research via live web search. For Ryo's review before applying corrections.

---

## Summary Table

| Claim | Verdict | Correction needed |
|---|---|---|
| Composio Instagram MCP: publish, read, analytics, DM | CONFIRMED | None |
| Inrō Instagram MCP: DM automation focus | CONFIRMED | None |
| CData Connect AI: Pinterest CRUD | CONFIRMED (with nuance) | Clarify: free GitHub version is read-only; CRUD requires commercial product |
| Ayrshare MCP (vanman2024/ayrshare-mcp): 75+ tools, 13+ platforms | CONFIRMED | None |
| Ayrshare pricing: $29/month Personal to $149/month Agency | INCORRECT | No Personal plan at $29/month; current pricing: Free / $149 Premium / $499 Business |
| Canva MCP: official, generate/fill/export | CONFIRMED | None |
| Blotato: $29/month | CONFIRMED | None |
| Blotato: YouTube transcript scraper, 9 pieces from one video in 40 min | PARTIALLY CONFIRMED | Capability confirmed; specific "9 pieces / 40 min" metric is community anecdote, not vendor claim |
| Shopify AI Toolkit: April 9 2026, 4 MCPs | CONFIRMED | Add: Checkout MCP is preview only, not GA |
| Every Shopify store gets free Storefront MCP endpoint | CONFIRMED | None |
| awesome-claude-code (hesreallyhim): #1 trending GitHub Feb 2026 | UNVERIFIED | The #1 trending claim may refer to rohitg00/awesome-claude-code-toolkit, not hesreallyhim's repo |
| Pinterest deployed MCP internally (InfoQ, April 2026) | CONFIRMED | None |

---

## Detailed Findings

### 1. Composio Instagram MCP

**Claim:** Read posts and comments, publish content, analytics, DM automation. Composio acts as auth middleware, handles OAuth. Free tier available.

**Verdict:** CONFIRMED.

Composio's Instagram MCP is documented and live. Capabilities confirmed: automated post and carousel publishing, comments retrieval, analytics and reporting (impressions, reach, engagement), DM access. Composio acts as the OAuth middleware. Free tier exists.

**Correction:** None.

---

### 2. Inrō Instagram MCP

**Claim:** Focused on DM automation and audience engagement. Less useful for publishing.

**Verdict:** CONFIRMED.

Inrō's MCP has 25+ tools focused on DM automation: contacts, campaigns, scenarios, folders, conversation history. The product is explicitly for DM automation, not content publishing. Confirmed to work via Meta's official API.

**Correction:** None.

---

### 3. CData Connect AI: Pinterest

**Claim:** "Read-only for Pinterest data (boards, pins, analytics). Full CRUD available through CData Connect AI cloud connector."

**Verdict:** CONFIRMED (with clarification).

CData offers two distinct products:
- Free GitHub repo (`CDataSoftware/pinterest-mcp-server-by-cdata`): explicitly read-only via JDBC driver.
- Commercial product ("MCP Server for Pinterest"): full CRUD (read, write, update, delete). This is the paid CData commercial offering, not a generic "CData Connect AI" product.

The document's framing is accurate in substance. The naming "CData Connect AI" may not be the exact commercial product name -- the paid product is labelled "CData MCP Server for Pinterest." Minor wording clarification recommended.

**Correction:** Minor. Change "CData Connect AI cloud connector" to "CData commercial MCP Server for Pinterest."

---

### 4. Ayrshare MCP: tools and platforms

**Claim:** 75+ tools, 13+ platforms.

**Verdict:** CONFIRMED.

GitHub repo `vanman2024/ayrshare-mcp` confirmed: "FastMCP server for Ayrshare Social Media API -- 75+ tools for multi-platform posting." Platforms include Facebook, Instagram, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Snapchat, Telegram, Threads, Bluesky, Google Business Profile (13+).

**Correction:** None on this claim.

---

### 5. Ayrshare pricing

**Claim:** "$29/month (Personal) to $149/month (Agency). API key-based auth."

**Verdict:** INCORRECT. Significant pricing error.

Current Ayrshare pricing (verified 2026):
- Free plan: 20 posts, images only
- Premium: $149/month
- Business: $499/month

There is no "$29/month Personal plan" and no "$149/month Agency plan." The pricing in the document does not match current Ayrshare pricing. The "Personal" tier at $29 may be from an earlier pricing structure that no longer exists, or may be fabricated.

API key-based auth: confirmed.

**Correction required:** Update pricing to "Free tier (limited) / $149/month Premium / $499/month Business." The "Personal" plan label should be removed. For Miozuki's volume, the Free tier or Premium tier applies -- not a $29 tier.

Note: this changes the recommendation in Section 6. The claim "For Miozuki's volume (small, curated), the Personal plan is sufficient" should be revised to reflect the actual pricing tiers and whether the Free tier is workable or Premium is needed.

---

### 6. Canva MCP

**Claim:** Official Canva MCP integration. Generate designs from text prompts, fill templates with product data, export PNG/PDF/MP4.

**Verdict:** CONFIRMED.

Canva MCP is official and documented at canva.dev. Two integration modes: AI Connector (no-code, via Claude Desktop) and MCP Server (developer). Capabilities confirmed: create designs with Canva AI, autofill templates, find existing designs, export as PDFs or images. The Canva + Anthropic Claude Design (Anthropic Labs) partnership is confirmed, including millions of users since launch.

MP4 export: confirmed via Canva video tools.

**Correction:** None.

---

### 7. Blotato pricing

**Claim:** $29/month.

**Verdict:** CONFIRMED.

Blotato Starter plan is $29/month with 30-day money-back guarantee. Creator plan at higher cost. Pricing matches the document.

**Correction:** None.

---

### 8. Blotato: YouTube transcript scraper and "9 pieces in 40 minutes"

**Claim:** "YouTube transcript scraper built in. Pulls transcript from any public video. Feed to Claude Code for repurposing. Documented workflow: one YouTube video, 40 minutes, generates nine pieces of platform-specific content."

**Verdict:** PARTIALLY CONFIRMED.

YouTube video input for content repurposing: confirmed. Blotato accepts YouTube videos and transforms them into platform-specific content for LinkedIn, TikTok, X, Instagram, Threads, Facebook. Consistent with the document.

The "9 pieces in 40 minutes" metric: this appears to be a community use-case claim (referenced on third-party blog posts), not a documented vendor benchmark. The specific numbers cannot be attributed to Blotato's official docs. The capability itself is real; the metric is anecdotal.

**Correction:** Qualify the "nine pieces of platform-specific content (caption + image prompt for each platform)" claim as a reported community use case, not a vendor guarantee. Suggested wording: "Community-reported workflow: one YouTube video generates around nine pieces of platform-specific content in a single session."

---

### 9. Shopify AI Toolkit: 4 MCPs, April 9 2026

**Claim:** "Shopify released the AI Toolkit on April 9, 2026. Four official MCP servers: Dev MCP, Storefront MCP, Customer Account MCP, Checkout MCP."

**Verdict:** CONFIRMED with one caveat.

Shopify AI Toolkit confirmed live. The four MCP servers (Dev, Storefront, Customer Account, Checkout) are all confirmed in official Shopify docs and multiple independent sources.

Caveat: Checkout MCP is currently in preview and not GA for all developers. The document does not flag this. For Miozuki, Checkout MCP is not yet usable. Dev MCP, Storefront MCP, and Customer Account MCP are live.

**Correction:** Add a note in the Checkout row that Checkout MCP is "preview only, not generally available."

---

### 10. Free Storefront MCP endpoint for every Shopify store

**Claim:** "Every Shopify store gets a free Storefront MCP endpoint. No third-party proxy needed."

**Verdict:** CONFIRMED.

Shopify official docs confirm the Storefront MCP endpoint is available to all merchants at no extra cost. No custom setup required. No plan restriction found in the search results.

**Correction:** None.

---

### 11. awesome-claude-code: #1 trending GitHub in February 2026

**Claim:** `hesreallyhim/awesome-claude-code` was "#1 trending GitHub repo in February 2026."

**Verdict:** UNVERIFIED for this specific repo.

The `hesreallyhim/awesome-claude-code` repo is confirmed to exist with 21.6k stars and is a major community resource. However, the "#1 trending GitHub repo in February 2026" claim appears to refer to `rohitg00/awesome-claude-code-toolkit`, not hesreallyhim's repo. The search result explicitly attributes the February 2026 trending position to the rohitg00 repo.

Both repos are legitimate and active. The trending claim in the document may be misattributed.

**Correction:** Change "#1 trending GitHub repo in February 2026" to "major community resource with 21.6k+ stars" to avoid the unverified attribution. Or specify the correct repo if the trending position is important to the narrative.

---

### 12. Pinterest deployed MCP internally (InfoQ, April 2026)

**Claim:** "Pinterest itself deployed MCP internally (confirmed InfoQ, April 2026)."

**Verdict:** CONFIRMED.

InfoQ published: "Pinterest Deploys Production-Scale Model Context Protocol Ecosystem for AI Agent Workflows" (April 2026). Pinterest Engineering Blog also published "Building an MCP Ecosystem at Pinterest" (March 2026 on Medium). This is a major confirmed deployment: domain-specific cloud-hosted MCP servers, central MCP registry, human-in-the-loop approval, thousands of engineer hours saved per month.

**Correction:** None.

---

## Corrections to Apply to claude-code-social-media.md

1. **Ayrshare pricing** (Section 1 and Section 6): Change "$29/month (Personal) to $149/month (Agency)" to "Free tier (20 posts, images only) / $149/month Premium / $499/month Business." Update Section 6 recommendation accordingly -- the "Personal plan is sufficient" statement needs revision.

2. **CData Pinterest wording** (Section 1): Change "CData Connect AI cloud connector" to "CData commercial MCP Server for Pinterest."

3. **Shopify Checkout MCP** (Section 2): Add "(preview only, not generally available)" to the Checkout row in the table.

4. **Blotato "9 pieces in 40 minutes"** (Section 3): Qualify as community-reported use case, not vendor claim.

5. **awesome-claude-code trending** (Section 5): Remove or qualify the "#1 trending GitHub Feb 2026" claim; attribute to the broader category of "highly popular community resource."

---

*Fact-check compiled 2026-04-25. Pending Ryo review before applying corrections.*
