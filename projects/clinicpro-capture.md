---
id: clinicpro-capture
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
title: "ClinicPro Capture"
description: "Mobile web app to capture clinical images into Medtech via ALEX API."
phase: "Phase 1 marketing and AU bundle deal"
dashboard: clinicpro-medtech
---

## Description
Mobile web app that photographs clinical images and commits them to patient records in Medtech Evolution via the ALEX API. All ALEX calls route through BFF at api.clinicpro.co.nz.

**API reference**: [[alex-api-docs]]

## Phase 1 marketing — status (19 April 2026)

| Task                                            | Status                                  |
| ----------------------------------------------- | --------------------------------------- |
| Task 0: URL refactor + (marketing) route group  | Complete (commit prior to 64788af)      |
| Task 1: `/medtech/capture` landing page         | Complete (commit 64788af, 19 Apr)       |
| Task 2: `/refer-a-practice` bounty page + API   | Complete (commit 4326d34, 19 Apr)       |
| Task 3: Capture upsell banner in clinicpro-saas | Open (unblocked; planned end of sprint) |
| Task 4: Champion email v1                       | Open (pending landing page review)      |
| Task 5: Demo Loom script + case-study template  | Open                                    |

Landing page copy/design review (task medtech-20260419-001) must complete before champion email send.

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
- Auth: Supabase OTP (6-digit code, no magic link)
- Pricing (decided 2026-04-15): annual per practice by enrolled patient count ($299 / $799 / $1,500 / contact). No self-serve trial. Concierge trial via ryo@clinicpro.co.nz.
- BFF mandatory: never call ALEX directly from Vercel
- Phase 1 plan: `clinicpro-medtech/docs/superpowers/plans/2026-04-15-capture-marketing-phase1.md`

## Two-contract architecture with Medtech (locked 19 April 2026)

Two separate contracts, two commercial logics. Both land at Wed 22 April 2026 meeting with Lawrence Peterson + Alex Cauble-Chantrenne. Medtech may attempt to link them; refuse linkage.

1. **AU bundle deal** (Lawrence-led). Medtech Global purchases ClinicPro Capture licences to bundle into the Evolution AU launch. Per-licence fee model. Distinct product track (Evolution AU, a new launch separate from Medtech Evolution).
2. **Integration contract** (Alex-led, NZ + AU direct sales). Commission on ClinicPro-direct Capture sales. Covers both NZ and AU (revised 19 April; earlier 14 April position was NZ-only).

Bundle practices and direct-sales practices are largely distinct sets. Double-dipping carve-out clause to be written as belt-and-suspenders.

**Strategic context note (19 April 2026):** Medtech is the only PMS without a native image capture tool — Indici, Bp Premier, Best Practice, MedicalDirector have this solved. BATNA inversion: they need Capture to plug a competitive gap more than Ryo needs Medtech on this specific product. Strengthens posture on both contracts.

## 22 April 2026 meeting outcomes

**Lawrence (AU):** Strong interest, deal likely. AUD 30 not objected to. 50-practice minimum flagged as too high; Lawrence taking to boss — expected response within days. Floor is 40 at AUD 30 (per trade rules). Product confirmed as entirely new G2M software (Medtech AU revamp). Same ALEX backend, not all APIs accessible; capture API available. White-label confirmed. Medtech handling all marketing. Setup fee acknowledged verbally in room, no cost given. Competitor image vendor slow on issue response; Lawrence prefers ClinicPro. Lawrence raised a management dashboard (tenancy/licence model) — confirmed as out-of-bundle scope, separate one-off build engagement (task medtech-20260422-001). Auth, update control, security requirements, domain, tax treatment not discussed — carry to next meeting.

**Alex (NZ):** 15% flat commission confirmed verbally, NZ + AU scope. Default position held. NZ deal still pending formal team sign-off. PIA/pentest timeline and reporting cadence not confirmed.

## AU bundle — Lawrence Peterson (Medtech Global)

**Execution sprint**: [[2026-04-medtech-sprint-2]] (21 Apr - 16 May 2026)
**Strategy and pricing analysis**: [[clinicpro-capture-au-strategy]]
**External proposal one-pager**: [[clinicpro-capture-au-proposal]]

**Proposal received 12 April 2026:** Lawrence proposes Medtech purchases ClinicPro Capture licenses to bundle as a value-add for AU G2M in May. Scope: image capture + post only as starting point. Two other integration partners already confirmed for AU launch.

