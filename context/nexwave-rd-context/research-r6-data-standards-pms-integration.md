---
title: Research R6 — Data Standards and PMS Integration
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-11
status: final
---

# Research R6 — Data Standards and PMS Integration

**Sprint:** 2026-04-rd-sprint-2
**Feeds:** rd-20260329-011 (Data requirements documented)
**Author:** R&D research track (R6, synthesised from R6-A/B/C/D parallel sub-agents, 11 April 2026)
**Cross-references:** [[research-r3-architecture-shortlist]], [[research-r4-care-gap-finder-subtasks]], [[research-r7-open-source-llm-self-hosted]], [[inbox-helper-task-spec]], [[care-gap-finder-task-spec]]

> **Confidence marking convention.** Each substantive claim is one of: **(D)** documented in a primary published source (HISO standard, vendor portal, peer-reviewed paper), **(P)** common NZ practice / industry-validated but not formally standardised, **(I)** inferred from triangulation, or **(U)** not publicly documented and deferred to engagement track.

---

## 1. Executive summary

The data layer for Inbox Helper and Care Gap Finder is **dominated by HL7 v2.4 messages over HealthLink** at the substrate level, **surfaced as a FHIR-shaped REST API by Medtech ALEX** at the integration layer, with **Read v2 + SNOMED CT International + NZULM + LOINC + HISO 10001 + NZDep2018** as the code-set stack and **partner-NDA gates around almost every operationally-significant detail** (rate limits, exact resource shapes, HealthLink envelope, sandbox credentials).

**Headline facts driving Sprint 2 architecture decisions:**

1. **ALEX is FHIR-shaped, not FHIR-conformant.** No public CapabilityStatement; ~261 endpoints across ~25–30 resource families × ~4 ops; Azure AD OAuth client credentials + static IP allowlist mandatory; **no `$export`, no Subscriptions** — everything is pull-based via `_lastUpdated`. The Odin Health precedent (scheduled daily delta pulls on partner tier) is the only public population-scale ALEX consumer. Sandbox is a Medtech-hosted demo practice via facility codes (e.g. `F99669-C` / `F2N060-E` convention), accessed only after MIPP NDA + signed agreement.
2. **Indici (Valentia) is substantially more closed.** No public developer portal, no public OpenAPI, no public CapabilityStatement. Predominantly proprietary REST with selective FHIR mapping. **6–12 weeks** from first contact to sandbox. Sprint 4+ scope; do not plan on Indici technical detail in Sprint 2.
3. **HL7 v2.4 is the substrate.** `ORU^R01` is the dominant inbound message type; `MDM^T02/T04/T08` carries radiology, discharge summaries, specialist letters as **PDF blobs in OBX-5 ED segments**. The ALEX FHIR view is a *rendering* of upstream v2 — detail (Z-segments, OBR/OBX structure, abnormal flag nuance) may be lost in the rendering and matter for urgency triage.
4. **Code-set stack:** SNOMED CT International Edition + HISO NZ reference sets (no separate "NZ Edition" release server); Read v2 unavoidable in Medtech Evolution legacy via NHS England TRUD map; NZULM via ATC prefix membership for medication classes; LOINC universal in lab feeds with dual local-code redundancy; HISO 10001:2017 for ethnicity (with PREDICT-specific highest-risk-wins prioritisation that **inverts** the MoH prioritised output rule); NZDep2018 (Dec 2020) still operational — NZDep2023 not yet released. Detail per variable in §8.
5. **Document mix per practice/day:** ~110 inbox items median (200 p90, **3× post-holiday burst**) for the 2,500-patient median practice, broken down approximately **60% labs / 10% radiology / 7% discharge / 13% specialist letters / 5% portal / 5% other**. Labs are >95% structured HL7 ORU. Radiology is ~25% structured (private) / <10% (public DHB). Discharge summaries are **40–55% structured CDA nationally**, ranging from 70–85% in Auckland metro to 20–50% in rural. Specialist letters and private radiology are dominantly **PDF-over-MDM**.
6. **Care Gap Finder denominators on a 2,500-patient register:** CVDRA priority cohort ~900–1,000; known diabetes ~140–180; hypertension on treatment ~350–450; CKD G3+ ~100–150; smokers ~150–200. Total unique in-scope ≈ **1,800–2,100 of 2,500**. Cold-scan 12,500–15,000 ALEX calls; weekly delta 2,000–3,500; daily delta ~500. At the conservative APIM 5 req/s default, cold scan is **~50 minutes** wall-clock. R4-D architecture decisions hold.
7. **Cost headline:** combined Inbox Helper + Care Gap Finder on Claude Haiku 4.5 via Bedrock (Sydney pricing as proxy for ap-southeast-6) is **NZD 6–10/month/practice**. Self-hosted Llama 3.3 70B is **uneconomic single-tenant** (~NZD 2,000–2,500/month/practice); pooled break-even vs Haiku is **~200 practices**, not ~50. Fine-tuned BioClinical ModernBERT 396M shared is **NZD 0.50–1.50/month/practice** if accuracy bar is met. **The architecture-side cost risk for Sprint 2 is not LLM inference — it is infrastructure, support, and compliance overhead.**
8. **The strategic ALEX opening holds.** No competitor (Health Accelerator RPA, Medtech AI, Inbox Magic, BPAC CS) is currently using the ALEX FHIR API for AI-driven inbox triage — they are screen-scraping, RPA, native first-party, or rule-based. ALEX is a structural opening for NexWave but every per-resource search-parameter and rate-limit detail must be flagged "to be confirmed against CapabilityStatement on partner onboarding".

**Most important Sprint 2 deliverable consequence:** the Sprint 2 data-requirements document (rd-20260329-011) must (a) treat every ALEX-dependent design assumption as provisional pending MIPP onboarding, (b) carry the variable-by-variable mapping table from §8 as the authoritative artefact for downstream Sprint 3 implementation, and (c) escalate the open questions in §11 onto the Lisa Pritchard / HISO / Te Whatu Ora / Catalyst Cloud engagement track.

---
## 2. Medtech ALEX FHIR API — deep dive

### 2.1 Overall posture

Medtech's **ALEX FHIR API** is the only first-party, FHIR-shaped, vendor-supported route into a Medtech Evolution / Medtech32 practice database. It is **partner-gated**: the developer-portal surface that is publicly crawlable is thin (marketing plus a "Become an Integration Partner" contact form); the substantive material — OpenAPI / Swagger, resource-by-resource search-parameter tables, CapabilityStatement, sandbox credentials, rate-limit SLAs, audit-event schema — sits behind an ISV NDA and the **Medtech Integration Partner Programme (MIPP)** onboarding.

For Sprint 2 architecture purposes, the following can be treated as **documented fact** from Medtech's public pages, HISO/HINZ conference content, and the Odin Health partner precedent:

- ALEX is a **REST-over-HTTPS API with FHIR-shaped resources** (FHIR R4-aligned, not a fully conformant R4 server — no public CapabilityStatement). **(P)**
- Authentication is **Azure AD OAuth 2.0** against a Medtech-owned tenant, with **static-IP allowlisting required** on top of OAuth. **(D)**
- Endpoint breadth is approximately **261 path+verb combinations across ~25–30 resource families**, decomposing as ~25–30 resource families × ~4 ops (read, vread, search, history) ≈ 100–120 FHIR endpoints, plus Medtech-specific custom operations and admin endpoints. **(P, from MIPP partner material cited in R4-D)**
- **No `$export`** (FHIR Bulk Data) and **no FHIR Subscription** support. Everything is pull-based, keyed off `_lastUpdated`. **(P)**
- Sandbox is via **dummy-practice facility codes** in a Medtech-hosted demo practice; the `F99669-C` / `F2N060-E` references are consistent with the Medtech training-facility naming convention but cannot be verified from public sources. **(I)**

> **The absence of a public `GET /metadata`** strongly suggests ALEX is FHIR-shaped rather than strictly FHIR-conformant. A conformant FHIR R4 server **MUST** expose `/metadata`. If ALEX does not, it cannot claim R4 conformance, only R4 alignment. This is the single most important question to put on the Medtech engagement track.

### 2.2 Versions and roadmap

| Version | Status | Confidence |
|---|---|---|
| ALEX v2.x (pre-2.10) | Deprecated for new integrations | (P) MIPP partner-disclosed |
| **ALEX v2.10** | Cited as current at time of R4-D research | (P) partner material |
| v2.11+ roadmap | No public roadmap; no `$export` planned | (U) |

**Action for Sprint 2:** confirm the GA version as of April 2026 directly with Medtech via Lisa Pritchard / MIPP — 12+ months have passed since the v2.10 figure was cited.

### 2.3 Sandbox / UAT

- Sandbox = a **hosted Medtech Evolution demo practice** pre-populated with synthetic patients, not a separate FHIR sandbox server. The FHIR endpoints point at this dummy practice's database. **(P)**
- Access requires NDA + signed MIPP agreement. Credentials (client ID, client secret, facility code, allowlisted IP) are issued per partner. **(P)**
- Sandbox is **not performance-representative** — it is a small single-practice footprint. Rate-limit, pagination, and delta-pull behaviour will differ materially from production at scale. **(I)**
- Synthetic-patient corpus is believed to include realistic NZ demographic shape (NHI format, DOB ranges, ethnicity codes), NZPOCS-structured lab results, and Read v2-coded problem lists, but exact composition is partner-NDA. **(I)**

### 2.4 MIPP onboarding lifecycle

| Step | Typical lead time | Source |
|---|---|---|
| Initial contact via `partners@medtechglobal.com` or website form | — | (D) public marketing |
| Qualification call | days–1 week | (P) HINZ panel content |
| NDA signing | 1–2 weeks | (P) partner anecdotal |
| MIPP commercial agreement | 2–4 weeks | (P) tiered standard / preferred / strategic |
| Sandbox credentials issued | 2–4 weeks (cumulative) | (P) HINZ 2023/24 |
| Sandbox → production certification | 4–12 weeks | (P) depends on partner readiness; no published SLA |
| Per-practice production enablement | per-practice support touchpoint | (P) — see §2.7 |

**Fee structure** is tier-dependent and partner-NDA. Believed to include an annual partner fee plus per-practice or per-call metering at higher tiers.

### 2.5 ALEX FHIR resource coverage (provisional)

The table below distinguishes **(D)** documented from public Medtech / HISO / HINZ material, **(I-likely)** inferred-likely from MIPP-advertised use cases, **(I-uncertain)** inferred-uncertain, and **(NDA)** partner-NDA only for per-resource search-parameter, interaction, and `_include` detail.

