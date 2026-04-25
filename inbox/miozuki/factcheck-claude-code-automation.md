---
title: "Fact-check: claude-code-content-automation.md"
created: 2026-04-25
status: draft
---

# Fact-check: claude-code-content-automation.md

Checked 2026-04-25 via web search. Sources: Claude Max pricing support page, Claude Code hooks reference, Shopify AI Toolkit changelog, Ayrshare pricing page, GitHub repos.

---

## Verified claims

- **Max 5x = $100/month, Max 20x = $200/month**: Confirmed. Both tiers and prices are accurate.
- **5-hour rolling usage window**: Confirmed. The 5-hour window is real; there is also a weekly limit mentioned in some sources but the 5-hour window description is accurate for Claude Code usage limits.
- **Features identical between tiers (only capacity differs)**: Confirmed.
- **Forks inherit full conversation context and share prompt cache**: Confirmed accurate description of fork behaviour.
- **Shopify AI Toolkit install command**: `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest` confirmed correct.
- **~16 agent skills in Shopify Dev MCP**: Confirmed. Sources describe "around 16 agent skills" across admin, Liquid, Hydrogen, Functions, Storefront, and checkout extensions.
- **Hydrogen 2026.1.4 MCP proxy at /api/mcp with proxyStandardRoutes enabled by default**: Confirmed. The /api/mcp endpoint is proxied automatically when proxyStandardRoutes is enabled (which is the default in createRequestHandler).
- **awesome-claude-code at github.com/hesreallyhim/awesome-claude-code**: Confirmed. Repo exists, actively maintained, 21.6k stars.
- **wshobson/commands repo**: Confirmed at github.com/wshobson/commands. Production-ready slash command collection for Claude Code.
- **Composio Instagram MCP at composio.dev**: Confirmed. Publish, analytics, DM automation capabilities are accurate.
- **"Content to Social MCP" transforming content in 10-15 seconds**: Confirmed. Available at apify.com/godberry/content-to-social-mcp. The 10-15 second claim is accurate per documented benchmarks.
- **Shopify Agentic Storefronts: US-only as of March 2026**: Still flagged correctly as requiring NZ eligibility verification.

---

## Corrections needed

**1. Shopify AI Toolkit release date**
- Doc says: "Shopify announced and shipped an official MCP server for Claude Code on April 15, 2026."
- Correct: The release date is April 9, 2026, per the official Shopify developer changelog (shopify.dev/changelog). The ecommerce doc correctly states April 9. Correct this doc to match.

**2. Hook types: incomplete table**
- Doc says: "Four hook types: PreToolUse, PostToolUse, Stop, Notification"
- Correct: Claude Code has 12 lifecycle hook events, not 4. The four listed are real but the table is incomplete. Additional events include: UserPromptSubmit, PermissionRequest, SubagentStop, SubagentStart, SessionStart, SessionEnd, PreCompact, PostToolUseFailure.
- Recommendation: Change "Four hook types" to "Key hook types" or "Primary hook types" and add a note that additional lifecycle events exist. Alternatively list all 12. The four described are the most relevant for content automation, so framing them as key/primary is accurate.

**3. Slash command variable syntax**
- Doc says: `{{PRODUCT_NAME}}` in the example product-description.md command template.
- Correct: The variable substitution syntax in Claude Code slash commands is `$ARGUMENTS` (full argument string) or positional `$0`, `$1`, `$2`. The `{{VARIABLE}}` curly-brace syntax is NOT used by Claude Code. This example will not work as written.
- Recommendation: Replace `{{PRODUCT_NAME}}` with `$ARGUMENTS` or restructure the example to use `$0`.

**4. Slash command directory format is now legacy**
- Doc says: "Create `.claude/commands/` in any repo. Each `.md` file in that directory becomes a slash command."
- Correct: As of Claude Code v2.1.101 (released April 11, 2026), the recommended format is `.claude/skills/<name>/SKILL.md`. The `.claude/commands/` directory still works (backwards compatible) but is now the legacy format. The skills format supports the same `/name` invocation plus autonomous invocation by Claude.
- Recommendation: Add a note that `.claude/commands/*.md` is the legacy format and the current recommended structure is `.claude/skills/<name>/SKILL.md`.

**5. Ayrshare pricing**
- Doc says: "plans start around $29/month USD"
- Correct: Ayrshare's current Premium plan (entry tier) costs $149/month. The $29 figure does not correspond to any current Ayrshare plan. Verify at ayrshare.com/pricing before acting on this.

---

## Unverifiable / flags

- **Claude Code v2.1.32+ for parallel agents**: Could not confirm the specific version number. Parallel fork support is confirmed as a real feature, but the "v2.1.32+" version attribution could not be verified against release notes in this check.
- **Shopify Agentic Storefronts NZ eligibility**: Still unconfirmed. The US-only status as of March 2026 appears accurate; NZ availability requires checking the Shopify partner portal directly.

---

*Fact-check complete 2026-04-25. Apply corrections before sharing doc with stakeholders.*
