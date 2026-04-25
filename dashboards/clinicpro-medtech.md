# Dashboard — ClinicPro Medtech

Products: ClinicPro Capture (and future Medtech ALEX products)

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "clinicpro-medtech" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
```

---

## Quick links

| | |
|--|--|
| **Products** | [[clinicpro-capture]], [[clinicpro-dashboard]] |
| **API reference** | [[alex-api-docs]] |
| **Glossary** | [Medtech / ALEX Glossary](context/medtech-context/glossary.md) |
| **Context** | [Capture context](context/medtech-context/clinicpro-capture/) · [Dashboard context](context/medtech-context/clinicpro-dashboard/) |
| **Repo map** | [[repos]] |
| **Finance & accounting** | Helen Yu (accountant, all entities) — see [people.md](../context/people.md#helen-yu) for scope |

---

## Weekly Progress Log

### Week of 2026-04-07
- Defne (Medtech) confirmed all five FHIR roles granted: Invoice R/W, ChargeItem R, ExplanationOfBenefit R, Task R/W, Communication R/W
- Tested Invoice endpoint via SSH on Lightsail BFF — discovered patient/date search not supported; only `GET /Invoice?_id=` works (confirmed against ALEX API docs)
- ChargeItem confirmed working — returns practice billing catalogue for facility F2N060-E
- Diagnosed billing completeness architectural constraint: cannot retroactively audit invoices by patient; redesigned as appointment-driven billing prompt (see clinicpro-dashboard.md)
- Updated clinicpro-dashboard.md with API status findings and new billing completeness architecture
- Sent follow-up to Alex Cauble-Chantrenne re Medtech partnership agreement (OOO until 10 April)
- Sent feature request to Defne requesting patient-based Invoice search (`Invoice?subject=Patient/{id}`)
- Confirmed invoice patient search not supported by design (Prashanth/ALEX Support 8 Apr): billing completeness module architectural constraint resolved
- Lawrence Peterson replied 12 April with AU deal proposal: Medtech seeking to purchase ClinicPro licenses to bundle into AU G2M product for May
- Alex Cauble-Chantrenne: partnership agreement draft promised 7 April but not yet received
- Lawrence Peterson: follow-up sent 13 April re infrastructure running costs

### Week of 2026-04-21 (continued 25 Apr, session 2)
- Hero video toolchain decided: Nano Banana (stills) + Kling 3.0 via Higsfield (animation) + Remotion + Claude Code (sequencing and integration)
- Hero video concept confirmed via board session: over-the-shoulder clinical scene wrap + screenshot walkthrough with cursor animation; 4:5 portrait, 6/6 hero grid split
- Hero video production brief written to `clinicpro-medtech/docs/marketing/phase-1/hero-video-brief.md`
- notebooklm-py v0.3.4 installed and authenticated; hero video research complete (10 YouTube sources indexed)
- Kling 3.0 Higsfield account setup pending (blocks cinematic shots 1-3); Remotion-only version (walkthrough) can ship independently

### Week of 2026-04-21 (continued 25 Apr)
- Hold replies sent to all 3 law firms: HGM (Andrew Dentice), Kindrik (Averill Dickson), Duncan Cotterill (Ron Arieli) — all on hold pending WHT resolution and term sheet finalisation
- Duncan Cotterill (Ron Arieli) appeared unsolicited; hold reply sent, task medtech-20260424-001 closed
- Mark Lowndes (Tompkins Wake) also replied unsolicited; no draft exists — task medtech-20260424-002 open, reply needed
- Partner portal concept scoped: one platform, two views — Medtech Global (AU bundle admin) and Medtech NZ (self-serve practice onboarding); self-serve licence purchasing planned for Lawrence's view
- DB schema confirmed: no practices entity exists; portal requires practices, partners, partner_users, practice_invites tables; `facility_id` in audit table is join key; 3-4 week build estimate
- Partner portal section added to clinicpro-capture.md with schema findings and build estimate
- Gmail draft ready: "Following up from the 22nd" to Lawrence (TO) + Alex (CC), introduces partner portal concept (draft r5920732408655842353)
- Tasks created: medtech-20260425-001 (send partner portal email), medtech-20260425-002 (scope Medtech NZ portal, blocked on commission decision)

### Week of 2026-04-21
- Capture landing page full design overhaul: ported `letter-grammar.tsx` (framer-motion) from clinicpro-saas, added `nz-green` Tailwind tokens, redesigned all 9 sections to match referral-images editorial-clinical aesthetic
- Dark navy trust section (`#0c1628`), ScrambleRotate cycling heading, amber/slate palette, CharStagger section headings, AnimatePresence FAQ accordion
- Fixed double-header bug (removed stray header from `app/(marketing)/layout.tsx`)
- Hero animation simplified to match referral-images: single `0.55s ease` fade-up replacing line mask reveal
- Hero heading updated: "The Medtech Evolution Capture problem." / italic "Solved."