| Resource | Status | Likely endpoint | Key search params (inferred) | Notes |
|---|---|---|---|---|
| `Patient` | (D) | `/Patient/{id}`, `/Patient?...` | `identifier` (NHI), `name`, `birthdate`, `gender`, `_lastUpdated` | NHI primary identifier; practice patient ID as secondary |
| `Practitioner` | (D) | `/Practitioner` | `identifier` (HPI-CPN), `name` | HPI-CPN is the NZ practitioner identifier |
| `PractitionerRole` | (I-likely) | `/PractitionerRole` | `practitioner`, `organization` | Uncertain whether modelled separately or embedded |
| `Organization` | (D) | `/Organization` | `identifier` (HPI-FAC / facility code) | The practice itself; facility code is the key |
| `Encounter` | (D) | `/Encounter` | `patient`, `date`, `practitioner`, `_lastUpdated` | Consultation records |
| `Condition` | (D) | `/Condition` | `patient`, `code`, `clinical-status`, `_lastUpdated` | SNOMED on Evolution; **Read v2 legacy** on MT32-migrated records |
| `Observation` (lab) | (D) | `/Observation?category=laboratory` | `patient`, `code` (LOINC/NZPOCS), `date` | NZPOCS codes appear alongside LOINC |
| `Observation` (vitals) | (D) | `/Observation?category=vital-signs` | `patient`, `code`, `date` | BP, weight, height, HbA1c, etc. |
| `DiagnosticReport` | (D) | `/DiagnosticReport` | `patient`, `code`, `date`, `status` | Wraps lab Observations |
| `MedicationRequest` | (D) | `/MedicationRequest` | `patient`, `code`, `status`, `authoredon` | NZULM / NZMT codes |
| `MedicationStatement` | (I-likely) | `/MedicationStatement` | `patient`, `status` | May be derived from MedicationRequest, not first-class |
| `MedicationDispense` | (I-uncertain) | `/MedicationDispense` | — | Dispense lives in NZ ePrescription Service, not GP PMS |
| `AllergyIntolerance` | (D) | `/AllergyIntolerance` | `patient`, `code`, `clinical-status` | First-class in Evolution |
| `Immunization` | (D) | `/Immunization` | `patient`, `vaccine-code`, `date` | Feeds AIR (Aotearoa Immunisation Register) |
| `DocumentReference` | (D) | `/DocumentReference` | `patient`, `type`, `date` | **Inbox items — central to Inbox Helper** |
| `FamilyMemberHistory` | (I-uncertain) | `/FamilyMemberHistory` | — | Medtech models family hx as free-text more often than structured FMH; exposure uncertain — **critical gap for Care Gap Finder** |
| `Procedure` | (I-likely) | `/Procedure` | `patient`, `code`, `date` | In-practice procedures |
| `CarePlan`, `Goal` | (I-uncertain) | — | — | Medtech has a care-plan module; FHIR exposure unknown |
| `Coverage` | (I-likely) | `/Coverage` | `patient`, `status` | Enrolled / VLCA / CSC subsidy status |
| `Appointment`, `Schedule`, `Slot` | (D / I-likely) | `/Appointment`, `/Schedule`, `/Slot` | `patient`, `practitioner`, `date` | Booking data |
| `ServiceRequest` | (I-likely) | `/ServiceRequest` | `patient`, `code`, `status` | Referrals to specialists, lab requests |
| `Communication`, `CommunicationRequest` | (I-uncertain) | — | — | Secure messaging typically bypasses ALEX (HealthLink direct) |
| `Group` | (I-uncertain) | `/Group` | — | Medtech has practice "patient groups" / recall lists; FHIR `Group` exposure unknown — **matters for Care Gap Finder cohort sync** |
| `RelatedPerson` | (I-likely) | `/RelatedPerson` | `patient` | NOK / caregiver contacts |

**Partner-NDA only for all rows:** exact HTTP verbs (vread? history? patch?), `_include` / `_revinclude` support, chained search support, token-system constraints, response cardinality limits, pagination defaults, gaps from canonical R4 (does `Patient.contact` round-trip? does `Observation.component` support multi-component BP?).

### 2.6 Authentication, tenancy, rate limits

| Item | Status | Detail |
|---|---|---|
| OAuth flow | (P) | **Client credentials** (partner BFF → ALEX). No authorization-code; no end-user browser. |
| Scopes | (NDA) | Believed resource-family scoped (`Patient.Read`, `Observation.Read`, etc.). **Open question:** SMART-on-FHIR scopes (`patient/*.read`, `user/*.read`) supported? |
| Token lifetime | (NDA) | Standard Azure AD app token is 60–90 min; Medtech may have customised |
| Static IP allowlist | (D) | Required in addition to OAuth ("defence in depth"). Hard constraint on BFF egress architecture — **NAT Gateway / fixed-IP egress mandatory.** No mTLS / IP-less alternative known |
| Rate limits | (NDA) | Per-partner global ceiling, per-practice soft limit, burst vs sustained. APIM-default-style 5 req/s is the working assumption; not confirmed |
| `$export` | (D — absent) | Not supported on v2.10. No public roadmap |
| Subscriptions / webhooks | (D — absent) | Not supported. Pull-based only via `_lastUpdated` |
| Latency (p50/p95) | (I) | p50 single-resource read 150–400 ms; p95 800 ms – 2 s; `_lastUpdated` delta on Observation multi-second, pagination-dominated |

**Architectural implication** (locked in R4-D, restated here): the partner BFF must have a **stable, small set of egress IPs**. Freshness SLA is bounded by partner pull cadence; for Inbox Helper a 15-minute delta-pull cadence is the practical minimum without rate-limit pressure.

### 2.7 Per-practice enrolment

ALEX integrations require **per-practice enrolment**, not bulk partner-tenant access. The workflow:

1. Practice signs a data-sharing agreement with the ISV partner.
2. Practice contacts Medtech support (or uses Evolution admin console) to enable the partner integration for their facility code.
3. Medtech provisions the partner's OAuth client with access scoped to that facility.
4. Partner can pull data for that facility.

**Operational consequence:** every practice onboarding is a Medtech support touchpoint, not self-service. This is an operations-cost factor for the Care Gap Finder / Inbox Helper rollout — budget for it explicitly in commercial planning.

### 2.8 Practice-administrator console visibility

**Open question.** It is unclear whether Medtech Evolution's admin console shows a practice administrator which ISV partners are pulling which data. If it does not, the partner has an **implicit obligation** to provide that visibility itself (practice-facing dashboard or regular report). This is a Sprint 3 UX question and a Sprint 2 budget item.

---
## 3. Indici (Valentia Technologies) — deep dive

### 3.1 Vendor and product

- **Valentia Technologies** — Palmerston North, NZ. Founder Mayur Patel. NZ-incorporated, with development presence in India.
- **indici** — cloud-native GP PMS launched ~2015, gaining share from Medtech especially in greenfield deployments and some large practice groups. Positioning is cloud-first / multi-tenant / "modern" vs Medtech's client-server heritage.
- **Market share (April 2026):** Medtech Evolution / Medtech32 still holds the **plurality** of NZ GP practices (~60–70% by HINZ surveys); **Indici** holds 15–25% growing; MyPractice / Profile (Intrahealth) / others make up the remainder. Indici over-indexes in larger urban practices, practice groups that migrated for cloud reasons, and greenfield practices. **(P)** Exact figures are vendor-disputed and shift annually — cite HINZ Market Survey rather than either vendor's own claim.

### 3.2 Developer access

| Item | Status |
|---|---|
| Public developer portal | **None publicly known.** No `developer.indici.health` or equivalent |
| Public API docs | **None.** Integration partnership-gated |
| Postman / OpenAPI | **Partner-NDA only** |
| FHIR conformance | (P) Stated FHIR support intentions in HINZ material; **actual exposed API is predominantly proprietary REST**, not a FHIR-conformant server. FHIR is a selective mapping layer on top of the internal model |
| CapabilityStatement | None public |
| Authentication | (NDA) Believed OAuth 2.0 + API key. IP allowlist may not apply (cloud-native architecture) |
| Sandbox | (NDA) Likely a dedicated tenant rather than facility code in shared instance |

### 3.3 Differences from ALEX (side-by-side)

| Dimension | ALEX (Medtech Evolution) | indici (Valentia) |
|---|---|---|
| Underlying problem-list code system | SNOMED CT on Evolution; **Read v2 legacy** on MT32-migrated records | **SNOMED CT native** (greenfield, no Read v2 legacy) |
| Medication codes | NZULM / NZMT | NZULM / NZMT |
| API shape | FHIR-shaped REST | Proprietary REST + selective FHIR mapping |
| Authentication | Azure AD OAuth + static IP allowlist | (NDA) likely OAuth + API key |
| Hosting | Mixed — see §10 | Cloud-native single architecture (believed NZ / AU) |
| Developer portal surface | Thin public, gated main | None public |
| Sandbox | Facility code in demo practice | Tenant-based |
| `$export` | Not supported | Unknown |
| Subscriptions / webhooks | Not supported | Unknown |
| Public ISV precedent | Odin Health | None known |

### 3.4 Sprint 4+ engagement plan

**Realistic 6–12 week timeline** from first contact to sandbox credentials:

| Week | Activity |
|---|---|
| 0 | First contact via `info@valentia.co.nz` or Mayur Patel (LinkedIn). State: NZ-sovereign clinical AI R&D, MBIE-funded, assist-only Care Gap + Inbox tools, looking for data-access partnership |
| 1–2 | Qualification call with Valentia commercial team |
| 2–4 | NDA signing |
| 4–8 | Technical briefing, API docs, sandbox credentials |
| 8–12 | ISV agreement, production path discussion |

**Pre-requisites before contact:**
- Signed MBIE R&D agreement (evidence of legitimate R&D funding)
- Named clinical use case (Care Gap Finder + Inbox Helper, scoped, assist-only)
- Data-handling statement compatible with HIPC 2020 + Privacy Act 2020
- **At least one clinical champion at a Valentia customer practice willing to be the pilot site** — this is often the unlock, because Valentia's commercial incentive is to support customers' workflows, not be a data-broker for external ISVs

### 3.5 Sprint 2 implication

**Sprint 2 should not plan on any indici technical detail beyond what is in this section.** Treat indici as Sprint 4+ scope. The Sprint 2 deliverable for rd-20260329-011 should explicitly flag indici support as deferred and contingent on Sprint 4 partnership engagement.

### 3.6 Historical and competing access paths (Medtech, briefly)

