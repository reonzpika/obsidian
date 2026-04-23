# Claude Code Audit — 23 April 2026

---

## Setup Summary

### Global Settings (`~/.claude/settings.json`)

- `defaultMode: bypassPermissions` is active globally. All permission checks skipped by default across every repo.
- `effortLevel: high` set globally. Good for deep work; no per-repo override exists.
- Three hooks configured: `PostToolUse` (skill evolver on Skill tool), `Stop` (skill evolver + session update pending), `SessionStart` (session start notify). All run via `C:/Users/reonz/Cursor/skill-evolver/`.
- `claude-hud` status line active. Four plugins enabled: `claude-code-setup`, `claude-md-management`, `frontend-design`, `skill-creator`.
- No `$schema` key in settings.json. No IDE validation of the file.
- `autoUpdatesChannel: latest` — tracking latest releases, appropriate for a power user.
- `skipDangerousModePermissionPrompt: true` — consistent with bypassPermissions default.

### Per-Repo Settings

- No `.claude/settings.json` exists in any repo: clinicpro-saas, clinicpro-medtech, nexwave-rd, linkedin, or obsidian.
- No `.mcp.json` exists in any repo. All MCP servers are configured globally via `.claude.json`.
- The obsidian vault has no `settings.json` in its `.claude/` folder (only skills).

### CLAUDE.md Coverage

- Global `~/.claude/CLAUDE.md`: strong. Covers identity, Plan check protocol, irreversible action gates, date awareness, analytical standards, formatting rules.
- `C:/Users/reonz/cursor/CLAUDE.md`: workspace-level. Directs to obsidian for portfolio, correct.
- `obsidian/CLAUDE.md`: thorough vault schema, workflow rules, gotchas, frontmatter specs.
- `clinicpro-saas/CLAUDE.md`: excellent. Architecture, commands, load-bearing patterns, design system pointer, coding standards.
- `clinicpro-medtech/CLAUDE.md`: solid. Three-tier architecture, PHI rules, env vars, load-bearing constraints.
- `nexwave-rd/CLAUDE.md`: good. MBIE compliance framing, docs structure, sovereignty constraint.
- `linkedin/CLAUDE.md`: comprehensive. WAT framework, session flow, approval gates, safety boundaries.
- Missing: no `~/.claude/CLAUDE.md` separate from `CLAUDE.md`. The global CLAUDE.md is actually at `~/.claude/CLAUDE.md` — confirmed.

### Hooks Configured

- `PostToolUse` on Skill matcher: logs skill usage for the skill-evolver system.
- `Stop`: runs `hook_stop.py` and `hook_session_update_pending.py`.
- `SessionStart`: runs `hook_session_start_notify.py`.
- No hooks for: `PreToolUse`, `PreCompact`, `UserPromptSubmit`, `SubagentStop`, `PermissionRequest`.
- 24 available hook events; 3 are used.

### MCP Servers

- Active via Claude.ai integration: Gmail, Google Calendar, Google Drive, Notion, Vercel, Supabase, Scholar Gateway, Context7, claude-in-chrome.
- These are claude.ai-managed MCP servers, not locally configured in `.mcp.json`.
- No locally configured MCP servers in `.claude.json` or any repo `.mcp.json`.
- Context7 is present (confirms doc-fetching capability). claude-in-chrome is present (confirms browser debugging).

### Skills (Obsidian vault)

- Well-populated: `obsidian`, `daily`, `weekly`, `monthly`, `calendar-sync`, `obsidian-markdown`, `obsidian-cli`, `obsidian-bases`, `json-canvas`, `defuddle`, `obsidian-task-table`, `adopt`.
- Global skills: `session-update`, `board`, `email-triage`, `gmail-draft`, `gws`, `linkedin-post-drafter`, `bff-debug`, `bff-deploy`, `bff-rotate-secret`, `frontend-design`, `skill-creator`, `claude-md-improver`, `session-search`, `handoff`, `evolve`, `evolve-queue`, and many more.

### Memory

- Auto-memory active. Project memory for obsidian vault exists at `~/.claude/projects/C--Users-reonz-cursor-obsidian/memory/` with 17 entries covering feedback, routing rules, reference data. Well-maintained.
- No global agents with persistent `memory:` frontmatter configured.

