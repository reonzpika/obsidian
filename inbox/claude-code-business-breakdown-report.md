# Claude Code End-to-End Breakdown: From Beginner to Advanced for Business - Reference Report

**Source:** https://www.youtube.com/watch?v=pUykUYkFVTM
**Analysed via:** Gemini 2.5 Flash (transcript-only mode)
**Speaker:** Simon (inferred from transcript reference "Simon MacBook F5" at [10:55])
**Channel:** Aentic Academy / Agentic OS
**Duration:** 02:41:41
**Status:** First draft. Requires human review before use as reference.

> **Note:** Visual analysis is limited. The video exceeded Gemini's direct video analysis token limit (1M tokens), so analysis is based on the auto-generated transcript only. On-screen demos, diagrams, and UI walkthroughs are inferred from spoken references, not direct visual inspection.

---

## Overview

A 2h 42m end-to-end tutorial on Claude Code aimed at non-developer business owners and solopreneurs. The speaker claims 300+ hours of hands-on use and walks through everything from installation to running parallel agent teams. The course is structured around building a "content repurposing engine" as a running example.

---

## Core Thesis

Claude Code is fundamentally different from chatbots because it acts on the user's computer directly: writing files, running commands, interacting with apps, and testing outputs. The speaker argues that most people plateau because they skip the foundational primitives (`claude.md`, skills, planning frameworks). Mastering those three things unlocks everything else, including Co-Work, and is the path to building repeatable, high-quality business systems.

---

## Transcript Summary

**[00:00] Introduction**
- Speaker claims 300+ hours building products with Claude Code, running a paid community.
- Frames the video as the path from terminal setup to parallel agents and business automation.
- Key promise: move from "AI-like output" to systems that sound like the user wrote them.

**[01:23] Why Claude Code Is Different**
- Compares Claude Code to ChatGPT, Claude web, Gemini, Custom GPTs, Claude Projects.
- All chatbots "hit the same wall at the chat window" - they can think and plan but cannot act.
- Claude Code "lives on your computer" and can write files, run commands, create folders, test results.
- User examples: Jane (agentic workflows), Donovan (contract reviews), Alli/Katherine/Prakar (websites), Mark (two apps in 3 weeks), Hogar (LinkedIn research), Oliver (personalised outreach).

**[06:36] Claude Code vs. Claude Co-Work**
- Co-Work has a friendlier visual UI but is built on the same engine and has fewer features currently.
- Skills and `.md` files are portable between Claude Code and Co-Work.
- Recommendation: learn Claude Code first; Co-Work becomes obvious after that.

**[08:34] Setup (Mac and Windows)**
- Mac: VS Code, Git check, `curl` install of Claude Code, path troubleshooting, login, NodeJS.
- Windows: VS Code, Git, Claude Code install, environment variable path fix, login, NodeJS, `Set-ExecutionPolicy` fix for npm.
- Recommends Claude account subscription over API for cost.

**[24:38] Understanding Markdown**
- `.md` files appear everywhere in Claude Code: `claude.md`, skills, plans.
- AI reads markdown well and understands document structure, which preserves context.

**[27:00] First Build: Simple Content Repurposing Engine**
- Zero-setup demo: create a folder, paste a transcript into `transcript.txt`, prompt Claude to generate LinkedIn post, X thread, and newsletter draft into a `/drafts` folder.
- Output is generic ("doesn't sound like me at all") - sets up the rest of the course.

**[35:10] Four Ways to Improve Outputs**
1. Context: teach Claude your business, audience, voice via a `.md` file.
2. Skills: process documents / SOPs that auto-invoke.
3. Personality / Agents: specialists for specific jobs.
4. Planning: break complex tasks into small focused steps to avoid context rot.

**[40:00] Permissions and `settings.json`**
- Three approaches: `--dangerously-skip-permission` (risky), no pre-approval (tedious), recommended pre-approved allow/deny list via `settings.json`.
- Allow: reading/editing files, running tests/dev servers, Git operations.
- Deny: package installs, file deletion, sending external data, reading sensitive files.
- Mentions Claude Code "auto mode" (research preview) for automatic classification.