- **Medtech32 ODBC / MT32 SOAP API:** deprecated for new integrations; ODBC actively discouraged on data-governance grounds. Some legacy analytics and billing integrations still run on ODBC at individual practices but it is not a viable greenfield pattern.
- **HL7 v2 outbound mirror:** some practices run an HL7 v2 outbound feed for backups/analytics, typically to HealthLink or a PHO data warehouse. Bilateral per-practice; not viable as a primary partner feed.
- **BPAC CareSuite / bestpractice Decision Support:** runs as a plugin inside Medtech Evolution, reading local patient context at point of care. **Does not expose a third-party API for external ISVs.** Not viable as an integration intermediary.

---
## 4. HL7 v2 in NZ primary care

NZ general practice runs on **HL7 v2.4** in production (with v2.3.1 fallback for some legacy lab interfaces and v2.5 emerging only in newer lab and Te Whatu Ora pilots). FHIR is additive, not a replacement. The ALEX FHIR view is a *rendering* of upstream HL7 v2 — detail (Z-segments, OBR/OBX structure, abnormal flag nuance) may be lost in the rendering and matter for urgency triage.

### 4.1 Inbound message types

| Msg type | Trigger | Typical content | Sender → GP | Volume class |
|---|---|---|---|---|
| `ORU^R01` | Unsolicited observation result | Discrete lab results: OBR per panel, OBX per analyte with LOINC or local code, units, reference range, abnormal flag | Community labs (Awanui, Pathlab, Medlab Central), DHB labs (LabPLUS, CHL), some imaging providers | **Dominant — majority of inbox messages** |
| `MDM^T02` | Original document notification | Clinical document: radiology report, discharge summary, specialist letter. Body in OBX-5 as `TX` / `FT` / **`ED` (encapsulated base64 PDF)** | DHB radiology, DHB discharge systems, private specialists via HealthLink, private radiology | Very high — second to ORU |
| `MDM^T04` | Document status change with content | Addendum or amended version of an earlier MDM | Same | Moderate |
| `MDM^T08` | Document content replacement | Corrected radiology / discharge | Radiology + DHB systems | Low–moderate |
| `REF^I12` | Patient referral | Inbound referral or referral acknowledgement | Hospital outpatients, private specialists, allied health | Moderate |
| `ADT^A01/A03/A04/A08` | Admit / discharge / outpatient / demographic update | Te Whatu Ora event notifications (where district sends to primary care) | Te Whatu Ora districts | Low–moderate, district-dependent |
| `ORM^O01`, `OML^O21`, `OMG^O19` | Order messages | Outbound only — GP → lab/imaging/hospital | N/A | N/A inbound |
| `DFT^P03` | Financial transaction | Effectively absent from NZ GP inbox; PHO capitation does not flow as HL7 | — | Negligible |

### 4.2 Inbox flow — what an Inbox Helper actually sees

1. HealthLink HMS / HCN client on the GP workstation polls the HealthLink Online Mailbox (or receives via the HealthLink Connect appliance).
2. Message is unwrapped from the HealthLink envelope and written to a local drop folder.
3. Medtech's integrator (formerly MT-Inbox, now the Evolution integration service) parses the HL7 and inserts the document into the patient's record and into the **Inbox** (provider unfiled results queue).
4. For `ORU^R01`, discrete OBX rows are filed into the results table and rendered into a human-readable result document.
5. For `MDM^T02` with embedded PDF, the PDF is extracted to the patient's document store and only the cover metadata (date, sender, title) is in discrete fields.

**Consequence for Inbox Helper:** the message arriving from ALEX FHIR is a post-processed representation. We get whatever Medtech exposed as `DocumentReference` / `DiagnosticReport` / `Observation`. The raw HL7 is upstream and **not always round-trippable from the FHIR view** — design assumption: lossy rendering is the norm.

### 4.3 NZ-specific HL7 v2 conventions

**NHI in PID-3.** Convention across NZ labs and DHBs:

```
PID|1||ABC1234^^^NHI^NHI||SURNAME^GIVEN||19700101|M|||11 EXAMPLE ST^^CITY^^1010^NZ
```

- PID-3 carries NHI with assigning authority `NHI` and identifier type code `NHI` (or `PI` in older feeds). Some senders use `NZL` as namespace ID.
- **Two NHI formats coexist**: legacy 3-alpha + 4-numeric (e.g. `ABC1234`); new extended 3-alpha + 2-numeric + 2-alpha (introduced 2019 to extend the namespace).
- Check-digit is **not** in the 7-character NHI itself — NHI validation uses a mod-11 check on a derived integer representation per **HISO 10046**. Parsers must accept both formats and validate via the HISO 10046 algorithm.
- Local patient IDs (DHB MRN, lab LIS ID) appear as additional PID-3 repetitions with different assigning authority strings (e.g. `1234567^^^ADHB^MR`).

**Ethnicity — two patterns:**
1. **PID-22** (Ethnic Group) populated with HISO 10001 level-2 codes as a repeating field — HL7 standard location, used by most DHB systems.
2. An **HL7-NZ Z-segment** (historically `ZPD`) carrying a richer NZ ethnicity record (up to 6 responses, prioritised, with source flags) — less common in labs but appears in some DHB PMS-to-PMS feeds.

**Address (PID-11)** uses `XAD` data type. NZ practice populates street, suburb, city, postcode, country (`NZ` or `NZL`). **Meshblock / SA1 / NZDep are not routinely carried in HL7 v2** — these are derived downstream by geocoding (see §6.6, §8 NZDep mapping).

**NZ Z-segments (observed, no canonical published list):**

| Z-segment | Usage | Notes |
|---|---|---|
| `ZPD` | Extended patient demographic (NZ ethnicity detail, country of birth, iwi affiliation) | Not universal; some DHB ADT feeds only |
| `ZAL` | Alert / warning (legacy allergy alert before `AL1`/`IAM` standardised) | Some labs still emit |
| `ZNZ` | Sender-specific Z for NZ-only extension fields | Vendor-specific, not canonical |
| `ZCT` | Lab control / clinical trial flag | Awanui / legacy Medlab |

**Parser rule:** treat unknown Z-segments as pass-through metadata — never fail on them, log them, keep a provider-keyed catalogue of ones seen.

### 4.4 NZ lab provider conventions

NZ lab provision is heavily consolidated under **Awanui Labs** (which absorbed SCL, Southern Community Labs, Northland Pathology, Labtests Auckland under the Awanui brand from 2022 onward). **Pathlab** (BoP/Waikato) and **Medlab Central** (Palmerston North) remain independent community providers. **DHB labs** (LabPLUS at Te Toka Tumai Auckland, Canterbury Health Laboratories) feed secondary-care results and, in some regions, community results.

| Provider | Region / role | HL7 ver | HbA1c units | Sender ID (MSH-4) | Quirks |
|---|---|---|---|---|---|
| **Awanui Auckland** (ex-Labtests) | Auckland metro community | v2.4 | IFCC primary; DCCT % may appear as secondary OBX | `LABTESTS` legacy → `AWANUI-AKL` | Local analyte codes; partial LOINC mapping in OBX-3 component 3 |
| **Awanui Wellington** (ex-SCL Wellington / Aotea) | Wellington community | v2.4 | IFCC | `SCL-WGN` / `AWANUI-WGN` | Long-standing SCL OBX catalogue; reference ranges in OBX-7 as `<4.0` or `4.0-6.0` |
| **Awanui Southern** (ex-SCL Dunedin/Invercargill) | Otago / Southland | v2.4 | IFCC | `SCL-DUN` / `AWANUI-DUN` | Shared LIS with Wellington |
| **Pathlab BoP/Waikato** | Waikato, BoP, Lakes | v2.4 | IFCC | `PATHLAB` | Generally cleaner LOINC mapping than Awanui legacy |
| **Medlab Central** | MidCentral / Palmerston North | v2.3.1 / v2.4 | IFCC | `MEDLAB` | **Older v2.3.1 still in some pipelines — fewer fields, shorter messages.** Parser must handle v2.3.1 fallback |
| **LabPLUS** (Te Toka Tumai Auckland DHB) | Secondary-care + esoteric tests | v2.4 | IFCC | `LABPLUS` | Esoteric and genetics results often as narrative `TX` OBX, not discrete |
| **Canterbury Health Laboratories (CHL)** | Canterbury DHB (community + hospital) | v2.4 | IFCC | `CHL` | Own local code system; LOINC partial. CHL does community work in Canterbury — unusual vs other districts |

**Consistent across providers:**
- HL7 v2.4 is dominant; v2.3.1 fallback for Medlab Central legacy.
- HbA1c in IFCC mmol/mol mandatory since the 2011 national switch; DCCT % only as additional derived OBX.
- Abnormal flags in OBX-8 follow HL7 table 0078 (`N`, `L`, `H`, `LL`, `HH`, `A`).
- Reference ranges in OBX-7 as free text.
- Units in OBX-6 — usually UCUM-compatible but not guaranteed.

**Parser must special-case:**
- **OBX-3 code systems** — every provider has its own local code catalogue; LOINC inconsistently populated in second triplet. **Maintain a sender-keyed local-code → canonical-analyte map.**
- **Panel grouping** — some send one OBR per test, others bundle a full profile under one OBR with many OBXes. Downstream "results per OBR" logic must handle both.
- **Narrative vs discrete** — esoteric results (genetics, immunology) often arrive as narrative `TX` OBX under a single OBR. Discrete extraction fails; inbox AI must fall back to text processing.
- **Corrected results** — OBR-25 result status (`C` corrected, `F` final, `P` preliminary) usage varies; corrections sometimes come as a new message with the same filler order number rather than a correction flag.
- **Sender identifier churn** during the Awanui consolidation — same physical lab may have multiple MSH-4 values in your historical corpus. **Build a sender-alias table.**

### 4.5 Document type structure summary

| Document type | Format on the wire | Structured? | Inbox Helper handling |
|---|---|---|---|
| Lab results (community + DHB) | `ORU^R01` HL7 v2.4 with OBR/OBX | **>95% structured** for chemistry/haematology; ~85% microbiology; ~30% histopathology; ~40% cytology; ~20% genetics | Discrete values available — LLM only needed for narrative OBX (interpretive comments, histology). **Materially lower token cost than naive full-document approach** (~1–5% of token budget) |
| Radiology — private (Pacific, ARG, Mercy, TRG, Bay, Hamilton) | `ORU^R01` with `TX` narrative OBX, **or** PDF-over-MDM | **~25% structured** (BI-RADS for mammography, CTPA, lung screening); rest free-text | LLM reads full report (~800–1,500 tokens) |
| Radiology — public DHB | PDF-over-MDM via HealthLink | **<10% structured** | LLM reads full report; OCR fallback for image-only PDFs |
| Discharge summaries | `MDM^T02` carrying PDF (or RTF) in OBX-5 ED, transported over HealthLink | **40–55% structured CDA nationally** (Auckland metro 70–85%; rural 20–50%); rest PDF-over-MDM | PDF text extraction + section detection (regex / LLM) |
| Specialist letters — public DHB | `MDM^T02` with dictated-and-transcribed free-text body; rare structured | **<10% structured** | LLM reads full text; high-value urgency content (e.g. "awaiting urgent biopsy", "commence treatment within 2 weeks") |
| Specialist letters — private | PDF over HealthLink SmartForms or MDM envelope | Free-text | OCR fallback for older rooms producing image-only PDFs |
| Patient portal messages | ManageMyHealth / MyIndici / ConnectMed proprietary | Free-text | LLM reads full text; tail-risk for missed urgent content |

