# The complete Claude Code power-user reference

Claude Code has evolved from a terminal-based coding assistant into a full agent orchestration platform with **skills, hooks, multi-agent teams, MCP integrations, and worktree-based parallelism**. This reference covers every major capability a solo technical founder needs to maximize productivity with a Next.js / TypeScript / Tailwind / Vercel / Supabase stack. It synthesizes official Anthropic documentation, community tooling as of April 2026, and the ETH Zürich research on context file effectiveness. Start with the minimum viable setup at the end, then expand into advanced patterns as your workflow demands.

---

## Start here: minimum viable vs full advanced setup

**Minimum viable power setup** (30 minutes):
1. Install Claude Code: `curl -fsSL https://claude.ai/install.sh | bash`
2. Run `/init` in your project root to scaffold a CLAUDE.md, then **manually rewrite it** using the "would removing this cause a mistake?" test (Section 2)
3. Install three essential MCP servers: Context7 (live docs), GitHub MCP, Playwright MCP
4. Learn three keyboard shortcuts: **Shift+Tab** (cycle permission modes), **Esc+Esc** (rewind checkpoints), **Option+P** (model picker)
5. Run `/powerup` for 18 interactive lessons on core features

**Full advanced setup** (add incrementally):
- Path-scoped rules in `.claude/rules/` for frontend, API, and database conventions
- PostToolUse hooks for auto-formatting and type-checking
- Supabase MCP (read-only), Vercel MCP, Figma MCP, Sentry MCP
- Install `frontend-design` skill from anthropics/skills and `react-best-practices` from vercel-labs/agent-skills
- Configure Agent Teams with worktree isolation for parallel feature development
- SessionStart hook injecting git branch context
- Happy Coder for mobile session control

---

## 1. Context window mechanics and core commands

### How context actually works

Claude Code operates within a **200K token context window** for Opus 4.6, Sonnet 4.6, and Haiku 4.5. Teams with Max, Team, or Enterprise plans unlock **1M token context** on Opus 4.6. The system reserves a **~33K token buffer** (previously 45K) for the compaction summarization process itself, leaving roughly 167K usable tokens in the standard window.

Auto-compact triggers at **~83.5% context utilization** (~167K of 200K). Override this threshold with `export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=90` (value 1–100). The output token reservation defaults to 32K tokens (`CLAUDE_CODE_MAX_OUTPUT_TOKENS`), which shares the same window — setting it very high reduces usable context. When compaction fires, Claude analyzes the conversation for key information, creates a concise summary of interactions and decisions, replaces old messages with the summary, and continues seamlessly.

Run `/context` at any time for a **visual grid** showing exact token allocation: system prompt, tools, memory files, skills, and conversation history. This is essential for diagnosing context pressure from too many MCP tools or bloated CLAUDE.md files.

### Complete slash command reference

Claude Code ships **60+ slash commands** including 50+ built-in plus bundled skills. Type `/` and filter by typing.

**Context management:**

| Command | Purpose | When to use |
|---------|---------|-------------|
| `/context` | Visual context usage grid | Check token budget before large tasks |
| `/compact [instructions]` | Compress with optional focus | `/compact keep the migration plan, drop the debugging` |
| `/clear` | Full context wipe | Starting fresh task in same session |
| `/memory` | Edit CLAUDE.md; toggle auto-memory | Adjusting project instructions |

**Session management:**

| Command | Purpose |
|---------|---------|
| `/resume` | Interactive session picker (P=preview, R=rename, B=browse forks) |
| `/rename [name]` | Name session: `/rename auth-refactor` |
| `/branch` or `/fork` | Parallel conversation copy — both paths stay alive |
| `/rewind` (or Esc+Esc) | Checkpoint menu: restore code+conversation, conversation only, code only, or "Summarize from here" |
| `/export` | Save session to file |

**Development tools:**

| Command | Purpose |
|---------|---------|
| `/btw` | Quick question in overlay — **never enters conversation history** (preserves context) |
| `/diff` | Show diff of changes |
| `/cost` | Cost breakdown by model and cache hit rate |
| `/init` | Generate starter CLAUDE.md from project structure |
| `/hooks` | Read-only hook viewer |
| `/mcp` | Manage MCP server connections |
| `/voice` | Push-to-talk dictation mode |
| `/status` | Version and connectivity (works while Claude responds) |
| `/stats` | Usage patterns, favorite models, streaks |
| `/install-github-app` | Set up automatic PR reviews |

**Bundled skills (can spawn parallel agents):**

| Command | Purpose |
|---------|---------|
| `/batch` | Run commands across files via parallel worktree agents |
| `/loop` | Recurring prompts on a schedule (up to 3 days locally) |
| `/simplify` | Refactor for reuse and efficiency |
| `/debug` | Debugging assistance |

**Essential keyboard shortcuts:**

| Shortcut | Action |
|----------|--------|
| **Shift+Tab** | Cycle: Normal → Auto-Accept → Plan Mode |
| **Esc+Esc** | Open /rewind checkpoint menu |
| **Option+P** (Alt+P) | Model picker |
| **Option+T** (Alt+T) | Toggle extended thinking |
| **Ctrl+G** | Open external editor (edit plans inline) |
| **Ctrl+B** | Background current agent |
| **Ctrl+O** | Toggle verbose mode (shows thinking + hook output) |
| **Ctrl+Z** | Suspend to terminal; `fg` to resume |

### Plan Mode mechanics

**Activate** via Shift+Tab twice, `/plan` command, or `claude --permission-mode plan`. In Plan Mode, Claude has access to **read-only tools** (Read, LS, Glob, Grep, WebSearch, WebFetch, Task for spawning research subagents, TodoRead/TodoWrite) plus **AskUserQuestion** for structured multiple-choice requirements gathering. All write tools (Edit, Write, Bash, MCP mutations) are blocked.

