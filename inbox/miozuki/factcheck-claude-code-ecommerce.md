---
title: "Fact-check: claude-code-ecommerce.md"
created: 2026-04-25
---

# Fact-check: claude-code-ecommerce.md

## Summary

Most claims held up. Main corrections: the Shopify Dev MCP is part of a broader AI Toolkit (4 MCP servers, not just one); the claude-seo sub-skill descriptions are wrong (technical SEO and schema focus, not keyword research and content briefs); Ahrefs MCP is confirmed available so the caveat can be softened. Two minor description corrections needed.

---

## Findings

### Shopify Dev MCP release date and install command

**Status:** CONFIRMED

**Finding:** @shopify/dev-mcp exists on npm (latest version 1.12.0 as of research date). Shopify AI Toolkit released April 9, 2026. Install command `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest` matches confirmed `claude mcp add` syntax.

**Note:** The ecommerce doc only describes the Dev MCP. Shopify's April 9 release was an "AI Toolkit" comprising four MCP servers: Dev MCP, Storefront MCP, Customer Account MCP, and Checkout MCP. The ecommerce doc correctly identifies the Dev MCP and Storefront MCP as separate (Section 1), so no structural error -- but the framing as a standalone release rather than part of a 4-server toolkit is slightly underselling the scope. The social media doc covers all four correctly. No correction required in the ecommerce doc.

**Correction needed:** None. Optionally note that Dev MCP is part of the Shopify AI Toolkit (4 servers total).

---

### Vercel Claude Code plugin (March 2026)

**Status:** CONFIRMED

**Finding:** Released March 17, 2026. Slash commands /bootstrap, /deploy, /env, /status, /marketplace confirmed. The plugin also includes 47+ skills, three specialist agents (AI Architect, Deployment Expert, Performance Optimizer), and real-time activity observation. The doc's description of commands is accurate.

**Install method:** The doc correctly notes to verify the install method at Vercel docs. The actual install is `npx plugins add vercel/vercel-plugin` or `/plugin install vercel` inside Claude Code. This is appropriate to leave as a verify-at-docs note since install methods for plugins may drift.

**Correction needed:** None.

---

### `claude mcp add` command syntax

**Status:** CONFIRMED

**Finding:** Syntax `claude mcp add [options] <name> -- <command> [args...]` is correct. Options (--transport, --env) must precede the server name; `--` separates the server name from the downstream command. The command in the doc matches this pattern exactly.

**Windows note:** On native Windows (non-WSL), stdio servers using npx require a `cmd /c` wrapper. The doc's command would need to be `claude mcp add --transport stdio shopify-dev-mcp -- cmd /c npx -y @shopify/dev-mcp@latest` on Windows. Miozuki's dev environment should be confirmed. Worth a caveat in the doc.

**Correction needed:** Add Windows caveat to install command, or note that the command shown is for macOS/Linux/WSL.

---

### karimmtarek GitHub Gist (CLAUDE.md for Shopify theme dev)

**Status:** CONFIRMED

**Finding:** Gist exists at https://gist.github.com/karimmtarek/3a8a636a05ae1c349ad0bba9d10425f0. Content is a CLAUDE.md for Shopify theme frontend conventions: directory structure (assets/, config/, layout/, sections/, snippets/, templates/, locales/), Shopify CLI 3.x workflow, branch naming and commit conventions. Matches the doc's description.

**Correction needed:** None.

---

### claude-seo (AgriciDaniel GitHub): sub-skill count and descriptions

**Status:** PARTIALLY CORRECTED

**Finding:** Repo exists at github.com/AgriciDaniel/claude-seo. Sub-skill count (19) and subagent count (12) confirmed in current repo title. However, the descriptions in the doc are wrong.

Doc says: "19 sub-skills covering keyword research, content briefs, meta generation, internal linking analysis"

Actual scope: technical SEO, E-E-A-T, schema markup, GEO/AEO (AI search optimisation), backlinks, local SEO, maps intelligence, Google Search Console/PageSpeed/CrUX/GA4 APIs, PDF/Excel reporting, content quality, sitemap architecture, SEO drift monitoring, e-commerce SEO, international SEO. Also integrates with DataForSEO, Firecrawl, and Banana extensions.

