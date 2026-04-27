# NexWave AI Agent System — Architecture & Control Design

**Status:** Design proposal v2 — incorporating feedback from 3 external reviews
**Last updated:** 2026-03-30
**Author:** Ryo Eguchi + Claude Code
**Purpose:** Defines how AI agents are structured, controlled, and orchestrated across all NexWave products using Paperclip.ing as the orchestration layer.

---

## Why Paperclip

**The problem with the current setup:** Ryo manually orchestrates every step. Give spec to Cursor → watch execution → trigger next step → check UI/UX → think about QA. Each step requires active involvement and context-switching.

**What Paperclip changes:** The CEO agent handles orchestration. Developer and QA agents execute. Ryo reviews output at defined checkpoints — not every step.

This is the shift from *supervising every step* to *reviewing at gates*. For a solo founder coding in the evenings, that difference is significant.

**Honest ceiling:** Agents handle orchestration, code execution, test writing, and basic UI checks reliably today. UI/UX judgement and clinical QA verification always require Ryo — especially for a healthcare product.

| Step | Without Paperclip | With Paperclip |
|------|------------------|----------------|
| Spec → task breakdown | Ryo does it | CEO agent does it |
| Implementation | Cursor, Ryo supervises | Developer agent, Ryo reviews output |
| UI/UX check | Ryo does manually | Agent flags obvious issues, Ryo does final check |
| Test writing + running | Ryo or skipped | QA agent writes and runs, Ryo verifies clinical logic |
| Deployment | Ryo triggers | Approval gate fires, Ryo approves |

---

## System Structure

```
Paperclip instance (local, localhost:3100)
│
├── NexWave HQ          → Planning, discussion, research, task management
├── ClinicPro SaaS      → Feature development (clinicpro-saas repo)
├── ClinicPro Medtech   → Product development (clinicpro-medtech repo)
└── NexWave R&D         → MBIE-funded research (nexwave-rd repo)
```

**Core principle:** Planning and execution are strictly separated. HQ never touches code. Execution companies only receive work after Ryo has reviewed and approved a written handoff spec.

---

## Company Designs

### 1. NexWave HQ

| Field | Value |
|-------|-------|
| **Goal** | Strategic planning, research, and task coordination across all NexWave products |
| **Working directory** | `cursor/obsidian/` — strictly enforced, no access to repo folders |
| **Agents** | 1 — CEO (planning only) |
| **Autonomy level** | Low — Ryo drives all discussions |
| **Implementation** | None. This company never touches code. |

**What Ryo does here:**
- Discusses ideas, features, and problems with the HQ CEO
- Researches options and evaluates tradeoffs
- Reviews and approves handoff specs before they are sent
- Maintains the Obsidian task/project system

**What the HQ CEO does:**
- Reads Obsidian tasks, projects, sprint files
- Helps Ryo research, plan, and think
- Produces written handoff spec documents
- Does NOT write code, does NOT touch any repo folder, does NOT delegate without Ryo's explicit approval

**Filesystem isolation:** HQ agent `cwd` is set to `cursor/obsidian/` only. No read or write access outside this directory. This is a configuration constraint, not just a policy — verify in Paperclip's adapter settings before running.

---

### 2. ClinicPro SaaS

| Field | Value |
|-------|-------|
| **Goal** | Build and maintain ClinicPro SaaS products for NZ GPs |
| **Working directory** | `cursor/clinicpro-saas/` |
| **Autonomy level** | Medium — executes approved specs autonomously within checkpoint model |

**Agent roster:**

| Agent | Role | Responsibility |
|-------|------|---------------|
| CEO | Orchestration | Receives spec, breaks into tasks, assigns to dev and QA agents, manages completion |
| Developer | Execution | Implements code on a feature branch per task |
| QA | Testing | Writes and runs tests, flags failures, produces test report |

**Products:** referral-images, ai-scribe, 12-month-prescription, acc, openmailer

---

### 3. ClinicPro Medtech

| Field | Value |
|-------|-------|
| **Goal** | Ship ClinicPro Capture and future Medtech ALEX integrations |
| **Working directory** | `cursor/clinicpro-medtech/` |
| **Autonomy level** | Medium — executes approved specs autonomously within checkpoint model |

**Agent roster:** Same structure as SaaS (CEO, Developer, QA)

**Additional constraint:** Any change touching the BFF, ALEX API routes, or Supabase auth is a hard approval trigger — no exceptions.

---

### 4. NexWave R&D

| Field | Value |
|-------|-------|
| **Goal** | Execute MBIE N2RD grant Objective 1 — Foundation AI Architecture |
| **Working directory** | `cursor/nexwave-rd/` |
| **Autonomy level** | Medium — executes approved specs autonomously |

**Agent roster:** CEO + Research/Development agent (no QA agent initially — output is research documents, not production code)

**MBIE Isolation Checklist** (enforced, not just stated):

