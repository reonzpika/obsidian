---
id: nexwave-rd-compliance
status: active
type: rd
repo: nexwave-rd
stack: []
title: "R&D Compliance"
description: "Regulatory and compliance track for NexWave Health."
phase: "Compliance framework scoping"
dashboard: nexwave-rd
---

# Regulatory & Compliance — NexWave Health

| Field | Detail |
|---|---|
| Budget line | Capability Development — Regulatory & Compliance |
| Budget | $18,000 |
| Period | Feb 2026–Jul 2027 |
| MBIE expectation | Gap analyses, DPIA methodology, compliance frameworks — not just consultant invoices |
| Parent dashboard | [[nexwave-rd]] |

---

## Compliance landscape

NZ has no AI-specific legislation. The framework is a patchwork of existing health, privacy, device, and professional regulation. What applies and when depends heavily on whether Inbox Helper is classified as a medical device.

### Essential now: answer first (Obj 1, synthetic data stage)

| Term | What it is | Why it matters now |
|---|---|---|
| **SaMD** (Software as a Medical Device) | International term for software that performs a medical function without being part of a physical device | Core classification question: does Inbox Helper or Care Gap Finder qualify? Determines the entire downstream compliance path |
| **Medicines Act 1981** | NZ's current medical devices law. Does not clearly extend to software. Medsafe has not formally classified assist-only clinical AI | Bell Gully Phase 1 is specifically about whether NexWave tools fall under this Act |
| **Medical Products Bill** | Planned legislation to replace the Medicines Act. Working papers confirm SaMD and AI are being actively considered. Bell Gully: introduction this parliamentary term "increasingly unlikely" due to election proximity | Will likely regulate tools like NexWave when it passes; architecture decisions now should leave room for compliance |
| **Assist-only posture** | Design choice where AI surfaces information only; GP makes all decisions | Directly relevant to SaMD classification risk. Strictly assist-only lowers (but does not eliminate) the risk of device classification |
| **MBIE grant obligations** | Conditions in CONT-109091-N2RD-NSIWKC governing use of grant funds, eligible costs, IP, publicity, co-funding, change of control | Already live; affects tool design decisions (NZ-only R&D, IP ownership, reporting) |

### Required before touching real patient data (Obj 2 trigger)

| Term | What it is | Why it matters |
|---|---|---|
| **Privacy Act 2020** | NZ's principal privacy law governing collection, use, and disclosure of personal information | Applies from the moment any real patient data enters the system |
| **Health Information Privacy Code 2020 (HIPC)** | Stricter rules for health information specifically. 13 rules covering collection, storage, access, and disclosure | All patient-level data processed by Inbox Helper or Care Gap Finder is health information under this code |
| **Privacy Impact Assessment (PIA)** | Structured document analysing how a new system handles personal data, the risks, and mitigations | Both Bell Gully and Buddle Findlay recommended this. NexWave well-placed to draft internally; firms would review. Not legally mandatory but expected by the Privacy Commissioner and any PHO/Health NZ integration partner |
| **Privacy Commissioner AI guidance** | Proactive, evolving guidance on AI systems handling personal data. Not binding law yet | Signals enforcement direction; design decisions now should be defensible against it |
| **HDC Code of Rights** | Health and Disability Commissioner Code giving patients rights over their health care | Applies when the tool is used in a clinical setting. Design must support GPs meeting obligations (e.g. right to information, informed consent) |
| **Health (Retention of Health Information) Regulations** | Prescribes how long health records must be kept (generally 10 years for adults) | Relevant if the tool generates, modifies, or stores any clinical record entries |

### Required before deploying into practices (Obj 3–4 trigger)

| Term | What it is | Why it matters |
|---|---|---|
| **HISO standards** | Health Information Standards Organisation technical standards for NZ health IT systems. Covers interoperability, security, data formats | PHOs and Health NZ contracts typically require compliance; must be baked into tool design |
| **PHO / Health NZ contract obligations** | GP practices contract with PHOs who contract with Health NZ. Back-to-back clauses can impose technical and security requirements on tools used within practices | NexWave tools operate inside PHO-contracted practices; obligations flow through |
| **Health NZ API standards** | Technical standards for connecting to Health NZ systems | Relevant if integration extends beyond ALEX (e.g. NHI lookups, national screening registers) |
| **MCNZ AI guidance (March 2026)** | Medical Council of NZ guidance on using AI in patient care, released March 2026 | Applies to GPs using the tool, not NexWave directly — but design must support GP compliance |
| **ALEX FHIR API licence terms** | Medtech's licence governing access to the ALEX integration layer | Constraints on what data can be extracted, stored, or processed. Flagged by Buddle Findlay as needing formal review |
| **Medtech partnership obligations** | Existing R&D partnership agreement with Medtech | May contain clauses about tool design, data use, exclusivity, or IP that affect compliance posture |

### Commercialisation stage (Obj 4 / post-launch)

| Term | What it is | Why it matters |
|---|---|---|
| **Fair Trading Act 1986** | Consumer protection law covering misleading claims | Marketing claims about accuracy, clinical benefit, and safety must be defensible |
| **IP protection** | Copyright, contractual, and trade secret protections for the tool's code, models, and training data | Worth addressing before sharing extensively with third parties |
| **Licensing / contractual protections** | Standard form agreement covering limitation of liability, data ownership, support obligations for practice customers | Must exist before any commercial deployment |
| **MTANZ Code of Ethics** | Medical Technology Association of NZ voluntary code. Consumer complaints and inter-member dispute mechanisms | Flagged by Buddle Findlay; not urgent. Only relevant if NexWave joins MTANZ or deals with members |

### Watch only

