# Skills Index

All Claude Code skills available in this workspace. Invoke with `/skill-name`.

---

## Rituals

| Skill | When to use |
|---|---|
| `/daily` | Morning orientation and midday check-in — updates `weekly.md` |
| `/daily-review` | Evening day review — reconstructs today's work across sessions |
| `/weekly` | End-of-week review and planning — archives `weekly.md`, resets for next week |
| `/monthly` | End-of-month review and planning — rolls up weekly summaries |
| `/session-update` | End of any working session — writes session log to `logs/`, updates briefing in `weekly.md` |
| `/handoff` | Generate a structured handoff prompt for the next Claude session |
| `/calendar-sync` | Sync active items to Google Calendar (Projects Roadmap) |

---

## Vault and Project Management

| Skill | When to use |
|---|---|
| `/obsidian` | Orient Claude for vault project management work — loads vault structure and rules |
| `/obsidian-markdown` | Create or edit `.md` files with Obsidian-specific syntax: wikilinks, callouts, embeds, properties |
| `/obsidian-task-table` | Generate a correctly-structured task table (dataviewjs + meta-bind selects) for any vault file |
| `/obsidian-bases` | Create or edit `.base` files — database-like views with filters, formulas, summaries |
| `/obsidian-cli` | Interact with a running Obsidian instance via CLI — read, create, search, manage notes |
| `/json-canvas` | Create or edit `.canvas` files — nodes, edges, groups, mind maps, flowcharts |
| `/vault-audit` | Structural audit — counts tasks, sprints, checks for inconsistencies |
| `/adopt` | One-time setup skill for this vault |

---

## Strategy and Research

| Skill | When to use |
|---|---|
| `/board` | High-level strategic thinking before any execution — multi-perspective canvas, produces PRD/ADR/memo |
| `/deep-research` | Generate a detailed ready-to-paste prompt for Claude's deep research feature |
| `/agent-batch` | Delegate 2+ independent tasks to background agents in parallel |
| `/run-agents` | Run multiple background agents for complex multi-step tasks |
| `/session-search` | Search across all Claude Code session transcripts |

---

## Communication

| Skill | When to use |
|---|---|
| `/gmail-draft` | **Always use this for email drafts.** Never use Gmail MCP for outgoing email. |
| `/gws` | Access Google Workspace (Gmail, Drive, Calendar, Docs, Sheets) via gws CLI |
| `/email-triage` | Deep Gmail triage for key project contacts (Medtech, partners, MBIE, etc.) |
| `/email-triage-project` | Project-scoped email audit — all sent and received emails for one project |
| `/linkedin-post-drafter` | Draft a LinkedIn post using Ryo's established voice and content pillars |
| `/medtech-prep` | Pre-meeting briefing for Medtech Global and partner meetings |

---

## Development

| Skill | When to use |
|---|---|
| `/bff-debug` | Debug a live BFF issue — check service status, read logs, test health |
| `/bff-deploy` | Deploy updated BFF code to Lightsail |
| `/bff-rotate-secret` | Rotate BFF_INTERNAL_SECRET — update Vercel env vars |
| `/alex-endpoint-test` | Test a new ALEX FHIR endpoint from scratch |
| `/deploy-to-vercel` | Deploy a Next.js project to Vercel — env vars, domain, smoke test |
| `/stripe-webhook-debug` | Diagnose Stripe webhook issues |
| `/frontend-design` | Create distinctive, production-grade frontend UI — React/Next.js/Tailwind |
| `/ui-ux-pro-max` | UI/UX design intelligence — styles, palettes, font pairings |
| `/claude-api` | Build, debug, and optimise Claude API and Anthropic SDK apps |

---

## Code Quality

| Skill | When to use |
|---|---|
| `/bug-audit` | Full bug audit for a reported issue — trace data flow, find all bugs, fix in priority order |
| `/systematic-debugging` | Structured debugging for any bug, test failure, or unexpected behaviour |
| `/test-driven-development` | TDD workflow — write tests before implementation |
| `/verification-before-completion` | Use before claiming work is complete — verify tests pass, smoke test |
| `/simplify` | Review changed code for reuse, quality, and efficiency |
| `/review` | Review a pull request |
| `/security-review` | Security review of pending changes on the current branch |

