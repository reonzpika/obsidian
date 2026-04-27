# Tech Stack Reference

## Shared tools

| Tool | Details |
|---|---|
| AI | Claude Code CLI — default model `claude-sonnet-4-6`; use `claude-opus-4-7` for complex reasoning |
| Vault | Obsidian with Dataview, Meta-bind, Templater, obsidian-git (auto-commits every edit) |
| Google Workspace | Access via `gws` CLI — never use Gmail/Drive/Calendar MCP tools directly |
| Version control | Git — obsidian vault auto-commits via obsidian-git; code repos use main branch only |
| Hosting | Vercel (all Next.js apps); AWS Lightsail (BFF only) |
| Cloud | AWS (Bedrock, Lightsail) — Auckland region `ap-southeast-6` for data residency |

---

## clinicpro-saas
- Framework: Next.js (App Router), TypeScript, Tailwind
- Database: Neon (Postgres), Drizzle ORM
- Auth: Clerk
- Payments: Stripe
- Deploy: Vercel (clinicpro.co.nz)

## clinicpro-medtech
- Framework: Next.js (App Router), TypeScript, Tailwind
- Database: Supabase Postgres (Sydney, ap-southeast-2)
- Auth: Supabase Auth (OTP — signInWithOtp + verifyOtp, no magic link)
- Deploy: Vercel (/medtech/* path)
- BFF: AWS Lightsail (api.clinicpro.co.nz, static IP)
- Critical: ALL Medtech ALEX API calls must route through BFF. Never call ALEX directly from Vercel.

## nexwave-rd
- AI: AWS Bedrock (Claude Haiku/Sonnet, AU Cross-Region Inference, ap-southeast-6)
- CVDRA: Deterministic Python (NZ PREDICT equation — not LLM)
- Data residency: AWS Auckland (ap-southeast-6)

## GitHub
- Account: reonzpika
- Workflow: main branch only. No PRs/issues workflow.

---

## Tools

### OpenSpace (custom build)
- Repo: https://github.com/HKUDS/OpenSpace
- What it is: Self-evolving skill engine for AI agents — captures reusable task patterns, auto-improves them, shares across agents
- Our version: Built a custom `/evolve` skill + hook system on top of Claude Code instead. No API key needed — uses Claude Max plan. Skills are `.md` files in `~/.claude/commands/`, tracked via `skill-evolver/` hooks, reviewed end-of-session with `/evolve`.

---

## Curious / Exploring

### CLI-Anything
- Repo: https://github.com/HKUDS/CLI-Anything
- What it is: Makes any software agent-native via CLI interfaces

### notebooklm-py
- Repo: https://github.com/teng-lin/notebooklm-py
- What it is: Unofficial Python API + CLI for Google NotebookLM — programmatic access including features not in the web UI, usable from scripts and AI agents

### Awesome Open Source AI
- Repo: https://github.com/alvinunreal/awesome-opensource-ai
- What it is: Curated list of open-source AI models, libraries, inference/serving, agents, RAG, MLOps, evaluation, safety, and related tooling (awesome-list style)
