---
id: clinicpro-capture
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
title: "ClinicPro Capture"
description: "Mobile web app to capture clinical images into Medtech via ALEX API."
phase: "Phase 1 marketing"
dashboard: clinicpro-medtech
---

**Commercial tracks**: [[clinicpro-capture-au-bundle]] (Lawrence Peterson) | [[clinicpro-capture-integration]] (Alex Cauble-Chantrenne)

## Description
Mobile web app that photographs clinical images and commits them to patient records in Medtech Evolution via the ALEX API. All ALEX calls route through BFF at api.clinicpro.co.nz.

**API reference**: [[alex-api-docs]]

## Phase 1 marketing — status (23 April 2026)

| Task                                            | Status                                  |
| ----------------------------------------------- | --------------------------------------- |
| Task 0: URL refactor + (marketing) route group  | Complete (commit prior to 64788af)      |
| Task 1: `/medtech/capture` landing page         | Complete (commit 64788af, 19 Apr); full design overhaul 23 Apr (framer-motion, nz-green tokens, 9 sections) |
| Task 2: `/refer-a-practice` bounty page + API   | Complete (commit 4326d34, 19 Apr)       |
| Task 3: Capture upsell banner in clinicpro-saas | Complete (commit 4be3b4f, 23 Apr)       |
| Task 4: Champion email v1                       | Drafted (`clinicpro-medtech/docs/marketing/phase-1/champion-email-v1.md`). Not sent: pending landing page review and incentive policy confirmation. |
| Task 5: Demo Loom script + case-study template  | Open                                    |
| Task 6: Hero video                              | Brief complete (25 Apr). Execution pending: `medtech-20260425-004`. Kling account pending: `medtech-20260425-003`. Brief at `docs/marketing/phase-1/hero-video-brief.md`. |

Landing page copy/design review (task medtech-20260419-001) must complete before champion email send. Capture subdomain `capture.clinicpro.co.nz` must be live before sending.

## Current goals
- Ship Phase 1 marketing (landing page, refer-a-practice, in-app banner, champion email, demo Loom) by 2026-04-21
- Warm-list blitz targeting ~60 NZ GP champions starts 2026-04-20
- Await Medtech production sign-off
- Onboard first paying practices after sign-off
- Success gate: 3+ practices paying or trialling by end of week 4

## Key decisions
- Deployment (decided 2026-04-22): dedicated subdomain `capture.clinicpro.co.nz`. Not path-based under `clinicpro.co.nz`. Vercel project owns the subdomain via CNAME. `clinicpro.co.nz` (SaaS) and `capture.clinicpro.co.nz` (Capture) are independent Vercel projects with no routing dependency between them.
- URL architecture (revised 2026-04-22): PMS-specific landing at `capture.clinicpro.co.nz/[pms]` (public, `(marketing)` route group) — build only when second PMS is added; authenticated app at `capture.clinicpro.co.nz/app/[pms]` (`(clinical)` route group, auth middleware covers all `/app/*`).
- Multi-PMS architecture (decided 2026-04-22): one repo (`clinicpro-medtech`), PMS adapters as modules. API and light UI differences per PMS are handled by the adapter, not separate repos or deployments. Adding a new PMS = new adapter module, no new repo.
- AU white-label deployment (decided 2026-04-22): separate Vercel project, same codebase, Lawrence's domain via CNAME (e.g. Medtech's own domain). Brand config via env vars. All product updates ship to NZ and AU from the same codebase.
- Marketing typography: Newsreader (serif display), IBM Plex Sans (body), JetBrains Mono (mono). Inter stays in-app only.
- Hero video toolchain (decided 2026-04-25): Nano Banana (still image generation, API already configured) + Kling 3.0 via Higsfield (image-to-video animation, setup pending). Workflow: generate key frames with Nano Banana, animate with Kling 3.0, Claude Code handles scroll-triggered frame integration and performance optimisation. Budget estimate ~$3-4 per hero clip. Kling 3.0 chosen over Veo 3.1 and Runway for quality/cost/control at 1080p.
- Auth: Supabase OTP (6-digit code, no magic link)
- Pricing (decided 2026-04-15): annual per practice by enrolled patient count ($299 / $799 / $1,500 / contact). No self-serve trial. Concierge trial via ryo@clinicpro.co.nz.
- BFF mandatory: never call ALEX directly from Vercel
- Phase 1 plan: `clinicpro-medtech/docs/superpowers/plans/2026-04-15-capture-marketing-phase1.md`

## Commercial overview

