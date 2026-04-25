---
title: "Claude Code for Miozuki: Background Agents, Hooks, and Content Automation"
created: 2026-04-25
status: draft
tags: [miozuki, claude-code, automation, tools]
---

# Claude Code for Miozuki: Background Agents, Hooks, and Content Automation

Research date: 2026-04-25. First draft for Ryo's review. All tool names and pricing verified via web search; verify current details before acting.

---

## 1. Claude Code Max Plan: What You Actually Get

Two tiers:
- **Max 5x** ($100/month USD): 5x the usage of Pro; 5-hour rolling usage window
- **Max 20x** ($200/month USD): 20x the usage; same 5-hour rolling window

Features are identical between tiers; the difference is pure capacity. Background agents, parallel forks, hooks, MCP servers, and all Claude Code features are available on both. The Max plan is not a different product -- it is the same Claude Code CLI with higher throughput limits.

The 5-hour rolling window means usage resets continuously, not on a fixed monthly date. Heavy multi-agent sessions (several forks running in parallel) consume the window faster than single-thread work.

---

## 2. Background Agents and Fork Mode

### How fork mode works

When Claude Code spawns a fork (`Agent` call without `subagent_type`), the fork:
- Inherits the full conversation context (no re-briefing required)
- Shares the parent's prompt cache (cache hits at 10% of standard input price)
- Runs in the background; parent conversation stays responsive
- Returns a single result message when complete

Multiple forks sent in a single message run in parallel. This is the primary pattern for batch work: fire 3-5 forks for independent research or content tasks, get results back asynchronously.

### Parallel agent support

Available since Claude Code v2.1.32+. You are already using this pattern in this session (the three research forks running right now are an example). The mechanism is stable.

### Practical throughput

A single Claude Code session with Max 5x can run 4-6 parallel forks without hitting limits for typical research or content generation tasks. For heavy batch work (generating 100+ product descriptions, running 10+ research agents simultaneously), Max 20x is the safer tier.

---

## 3. Hooks for Content Automation

Hooks are shell commands that fire automatically on tool events. They run outside the AI context, on your local machine (or CI). Four hook types:

| Hook type | When it fires | Primary use |
|---|---|---|
| `PreToolUse` | Before any tool executes | Gate dangerous operations; inject context |
| `PostToolUse` | After any tool executes | Auto-commit, spell check, format check |
| `Stop` | When Claude finishes a turn | Run tests, notify, log output |
| `Notification` | On system events | Alert on task completion |

Hooks are configured in `.claude/settings.json` (project-level) or `~/.claude/settings.json` (global). They receive tool input/output as JSON via stdin.

### Content automation hooks relevant to Miozuki

**Auto-commit written markdown:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{"type": "command", "command": "cd $PROJECT_DIR && git add -A && git commit -m 'Claude Code: auto-commit content'"}]
    }]
  }
}
```
Every time Claude Code writes a file, git auto-commits. Useful for tracking all AI-generated draft content without manual commit steps.

**Spell/style check on markdown writes:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{"type": "command", "command": "vale --glob='*.md' $TOOL_OUTPUT_PATH 2>&1 | head -20"}]
    }]
  }
}
```
Vale is a prose linter; runs after every markdown write. Catches passive voice, NZ English violations, and style errors before content reaches Ryo for review.

**Stop hook for batch completion notification:**
```json
{
  "hooks": {
    "Stop": [{"type": "command", "command": "notify-send 'Claude Code' 'Batch complete' 2>/dev/null || true"}]
  }
}
```
Fires a desktop notification when an unattended multi-agent batch completes.

**PreToolUse gate for Bash on production:**
Blocks any `git push` or Shopify deployment until a custom condition is met. Useful if running Claude Code against the production miozuki-web repo.

---

## 4. Custom Slash Commands

### How they work

Create `.claude/commands/` in any repo. Each `.md` file in that directory becomes a slash command available in that Claude Code session. The file content is the command prompt.

Example: `.claude/commands/product-description.md`
```markdown
Generate a product description for {{PRODUCT_NAME}} using Miozuki's brand voice. 
Tone: editorial, informed, not salesy. NZ English. 150-200 words.
Mention: stone type, setting, care, ethical sourcing angle.
Do not use: "stunning", "gorgeous", "perfect", "unique".
```
Usage: `/product-description` in Claude Code; prompts for `{{PRODUCT_NAME}}`.

### Curated command repositories

**awesome-claude-code** (`github.com/hesreallyhim/awesome-claude-code`): community-curated list of slash commands, hooks, MCP configs, agent orchestrators, and workflow examples. Start here for vetted community patterns.

**wshobson/commands**: production-ready slash command set covering code review, test generation, refactor, and documentation. Extraction/adaptation of relevant commands (e.g. `review-content`) for content workflows is straightforward.

### Miozuki-specific commands worth building

- `/product-description [product]`: generates Miozuki brand-voice product copy
- `/seo-meta [page]`: generates title, description, OG tags for a given page
- `/blog-outline [topic]`: structures a moissanite education blog post
- `/pin-caption [product]`: generates Pinterest pin caption + board suggestion
- `/faq-entry [question]`: generates FAQ schema-ready Q&A pair for the stone guide

---

## 5. Shopify AI Toolkit MCP (April 2026)

Shopify announced and shipped an official MCP server for Claude Code on April 15, 2026.

### Setup

One command:
```bash
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
```

After adding, verify with `claude mcp list`. The server appears as `shopify-dev-mcp`.

### What it gives Claude Code

~16 agent skills across three areas:
- **shopify-admin**: inventory, orders, metafields, product management via Admin API
- **shopify-liquid**: theme development, section schemas, Liquid template help
- **shopify-hydrogen**: headless storefront, Storefront API, React Server Components