| Control | How |
|---------|-----|
| Separate API keys | R&D agents use dedicated `ANTHROPIC_API_KEY` env var, not shared with commercial companies |
| No shared codebase access | `cwd` locked to `nexwave-rd/` — no imports from or references to commercial repos |
| Separate Paperclip company | R&D is its own company — no cross-company task creation or agent sharing |
| Separate cost tracking | Paperclip tracks R&D spend separately for MBIE quarterly claims |
| Audit trail | All agent activity logged in Paperclip; exportable for MBIE evidence |
| Context isolation | R&D agent prompt templates contain no commercial product context |

---

## How Work Flows

### Step 1 — Discussion at HQ
Ryo talks to the HQ CEO. They discuss the idea, research options, and think through tradeoffs. No implementation happens. This can take multiple sessions.

### Step 2 — Ryo approves the plan
When the discussion reaches a conclusion, Ryo explicitly confirms the plan is approved.

### Step 3 — Determine spec type

Before writing the spec, classify the work:

| Spec type | When to use | Output |
|-----------|-------------|--------|
| **Implementation spec** | Work is well-understood, files and approach are clear | Execution company builds it |
| **Spike spec** | Significant unknowns exist (new integration, unfamiliar area, unclear scope) | Time-boxed investigation only — output is a short report + revised implementation spec, no production code |

If in doubt, default to spike. A spike that confirms the approach is fast. An implementation that hits a wall mid-execution is expensive.

### Step 4 — HQ CEO writes the handoff spec
The spec is saved to `cursor/obsidian/inbox/` as a dated markdown file. It must include:

- **Spec type** — implementation or spike
- **Objective** — what this achieves and why
- **Scope** — exactly what will be built or changed
- **Out of scope** — what must NOT be touched
- **Files/areas affected** — specific files, routes, or systems involved
- **Definition of done** — how to know the work is complete
- **Constraints** — technical and business rules to respect
- **Approval triggers** — any anticipated decisions that will require Ryo's sign-off
- **Target company** — which execution company receives this spec

### Step 5 — Ryo reviews the written spec
The written spec is reviewed before it is sent — even though the plan was already verbally approved. This catches translation errors between discussion and written brief.

### Step 6 — Ryo manually triggers the execution company
Ryo opens the relevant execution company in Paperclip and **pastes the spec content directly into the trigger message**. The `obsidian/inbox/` file is an archive copy; the transport is Ryo's manual paste. This keeps the handoff explicit and avoids execution agents having read access to the Obsidian directory.

### Step 7 — Execution company CEO orchestrates autonomously
The company CEO receives the spec, breaks it into tasks (implementation, UI check, testing), assigns to developer and QA agents, and monitors progress. Ryo is not involved unless an approval trigger fires.

### Step 8 — Ryo reviews at defined checkpoints
Ryo reviews output at these mandatory checkpoints. The CEO agent does not proceed past a checkpoint without Ryo's explicit sign-off:

| Checkpoint | What Ryo reviews |
|-----------|-----------------|
| After implementation | Code diff / PR — is the approach correct? |
| After UI check | Screenshots or live preview — does it look right? |
| After QA | Test report — are all cases covered? Any failures? |
| Before deployment | Final check before the approval gate fires |

### Step 9 — Completion synced back to Obsidian
When execution is complete, the execution company CEO writes a one-paragraph completion summary (what was built, PR link, any deviations from the spec). Ryo reviews this, then updates the relevant Obsidian task status to `done` manually or asks the HQ CEO to do it in the same session.

**Obsidian is the authoritative record. Paperclip's issue state is ephemeral.**

---

## Approval Triggers — Mechanical, Not Judgement-Based

Execution agents must surface an approval to Ryo when any of the following conditions are true. These are checked mechanically against the diff — not left to agent interpretation.

**Hard triggers (file-based):**

| File pattern | Reason |
|-------------|--------|
| `package.json`, lockfiles | New dependency introduced |
| `middleware.ts`, `middleware.js` | Auth/routing change |
| `vercel.json`, `next.config.*` | Deployment config change |
| `*.env*`, secret references | Credentials or environment change |
| `database/migrations/*` | Schema change |
| Any Stripe/Clerk/Supabase auth file | Billing or auth change |
| BFF files (`lightsail-bff/*`) | Medtech/ALEX integration |
| `drizzle.config.*`, `schema/*` | Database schema |

**Judgement triggers (backup only — not the primary control):**

| Condition | Reason |
|-----------|--------|
| Any architectural decision not in the spec | Scope drift |
| Anything the agent is genuinely uncertain about | Default to asking |

`When in doubt, surface it` remains as a backup instruction but is not relied upon as a primary control.

---

## Git Containment Model (Non-Negotiable)

All execution agents operate under these git rules regardless of autonomy level:

