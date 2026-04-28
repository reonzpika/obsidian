---
title: Claude Code setup audit
created: 2026-04-25
type: audit
---

## Executive summary

- All recommendations from the 23 April audit remain unimplemented as of this audit.
- The single highest-risk item is unchanged: `defaultMode: bypassPermissions` globally with zero repo-level `deny` rules. clinicpro-medtech (PHI, ALEX FHIR), nexwave-rd (MBIE audit trail), and clinicpro-saas (live Stripe billing) can all fire irreversible bash commands without a tool-level gate.
- No custom agents (`~/.claude/agents/` does not exist). Every session starts cold with no accumulated cross-session domain knowledge for any repo.
- No `PreToolUse` bash audit hook. With bypassPermissions active and no logging, there is no post-hoc record of what commands ran.
- CLAUDE.md quality is strong across all five repos. The weak point is not instructions but harness-enforced safety and no subagents.
- New finding vs 23 April: miozuki-web has a `.claude/rules/` directory with path-scoped UI rules, a pattern not used in any other repo. Worth replicating.
- New finding vs 23 April: `evolve`, `board`, and `handoff` skills lack `disable-model-invocation: true`, meaning the model can auto-trigger them mid-task.

---

## Current config snapshot

### Global settings (`~/.claude/settings.json`)

| Key | Value | Notes |
|-----|-------|-------|
| `$schema` | MISSING | No IDE validation of 60+ key file |
| `defaultMode` | `bypassPermissions` | Skips all permission checks globally |
| `skipDangerousModePermissionPrompt` | `true` | Consistent with bypassPermissions |
| `model` | `sonnet` | Correct default |
| `effortLevel` | `high` | Good for complex work |
| `autoUpdatesChannel` | `latest` | Appropriate for power user |
| `CLAUDE_CODE_FORK_SUBAGENT` | `1` (env block) | Subagents fork to isolated context |
| `CLAUDE_CODE_SUBAGENT_MODEL` | MISSING from env | Subagents default to Sonnet, not Haiku |
| `cleanupPeriodDays` | MISSING (default 30) | Transcripts purged at 30 days |
| `language` | MISSING | NZ English only in CLAUDE.md, not harness-enforced |
| `alwaysThinkingEnabled` | MISSING | Extended thinking requires explicit opt-in per session |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | MISSING | Best-practice repo uses 80; not set here |
| Status line | claude-hud plugin | Active |
| Attribution | MISSING | Co-Authored-By still at default |
| Plugins | claude-code-setup, claude-md-management, frontend-design, skill-creator, claude-hud | superpowers disabled |

### Hooks (`~/.claude/settings.json`)

| Event | Matcher | Script | Purpose |
|-------|---------|--------|---------|
| `PostToolUse` | Skill | `skill-evolver/hook_skill.py` | Logs skill invocations for /evolve |
| `Stop` | (all) | `skill-evolver/hook_stop.py` | Records transcript path for /evolve |
| `Stop` | (all) | `skill-evolver/hook_session_update_pending.py` | Queues sessions needing /session-update |
| `SessionStart` | (all) | `skill-evolver/hook_session_start_notify.py` | Alerts on pending session-update count |

**Missing:** `PreToolUse` (bash audit, git push gate, em dash scan), `PreCompact`, `UserPromptSubmit`, `SubagentStop`, `PermissionRequest`, `PostToolUse` auto-format. 4 of 25+ hook events in use.

No `~/.claude/hooks/` directory exists. No hooks are scripts separate from skill-evolver.

### Per-repo `.claude/settings.json`

| Repo | Has `.claude/` | Has `settings.json` | Notes |
|------|---------------|---------------------|-------|
| `clinicpro-saas` | No | No | No guardrails; live Stripe billing repo |
| `clinicpro-medtech` | No | No | PHI context, highest risk |
| `nexwave-rd` | No | No | MBIE audit trail, second-highest risk |
| `obsidian` | Yes | No | Only `settings.local.json` (spinner + additionalDirs) |
| `miozuki-web` | Yes (rules/ only) | No | No settings.json, but has path-scoped rules |

