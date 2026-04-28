# 5 Advanced Claude Code Patterns That Will Change How You Work - Reference Report

**Source:** https://www.youtube.com/watch?v=38t5UBCa4OI
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Simon Coton
**Channel:** Simon Coton
**Duration:** 17:50
**Status:** First draft. Requires human review before use as reference.

---

## Overview

A practical walkthrough of five Claude Code agentic workflow patterns, ranging from basic sequential use to fully autonomous headless execution. Aimed at developers already using Claude Code who want to move beyond single-conversation interactions. The video is demonstrative: each pattern is explained with diagrams and live terminal examples.

---

## Core Thesis

Claude Code is built for multi-agent, parallelised, and autonomous operation, not just linear conversation. Most users only use the sequential mode, leaving significant productivity gains on the table. The five patterns presented form a progression from simple shared context through to fully automated fire-and-forget workflows, and understanding them allows developers to structure Claude as an actual team rather than a single assistant.

---

## Built-in Sub-agents (Background Context)

Claude Code already uses specialised sub-agents automatically. Understanding them is prerequisite to the five patterns.

| Sub-agent | Model | Tools | Purpose |
|---|---|---|---|
| Explore | Haiku (fast, low-latency) | Read-only | File discovery, code search, codebase exploration |
| Plan | Inherits from main | Read-only | Codebase research during `/plan` mode; cannot spawn further sub-agents |
| General-purpose | Inherits from main | All tools | Complex, multi-step tasks requiring both exploration and modification |

Each sub-agent has its own context window. This keeps the main conversation clean and prevents context rot. Claude routes tasks to the appropriate sub-agent without explicit instruction.

---

## Patterns Summary

| # | Pattern | Best For | Key Constraint |
|---|---|---|---|
| 1 | Sequential Flow | Iterative work with dependencies | Context window fills over time |
| 2 | The Operator | Independent parallel tasks, user orchestrates | You can only manage ~4-5 terminals |
| 3 | Split and Merge | Related but independent parallel tasks | Sub-agents cannot talk to each other |
| 4 | Agent Team | Complex interdependent work with cross-checks | Experimental; 4-7x token cost |
| 5 | Headless | Automated, scheduled, batch work | Requires high trust; limited iteration |

---

## Transcript Summary

**00:00 - 00:35 Introduction**
Sequential task-by-task usage described as "wrong." Analogy: you would not run a team sequentially. Claude Code is built for parallel, specialist deployment.

**00:35 - 02:44 Built-in Sub-agents**
Claude already delegates behind the scenes. Explore (Haiku, read-only) handles codebase search. Plan (read-only) activates in plan mode and prevents infinite nesting. General-purpose (all tools) handles tasks needing both exploration and modification. All three keep the main context clean.

**02:44 - 04:26 Pattern 1: Sequential Flow**
One shared context, tasks run in order. Each task builds on the last. Context rot is the main failure mode as the window fills. Mitigation: `/.claude/commands`, `/clear`, `/compact`.

**04:26 - 07:31 Pattern 2: The Operator**
Run separate isolated sessions in parallel: `claude -w <branch-name>` creates a worktree with its own branch and context window. You orchestrate, combining outputs yourself. No cross-terminal communication. Practical limit is 4-5 terminals. Worktrees clean up on session close.

**07:31 - 11:44 Pattern 3: Split and Merge**
One prompt fans out to up to 10 concurrent sub-agents, each with a clean context. Results funnel back to the main agent which merges and presents output. Custom sub-agents can be defined in `.claude/agents/` with roles, tools, and context. The GSD framework (by Tash) is cited as a real-world implementation. Builder-validator chain is a specific sub-pattern: one agent builds, another reviews, main agent arbitrates.

**11:44 - 14:29 Pattern 4: Agent Team**
A Team Lead coordinates agents that can communicate directly with each other via a shared task list, not just through the orchestrator. Best for tasks with genuine cross-functional overlap (e.g., pricing, messaging, and app changes for a product launch). Currently experimental: requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"` in `settings.json`. Token cost estimated at 4-7x a single session. Each teammate is a full Claude Code instance.

**14:29 - 17:50 Pattern 5: Headless**
`claude -p "prompt"` runs Claude without human interaction. Output saved to file (e.g., `output.json`). Pair with cron or a scheduler for automated recurring tasks. Use `--allow-tools` to restrict what Claude can do. The "Ralph Loop" repeatedly feeds the same prompt until a task is complete. Some users reportedly ship entire projects overnight using this mode.

---

## Visual Analysis

The video uses a consistent visual language: speaker to camera for concept introduction, then clean minimal diagrams for each pattern, then live VS Code terminal for implementation. Key visuals:

- **Sub-agent slide overlays:** Black background, white text with bullet definitions. Clearly shows model, tools, and purpose for each built-in agent.
- **Pattern diagrams:** Each pattern has its own labelled flow diagram. Pattern 3 (Split and Merge) shows the fan-out/fan-in structure explicitly. Pattern 4 (Agent Team) shows bidirectional arrows between agents, distinct from Pattern 3's hub-and-spoke.
- **Worktree demo:** Three side-by-side terminals (`claude -w new-onboarding-flow`, `claude -w fix-checkout-bug`, `claude -w redesign-user-settings`) with corresponding folders visible in VS Code's file explorer under `.claude/worktrees/`.
- **GSD GitHub repo:** Shows the `.claude/agents/` folder structure and the contents of `gsd-advisor-researcher.md`, which defines agent name, description, tools, and output format.
- **Agent Team terminal output:** Shows team-lead, blog-writer, carousel-writer, newsletter-writer with per-agent token and time metrics. Demonstrates navigating between teammates.
- **Headless diagram:** Shows the cron trigger, `claude -p`, output file, and optional JSON schema guardrail in a single linear flow.

