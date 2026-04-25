---
title: "Claude Code for Shopify and Ecommerce: Workflows and Tools"
created: 2026-04-25
status: draft
tags: [miozuki, claude-code, shopify, ecommerce, tools, seo]
---

# Claude Code for Shopify and Ecommerce: Workflows and Tools

**Research date:** 2026-04-25
**Scope:** How practitioners are using Claude Code (CLI, Max plan) for Shopify and headless ecommerce development, SEO, and content operations. Not Claude API. Relevant to Miozuki's Next.js + Shopify Storefront API + Vercel stack.
**Status:** First draft for human review.

---

## 1. Shopify Dev MCP (Official, April 2026)

The most significant recent development for Shopify + Claude Code workflows is Shopify's official MCP server, released 9 April 2026.

**What it does:**
- Connects Claude Code directly to Shopify Admin API
- Provides access to Shopify documentation, GraphQL schemas, and API references from inside a Claude Code session
- Enables Claude Code to read and write Shopify store data, query products, check orders, manage metafields
- Useful for Liquid theme development and headless storefront queries

**Install command (macOS/Linux/WSL):**
```bash
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
```

**Windows (native, non-WSL):**
```bash
claude mcp add --transport stdio shopify-dev-mcp -- cmd /c npx -y @shopify/dev-mcp@latest
```

**Miozuki relevance:** Miozuki runs headless Next.js over Shopify Storefront API. The Shopify Dev MCP gives Claude Code visibility into the Shopify schema without copy-pasting GraphQL docs. Speeds up writing Storefront API queries, product data fetching, and metafield schema work.

**Shopify Storefront MCP (separate):** A distinct MCP exists for customer-facing chat agents built on headless storefronts. Different from the Dev MCP. The Dev MCP is for development; the Storefront MCP is for runtime customer interactions. Both are relevant to Miozuki but serve different purposes.

---

## 2. Vercel Plugin for Claude Code (March 2026)

Vercel released a Claude Code plugin in March 2026, adding slash commands directly inside Claude Code sessions for Vercel project management.

**Commands:**
- `/bootstrap` -- scaffold a new Vercel project from templates
- `/deploy` -- trigger a Vercel deployment
- `/env` -- manage environment variables
- `/status` -- check deployment status and logs
- `/marketplace` -- browse and add Vercel marketplace integrations

**Miozuki relevance:** Miozuki deploys on Vercel. The plugin means deployment, env var management, and log checking can happen inside a Claude Code session without context-switching to the Vercel dashboard or terminal. Practical for the build-deploy-review loop on the Next.js frontend.

---

## 3. CLAUDE.md Templates for Shopify Theme Development

A community-maintained GitHub Gist (karimmtarek) provides CLAUDE.md templates specifically for Shopify theme development. The templates encode:
- Shopify Liquid syntax conventions
- Theme architecture patterns (sections, blocks, snippets)
- Dawn theme structure
- Shopify CLI workflow integration

**Pattern:** Drop the appropriate CLAUDE.md into the project root and Claude Code automatically follows the Shopify-specific conventions throughout the session. Reduces repetitive instruction in prompts.

**Miozuki relevance:** Miozuki is headless (not a Liquid theme), so these templates are not directly applicable. However, the pattern of Shopify-specific CLAUDE.md context files is worth noting for any theme work or for building out a Shopify-adjacent CLAUDE.md capturing Miozuki's storefront API conventions.

---

## 4. SEO Automation with Claude Code

### claude-seo (GitHub: AgriciDaniel)

A Claude Code skill set specifically for SEO, comprising:
- 19 sub-skills covering technical SEO, E-E-A-T, schema markup, GEO/AEO, backlinks, local SEO, maps intelligence, and Google API integrations (Search Console, PageSpeed, GA4)
- 12 subagents for parallelising SEO research tasks (competitor analysis, SERP research, content gap analysis)

This is a practitioner-built tool, not an official Anthropic product. Quality and maintenance status require verification.

**Miozuki relevance:** The content roadmap in `seo-landscape.md` and the directory strategy in `directory-seo-feasibility.md` both involve sustained content production. Claude Code with SEO-oriented sub-skills could automate the content brief and meta-writing stage of the `/moissanite-guide` build.

