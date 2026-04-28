# Claude Code settings.json changes — apply via /update-config

Generated from: claude-code-audit-2026-04-23.md
Date: 2026-04-23

These changes cannot be applied by direct file edit. Use `/update-config` for each item.

---

## Checklist

### 1. Add $schema key (Audit: Gap 5, QW1)

Add as the first key in `~/.claude/settings.json`:

```json
"$schema": "https://json.schemastore.org/claude-code-settings.json"
```

Benefit: IDE catches key typos immediately. The settings file has 60+ keys; silent miskeys are a real risk.

- [ ] Applied via /update-config

---

### 2. Add cleanupPeriodDays: 90 (Audit: Gap 9, QW4)

Add to `~/.claude/settings.json`:

```json
"cleanupPeriodDays": 90
```

Benefit: Extends session-search history from the 30-day default to a full quarter. Aligns with MBIE quarterly review cycles. session-search value is directly proportional to transcript retention.

- [ ] Applied via /update-config

---

### 3. Add CLAUDE_CODE_SUBAGENT_MODEL: haiku to env block (Audit: QW7)

Add to the `env` block in `~/.claude/settings.json`:

```json
"env": {
  "CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
}
```

If an `env` block already exists, add the key inside it rather than creating a second block.

Benefit: All lightweight subagent spawning defaults to Haiku rather than Sonnet, preserving rate-limit budget for the main session.

- [ ] Applied via /update-config

---

### 4. Add PreToolUse bash logging hook (Audit: Gap 7, Recommendation 3)

Prerequisite: `hook_bash_log.py` must exist at `C:/Users/reonz/Cursor/skill-evolver/hook_bash_log.py`.
See file content below. Create it first, then apply this hook.

**hook_bash_log.py content:**
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

Add to the `hooks` block in `~/.claude/settings.json` (merge with the existing hooks object that already has PostToolUse, Stop, SessionStart):

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

Benefit: Every bash command Claude runs is appended to a daily JSONL audit file at `~/.claude/bash-audit/YYYY-MM-DD.jsonl`. Zero performance impact (async). Interim safety layer while bypassPermissions is active globally.

- [ ] Created hook_bash_log.py at the path above
- [ ] Applied via /update-config

---

### 5. Verify language: en-NZ is a valid settings key (Audit: QW6)

The audit notes `language: en-NZ` as a possible settings key. Before applying, confirm it is valid for the current Claude Code version. Do not add unvalidated keys.

Check: run `/update-config` and inspect autocomplete suggestions, or check `https://json.schemastore.org/claude-code-settings.json` for a `language` property.

If confirmed valid:
```json
"language": "en-NZ"
```

If not in the schema, skip. NZ English is already enforced via CLAUDE.md instructions at every layer.

- [ ] Confirmed valid (or skipped if not in schema)
- [ ] Applied via /update-config (if valid)

---

## Tasks requiring writes outside the vault (apply manually)

These were blocked during audit implementation because write permissions are scoped to the obsidian vault. Apply each one in a separate Claude Code session rooted in the correct directory.

### Task 1: Create code-reviewer agent

File: `C:/Users/reonz/.claude/agents/code-reviewer.md`

Create the `~/.claude/agents/` directory if it does not exist, then write:

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

- [ ] Directory created
- [ ] File written

---

### Task 2: Create bash audit logging hook script

File: `C:/Users/reonz/Cursor/skill-evolver/hook_bash_log.py`

Content is the Python script in Task 4 above (hook_bash_log.py content section).

- [ ] File written

---

### Task 3A: linkedin repo settings

File: `C:/Users/reonz/cursor/linkedin/.claude/settings.json`

Create `C:/Users/reonz/cursor/linkedin/.claude/` directory if it does not exist. The directory already has a `skills/` subfolder, so `.claude/` itself exists. Write:

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

- [ ] File written

---

### Task 3B: clinicpro-medtech repo settings

File: `C:/Users/reonz/cursor/clinicpro-medtech/.claude/settings.json`

Create the `.claude/` directory if it does not exist. Write:

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

- [ ] Directory created
- [ ] File written

---

### Task 3C: nexwave-rd repo settings

File: `C:/Users/reonz/cursor/nexwave-rd/.claude/settings.json`

Create the `.claude/` directory if it does not exist. Write:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "ask": [
      "Edit(docs/obj-*/output/**)",
      "Write(docs/obj-*/output/**)"
    ]
  },
  "disabledMcpjsonServers": ["supabase", "notion", "vercel"]
}
```

- [ ] Directory created
- [ ] File written

---

### Task 4: Add disable-model-invocation to high-consequence skills

For each file below, add `disable-model-invocation: true` to the YAML frontmatter. Edit frontmatter only.

**evolve** — `C:/Users/reonz/.claude/commands/evolve/SKILL.md`

Current frontmatter:
```yaml
---
name: evolve
description: End-of-session skill reviewer...
---
```

Add after `name:` line:
```yaml
disable-model-invocation: true
```

**evolve-queue** — `C:/Users/reonz/.claude/commands/evolve-queue/SKILL.md`

Same pattern. Add `disable-model-invocation: true` after `name:` line.

**handoff** — `C:/Users/reonz/.claude/commands/handoff/SKILL.md`

Current frontmatter already has `user-invocable: true`, `argument-hint:`, `allowed-tools:`. Add `disable-model-invocation: true` after `name:` line.

**board** — `C:/Users/reonz/.claude/commands/board/SKILL.md`

Current frontmatter has `user-invocable: true`, `argument-hint:`, `allowed-tools: []`. Add `disable-model-invocation: true` after `name:` line.

- [ ] evolve updated
- [ ] evolve-queue updated
- [ ] handoff updated
- [ ] board updated

---

## Reference

Audit source: `context/tools/claude-code-audit-2026-04-23.md`
Best-practice repo: `C:/Users/reonz/cursor/claude-code-best-practice/`