---

## All Concepts, Tools, People, and Entities Referenced

| Item | Type | Notes |
|---|---|---|
| Claude Code | Tool | Anthropic's AI dev environment |
| Haiku | Model | Anthropic's fastest, cheapest model. Used for Explore sub-agent |
| Sonnet | Model | Anthropic model. Used for General-purpose sub-agent |
| Opus | Model | Anthropic's most capable model. Mentioned in context of Agent Teams |
| `.claude/` folder | Config location | Stores agents, commands, hooks, skills, worktrees |
| `claude -w <branch>` | CLI flag | Opens a new isolated worktree |
| `claude -p "prompt"` | CLI flag | Headless mode, no human interaction |
| `--allow-tools` | CLI flag | Restricts which tools Claude can use in headless mode |
| `/plan` command | Claude Code command | Enters plan mode, triggers Plan sub-agent |
| `/clear` command | Claude Code command | Clears conversation history |
| `/compact` command | Claude Code command | Clears history but retains a summary |
| `shift+tab` | Keyboard shortcut | Cycles into plan mode |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Environment variable | Must be set to `"1"` to enable Agent Teams |
| GSD (Get Shit Done) | Framework | Meta-prompting framework for Claude Code by Tash |
| Tash | Person | Creator of the GSD framework |
| Ralph Loop | Concept | Repeatedly feeds a prompt until task completion |
| Agentic Academy | External resource | Full Claude Code course linked in video description |
| VS Code | Tool | Code editor used for all demos |
| `settings.json` | Config file | Used to set env vars including Agent Teams flag |
| `output.json` / `report.json` | Output format | Example filenames for headless structured output |
| cron / Task Scheduler | Tools | Scheduling utilities for triggering headless Claude |
| `.claude/worktrees/` | Folder | Where worktree environments are created and managed |

---

## Steps Covered (Tutorial-Specific)

1. Understand the three built-in sub-agents (Explore, Plan, General-purpose) and what each does.
2. Use Sequential Flow for iterative, dependent tasks. Manage context with `/clear` and `/compact`.
3. Use `claude -w <branch>` to open parallel worktrees for independent tasks. Act as orchestrator.
4. Use a single prompt to trigger Split and Merge; Claude fans out to sub-agents automatically. Define custom agents in `.claude/agents/`.
5. Enable Agent Teams via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"`. Explicitly instruct Claude to use a team in the prompt.
6. Use `claude -p "prompt"` for headless execution. Pipe to scheduled tasks. Add `--allow-tools` guardrails.

---

## Key Takeaways

- Most Claude Code users are leaving parallelisation and automation capability unused by defaulting to sequential conversation.
- Built-in sub-agents already operate behind the scenes; understanding them explains why context windows stay cleaner than expected.
- Worktrees (`claude -w`) are the practical tool for parallel independent work with no setup complexity.
- Split and Merge is the most accessible form of parallelisation: one prompt, Claude handles the fan-out.
- Agent Teams is powerful but experimental, token-expensive, and should be reserved for tasks with genuine cross-functional interdependence.
- Headless mode changes the relationship with Claude from interactive tool to autonomous team member. High trust required.
- Custom agents in `.claude/agents/` with defined roles, tools, and output formats are the key customisation lever for Split and Merge and Agent Teams.
- Context rot is the primary failure mode for Sequential Flow. Explicit context management (`/clear`, `/compact`, worktrees) is a first-class concern.
- The Ralph Loop pattern (repeated headless prompting until completion) enables full autonomous iteration.

---

## Claims Requiring Verification

- Sub-agent concurrency cap of 10 for Split and Merge (presented as fact; no source cited).
- Agent Teams token usage is "4-7x" a single session (speaker's estimate, not a measured figure).
- Agent Teams shipped as experimental with Opus 4.6 as a research preview (verify current status, as this may have changed).
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"` is the correct env var name and still required (check current Claude Code docs; experimental flags change frequently).
- Claims about users shipping "entire projects overnight" via headless mode (anecdotal, not documented).
- Haiku being the current model for the Explore sub-agent (may have been updated since recording).

---

## Open Questions

- What is the current release status of Agent Teams? Is it still experimental, and what are the known limitations?
- Are there documented best practices for structuring `.claude/agents/` definitions to avoid agent scope overlap or conflicting instructions?
- How does Claude handle failure modes in headless mode (network errors, tool failures, partial completion)? Is there a retry or rollback mechanism?
- What monitoring or logging is available for parallel worktree sessions or agent team runs?
- What is the practical token cost of Agent Teams on a representative engineering task? The "4-7x" estimate needs a concrete example.
- Are there output schema validation tools that work natively with `claude -p` for structured headless output, beyond a manual JSON schema check?
