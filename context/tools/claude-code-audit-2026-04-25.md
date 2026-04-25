---
title: Claude Code setup audit
created: 2026-04-25
type: audit
---

## Executive summary

- All five recommendations from the 23 April 2026 audit remain unimplemented. This audit confirms the same gaps are still live two days later.
- The single highest-risk item is unchanged: `defaultMode: bypassPermissions` globally with zero repo-level `deny` rules. clinicpro-medtech (PHI), nexwave-rd (MBIE audit trail), and any live-posting repo can fire irreversible bash commands without a tool-level gate.
- No custom subagents (`~/.claude/agents/` still does not exist). Every session starts cold with no accumulated cross-session domain knowledge.
- No bash audit hook. With bypassPermissions active and no PreToolUse logging, there is no post-hoc record of what commands Claude ran.
- CLAUDE.md quality is genuinely strong across all repos. The weak point is not instructions but harness-enforced safety.

---

## Current config snapshot

### Global settings (`~/.claude/settings.json`)

| Key | Value | Notes |
|-----|-------|-------|
| `$schema` | MISSING | No IDE validation |
| `defaultMode` | `bypassPermissions` | Skips all permission checks globally |
| `model` | `sonnet` | Correct default |
| `effortLevel` | `high` | Good for complex work |
| `autoUpdatesChannel` | `latest` | Appropriate for power user |
| `skipDangerousModePermissionPrompt` | `true` | Consistent with bypassPermissions |
| `CLAUDE_CODE_FORK_SUBAGENT` | `1` | Subagents fork correctly |
| `CLAUDE_CODE_SUBAGENT_MODEL` | MISSING | Subagents default to Sonnet, not Haiku |
| `cleanupPeriodDays` | MISSING (default 30) | Transcripts deleted at 30 days |
| `language` | MISSING | NZ English not hinted at harness level |

### Hooks (`~/.claude/settings.json` hooks block)

| Event | Hook | Purpose |
|-------|------|---------|
| `PostToolUse` (Skill matcher) | `hook_skill.py` | Logs skill invocations for skill-evolver |
| `Stop` | `hook_stop.py` | Records transcript path for /evolve |
| `Stop` | `hook_session_update_pending.py` | Queues sessions needing /session-update |
| `SessionStart` | `hook_session_start_notify.py` | Alerts on pending session-updates |

**Missing hooks:** `PreToolUse` (bash audit log, git push gate, em dash scan), `PreCompact` (compaction prompt), `UserPromptSubmit`, `SubagentStop`, `PermissionRequest`. 4 of 25 hook events used.

### Per-repo `.claude/settings.json`

| Repo | Has settings.json | Notes |
|------|-------------------|-------|
| `clinicpro-saas` | No | No repo guardrails |
| `clinicpro-medtech` | No | PHI context, highest risk |
| `nexwave-rd` | No | MBIE audit trail, second-highest risk |
| `obsidian` | Has `.claude/` dir but NO settings.json | Only `settings.local.json` exists (spinner + additionalDirs) |

### Per-repo CLAUDE.md

| Repo | Has CLAUDE.md | Quality |
|------|---------------|---------|
| `clinicpro-saas` | Yes | Excellent: stack, commands, load-bearing patterns, coding standards, design system pointer |
| `clinicpro-medtech` | Yes | Solid: three-tier arch, PHI rules, env vars, hard constraints |
| `nexwave-rd` | Yes | Good: MBIE compliance framing, docs structure, sovereignty constraint |
| `obsidian` | Yes | Thorough: vault schema, workflow rules, frontmatter specs, gotchas |
| `~/.claude/CLAUDE.md` | Yes | Strong: identity, plan check protocol, irreversible action gates, formatting rules |
| `cursor/CLAUDE.md` | Yes | Workspace-level pointer, correct |

### Custom agents (`~/.claude/agents/`)

Directory does not exist. Zero custom agents defined anywhere.

### Skills

Global (`~/.claude/commands/`): 26 skills including `board`, `evolve`, `evolve-queue`, `email-triage`, `gmail-draft`, `gws`, `handoff`, `session-search`, `skill-creator`, `claude-md-improver`, `run-agents`, `agent-batch`.

Obsidian project (`obsidian/.claude/skills/`): 14 skills including `daily`, `weekly`, `monthly`, `obsidian`, `obsidian-markdown`, `vault-audit`, `calendar-sync`.

