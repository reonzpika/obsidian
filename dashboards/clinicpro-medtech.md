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

### Week of 2026-04-21
- Held Wed 22 April meeting with Lawrence Peterson (AU) and Alex Cauble-Chantrenne (NZ)
- AU: Lawrence confirmed strong interest. No objection to AUD 30/practice. Flagged 50-practice minimum too high, taking to boss. Floor is 40 at AUD 30.
- AU: product confirmed as G2M, entirely new software. Same ALEX backend. Capture API available. White-label confirmed. Medtech handling all marketing.
- AU: Lawrence raised management dashboard with tenancy/licence model. Confirmed as out-of-bundle scope, separate one-off build engagement.
- NZ: Alex confirmed 15% flat commission covering NZ + AU direct sales. Default position held, no concession.
- Meeting briefing updated with notes and checklist ticks; pricing table updated with +10k profit threshold per price scenario.
- Task `medtech-20260422-001` created: scope and ideate management dashboard.

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
