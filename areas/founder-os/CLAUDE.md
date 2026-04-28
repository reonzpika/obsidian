# Founder OS — Area Context

Meta-layer: Claude Code config, vault structure, memory, hooks, skills, automation.

## Active sprint

Vault OS Redesign (fo-20260427-001 to fo-20260427-005).
Sprint plan: `context/vault-os-redesign-sprint-plan.md`

## Task prefix

`fo-*`

## Key files

- Skills: `~/.claude/commands/` (27 skills) and `~/.claude/skills/` (9 skills)
- Skill map: `~/.claude/skill-map.md`
- Memory: `~/.claude/projects/C--Users-reonz-cursor-obsidian/memory/`
- Hooks: `C:/Users/reonz/Cursor/hooks/`
- Settings: `~/.claude/settings.json`
- Best practice: `C:/Users/reonz/cursor/claude-code-best-practice/`

## Rules

- Before editing settings.json or .mcp.json: invoke `/update-config`
- Skill triggers must be specific; avoid "use this when…" vagueness
- No user-invocable skills without `user-invocable: true` and `argument-hint:`

## Decisions log

`C:/Users/reonz/cursor/obsidian/system/decisions-log.md` — all vault structure decisions.