### Subagents / Agents

- No custom agents defined in `~/.claude/agents/`.
- No custom agents in any repo `.claude/agents/`.
- Agent worktrees are being created (evidenced by worktree artifacts in obsidian's `.claude/worktrees/`).

---

## Gaps — High Priority

### 1. No repo-level `.claude/settings.json` in code repos

**What:** clinicpro-saas, clinicpro-medtech, nexwave-rd, and linkedin have no `.claude/settings.json`. All permission controls are inherited from the global `bypassPermissions` default.

**Why it matters for Ryo:** Each repo has different risk profiles. clinicpro-medtech handles PHI. nexwave-rd is an audit trail for MBIE. linkedin has live Playwright execution that posts to LinkedIn. A misconfigured Claude action in any of these repos has real consequences. Currently there is no repo-level guardrail of any kind.

**What to do:** Create `.claude/settings.json` in each code repo with repo-appropriate permission controls. At minimum, clinicpro-medtech should add a `deny` rule on direct ALEX calls and PHI paths. The nexwave-rd repo should add `deny` on anything that modifies `docs/obj-*/` without explicit task scope.

Example for `C:/Users/reonz/cursor/clinicpro-medtech/.claude/settings.json`:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Bash(curl * alexapi*)",
      "Bash(curl * medtechglobal*)"
    ]
  }
}
```

Example for `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "ask": [
      "Edit(docs/obj-*/output/**)",
      "Write(docs/obj-*/output/**)"
    ]
  }
}
```

**Source:** `best-practice/claude-settings.md` — settings hierarchy; `reports/claude-global-vs-project-settings.md`.

---

### 2. No custom subagents defined anywhere

**What:** `~/.claude/agents/` is empty. No repo has a `.claude/agents/` directory.

**Why it matters for Ryo:** A solo founder across 4+ active repos is the exact use case where specialised agents return the highest ROI. The existing skill library is rich, but skills run inline and share context. Agents run in isolation with their own context window, their own tool restrictions, and can have persistent memory. The best-practice repo shows patterns like a `code-reviewer` agent with `memory: user` that accumulates project-specific patterns across sessions.

Concrete gaps:
- No `research-agent` for R&D literature work (nexwave-rd). Running research inline pollutes the session and bloats context.
- No `medtech-debug` agent restricted to read-only tools for safe ALEX/BFF diagnostics.
- No `code-reviewer` agent with `permissionMode: plan` that cannot write files, only critique.
- No `linkedin-executor` agent to isolate Playwright actions from the main session.

**What to do:** Create `~/.claude/agents/` directory and add at minimum:

`~/.claude/agents/code-reviewer.md`:
```yaml
---
name: code-reviewer
description: Reviews code changes for quality, security, and alignment with repo standards. Use PROACTIVELY when asked to review a PR or diff.
tools: Read, Grep, Glob, WebFetch
model: sonnet
permissionMode: plan
memory: user
---
You are a senior code reviewer. Before reviewing, read your memory for patterns you have encountered before. After reviewing, update your memory with new patterns, recurring issues, or decisions made.
```

**Source:** `best-practice/claude-subagents.md`; `reports/claude-agent-memory.md`.

---

### 3. `bypassPermissions` global default with no repo-level safety net

**What:** `"defaultMode": "bypassPermissions"` in `~/.claude/settings.json` means Claude skips all permission checks in every session across every repo.

**Why it matters for Ryo:** The global CLAUDE.md has an irreversible-action gate enforced by prompt instructions. But `bypassPermissions` means Claude can execute `git push`, `rm -rf`, or a Playwright LinkedIn post without any tool-level confirmation. The gate is instruction-based only. For `bypassPermissions`, the best practice doc notes: "dangerous." The `disableBypassPermissionsMode` setting can prevent this from being activated in sensitive repos.

This is a deliberate choice for speed, but it is currently uncompensated by any repo-level `deny` rules or `ask` escalations for the truly irreversible actions (push, delete, LinkedIn post).

**What to do:** Two options. Option A (preferred): keep `bypassPermissions` globally but add repo-specific `deny` rules for the three highest-risk actions in `linkedin/.claude/settings.json`:
```json
{
  "permissions": {
    "deny": [
      "Bash(python execute_post.py*)",
      "Bash(python scripts/execute*)"
    ]
  }
}
```
Option B: change global `defaultMode` to `acceptEdits` and selectively restore `bypassPermissions` only in obsidian where speed matters most.

**Source:** `best-practice/claude-settings.md` — Permission Modes; `reports/claude-global-vs-project-settings.md`.

---

### 4. No repo-level `.mcp.json` for project-scoped MCP servers

**What:** All MCP servers are globally managed via claude.ai. No repo has a `.mcp.json`.

**Why it matters for Ryo:** Supabase MCP is active globally, meaning it is available (and potentially auto-used) in every session including nexwave-rd, which explicitly forbids commercial-code cross-contamination. Context7 is valuable for clinicpro-saas code sessions but irrelevant in the nexwave-rd docs repo. Playwright MCP would be useful scoped to the linkedin repo only.

**What to do:** Create per-repo `.mcp.json` files to scope server availability. Add `Playwright` MCP to linkedin only. Add `enabledMcpjsonServers` in nexwave-rd's settings to explicitly blocklist Supabase and Notion from that session.

For `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`, add:
```json
{
  "disabledMcpjsonServers": ["supabase", "notion", "vercel"]
}
```

**Source:** `best-practice/claude-mcp.md`.

---

## Gaps — Medium Priority

### 5. No `$schema` in `~/.claude/settings.json`

**What:** The settings file has no `"$schema"` key.

**Why it matters:** The schema at `https://json.schemastore.org/claude-code-settings.json` provides IDE validation and autocomplete. Given the complexity of the settings file (60+ keys, 170+ env vars), a typo in a key silently does nothing. With the schema, miskeys are caught immediately.