- Held Wed 22 April meeting with Lawrence Peterson (AU) and Alex Cauble-Chantrenne (NZ)
- AU: Lawrence confirmed strong interest. No objection to AUD 30/practice. Flagged 50-practice minimum too high, taking to boss. Floor is 40 at AUD 30.
- AU: product confirmed as G2M, entirely new software. Same ALEX backend. Capture API available. White-label confirmed. Medtech handling all marketing.
- AU: Lawrence raised management dashboard with tenancy/licence model. Confirmed as out-of-bundle scope, separate one-off build engagement.
- NZ: Alex confirmed 15% flat commission covering NZ + AU direct sales. Default position held, no concession.
- Meeting briefing updated with notes and checklist ticks; pricing table updated with +10k profit threshold per price scenario.
- Task `medtech-20260422-001` created: scope and ideate management dashboard.
- Supabase MCP server configured globally (`~/.claude.json`), scoped to project fnyiqyxgwwbjrklongda; `SUPABASE_ACCESS_TOKEN` set as Windows env var
- Verified all 7 DB migrations applied correctly via MCP
- Renamed `clerk_user_id` to `user_id` on `medtech_image_commit_audit`: migration 0006 + Drizzle schema + API route updated, pushed to main
- Created `public.schema_migrations` tracking table (migration 0007): all migrations backfilled; going forward each migration registers itself
- RLS advisory: 3 tables have RLS disabled; SQL ready, task medtech-20260422-003 tracks the fix
- Tasks created: 003 (RLS), 004 (Vercel env vars for duplicate NHI alerts), 005 (BFF deployment with security deps)
- Audited Lightsail BFF codebase in full: 18 endpoints, auth model, rate limiting, OAuth flow, deployment config, known gaps
- Created `context/medtech-context/lightsail-bff.md`: complete BFF reference (env vars, all endpoints, systemd commands, error patterns, non-obvious design decisions)
- Created skills: `/bff-deploy`, `/bff-rotate-secret`, `/bff-debug`
- Route refactor shipped (commit 6d7b0fe): moved capture routes up one level, dropped `/capture` path segment
- Duplicate-NHI hardening ported from PR claude/fix-duplicate-nhi-patients-DoaFF (commit eaea8af): guards against race-condition duplicate NHI patient records
- API path and middleware route fixes applied (commit 7523392): corrected broken routes from port rename
- Correction: Alex did not confirm 15% verbally at 22 Apr meeting — asked for clarification on the figure only; team decision still pending
- Lawrence follow-up email drafted (Gmail draft): short "minimum practice number outstanding" note, threaded in AU bundle thread
- Alex follow-up email drafted (Gmail draft): signals readiness to move to contract, asks if anything needed to unblock team decision
- Term sheet approach confirmed: 3-year term goes in term sheet (already in 19 Apr proposal); no pre-negotiation needed
- AU term sheet v1 drafted: `clinicpro-medtech/docs/commercial/au-bundle-term-sheet-v1.md` — AUD $30/practice/month, 40-50 practice floor ($14,400-$18,000/year). 8 open questions documented. Hold until Q5 (WHT/Helen) resolved before sending to Lawrence.
- AU deal value corrected: $14,400-$18,000/year (not $50-150k as previously stated in draft emails)
- AU contract approach decided: self-draft with AI, get reviewed only — proportionate for deal size
- HGM (Andrew Dentice): fee estimate request sent — review-only scope, deal value corrected, WHT flagged as key issue
- Kindrik Partners: simple inquiry email sent — add scope/deal context when they reply
- Champion email v1 drafted: `clinicpro-medtech/docs/marketing/phase-1/champion-email-v1.md` — "3 months of Capture, on me" offer; confirm incentive policy and capture.clinicpro.co.nz live before sending
- Lawrence follow-up "Following up — AU bundle" sent
- Alex Cauble-Chantrenne follow-up sent: NZ/AU integration contract readiness, signals move to contract
- Legal inquiries sent to HGM (Andrew Dentice) and Kindrik Partners for AU contract review; scope: review-only, AUD $14-18k/year deal value
- Buddle Findlay selected as primary legal partner (covers 5 areas for full R&D year); Bell Gully and Elevate Medtech deferred
- AU contract approach confirmed: self-draft with AI assistance, review-only legal engagement (proportionate for deal size)
- New task created: medtech-20260423-002 — review lawyer quotes and engage firm, due 30 Apr
- `clinicpro-capture` split into three project files: product (`clinicpro-capture`), AU bundle deal (`clinicpro-capture-au-bundle`), Medtech integration contract (`clinicpro-capture-integration`)
- 10 AU bundle tasks reassigned from `clinicpro-capture` to `clinicpro-capture-au-bundle`
- Vault rule added: project scope check — flag proactively when a project file covers more than one distinct workstream