| Rule | Detail |
|------|--------|
| Feature branches only | Agents never commit to `main` or `master` directly |
| PR required | Every piece of work ends with an open PR, not a merged commit |
| No agent merges | Agents open PRs. Ryo reviews and merges. |
| No direct deploys | Agents never trigger production deployments. Deployment requires Ryo's approval gate. |
| Branch naming | `agent/<company>/<spec-id>/<short-description>` |

This uses existing git infrastructure as a control layer. It is cheap to enforce and high value — a bad agent commit is reviewable before it affects anything.

---

## Safety Constraints (Non-Negotiable)

| Constraint | Setting | Reason |
|-----------|---------|--------|
| `maxTurnsPerRun` | 10 | Caps steps per heartbeat; agent reports and stops |
| `dangerouslySkipPermissions` | `false` always | Claude Code always asks before writes and commands |
| Monthly budget per agent | Start low, increase based on pilot data | Auto-pause at 100%, soft alert at 80% |
| Heartbeat schedule | **Manual only** | No automated triggers. Ryo decides when agents run. |
| Company-level monthly cap | Set per company | Hard ceiling on total spend |

---

## Communication Model

```
Ryo
 │
 ├──[daily]──→ HQ CEO (discussion, planning, spec writing)
 │
 └──[checkpoint reviews + approval gates]──→ Execution company CEOs
                              ├── ClinicPro SaaS CEO
                              ├── ClinicPro Medtech CEO
                              └── NexWave R&D CEO
```

Ryo does not talk to developer or QA agents directly. They are managed by their company CEO.

---

## Obsidian and Paperclip — Roles

| Obsidian | Paperclip |
|----------|-----------|
| **Source of truth** — all task/project records | **Ephemeral execution state** — agent activity, issue status per run |
| Sprint planning and project strategy | Heartbeat scheduling and agent monitoring |
| Handoff spec archive (`inbox/`) | Real-time cost and activity dashboard |
| Long-term reference context | Audit log (exportable for MBIE) |

When the two conflict, **Obsidian wins**. Paperclip's issue state is reset after each execution cycle.

---

## Google Calendar Integration

A dedicated Google Calendar **"NexWave Tasks"** provides timeline visualisation across all repos.

**What gets synced:**

| Source | Calendar event |
|--------|---------------|
| Task with due date | All-day event on due date |
| Overdue task | All-day event on today with "⚠️ OVERDUE:" prefix |
| Active sprint | Multi-day event spanning sprint start → end |
| Hard deadline (e.g. MBIE claim 31 May) | All-day event with "🔴 DEADLINE:" prefix |

**Colour coding:**

| Repo | Colour |
|------|--------|
| clinicpro-medtech | Blue (Peacock) |
| clinicpro-saas | Green (Sage) |
| nexwave-rd | Purple (Grape) |
| HQ / cross-project | Grey (Graphite) |

**Sync:** Runs at end of each session via `done` skill. Claude Code reads Obsidian tasks, diffs against current calendar state, creates/updates/deletes events using the Google Calendar MCP.

**Scope note:** Calendar sync is read from Obsidian only — it is not wired to Paperclip. The calendar reflects task due dates, not agent execution state.

---

## Paperclip Setup

**Prerequisites:** Node.js 20+, pnpm 9.15+, `ANTHROPIC_API_KEY`

**Quickstart:**
```bash
npx paperclipai onboard --yes
# API at http://localhost:3100
```

**Claude Local adapter config (per execution agent):**
```json
{
  "adapter": "claude_local",
  "cwd": "/absolute/path/to/repo",
  "model": "claude-sonnet-4-6",
  "maxTurnsPerRun": 10,
  "dangerouslySkipPermissions": false,
  "timeoutSec": 300
}
```

**Caution:** Paperclip launched March 2026 and is approximately 3 weeks old. Treat it as alpha infrastructure. Build escape hatches — if Paperclip breaks, the fallback is: Ryo pastes the spec directly into a Claude Code session in the relevant repo. Same spec, same output, zero orchestration overhead.

---

## Implementation Sequence

1. **Google Calendar sync** — immediate visibility win, no new infrastructure, can be done now
2. **Paperclip pilot — ClinicPro Medtech only** — active sprint, one company, real feature from spec to PR
3. **Evaluate:** Did the CEO→Developer→QA handoff work? Was the overhead worth it vs a single Claude Code session?
4. **If pilot succeeds:** Add ClinicPro SaaS
5. **Then:** Add NexWave R&D (requires MBIE isolation checklist verified first)
6. **Add HQ company last** — once execution companies are stable and the orchestration model is proven

---

## Open Questions

1. Can Paperclip's adapter config hard-restrict filesystem access to `cwd` only, or is it enforced only at the prompt level?
2. What is the break-glass policy for an urgent production incident when Ryo is unavailable and an approval gate is blocking?
3. How are secrets scoped per company when all companies run under one local Paperclip instance?
4. If a spec turns out to be wrong mid-execution, does the execution CEO abandon the branch and request a revised spec, or can Ryo amend the spec in-flight?