**Image-only PDFs.** Medtech and Indici **do not routinely OCR** inbound PDFs. Text-layer PDFs (the majority of electronically produced clinical letters) are handled via text extraction at display time; image-only PDFs (scanned fax-to-email, old dictation workflows) sit as opaque blobs in the document store. **Any inbox AI that wants to work on these must run its own OCR pipeline** as a first-class component, not an afterthought.

### 4.6 HealthLink — the secure messaging substrate

HealthLink (owned by **Clanwilliam Group**) is the **near-monopoly** secure messaging carrier between NZ healthcare providers. The envelope wraps an HL7 v2 payload with routing metadata: source (HPI-ORG / EDI account), destination, message type+subtype, and a content block that is the HL7 v2 message as a blob (or an HMS "SmartForm" XML, or a generic file attachment).

**HealthLink envelope documentation is partner-portal only** — HealthLink EDI partners receive specification documents under NDA. There is no fully public versioned spec comparable to HL7 IGs.

**For our parser**, by the time Medtech or Indici has processed the message, the envelope is gone and we see HL7 v2 (or a PDF / HTML blob). The HealthLink envelope is invisible to us via ALEX FHIR. If we ever consume at the mailbox level, the envelope format must be obtained via HealthLink partner agreement.

**HealthLink SmartForms** is the structured-form layer for outbound flows (eReferrals, ACC forms, outpatient bookings). Outbound only — GP → hospital — and out of scope for inbox urgency triage on the receive side.

**Alternatives** (mostly not viable as inbound feeds):
- Connected Care / TestSafe / HealthOne / Your Health Summary — shared care records, queryable repositories, **not** messaging carriers / inbox sources.
- Direct fax — residual but diminishing; fax-to-email gateways create scanned PDFs that land in inbox — worst case for automated triage (no HL7, no text layer).
- SimpleSend / direct email — informal; not a sanctioned clinical messaging channel.

---
## 5. FHIR AU/NZ Profile Status — April 2026

### 5.1 HL7 NZ FHIR profiles

HL7 NZ hosts its FHIR work at `confluence.hl7.org.nz` and in its GitHub organisation. Current state:

- A **draft NZ Base IG** exists with profiles for `Patient`, `Practitioner`, `PractitionerRole`, `Organization`, `Location`, and a handful of clinical resources. **Status: draft / trial use, not normative.**
- The NZ `Patient` profile **requires** NHI as an identifier with a defined system URL, **supports** an ethnicity extension bound to HISO 10001 level-2, and **supports** an optional NZDep extension.
- `DocumentReference` and `Observation` profiles exist in draft form but are thin; they do not fully constrain code-system bindings for NZ lab catalogues.
- **Production uptake is limited** — most NZ FHIR APIs (including ALEX) use vanilla R4 with NZ-specific extensions rather than strict conformance to HL7 NZ profiles.

### 5.2 HISO FHIR work

HISO's approved-standards list is HL7 v2 / CDA / ethnicity / NHI heavy. **As of April 2026, HISO has not published a normative FHIR implementation guide for primary care, CVDRA, eDischarge, or immunisation.** FHIR work is being coordinated with HL7 NZ and Te Whatu Ora's digital team but has not produced HISO-stamped normative artefacts.

### 5.3 AU Core as de facto fallback

Because NZ lacks a complete, widely-implemented FHIR Core IG, NZ implementers frequently look to **AU Core** (Sparked / HL7 Australia) as a reference profile set. AU Core is mature, actively maintained, and covers the same primary-care resources. NZ implementations typically:

- Start from AU Core structure definitions
- Swap identifier system URLs for NHI
- Swap ethnicity extensions to HISO 10001
- Relax bindings that reference AU-specific code systems (IHI, Medicare, PBS)

This is **de facto, not standards-endorsed**. AU eRequesting is a relevant adjacent standard but NZ has no current primary-care e-ordering FHIR standard.

### 5.4 NHI FHIR identifier system URL

The canonical NHI system URL used by HL7 NZ and NZ FHIR implementers is `https://standards.digital.health.nz/ns/nhi-id` (with equivalent legacy forms under `health.govt.nz`). Historic OIDs for NHI persist in CDA work; the HTTP-form URL is preferred for FHIR. **A robust inbox parser must accept both.**

### 5.5 FHIR resource-by-resource summary for NZ primary care

| Resource | NZ production convention | Code system binding | Gap from vanilla R4 |
|---|---|---|---|
| `Patient` | NHI primary identifier; HISO ethnicity extension | NHI system URL; HISO 10001 | HL7 NZ Patient profile is draft; vanilla R4 + extensions in practice |
| `Observation` (lab) | Pathology result with local code + optional LOINC | LOINC where available, local lab code otherwise | No NZ-enforced LOINC binding; local codes dominate |
| `Observation` (vital) | BP, pulse, weight, BMI, smoking status | LOINC for vitals; SNOMED CT for qualifiers | Generally vanilla R4 vital-signs profile |
| `Condition` | GP problem list | **Read v2 widespread (Medtech legacy)**; SNOMED CT in newer systems | Large Read v2 legacy — not FHIR-native |
| `DiagnosticReport` | Lab panel-level report | LOINC panel codes inconsistent | Often wraps narrative + Observations |
| `MedicationRequest` | GP prescription | NZULM | NZULM IDs widely used, not necessarily in FHIR-canonical form |
| `Encounter` | GP consultation | SNOMED for reason | Often thin |
| `DocumentReference` | Inbox PDF / letter / discharge summary | Local document type codes | The main carrier for MDM-derived inbox documents |
| `AllergyIntolerance` | GP-entered allergy | SNOMED CT substance where possible | Free-text tail is large |
| `Immunization` | NIR-sourced vaccinations | NZ vaccine code set | NIR integration; FHIR profile draft |
| `FamilyMemberHistory` | GP-entered family history | SNOMED CT for conditions | Sparse; quality varies |

### 5.6 NZ FHIR terminology service

Te Whatu Ora / HISO operate a **NZ Terminology Service** (built on Snowstorm) hosting SNOMED CT NZ Edition. Public-facing FHIR terminology endpoints (`ValueSet/$expand`, `CodeSystem/$lookup`) have been discussed and partially deployed, but **full public access is licensed/credentialed, not open internet**. A fully public, unauthenticated NZ FHIR terminology endpoint equivalent to AU's NCTS is **not publicly documented as GA** in April 2026. R&D programmes likely need credentialed access — open question for HISO engagement.

### 5.7 Implications for the inbox parser

- **Do not assume strict HL7 NZ FHIR conformance.** Vanilla R4 + NZ extensions is what production ALEX FHIR returns. Write parsers that tolerate the gap.
- **Identifier matching must accept both NHI URL forms** (HTTPS canonical + legacy OID).
- **Ethnicity extensions** may use HL7 NZ's pattern or a Medtech-specific extension URL — accept both, normalise to HISO 10001 level-2 internally.
- **Code-system bindings are lenient** — `Observation.code` may carry only a local lab code, no LOINC. Plan a normalisation layer (see §6.5 LOINC).

---

## 6. NZ Clinical Code Sets Reference

### 6.1 SNOMED CT — international edition + HISO reference sets

- **There is no separately released "SNOMED CT NZ Edition" with its own release server.** NZ uses the **SNOMED CT International Edition** as the substrate, plus **HISO-curated NZ reference sets** (refsets) layered on top for NZ-specific subsets (priority conditions, smoking status, ethnicity, NZ-specific qualifiers).
- Distribution: HISO / Te Whatu Ora terminology team, via the NZ Terminology Service (Snowstorm-based, credentialed). International release every 6 months (1 Apr / 1 Oct).
- Licensing: NZ is a SNOMED International member country — **free for NZ-affiliate use**, including for R&D programmes registered with the NZ National Release Centre.
- For NexWave: pin the SNOMED release version in code; refsets for diabetes, CVD, hypertension, smoking are the building blocks for Care Gap Finder denominators.

### 6.2 Read v2 — unavoidable legacy in Medtech Evolution

- **Medtech Evolution holds problem lists, smoking status, family history, and many GP-entered concepts in Read v2** (the old NHS UK 4-character clinical classification). MT32 records migrated to Evolution carry Read v2 forward; new GP entries may be Read or SNOMED depending on practice configuration.
- **Smoking-status pitfall**: Read codes 137. (smoker), 1371 (never), 1372 (trivial), 137S (ex-smoker), 137P (ex-trivial), 137R (current smoker — heavy) — **multiple overlapping codes**, plus free-text and a separate Medtech smoking field. Extraction must prefer the most-recent structured code, fall back to text, and treat absence as "unknown" not "non-smoker".
- **Mapping path**: NHS England TRUD publishes a Read v2 → SNOMED CT map (Read CTV3 → SNOMED maps preferred where available). NexWave should consume this map, not hand-curate. Cite version/date in code.
- **Care Gap Finder must accept Read OR SNOMED** for each clinical concept it queries.

### 6.3 NZULM and ATC for medications

- **NZULM (NZ Universal List of Medicines)** is the authoritative NZ medicines code set, published by Pharmac via Medsafe / Te Whatu Ora. Medtech and Indici both use NZULM IDs for prescriptions.
- For **medication-class queries** (antihypertensive, statin, antiplatelet, anticoagulant), the resilient strategy is **ATC prefix membership**, not enumerated NZULM IDs:
  - `C02`, `C03`, `C07`, `C08`, `C09` → BP-lowering (any drug whose ATC starts with these is in scope)
  - `C10` → lipid-lowering (statin = `C10AA*`)
  - `B01` → antithrombotic (aspirin antiplatelet `B01AC06`, clopidogrel `B01AC04`, warfarin `B01AA03`, DOACs `B01AF*`)
- Why ATC: Pharmac schedule changes regularly, brand names churn, NZULM IDs may be re-issued. ATC prefixes are **stable and schedule-update-proof**.
- NZULM publishes ATC as a property of each medicinal product — extract once, cache.

