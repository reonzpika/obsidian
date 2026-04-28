# 5 Agentic Patterns for Claude Code - Reference Report

**Source:** https://www.youtube.com/watch?v=38t5UBCa4OI
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Unknown (unidentified male presenter)
**Channel:** Unknown
**Duration:** 17:50
**Status:** First draft. Requires human review before use as reference.

---

## Overview

A practical walkthrough of five agentic patterns for Claude Code, targeting users who currently work one conversation at a time. The presenter argues that sequential single-session use is inefficient and that Claude Code is architected to support parallel, autonomous, and multi-agent workflows. Aimed at developers who want to move beyond basic usage.

---

## Core Thesis

Claude Code is built to run like a managed team, not a single assistant. Most users operate it as a sequential tool, which wastes its capacity. By adopting five progressively autonomous patterns, from manual parallel sessions through to fully headless scheduled workflows, users can eliminate context rot, parallelize independent work, and automate repetitive tasks without being present.

---

## Patterns Overview

| # | Pattern | Human Role | Agents | Comms | Best For |
|---|---------|-----------|--------|-------|----------|
| 0 | Built-in sub-agents | Passive (automatic) | Explore, Plan, General-purpose | Internal | All sessions |
| 1 | Sequential Flow | Active, sequential | 1 | N/A | Dependent iterative work |
| 2 | The Operator | Active orchestrator | N (separate terminals) | None (human merges) | Independent parallel tasks |
| 3 | Split and Merge | Prompt only | N sub-agents, 1 main | Through main agent only | Parallel related research |
| 4 | Agent Teams | Prompt + oversight | N full instances | Direct agent-to-agent | Complex cross-functional work |
| 5 | Headless | None (set and leave) | 1+ | N/A | Automated / scheduled batch |

---

## Transcript Summary

**0:00 - 0:35: Hook and problem framing**
Using Claude Code one conversation at a time is compared to running a team inefficiently. Claude is built for parallel work; most users do not use this.

**0:35 - 2:46: Built-in sub-agents (Pattern 0)**
Claude Code already routes tasks to specialised sub-agents automatically:
- **Explore Agent:** Haiku model, read-only tools. Handles file discovery and codebase search without polluting main context. Invocable at quick / medium / very thorough thoroughness.
- **Plan Agent:** Inherits main model, read-only tools. Runs during plan mode (Shift+Tab twice or `/plan`) to gather context before presenting a strategy. Cannot spawn further sub-agents.
- **General-purpose Agent:** Inherits main model, all tools. Handles complex multi-step tasks requiring both exploration and code modification.

Boris Cherny (Claude Code co-creator) noted as heavy user of sub-agents.

**2:46 - 4:18: Pattern 1: Sequential Flow**
Default interaction. Shared context grows linearly. Tasks must run in order; each step builds on prior output. Context rot (degradation from a full context window) is the main failure mode. Mitigations: `/clear` (wipes history) and `/compact` (wipes history, retains summary).

**4:18 - 7:31: Pattern 2: The Operator**
Run separate Claude Code sessions via `claude -w <worktree-name>`. Each session is an isolated context window. Worktrees appear under `.claude/worktrees/`. Human coordinates and merges outputs manually. Practical ceiling around 4-5 terminals. Demonstrated in VS Code with three parallel worktrees (`new-onboarding-flow`, `fix-checkout-bug`, `redesign-user-settings`).

**7:31 - 11:44: Pattern 3: Split and Merge**
Single session. Claude fans out a prompt into up to 10 parallel sub-agents (queues further tasks beyond that), each working independently. No cross-talk between sub-agents; all results flow back through the main agent, which synthesises them. Custom sub-agents can be defined in `.claude/agents/` with a markdown spec file (name, description, tools, responsibilities, output format). Demonstrated via the `gsd-advisor-researcher` agent from the get-shit-done (GSD) framework.

