---
id: linkedin-agent
status: production
type: side-project
owner: ryo
title: "LinkedIn Agent"
description: "Automated LinkedIn agent. Production, low maintenance."
phase: "Strategy execution and automation"
dashboard: other-projects
---

## Description
Automated LinkedIn agent. Runs in production with low maintenance overhead.

## Notes
- Automated. Low maintenance.

## Decisions

### 2026-04-15 — Skill-driven agent architecture
Full cutover from monolithic agent prompts to markdown-extracted skill files across the pipeline: Researcher, Architect, Strategist, Analyst, Picker, Planner. Strategist's deterministic guardrails split into a standalone module with tests, separate from the judgement prompt. Rationale: prompts in code are expensive to iterate; prompts as skill markdown can be edited, diffed, and versioned independently of agent wiring. Side benefit: the Architect now loads an MBIE N2RD "LinkedIn-safe" context file at runtime for Pillar 2 posts, so R&D content constraints are enforced at prompt-assembly time rather than buried in agent logic.

### 2026-04-15 (later) — Eliminated Anthropic API dependency entirely
Pushed the skill-driven architecture to its conclusion: deleted `agents/_llm.py`, `langchain-anthropic`, `langchain-core`, `config/model_config.json`. All seven agent roles (Planner, Researcher, Picker, Architect, Strategist, Analyst, Image Architect) now reason inside the active Claude Code session reading `agents/<name>.md` prompts. Cost model is now Claude Code subscription only — zero per-post API spend. Trade-off: the chat-first flow can no longer be cron-fired (it always required a Claude Code session for approval gates anyway, so this is theoretical not practical). Posting and analytics scraping remain cron-safe (Playwright, no LLM). Plan and execution diary at `temporary/plans/2026-04-15-claude-code-as-llm-refactor.md`.

### 2026-04-15 — Dev-time tooling: Playwright CLI + selector-repair skill
Installed `@playwright/cli` v0.1.8 globally, registered its skills at `.claude/skills/playwright-cli/`, and authored a project-specific `.cursor/skills/linkedin-selector-repair/SKILL.md`. Repair loop is now: drive LinkedIn live from the shell, find new selector via accessibility tree refs, update `tools/browser.py` `.or_()` chain. Production Python runtime untouched. Repair time when a selector breaks dropped from "half a day" to "~5 minutes". The CLI shares `auth/linkedin_session.json` with production via `state-load`/`state-save` (storageState format identical).

### 2026-04-15 — Audit + bug sweep across 10 workflows
Comprehensive audit at `temporary/audit/` (10 workflow markdowns + index): 7 critical, 28 significant, 36 minor issues identified. High-priority fixes shipped this session: silent `first_comment` drop in `schedule_post` (now retries URN extraction 3×, preserves text on failure), `executor_run` per-comment failure tolerance (≥4/6 success threshold), two-phase execution result merging (no more lost phase-1 comments), session cookie expiry pre-check in `playwright_settings`, auth pre-flight script (`scripts/auth_preflight.py`), nav-chrome heuristic in planner output, scheduling registry pruning + hash-based task names, em-dash check extended to Golden Hour comments, debug instrumentation purged from production. Pure-logic test coverage added for executor + scheduler.

## Decisions

### 2026-04-16 — SDUI DOM selector fix for feed scraping
LinkedIn overhauled their feed DOM to SDUI architecture (obfuscated class hashes, `componentkey` UUIDs, no more `data-id`/`data-urn` attributes). Scout was returning 0 targets for 3 weeks. Fix: auto-detect LazyColumn presence, use `[role="listitem"]` for post containers, regex `urn:li:activity:\d+` from innerHTML for post URLs, `[data-testid="expandable-text-box"]` for snippets, `a[href*="/in/"]` for author names. Legacy selectors kept as fallback if LinkedIn reverts. Changes confined to `tools/browser.py`. Verified: 20 feed targets + 1 pinned target extracted successfully.

### 2026-04-16 — Strategy pivot: audience-value-first content
Full strategy overhaul documented at `context/linkedin-strategy-pivot-2026-04.md`. Diagnosis: 8 tracked posts averaged 378 median impressions, 2 followers/week, content burnout, text-only format penalty (carousels get 596% more engagement), no commenting strategy, no newsletter. Pivot: from 3x/week text-only infrastructure commentary to 3x/week (1 carousel + 2 text) + fortnightly newsletter + daily 15-min commenting. Audience-value-first pillars: "What Works in NZ Primary Care" (55%, save-worthy: tool reviews, workflow tips, comparisons, checklists) and "What's Changing in NZ Primary Care" (40%, share-worthy: news impact, policy explainers, myth-busters, trend signals). Building/founder content moved to newsletter only. Quality gate: "Would a GP in Christchurch who's never heard of me save or share this?" Deep research addendum covers: competitive landscape (NZ space is empty), AI detection avoidance (44% healthcare penalty), carousel design (7 slides, 1080x1350), content efficiency (2 hrs 15 min/week via voice memo capture). Targets: 350 followers by July, 500 by October.