The recommended flow: enter Plan Mode → Claude reads codebase and asks clarifying questions → generates structured plan → review/edit plan with **Ctrl+G** → switch out of Plan Mode → Claude executes step-by-step. Most multi-file refactors benefit from **2–3 plan revisions**, toggling back into Plan Mode when drift occurs.

**opusplan mode** (`/model opusplan`) uses **Opus 4.6 for planning** and auto-switches to **Sonnet 4.6 for implementation** — the best cost-quality tradeoff for complex work.

### Headless and non-interactive mode

```bash
claude -p "Your prompt here"                    # Basic one-shot
claude -p "Analyze code" --output-format json   # Structured JSON output
claude -p "Review" --output-format stream-json  # Streaming JSON events
claude -p "Fix bugs" --allowedTools "Read,Edit,Bash"  # Scoped tools
claude -p "Task" --max-turns 3                  # Limit execution steps
claude -p "Task" --max-budget-usd 5.00          # Hard cost ceiling
```

The `--bare` flag (recommended for CI) skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. JSON schema enforcement: `claude -p "Extract functions" --output-format json --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}'`. Pipe input naturally: `git diff HEAD~5 | claude -p "Review changes"`.

### Checkpointing and session recovery

**Every file edit creates a checkpoint** — Claude snapshots file contents before any modification. Access via **Esc+Esc** or `/rewind`. Four restore options: restore code + conversation, conversation only, code only, or **"Summarize from here"** (preserves everything before the selected point perfectly, compresses trial-and-error after it). Checkpoints persist across sessions but only track Claude's file edits — not external processes, bash commands, or database operations.

### The /powerup tutorial system

Shipped in **v2.1.90 (April 1, 2026)**, `/powerup` provides **18 interactive lessons** with animated demos rendered via React + Ink. Three difficulty tiers: **Beginner** (context management, CLAUDE.md, plan mode, model selection), **Intermediate** (skills, hooks, sub-agent orchestration, MCP config, checkpointing), **Advanced** (worktrees, parallel sessions, auto mode, permission management, headless mode, SDK). Progress is gamified and persistent. Companion feature: `/insights` generates a personalized HTML usage report at `~/.claude/usage-data/report.html`.

### Auto-memory system

Claude Code maintains two memory systems. **CLAUDE.md** contains instructions you write. **Auto Memory (MEMORY.md)** contains notes Claude writes itself — build commands, debugging insights, architecture decisions, code style preferences, workflow habits.

Auto Memory stores files at `~/.claude/projects/<project-hash>/memory/` with a `MEMORY.md` index (first **200 lines or 25KB** loaded at startup) plus topic files (debugging.md, patterns.md) loaded on demand. The system is on by default; toggle via `/memory` or disable with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` for CI. **Auto Dream** periodically consolidates scattered memory files through a four-phase process: inventory → search transcripts → consolidate → update index.

The earlier `#` prefix shortcut for saving preferences is now deprecated in favor of direct CLAUDE.md editing and auto-memory.

### Model selection guide

| Model | Pricing (input/output per 1M) | Context | Use for |
|-------|-----|---------|---------|
| **Sonnet 4.6** | $3 / $15 | 200K (1M available) | **Daily driver** — 90%+ of tasks. Preferred by 59% of developers over Opus 4.5 |
| **Opus 4.6** | $5 / $25 | 200K (1M on Max/Team/Enterprise) | Deep reasoning, architecture, complex debugging, multi-file refactors |
| **Haiku 4.5** | $0.80 / $4 | 200K | Fast/cheap: classification, simple edits, batch tasks |
| **opusplan** | Mixed | — | Opus for planning, Sonnet for implementation — best cost-quality balance |

Switch in-session: `/model sonnet`, `/model opus`, `/model haiku`, `/model opusplan`. At startup: `claude --model opus`. Permanent default: `ANTHROPIC_MODEL` env var. Effort levels: `/effort low|medium|high|max` (max is Opus-only). **Rule of thumb**: default to Sonnet 4.6; escalate to Opus for multi-file architecture, race conditions, or 10+ file refactors; use Haiku for batch and routine operations.

---

## 2. CLAUDE.md mastery

### The full hierarchy

Claude Code reads CLAUDE.md files by walking up the directory tree. All discovered files are **concatenated into context** (not replaced). Resolution order from broadest to most specific:

| Priority | Location | Shared? |
|----------|----------|---------|
| 1 (Lowest) | `~/.claude/CLAUDE.md` | Just you, all projects |
| 2 | `~/.claude/rules/*.md` | Just you, all projects |
| 3 | **Managed policy** (macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`) | All org users, **cannot be excluded** |
| 4 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via VCS |
| 5 | `.claude/rules/*.md` (unconditional) | Team via VCS |
| 5b | `.claude/rules/*.md` with `paths:` frontmatter | Team, loaded on file-pattern match |
| 6 | Subdirectory `CLAUDE.md` files | Loaded on demand when Claude reads files there |
| 7 (Highest) | `./CLAUDE.local.md` | Just you (gitignored) |

Key behaviors: managed policy **cannot** be excluded by any setting. `./CLAUDE.md` takes precedence over `./.claude/CLAUDE.md` if both exist. Subdirectory files load on demand. `@import` syntax (`@path/to/file`) expands inline with max 5 hops recursion. HTML comments are stripped from context. Use `claudeMdExcludes` (glob patterns) to skip irrelevant ancestor files in monorepos.

### Path-scoped rules with frontmatter

Rules in `.claude/rules/` can be scoped to specific file patterns:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation with Zod
- Return consistent error shapes: { error: string, code: number }
```

Rules **without** `paths:` load unconditionally at launch. Rules **with** `paths:` load **on demand** when Claude reads files matching the glob. Always quote glob patterns in YAML (patterns starting with `{` or `*` are reserved YAML indicators). **Known bugs** as of early 2026: GitHub issues #17204, #16299, #16853 report YAML parsing issues and rules loading globally regardless of frontmatter. Verify behavior with `/memory`.

### The "would removing this cause a mistake?" test

The **ETH Zürich study** (arXiv:2602.11988, February 2026 — Gloaguen et al.) tested AI-generated context files across 138 tasks on 12 Python repos. Key findings: **LLM-generated context files reduced task success by ~3%** in 5 of 8 settings **while increasing costs 20–23%**. Codebase overviews and directory listings provided zero navigation improvement. The only exception: in documentation-poor repos, context files improved performance by 2.7%.

The practical takeaway is ruthless: **include only what Claude cannot infer from the code itself**. Apply the test: "If I removed this line, would Claude make a mistake?" High-signal content includes build/test commands (`pnpm build`, `pnpm --filter web dev`), non-obvious tooling (`uv` instead of `pip` — the study showed **160x usage increase** when mentioned), architectural constraints, naming conventions, and ALWAYS/NEVER rules. Low-signal content to cut: directory listings, generic coding standards, comprehensive API docs available elsewhere, anything redundant with README.md.

Target **50–200 lines** per CLAUDE.md file. Place critical rules early (mitigates "lost in the middle" phenomenon). Review periodically to remove contradictions.

### CLAUDE.md for a Next.js / Supabase stack

```markdown
# Project: [Name]
Next.js 15+ / App Router / TypeScript strict / Tailwind CSS / Supabase

## Commands
- `pnpm install` from root
- `pnpm dev` — Next.js dev server (port 3000)
- `pnpm build` — production build
- `pnpm test` — run Vitest
- `supabase migration new <name>` — create migration
- `supabase gen types typescript --project-id <ref> > src/types/database.ts`

## Architecture
- App Router EXCLUSIVELY. NEVER use Pages Router, getServerSideProps, getStaticProps.
- Server Components by default. 'use client' ONLY for useState, useEffect, event handlers.
- Server Actions for mutations. NO API routes for internal data.
- Fetch data in Server Components with async/await.
- Zod for runtime validation at API boundaries.
- TypeScript strict — NEVER use `any`. Use `unknown` for truly unknown types.
- Tailwind utility classes only, no custom CSS files.
- All secrets from environment variables. NEVER hardcode credentials.

## Supabase Conventions
- All schema changes via migration files in supabase/migrations/
- Database types generated from schema at src/types/database.ts
- RLS policies required on all tables
- Edge Functions in supabase/functions/
```

### Anti-patterns that waste tokens or cause drift

Stuffing everything into one file instead of splitting into `.claude/rules/`. Using `/init`-generated context files without manual editing (–3% success rate). Including directory listings (agents navigate on their own). Vague instructions like "keep code clean" instead of "use ESLint with Airbnb config." Accumulating contradictory rules across hierarchy levels without periodic audits. Rules bloating past 200 lines, which degrades adherence quality.

### How CLAUDE.md interacts with skills

CLAUDE.md instructions are **advisory** — Claude reads them and tries to follow them but exercises judgment. The system prompt explicitly notes content "may or may not be relevant." For mandatory enforcement, use **hooks** (Section 3). Skills and CLAUDE.md serve different roles: rules are always-active behavioral constraints ("nouns" — where things are, what standards apply), while skills are on-demand task-specific workflows ("verbs" — how to do things). Rules load every session; skills load only when invoked. For task-specific instructions, prefer skills over CLAUDE.md to save context.

---

## 3. The hooks system

### All hook lifecycle events

Claude Code provides **21+ hook lifecycle events** with four handler types. Hooks are configured in `.claude/settings.json` (project-wide, committable), `.claude/settings.local.json` (project-local, gitignored), or `~/.claude/settings.json` (user-wide).

| Event | Trigger | Can block? (exit 2) |
|-------|---------|---------------------|
| **SessionStart** | Session begins/resumes/clear/compact | No |
| **UserPromptSubmit** | User submits prompt | Yes (blocks and erases) |
| **PreToolUse** | Before tool executes | **Yes** (blocks tool call) |
| **PermissionRequest** | Permission dialog appears | Yes (denies permission) |
| **PostToolUse** | After tool succeeds | No (stderr shown to Claude) |
| **PostToolUseFailure** | After tool fails | No |
| **Notification** | Permission/idle/auth events | No |
| **SubagentStart** | Subagent spawned | No |
| **SubagentStop** | Subagent finishes | Yes (prevents stop) |
| **TaskCreated** | Task created via TaskCreate | Yes (rolls back) |
| **TaskCompleted** | Task marked complete | Yes (prevents completion) |
| **Stop** | Claude finishes responding | **Yes** (forces continuation) |
| **TeammateIdle** | Agent team teammate going idle | Yes |
| **WorktreeCreate** | Worktree being created | Yes (failure = creation fails) |
| **WorktreeRemove** | Worktree being removed | No |
| **PreCompact/PostCompact** | Before/after compaction | No |
| **FileChanged** | Watched file changes on disk | No |
| **ConfigChange** | Config file changes | Yes |
| **SessionEnd** | Session terminates | No |

### Four hook handler types

**Command hooks** (`type: "command"`): Execute shell scripts. Receive JSON via stdin. Exit code 0 = proceed, **exit code 2 = block**, other = non-blocking error. Environment variables available: `$CLAUDE_PROJECT_DIR`, `$CLAUDE_TOOL_INPUT_FILE_PATH`, `$CLAUDE_ENV_FILE`.

**HTTP hooks** (`type: "http"`): POST JSON to an endpoint. Non-2xx responses = non-blocking error. To block, return 2xx with `{"decision": "block"}`. Support `allowedEnvVars` for secure header injection.

**Prompt hooks** (`type: "prompt"`): Send context to a Claude model for single-turn evaluation. Use `$ARGUMENTS` placeholder for hook input JSON. Returns yes/no decision.

**Agent hooks** (`type: "agent"`): Spawn a subagent with tools (Read, Grep, Glob) for deep multi-step verification before returning a decision.

### Practical hook recipes

**Auto-format and lint on every file write:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [
        { "type": "command", "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\"" },
        { "type": "command", "command": "npx eslint --fix \"$CLAUDE_TOOL_INPUT_FILE_PATH\"" }
      ]
    }]
  }
}
```

**Git branch context on session start:**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '{\"additionalContext\": \"Branch: '$(git branch --show-current)'\"}'"
      }]
    }]
  }
}
```

**Block dangerous commands:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|DROP TABLE' && exit 2 || exit 0"
      }]
    }]
  }
}
```

**Protect .env files from reads:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write|Read",
      "hooks": [{
        "type": "command",
        "command": "if [[ \"$CLAUDE_FILE_PATHS\" == *\".env\"* ]]; then echo 'Blocked .env access' && exit 2; fi"
      }]
    }]
  }
}
```

**Stop hook — keep Claude working until tests pass:**
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "./scripts/check-tests.sh"
      }]
    }]
  }
}
```
If tests fail → exit 2 → Claude continues working. If tests pass → exit 0 → Claude stops.

### Security considerations

Hooks run with **full environment access** in the current directory. PreToolUse hooks firing exit 2 have absolute blocking power. No runtime hot-reload — edits to hooks don't take effect until next session. Hook output capped at **10,000 characters** injected into context. Enterprise admins can set `allowManagedHooksOnly` to block all non-admin hooks. Test hooks with `Ctrl+O` (verbose mode shows stdout/stderr) and the `/hooks` read-only browser.

---

## 4. Multi-agent architecture

### Subagents vs Agent Teams vs manual multi-instance

**Subagents** are specialized assistants spawned via the `Task` tool, each running in its own context window with a custom system prompt. Built-in types: **Explore** (fast, read-only, uses Haiku), **Plan** (inherits main model), and general-purpose. Each receives only the parent's prompt string and returns a final message — intermediate work stays isolated. Subagents **cannot spawn other subagents** (no infinite nesting). Define custom subagents in `.claude/agents/`:

```yaml
---
name: test-runner
description: Run tests and fix failures. Use PROACTIVELY.
tools: Bash, Read, Grep
model: sonnet
maxTurns: 20
isolation: worktree
---
You are a test automation expert...
```

**Agent Teams** (experimental, v2.1.32+) provide true multi-agent coordination. Enable with `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. The **lead** orchestrates; **teammates** are independent Claude Code instances with their own 1M-token context windows. Communication uses a **shared task list** (file-based with dependency chains, states: pending → in_progress → completed → blocked) and a **mailbox system** (peer-to-peer JSON messages on disk). Tools: `TeamCreate`, `TaskCreate`, `SendMessage`. Display in-process (Shift+Down to cycle) or split-pane via tmux.

**When NOT to use multi-agent (the 95% rule)**: Shipyard's analysis found multi-agent workflows don't make sense for **95% of agent-assisted development tasks**. Avoid when: single-feature work (one session suffices), sequential tasks with heavy dependencies, agents would touch the same files, cost matters (each teammate = separate instance), or session resumption reliability is needed.

### Git worktrees for parallel isolation

Native support since v2.1.50:

```bash
claude --worktree feature-auth    # Creates .claude/worktrees/feature-auth/
claude -w bugfix-api              # Short form
```

Each worktree gets its own branch (`worktree-<name>`), session, and filesystem state. Subagent frontmatter supports `isolation: "worktree"` for per-agent isolation. Auto-cleanup: no changes → worktree + branch removed automatically; changes exist → prompt to keep/remove. Practical limit: **3–5 parallel worktrees** per machine. Add `.claude/worktrees/` to `.gitignore`.

### The C compiler case study

Nicholas Carlini (Anthropic Safeguards team) used **16 Claude Opus 4.6 instances** working in parallel to build a **~100,000-line Rust-based C compiler** in ~2 weeks for **~$20,000** in API costs across ~2,000 sessions. The compiler achieves **99% pass rate** on the GCC torture test suite and successfully compiles Linux 6.9 on x86, ARM, and RISC-V, plus QEMU, FFmpeg, SQLite, PostgreSQL, Redis, and Doom. Coordination used task locking via text files in `current_tasks/` with git synchronization forcing sequential claiming, plus Docker containers for isolation with no internet access. Key lesson: when all 16 agents hit the same Linux kernel bug, human architectural intervention (binary search using GCC as oracle) was required.

### Orchestration tools

| Tool | Install | Key concept | Best for |
|------|---------|-------------|----------|
| **Gas Town** (Steve Yegge) | `npm install -g @gastown/gt` | Mayor/Rigs/Crew/Beads — git worktree-based persistent storage | Solo devs running 20–30 parallel agents |
| **Multiclaude** (Dan Lorenc) | `go install github.com/dlorenc/multiclaude/cmd/multiclaude@latest` | "Brownian ratchet" — CI tests pass, PRs merge | Team usage, give prompt and walk away |
| **Ruflo** v3.5 (rUv) | `npx ruflo@latest init` | 60+ pre-built agents, self-learning swarms, WASM policy engine | Multi-model routing, cost optimization |
| **Happy Coder** | `npm install -g happy-coder` | Mobile control of Claude Code instances, E2E encrypted | Remote session management from phone |
| **sudocode** | `npm install -g sudocode && sudocode init` | Git repo as distributed context database, 4-tier abstraction | Agent memory and task tracking |

---

## 5. The skills ecosystem

### Skill architecture

Skills are filesystem-based, reusable instruction packages giving Claude domain expertise. Structure:

```
skill-name/
├── SKILL.md           # Instructions + YAML frontmatter
├── references/        # Reference docs (loaded on demand)
├── scripts/           # Executable scripts (output enters context)
└── assets/            # Templates, data files
```

Three-level progressive disclosure: **Level 1** (startup) loads only YAML frontmatter (~100 tokens); **Level 2** (on invoke) loads full SKILL.md body; **Level 3** (as needed) loads references and scripts. Install at user level (`~/.claude/skills/`) or project level (`.claude/skills/`).

Key frontmatter fields: `name` (becomes /slash-command), `description` (**250-char cap** for trigger matching — front-load keywords), `context: fork|inline` (subagent or inline), `disable-model-invocation: true` (user-only, essential for deploys), `user-invocable: false` (model-only background knowledge), `model`, `effort`, `paths`.

**Auto-activation reality check**: Community reports indicate skills don't reliably auto-trigger (20–50% baseline). Workaround: UserPromptSubmit hooks injecting explicit activation instructions (84% with forced eval pattern).

### Official Anthropic skills (anthropics/skills — ⭐ 111K)

18 skills including: **frontend-design** (277K+ installs, anti-"AI slop" aesthetics), **skill-creator** (create/validate/package skills with eval framework), **webapp-testing**, **pdf/docx/pptx/xlsx** (document generation), **algorithmic-art**, **brand-guidelines**, **mcp-builder**, **web-artifacts-builder**, **claude-api**.

```bash
/plugin marketplace add anthropics/skills
npx skills add anthropics/skills --skill frontend-design
```

### Official Vercel skills (vercel-labs/agent-skills — ⭐ 19.5K)

**react-best-practices** (69 rules across 8 categories, 185K+ installs), **web-design-guidelines** (100+ accessibility/performance/UX rules), **composition-patterns** (compound components, state lifting, React 19 APIs), **react-native**, **view-transitions**, **vercel-deploy**, **ai-sdk**, **commerce**, **workflows**.

```bash
npx skills add vercel-labs/agent-skills --skill react-best-practices
```

### Community skills highlights

| Source | Skills | Install |
|--------|--------|---------|
| **Bencium marketplace** (13 skills) | controlled-ux-designer (WCAG 2.1 AA), innovative-ux-designer, typography, design-audit, architecture | `/plugin marketplace add bencium/bencium-marketplace` |
| **Design motion principles** (kylezantos) | Motion audit trained on Emil Kowalski, Jakub Krehel, Jhey Tompkins | `cp -r skills/design-motion-principles ~/.claude/skills/` |
| **ShadcnBlocks** (masonjames) | 2,500+ shadcn/ui blocks and components knowledge | Copy to `~/.claude/skills/` |
| **AccessLint** (accesslint/claude-marketplace) | contrast-checker, refactor, use-of-color, link-purpose | `/plugin marketplace add accesslint/claude-marketplace` |
| **Google Stitch** (google-labs-code/stitch-skills) | stitch-design, stitch-loop, design-md, react:components | `npx skills add google-labs-code/stitch-skills --skill stitch-design --global` |
| **obra/superpowers** | 20+ battle-tested skills: /brainstorm, /write-plan, /execute-plan, TDD | Community marketplace |
| **alirezarezvani/claude-skills** | 248 production-ready skills across engineering, marketing, compliance | GitHub |

---

## 6. MCP servers with install commands

### Configuration

```bash
# Add a server (CLI)
claude mcp add <name> -- npx -y @package/server
claude mcp add --transport http <name> <url>         # Remote HTTP
claude mcp add <name> -e API_KEY=value -- npx -y @pkg  # With env vars
claude mcp add --scope user <name> -- npx -y @pkg    # User-wide

# Manage
claude mcp list          # List all
claude mcp remove <name> # Remove
/mcp                     # In-session: check status, authenticate
```

Project-scoped config (`.mcp.json` in project root, version-controlled):
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/server"],
      "env": { "API_KEY": "value" }
    }
  }
}
```

**Tool Search** auto-activates when tool definitions exceed 10% of context window, reducing ~72K tokens to ~8.7K (85% reduction). Limit to **3–5 servers** — each adds 500–1,000 tokens per tool.

### Essential servers for the Next.js / Supabase stack

**Context7** (Upstash, Official) — Live versioned documentation. **Single biggest improvement to AI coding accuracy** by eliminating stale docs.
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```
Supports Next.js, Tailwind, Supabase. Add "use context7" to prompts to trigger. Free tier available.

**GitHub MCP** (Official GitHub, ⭐ 28.3K) — 51 tools across repos, issues, PRs, actions, code security.
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```
Rate limit: 5,000 req/hour. Use fine-grained PATs scoped to specific repos.

**Playwright MCP** (Official Microsoft, ⭐ ~30K) — Browser automation via accessibility snapshots.
```bash
claude mcp add playwright -- npx @playwright/mcp@latest
# Headed mode: npx @playwright/mcp@latest --headed
```
Replaces deprecated Puppeteer MCP. Requires Node.js 18+.

**Supabase MCP** (Official Supabase) — Database, auth, edge functions, migrations, type generation.
```bash
claude mcp add --transport http supabase https://mcp.supabase.com/mcp
# RECOMMENDED: Scoped + read-only
# https://mcp.supabase.com/mcp?project_ref=<ref>&read_only=true
```
**Always use `read_only=true` by default** — prompt injection risk from data in tables.

**Vercel MCP** (Official Vercel) — Deploy, logs, env vars, domains, project management.
```bash
claude mcp add --transport http vercel https://mcp.vercel.com
# Project-specific: https://mcp.vercel.com/my-team/my-project
```

**Figma MCP** (Official Figma, Feb 2026) — Design to code (React + Tailwind default), code to canvas (beta).
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```
Free plan limited to 6 tool calls/month. Dev/Full seat on Pro/Org/Enterprise needed.

**shadcn MCP** (Official shadcn/ui) — Browse, search, install components from registries.
```json
{ "mcpServers": { "shadcn": { "command": "npx", "args": ["-y", "@shadcn/mcp@latest"] } } }
```

**Sentry MCP** (Official Sentry) — Stack traces, breadcrumbs, Seer AI root cause analysis.
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

**Task Master** (Community, ⭐ 15.5K) — Parse PRDs into structured, dependency-aware task plans.
```bash
claude mcp add task-master-ai --scope user -- npx -y task-master-ai@latest
# Core mode (~70% token reduction): -e TASK_MASTER_TOOLS="core"
```

**Notion MCP** (Official Notion):
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**PostHog MCP** (Official PostHog) — Analytics, feature flags, experiments, error tracking.
```bash
claude mcp add --transport http posthog https://mcp.posthog.com/sse
```

**Firecrawl MCP** (Official Firecrawl) — Web scraping with JS rendering, clean Markdown output.
```bash
claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/your-api-key/v2/mcp
```

**Storybook MCP** (Official Storybook 10.3+) — Component metadata, stories, self-healing tests, a11y checks.
```bash
npx storybook@latest add @storybook/addon-mcp
# Server at http://localhost:6006/mcp when Storybook running
```

### MCP registries

| Registry | URL | Notes |
|----------|-----|-------|
| **Smithery** | smithery.ai | One-click install, managed configs |
| **Glama** | glama.ai/mcp/servers | Most comprehensive, daily updates |
| **PulseMCP** | pulsemcp.com | Curated with server.json files |
| **mcpmarket.com** | mcpmarket.com | Top 100 leaderboard by GitHub stars |
| **Official MCP Registry** | registry.modelcontextprotocol.io | Community-driven, replacing README lists |
| **mcp.so** (Warp) | mcp.so | Server listings with configs |

### MCP security

**66% of scanned MCP servers had security findings** in audit; 30+ CVEs in Jan–Feb 2026. Real-world incidents include the GitHub MCP prompt injection (May 2025), "NeighborJack" servers bound to 0.0.0.0 without auth (June 2025), and **24,008 secrets found in MCP config files** on public GitHub (GitGuardian 2026). Best practices: validate all inputs server-side, use OAuth 2.1 with PKCE, short-lived tokens, least privilege scoping, sandbox tool executions, audit before installing, pin versions, and treat agents as first-class identities.

---

## 7. Essential GitHub repositories

### Official repositories

| Repository | Stars | Description |
|------------|-------|-------------|
| **anthropics/claude-code** | ~109K | Official Claude Code. Includes plugins directory (code-review, hookify, frontend-design), claude-code-action for GitHub Actions. Install: `curl -fsSL https://claude.ai/install.sh \| bash` |
| **anthropics/skills** | ~111K | Official skills (18 skills). Apache 2.0 license. `npx skills add anthropics/skills --skill frontend-design` |
| **vercel-labs/agent-skills** | ~19.5K | Vercel's official skills. react-best-practices (185K+ installs), web-design-guidelines, composition-patterns |
| **modelcontextprotocol/servers** | ~82K | Official MCP reference servers (filesystem, postgres, git, memory, sequential-thinking). Being deprecated in favor of registry |

### Community essentials

| Repository | Stars | Value proposition |
|------------|-------|-------------------|
| **hesreallyhim/awesome-claude-code** | ~35.9K | Definitive curated list. Skills, hooks, slash commands, orchestrators, applications, CLAUDE.md templates. Companion: awesomeclaude.ai |
| **affaan-m/everything-claude-code** | ~128K | 30 agents, 136 skills, 60 commands, hooks. By Anthropic hackathon winner |
| **FlorianBruniaux/claude-code-ultimate-guide** | Active | 24K+ lines of docs, 228 production templates (9 agents, 26 slash commands, 31 hooks, 14 skills), 271 quiz questions, security threat intelligence (24 CVEs tracked). MCP server: `npx -y claude-code-ultimate-guide-mcp` |
| **alirezarezvani/claude-skills** | ~5.2K | 248 production-ready skills across engineering, marketing, compliance, C-level |
| **bencium/bencium-marketplace** | ~126 | 13 design/architecture/productivity skills. Controlled + innovative UX designers |
| **bencium/bencium-claude-code-design-skill** | ~126 | 28,000+ char UX design skill with ACCESSIBILITY.md, RESPONSIVE-DESIGN.md, MOTION-SPEC.md |
| **accesslint/claude-marketplace** | ~8 | MIT. 4 a11y skills + MCP server for WCAG contrast checking |
| **kylezantos/design-motion-principles** | Small | Motion audit trained on 3 designers (Emil Kowalski, Jakub Krehel, Jhey Tompkins) |
| **masonjames/Shadcnblocks-Skill** | Small | 2,500+ shadcn/ui blocks knowledge for intelligent UI composition |
| **SpillwaveSolutions/parallel-worktrees** | Small | Parallel subagent development using git worktrees with `.agent-status/` monitoring |
| **wilwaldon/Claude-Code-Frontend-Design-Toolkit** | Small | Curated collection for better-looking frontends. 240+ styles, 127 font pairings, design token generators |
| **google-labs-code/stitch-skills** | Official 3P | 7 Google Stitch skills: stitch-design, stitch-loop, design-md, react:components |
| **obra/superpowers** | Active | 20+ battle-tested skills including TDD, debugging, /brainstorm, /write-plan |
| **github.com/eyaltoledano/claude-task-master** | ~15.5K | Task Master. PRD to structured tasks. 36 MCP tools |
| **github.com/ruvnet/ruflo** | ~16.6K | Ruflo orchestration framework. 60+ pre-built agents |

---

## 8. Advanced workflow patterns

### The spec-first interview pattern

The highest-impact workflow pattern, **officially recommended by Anthropic**. Start with a minimal prompt plus AskUserQuestion-driven interview:

```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.
Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask
obvious questions, dig into the hard parts I might not have considered. Keep interviewing
until we've covered everything, then write a complete spec to SPEC.md.
```

Claude asks 40+ structured multiple-choice questions. After SPEC.md is written, **start a fresh session** to execute — clean context prevents accumulated confusion. The spec becomes the single source of truth. Research shows **85% fewer security vulnerabilities** and **300% better maintainability** vs ad-hoc prompting. ★★★★★ Official Anthropic.

### The Ralph technique

An autonomous loop where Claude iterates until task completion. Named after Ralph Wiggum (The Simpsons). Now an official Anthropic plugin:

```bash
/plugin install ralph-loop@claude-plugins-official
/ralph-loop:ralph-loop "Build auth system" --completion-promise "DONE" --max-iterations 10
```

How it works: Claude works → tries to exit → Stop hook blocks exit → same prompt fed back → repeat until completion promise matched or max iterations hit. Real-world results: 6 repos generated overnight at a YC hackathon; $50K contract completed for $297 in API costs. Best for well-defined tasks with clear success criteria or TDD loops. ★★★★☆ Official Plugin.

### RIPER workflow

**Research → Innovate → Plan → Execute → Review.** A structured 5-phase workflow using custom slash commands with 3 consolidated agents and a branch-aware memory bank (`.claude/memory-bank/`). Each phase uses minimum necessary capabilities (read-only for research). Source: github.com/tony/claude-code-riper-5. ★★★☆☆ Community.

### The "benchy" parallel pattern

Run N parallel Claude implementations in separate worktrees, compare results:

```bash
git worktree add ../impl-sonnet -b experiment/sonnet main
git worktree add ../impl-opus -b experiment/opus main
cd ../impl-sonnet && claude --model sonnet -p "Implement auth using SPEC.md"
cd ../impl-opus && claude --model opus -p "Implement auth using SPEC.md"
# Compare, merge winner
```

### Dispatch, Channels, and remote control

Three mechanisms for controlling Claude Code remotely:

| Mechanism | Purpose | Setup |
|-----------|---------|-------|
| **Dispatch** | Submit tasks programmatically, no persistent connection | CI/CD, event-driven automation |
| **Channels** | Persistent bidirectional (Telegram, Discord) | `claude --channels plugin:telegram@claude-plugins-official` |
| **Remote Control** | Full lifecycle control of live session | `claude --remote-control` |

Channels enable **permission relay** — when Claude hits a permission prompt, it relays to your phone for remote approval (v2.1.81+). ★★★★☆ Official Anthropic (Channels in research preview).

### TDD enforcement via hooks

Hook-based approach: PreToolUse wraps `Bash(git commit)` — checks for `/tmp/agent-pre-commit-pass` file. Test script only creates pass file if all tests green. Hook blocks commit if file missing → forces Claude into "test-and-fix" loop. Combine with Ralph technique for autonomous TDD:

```
/ralph-loop:ralph-loop "Implement [FEATURE] using TDD. Write failing test → implement
minimal code → run tests → fix if failing → refactor. Output <promise>DONE</promise>
when all tests green." --max-iterations 50
```

---

## 9. Productivity tools and integrations

**Happy Coder** (free, MIT, github.com/slopus/happy): Mobile/web client for Claude Code. `npm install -g happy-coder` → run `happy` instead of `claude`. iOS/Android/Web apps. E2E encrypted (TweetNaCl, zero-knowledge). QR code pairing. Control multiple instances, push notifications, voice coding, MCP tool approval from phone.

**Claude Code Review** (Official Anthropic): Two mechanisms — (1) `claude-code-action` GitHub Action responds to @claude mentions in PRs/issues, (2) built-in `/code-review` plugin launches 4–5 parallel Sonnet agents for compliance, bug detection, and PR history analysis. Confidence-based scoring filters false positives (threshold ≥80).

**Task Master** (⭐ 15.5K, github.com/eyaltoledano/claude-task-master): PRD → structured tasks. Set `TASK_MASTER_TOOLS=core` for 70% token reduction. Supports claude-code as model provider (routes through your subscription — no extra API costs).

**Buoy** (buoy.design): Design system drift detection. Core drift detection is 100% deterministic — no LLMs, no API keys, no data leaves your machine. Watches PRs for hardcoded colors, token violations, rogue components. `buoy drift check` runs locally.

**Boris Cherny's tips** (creator of Claude Code, howborisusesclaudecode.com — 72 tips): His workflow runs **10–15 concurrent sessions** (5 terminal, 5–10 browser, plus mobile). Key insights: starts in Plan Mode, iterates until good, then auto-accept. Uses worktrees as the "single biggest productivity unlock." `/batch` for large-scale refactors via 5–30 parallel worktree agents. Auto-dream consolidates memory between sessions.

### Performance pitfalls to avoid

Loading too many MCP tool descriptions reduces the 200K window to ~70K usable tokens. Use `/compact` when context exceeds 70%. Skipping Plan Mode leads to 40+ unwanted file changes — always spec before execution. Single-session bottleneck: use worktrees instead of subagents in the same context. Claude Code-assisted commits leak secrets at **3.2% rate** vs 1.5% baseline (GitGuardian 2026) — always review diffs before committing. Missing a verification loop (browser tests, type checks) — Boris Cherny says giving Claude a way to verify its work improves quality **2–3x**.

---

## 10. Next.js / TypeScript / Vercel / Supabase specifics

### Next.js App Router with Claude Code

Next.js ships bundled docs in `node_modules/next/dist/docs/` and generates `AGENTS.md` files. Import into CLAUDE.md with `@import` syntax. **Critical CLAUDE.md rules** for App Router: explicitly state "App Router EXCLUSIVELY, NEVER Pages Router" — without this, Claude frequently mixes patterns. Specify "Server Components by default, 'use client' ONLY for useState, useEffect, event handlers." Lock data fetching: "async/await in Server Components, Server Actions for mutations, NO API routes for internal data." Specify `next/image` for images, `next/link` for navigation.

**Component decision tree for CLAUDE.md:**
```
Needs useState/useEffect/event handlers/browser APIs → Client Component ('use client')
Direct data fetching, no interactivity → Server Component (default)
Both → Split: Server parent + Client child
```

### Database migration workflow

With Supabase MCP + branching (paid plans): create dev branch → test migrations → merge to production. Migration rules for CLAUDE.md: all schema changes via `supabase migration new <name>`, never modify production directly, generate types after migration with `supabase gen types typescript --project-id <ref> > src/types/database.ts`. Claude can directly run SQL queries and generate migrations through MCP tools — but **always use `read_only=true` for production**.

### Environment variable security

**Critical finding**: Claude Code **automatically loads .env files** into runtime memory without explicit permission. Deny .env reads in settings:

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"]
  }
}
```

Even with deny rules, once `npm test` or `npm run dev` executes, secrets resolved into the shell environment become visible via `process.env`. Use dedicated test credentials and container isolation for defense-in-depth. Use a centralized `src/config/env.ts` pattern with `requireEnv()` validation.

### Type safety enforcement

Effective CLAUDE.md rules: TypeScript strict mode, NEVER `any` (use `unknown`), explicit return types on all functions, interfaces over type aliases for object shapes, discriminated unions over optional properties, Zod for runtime validation at API boundaries, generated Supabase `Database` type from `src/types/database.ts`.

### Edge runtime rules for CLAUDE.md

```markdown
## Edge Runtime (Vercel)
- Edge does NOT support Node.js APIs (fs, path, full crypto)
- Web Standard APIs only (fetch, Request, Response, URL, crypto.subtle)
- No dynamic imports or eval()
- Max execution: 30 seconds
- Database: HTTP-based clients only (Supabase JS client), NOT connection pooling
- Mark with: export const runtime = 'edge'
```

---

## 11. Security and governance

### Permission modes

| Mode | Auto-approved | Activate |
|------|--------------|----------|
| **default** | File reads only | Default |
| **acceptEdits** | Reads + edits | Shift+Tab |
| **plan** | Reads only (NO edits) | Shift+Tab or `--permission-mode plan` |
| **auto** | All actions with background safety classifier | Requires Team/Enterprise + Sonnet/Opus 4.6 |
| **dontAsk** | Only pre-approved tools | `--permission-mode dontAsk` |
| **bypassPermissions** | Everything | `--dangerously-skip-permissions` — **isolated containers only** |

**Auto mode** runs a background classifier (Sonnet 4.6) evaluating each action before execution. Blocks destructive commands, deploy-with-skip-verification, and exfiltration attempts. 3 consecutive denials or 20 total → escalation to human. **bypassPermissions** auto-approves ALL operations — subagents **inherit** full bypass (cannot override). Hooks still fire even in bypass mode.

### Known CVEs and injection risks

**CVE-2025-59536 (CVSS 8.7)**: Code injection via malicious hooks in `.claude/settings.json` from untrusted repos. Fixed in v1.0.111. **CVE-2026-21852 (CVSS 5.3)**: Malicious repo sets `ANTHROPIC_BASE_URL` to attacker endpoint, exfiltrating API keys. Fixed in v2.0.65. **Source code leak (March 31, 2026)**: 512,000-line TypeScript source leaked via npm sourcemap in v2.1.88. **Always inspect `.claude/` and `.vscode/` directories** before opening cloned repos. CLAUDE.md instructions survive compaction and get treated as user directives — a persistent injection surface.

### Sandboxing options

**Official Anthropic devcontainer** (anthropics/claude-code/.devcontainer): Pre-configured firewall (default-deny, allows npm/GitHub/Claude API), non-root user. Enables safe `--dangerously-skip-permissions`. **Trail of Bits devcontainer** (trailofbits/claude-code-devcontainer): Built for security audits. `devc .` launches, read-only mounts via `devc mount ~/secrets /secrets --readonly`. **Docker isolation**:

```bash
docker run -it \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd):/workspace:ro \
  --network=none \
  claude-sandbox -p "Analyze codebase"
```

### Audit trails

Local transcripts stored in `~/.claude/projects/`. Hook-based logging via PreToolUse matcher `"*"` writing to `/var/log/claude-audit.log`. Enterprise: Compliance API with real-time programmatic access, OpenTelemetry export (`OTEL_METRICS_EXPORTER`, `OTEL_EXPORTER_OTLP_ENDPOINT`), and SIEM integration (Grafana/Datadog/Splunk).

### Recommended minimum security posture

1. Always run latest Claude Code version
2. Deny .env reads in project `settings.json`
3. Use devcontainer for any `--dangerously-skip-permissions` usage
4. Audit `.claude/` directories in cloned repos before opening
5. Use PreToolUse hooks for governance enforcement
6. Scope MCP servers to specific projects with `read_only` where possible
7. Route API traffic through gateway (LiteLLM/Portkey) for cost control and audit
8. Budget limits: `claude --max-budget-usd 5.00` for automated tasks

---

## Conclusion: what changes when you actually use all of this

The highest-leverage patterns aren't the most complex ones. **Three changes deliver 80% of the productivity gain**: writing a tight, manually-authored CLAUDE.md with the "would-removing-this-cause-a-mistake" filter (avoids the 3% accuracy penalty and 20% cost increase from auto-generated context); using **Plan Mode → spec → fresh session** for every non-trivial feature (85% fewer security vulnerabilities); and running **PostToolUse hooks** for auto-formatting and type-checking (eliminates the review-fix-review loop that dominates session time).

The multi-agent patterns — Agent Teams, worktrees, orchestration tools — are powerful but serve the 5% of tasks where parallel work isolation matters. The C compiler case study proves they work at scale, but most solo founders will get more from disciplined single-session workflows with MCP servers providing live docs (Context7) and stack integration (Supabase, Vercel, GitHub).

The security surface is real and growing. Three CVEs in 14 months, secrets leaking at 2x the baseline rate, and .env files loaded without consent mean that **hooks aren't optional — they're the enforcement layer** that turns advisory CLAUDE.md rules into hard gates. The minimum viable security setup (deny .env reads, scope MCP servers, devcontainer for automation) costs 15 minutes and prevents the most common catastrophic failures.