---
title: Skill usage audit
created: 2026-04-25
type: audit
---

All output is a first draft for human review.

Note: all transcripts fall within the last 30 days (repository is relatively new or recently initialised). The total session count is therefore the primary ranking signal. Classification thresholds below are applied to total sessions rather than "last 30 days" sessions since they are identical.

- Frequently used: 10+ sessions
- Occasionally used: 3-9 sessions
- Low use: 1-2 sessions
- Never invoked: 0 sessions

---

## Summary

26 skills inventoried. None are "never invoked." The skill library is actively used across all items. The main concern is not stale skills but coverage gaps and trigger clarity: a few skills overlap in trigger language (run-agents vs agent-batch), two are one-time-setup tools that correctly show low counts, and several low-use skills have legitimate but infrequent trigger conditions (PDF editing, Stripe debugging, mermaid zoom) that are situationally appropriate rather than structurally underused.

Three areas to act on:
1. Resolve the `run-agents` / `agent-batch` overlap.
2. Improve trigger specificity on `handoff` and `medtech-prep`.
3. `stripe-webhook-debug` has 8 sessions but is stack-specific; keep but flag it may become stale if the stack evolves.

---

## Usage table

| Skill | Total sessions | Last used | Category | Recommendation |
|---|---|---|---|---|
| session-update | 127 | 2026-04-26 | Frequently used | Keep, high ROI, core ritual |
| evolve | 110 | 2026-04-26 | Frequently used | Keep, end-of-session standard |
| board | 43 | 2026-04-26 | Frequently used | Keep, strategic anchor |
| skill-creator | 29 | 2026-04-25 | Frequently used | Keep, used to build this list |
| gws | 27 | 2026-04-25 | Frequently used | Keep, core Google Workspace integration |
| gmail-draft | 24 | 2026-04-26 | Frequently used | Keep, enforces correct Gmail workflow |
| frontend-design | 19 | 2026-04-25 | Frequently used | Keep, high-value UI output |
| bug-audit | 13 | 2026-04-25 | Frequently used | Keep, systematic debugging |
| claude-automation-recommender | 11 | 2026-04-26 | Frequently used | Keep, growing use |
| claude-md-improver | 10 | 2026-04-25 | Frequently used | Keep, regular maintenance use |
| evolve-queue | 8 | 2026-04-25 | Occasionally used | Keep, batch version of evolve |
| stripe-webhook-debug | 8 | 2026-04-25 | Occasionally used | Keep short-term, review if Stripe work ends |
| email-triage | 6 | 2026-04-25 | Occasionally used | Keep, clear trigger |
| alex-endpoint-test | 5 | 2026-04-25 | Occasionally used | Keep, specific to Medtech integration |
| session-search | 4 | 2026-04-26 | Occasionally used | Keep, useful for retrospective queries |
| deep-research | 4 | 2026-04-25 | Occasionally used | Keep, improve trigger wording |
| agent-batch | 3 | 2026-04-26 | Occasionally used | Keep, but resolve overlap with run-agents |
| handoff | 3 | 2026-04-25 | Occasionally used | Keep, improve trigger wording |
| mermaid-zoom | 3 | 2026-04-25 | Occasionally used | Keep, situational use is correct |
| deploy-to-vercel | 2 | 2026-04-25 | Low use | Keep, infrequent by nature |
| email-triage-project | 2 | 2026-04-25 | Low use | Keep, distinct from email-triage |
| linkedin-post-drafter | 2 | 2026-04-25 | Low use | Keep, needs trigger clarification |
| medtech-prep | 2 | 2026-04-25 | Low use | Keep, meeting-gated use is correct |
| model-shortcut-setup | 2 | 2026-04-25 | Low use | Keep, one-time setup, counts are expected |
| run-agents | 2 | 2026-04-25 | Low use | Investigate overlap with agent-batch |
| pdf-edit | 1 | 2026-04-25 | Low use | Keep, situational, strong skill content |

---

## Retirement candidates

None. Every skill has been invoked at least once in the current transcript window. No retirement is recommended at this time.

The lowest-use skills (pdf-edit, model-shortcut-setup, run-agents, medtech-prep) are all situationally appropriate: PDF editing is not a daily task, model shortcuts are a one-time setup, medtech-prep fires only before specific meetings, and run-agents overlaps with agent-batch.

---

## High-value skills (invest more)

**session-update (127 sessions)** and **evolve (110 sessions)** are the backbone of the daily workflow. Any improvement to their templates or output quality has compounding value.

**board (43 sessions):** Most-used strategic skill. Worth auditing whether its output format is prompting the right downstream actions, or whether sessions end without a clear decision captured.

**gmail-draft (24 sessions):** High use, and the trigger-enforcement role (redirect from Gmail MCP) is working. Worth reviewing if new gws features have changed the optimal draft flow.

**frontend-design (19 sessions):** High use for a design tool. Worth checking whether the 67-style/96-palette library is being actively drawn on or ignored by default.

**bug-audit (13 sessions):** Systematic debugging use is healthy. Consider whether the skill template has been updated to reflect any new stack components (Supabase edge functions, Vercel deployments).

---

## Trigger improvements needed

**run-agents vs agent-batch:** These two skills have near-identical trigger language. `run-agents` description says "run agents, send agents, spin up agents" and `agent-batch` says "run agents, fire agents, kick off agents, background agents". In practice, agent-batch is the more complete orchestrator (triage, prompts, recovery, inbox organisation). Recommendation: retire `run-agents` or merge its Phase 4 review loop into `agent-batch`, keeping only one entry point.

**handoff (3 sessions):** Strong skill, low discoverability. The description only triggers on explicit handoff requests. Users mid-session who need to wrap up may not think to say "write a handoff." Consider adding trigger phrases like "I need to stop here", "continue this tomorrow", or "pause this task."

**deep-research (4 sessions):** Trigger is clear but the skill produces a prompt rather than executing research directly. The description should state this upfront ("generates a prompt for Claude.ai deep research") so users know to expect a prompt, not a result.

**linkedin-post-drafter (2 sessions):** The skill loads a voice profile from `C:/Users/reonz/cursor/LinkedIn/knowledge/`. Verify those files exist before the skill is likely to produce high-quality output. If the voice profile has not been built out, either build it or set realistic expectations in the description.

**medtech-prep (2 sessions):** Uses Gmail MCP tools (`mcp__claude_ai_Gmail__search_threads`) in its allowed-tools list. Per the MEMORY.md feedback, Gmail MCP should not be used for outgoing drafts, but reading threads for research appears to be acceptable. Confirm this is intentional and consistent with the gws-over-MCP preference.

**email-triage vs email-triage-project:** Triggers overlap ("triage the MBIE thread" could hit either). The distinction is useful (general triage vs. single-counterparty deep dive) but the descriptions need a clearer decision rule, e.g. "use email-triage for daily inbox processing; use email-triage-project when you need a complete historical thread audit for one counterparty."