### Week of 2026-04-14 (continued 19 Apr)
- `/medtech/capture` landing page shipped (Phase 1 Task 1, commit 64788af): 7-section server-rendered page, editorial-clinical aesthetic, Newsreader + IBM Plex Sans + JetBrains Mono, teal-600 accent, mailto CTA, full spec copy
- `/refer-a-practice` bounty page + Resend API route shipped (Phase 1 Task 2, commit 4326d34): $200 credit / 3-months-free referral incentive, smoke-tested end-to-end
- `resend` package added to clinicpro-medtech; RESEND_API_KEY added to .env
- Landing page copy/design review scheduled before champion email send (task medtech-20260419-001)
- AU bundle proposal sent to Lawrence Peterson (CC Alex) ahead of Wed 22 April meeting: AUD 30/active practice/month, 50-practice floor (AUD 18k/year), 3-year term, May-June 2026 launch, AU data residency via Sydney AWS
- Integration-contract scope revised: pulled back 14 April NZ-only line via follow-up email to Alex. Integration contract now covers NZ + AU, sits separate from Lawrence-led AU bundle. Two-contract architecture locked.
- NZ integration commercial position: 15% flat commission (opening ask), 20% fallback, walkaway above 20%. Alex already taking 15% back to her team since 16 Apr call.
- NZ integration strategy doc shipped: `context/medtech-context/clinicpro-capture/clinicpro-capture-medtech-integration-strategy.md`
- AU strategy doc annotated with PMS-only insight: Medtech is the only PMS without a native image capture tool

### Week of 2026-04-14
- Received partnership agreement draft from Alex (13 Apr): reviewed in full including Schedule 1 (fee table extracted via python-docx)
- Schedule 1 confirmed: Commencement Date 18 Mar 2026, Initial Term 36 months, fee structure $10-$60/month per Active Facility by enrolment tier
- Identified three issues with draft: (1) flat fee model not commission-based, (2) no NZ-only geographic scope, (3) PIA/pentest timeline 3 months vs 6 months
- Replied to Alex 14 April: requested commission model, explicit NZ-only scope, and correction of PIA/pentest timeline
- Lawrence Peterson AU thread reviewed: all five commercial questions sent (12-13 Apr); awaiting reply
