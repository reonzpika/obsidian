---
title: "Fact-check: claude-code-social-media.md"
created: 2026-04-25
status: draft
---

# Fact-check: claude-code-social-media.md

Checked 2026-04-25 via web search. Sources: Composio, Inrō, Ayrshare pricing page, Canva newsroom, Shopify changelog, Blotato pricing page, GitHub.

---

## Verified claims

- **Composio Instagram MCP: publish, analytics, DM automation, 250+ tool ecosystem**: Confirmed. Composio Instagram MCP exists at composio.dev with the described capabilities.
- **Inrō Instagram MCP: focused on DM automation**: Confirmed. Inrō MCP exists at inro.social, specifically for Instagram DM automation (25+ tools, contacts, campaigns, scenarios).
- **Pinterest MCP internal deployment (InfoQ, April 2026)**: Confirmed via search results. Pinterest has deployed MCP internally.
- **Ayrshare MCP at github.com/vanman2024/ayrshare-mcp**: Confirmed. Repo exists with 75+ tools, 13+ platforms as described.
- **Canva MCP: official integration, available now**: Confirmed. Official Canva MCP exists at canva.dev/docs/apps/mcp-server/. Both a developer MCP server and a no-code AI Connector are available.
- **Claude Design by Anthropic Labs with Canva Design Engine**: Confirmed. Canva announced the integration with Claude Design (Anthropic Labs product) on the Canva newsroom.
- **Shopify AI Toolkit: April 9, 2026**: Confirmed. This doc has the correct date (April 9). Note: the content-automation doc incorrectly says April 15.
- **Shopify AI Toolkit: four MCP server types (Dev, Storefront, Customer Account, Checkout)**: Confirmed via Shopify documentation.
- **Every Shopify store gets a free Storefront MCP endpoint**: Confirmed. Shopify activated a default /api/mcp endpoint on every store as part of Summer 2025 Edition.
- **Blotato at $29/month**: Confirmed. Blotato Starter plan is $29/month.
- **Blotato: 1 video to 9 pieces of content in 40 minutes**: Confirmed. This workflow is documented on the Blotato site and in community write-ups.
- **awesome-claude-code at github.com/hesreallyhim/awesome-claude-code**: Confirmed. Repo exists with 21.6k stars.

---

## Corrections needed

**1. Ayrshare pricing: significant error**
- Doc says: "$29/month (Personal) to $149/month (Agency)"
- Correct: Ayrshare's current pricing has no "Personal" or "Agency" tier names. The entry tier is Premium at $149/month. Higher tiers are Launch ($299/month) and Business ($599/month). There is no $29/month plan at Ayrshare.
- The $29 figure may have been confused with Blotato's $29/month Starter plan. These are different products.
- Recommendation: Update to "Premium $149/month, Launch $299/month, Business $599/month. Verify current pricing at ayrshare.com before committing."
- Impact: This affects the implementation priority table recommendation and the "Miozuki fit" assessment. At $149/month (not $29), Ayrshare is a more significant commitment. Reassess fit accordingly.

**2. awesome-claude-code "#1 trending GitHub repo in February 2026"**
- Doc says: "Was the #1 trending GitHub repo in February 2026."
- Could not confirm the specific "#1 trending" claim. The repo has 21.6k stars and is clearly popular, but trending rank at a specific date is not verifiable in this check.
- Recommendation: Change to "one of the most-starred Claude Code community resources" or simply remove the trending rank claim. The repo's value is evident from its star count and community adoption; the "#1 trending" superlative is not load-bearing.

---

## Unverifiable / flags

- **CData Connect AI: full CRUD over Instagram Graph API**: Could not confirm specific capabilities in this check. CData exists as a data connectivity platform; Instagram integration may exist but was not independently verified.
- **Shopify Storefront MCP plan requirements**: Doc suggests checking plan requirements at shopify.dev/docs/apps/build/devmcp. The /api/mcp endpoint appears to be available on all plans by default (confirmed), but specific plan restrictions for authenticated operations were not fully verified.
- **Canva MCP: template fill from product data (name, price, image URL)**: The general autofill capability is confirmed, but the specific workflow of feeding Shopify product data via Storefront MCP into Canva templates was not end-to-end verified. The components are real; the combined workflow is plausible but has not been documented as a tested pattern.

---

*Fact-check complete 2026-04-25. The Ayrshare pricing error is the most impactful correction: the entry price is $149/month, not $29/month. Reassess priority table before acting on recommendations.*