| Term | Status |
|---|---|
| **Medical Products Bill (ongoing)** | Not this parliamentary term (Bell Gully). When passed, likely to require formal SaMD registration and assessment. Monitor; design for eventual compliance |
| **Privacy Commissioner AI guidance (evolving)** | Tightening over time. No binding rules yet |
| **Overseas regulatory regimes** | Buddle Findlay explicitly out-of-scoped. Only relevant if NexWave expands outside NZ |

---

## Sequencing guidance

**Now (Obj 1, synthetic data):**
Commission Bell Gully Phase 1 ($2,500–$4,000). The SaMD classification answer controls everything downstream. The Buddle Findlay landscape overview is already captured in this document — the missing piece is the classification determination.

**Before Obj 2 (real patient data):**
Draft a PIA internally. Both firms confirmed NexWave is well-placed to do this. Budget a brief legal review of the PIA ($1,000–$2,000) before submitting to any Health NZ or PHO integration partner.

**Before Obj 3 (trialling in practices):**
Broader Buddle Findlay engagement. By then you'll have real data flows, a live ALEX integration, and PHO relationships to structure. The compliance picture will be concrete rather than hypothetical.

**Before Obj 4 (commercialisation):**
Full formal assessment: IP, licensing, marketing, contractual protections. Likely the right time for a combined Bell Gully (SaMD/device) + Buddle Findlay (commercial/privacy) engagement.

**On Elevate Medtech (Anne Arndt, back 29 Apr):**
Different layer — computer science and SaMD technical pathway (IEC 62304, ISO 13485, verification and validation). Complements the legal advice; does not replace it.

---

## Firms contacted

| Firm | Contact | Type | Reached out | Status | Proposal |
|---|---|---|---|---|---|
| Bell Gully | Laura Hardcastle (Sr Associate), Kirsty Dobbs | Health law, SaMD specialist | 2026-04-15 | Proposal received 2026-04-16 | Phase 1 $2,500–$4,000 + GST. SaMD obligations under current law plus Medical Products Bill pipeline. Conflict check + 3 AI-output Qs required before proceeding. |
| Buddle Findlay | Catherine Miller (Special Counsel) | Health law firm | 2026-04-07 | Proposal received 2026-04-17 | $9,000–$12,000 + GST + 3.5% service fee (20% R&D discount). Overview across 5 compliance areas: Privacy, System Standards, Professional Regulation, Contract Compliance, Marketing. Optional MTANZ/IP/Medical Products Bill notes. |
| Elevate Medtech | Anne Arndt | SaMD regulatory consultant | 2026-04-08 | Away until 2026-04-29 | Awaiting response |
| Aesculytics | Dr Arindam Bose | Clinical AI + Medsafe consultant | 2026-04-15 | No response | — |
| CARSL | David Smyth | Medsafe sponsor / device registration | 2026-04-08 | Deprioritised | Not relevant — sponsor/registration focus only |

### Combined summary (Bell Gully + Buddle Findlay)

- **No NZ AI-specific legislation.** Core statutory framework is the Privacy Act 2020 + Health Information Privacy Code 2020. Privacy Commissioner is proactively publishing AI guidance.
- **Recommended first step:** Privacy Impact Assessment (PIA). NexWave likely well-placed to draft; firms can review or support.
- **SaMD question is central.** Under the Medicines Act 1981, clarity on whether assist-only clinical AI qualifies as a medical device is limited. The proposed Medical Products Bill is intended to cover SaMD + AI, but Bell Gully views introduction in this parliamentary term as increasingly unlikely given election proximity.
- **System standards:** HISO technical standards, PHO contract obligations (back-to-back with Health NZ funding agreements), Health NZ API standards — all potentially relevant to tool design.
- **Professional regulation:** MCNZ released new AI-in-patient-care guidance March 2026. Health (Retention of Health Information) Regulations, HDC Code of Rights, and recordkeeping obligations all sit on the GP, but tools must support compliance.
- **Contract compliance:** Overlapping obligations from MBIE grant, Medtech partnership, and ALEX FHIR API licence flow through to tool design and licensing.
- **MTANZ Code of Ethics:** Voluntary body with consumer complaints + inter-member dispute mechanisms. Flagged by Buddle Findlay as worth considering.
- **Marketing / Fair Trading Act 1986:** Relevant at trial-pool recruitment and commercialisation, not now.

### Proposal comparison

| | Bell Gully (Phase 1) | Buddle Findlay |
|---|---|---|
| Cost | $2,500–$4,000 + GST | $9,000–$12,000 + GST + 3.5% |
| Scope | SaMD classification + Medical Products Bill | All 5 compliance areas overview |
| Follow-up | Explicit Phase 2 for deeper SaMD advice | Self-directed deep-dives after overview |
| Prerequisites | Conflict check, 3 AI-output Qs answered | None stated |
| Best fit | Primary concern: device classification | Want full compliance landscape map |

### Decision log

| Date | Entry |
|---|---|
| 2026-04-17 | Both proposals in hand. Open question: narrow-and-cheap (Bell Gully) vs broad-and-expensive (Buddle Findlay), or both-in-parallel. Budget envelope $18k across 18 months comfortably covers either; combining both would consume most of the first engagement. Elevate Medtech may add a third view when Anne returns 2026-04-29. |
| 2026-04-20 | Full thread review completed. Bell Gully 3-question answers drafted (Inbox Helper: urgency suggestions only, not prescriptive actions; Care Gap Finder: identifies overdue checks, no treatment recommendations; urgent items: inbox reorder only, no push notifications) — reply pending Ryo sign-off on rd-20260420-002. Aesculytics: no response after 5 days, consider follow-up or deprioritise. Elevate Medtech: await Anne Arndt quote after 2026-04-29 return before deciding on Buddle Findlay. |

---

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
  .where(p => p.project === "nexwave-rd-compliance" && p.status !== "done")
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