**What to do:** Add as the first line of `~/.claude/settings.json`:
```json
"$schema": "https://json.schemastore.org/claude-code-settings.json"
```
Use `/update-config` to make this change.

**Source:** `best-practice/claude-settings.md` — Core Configuration.

---

### 6. No custom agents with `memory: user` for cross-session learning

**What:** The auto-memory system records Claude's learnings per project. But no agents have `memory: user` frontmatter, meaning no agent accumulates domain-specific knowledge across sessions.

**Why it matters for Ryo:** The `session-search` skill can retrieve past session transcripts, which partially compensates. But agent memory is different: it is curated, structured, and injected automatically at agent startup. A `nexwave-research-agent` with `memory: user` could accumulate NZ clinical AI knowledge, competitor tracking, and architecture decisions across every R&D session without manual context loading.

**What to do:** Add `memory: user` to any new agent definitions. Start with a `code-reviewer` agent (see Gap 2) and a `rd-researcher` agent for the nexwave-rd context.

**Source:** `reports/claude-agent-memory.md`.

---

### 7. No `PreToolUse` hook for bash command logging or blocking

**What:** The three configured hooks cover skill evolver tracking and session notifications. No hook monitors what bash commands Claude runs.

**Why it matters for Ryo:** With `bypassPermissions` active, there is no friction on destructive bash commands. A `PreToolUse` hook matched on `Bash` can log every command to a rolling audit file, or block specific patterns (e.g., `git push`, `rm`). This is a zero-cost safety layer.

**What to do:** Add to `~/.claude/settings.json` via `/update-config`:
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
Create `hook_bash_log.py` to append stdin JSON (which contains the bash command) to a dated log file. Two hours of work; ongoing audit trail.

**Source:** `.claude/hooks/HOOKS-README.md` in best-practice repo.

---

### 8. No `global` commands directory (`~/.claude/commands/`)

**What:** `~/.claude/commands/` does not exist. All slash commands are in obsidian's `.claude/skills/` folder (skills, not commands).

**Why it matters for Ryo:** Commands are the right tool for user-initiated orchestration workflows across repos. The best-practice pattern is: command as entry point, agent for autonomous work, skill for reusable procedures. Currently everything is a skill, which means Claude can auto-invoke workflows that should only be explicitly triggered.