---

## Content and Media

| Skill | When to use |
|---|---|
| `/youtube-analyse` | Analyse a YouTube video using Gemini 2.5 Flash — comprehensive summary |
| `/pdf-edit` | Programmatic PDF editing — fill form fields, insert text, remove overlays |
| `/defuddle` | Extract clean markdown from a web page — use instead of WebFetch for articles and docs |
| `/mermaid-zoom` | Add click-to-enlarge functionality to Mermaid diagrams in Obsidian |

---

## System and Config

| Skill | When to use |
|---|---|
| `/update-config` | Configure `settings.json` or `.mcp.json` — **always use this, never edit directly** |
| `/fewer-permission-prompts` | Scan transcripts, add allowlist to reduce permission prompts |
| `/keybindings-help` | Customise keyboard shortcuts, rebind keys, modify keybindings.json |
| `/loop` | Run a prompt or skill on a recurring interval |
| `/schedule` | Create or manage scheduled remote agents on a cron schedule |
| `/model-shortcut-setup` | Set up OS-level text expansion shortcuts for Claude Code model switching |
| `/claude-hud:setup` | Configure claude-hud as the statusline |
| `/claude-hud:configure` | Configure HUD display options |

---

## Skill Management

| Skill | When to use |
|---|---|
| `/skill-creator` | Create new skills, modify and improve existing skills |
| `/evolve` | End-of-session skill reviewer — scores quality, suggests improvements |
| `/evolve-queue` | Batch /evolve — walks all pending sessions |
| `/claude-md-improver` | Audit and improve CLAUDE.md files |
| `/claude-md-management:revise-claude-md` | Update CLAUDE.md with learnings from this session |
| `/claude-automation-recommender` | Analyse a codebase and recommend Claude Code automations |
| `/init` | Initialise a new CLAUDE.md file with codebase documentation |

---

## Plugin: Data

Built-in Claude desktop app plugin. For SQL, data analysis, and visualisation.

| Skill | When to use |
|---|---|
| `/explore-data` | Profile a dataset — shape, quality, null rates, distributions, anomalies |
| `/analyze` | Answer data questions — quick lookups to full trend analyses |
| `/sql-queries` | Write or optimise SQL across Snowflake, BigQuery, Databricks, PostgreSQL |
| `/write-query` | Translate a natural-language data need into optimised SQL |
| `/statistical-analysis` | Apply statistical methods — descriptive stats, outlier detection, hypothesis testing |
| `/data-visualization` | Create charts with Python (matplotlib, seaborn, plotly) |
| `/create-viz` | Generate publication-quality visualisations from query results or DataFrames |
| `/build-dashboard` | Build an interactive self-contained HTML dashboard with charts and filters |
| `/validate-data` | QA an analysis before sharing — methodology, accuracy, and bias checks |

---

## Plugin: Product Management

Built-in Claude desktop app plugin. For specs, roadmaps, and research synthesis.

| Skill | When to use |
|---|---|
| `/write-spec` | Write a feature spec or PRD from a problem statement or feature idea |
| `/roadmap-update` | Update, reprioritise, or create a product roadmap |
| `/metrics-review` | Review and analyse product metrics with trend analysis |
| `/synthesize-research` | Synthesise user research (interviews, surveys, feedback) into structured insights |
| `/stakeholder-update` | Generate a stakeholder update tailored to audience and cadence |
| `/competitive-brief` | Create a competitive analysis brief for a competitor or feature area |

---

## MCP Skills

| Skill | Source | When to use |
|---|---|---|
| `/claude.ai Vercel:vercel_help` | Vercel MCP | Get help and guidance on Vercel features and configuration |

---

## Skill file locations

| Scope | Path |
|---|---|
| Personal skills (all projects) | `C:\Users\reonz\.claude\skills\` |
| Personal commands (all projects) | `C:\Users\reonz\.claude\commands\` |
| Project skills (vault only) | `C:\Users\reonz\cursor\obsidian\.claude\skills\` |
| App plugins | `AppData\Local\Packages\Claude_pzs8sxrjxfjjc\...\rpm\` — managed by Claude desktop app |
| Built-in | Bundled with Claude Code — no file path |
