---
id: other-projects
status: active
type: side-project
---

# Other Projects

Personal, family, and training projects outside of ClinicPro and NexWave R&D. Maintained by Ryo and Ting.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "other-projects" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "other-projects" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Weekly Progress Log

### Week of 2026-04-14

**miozuki**
- Two-track collaboration workflow shipped: Ting works direct on master, Ryo on feature branches with Vercel previews. `.vscode/tasks.json` (dev server auto-start), `.vscode/settings.json` (one-click auto-push commit), `Ctrl+Alt+P` publish shortcut, `TING-GUIDE.md`, `CLAUDE.md` workflow note, `docs/ting-laptop-setup.md` checklist
- In-person setup on Ting's laptop completed 15 Apr — miozuki-20260415-001 closed
- Site audit cycle run: first audit results filed, audit scripts added to repo, Instagram proxy, Klaviyo subscribe + email popup a11y + contact form fixes shipped
- LCP image perf pass: priority + responsive `sizes` added; audit re-run against fixes

**linkedin (automation go-live, Apr 19)**
- First post on new strategy scheduled: ManageMyHealth patient portal login UX (Pillar A, text), publishes Tue 21 Apr 10:00 NZST
- Golden Hour Windows automation shipped and verified: wake timers enabled on AC + DC; auth session valid; schedule registry + task actions verified end-to-end
- Bug fixed: `scripts/ensure_claude_desktop.bat` Claude Desktop MSIX/UWP package path resolved

**linkedin (strategy pivot, Apr 16-17)**
- Full LinkedIn strategy overhaul: Pillar A "What Works in NZ Primary Care" (55%) + Pillar B "What's Changing in NZ Primary Care" (40%)
- Cadence: 3x/week (1 carousel Tue + 2 text Thu/Sat) + fortnightly "The GP Builder" newsletter
- Knowledge files updated to v4.0; Golden Hour system redesigned with core_targets.json

### Week of 2026-04-23

**founder-os**
- Project created: Claude Code setup audit and improvement. Dashboard: Other Projects.
- Claude Code audit completed: `context/tools/claude-code-audit-2026-04-23.md` — 4 critical gaps, 7 quick wins. Critical gap: bypassPermissions active globally with no per-repo guardrails.
- Settings-todo checklist created: `context/tools/claude-code-settings-todo.md` — exact JSON for all settings.json changes, per-repo settings.json for linkedin/clinicpro-medtech/nexwave-rd, code-reviewer agent content. Apply via /update-config from home directory.
- Task fo-20260423-001 created: watch "The Claude Code Setup Nobody Shows You" and apply improvements (due 27 Apr)

**linkedin-agent**
- grow reliability: diagnosis doc fact-checked against code; 4 inaccuracies found (atexit claim wrong, line numbers off, Apr 20 grow-2 gap unexplained)
- RC-5: stderr now written to `temporary/logs/grow_run_YYYY-MM-DD.log` in `grow_run.py`
- RC-1: ctypes `SetThreadExecutionState` sleep block prevents laptop lid from killing headed Playwright browser mid-scout; released on atexit and normal exit
- RC-3: `ExecutionTimeLimit` bumped 30 to 90 min in `install_grow_scheduler.ps1`; all three tasks re-registered via elevated PowerShell
- RC-2 diagnostic: `claude -p` confirmed exit 0 in non-interactive context; no code change needed
- `linkedin-20260426-001` closed

### Week of 2026-04-21

**miozuki**
- Full strategy review: 10 AI research docs reviewed (1 deleted), selective do/defer/skip decisions made across SEO, content, backlinks, tooling, and community themes
- Brand positioning locked: heirloom ethics narrative, dual-category (moissanite + pearl) positioning, NZ provenance narrative, gifting collection ($300-$1,200 tier)
- SEO architecture confirmed: subdirectory /learn (not subdomain), /moissanite-guide hub launching Month 4-6, 1-2 posts/month content floor
- Action plan produced: `inbox/miozuki/action-plan.md` -- 6 phases, source docs deleted
- 9 new tasks created (miozuki-20260426-002..010): Phase 0 (this week urgent), Phase 1 (developer sprint), Phase 2 (brand positioning)
- Deferred: Reddit, micro-influencer campaign, Pinterest active channel, all AI photography tools
- Open blocker: product photography needed before Viva pitch, chatbot build, and collection copy