Two separate contracts with Medtech, kept strictly separate. Medtech may attempt to link them; refuse linkage.

- **AU bundle deal** (Lawrence Peterson, Medtech Global): [[clinicpro-capture-au-bundle]]
- **Integration contract** (Alex Cauble-Chantrenne, Medtech NZ): [[clinicpro-capture-integration]]

**Strategic note (19 April 2026):** Medtech is the only PMS without a native image capture tool. Indici, Bp Premier, Best Practice, and MedicalDirector have this solved. BATNA inversion: they need Capture to plug a competitive gap more than Ryo needs Medtech on this product. Strengthens posture on both contracts.

## BFF infrastructure (as of 22 April 2026)

- **Reference doc:** `context/medtech-context/lightsail-bff.md` contains the full BFF reference: all 18 endpoints, `BFF_INTERNAL_SECRET` auth model, rate limiting, OAuth token flow, systemd deployment, env vars, error patterns, and non-obvious design decisions. Read this before any BFF session.
- **Skills:** `/bff-deploy`, `/bff-rotate-secret`, `/bff-debug` created 22 April. Use these for all BFF operations.
- **Route refactor (commit 6d7b0fe):** capture routes moved up one level; `/capture` path segment dropped. API paths updated accordingly (commit 7523392).
- **Duplicate-NHI hardening (commit eaea8af):** guards ported from PR claude/fix-duplicate-nhi-patients-DoaFF. Race-condition duplicate NHI patient record creation is now blocked.

## DB infrastructure (as of 22 April 2026)

- **Migration tracking:** `public.schema_migrations` table created (migration 0007). All 7 migrations registered. Future migrations must include `INSERT INTO public.schema_migrations (version) VALUES ('XXXX_name') ON CONFLICT DO NOTHING;` at the end.
- **Column rename:** `clerk_user_id` renamed to `user_id` on `medtech_image_commit_audit` (migration 0006). Drizzle schema and API route updated.
- **RLS:** All three tables (`medtech_image_commit_audit`, `rate_limit_buckets`, `users`) have RLS disabled. Service role access is unaffected, but anon key can query via PostgREST. Enable RLS with no policies to close this (task medtech-20260422-003).
- **Supabase MCP:** Configured globally in `~/.claude.json`. Use `mcp__supabase__execute_sql` for direct DB access in Claude Code sessions.

## Partner portal

Scoped 25 April 2026. Provides dedicated views for each Medtech counterparty to manage their own practice pipeline without going through Ryo.

**Medtech Global (Lawrence):** manage AU bundle practices, see active licence counts, trigger practice onboarding directly.
**Medtech NZ (Alex):** initiate Capture onboarding for integration-side practices, self-serve, with usage data and commission tracking.

Same platform, separate data scopes. Bundle and direct-sales practices kept distinct by design.

**Schema finding (25 April 2026):** No `practices` table exists. Practices are currently just `facility_id` values in `medtech_image_commit_audit`. Portal requires four new tables: `practices`, `partners`, `partner_users`, `practice_invites`. The `facility_id` column in the audit table is the join key for usage data.

**Build estimate:** 3-4 weeks focused. Not started. Gated on both commercial arrangements being confirmed.

Tasks: AU bundle view tracked in `medtech-20260425-001`. Medtech NZ view tracked in `medtech-20260425-002`.

## Open questions

| # | Question | Status |
|---|---|---|
| Q3 | Double-dipping carve-out language — operational definition of "bundle practice" vs "direct-sales practice"? | To draft post-meeting |
| Q7 | Auth model for main product and admin dashboard | Not discussed 22 Apr. Must resolve before engineering starts. |

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
const all = dv.pages('"tasks/open"')
  .where(p => p.project === "clinicpro-capture" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const groups = {};
const unassigned = [];
for (let p of all) {
  const m = p.milestone ?? "";
  if (m) {
    if (!groups[m]) groups[m] = [];
    groups[m].push(p);
  } else {
    unassigned.push(p);
  }
}
const render = (tasks) => dv.table(
  ['Task', 'Status', 'Priority', 'Due'],
  tasks.map(p => [dv.fileLink(p.file.path, false, p.title || p.file.name), statusSelect(p.file.path), prioritySelect(p.file.path), p.due])
);
for (const [m, tasks] of Object.entries(groups)) {
  dv.paragraph(`**${m}**`);
  render(tasks);
}
if (unassigned.length > 0) {
  if (Object.keys(groups).length > 0) dv.paragraph("**Backlog**");
  render(unassigned);
}
```