### 2026-04-19 — Windows Task Scheduler Golden Hour automation shipped
Full automation for "post while away from computer" in production. Two scheduled tasks are created per post: `LinkedInWake_<session_id>` fires at T-40min (`WakeToRun=True`, `StartWhenAvailable=True`, allowed on battery) and runs `scripts/ensure_claude_desktop.bat`; `LinkedInPost_<hash>` fires at T-20min and runs `python execute_post.py <session_id>` for the Golden Hour comments and main post sequence. Bug found and fixed during verification: Claude Desktop is installed as an MSIX/UWP package on this machine (`PackageFamilyName=Claude_pzs8sxrjxfjjc`, `AppID=Claude_pzs8sxrjxfjjc!Claude`, install location under `C:\Program Files\WindowsApps\...`), so the original `.bat` probing `%LOCALAPPDATA%\Programs\Claude\Claude.exe` would have silently failed to launch anything after wake. Rewrote launcher to use `start "" "explorer.exe" "shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude"`. Wake Timers verified enabled on AC and DC power. Schedule registry and task actions both confirmed pointing at correct paths and session IDs. First live firing: ManageMyHealth login UX post, Tue 21 Apr 2026 10:00 NZST.

### 2026-04-16 — Daily auth pre-flight cron
`schtasks` task `LinkedInAuthPreflight` runs `scripts/auth_preflight.py` daily at 8am NZST. Exit 0 = session valid; exit 2 = expired (run `login.py`); exit 3 = file missing. Gives 24-hour warning before any post slot. Task created via `scripts/create_auth_cron.bat`.

### 2026-04-22 — Bug fixes: post content and grow email
Two production bugs found and fixed. (1) `scripts/assemble_session_state.py` was reading the entire `draft_final.md` including metadata headers, causing those headers to be posted to LinkedIn verbatim. Fixed with `_extract_post_body()` regex parser that extracts only the `## Post Body` section, with fallback to full file for plain-format drafts. (2) `scripts/grow_run.py` live scout was gated by `return 2` (never wired), meaning Task Scheduler runs exited immediately with no log and no digest email. Fixed: removed gate, opens a browser context and calls `scout_targets_live()`. Execute phase also hardened: exception in `get_browser_context()` no longer crashes the process before `append_grow_log` and `send_digest` are reached.

### 2026-04-22 — Post execute workflow redesigned: fresh scout on posting day
Option 3 chosen: scout deferred from creation time to execution day. `linkedin-post-create` skill now covers post body, first comment, hashtags, and scheduling only — no scout, no GH comment drafting, no assemble. `linkedin-post-execute` skill rebuilt as four phases: (1) scout, (2) picker + GH draft + approval gate, (3) assemble, (4) execute. Golden Hour comments now anchored to posts scouted on the morning of posting, not days earlier.

### 2026-04-22 — Full automated pipeline design agreed
Architecture for fully autonomous posting pipeline with Telegram human-in-loop. Three zones: (1) Automated idea generation: weekly Telegram suggestions from NZ health news scan; (2) In-session creation: topic selection, research, draft review, schedule — one laptop session per post; (3) Autonomous execution: Task Scheduler fires Python script at T-40min, runs scout + `claude -p` GH draft, sends comments to Telegram for approval (15 min timeout, posts as-is on no reply), assembles and executes. Additional: Telegram auth health check weekly, automated 48h review via Telegram. Build order: autonomous execute script + Telegram bot first.

### 2026-04-23 — Root cause: ANTHROPIC_API_KEY contamination kills all claude -p calls
`load_dotenv(ROOT / ".env")` runs at startup in both `grow_run.py` and `execute_scheduled.py`, setting `ANTHROPIC_API_KEY` in the process env. Every `claude -p` subprocess inherits it. Claude CLI, when it sees `ANTHROPIC_API_KEY`, uses the Anthropic API directly instead of the Claude Code subscription. The API key has depleted credits ("Credit balance is too low"), so every call exits 1. The error appears on stdout, not stderr, so the old handler (`stderr: {result.stderr[:400]}`) silently swallowed it — the log showed empty stderr and "0 drafts" or "GH draft failed". This affected all unattended runs since April 20.