Concretely: `board`, `evolve`, `handoff` should probably be commands (explicit user trigger) rather than skills (auto-invocable by Claude). The `evolve` skill is particularly risky as auto-invocable: it modifies skill files.

**What to do:** Review the skill library and convert any skill that should not be auto-invoked to either: (a) a command in `~/.claude/commands/`, or (b) a skill with `disable-model-invocation: true`. At minimum, add `disable-model-invocation: true` to `evolve`, `evolve-queue`, `handoff`, and `board` SKILL.md frontmatter.

**Source:** `reports/claude-agent-command-skill.md`; `best-practice/claude-commands.md`.

---

### 9. No `cleanupPeriodDays` setting for session transcript management

**What:** `cleanupPeriodDays` defaults to 30. With 169+ startups and heavy daily use, the `~/.claude/projects/` directory will accumulate significant transcript volume.

**Why it matters:** The `session-search` skill relies on transcript history. If transcripts are deleted at 30 days, cross-session search loses history. Conversely, unlimited accumulation wastes disk. The `session-search` skill's value is directly proportional to transcript retention.

**What to do:** Set `cleanupPeriodDays: 90` in `~/.claude/settings.json` to extend retention to a quarter. Aligns with MBIE quarterly review cycles.

**Source:** `best-practice/claude-settings.md` — General Settings.

---

### 10. LinkedIn repo skills use `.cursor/skills/` path not `.claude/skills/`

**What:** The `linkedin/CLAUDE.md` references skills at `.cursor/skills/` directory. The standard Claude Code skills path is `.claude/skills/`.

**Why it matters:** If Claude Code is launched from the linkedin repo root, it will look for skills in `.claude/skills/`, not `.cursor/skills/`. The skills may not load correctly.

**What to do:** Verify the actual skill files exist and are being found. If the skills are in `.cursor/skills/`, they may need to be moved or symlinked to `.claude/skills/`. Check with `ls C:/Users/reonz/cursor/linkedin/.cursor/skills/` and `ls C:/Users/reonz/cursor/linkedin/.claude/skills/` to confirm which path is canonical.

**Source:** `best-practice/claude-skills.md` — standard `.claude/skills/` path convention.

---

## Quick Wins (under 30 min each)

**QW1. Add `$schema` to `~/.claude/settings.json`.**
One line. Invoke `/update-config` and add `"$schema": "https://json.schemastore.org/claude-code-settings.json"`. Immediate benefit: IDE catches key typos.

**QW2. Add `disable-model-invocation: true` to `evolve`, `evolve-queue`, `handoff`, and `board` SKILL.md files.**
These are high-consequence skills that should never fire automatically. Edit the frontmatter in each `SKILL.md`. Takes 10 minutes. Eliminates the risk of Claude accidentally triggering skill evolution or session handoff mid-task.
- `C:/Users/reonz/cursor/obsidian/.claude/skills/evolve/SKILL.md`
- `C:/Users/reonz/cursor/obsidian/.claude/skills/evolve-queue/SKILL.md` (if exists)
- And equivalent global skill locations.

**QW3. Create `~/.claude/agents/` directory and add a read-only `code-reviewer` agent.**
20 minutes. Create `C:/Users/reonz/.claude/agents/code-reviewer.md` with `tools: Read, Grep, Glob`, `permissionMode: plan`, `memory: user`. Immediately useful across all repos.

**QW4. Add `"cleanupPeriodDays": 90` to `~/.claude/settings.json`.**
One line via `/update-config`. Extends session-search history from 30 to 90 days. Aligns with quarterly MBIE reporting cadence.

**QW5. Add `deny` rules to `linkedin` repo to gate Playwright execution.**
Create `C:/Users/reonz/cursor/linkedin/.claude/settings.json` with a `deny` rule on `Bash(python execute_post.py*)`. 5 minutes. Prevents accidental live LinkedIn posting.

**QW6. Add `"language": "en-NZ"` to `~/.claude/settings.json`.**
The settings doc supports a `language` key. NZ English is enforced via CLAUDE.md instructions but a settings-level hint reinforces it. One line.