**[43:18] `claude.md`: Your Project's Brain**
- "If you only learn one thing, make it this."
- Loaded into context at the start of every session.
- Five questions it should answer: What is this project? How do I run things? What patterns do I follow? What's weird here? What's the process?
- Keep under ~200 lines. Use the "Don't Dump Trick": point to external reference files rather than embedding all content.
- Demonstrates using Claude itself to generate `claude.md` via "ask user questions" feature.

**[53:51] Parent Inheritance**
- `claude.md` files inherit from parent folders up the directory tree; closest file takes priority.
- Example hierarchy: `projects/master-claude.md` > `content-engine/claude.md` > `agency-rules.md` > `client-specific-rules.md`.
- Common references (brand voice, universal rules) belong at higher folder levels for wide inheritance.

**[01:02:18] Global vs. Local Installation**
- Global (`~/.claude/`): loads everywhere, harder to debug.
- Local (within project folder): visible, editable, easier to control context.
- Rule of thumb: always install locally first using `--local` flag.

**[01:06:00] Planning Frameworks**
- Context rot is the main enemy for longer projects.
- Three tiers:
  1. Plan Mode (built-in): tasks under an hour; Claude reads and thinks, cannot write; produces `spec.md`.
  2. PRD Taskmaster (skill, GitHub: `anon byte 93`): multi-hour projects; 12-step workflow generating `prd.md`, `architecture.md`, tracking scripts.
  3. GSD Framework ("Get Shit Done", skill by Tash): multi-day builds; three commands per phase: `/gsd plan`, `/gsd execute`, `/gsd verify`.

**[01:14:50] Slash Commands**
- For weekly tasks that repeat with the same brief but different inputs.
- Live in `.claude/commands`; invoked manually with `/command`.
- Supports dynamic `$arguments`. Keep files succinct (no large context dumps).

**[01:23:07] Skills (Called "The Most Powerful Concept")**
- Key difference from commands: Claude invokes skills automatically based on natural language and the skill's description in YAML front matter.
- A skill is a folder containing `skill.md` plus optional `references/` folders, scripts, or assets.
- `skill.md` structure: YAML front matter (name, description, triggers, "do not trigger when") + step-by-step instruction body.
- Progressive disclosure: description always loaded; body loaded only when triggered; reference files loaded only at the specific step that calls them. Saves tokens, prevents context rot.
- Demonstrates building a `content-repurpose` skill with `content-angles.md` and `platform-formatting.md` reference files.
- Six-step framework for building skills: Name, Triggers, Outcome State, Dependencies, Step-by-step Instructions, Edge Cases/Examples.
- Installation: `npx skills add <repo_name> --local`.
- Skills are portable across Claude Code, Claude.ai, Co-Work, API, and other platforms.
- Anthropic's Skill Creator skill can be installed to help build skills correctly.

**[01:48:23] Hooks**
- Automated actions outside skills and commands; live in `settings.json`.
- Examples: ban word checker, task completion notifications, GitHub staging, secret protection.

**[01:50:47] MCP Servers**
- "USB-C of the AI agent world" - unified interface for external app APIs.
- Allows Claude to read from and write to Notion, HubSpot, Gmail, Google Drive, etc.
- Finding MCPs: `mcp.so`, `mcpservers.org`.
- Demo: connects Notion MCP, searches a YouTube videos database, pulls a transcript, runs the content-repurpose skill, pushes the LinkedIn post back to a Notion column.

**[01:58:19] Plugins**
- Bundle of skills, hooks, and slash commands in one installable package.
- Speaker avoids them personally to keep context clean; caution advised on quality.
- `/plugin` command shows installed plugins.

**[01:59:40] Planning Frameworks (Detailed Demo)**
- PRD Taskmaster: 12-step workflow including discovery questions, directory setup, PRD creation, 13-point quality validation.
- GSD Framework: `/gsd plan` > `/gsd execute` > `/gsd verify` per phase; creates `state.md`, `roadmap.md`, `requirements.md`, per-phase plans. Speaker notes max plan likely required for single-day completion of large projects.