Fix shipped: `CLAUDE_CLI=C:/Users/reonz/.local/bin/claude.exe` added to `.env` (resolves Task Scheduler PATH gap); both `_invoke_claude` functions now strip `ANTHROPIC_API_KEY` from subprocess env and pass prompt via stdin. Error message now includes stdout. Verified working.

Secondary issue also fixed: `StartWhenAvailable` caused a concurrent second fire of `execute_scheduled.py` on Apr 22 when the live run was still alive. A lock file (`temporary/execute_scheduled.lock`, stale threshold 2h) prevents this.

### 2026-04-23 — Autonomous execute pipeline built
`scripts/execute_scheduled.py` ships as the unattended posting entry point. Phases: (1) scout via `agents.scout.run()` — aborts with Telegram alert on 0 targets; (2) draft 6 GH comments via `claude -p` + `agents/gh_commenter.md` — continues without GH comments on failure; (3) Telegram approval loop: 15 min total budget, natural-language edits parsed via second `claude -p` call, posts as-is on timeout; (4) write `engagement.json`; (5) assemble `session_state.json`; (6) run `execute_post.py`. `tools/scheduler.py` updated: `schedule_execution` now registers `execute_scheduled.py` at T-40min with WakeToRun + StartWhenAvailable. `tools/telegram.py` added (send + poll utility). `agents/gh_commenter.md` added (self-contained picker + drafter prompt). Dry-run verified: 19 live feed targets found; GH draft gracefully degrades when `claude -p` unavailable in nested session. Pending user action: add TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID to .env. Blocked by Telegram login issue — tracked in `linkedin-20260422-002`.

## Weekly Progress Log

### Week of 2026-04-21

**linkedin**
- Fixed: `assemble_session_state.py` now extracts post body only from `draft_final.md` — metadata headers no longer posted to LinkedIn
- Fixed: grow live scout wired in `grow_run.py` (removed `return 2` gate); execute phase hardened so log and digest email always run even on browser crash
- Post execute workflow redesigned: scout deferred to posting day; `linkedin-post-execute` rebuilt with scout, GH approval gate, assemble, and execute phases
- Full autonomous pipeline agreed: Task Scheduler + `claude -p` GH drafting + Telegram approval loop; build starts next session
- `tools/telegram.py` built: send message + long-poll utility for Bot API
- `agents/gh_commenter.md` built: self-contained picker + GH comment drafter prompt for headless `claude -p` calls
- `scripts/execute_scheduled.py` built: full autonomous execute orchestration (scout, GH draft, Telegram approval, assemble, execute)
- `tools/scheduler.py` updated: `schedule_execution` now fires `execute_scheduled.py` at T-40min with WakeToRun and StartWhenAvailable
- Dry-run confirmed: scout finds 19 live targets; GH draft degrades gracefully if `claude -p` unavailable; Telegram abort/approval/edit loop designed and tested
- Pending: add TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID to `.env` before next live post

### Week of 2026-04-14

- Scout feed scraping fixed for April 2026 LinkedIn SDUI DOM overhaul: new selectors (`role="listitem"`, regex URN from innerHTML, `data-testid` for snippets), auto-detection with legacy fallback
- Daily auth_preflight cron set up at 8am via `schtasks` (24h warning before post slots)
- linkedin-20260415-001 and linkedin-20260415-002 closed
- Phase 1–8 skill-driven flow cutover complete: Researcher → Architect → Strategist → Analyst → Picker → Planner → Image Architect; `agents/_llm.py` and langchain dependencies removed
- Strategist judgement prompt extracted to markdown; deterministic guardrails extracted to standalone module with 14 tests
- Architect loads MBIE N2RD LinkedIn-safe context at runtime for Pillar 2 posts
- Anthropic API dependency eliminated entirely — engine now runs on Claude Code subscription only
- `@playwright/cli` installed + new `linkedin-selector-repair` skill for ~5-min selector fixes via shell
- Comprehensive audit (10 workflows) shipped at `temporary/audit/`; high-priority bugs fixed (first_comment retry, executor failure tolerance, two-phase merge, auth pre-flight, scheduling registry pruning, em-dash check on comments)
- New scripts: `scripts/auth_preflight.py` (cron-safe session check), `scripts/append_performance_history.py` (extracted from deleted analyse_performance.py)
- Test suite rationalised: removed Phase 2 (Redis) + Phase 4b (script integration) + Phase 5 (agent pipeline); all 7 remaining phases pass with no Anthropic API calls
- Scout agent debug (linkedin-20260415-001) still in-progress — graph.state cause cleared, awaits live verification (pending session refresh via login.py)