**fellowship-application**
- Module 2 Clinical Record Review completed: 10 records, all 17 criteria audited
- 4 criteria with findings: cr.1 (history source), cr.11 (medication labelling), cr.16 (non-scheduled immunisations), cr.17 (occupational history)
- Report and Plan template filled in PDF programmatically; output: `Clinical Record Review Audit Checklist - Complete.pdf`
- gpf-20260330-004 closed
- Fellowship Assessment Visit form (7-page fillable PDF) walked through; submission package broken into 7 tasks (gpf-20260425-001..007) split across desk fill (Sun/Mon) and on-site equipment + drug walkthrough (Tue)

**linkedin-agent**
- Fixed: `assemble_session_state.py` now extracts `## Post Body` section only; metadata headers no longer posted to LinkedIn
- Fixed: grow live scout wired in `grow_run.py` (removed `return 2` gate); execute phase hardened so log and digest email always run on browser crash
- Post execute workflow redesigned: scout deferred to posting day; `linkedin-post-execute` rebuilt with four phases (scout, GH approval gate, assemble, execute)
- Autonomous execute pipeline built: `scripts/execute_scheduled.py`, `tools/telegram.py`, `agents/gh_commenter.md`; Task Scheduler updated to fire at T-40min with WakeToRun
- Dry-run confirmed: 19 live feed targets found; GH draft degrades gracefully; exit code 0
- Blocked: Telegram login issue prevents bot setup (tracked: `linkedin-20260422-002`)
- Diagnosed two production failures (grow 0-draft digest, Apr 21 post not executing): root cause `load_dotenv` sets `ANTHROPIC_API_KEY` in process env; `claude -p` subprocess inherits it and hits depleted API credits; error appeared on stdout not stderr so was silently swallowed as empty stderr
- Fixed: `CLAUDE_CLI=C:/Users/reonz/.local/bin/claude.exe` added to `.env` (Task Scheduler PATH gap); `ANTHROPIC_API_KEY` stripped from subprocess env in both grow and execute scripts; prompt passed via stdin to avoid Windows arg-length edge cases
- Fixed: lock file in `execute_scheduled.py` prevents concurrent runs when `StartWhenAvailable` double-fires; `mark_post_executed()` called on success; atexit + SIGTERM handler flushes `grow_log.json` on unexpected termination
- Apr 21 post (`2026-04-16_managemyhealth-login-ux`) was never executed; registry still "scheduled"; decision needed once Telegram is set up (tracked: `linkedin-20260423-002`)

**vault restructure**
- Sprint layer eliminated: `sprints/active/` removed from vault, replaced with `phase:` on projects and `milestone:` on tasks
- GP Fellowship wikilink ambiguity resolved: `projects/gp-fellowship.md` renamed to `projects/fellowship-application.md` (`id: fellowship-application`); 15 gpf-* task files updated
- `dashboards/gp-fellowship.md` deleted; GP Fellowship project absorbed into Other Projects dashboard
- `dashboards/side-projects.md` renamed to `dashboards/other-projects.md`; all Dataview queries and project frontmatter updated
- Heron project moved from Partnerships to Other Projects (`dashboard: other-projects`)
- `home.md` nav and section headers updated: GP Fellowship removed, Side Projects → Other Projects
- All skill files updated (daily, weekly, monthly, obsidian, obsidian-task-table, adopt): sprint references removed, project/phase/milestone pattern adopted throughout
- Vault `CLAUDE.md` updated: hierarchy rules, task schema, project schema, gotchas

**vault restructure (Apr 26)**
- `home.md` moved to repo root; references updated in `.obsidian/app.json`, vault `CLAUDE.md`, and `daily/SKILL.md`
- LinkedIn dashboard created: `dashboards/linkedin.md`; `linkedin-agent` split into two projects: `linkedin-content` (strategy, pillars, post management) and `linkedin-agent` (automation pipeline); both under `dashboard: linkedin`; tasks linkedin-20260419-001 and linkedin-20260423-002 reassigned to `linkedin-content`
- Miozuki dashboard created: `dashboards/miozuki.md`; `projects/miozuki.md` moved from `other-projects` to `miozuki` dashboard
- `home.md` nav and sections updated: LinkedIn and Miozuki added between Personal and Other Projects
- `daily/SKILL.md` Dashboard areas table updated: added gp-os, personal, linkedin, miozuki
