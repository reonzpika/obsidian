# Fork Agent Commands

| Command | What it does |
|---|---|
| `/branch [name]` | Create conversation branch at current point. Alias: `/fork` (unless `CLAUDE_CODE_FORK_SUBAGENT=1`) |
| `/fork` | Alias for `/branch` by default. When `CLAUDE_CODE_FORK_SUBAGENT=1`, spawns a forked subagent that inherits full parent conversation history and shares the prompt cache |
| `/resume [session]` | Return to a named or ID'd session |
| `/rewind` | Undo conversation and file state to a prior checkpoint (double-tap Escape also works) |
| `/btw <question>` | Side question that does not pollute context. No tools, no history write. Can fire mid-response |
| `/tasks` | List and manage all background agents |
| `/batch <instruction>` | Parallel large-scale changes: decomposes into 5-30 units, each in its own worktree |

## Fork vs non-fork decision rule

Fork when: the nuance of the main conversation is useful to the subagent (e.g. parallel research, continuing a thread with context).

Do not fork when: the main conversation would bias the subagent (e.g. code review of your own code).

## Cost note

Forked subagents share the parent's prompt cache. Up to 10x cost reduction vs spawning independent agents.

## Enable

`CLAUDE_CODE_FORK_SUBAGENT=1` is set in `~/.claude/settings.json` (global).

## SDK

```python
# Python
result = await claude.fork_session(session_id=..., fork_session=True)
```

```typescript
// TypeScript
const result = await claude.forkSession({ sessionId: ..., forkSession: true });
```