Doc says: "12 subagents for parallelising SEO research tasks (competitor analysis, SERP research, content gap analysis)"

This is broadly correct directionally but the tool is much more technically oriented than the doc implies. It is a technical SEO + schema + AI-search tool, not primarily a content brief generator.

**Correction needed:** Update the sub-skill description from "keyword research, content briefs, meta generation, internal linking analysis" to "technical SEO, E-E-A-T, schema markup, GEO/AEO, backlinks, local SEO, maps intelligence, and Google API integrations (Search Console, PageSpeed, GA4)."

---

### awesome-claude-code-subagents (VoltAgent GitHub)

**Status:** CONFIRMED

**Finding:** Repo exists at github.com/VoltAgent/awesome-claude-code-subagents. 100+ subagents confirmed. Organised into categories (core development, language specialists, etc.). The doc's claim of "Next.js developer subagent, Shopify developer subagent, SEO analyst subagent, Content writer subagent, Code reviewer subagent" as specific examples could not be individually verified against the category list from search alone, but the overall repo description and 100+ count is confirmed. Note: VoltAgent also has a related repo `awesome-agent-skills` with 1,000+ skills for Claude Code, Codex, Gemini CLI, and Cursor.

**Correction needed:** None. Note about the related `awesome-agent-skills` repo is additive information only.

---

### Ahrefs MCP availability

**Status:** CORRECTED (caveat should be removed)

**Finding:** Official Ahrefs MCP server confirmed at github.com/ahrefs/ahrefs-mcp-server. Available via Ahrefs paid plans from Lite tier. Exposes keyword overviews, search volumes by country, keyword difficulty, traffic potential, growth trends, backlink analysis, and competitive insights. Claude Code integration documented at docs.ahrefs.com/mcp/docs/claude-code. This is an official Ahrefs product, not community-built.

The doc's "Caveat on Ahrefs MCP: Ahrefs MCP availability and current pricing require verification" is now unnecessarily cautious. The tool is confirmed available. The caveat about pricing is reasonable since Lite plan cost changes, but availability is not in question.

**Correction needed:** Update Section 4 Ahrefs MCP caveat. Change from "Ahrefs MCP availability and current pricing require verification" to "Ahrefs MCP is confirmed available on paid plans from Lite tier. Verify current Lite plan pricing at ahrefs.com before committing to the workflow."

Also: the Ahrefs MCP integrates directly into claude-seo (AgriciDaniel) as one of its official integrations -- these two tools are related and worth cross-referencing in the doc.

---

### mcpmarket.com and agentskills.so

**Status:** CONFIRMED

**Finding:** mcpmarket.com confirmed as MCP directory listing 10,000+ servers across 23+ categories. Also hosts an Agent Skills directory at mcpmarket.com/tools/skills. agentskills.so confirmed as a separate site for discoverable Claude Code skills (a Shopify theme development skill appeared at agentskills.so/skills/...). Both exist and function as described.

**Correction needed:** None.

---

## Corrections to apply to claude-code-ecommerce.md

1. **Section 4, claude-seo description**: Replace "19 sub-skills covering keyword research, content briefs, meta generation, internal linking analysis" with "19 sub-skills covering technical SEO, E-E-A-T, schema markup, GEO/AEO, backlinks, local SEO, maps intelligence, and Google API integrations (Search Console, PageSpeed, GA4)."

2. **Section 4, Ahrefs MCP caveat**: Replace "Caveat on Ahrefs MCP: Ahrefs MCP availability and current pricing require verification. The pattern is documented but tool-specific details may have changed." with "Ahrefs MCP is confirmed available (github.com/ahrefs/ahrefs-mcp-server) on paid plans from Lite tier. Verify current Lite plan cost at ahrefs.com before committing."

3. **Section 1, install command**: Optionally add Windows caveat: on native Windows (non-WSL), wrap with `cmd /c`: `claude mcp add --transport stdio shopify-dev-mcp -- cmd /c npx -y @shopify/dev-mcp@latest`.

---

*Fact-check complete 2026-04-25.*