**QW7. Set `CLAUDE_CODE_SUBAGENT_MODEL` to `haiku` in the global `env` block.**
Add to `~/.claude/settings.json`:
```json
"env": {
  "CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
}
```
The `Explore` built-in subagent already uses Haiku; this ensures all lightweight subagent spawning defaults to Haiku rather than Sonnet, saving rate-limit budget for the main session.

---

## Top 3 Recommendations for This Week

### Recommendation 1: Create per-repo `.claude/settings.json` with safety rules

**Files to create:**
- `C:/Users/reonz/cursor/clinicpro-medtech/.claude/settings.json`
- `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`
- `C:/Users/reonz/cursor/linkedin/.claude/settings.json`

**Why first:** The global `bypassPermissions` + no repo-level guardrails is the single biggest risk in the current setup. One misfire in clinicpro-medtech (PHI context), nexwave-rd (MBIE audit trail), or linkedin (live posting) has real-world consequences. This is a two-hour job that removes a class of irreversible-action risk permanently.

**Exact change for linkedin** (most urgent):
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Bash(python execute_post.py*)",
      "Bash(python scripts/assemble_session_state.py*)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(git commit*)"
    ]
  }
}
```

Use `/update-config` for each. Do not edit settings.json directly.

---

### Recommendation 2: Build a `code-reviewer` agent with persistent memory

**File to create:** `C:/Users/reonz/.claude/agents/code-reviewer.md`

**Why second:** This is the highest-ROI agent for a solo founder. A code-reviewer that remembers your stack patterns, recurring issues (Drizzle migration pitfalls, Clerk metadata conventions, Ably strict-mode behaviour), and past decisions accumulates value every session. Right now every review starts cold. The `memory: user` scope means it builds cross-repo knowledge.

**Full content:**
```markdown
---
name: code-reviewer
description: Reviews code changes for correctness, security, and alignment with repo patterns. Use when asked to review changes, check a diff, or audit a PR. Run PROACTIVELY when the user says "review this" or "check these changes".
tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*)
model: sonnet
permissionMode: plan
memory: user
---

You are a senior code reviewer for a GP-founder's startup stack (Next.js, Clerk, Neon/Supabase Postgres, Drizzle, Ably, Stripe, Playwright).

Before starting any review:
1. Read your memory for patterns, conventions, and recurring issues you have seen before.
2. Check the repo's CLAUDE.md for load-bearing patterns you must not break.

During review, flag:
- PHI handling (never plaintext, always HMAC/hashed)
- Drizzle migration patterns (hand-rolled only, never drizzle-kit push)
- Webhook routes that must stay public
- Clerk metadata mutations vs DB writes
- Ably strict-mode double-connection risk
- em dashes in any generated text (must never appear)

After review:
1. Update your memory with new patterns, decisions made, or recurring issues.
2. Summarise findings in a numbered list with severity (blocker / warning / suggestion).
```

---

### Recommendation 3: Add a `PreToolUse` bash logging hook

**Why third:** With `bypassPermissions` active and no repo-level `deny` rules yet in place, this is the fastest interim safety layer. A bash audit log costs nothing at runtime (async), provides a full command history for debugging, and can be extended later to block specific patterns.

**Exact settings.json addition** (via `/update-config`):
```json
"hooks": {
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
}
```

Create `C:/Users/reonz/Cursor/skill-evolver/hook_bash_log.py`:
```python
import json, sys, datetime, pathlib

data = json.load(sys.stdin)
log_dir = pathlib.Path.home() / ".claude" / "bash-audit"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"{datetime.date.today()}.jsonl"
with open(log_file, "a", encoding="utf-8") as f:
    json.dump({
        "ts": datetime.datetime.now().isoformat(),
        "cwd": data.get("cwd"),
        "cmd": data.get("tool_input", {}).get("command"),
        "session": data.get("session_id")
    }, f)
    f.write("\n")
```

This produces a daily JSONL audit file at `~/.claude/bash-audit/YYYY-MM-DD.jsonl`. Searchable. Cross-sessions. Zero performance impact.

---

*Produced by Claude Code audit agent — 23 April 2026.*
*Reference: `C:/Users/reonz/cursor/claude-code-best-practice/` (updated Apr 13, 2026, v2.1.101).*