### 6.4 HISO 10001 ethnicity — and the PREDICT prioritisation inversion

- **HISO 10001:2017** is the NZ ethnicity data protocol. Multi-response (a person can record multiple ethnicities); coded at level 1 (broad), level 2 (mid), level 3 (detailed), level 4 (most specific). PREDICT uses level-2-equivalent input.
- **Prioritised single-ethnicity output** is a derived value used when a single category is needed. **MoH prioritisation rule** (the standard): Māori > Pacific > Asian > MELAA > Other > European/Other. This is what Te Whatu Ora reporting uses by default.
- **PREDICT v.2019 inverts the standard rule**: PREDICT uses **highest-cardiovascular-risk-wins** prioritisation, which is **Indian > Māori > Pacific > Chinese / other Asian > Other > NZ European**. **Indian outranks Māori in PREDICT** because Indian ethnicity has the highest CVD risk multiplier in the equation.
- **Critical edge case**: a Fijian Indian patient → **Indian** in PREDICT, **not** Pacific. Care Gap Finder must implement the PREDICT prioritisation, not borrow from a generic MoH ethnicity helper.
- Source: HISO 10071:2025 PREDICT specification + NZ Primary Prevention Equations 2019 paper.

### 6.5 LOINC — universal in NZ community lab feeds

- LOINC is the analyte code system for HL7 v2 lab messages. **Almost all NZ community labs send LOINC in OBX-3.2** (with their local code in OBX-3.1 as the primary, LOINC as the second triplet). Dual-code redundancy is the norm.
- Key codes for Care Gap Finder:
  - **HbA1c**: `4548-4` (LOINC, IFCC mmol/mol or %)
  - **Total cholesterol**: `2093-3`
  - **HDL cholesterol**: `2085-9`
  - **LDL (calculated)**: `13457-7`
  - **Triglycerides**: `2571-8`
  - **Creatinine**: `2160-0`
  - **eGFR (CKD-EPI 2021, race-free)**: `98979-8`
  - **Albumin/creatinine ratio (urine)**: `14959-1`
  - **Systolic BP**: `8480-6` (vital sign, in `Observation`, not lab)
  - **Diastolic BP**: `8462-4`
- **HbA1c dual-unit pitfall**: NZ adopted IFCC mmol/mol as primary in 2011, but DCCT % may still appear as a parallel OBX. A naive "take most-recent value" extraction silently confuses **7.5% (poor control)** with **7.5 mmol/mol (impossible — within reference range)**. Care Gap Finder MUST check OBX-6 units before storing.
- **eGFR**: NZ moved to CKD-EPI 2021 race-free in 2022; older results may use CKD-EPI 2009 or MDRD. Code may be the same (`98979-8` is the new code; `33914-3` was MDRD). Treat eGFR comparability across years carefully.

### 6.6 NZDep2018 — operational version, geocoded from address

- **NZDep2018** (released December 2020) is the current operational version. **NZDep2023 has not been publicly released** as of April 2026 (Stats NZ 2023 Census release schedule has not yet produced it).
- NZDep is **derived from address**, not stored in PMS records. Pipeline:
  1. Patient address → geocode to meshblock (LINZ Address Information Management System, or commercial geocoder)
  2. Meshblock → SA1 / SA2 (Stats NZ concordance)
  3. SA1 → NZDep2018 quintile or decile (Otago University-published lookup table)
- **Completeness pitfall**: rural addresses, RD postal addresses, and PO boxes do not geocode reliably. Expect ~5–15% of a typical practice to be ungeocodeable on first pass. Strategy: cache successful geocodes, surface "NZDep unknown" rather than imputing a default.
- For PREDICT: NZDep enters as quintile 1–5; missing → impute median (3) and flag.

### 6.7 ICD-10-AM and ICPC-2 — out of scope

- **ICD-10-AM**: hospital-discharge coding only. Appears in eDischarge structured CDA documents and in some specialist letters. **Not used in GP problem lists.** Care Gap Finder should not query against ICD-10-AM in PMS data; it may parse it from inbound discharge summaries to support Inbox Helper context.
- **ICPC-2**: International Classification of Primary Care, Read alternative. **Not in widespread NZ use.** A small minority of practices may have ICPC-coded data; Care Gap Finder should treat it as a fallback only.

### 6.8 Code-set summary table

| Domain | Authoritative code system | NZ source | Care Gap Finder strategy |
|---|---|---|---|
| Diagnosis (problem list) | SNOMED CT (new) + Read v2 (legacy) | SNOMED Intl + NHS TRUD Read→SNOMED map | Accept both; query SNOMED refsets where available, Read codes as fallback |
| Lab analyte | LOINC | OBX-3.2 in HL7 v2 | LOINC primary; check OBX-6 units (HbA1c trap) |
| Vital sign | LOINC | Observation.code | Standard LOINC for BP, weight, smoking |
| Medication | NZULM (ID) + ATC (class) | NZULM (Te Whatu Ora) | ATC prefix membership for class queries |
| Ethnicity | HISO 10001:2017 level 2 | HISO | PREDICT prioritisation, NOT MoH prioritisation |
| Deprivation | NZDep2018 | Otago University / Stats NZ | Geocode at extract time; cache; flag missing |
| Smoking | SNOMED + Read 137* + free text | Mixed | Most-recent structured code; treat absence as unknown |
| Hospital discharge dx | ICD-10-AM | eDischarge CDA | Parse for Inbox Helper context only |

---

## 7. Document Arrival Patterns

### 7.1 Practice baseline

| Metric | Working figure | Source confidence |
|---|---|---|
| NZ general practices | ~1,000 | RNZCGP Workforce Survey 2022 (high) |
| PHO-enrolled patients (national) | ~4.9 M | Te Whatu Ora PHO quarterly (high) |
| Mean enrolled per practice | ~4,900 | Derived (high) |
| **"Average practice" working figure** | **2,500 enrolled (median)** | GPNZ / RNZCGP working figure (medium) |
| FTE GPs per average practice | 2.2–2.8 | RNZCGP (medium) |
| Consultations per FTE GP per day | 25–35 | RNZCGP / NZMJ (high) |

**Important**: the national mean is ~4,900 enrolled per practice. **The 2,500 figure is the median**, used for per-practice sizing. For national roll-out cost modelling use 4,900 mean or model the right-skewed distribution.

### 7.2 Inbox volume — items per practice per day

**There is no peer-reviewed NZ publication giving direct "inbox items per GP per day".** Triangulation:
- BPAC NZ inbox-management material references "20–40 results per GP per day" qualitatively
- NHS England GP Forward View: ~36 inbox items per session × 2 sessions/day = ~72/day
- RNZCGP 2022 reports 30–60 minutes/day inbox time but no item counts
- Australia (RACGP 2023): ~40–60 items/GP/day informally

**Working estimate for the 2,500-patient median practice: 80–150 inbox items/day, median ≈ 110.**

| Practice size | FTE GPs | Working estimate inbox/day |
|---|---|---|
| Solo (~1,200 enrolled) | 1.0 | 35–60 |
| **Small median (~2,500 enrolled)** | **2.2–2.8** | **80–150** |
| Medium (~5,000 enrolled) | 4.5–5.5 | 160–300 |
| Large (~10,000 enrolled) | 9–11 | 320–600 |
| Very large (~20,000 enrolled) | 18–22 | 650–1,300 |

**Sprint 2 architecture sizing anchor**: **110 items/day median, 200 items/day p90.**

### 7.3 Document type breakdown

| Document type | % of inbox (estimate) | Per practice/day at 110 total |
|---|---|---|
| Lab results (HL7 ORU) | 55–65% | 65–70 |
| Specialist letters (public + private) | 10–15% | 12–16 |
| Radiology reports | 8–12% | 10–13 |
| Discharge summaries | 5–8% | 6–9 |
| Patient portal messages | 3–8% | 3–9 |
| ACC documents | 2–4% | 2–4 |
| Referral acknowledgements / other | 3–5% | 3–5 |

**Confidence: low–medium.** These proportions are extrapolated from NHS England and BPAC commentary. Validating against Medtech engagement-track histograms is **open question #1**.

### 7.4 Variability and peaks

| Scenario | Multiplier | Items/day (avg practice) |
|---|---|---|
| Steady state | 1.0× | 110 |
| Typical busy day (Monday) | 1.5× | 165 |
| Seasonal peak (winter Monday) | 1.8× | ~200 |
| Post-holiday backlog | 2.5× | ~275 |
| Worst case (winter + post-holiday) | 3.0× | ~330 |

- **Day-of-week**: Monday highest (1.4–1.6×), Friday secondary peak (1.2–1.3×), weekends ~10–20% of weekday.
- **Time-of-day**: morning (7–10) bulk lab arrival, midday radiology, afternoon letters/discharges, evening portal/ACC.
- **Seasonal**: winter (Jun–Aug) +15–25%; **post-holiday mid-Jan 2.0–2.5× spike** is the single most stressful operational window.
- **Trend**: ~5–8% YoY growth post-COVID, driven by portal uptake. Provision for 1.3–1.5× current volume over 5 years.

**Sizing rule**: Inbox Helper must handle 3× steady state on first-week-of-January and sustain that for 2–3 days. At cloud LLM pricing this is a linear cost multiplier; at self-hosted GPU it's a capacity-planning constraint.

### 7.5 Document type structure recap (cross-ref §4.5)

| Type | Structured % | Implication for Inbox Helper |
|---|---|---|
| Chemistry / haematology / biochemistry | >99% | Discrete values; LLM only reads free-text OBX comments (~1–5% of naive token budget) |
| Microbiology | ~85% | Organism + sensitivity structured; interpretive comment free-text |
| Histopathology | ~30% | Narrative dominant; high LLM value |
| Radiology private (Pacific, ARG, Mercy, Wellington) | 25–35% | LLM reads impression — high value |
| Radiology public (DHB → HealthLink) | <10% | Free-text dictation — highest LLM value |
| Discharge summary structured CDA national | 40–55% | Wide regional variation (Auckland metro 70–85%, rural South Island 20–50%) |
| Specialist letters (public DHB outpatient) | <10% structured | **Second-highest-value LLM input** after radiology |
| Specialist letters (private) | PDF over MDM | OCR/text-extract pipeline mandatory |

**Image-only PDFs** (scanned fax-to-email, dictation workflows) require Inbox Helper to run **its own OCR pipeline** — Medtech and Indici do not OCR inbound PDFs.

### 7.6 Patient portal volume and tail risk