Repo-level skills (`~/.claude/skills/`): 9 skills including `bff-debug`, `bff-deploy`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `ui-ux-pro-max`.

### MCP servers

All via claude.ai managed integration. No `.mcp.json` in any repo or global `.claude/` dir.

Active: Gmail, Google Calendar, Google Drive, Notion, Vercel, Supabase, Scholar Gateway, Context7, claude-in-chrome.

Supabase MCP is available in every session including nexwave-rd (cross-contamination risk). No repo-level scoping.

### Memory

Auto-memory active. Project memory for obsidian vault at `~/.claude/projects/C--Users-reonz-cursor-obsidian/memory/MEMORY.md`: 20 entries, well-maintained, covering feedback, routing rules, and reference data.

No memory for: clinicpro-saas, clinicpro-medtech, nexwave-rd at the project level. No agents with `memory: user` frontmatter.

---

## Gap table

| # | Gap | Impact (1-5) | Ease (1-5) | Score | Priority |
|---|-----|-------------|------------|-------|----------|
| 1 | No repo-level `deny` rules in clinicpro-medtech (PHI + ALEX) | 5 | 4 | 20 | Critical |
| 2 | No custom agents at all (`~/.claude/agents/` missing) | 5 | 3 | 15 | High |
| 3 | `bypassPermissions` global with no compensating hooks | 5 | 3 | 15 | High |
| 4 | No `PreToolUse` bash audit hook | 4 | 4 | 16 | High |
| 5 | No repo-level `deny` in nexwave-rd (MBIE audit trail) | 4 | 4 | 16 | High |
| 6 | No `CLAUDE_CODE_SUBAGENT_MODEL=haiku` in env | 3 | 5 | 15 | Medium |
| 7 | No `$schema` in global settings.json | 2 | 5 | 10 | Medium |
| 8 | No `cleanupPeriodDays` set (defaults to 30 days) | 3 | 5 | 15 | Medium |
| 9 | Supabase MCP available in nexwave-rd (cross-contamination) | 4 | 3 | 12 | Medium |
| 10 | No `code-reviewer` agent with persistent memory | 4 | 3 | 12 | Medium |
| 11 | No `rd-researcher` agent for nexwave-rd R&D work | 3 | 3 | 9 | Medium |
| 12 | No `PreCompact` hook to preserve key context on compaction | 3 | 3 | 9 | Medium |
| 13 | No per-repo `memory/MEMORY.md` for clinicpro-saas or medtech | 3 | 3 | 9 | Medium |
| 14 | `evolve` and `board` skills can be auto-invoked by model | 3 | 4 | 12 | Medium |
| 15 | No `language` hint in settings.json (NZ English only in CLAUDE.md) | 1 | 5 | 5 | Low |

---

## Top 10 improvements

### 1. Add `deny` rules to clinicpro-medtech

**Why:** This repo handles PHI. ALEX FHIR calls go through the BFF. A Claude session should not be able to directly curl the ALEX API or touch patient data paths.

**Steps:**
1. Run `/update-config` in the clinicpro-medtech repo.
2. Create `C:/Users/reonz/cursor/clinicpro-medtech/.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Bash(curl *alexapi*)",
      "Bash(curl *medtechglobal*)",
      "Bash(curl *fhir*)",
      "Bash(rm -rf *)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(git commit*)"
    ]
  }
}
```

---

### 2. Add `deny` rules to nexwave-rd

**Why:** nexwave-rd is an MBIE audit trail. Accidental modification of `docs/obj-*/output/` artefacts (specs, decision records) without explicit intent could compromise the audit trail integrity.

**Steps:**
1. Create `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "ask": [
      "Edit(docs/obj-*/output/**)",
      "Write(docs/obj-*/output/**)",
      "Bash(git push*)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "disabledMcpjsonServers": ["supabase", "notion", "vercel"]
}
```

---

### 3. Create `~/.claude/agents/` directory and add `code-reviewer` agent

**Why:** A solo founder with 4+ active repos needs a code reviewer that accumulates domain knowledge across sessions (Drizzle pitfalls, Clerk metadata conventions, Ably strict mode, HMAC PHI handling). Agent memory makes this permanent.