### Per-repo CLAUDE.md

| Repo | Has CLAUDE.md | Quality | Notes |
|------|---------------|---------|-------|
| `~/.claude/CLAUDE.md` | Yes | Strong | Identity, plan check, irreversible action gates, formatting rules |
| `cursor/CLAUDE.md` | Yes | Adequate | Workspace pointer to obsidian, minimal |
| `obsidian/CLAUDE.md` | Yes | Excellent | Vault schema, workflow rules, frontmatter specs, gotchas |
| `clinicpro-saas/CLAUDE.md` | Yes | Excellent | Stack, commands, load-bearing patterns, coding standards, design system pointer |
| `clinicpro-medtech/CLAUDE.md` | Yes | Solid | Three-tier arch, PHI rules, env vars, hard constraints |
| `nexwave-rd/CLAUDE.md` | Yes | Good | MBIE compliance framing, docs structure, sovereignty constraint |
| `miozuki-web/CLAUDE.md` | Yes | Good | Plan check baked in, irreversible action gate |

Line count concern: clinicpro-saas CLAUDE.md is 183 lines, clinicpro-medtech is 180 lines. Best-practice recommendation is under 200 lines per file. Both are near the limit. Worth watching.

### Custom agents (`~/.claude/agents/`)

Directory does not exist. Zero custom agents defined at any level (global, project, or repo).

### Skills

**Global (`~/.claude/commands/`):** 26 skills including `board`, `evolve`, `evolve-queue`, `email-triage`, `gmail-draft`, `gws`, `handoff`, `session-search`, `skill-creator`, `claude-md-improver`, `run-agents`, `agent-batch`, `deep-research`, `bug-audit`.

**Global (`~/.claude/skills/`):** 9 skills including `bff-debug`, `bff-deploy`, `bff-rotate-secret`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `ui-ux-pro-max`, `session-update`, `session-review`.

**Obsidian project (`obsidian/.claude/skills/`):** 14 skills including `daily`, `weekly`, `monthly`, `obsidian`, `obsidian-markdown`, `vault-audit`, `calendar-sync`, `json-canvas`, `obsidian-bases`.

**Notable gaps:**
- No `gp-fellowship` skill (clinical training workflow)
- No `mbie-claim` skill (quarterly MBIE cost report generation)
- No `deploy-check` skill for pre-deploy validation in clinicpro-saas or medtech
- `evolve`, `board`, `handoff`: likely missing `disable-model-invocation: true`

### MCP servers

All configured via claude.ai managed integration. No `.mcp.json` in any repo or global `~/.claude/` dir.

Active globally: Gmail, Google Calendar, Google Drive, Notion, Vercel, Supabase, Scholar Gateway, Context7, claude-in-chrome.

**Risk:** Supabase MCP (clinicpro-medtech production DB), Notion MCP, and Vercel MCP are active in every session, including nexwave-rd and obsidian. No repo-level scoping. A distracted agent in an R&D session has write access to production infrastructure.

### Memory

Auto-memory active. Project memory for obsidian vault (`~/.claude/projects/C--Users-reonz-cursor-obsidian/memory/`): 20 entries, well-maintained. Covers feedback patterns, routing rules, references.

Project memory directories exist for: obsidian, clinicpro-saas, clinicpro-medtech (created by auto-memory). No seeded MEMORY.md in clinicpro-saas or clinicpro-medtech.

No agents with `memory: user` frontmatter exist anywhere. Global rules dir (`~/.claude/rules/`) does not exist.

---

## Gap table