**Terms sent to Lawrence 19 April 2026** (CC Alex, existing thread 19cfe204467d0370):

- AUD 30 per active practice per month
- 50 active practices per year minimum → AUD 18,000/year floor
- 3-year initial term
- Scope: image capture and ALEX /DocumentReference POST
- Launch target May–June 2026 to align with Evolution AU G2M
- Sydney AWS hosting, AU data residency covered

## NZ + AU Integration Contract — Alex Cauble-Chantrenne (Medtech NZ)

**Strategy and pricing analysis**: [[clinicpro-capture-medtech-integration-strategy]]

Draft received from Alex 13 April 2026. Schedule 1 confirmed:

- Commencement Date: 18 March 2026
- Initial Term: 36 months (expires 18 March 2029)
- Fee structure (draft): $10–$60/month per Active Facility by enrolment tier — being renegotiated
- Permitted Purposes: direct image service only (Base + Portal without Confidential Scope + ALEX Apps)
- Software: Medtech Artia and Medtech Evolution

**Commercial position (confirmed 19 April 2026):**

- Opening ask: 15% flat commission on Gross Revenue. Simplified from earlier 10/15% self-referred / Medtech-referred split (14 April email), consolidated on 16 April call.
- Fallback: 20% flat commission.
- Walkaway: above 20%.
- Scope: both NZ and AU direct sales (revised from 14 April NZ-only position).
- PIA/pentest timeline: 6 months from go-live (not draft's 3 months).

Alex signalled personally on 16 April call that 30% was always "too much internally" and took 15% back to her team. Scope-revision email sent to Alex 19 April on existing thread (19cdf07cdcd3c13b) pulling back NZ-only line, keeping integration contract separate from AU bundle. 15% not re-mentioned in scope email — Alex already in team discussion.

Non-negotiables (full list in strategy doc):
1. Explicit NZ + AU geographic scope
2. Double-dipping carve-out (bundle practices excluded from commission until they convert to direct)
3. WHT on AU-sourced commission (services fee restructure, same as AU bundle)
4. Scope locked to ClinicPro Capture (future tools separate)
5. No exclusivity on ClinicPro side
6. Termination + integration IP with 6-month wind-down
7. PIA/pentest at 6 months from go-live

Tracked in task medtech-20260414-001.

## DB infrastructure (as of 22 April 2026)

- **Migration tracking:** `public.schema_migrations` table created (migration 0007). All 7 migrations registered. Future migrations must include `INSERT INTO public.schema_migrations (version) VALUES ('XXXX_name') ON CONFLICT DO NOTHING;` at the end.
- **Column rename:** `clerk_user_id` renamed to `user_id` on `medtech_image_commit_audit` (migration 0006). Drizzle schema and API route updated.
- **RLS:** All three tables (`medtech_image_commit_audit`, `rate_limit_buckets`, `users`) have RLS disabled. Service role access is unaffected, but anon key can query via PostgREST. Enable RLS with no policies to close this (task medtech-20260422-003).
- **Supabase MCP:** Configured globally in `~/.claude.json`. Use `mcp__supabase__execute_sql` for direct DB access in Claude Code sessions.

## Open questions / blockers

| # | Question | Status |
|---|---|---|
| Q1 | Does Medtech team accept 15% flat commission on NZ + AU direct sales? | Verbally confirmed by Alex in 22 Apr meeting. Awaiting formal contract. |
| Q2 | Does Lawrence accept AUD 30/practice/month — minimum practice number? | AUD 30 not objected to. 50-practice minimum flagged as too high. Lawrence taking to boss. Floor is 40 at AUD 30. |
| Q3 | Double-dipping carve-out language — operational definition of "bundle practice" vs "direct-sales practice"? | To draft post-meeting |
| Q4 | Reporting cadence for commission (quarterly acceptable, monthly burdensome) | Not discussed 22 Apr. To confirm next meeting. |
| Q5 | WHT services-fee restructure applied to both contracts — Helen briefing | Task medtech-20260418-004 |
| Q6 | Management dashboard scope — what does Lawrence need it to do? | Raised 22 Apr. Cannot price or commit until scope received from Lawrence in writing. Separate one-off invoice. Task medtech-20260422-001. |
| Q7 | Auth model for main product and admin dashboard | Not discussed 22 Apr. Must resolve before engineering starts. |
| Q8 | Update control: Medtech approval vs ClinicPro auto-deploy | Not discussed 22 Apr. Needed for setup fee scoping. |

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
