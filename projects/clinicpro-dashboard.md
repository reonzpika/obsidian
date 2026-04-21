---
id: clinicpro-dashboard
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
title: "ClinicPro Dashboard"
description: "GP clinical dashboard centralising missed-action risks."
phase: "API integration and billing module"
dashboard: clinicpro-medtech
---

## Description

GP clinical dashboard centralising three problems that cause GPs to miss critical actions:

1. **Clinical todos** — NLP extracts action items (labs, referrals, radiology) from free-text consult notes. Extracted items written back to ALEX as native tasks via `POST /FHIR/Task`.
2. **Billing completeness** — Detects unbilled ACC procedure codes, nurse involvement, and CSC/HUHC rate mismatches from consult note content and patient demographics.
3. **Inbox triage** — Prioritises lab results, radiology reports, and clinical correspondence by urgency. Radiology NLP (free-text PDF) for abnormality detection; structured Observation interpretation codes for labs.

**Research**: [[Clinical-Dashboard for NZ General Practice]]
**API reference**: [[alex-api-docs]]

## Build order

Billing first, action items second, inbox triage third.

Billing is the simplest NLP problem, generates immediate measurable revenue, and builds clinical trust for the higher-complexity modules.

## Key decisions

- All ALEX calls via BFF (api.clinicpro.co.nz) — never direct from Vercel
- Consult notes are RTF-encoded base64 — decode step required before LLM processing
- Task write-back is bidirectional: extracted action items land in ALEX as native tasks
- Unfiled inbox queue via `GET /FHIR/V2/DiagnosticReport?attentionto={hpi-cpn}` (v2.10)
- Human-in-the-loop required for all AI outputs — NZ regulatory + patient safety
- Billing completeness uses appointment-driven prompting, not invoice auditing — ALEX Invoice API has no patient search; only `?_id=` lookup exists (tested 2026-04-08)
- No dashboard-owned invoice state — prompt is driven by completed appointments for the session; GP confirms billing or creates invoice via write-back

## Open questions / blockers

| Item | Status | Date |
|---|---|---|
| Invoice patient search (`Invoice?subject=Patient/{id}`) | Awaiting Defne response | 2026-04-08 |
| ExplanationOfBenefit endpoint test | Pending — roles granted, not yet tested | 2026-04-08 |
| Task endpoint live test (write-back) | Pending — roles granted, not yet tested | 2026-04-08 |
| Communication endpoint live test (write-back) | Pending — roles granted, not yet tested | 2026-04-08 |

## API status

| Resource | Access | Notes |
|---|---|---|
| Patient + Coverage | Confirmed | CSC and HUHC via `_include=Coverage:patient` |
| DocumentReference | Confirmed | Consult notes — RTF base64 |
| DiagnosticReport (V2) | Confirmed | Labs + radiology; unfiled inbox via `attentionto` |
| Task | Confirmed (docs) | Pending role test |
| Communication | Confirmed (docs) | Inbox messages; pending role test |
| Invoice | Confirmed (limited) | Roles granted 6 Apr. Read by `_id` only — no patient/date search. See billing constraint below. |
| ChargeItem | Confirmed | Roles granted 6 Apr. Returns practice billing catalogue. No patient filter needed. |
| ExplanationOfBenefit | Confirmed (docs) | Roles granted 6 Apr. Pending endpoint test. |
| Appointment | Confirmed (docs) | Queryable by patient NHI + date range + status. Key to billing completeness flow. |

## Billing completeness: API constraint (tested 2026-04-08)

**Critical finding:** The ALEX Invoice API does not support patient-based search. Only `GET /FHIR/Invoice?_id={invoiceId}` works. Queries using `subject=Patient/{id}` or `date=` return 403. This is a documentation gap, not a permissions issue — the endpoint simply does not exist.

**Implication:** The billing completeness module cannot retroactively check if an invoice was raised for a given encounter. Any approach that requires "does an invoice exist for this patient today?" is blocked unless Medtech adds a patient search endpoint (requested via Defne, 2026-04-08).

**Preferred interim architecture — Appointment-driven prompting:**
1. Pull completed appointments for the session: `GET /FHIR/Appointment?actor={provider-id}&date={today}&status=fulfilled`
2. For each appointment, fetch the consult note: `GET /FHIR/DocumentReference?subject=Patient/{id}&date={date}`
3. NLP-extract expected service codes from the consult note (consultation type, procedures, nurse involvement, CSC/HUHC eligibility)
4. Surface a per-patient billing prompt to the GP at end of session: "We found X, Y, Z in this note — confirm billed or create invoice"
5. If GP confirms or writes back via `POST /FHIR/Invoice`, the encounter is resolved
6. No dashboard-side invoice state needed — the prompt is driven by appointments, not by checking existing invoices

This reframes the module from "flag missing invoices" to "prompt billing confirmation after each consult" — better UX and no dependency on a patient Invoice search API.

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
  .where(p => p.project === "clinicpro-dashboard" && p.status !== "done")
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
