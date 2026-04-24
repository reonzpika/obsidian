# Brain Dump Inbox

Drop any thought, idea, or task here with no structure required.
At session start, process this file: create task files from any actionable items, then clear processed items.

---

## 2026-04-24 — Claude ecosystem ideas

**1. Board + web search**
Board skill currently has `allowed-tools: []` — no tools available during a session. Step 0 source-read mentions Gmail MCP but those calls are blocked. Want to add web search capability so board can pull live research (competitor data, regulatory updates, pricing) mid-discussion. Key constraint: search must serve the board goal only — Claude must not lose track of the main question and go down research rabbit holes. Needs a guardrail in the skill: one search, return the fact, continue the discussion.

**2. Research agents for nexwave-rd**
Want background research agents that run autonomously against the nexwave-rd dashboard — e.g. scan for new SaMD regulatory updates, competitor moves, new NZ clinical AI publications, MBIE policy changes. Output lands in vault or dashboard so I can focus on high-level management and decisions rather than doing the research manually each session.

**3. Proactive Claude ecosystem suggestions**
At the moment I have to manually ask Claude to use skills/routines/agents. Want Claude to proactively surface these tools when the context warrants it — e.g. "this looks like a /board discussion", "there's a skill for this", "I could run a background agent for the research part". Less friction, more leverage from the ecosystem I've already built.

---