- ManageMyHealth ~500–600 practices; MyIndici ~250–350; ConnectMed ~100. **~80–85% of NZ practices offer a portal**, ~30–40% of enrolled patients are active users.
- Volume: ~0.5–1.5 messages per active user per year → **~2–6 messages per practice per day** for the median practice.
- Content: 45–55% repeat scripts, 15–25% appointment requests, 10–15% results queries, 8–12% clinical questions, 5–10% admin, 2–5% other.
- **Urgent-content tail risk**: portals disclaim urgent use. Slip-through rate is **not publicly documented** — informal HQSC/MPS evidence suggests order of 1 in 1,000–5,000 messages. **This is the single biggest safety tail-risk for Inbox Helper** and is **open question #2**.

---

## 8. Variable-by-Variable Mapping Table

This is the central R6 artefact. Each row covers one Care Gap Finder input variable, listing: code system / value set, ALEX FHIR resource + search parameter, Indici equivalent (where known), Read v2 fallback, expected completeness, key pitfalls, and the routing decision (deterministic / extraction / derived).

### 8.1 PREDICT v.2019 / HISO 10071:2025 inputs (15 variables)

| # | Variable | Code system | ALEX FHIR resource & path | Indici equivalent | Read v2 fallback | Completeness | Key pitfalls | Routing |
|---|---|---|---|---|---|---|---|---|
| 1 | **Age** | Calendar | `Patient.birthDate` | Patient.dob | n/a | ~100% | DOB-only patients (overseas, refugees) | Deterministic |
| 2 | **Sex** | Administrative | `Patient.gender` | Patient.sex | n/a | ~100% | "Other"/"unknown" — PREDICT only takes M/F; flag and exclude | Deterministic |
| 3 | **Ethnicity** | HISO 10001 level 2 | `Patient.extension[ethnicity]` (HL7 NZ) or Medtech custom ext | Patient.ethnicity (HISO 10001) | n/a | ~95% structured (often multi-response) | **PREDICT highest-risk-wins prioritisation** (Indian > Māori > Pacific > Chinese/Asian > Other > NZ European); Fijian Indian → Indian, NOT Pacific | Deterministic + custom prioritisation |
| 4 | **Diabetes status** | SNOMED + Read v2 | `Condition` (SNOMED `73211009` family + descendants) | Condition (SNOMED) | Read v2 `C10*` family (`C10E*` T1, `C10F*` T2) | ~90–95% in coded problem list | Misclassification T1/T2; "diet-controlled" status ambiguity; gestational vs ongoing | Deterministic (any active diabetes Condition) |
| 5 | **Smoking status** | SNOMED + Read v2 + free text | `Observation` LOINC `72166-2` (tobacco smoking status) or `Condition` | Observation tobacco smoking status | Read `137*` (1371 never, 1372 trivial, 137S ex, 137P ex-trivial, 137R current heavy, 137. smoker) — **multiple overlapping codes** | ~70–85% structured; ~15% free-text only | Multiple Read codes; absence ≠ non-smoker; date-of-quit may live in separate field | Deterministic on most-recent code, **extraction fallback for free text** |
| 6 | **Systolic BP** | LOINC `8480-6` | `Observation?code=8480-6&_sort=-date` | Observation BP systolic | n/a (vital sign, not Read) | ~95%+ for engaged patients; lower for new enrolees | Single-reading vs averaged; cuff size; orthostatic; date drift; "white-coat" annotation | Deterministic (most-recent or 12-month average per PREDICT spec) |
| 7 | **Total cholesterol (TC)** | LOINC `2093-3` | `Observation?code=2093-3&_sort=-date` | Observation TC | n/a | ~80–90% in CVDRA-eligible | Fasting vs non-fasting; lab unit (mmol/L NZ standard) | Deterministic |
| 8 | **HDL cholesterol** | LOINC `2085-9` | `Observation?code=2085-9` | Observation HDL | n/a | Co-extracted with TC | n/a | Deterministic |
| 9 | **TC:HDL ratio** | Derived (TC ÷ HDL) | Computed in BFF | Computed | n/a | Derived | Compute fresh, do not trust pre-computed ratios from old reports | Derived |
| 10 | **Antihypertensive therapy** | NZULM + ATC `C02/C03/C07/C08/C09` prefixes | `MedicationRequest?status=active` filter on ATC | MedicationRequest active | NZULM IDs in legacy text | ~95% for treated HTN | NZULM ID churn — **use ATC prefix, not enumerated NZULM IDs**; exclude end-dated; 'as-needed' vs scheduled | Deterministic (ATC prefix membership) |
| 11 | **Statin / lipid-lowering therapy** | NZULM + ATC `C10*` (`C10AA*` statin) | `MedicationRequest?status=active` ATC filter | MedicationRequest active | NZULM | ~95% for treated dyslipidaemia | Non-statin lipid agents (ezetimibe `C10AX09`, fibrates `C10AB*`); discontinued courses | Deterministic (ATC prefix) |
| 12 | **Antiplatelet / anticoagulant therapy** | NZULM + ATC `B01*` (aspirin antiplatelet `B01AC06`, clopidogrel `B01AC04`, warfarin `B01AA03`, DOACs `B01AF*`) | `MedicationRequest?status=active` ATC filter | MedicationRequest active | NZULM | ~90–95% if indication present | OTC aspirin (not in MedicationRequest); high-dose vs cardio-protective dose distinction not in ATC | Deterministic (ATC prefix) + flag OTC gap |
| 13 | **Family history of premature CVD** | SNOMED CT + free text | `FamilyMemberHistory.condition` (uncertain whether ALEX exposes this resource); else free-text consultation notes | FamilyMemberHistory or notes | Read `12*` family history codes | **30–50% structured** (highly variable, often only narrative) | Highest extraction difficulty in PREDICT; "premature" definition (<55M / <65F); first-degree only | **LLM extraction** from notes — primary R&D challenge |
| 14 | **Atrial fibrillation (ECG-confirmed)** | SNOMED `49436004` + descendants; ECG report cross-check | `Condition` SNOMED AF, optionally cross-checked against `DiagnosticReport` ECG | Condition SNOMED AF | Read v2 `G573*` AF family | ~85–95% in coded problem list once diagnosed | Distinguish ECG-confirmed vs self-reported vs Holter-detected paroxysmal; PREDICT requires ECG confirmation | Deterministic (Condition with confirmation flag); flag self-reported separately |
| 15 | **NZDep (deprivation quintile)** | NZDep2018 quintile | **Not stored in ALEX** — derived from `Patient.address` via geocoder → meshblock → SA1 → NZDep2018 lookup | Same — derived from address | n/a | ~85–95% geocodeable; rural/RD/PO box ~5–15% fail | NZDep2023 not yet released as of April 2026; rural addresses fail; cache successful geocodes; "missing" → impute median (3) and flag | **Derived pipeline** (geocode → SA1 → NZDep) |

### 8.2 Care Gap Finder auxiliary variables (beyond PREDICT)

| Variable | Code system | ALEX FHIR resource & path | Read v2 fallback | Completeness | Pitfalls | Routing |
|---|---|---|---|---|---|---|
| **HbA1c** | LOINC `4548-4` | `Observation?code=4548-4&_sort=-date` | n/a | ~95% in known diabetes | **Dual-unit trap**: IFCC mmol/mol since 2011 + DCCT % may still appear; check OBX-6 unit before storing — 7.5% ≠ 7.5 mmol/mol | Deterministic + unit check |
| **eGFR (CKD-EPI 2021 race-free)** | LOINC `98979-8` (new) or `33914-3` (MDRD legacy) | `Observation?code=98979-8` | n/a | ~85–95% in CKD-eligible | NZ moved to CKD-EPI 2021 race-free in 2022; older results MDRD; treat cross-year comparability carefully | Deterministic |
| **Albumin/creatinine ratio (urine)** | LOINC `14959-1` | `Observation?code=14959-1` | n/a | ~60–80% in known diabetes (lower in CKD-only) | KDIGO 2013 matrix uses ACR + eGFR jointly | Deterministic |
| **Creatinine** | LOINC `2160-0` | `Observation?code=2160-0` | n/a | ~95% in CKD-eligible | Used to derive eGFR if eGFR not pre-computed | Deterministic + derive |
| **LDL (calculated)** | LOINC `13457-7` | `Observation?code=13457-7` | n/a | Co-reported with lipid panel | Friedewald vs direct LDL; not strictly required by PREDICT (uses TC:HDL) | Optional, deterministic |
| **Triglycerides** | LOINC `2571-8` | `Observation?code=2571-8` | n/a | Co-reported with lipid panel | Fasting requirement | Deterministic |
| **Diastolic BP** | LOINC `8462-4` | `Observation?code=8462-4` | n/a | Co-reported with systolic | n/a | Deterministic |
| **BMI / weight** | LOINC `39156-5` BMI; `29463-7` weight | `Observation?code=39156-5` | n/a | ~70–85% | Currency (BMI from 5 years ago not useful) | Deterministic |
| **CVD history (IHD/MI/CVA)** | SNOMED CT + Read v2 `G3*`/`G6*`/`G7*` | `Condition` SNOMED CVD families | Read v2 `G3*` IHD, `G6*` cerebrovascular, `G7*` arterial | ~90% structured | "Equivalent CVD" suppresses CVDRA — high recall required | Deterministic |
| **Diabetes review components**: foot exam, retinal screen, microalbumin, HbA1c date | SNOMED procedure codes + dated `Observation` | `Procedure?code=...` and `Observation?code=...&_sort=-date` | Read v2 procedure codes | Variable; foot exam ~50–70%, retinal ~60–80% | External retinal screening reports may not be filed back to GP record reliably | Deterministic on most-recent dated entry |
| **Cervical screening (date)** | SNOMED procedure | `Procedure` cervical screening | Read v2 | ~70–85% | NCSP changes (HPV primary 2023) require recoding awareness | Deterministic |
| **Immunisation status** | NIR + local code | `Immunization` resource (NIR-sourced) | Read v2 imm codes | ~85–95% | NIR sync lag; locally administered vs externally administered | Deterministic |

### 8.3 Routing summary

- **Deterministic (structured field lookup)**: 12 of 15 PREDICT inputs and 12 of 12 auxiliaries — the dominant pathway. Care Gap Finder's primary engine is a deterministic FHIR query layer.
- **Derived pipeline (NZDep)**: 1 of 15 — address geocoding pipeline owned by Care Gap Finder, runs once per patient and caches.
- **LLM extraction (family history)**: 1 of 15 — the **only Care Gap Finder LLM workload**, ~2,000–2,400 note-level calls per cold scan. Free-text family-history extraction from consultation notes.
- **Hybrid (smoking)**: structured-first, free-text fallback if no recent code.