**Steps:**
1. Create directory: `mkdir C:/Users/reonz/.claude/agents/`
2. Create `C:/Users/reonz/.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code changes for correctness, security, and alignment with repo patterns. Use PROACTIVELY when asked to review changes, check a diff, or audit a PR.
tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*)
model: sonnet
permissionMode: plan
memory: user
---

You are a senior code reviewer for a GP-founder's startup stack (Next.js, Clerk, Neon/Supabase Postgres, Drizzle, Ably, Stripe, Playwright, FHIR).

Before reviewing: read your memory for patterns and recurring issues. Check the repo's CLAUDE.md for load-bearing constraints.

Flag: PHI handling (never plaintext), Drizzle migration patterns (hand-rolled only, never drizzle-kit push), public webhook routes, Clerk metadata mutations, Ably strict-mode risk, em dashes in any text output.

After review: update memory with new patterns, summarise findings as numbered list with severity (blocker / warning / suggestion).
```

---

### 4. Add `PreToolUse` bash audit hook

**Why:** With bypassPermissions active, there is no tool-level gate on any bash command. A rolling JSONL audit log is the minimum viable safety net. Async, zero latency impact.

**Steps:**
1. Create `C:/Users/reonz/cursor/skill-evolver/hook_bash_log.py`:

```python
import json, sys, datetime, pathlib

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

log_dir = pathlib.Path.home() / ".claude" / "bash-audit"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"{datetime.date.today().isoformat()}.jsonl"
with open(log_file, "a", encoding="utf-8") as f:
    json.dump({
        "ts": datetime.datetime.now().isoformat(),
        "cwd": data.get("cwd"),
        "cmd": data.get("tool_input", {}).get("command"),
        "session": data.get("session_id")
    }, f)
    f.write("\n")
```

2. Run `/update-config` to add to global hooks:

```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python C:/Users/reonz/Cursor/skill-evolver/hook_bash_log.py",
        "async": true,
        "timeout": 3000
      }
    ]
  }
]
```

---

### 5. Set `CLAUDE_CODE_SUBAGENT_MODEL=haiku` in global env

**Why:** The `Explore` built-in agent already uses Haiku. Without this env var, any other subagent invocation defaults to Sonnet. File search, codebase exploration, and parallel read-only tasks all run fine on Haiku. Saves rate-limit budget for the main session.

**Steps:** Run `/update-config`, add to `env` block:

```json
"CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
```

---

### 6. Add `$schema` and `cleanupPeriodDays` to global settings

**Why:** `$schema` enables IDE validation of settings.json (60+ keys, easy to typo silently). `cleanupPeriodDays: 90` extends `session-search` history from 30 to 90 days, aligning with MBIE quarterly reporting.

**Steps:** Run `/update-config`:

```json
"$schema": "https://json.schemastore.org/claude-code-settings.json",
"cleanupPeriodDays": 90
```

---

### 7. Add `rd-researcher` agent for nexwave-rd R&D sessions

**Why:** Research sessions for Obj-1 pull in literature, architecture candidates, and competitor analysis. Running this inline pollutes the main session context with intermediate search results. An isolated agent with `model: opus` and read-only tools keeps the main context clean.

**Steps:** Create `C:/Users/reonz/.claude/agents/rd-researcher.md`:

```markdown
---
name: rd-researcher
description: Deep research agent for NexWave Health R&D. Use when tasked with literature search, competitor analysis, architecture evaluation, or MBIE compliance research.
tools: Read, Grep, Glob, WebFetch, WebSearch
model: opus
permissionMode: plan
memory: user
---

You are an R&D researcher for NexWave Health, an MBIE-funded programme (CONT-109091-N2RD-NSIWKC) building clinical AI for NZ primary care. Sovereignty constraint: identifiable NZ clinical data must stay in NZ.

Before researching: read your memory for prior findings on this topic. After researching: update memory with key findings, sources, and conclusions. Output a structured report suitable for the nexwave-rd docs repo.
```

---

### 8. Add `PreCompact` hook to preserve context on compaction

**Why:** When context compaction triggers automatically at ~95%, the compaction prompt is generic. A `PreCompact` hook can inject a custom prompt that tells Claude what to preserve (current task state, in-flight decisions, key file paths).

**Steps:** Run `/update-config` to add:

```json
"PreCompact": [
  {
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Before compacting, ensure you preserve: (1) the current task objective and any incomplete sub-steps, (2) all file paths you have opened or modified this session, (3) any decisions or constraints established during this session, (4) any errors encountered and their resolutions."
      }
    ]
  }
]
```

---

### 9. Disable `evolve` and `board` model auto-invocation

