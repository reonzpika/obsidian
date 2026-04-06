# Skills Index

All Claude Code skills available in this workspace. Invoke with `/skill-name`.

---

## My Skills — Session Management

| Skill | Scope | When to use |
|---|---|---|
| `/session-update` | Personal | End of any working session — updates weekly progress log, creates follow-up task files, updates project step status |

---

## My Skills — Obsidian Vault

| Skill | Scope | When to use |
|---|---|---|
| `/obsidian` | Project | Orient Claude for vault project management work — loads vault structure and rules |
| `/obsidian-markdown` | Project | Create or edit `.md` files with Obsidian-specific syntax: wikilinks, callouts, embeds, properties |
| `/obsidian-task-table` | Project | Generate a correctly-structured task table (dataviewjs + meta-bind selects) for any vault file |
| `/obsidian-bases` | Project | Create or edit `.base` files — database-like views with filters, formulas, summaries |
| `/obsidian-cli` | Project | Interact with a running Obsidian instance via CLI — read, create, search, manage notes |

---

## My Skills — Visual / Canvas

| Skill | Scope | When to use |
|---|---|---|
| `/json-canvas` | Project | Create or edit `.canvas` files — nodes, edges, groups, mind maps, flowcharts |

---

## My Skills — Integrations

| Skill | Scope | When to use |
|---|---|---|
| `/calendar-sync` | Project | Sync active sprint files to Google Calendar (Projects Roadmap) |

---

## My Skills — Utilities

| Skill | Scope | When to use |
|---|---|---|
| `/defuddle` | Project | Extract clean markdown from a web page — use instead of WebFetch for articles, docs, blog posts |

---

## Built-in Claude Code Skills

Bundled with the Claude Code app. Always available across all projects.

| Skill | When to use |
|---|---|
| `/claude-api` | Build apps with the Claude API or Anthropic SDK — auto-triggers when code imports `anthropic` / `@anthropic-ai/sdk` |
| `/claude-md-improver` | Audit and improve CLAUDE.md files in any repository |
| `/claude-automation-recommender` | Analyse a codebase and recommend Claude Code automations (hooks, subagents, skills, MCP servers) |

---

## Plugin: Productivity

Installed Claude desktop app plugin. Skills for task management and working memory.

| Skill | When to use |
|---|---|
| `/start` | Initialise the productivity system — bootstrap working memory from existing task list |
| `/task-management` | Add, complete, or review tasks in TASKS.md |
| `/update` | Sync tasks and refresh memory from current activity — pull new assignments, triage overdue items |
| `/memory-management` | Manage the two-tier memory system (CLAUDE.md + memory/ directory) |

---

## Plugin: Data

Installed Claude desktop app plugin. Skills for SQL, data analysis, and visualisation.

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

Installed Claude desktop app plugin. Skills for specs, roadmaps, and research synthesis.

| Skill | When to use |
|---|---|
| `/write-spec` | Write a feature spec or PRD from a problem statement or feature idea |
| `/roadmap-update` | Update, reprioritise, or create a product roadmap |
| `/sprint-planning` | Plan a sprint — scope work, estimate capacity, set goals |
| `/metrics-review` | Review and analyse product metrics with trend analysis and recommended actions |
| `/synthesize-research` | Synthesise user research (interviews, surveys, feedback) into structured insights |
| `/stakeholder-update` | Generate a stakeholder update tailored to audience and cadence |
| `/competitive-brief` | Create a competitive analysis brief for a competitor or feature area |

---

## MCP Skills

Exposed by connected MCP servers via claude.ai integrations.

| Skill | Source | When to use |
|---|---|---|
| `/claude.ai Vercel:vercel_help` | Vercel MCP | Get help and guidance on Vercel features, best practices, and configuration |

---

## Skill file locations

| Scope | Path |
|---|---|
| Personal (all projects) | `C:\Users\reonz\.claude\skills\` |
| Project (vault only) | `C:\Users\reonz\cursor\obsidian\.claude\skills\` |
| App plugins | `AppData\Local\Packages\Claude_pzs8sxrjxfjjc\...\rpm\` — managed by Claude desktop app |
| Built-in | Bundled with Claude Code — no file path |