**[02:13:40] Agents, Sub-Agents, and Agent Teams**
- Each terminal/conversation is an agent; `claude.md` acts as its system prompt.
- Sub-agents: isolated-context specialists spun off by Claude for self-contained jobs. Built-in: `plan`, `explore`, `general-purpose`.
- Agent teams (experimental): multiple agents communicate with each other and share a task list. Enabled via `claude.code.experimental.agent.teams` in `settings.json`.
- Controversial opinion: well-structured `claude.md` files + skills already achieve much of what agents offer; beginners should not jump to agents first.

**[02:23:38] Quickfire New Features (Early 2026)**
- `/loop`: recurring prompt on a cron interval; expires after 3 days by default; session must stay open.
- `git worktrees` (`claude -w`): isolated copies of a repo branch for parallel feature work.
- `/clear`: clears conversation context.
- `/remote-control`: access Claude Code from a phone via URL or QR code.
- `claude --resume`: view and resume past conversations.

**[02:33:16] Closing**
- Three most important things: `claude.md`, skills (build/use), context/planning frameworks.
- Hot tips: use plan mode always; build one skill for a weekly task; connect one MCP; defer sub-agents until experienced.

---

## Visual Analysis

Visual analysis limited - transcript only.

The speaker references the following on-screen content at various points (inferred from spoken descriptions):
- Split-screen Mac/Windows setup demo [08:37].
- VS Code sidebar showing folder structures and generated files throughout.
- Markdown preview panels showing rendered `.md` output.
- Terminal bottom bar showing context usage ("12% of context window" at [01:09:44]).
- Diagrams of parent inheritance folder hierarchy, global vs. local file structure, and sub-agent/agent team communication.
- Live Notion database with LinkedIn post columns being populated by Claude via MCP.
- Phone screen showing remote control messages appearing in terminal [02:31:06].
- `/loop` cron expression in terminal output [02:24:42].

---

## All Concepts, Tools, People, and Entities Referenced

| Name | What it is / Why mentioned |
|---|---|
| Claude Code | Primary tool: local AI agent that writes files, runs commands, interacts with apps |
| Anthropic | Company that built Claude and Claude Code |
| Claude Co-Work | Newer Anthropic product with visual UI, same engine as Claude Code |
| ChatGPT / Gemini / Claude web | Chatbots used as contrast - "hit the wall" at the chat interface |
| VS Code | Development environment for Claude Code; used throughout |
| Git | Version control system; required for developer tooling |
| NodeJS / npm / nvm | JavaScript runtime and package manager; needed for installing tools/plugins |
| Markdown / `.md` files | Formatting language used throughout Claude Code for instructions, plans, skills |
| `claude.md` | Project brain file; loaded into context every session |
| `settings.json` | Config file for permissions and hooks |
| `spec.md` | Plan output file from Plan Mode |
| Context rot | Degradation of output quality as context window fills |
| Plan Mode | Built-in Claude Code feature: read-only planning phase |
| Slash commands | Manually invoked repeatable prompts in `.claude/commands` |
| Skills | Auto-invoking process folders with `skill.md` and reference files |
| Progressive disclosure | Layered context loading to save tokens |
| Hooks | Automated event-based actions in `settings.json` |
| MCP Servers | Model Context Protocol: unified interface to external app APIs |
| Plugins | Bundles of skills, hooks, and commands |
| PRD Taskmaster | GitHub skill (anon byte 93) for multi-hour project planning |
| GSD Framework | "Get Shit Done" skill by Tash; for multi-day builds |
| `git worktrees` | Git feature for isolated parallel branches |
| `/loop` | Claude Code recurring task scheduler (cron-based, 3-day default expiry) |
| `/remote-control` | Phone-based remote access to Claude Code session |
| `claude --resume` | Resume past Claude Code conversations |
| Notion | Workspace app; demonstrated via MCP integration |
| Supabase | Database MCP server example |
| Context 7 | MCP for up-to-date library documentation |
| shadcn/ui | React UI component library (docs via Context 7) |
| PostHog | Product analytics tool (docs via Context 7) |
| mcp.so / mcpservers.org | MCP server marketplaces |
| skillsmpp.com | Claude Code skills marketplace (800k skills claimed) |
| Aentic Academy | Speaker's paid community; source of "Agentic OS" |
| Aentic OS Command Center | UI being built to manage multiple terminals and GSD frameworks |
| Boris Churnney | Cited as creator of Claude Code; mentioned as always using plan mode |
| Jane, Donovan, Alli, Katherine, Prakar, Mark, Hogar, Oliver, Martin, James, Jury | Named community members used as user examples |