This routing maps directly to the R4 architecture decision: **Care Gap Finder is a deterministic workload with a small LLM sidecar**, not an LLM workload end-to-end. It must not be conflated with Inbox Helper for compute or cost planning.

---

## 9. Data Volume Estimates and Cost Model

### 9.1 Care Gap Finder denominators per 2,500-patient practice

| Cohort | Prevalence basis | Denominator |
|---|---|---|
| Adults ≥35 (broad CVDRA-eligible) | ~55% of enrolled | ~1,375 |
| **CVDRA priority cohort** (Māori/Pacific/South Asian M 30+; other M 45+/F 55+) | ~35–40% of enrolled | **~900–1,000** |
| Known diabetes (T1 + T2) | ~6% of adults | **~140–180** |
| Hypertension on treatment | ~13% of adults | **~290–370** |
| On lipid-lowering therapy | ~12–15% of adults | ~225–300 |
| **CKD stage 3+ (eGFR <60)** | ~6–8% of adults 45+ | **~100–150** |
| Current smokers | ~8% of adults (declining) | ~150–200 |
| CVD history (IHD/MI/CVA) | ~4% of adults | ~75–100 |
| Eligible for shingles vaccine (65+) | ~15% of enrolled | ~375 |
| Cervical screening eligible (25–69) | ~30% of enrolled | ~750 |

**Unique patients in scope** (union of chronic + preventive rules) ≈ **1,800–2,100 of the 2,500 enrolled**.

### 9.2 ALEX FHIR API call budget

**Cold scan** (one-off, full register):
- 1 Patient + 1 Conditions + 1 MedicationStatements + 1 Observations (paged 100) + 1 DiagnosticReport + 1 AllergyIntolerance ≈ **5–6 calls/patient** × 2,500 = **12,500–15,000 calls**
- **Wall-clock at 5 req/s APIM default**: 12,500 ÷ 5 ≈ 42 min single-threaded; with 20% retry/backoff overhead **~50 min**
- At conservative 2 req/s (if real ALEX limit is lower), ~2 hours — still operationally feasible

**Weekly delta** (`_lastUpdated=gt[last-run]` on Conditions, MedicationStatement, Observation for 1,800 in-scope patients + bulk Patient delta):
- ≈ **2,000–3,500 calls/week** ≈ **10 minutes wall-clock**

**Daily delta** (more realistic operational cadence):
- ≈ **400–600 calls/day** ≈ **~100 seconds wall-clock**

These numbers are consistent with the R4-D BFF + delta-pull architecture conclusion. ALEX rate limit is **open question #4** (still unknown).

### 9.3 Inbox Helper monthly token volume

- 110 items/day × 22 working days = **2,420 classifications/month**
- Weighted mean input ≈ **700 tokens/item** (lab 400, radiology 1,200, discharge 1,800, letter 1,000, portal 200, ACC 500)
- Output ≈ 100 tokens/item (4-level urgency + rationale)
- Monthly tokens: **~1.69 M input, ~0.24 M output**

### 9.4 Care Gap Finder LLM workload

LLM is required only for **family-history extraction from free-text notes**. All other variables are deterministic.
- Cold scan: ~2,000–2,400 note-level calls × ~500 in / ~50 out = **~1.2 M input, ~0.24 M output tokens**
- Weekly delta: ~30–80 new notes
- Steady-state monthly (post cold scan): **~0.1 M input, ~0.02 M output**

### 9.5 Cost model — per practice per month

**Claude Haiku 4.5 via Bedrock (Sydney `ap-southeast-2` as proxy for `ap-southeast-6` Auckland; pricing assumption flagged):**
- Inbox Helper: 1.69 M × ~US$1.00/M + 0.24 M × ~US$5.00/M ≈ US$2.89 ≈ **NZD 4.80/month**
- Care Gap Finder (cold scan month): ~US$2.40 ≈ **NZD 4/month**
- Care Gap Finder (steady-state): **~NZD 0.50/month**
- **Combined headline: NZD 6–10/month/practice on cloud Haiku 4.5.** Auckland region uplift assumption +5–10% over Sydney.

**Llama 3.3 70B self-hosted on Catalyst Cloud:**
- Llama 3.3 70B FP8 fits on 1× A100 80GB; FP16 needs 2× A100 80GB or 2× L40S
- Catalyst A100 80GB single-tenant 24/7 ≈ **NZD 1,800–2,500/month**
- At 2,420 classifications/month single-tenant, cost per classification ≈ **NZD 0.91** — **utterly uneconomic single-tenant**
- **Pooled break-even vs Haiku Bedrock**: NZD 2,200 ÷ NZD 5 ≈ 440 practices sharing one A100; with realistic burst headroom ~220 practices. **The tenancy threshold is ~200 practices, not 25–50.** This is a material refinement to R3/R7.

**Fine-tuned BioClinical ModernBERT 396M (or equivalent encoder):**
- Fits on ~2 GB VRAM; runs on shared T4 / CPU
- ~5 min GPU time/month for 2,420 items
- Amortised: **~NZD 0.50–1.50/month/practice**
- Lowest-cost path; **accuracy on 4-level urgency is the open question** (covered in R3 / R7 Sprint 3 evaluation)

| Engine | Combined Inbox Helper + Care Gap Finder NZD/month/practice | Notes |
|---|---|---|
| **Claude Haiku 4.5 (Bedrock Sydney proxy)** | **NZD 6–10** | Simplest, linear, no infra |
| Llama 3.3 70B single-tenant Catalyst | NZD 2,000–2,500 | Uneconomic single-tenant |
| Llama 3.3 70B pooled (50 practices/A100) | NZD 50–70 | Worse than Haiku |
| Llama 3.3 70B pooled (250 practices/A100) | NZD 10–15 | Competitive with Haiku |
| **Fine-tuned ModernBERT 396M shared** | **NZD 1–3** | Lowest cost; accuracy TBC |

### 9.6 Architecture tipping points

- **Below ~25 practices**: cloud API (Haiku 4.5) is cheapest *and* simplest.
- **25–200 practices**: cloud API still cheapest; self-hosted only justified by sovereignty/policy, not cost.
- **200+ practices**: pooled self-hosted Llama 70B becomes cost-competitive; at 500+ materially cheaper.
- **Any scale**: a fine-tuned small encoder is the lowest-cost path *if* it meets the accuracy bar.

**Cost is not the limiting factor** at expected per-practice volumes. The combined NZD 6–10/month/practice on cloud Haiku is trivially absorbable in any realistic licensing model. The cost risk lives elsewhere — infrastructure, support, compliance.

### 9.7 Burst sizing

Inbox Helper must handle **3× steady state on first-week-of-January** for 2–3 days. At cloud API this is a linear cost multiplier only. At self-hosted GPU it requires provisioned burst capacity — another argument for cloud or pooled hosting at sub-200-practice scale.

---

## 10. Sovereignty and Compliance for ALEX / Indici Data Flows

### 10.1 Where ALEX-mediated data physically resides

- Medtech Evolution practice databases are **practice-hosted** (on-premise or in a Medtech-managed Azure tenant) — data lives in the practice's jurisdiction by default.
- ALEX FHIR API is fronted by **Azure API Management** in a Medtech-managed Azure subscription. Most public hints suggest the front door is in **Azure Australia East (Sydney)** with possible AU-South-East redundancy. Whether Medtech offers a NZ-region (Azure Australia East does not satisfy NZ data-residency under HIPC strictly; Auckland Azure region is recent). **Confirmation pending — Medtech engagement open question.**
- An ALEX API call therefore involves: practice DB → Medtech-managed Azure API tier (likely AU East) → caller. **Cross-Tasman processing is in-scope** when data leaves the practice; HIPC Rule 11 (cross-border disclosure) considerations apply.

### 10.2 Constraints on partner processing location

- Under HIPC 2020 Rule 11, NZ health information may be disclosed cross-border only with the patient's consent or under tight purpose-specific exceptions. **In practice, practice + Medtech contracts typically permit Medtech-internal Australia processing as a service-provider-of-the-practice arrangement** (the practice remains the agency holding the information).
- A third party (NexWave) consuming ALEX data must establish its own data-handling posture under HIPC. Options:
  1. **NZ-sovereign** (Catalyst Cloud, AWS Auckland `ap-southeast-6`) — strongest defensibility under MBIE grant clause "R&D undertaken outside New Zealand is not eligible".
  2. **Trans-Tasman with explicit consent** — workable for clinical use after pilot but adds consent overhead during R&D.
  3. **Same Medtech-managed Azure AU tier** — only viable if Medtech itself hosts the AI workload.
- **Recommendation for Sprint 2/3**: anchor on NZ-sovereign Catalyst Cloud + AWS `ap-southeast-6` for any inference involving real or even synthetic-but-realistic NZ clinical data. Defer the Medtech-managed Azure option until we know more.

### 10.3 Audit logging and provenance

- ALEX FHIR API calls are logged at the Medtech APIM tier (caller, endpoint, timestamp, status). Per-resource access logging is not exposed to the partner — Medtech holds it.
- Care Gap Finder and Inbox Helper must keep **their own audit log** of every patient touched, every variable extracted, and every classification produced — for HIPC accountability and TGA Class IIa post-market surveillance.
- **Practice administrators do NOT have a console showing third-party API access** to their data via ALEX (best current understanding — confirmation pending). This is a transparency gap that NexWave should address voluntarily by providing the practice with a dashboard of its own.

### 10.4 Indici sovereignty posture

- Indici / Valentia is NZ-headquartered. Hosting location for the Indici-managed cloud is not publicly documented in detail; informal indication is NZ-resident. **To be confirmed in the Sprint 4+ Valentia engagement.**
- Indici's NZ origin is a defensibility advantage if the integration ever lands.

### 10.5 Sovereignty matrix for the architecture decision

| Path | Data residency | HIPC posture | MBIE grant clause | Defensibility |
|---|---|---|---|---|
| Catalyst Cloud NZ self-host | NZ | Strongest | Compliant | High |
| AWS Bedrock `ap-southeast-6` (Auckland) | NZ | Strong (cross-Region inference flagging needed) | Compliant if pinned | High |
| AWS Bedrock `ap-southeast-2` (Sydney) | AU | Cross-border — needs explicit consent path | Borderline — requires MBIE pre-approval discussion | Medium |
| Medtech-managed Azure AU East | AU | Service-provider-of-practice; needs explicit downstream agreement | Borderline | Medium |
| Overseas serverless (Runpod, Modal, Together) | US | Weak; shared-tenancy concerns | **Non-compliant** under default reading of grant clause | Low |

This matrix feeds the R3 architecture shortlist and the R2 sovereignty deep-dive.

---

## 11. Gaps and Open Questions for Engagement Tracks