| # | Gap | Impact (1-5) | Ease (1-5) | Score | Priority |
|---|-----|-------------|------------|-------|----------|
| 1 | No repo-level `deny` rules in clinicpro-medtech (PHI + ALEX FHIR) | 5 | 4 | 20 | Critical |
| 2 | No `PreToolUse` bash audit hook (no command log with bypassPermissions active) | 4 | 4 | 16 | Critical |
| 3 | No repo-level `deny` in nexwave-rd (MBIE audit trail artefacts unprotected) | 4 | 4 | 16 | High |
| 4 | No custom agents at all (`~/.claude/agents/` missing) | 5 | 3 | 15 | High |
| 5 | Supabase, Vercel, Notion MCP active globally across all repos | 4 | 3 | 12 | High |
| 6 | `CLAUDE_CODE_SUBAGENT_MODEL=haiku` not set in env | 3 | 5 | 15 | Medium |
| 7 | `cleanupPeriodDays` missing (30-day default vs 90-day MBIE quarters) | 3 | 5 | 15 | Medium |
| 8 | No `$schema` in global settings.json | 2 | 5 | 10 | Medium |
| 9 | No `PreCompact` hook to preserve task state on compaction | 3 | 3 | 9 | Medium |
| 10 | `evolve`, `board`, `handoff` missing `disable-model-invocation: true` | 3 | 4 | 12 | Medium |
| 11 | No seeded MEMORY.md for clinicpro-saas or clinicpro-medtech | 3 | 3 | 9 | Medium |
| 12 | No `code-reviewer` agent with persistent cross-session memory | 4 | 3 | 12 | Medium |
| 13 | No `.claude/rules/` at global level (path-scoped rules not in use globally) | 2 | 3 | 6 | Low |
| 14 | `language` not set in settings.json | 1 | 5 | 5 | Low |
| 15 | No `gp-fellowship` or `mbie-claim` skills | 2 | 2 | 4 | Low |

---

## Top 10 improvements

### 1. Add `deny` rules to clinicpro-medtech

**Why:** This repo handles PHI. ALEX FHIR calls must go through the Lightsail BFF. A Claude session must never directly curl the ALEX API or touch patient data paths outside the defined patterns.

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

### 2. Add `PreToolUse` bash audit hook

**Why:** With bypassPermissions active globally, there is no tool-level gate on any bash command. A JSONL audit log per day is the minimum viable safety net and adds zero perceptible latency (async).

**Steps:**
1. Create `C:/Users/reonz/cursor/skill-evolver/hook_bash_log.py`:

```python
import json, sys, datetime, pathlib

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if data.get("tool_name") != "Bash":
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

2. Run `/update-config` to add to global `PreToolUse` hooks:

```json
{
  "matcher": "Bash",
  "hooks": [{"type": "command", "command": "python C:/Users/reonz/Cursor/skill-evolver/hook_bash_log.py", "async": true, "timeout": 3000}]
}
```

---

### 3. Add `deny` rules to nexwave-rd

**Why:** nexwave-rd is an MBIE audit trail repo. Research reports in `docs/obj-*/output/` are evidence artefacts. Accidental modification without explicit intent could compromise the audit trail.

**Steps:** Create `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "ask": [
      "Edit(docs/obj-*/output/**)",
      "Write(docs/obj-*/output/**)",
      "Bash(git push*)"
    ],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

---

### 4. Create `code-reviewer` agent in `~/.claude/agents/`

**Why:** A solo founder with 4 active repos needs a code reviewer that accumulates domain knowledge across sessions (Drizzle pitfalls, Clerk metadata conventions, Ably strict mode, HMAC PHI handling). Agent `memory: user` makes this permanent.

**Steps:**
1. `mkdir C:/Users/reonz/.claude/agents/`
2. Create `C:/Users/reonz/.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code changes for correctness, security, and alignment with repo patterns. Use PROACTIVELY when asked to review changes, check a diff, or audit a PR.
tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*), Bash(git status*)
model: sonnet
permissionMode: plan
memory: user
---

You are a senior code reviewer for a GP-founder's startup stack (Next.js 16, Clerk, Neon/Supabase Postgres, Drizzle ORM, Ably, Stripe, FHIR, Lightsail BFF).

Before reviewing: read your memory for patterns and recurring issues. Check the repo's CLAUDE.md for load-bearing constraints.

Flag without fail: PHI handling (never plaintext), Drizzle migrations (hand-rolled only, never drizzle-kit push or migrate), public webhook routes missing auth bypass, Clerk metadata mutations, Ably strict-mode risk, em dashes in any generated text, MBIE audit artefacts being modified without explicit instruction.

After review: update memory with new patterns found. Output findings as a numbered list with severity (blocker / warning / suggestion).
```