### Hydrogen MCP proxy (2026.1.4+)

Miozuki's stack is headless Next.js over Shopify Storefront API, not Hydrogen. But this is still relevant: Hydrogen 2026.1.4 shipped a built-in Storefront MCP proxy at `/api/mcp` with `proxyStandardRoutes` enabled by default. The pattern -- an MCP proxy that gives Claude Code live product data -- can be replicated for Next.js with a custom `/api/mcp` route.

**Practical application for Miozuki:** A custom Next.js API route that exposes Shopify product catalogue data via MCP context lets Claude Code read live inventory, pricing, and product details during any content generation task. No manual copy-pasting of product specs.

### NZ merchant note

Shopify Agentic Storefronts (product discovery in ChatGPT, Perplexity, Google AI Mode) was US-only as of March 2026. Verify current NZ eligibility at shopify.com/editions/winter2026 before assuming it is active on miozuki.co.nz.

---

## 6. Social Media MCP Integrations

### Instagram MCP (via Composio)

Composio provides an Instagram MCP that connects Claude Code to an Instagram Business or Creator account.

Capabilities:
- Publish posts, carousels, reels
- Read analytics (reach, engagement, impressions)
- Schedule content
- Retrieve comments

Setup: Composio's MCP config requires an Instagram Business account linked to a Facebook Page, and a Meta Developer app with Instagram Graph API access. Not trivial to set up; the Composio abstraction reduces the OAuth complexity. Verify current setup docs at composio.dev.

**Miozuki fit:** Instagram Business account required (Creator may work; verify with Composio docs). Enables Claude Code to generate a caption and publish a post in a single command. Workflow: Midjourney generates background, Claude Code composites + writes caption + publishes via MCP.

### Ayrshare MCP

Ayrshare is a social media API that aggregates 13+ platforms behind a single API key. MCP integration available.

Platforms supported: Pinterest, Twitter/X, Facebook, Instagram, TikTok, LinkedIn, Reddit, Threads, YouTube, Telegram, Bluesky.

75+ tools exposed via MCP: post creation, scheduling, analytics, comment management.

**Pricing:** Verify current plans at ayrshare.com; plans start around $29/month USD. The MCP integration is available on paid plans.

**Miozuki fit:** Pinterest is the highest-value platform for Miozuki SEO (covered in community-seo-strategy.md). Ayrshare's MCP lets Claude Code post product pins with descriptions, alt text, and board assignment directly. Eliminates manual publishing step.

### Content to Social MCP

Transforms existing content (blog post, product page, guide section) into platform-specific social posts. Processes in 10-15 seconds.

**Miozuki fit:** Feed `/moissanite-guide` page content or blog posts; get Instagram caption, Pinterest pin text, and TikTok script generated simultaneously. Platform-appropriate tone and length handled automatically.

---

## 7. Programmatic SEO via Claude Code

### Batch product description pattern

Pattern validated by DTC brands in 2026: provide a CSV of product names and attributes, Claude Code generates formatted descriptions for all rows, writes to output file. Scale: 100 products in 2-3 hours with a single Max 5x session.

**Implementation sketch:**
1. Export product data from Shopify admin as CSV
2. Claude Code reads CSV, iterates rows
3. Custom `/product-description` slash command applied to each row
4. Output written to a new CSV or markdown file
5. PostToolUse hook auto-commits each written file

For Miozuki's current catalogue size this is overkill. The pattern becomes relevant when launching the `/moissanite-guide` page with 10-15 retailer profiles: Claude Code can draft all profiles in a single batch session, with Ryo reviewing the output before committing.

### FAQ schema batch generation

Same pattern for FAQ schema: provide a list of questions (from the moissanite guide brief), Claude Code generates JSON-LD schema entries for each. Output reviewed by Ryo, then inserted into the relevant page component.

---

## 8. Miozuki Implementation Priority

| Action | Effort | When | Why |
|---|---|---|---|
| Add Shopify AI Toolkit MCP | 5 min | Now | Gives Claude Code live product data for all content tasks |
| Build /product-description slash command | 1-2 hr | Now | Speeds up any catalogue or guide content work |
| Build /pin-caption slash command | 30 min | Now | Pinterest is highest-value SEO platform for Miozuki |
| Set up auto-commit hook | 30 min | Now | Tracks all AI-generated content in git without manual steps |
| Ayrshare MCP for Pinterest publishing | 2-4 hr | Months 1-3 | Automates pin publishing; $29/month plan required |
| Composio Instagram MCP | 2-4 hr | Months 1-3 | Automates Instagram post publishing; Meta dev app setup required |
| Next.js Storefront MCP proxy | 4-8 hr | Months 1-3 | Live product data in Claude Code context; dev work required |
| Batch guide content generation | 1 session | Months 4-6 | When /moissanite-guide build starts |

**Immediate action (5 minutes):** Run `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest` in the miozuki-web repo. No code changes, no build step. Claude Code immediately gains access to Shopify admin and Storefront API context.

---

## Sources

- [Shopify AI Toolkit MCP announcement, April 2026](https://shopify.dev/docs/storefronts/headless/claude-ai-toolkit)
- [Claude Code hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [awesome-claude-code curated repo](https://github.com/hesreallyhim/awesome-claude-code)
- [Ayrshare MCP social media integration](https://www.ayrshare.com/social-media-api-mcp/)
- [Composio Instagram MCP](https://composio.dev/integrations/instagram/)
- Claude Code changelog v2.1.32+ (parallel agents)
- Claude Code Max plan feature set (anthropic.com/claude-code)

*First draft, April 2026. Requires Ryo review before acting on any recommendation.*