**Why:** `evolve` modifies skill files. `board` opens a multi-perspective strategy canvas. Both should be explicitly triggered by Ryo, never auto-invoked by the model mid-task.

**Steps:** For each of the following SKILL.md files, add `disable-model-invocation: true` to the frontmatter:

- `C:/Users/reonz/.claude/commands/evolve/SKILL.md`
- `C:/Users/reonz/.claude/commands/evolve-queue/SKILL.md`
- `C:/Users/reonz/.claude/commands/board/SKILL.md`
- `C:/Users/reonz/.claude/commands/handoff/SKILL.md`

---

### 10. Create per-project MEMORY.md seeds for clinicpro-saas and clinicpro-medtech

**Why:** The obsidian vault has a well-maintained MEMORY.md. clinicpro-saas and clinicpro-medtech have no project-level memory despite accumulating significant learnings (Drizzle migration pitfalls, Stripe webhook behaviour, BFF auth patterns). Auto-memory is active but unstructured. A seed MEMORY.md gives auto-memory a starting structure.

**Steps:**
1. Create `~/.claude/projects/C--Users-reonz-Cursor-clinicpro-saas/memory/MEMORY.md` with initial entries covering: Drizzle hand-rolled migration rule, Clerk metadata as feature flag store, `reactStrictMode: false` in dev, Stripe webhook public route requirement.
2. Create `~/.claude/projects/C--Users-reonz-Cursor-clinicpro-medtech/memory/MEMORY.md` with: three-tier request flow (Vercel → Lightsail BFF → ALEX), static IP constraint, HMAC PHI rule, Azure AD token 55-min cache.

---

## Quick wins (under 15 min each)

| # | Action | Time | File |
|---|--------|------|------|
| QW1 | Add `$schema` to `~/.claude/settings.json` via `/update-config` | 2 min | `~/.claude/settings.json` |
| QW2 | Add `cleanupPeriodDays: 90` via `/update-config` | 2 min | `~/.claude/settings.json` |
| QW3 | Add `CLAUDE_CODE_SUBAGENT_MODEL: haiku` to env via `/update-config` | 2 min | `~/.claude/settings.json` |
| QW4 | Create `~/.claude/agents/` directory | 1 min | filesystem |
| QW5 | Add `disable-model-invocation: true` to `evolve` SKILL.md frontmatter | 5 min | `~/.claude/commands/evolve/SKILL.md` |
| QW6 | Create `nexwave-rd/.claude/settings.json` with `disabledMcpjsonServers` | 10 min | new file |
| QW7 | Create `hook_bash_log.py` script (30 lines) | 10 min | `skill-evolver/hook_bash_log.py` |

All QW items together: approximately 30 minutes. QW1, QW2, QW3 are one `/update-config` call.

---

## Delta since 23 April 2026 audit

The prior audit (23 April 2026, at `context/tools/claude-code-audit-2026-04-23.md`) identified the same top gaps. As of 25 April, zero recommendations from that audit have been implemented:

| Prior recommendation | Status |
|---------------------|--------|
| Create per-repo `.claude/settings.json` with safety rules | Not done |
| Build `code-reviewer` agent with persistent memory | Not done |
| Add `PreToolUse` bash logging hook | Not done |
| Add `$schema` to settings.json | Not done |
| Set `cleanupPeriodDays: 90` | Not done |
| Set `CLAUDE_CODE_SUBAGENT_MODEL: haiku` | Not done |

This is a second prompt. No new gaps have appeared in the last two days. The risk profile is unchanged.

---

## Assumptions

- `claude-code-best-practice` repo was last updated 13 April 2026 (v2.1.101). Claude Code may have shipped additional features between 13 April and 25 April. Assumption: no breaking changes to hooks, agents, or settings since then (confidence ~85%, flagged as below 95%).
- linkedin repo not found at `C:/Users/reonz/cursor/linkedin/`. It may be under a different name or path. The 23 April audit referenced it; this audit scopes only to the four repos listed in the task. LinkedIn-specific gap (Playwright gate) was not re-assessed.
- MCP server list is inferred from claude.ai managed integration. The exact list cannot be verified from the local filesystem. The nine servers listed match prior audit findings.

---

*First draft for human review. All recommendations require Ryo's explicit approval before implementation.*
*Reference: `C:/Users/reonz/cursor/claude-code-best-practice/` (updated Apr 13, 2026, v2.1.101).*
*Produced by Claude Code audit agent, 25 April 2026.*