---

## Key Takeaways

- Claude Code acts on your computer (files, commands, apps) - it is not a chatbot.
- `claude.md` is the single highest-leverage thing to learn. Keep it under 200 lines and use "Don't Dump" (point to reference files, don't embed everything).
- Skills are automatable SOPs. The progressive disclosure pattern (description > body > reference files) is what makes them scale without degrading context.
- Context rot is the main failure mode for longer sessions. Always use at least Plan Mode; use PRD/GSD for multi-hour or multi-day work.
- Install everything locally first (`--local` flag). Global installation is harder to debug and pollutes context.
- MCP servers are the bridge to your actual business tools (Notion, HubSpot, Gmail). One MCP connection transforms Claude Code from a local tool to a workflow automation layer.
- Beginners should master `claude.md` and one skill before touching agents, plugins, or teams.
- `/loop` exists but has a 3-day expiry and requires an open session. Not yet suitable for unattended long-running automation.
- Agent teams are experimental; well-structured `claude.md` files achieve similar results without the overhead.
- The portability of skills across Claude Code, Co-Work, and API is significant: build once, reuse everywhere.

---

## Claims Requiring Verification

| Claim | Timestamp | Notes |
|---|---|---|
| "300+ hours" with Claude Code | [00:00] | Personal testimonial, unverifiable |
| Claude Co-Work "built in a week with Claude Code" | [06:51] | Anthropic product claim; check Anthropic blog |
| "Claude Code currently more powerful than Co-Work" | [07:18] | May have changed since recording; verify feature parity |
| Subscription cheaper than API for typical use | [12:01] | Depends heavily on usage patterns; model pricing changes |
| Prakar "built first landing page in 15 minutes" | [01:47] | User testimonial, subjective |
| Mark "two apps in 3 weeks" | [02:06] | User testimonial; comparison to prior timeline is subjective |
| `/loop` expires after 3 days by default | [02:23:46] | Feature-specific; verify against current Claude Code docs |
| `/loop` can be extended past 3 days | [02:26:25] | Workaround claim; verify |
| GSD framework requires Max plan for single-day completion | [02:09:29] | Pricing-tier claim; verify current plan tiers |
| skillsmpp.com has 800,000 skills | [01:41:01] | Website statistic; may be inflated or cached |

---

## Open Questions

- What are the actual token costs per session for typical skill invocations vs. direct prompts? The video does not give concrete figures.
- How are API keys and secrets managed securely when connecting MCP servers, especially on shared or multi-user machines?
- Are there official Anthropic-maintained MCP servers, or is the ecosystem entirely community-built?
- How does one manage version control and team collaboration for `claude.md` and skill files across a team?
- What exactly constitutes the `/loop` 3-day expiry and can it be reset without manual intervention?
- Is there a way to run Claude Code tasks fully unattended (no open terminal session) for overnight or scheduled automation?
- The speaker deprecates custom agents in favour of `claude.md` + skills - has Anthropic published guidance on when agents genuinely add value over skills?
- How does the experimental agent teams feature interact with `claude.md` parent inheritance?
- Is `skillsmpp.com` officially affiliated with Anthropic, or is it a third-party community marketplace?