## Tasks

```dataviewjs
const mb = app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api;
const lifecycle = this.component;
const statusOpts = [
  { name: 'option', value: ['open'] },
  { name: 'option', value: ['in-progress'] },
  { name: 'option', value: ['blocked'] },
  { name: 'option', value: ['done'] }
];
const priorityOpts = [
  { name: 'option', value: ['high'] },
  { name: 'option', value: ['medium'] },
  { name: 'option', value: ['low'] }
];
function statusSelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('status', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--status'] }, ...statusOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function prioritySelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('priority', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--priority'] }, ...priorityOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function scheduleDashboardColumnSort(dv, headerNames) {
  const bind = (table) => {
    if (table.dataset.vaultDashSortBound) return;
    const thead = table.querySelector('thead');
    const tbody = table.tBodies[0] ?? table.querySelector('tbody');
    if (!thead || !tbody || tbody.rows.length === 0) return;
    table.dataset.vaultDashSortBound = '1';
    const ths = thead.querySelectorAll('th');
    const stripArrows = (s) => String(s).replace(/\s*[\u25B2\u25BC]\s*$/, '').trim();
    const state = { col: -1, dir: 'asc' };
    ths.forEach((th) => { th.dataset.sortLabel = stripArrows(th.textContent); });
    ths.forEach((th, colIndex) => {
      th.style.cursor = 'pointer';
      th.title = 'Sort column';
      th.classList.add('vault-dash-sortable-th');
      th.addEventListener('click', (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        const nextDir = state.col === colIndex && state.dir === 'asc' ? 'desc' : 'asc';
        state.col = colIndex; state.dir = nextDir;
        const headerName = headerNames[colIndex] ?? '';
        const sortKey = (row) => {
          const cell = row.cells[colIndex];
          if (!cell) return '';
          if (/due/i.test(headerName)) {
            const raw = cell.innerText?.trim() ?? '';
            const L = dv.luxon.DateTime;
            const iso = L.fromISO(raw);
            if (iso.isValid) return iso.toMillis();
            const fmts = ['MMMM d, yyyy', 'd MMMM yyyy', 'yyyy-MM-dd', 'dd/MM/yyyy', 'd/MM/yyyy'];
            for (const f of fmts) { const d = L.fromFormat(raw, f, { locale: 'en-NZ' }); if (d.isValid) return d.toMillis(); }
            const ms = Date.parse(raw);
            if (!isNaN(ms)) return ms;
            return raw.toLowerCase();
          }
          const sel = cell.querySelector('select');
          if (sel) { const opt = sel.options[sel.selectedIndex]; return (opt?.textContent ?? opt?.innerText ?? sel.value ?? '').trim().toLowerCase(); }
          return (cell.innerText?.trim() ?? '').toLowerCase();
        };
        const tb = table.tBodies[0] ?? table.querySelector('tbody');
        if (!tb) return;
        const rows = Array.from(tb.rows);
        rows.sort((a, b) => { const ka = sortKey(a), kb = sortKey(b); let cmp = (typeof ka === 'number' && typeof kb === 'number') ? ka - kb : String(ka).localeCompare(String(kb), undefined, { numeric: true, sensitivity: 'base' }); return nextDir === 'asc' ? cmp : -cmp; });
        rows.forEach((r) => tb.appendChild(r));
        ths.forEach((h, i) => { const base = h.dataset.sortLabel || stripArrows(h.textContent); h.textContent = base + (i === colIndex ? (nextDir === 'asc' ? ' ▲' : ' ▼') : ''); });
      });
    });
  };
  const tryBind = () => { const table = dv.container.querySelector('table'); if (!table) return false; const tbody = table.tBodies[0] ?? table.querySelector('tbody'); if (!tbody || tbody.rows.length === 0) return false; bind(table); return true; };
  if (tryBind()) return;
  const obs = new MutationObserver(() => { if (tryBind()) obs.disconnect(); });
  obs.observe(dv.container, { childList: true, subtree: true });
  setTimeout(() => obs.disconnect(), 8000);
}
const pages = dv.pages('"tasks/open"')
  .where(p => p.project === "linkedin-agent" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