**11:44 - 14:29: Pattern 4: Agent Teams**
Experimental feature. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` in `settings.json` env block. Shipped as research preview with Opus 4.6. Each agent is a full Claude Code instance. Agents communicate directly via a shared task list; a Team Lead orchestrates. User navigates between agents with Shift+Up/Down. Token usage estimated at 4-7x a single session. Reserved for genuinely complex cross-functional tasks.

**14:29 - 17:20: Pattern 5: Headless**
`claude -p "prompt"` runs Claude with no interactive loop; no human approvals required. Integrates with cron (Mac/Linux) or Windows Task Scheduler. Output structured via JSON schema. Some users apply a "Ralph Loop": feed output back as next-iteration input, letting Claude self-iterate to a quality threshold. Key risk is trust; guardrails (read-only tools, strict output schema) are essential.

**17:20 - 17:50: Conclusion**
Recap of five patterns. Reference to Agentic Academy (linked in video description) for deeper material on skills, custom sub-agents, and `CLAUDE.md` structuring.

---

## Visual Analysis

Slides use a dark animated grid background. Each pattern has a dedicated diagram:

- **Sequential Flow:** Linear arrow chain (You -> Task 1 -> Task 2 -> ... -> Task N), enclosed in a "SHARED CONTEXT GROWS OVER TIME" box.
- **The Operator:** Central "You (orchestrator)" radiating to 4 isolated Terminal boxes. Label: "NO CONNECTION BETWEEN TERMINALS - YOU COORDINATE".
- **Split and Merge:** Main Agent fans out to Sub-agents 1-5 in parallel (FAN OUT), all converge back (FAN IN). Label: "ALL PARALLEL - NO CROSS-TALK".
- **Agent Team:** Team Lead connected to a "Shared task list", with 3 Agent boxes having bidirectional "message" arrows between each other. Label: "AGENTS COMMUNICATE WITH EACH OTHER".
- **Headless:** Cron/Scheduler -> `claude -p 'prompt'` -> `output.json`, with a loop-back arrow labelled "Iterates". Guardrails box top-right. Label: "NO HUMAN IN THE LOOP - FIRE AND FORGET".

Terminal demos show:
- Context window status bar: `Opus 4.5 | [##################] 18% | 590/200K`
- VS Code with `.claude/worktrees/` directory structure
- `gsd-advisor-researcher.md` sub-agent spec file on GitHub
- Agent Teams terminal output with token counts per agent

---

## All Concepts, Tools, People, and Entities Referenced

| Item | Type | Notes |
|------|------|-------|
| Claude Code | Product | Anthropic AI coding CLI |
| Haiku | Model | Used by Explore agent; fast, low-latency |
| Sonnet | Model | Used by General-purpose agent |
| Opus 4.6 | Model | Used for Agent Teams research preview |
| Explore Agent | Built-in sub-agent | Read-only, codebase search |
| Plan Agent | Built-in sub-agent | Read-only, plan mode research |
| General-purpose Agent | Built-in sub-agent | Full tools, complex tasks |
| Context rot | Concept | Context window degradation from overload |
| `/clear` | Command | Wipes conversation history |
| `/compact` | Command | Wipes history, keeps summary |
| `-w` flag | CLI flag | Creates worktree session |
| `-p` flag | CLI flag | Headless prompt mode |
| Worktrees | Git feature | Separate working directories per session |
| `.claude/agents/` | Directory | Custom sub-agent definitions |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Env var | Enables Agent Teams feature |
| Boris Cherny | Person | Claude Code co-creator; noted heavy sub-agent user |
| get-shit-done (GSD) | Framework | Meta-prompting / context engineering system by TACHES |
| TACHES | GitHub account | Creator of GSD framework |
| `gsd-advisor-researcher` | Custom agent | Research agent from GSD; produces structured comparison tables |
| Ralph Loop | Community technique | Claude self-iterates on output until quality threshold met |
| Agentic Academy | Resource | Linked in video description; deeper Claude Code content |
| cron | Tool | Unix scheduler for headless automation |
| Windows Task Scheduler | Tool | Windows equivalent for headless automation |

---

## Key Takeaways

1. Claude Code already uses built-in sub-agents (Explore, Plan, General-purpose) automatically in every session.
2. Sequential Flow is fine for dependent iterative work; context rot is the failure mode to watch.
3. The Operator pattern gives each task a clean context window; human is the merge layer.
4. Split and Merge lets Claude fan out up to 10 parallel sub-agents from a single prompt; limit is no cross-talk between agents.
5. Custom sub-agents in `.claude/agents/` are markdown spec files; Claude routes to them automatically based on description.
6. Agent Teams allow direct agent-to-agent communication; cost is 4-7x normal token usage.
7. Agent Teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` in `settings.json` env block.
8. Headless mode (`claude -p`) integrates with OS schedulers for fully autonomous batch work.
9. Guardrails (read-only tools, JSON schema output) are essential for headless trust.
10. Pattern selection is a cost/complexity tradeoff: Sequential < Operator < Split and Merge < Agent Teams < Headless (by setup complexity); Headless < Agent Teams (by token cost).

---

## Claims Requiring Verification

| Claim | Timestamp | Flag |
|-------|-----------|------|
| Explore agent uses Haiku model | 0:59 | Internal implementation detail; may change |
| General-purpose agent uses Sonnet | 2:00 | Internal implementation detail; may change |
| Split and Merge limit is 10 sub-agents | 9:10 | Check current docs; may be configurable |
| Boris Cherny uses 15 sub-agents at once | 9:05 | Contradicts stated 10 limit; context unclear |
| Agent Teams uses 4-7x more tokens | 12:20 | Estimate only; varies by task |
| Agent Teams shipped with Opus 4.6 as research preview | 12:26 | Check current feature status |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` is the correct env var key | 12:31 | Verify against current docs |
| Headless users have shipped "entire projects overnight" | 17:07 | Anecdotal; no source cited |

---

## Open Questions

- What are the actual per-session cost implications of each pattern at typical task volume?
- How does error handling and logging work in headless mode with no human present?
- How configurable are guardrails beyond read-only tools (e.g., per-tool allow-lists, output schema enforcement)?
- How does Split and Merge queue management work beyond 10 agents: FIFO, priority, or other?
- Is Agent Teams still experimental in the current Claude Code release, or has it been promoted?
- What is the recommended `CLAUDE.md` structure for projects using custom sub-agents?
- Are there public benchmarks on quality or time-saving from agentic vs. sequential workflows?