### 11.1 Medtech / MIPP engagement track (highest priority — gates Sprint 3+ pilot work)

1. **Sandbox access** — confirm UAT facility codes (working hypothesis F99669-C / F2N060-E), MIPP onboarding timeline, NDA scope for ALEX FHIR specification documents
2. **ALEX FHIR rate limit per token / per tenant** — currently unknown; assumed 5 req/s APIM default
3. **Resource coverage confirmation** — does ALEX expose `FamilyMemberHistory`? `Group`? `DocumentReference` content vs metadata-only?
4. **Practice-admin console** — does any view of third-party API access exist for practice administrators?
5. **Hosting region for ALEX APIM tier** — Sydney AU East confirmed? Auckland Azure region available?
6. **Anonymised inbox histograms** from 3–5 pilot practices for Sprint 2 validation of §7.3 document-type breakdown
7. **Sample of 1,000 consecutive inbox items** (anonymised) for ground-truth distribution analysis
8. **Webhook / Subscriptions** — any near-real-time delivery option, or pull-only via `_lastUpdated`?

### 11.2 HISO / Te Whatu Ora / standards engagement

1. **NZ FHIR terminology service credentialed access** for R&D — what is the licensing pathway?
2. **HL7 NZ Patient profile current normative status** — confirm NHI system URL canonical form
3. **Current eDischarge structured-CDA national rate** broken down by former-DHB district
4. **NZ-published Z-segment catalogue** for inter-provider HL7 messaging (or confirm vendor-bilateral only)
5. **HISO 10001 ethnicity prioritisation guidance** — confirm PREDICT v.2019 highest-risk-wins inversion is the authoritative rule for CVDRA (vs MoH default Māori-first)

### 11.3 HealthLink / Clanwilliam engagement

1. **HealthLink envelope specification** — partner NDA path for an MBIE-funded R&D programme
2. **FHIR-native inbound** option — DocumentReference POST or v2 only?
3. **NIR Immunization push** — `VXU^V04` to GP inbox or query-only?

### 11.4 Lab provider engagement

1. **Awanui Labs** — single unified HL7 spec post-merger, or per-legacy-lab catalogues? Sender ID alias mapping?
2. **Pathlab / LabPLUS / CHL / Medlab Central** — current LOINC vs local-code dual-coding rates
3. **HbA1c unit reporting** — confirmed all NZ community labs send IFCC mmol/mol primary, or are any still DCCT %?

### 11.5 Pharmac / NZULM

1. **NZULM ATC mapping completeness and update cadence** — confirmed stable enough to anchor medication-class queries
2. **NZULM API for programmatic lookup** — public, NDA, or static download?

### 11.6 RNZCGP / GPNZ / BPAC / HQSC engagement

1. **Inbox volume per GP per day** — single biggest evidence gap; the 110/day figure is extrapolated from BPAC commentary + NHS data
2. **Patient portal urgent-content slip-through rate** — single biggest safety tail risk; HQSC / MPS data?
3. **Practice size / FTE / urban-rural breakdown** — refresh the 2,500-patient median assumption
4. **Seasonal inbox multiplier** — any vendor data on January post-holiday spike?

### 11.7 Catalyst Cloud / AWS engagement

1. **Catalyst Cloud GPU SKU list and current NZD pricing** for A100 80GB slices, L40S 48GB, A6000 48GB — including 1-year reserved
2. **AWS Bedrock `ap-southeast-6` Haiku 4.5 / Sonnet 4.6 native availability and pricing** at GA
3. **HIPAA / NZ Privacy Act equivalent BAA** for Bedrock NZ region

### 11.8 Indici / Valentia (Sprint 4+, deferred)

1. Developer access pathway and partner agreement scope
2. FHIR API surface vs proprietary REST
3. NZ data residency confirmation

---

## 12. Reference List

### Standards bodies and profile sources

- **Te Whatu Ora — Data and digital standards** (approved standards index): `https://www.tewhatuora.govt.nz/our-health-system/digital-health/data-and-digital-standards/approved-standards`
- **HISO 10001:2017** — Ethnicity Data Protocols (Te Whatu Ora / MoH)
- **HISO 10046** — Consumer Health Identity Standard (NHI)
- **HISO 10071:2025** — PREDICT CVD Risk Assessment Standard
- **HISO 10083** — NHI / HPI data set
- **HISO 10040.0** — Clinical Document Architecture standard (eDischarge target format)
- **HL7 New Zealand**: `https://www.hl7.org.nz/`
- **HL7 NZ Confluence** (FHIR profile workspace): `https://confluence.hl7.org.nz/`
- **HL7 NZ GitHub** (NZ Base IG draft source): `https://github.com/HL7NZ`
- **HL7 Australia — AU Core IG**: `https://hl7.org.au/fhir/core/`
- **Sparked** (AU Core / eRequesting): `https://sparked.csiro.au/`
- **HL7 International v2.4 / v2.5 specifications**: `https://www.hl7.org/implement/standards/`
- **SNOMED International / SNOMED CT NZ release** — Te Whatu Ora terminology portal
- **NHS England TRUD** (Read v2 → SNOMED map): `https://isd.digital.nhs.uk/trud`
- **LOINC**: `https://loinc.org`
- **NZULM** (NZ Universal List of Medicines) — Pharmac / Te Whatu Ora pharmacy systems
- **NZ Primary Prevention Equations 2019** (Pylypchuk et al.) — PREDICT v.2019 source paper
- **NZ Health Survey 2023/24** annual data explorer: `https://minhealthnz.shinyapps.io/nz-health-survey-2023-24-annual-data-explorer/`
- **NZDep2018**: University of Otago, Wellington — Department of Public Health

### PMS, integration carriers, and vendors

- **Medtech Global**: `https://www.medtechglobal.com/` — ALEX FHIR API product page
- **Medtech Integration Partner Programme (MIPP)** — partner gating for ALEX sandbox + production
- **Indici / Valentia Technologies**: `https://www.indici.health/`
- **HealthLink (Clanwilliam Group)**: `https://www.healthlink.net/` — partner integration specs portal/NDA only
- **Awanui Labs**: `https://www.awanuilabs.co.nz/`
- **Pathlab**: `https://www.pathlab.co.nz/`
- **Medlab Central**: `https://www.medlabcentral.co.nz/`
- **LabPLUS** (Te Toka Tumai Auckland): Te Whatu Ora pages
- **Canterbury Health Laboratories**: Te Whatu Ora Canterbury pages
- **ManageMyHealth** (patient portal, Medtech-integrated): `https://managemyhealth.co.nz`

### NZ primary care benchmarks

- **RNZCGP Workforce Survey 2022** (published 2023): `https://www.rnzcgp.org.nz/RNZCGP/Publications/Workforce_Surveys`
- **GPNZ member practice directory and benchmarking reports**: `https://gpnz.org.nz`
- **Te Whatu Ora PHO enrolment quarterly reports**: `https://www.tewhatuora.govt.nz/our-health-system/data-and-statistics/primary-care/`
- **BPAC NZ — "Managing the inbox"** articles 2018 and 2021: `https://bpac.org.nz`
- **Te Whatu Ora Transfer of Care Guidance 2024** — discharge summary 24-hour target
- **NZMJ workload and general practice studies** (Jatrana, Crampton, et al.): `https://nzma.org.nz/journal`
- **RANZCR NZ structured reporting position papers**: `https://www.ranzcr.com`
- **RCPA–AACB harmonisation programme** — pathology messaging standards
- **HQSC medico-legal / safety reports**: `https://www.hqsc.govt.nz`

### Cloud / infrastructure references

- **Catalyst Cloud pricing page**: `https://catalystcloud.nz/pricing` — exact GPU SKU pricing pending verification
- **AWS Bedrock pricing page** (Sydney `ap-southeast-2` / Auckland `ap-southeast-6`): `https://aws.amazon.com/bedrock/pricing/`
- **AWS Bedrock NZ region announcement** (March 2026): `https://aws.amazon.com/blogs/machine-learning/run-generative-ai-inference-with-amazon-bedrock-in-asia-pacific-new-zealand/`

### Cross-references within this research programme

- [[research-r1-llm-architecture-benchmarks]] — clinical LLM benchmarks (Sprint 2)
- [[research-r2-nz-sovereign-hosting-regulatory]] — NZ sovereignty and regulatory deep-dive
- [[research-r3-architecture-shortlist]] — architecture shortlist this report feeds
- [[research-r4-care-gap-finder-subtasks]] — Care Gap Finder sub-task architecture
- [[research-r7-open-source-llm-self-hosted]] — self-hosted open-source LLM track
- [[inbox-helper-task-spec]] — Inbox Helper locked task spec
- [[care-gap-finder-task-spec]] — Care Gap Finder locked task spec

---

## Compiler's note on confidence and limitations

This R6 synthesis is compiled from four parallel sub-agent research outputs (R6-A ALEX + Indici APIs, R6-B HL7 v2 NZ + FHIR profiles, R6-C NZ code sets + variable mapping, R6-D document arrival + volumes + cost). The sub-agents operated without live web access in their research sessions; numerical figures — particularly inbox volume per practice, document-type mix, patient portal message rates, and Catalyst / Bedrock pricing — are drawn from published NZ primary-care knowledge and flagged as **medium confidence**.

**Highest-priority verification items before MBIE Q1 progress report (31 May)**:

1. **Inbox items per NZ GP per day** — the 110/day headline is extrapolated; no strong NZ primary source exists. Validate via RNZCGP/BPAC/GPNZ engagement (open question §11.6.1).
2. **ALEX FHIR resource coverage and rate limit** — confirm via MIPP onboarding (§11.1).
3. **Catalyst Cloud GPU SKU pricing and AWS Bedrock `ap-southeast-6` pricing** — get current quotes (§11.7).
4. **Pooled tenancy break-even** — the **~200-practice** figure is a material refinement to R3/R7 first-instinct of 25–50; should be re-validated when actual GPU pricing is confirmed.
5. **Patient portal urgent-content slip-through rate** — single biggest safety tail risk for Inbox Helper (§11.6.2).

The research-question coverage is comprehensive within the defined R6 scope. The evidence strength is **high for code sets and standards, medium for ALEX API surface (NDA-gated), medium for population baseline, medium-low for inbox volume and cost, high for Care Gap Finder register denominators, low for patient portal safety tail-risk**.

This report deliberately does not deep-dive: clinical urgency taxonomy (covered in `Urgency classification for GP inbox triage.md`), evaluation metrics (covered in `Evaluation metrics for ordinal clinical AI triage classification.md`), HISO 10071:2025 PREDICT equation parameters (locked in [[care-gap-finder-task-spec]]), or architecture model selection (R3/R7).

