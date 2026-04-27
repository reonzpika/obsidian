# Workflow Reference

Rituals and skill triggers. Full skill list: `context/skills-index.md`.

---

## Daily ritual

1. Open `weekly.md`. Read the briefing section at the top (4 lines, one per stream).
2. Run `/daily`. It updates the weekly file with today's section. Surfaces urgent items.
3. Pick one stream. Start directing.

---

## Session end ritual

1. Run `/session-update`. Writes session summary to `logs/YYYY-WNN.md`. Updates briefing section in `weekly.md`.
2. Confirm any AI output generated this session landed in `inbox/` before moving anywhere.

---

## Weekly ritual (Friday or end of last session of the week)

1. Run `/weekly`. Rolls up the week. Archives `weekly.md` to `logs/`. Resets `weekly.md` for next week.

---

## Monthly ritual (end of month)

1. Run `/monthly`. Rolls up weekly summaries. Writes `monthly.md`. Updates dashboard phase fields.

---

## Skill decision tree

| Situation | Skill |
|---|---|
| Strategic question, direction choice, "which way do I go" | `/board` first — before any write-up |
| Morning orientation | `/daily` |
| New Obsidian file or Obsidian syntax | `/obsidian-markdown` |
| New task table in a project | `/obsidian-task-table` |
| Canvas file | `/json-canvas` |
| Email draft | `/gmail-draft` (never Gmail MCP) |
| Google Workspace (Gmail, Drive, Calendar) | `/gws` |
| Parallel research tasks (2+ independent) | `/agent-batch` |
| End of session | `/session-update` |
| End of week | `/weekly` |
| End of month | `/monthly` |
| Skill improvement | `/evolve` |
| System config change (settings.json, .mcp.json) | `/update-config` — never edit directly |
| Web page content extraction | `/defuddle` |
| Medtech partner meeting prep | `/medtech-prep` |
| LinkedIn post | `/linkedin-post-drafter` |

---

## Key rules

- Every strategic question: propose `/board` before writing anything.
- Every AI output: lands in `inbox/` first. No exceptions.
- Never create `daily/YYYY-MM-DD.md` files. Update `weekly.md` instead.
- History and logs go to `logs/`. Not dashboards.
- Before editing `settings.json` or `.mcp.json`: run `/update-config`.
- Irreversible actions (delete, push, send, bulk move): one-line confirmation, wait for explicit yes.