### Programmatic SEO engine pattern

Practitioners are combining Claude Code + Ahrefs MCP to build programmatic SEO landing page generators:
1. Ahrefs MCP pulls keyword clusters and search volume data
2. Claude Code generates landing page content for each keyword cluster
3. Pages are pushed to a Next.js static site via Vercel

This pattern is directly applicable to the Moissanite Guide NZ concept (see `directory-seo-feasibility.md`). Rather than manually writing guide pages, a Claude Code workflow could generate first drafts against a keyword list, with human editorial review before publish. The editorial review step is non-negotiable given Google's E-E-A-T requirements and the accuracy standards required for gemstone education content.

**Ahrefs MCP:** Confirmed available at github.com/ahrefs/ahrefs-mcp-server (official Ahrefs product). Requires a paid Ahrefs plan from Lite tier. Verify current Lite plan pricing at ahrefs.com before committing to this workflow.

---

## 5. Subagent Libraries

### awesome-claude-code-subagents (VoltAgent GitHub)

A community-curated library of 100+ Claude Code subagent definitions covering specialist domains:
- Next.js developer subagent
- Shopify developer subagent
- SEO analyst subagent
- Content writer subagent
- Code reviewer subagent

These are CLAUDE.md-based context definitions that can be loaded into a Claude Code session to give it a specialised role. Not AI agents in the autonomous sense -- they define how Claude Code behaves within a session.

**Miozuki relevance:** A Next.js + Shopify developer subagent loaded into the miozuki-web repo session would encode the headless storefront patterns, Vercel deploy conventions, and Miozuki-specific decisions. Worth building a Miozuki-specific variant rather than using a generic template.

### mcpmarket.com and agentskills.so

Community directories for discoverable MCP servers and Claude Code skill definitions. Relevant for finding Shopify, Klaviyo, or analytics integrations. Quality varies; treat as a discovery layer, not a source of production-ready tools.

---

## 6. Claude Code + Klaviyo

No official Klaviyo MCP for Claude Code has been confirmed as of April 2026. However, practitioners are using Claude Code to:
- Generate Klaviyo email HTML templates from briefs
- Write Klaviyo flow logic descriptions that are then manually implemented
- Draft A/B test variant copy for subject lines and CTAs

Without an official Klaviyo MCP, the workflow is prompt-in/code-out rather than connected. An unofficial MCP could be built using Klaviyo's REST API, but this is a DIY project.

---

## 7. Practical Stack for Miozuki

Based on the research, a Claude Code setup optimised for Miozuki's stack:

**Install:**
```bash
# Shopify Dev MCP
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest

# Vercel plugin (via Claude Code plugin system -- verify install method at current Vercel docs)
# Check: vercel.com/docs/integrations/claude-code
```

**CLAUDE.md additions for miozuki-web repo:**
- Shopify Storefront API version in use
- Product metafield schema
- Vercel project name and environment names
- NZ English spelling conventions
- Brand voice rules for any AI-generated content

**Workflow for /moissanite-guide content:**
1. Claude Code + Ahrefs MCP to pull NZ moissanite keyword clusters
2. Claude Code generates content briefs per page
3. Ryo reviews briefs and approves scope
4. Claude Code drafts guide pages against approved briefs
5. Ryo edits every page before publishing (E-E-A-T requires genuine human expertise)
6. Vercel plugin deploys to preview, Ryo approves, promotes to production

---

## 8. Limitations and Gaps

- **No confirmed Klaviyo MCP.** Email flow automation remains manual or DIY.
- **No confirmed Judge.me or Shopify review platform MCP.** Review management stays in Shopify admin.
- **Shopify Agentic Storefronts NZ eligibility unconfirmed.** March 2026 rollout was US-only. Check Shopify partner portal for NZ activation status before building toward it.
- **Subagent and skill quality varies widely.** Community-built tools require validation before production use. Treat as starting points, not production infrastructure.
- **Ahrefs MCP:** Confirmed available; requires paid Ahrefs plan from Lite tier. Verify current Lite pricing at ahrefs.com before committing.

---

*Research compiled 2026-04-25. All tool capabilities are evolving rapidly. Re-verify before committing to any specific integration.*