---

### 5. Scope MCP servers per-repo (Supabase, Vercel, Notion)

**Why:** Supabase MCP (production DB), Vercel MCP, and Notion MCP being active in a nexwave-rd R&D session or an obsidian planning session is unnecessary risk. A distracted agent could mutate production data.

**Steps:** Until per-repo `.mcp.json` scoping is fully documented, use `disabledMcpjsonServers` in project settings:

For nexwave-rd `.claude/settings.json`, add:
```json
"disabledMcpjsonServers": ["supabase", "mcp__supabase", "mcp__claude_ai_Vercel"]
```

Longer-term: create project-specific `.mcp.json` in clinicpro-saas and clinicpro-medtech with only the servers each project needs, rather than relying on the global set.

---

### 6. Set `CLAUDE_CODE_SUBAGENT_MODEL=haiku` + `cleanupPeriodDays: 90` + `$schema`

**Why:** Three one-line wins addressable in a single `/update-config` call.
- `CLAUDE_CODE_SUBAGENT_MODEL=haiku`: lightweight subagents (file search, parallel reads) run on Haiku, preserving Sonnet rate-limit budget for the main session.
- `cleanupPeriodDays: 90`: extends session-search history from 30 days to a full quarter, aligning with MBIE quarterly reporting.
- `$schema`: IDE validates 60+ key settings.json; catches typos silently otherwise.

**Steps:** Run `/update-config`:

```json
"$schema": "https://json.schemastore.org/claude-code-settings.json",
"cleanupPeriodDays": 90,
"env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" }
```

---

### 7. Create `rd-researcher` agent for nexwave-rd

**Why:** Research sessions for Obj-1 pull in literature, architecture candidates, and competitor analysis. Running inline pollutes the main session context with intermediate tool calls. An isolated agent with `model: opus` and read-only tools keeps main context focused.

**Steps:** Create `C:/Users/reonz/.claude/agents/rd-researcher.md`:

```markdown
---
name: rd-researcher
description: Deep research for NexWave Health R&D. Use when tasked with literature search, competitor analysis, architecture evaluation, or MBIE compliance research.
tools: Read, Grep, Glob, WebFetch, WebSearch
model: opus
permissionMode: plan
memory: user
---

You are an R&D researcher for NexWave Health (MBIE grant CONT-109091-N2RD-NSIWKC), building clinical AI for NZ primary care. Sovereignty constraint: identifiable NZ clinical data must stay in NZ (AWS Auckland ap-southeast-6, or Catalyst Cloud NZ).

Before researching: read your memory for prior findings on this topic. After researching: update memory with key findings, sources, and conclusions. Output a structured report suitable for filing in docs/obj-N/research/.
```

---

### 8. Add `PreCompact` hook

**Why:** Auto-compaction at ~95% context discards intermediate state. A `PreCompact` prompt hook tells Claude what to preserve before the summary is written, reducing the "lost my place" problem on long sessions.

**Steps:** Run `/update-config`:

```json
"PreCompact": [
  {
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Before compacting, preserve: (1) the current task objective and any incomplete sub-steps, (2) all file paths opened or modified this session, (3) decisions or constraints established this session, (4) any errors encountered and how they were resolved."
      }
    ]
  }
]
```

---

### 9. Add `disable-model-invocation: true` to `evolve`, `board`, `handoff`

**Why:** These three skills make significant, potentially irreversible changes (modifying skill files, opening strategy sessions). The model should never auto-trigger them mid-task.

**Steps:** Add `disable-model-invocation: true` to the frontmatter of:

- `C:/Users/reonz/.claude/commands/evolve/SKILL.md`
- `C:/Users/reonz/.claude/commands/evolve-queue/SKILL.md`
- `C:/Users/reonz/.claude/commands/board/SKILL.md`
- `C:/Users/reonz/.claude/commands/handoff/SKILL.md`

---

### 10. Seed MEMORY.md for clinicpro-saas and clinicpro-medtech

**Why:** Auto-memory exists for both repos but is unstructured. A seeded MEMORY.md gives auto-memory a starting structure and ensures key load-bearing patterns survive session boundaries.

**Steps:**
1. Create `~/.claude/projects/C--Users-reonz-Cursor-clinicpro-saas/memory/MEMORY.md` with entries for: Drizzle hand-rolled migration rule, Clerk metadata as feature-flag store, `reactStrictMode: false` in dev reason, Stripe webhook public route requirement, `transcription_chunks` IDENTITY sequence protection.
2. Create `~/.claude/projects/C--Users-reonz-Cursor-clinicpro-medtech/memory/MEMORY.md` with: three-tier request flow (Vercel to Lightsail BFF to ALEX), static IP constraint, HMAC-SHA256 PHI rule, Azure AD token 55-min cache, never import Clerk in this repo.

---

## Quick wins (under 15 min each)

| # | Action | Time | How |
|---|--------|------|-----|
| QW1 | Add `$schema`, `cleanupPeriodDays: 90`, `CLAUDE_CODE_SUBAGENT_MODEL: haiku` | 3 min | `/update-config` |
| QW2 | Create `~/.claude/agents/` directory | 1 min | mkdir |
| QW3 | Add `disable-model-invocation: true` to evolve + board + handoff | 5 min | Edit SKILL.md frontmatter |
| QW4 | Create `hook_bash_log.py` (30-line script) | 10 min | Write file + `/update-config` |
| QW5 | Create `nexwave-rd/.claude/settings.json` with output dir protection | 5 min | Write file |

QW1 + QW2 + QW3 combined: under 10 minutes. Start there.

---

## Delta since 23 April 2026 audit

Zero recommendations from the 23 April audit have been implemented. The risk profile is unchanged.

| Prior recommendation | Status |
|---------------------|--------|
| Create per-repo `.claude/settings.json` with deny rules | Not done |
| Build `code-reviewer` agent with persistent memory | Not done |
| Add `PreToolUse` bash logging hook | Not done |
| Add `$schema` to global settings.json | Not done |
| Set `cleanupPeriodDays: 90` | Not done |
| Set `CLAUDE_CODE_SUBAGENT_MODEL: haiku` | Not done |

New gaps found in this audit (not in 23 April audit):
- `evolve`, `board`, `handoff` missing `disable-model-invocation: true`
- Supabase/Vercel/Notion MCP active globally including in nexwave-rd and obsidian sessions
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (best-practice: 80) not set
- miozuki-web `.claude/rules/` pattern not replicated to other repos

---

## Assumptions

- `claude-code-best-practice` repo last updated 13 April 2026 (v2.1.101). Claude Code may have shipped features between that date and 25 April 2026. Assumption: no breaking changes to hooks, agents, or settings in that window. Confidence approximately 85%.
- MCP server list inferred from claude.ai managed integration visible in the system prompt. Cannot be verified from local filesystem. The list (Gmail, Google Calendar, Google Drive, Notion, Vercel, Supabase, Scholar Gateway, Context7, claude-in-chrome) matches prior audit findings.
- `disabledMcpjsonServers` key is assumed to support the server name strings shown. If the key does not exist in the current version, per-repo `.mcp.json` is the alternative. Verify before implementing gap 5.
- The `linkedin` repo referenced in the 23 April audit was not found at `C:/Users/reonz/cursor/linkedin/`. It may be archived, renamed, or parked. Not assessed here.

---

*First draft for human review. All recommendations require Ryo's explicit approval before implementation.*
*Reference: `C:/Users/reonz/cursor/claude-code-best-practice/` (v2.1.101, updated 13 April 2026).*
*Audit produced by Claude Code agent, 25 April 2026.*
