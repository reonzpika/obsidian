# ClinicPro Capture — Australian Privacy Impact Assessment

**DRAFT — DO NOT FILE WITHOUT LEGAL REVIEW**

Version: 0.1 Draft
Date: 2026-04-23
Author: Ryo (NexWave Solutions Limited)
Reviewer: [Legal counsel — TBC]
Status: Internal draft only. Not submitted to OAIC or any regulatory body.

Prepared in accordance with the OAIC Guide to Undertaking Privacy Impact Assessments (updated September 2024) and the OAIC 10-step PIA framework.

---

## Contents

1. Threshold Assessment
2. Project Description
3. Scope and Methodology
4. Stakeholder Consultation
5. Information Flow Mapping
6. Privacy Impact Analysis (APP-by-APP)
7. Risk Register
8. Recommendations and Mitigations
9. Residual Risks and Items Requiring Legal Review
10. Review and Monitoring Plan

---

## 1. Threshold Assessment

**Does this project collect, use, store, or disclose personal information?**

Yes. ClinicPro Capture collects Supabase authentication records (email address, facility identifier, practitioner identifier) and generates an audit log (`medtech_image_commit_audit`) recording image commit events. Clinical images are transiently processed in-memory but are immediately committed to the Medtech Evolution patient record via the ALEX FHIR API. No images are retained by ClinicPro infrastructure.

**Is the personal information sensitive?**

Partially. Authentication data (email, practitioner ID) is personal information under the Privacy Act 1988 (Cth). Clinical images, when transiently processed, constitute health information, which is sensitive information under section 6 of the Privacy Act. The audit log records which practitioner committed an image for which patient at what time, which is health-adjacent metadata and likely sensitive information in context.

**Is a PIA warranted?**

Yes. The project:
- handles health information, even transiently
- involves cross-border data flows (NZ operator, NZ BFF proxy, AU Supabase instance)
- is deployed into Australian GP practices under a distribution agreement with Medtech Global
- has no AU legal entity in place at time of writing

**Conclusion:** Full PIA required.

---

## 2. Project Description

### 2.1 Product

ClinicPro Capture is a clinical image capture web application. It enables practitioners in Australian GP practices to capture (photograph or upload) clinical images at the point of care and commit them directly to the patient's existing Medtech Evolution record as a FHIR DocumentReference resource via the ALEX API.

### 2.2 Distribution Model

ClinicPro Capture is white-labelled and bundled by Medtech Global for Australian GP practices using the Medtech Evolution practice management system. The commercial arrangement is managed by Lawrence Peterson (Medtech Global). The application is presented under Medtech Global branding, accessed via a CNAME on a Medtech Global-controlled domain.

### 2.3 Operator

NexWave Solutions Limited, a New Zealand company (NZ registered, no AU entity at time of writing). Business contact: ryo@clinicpro.co.nz.

**Gap: No AU legal entity exists.** The operator is a foreign entity subject to the Privacy Act 1988 (Cth) by virtue of operating in Australia (s 5B: Act applies to acts done in Australia or a Territory). The absence of an AU entity does not remove legal obligation but creates gaps in accountability, a registered local address for OAIC correspondence, and accessible contact obligations under APP 1. This must be resolved before commercial launch. See Section 9.

### 2.4 Deployment Architecture

| Component | Location | Provider |
|---|---|---|
| Frontend web app | Vercel edge network (global CDN) | Vercel Inc. (US) |
| BFF (Backend-for-Frontend) proxy | NZ AWS Lightsail instance | Amazon Web Services |
| Supabase database and auth | Sydney, AWS ap-southeast-2 | Supabase Inc. (US-incorporated, AU-hosted) |
| ALEX FHIR API | Medtech Global infrastructure (AU) | Medtech Global |
| Medtech Evolution patient record | GP practice server (on-premises) | GP practice / Medtech Global |

### 2.5 Authentication

OTP-based authentication via Supabase Auth. A 6-digit code is sent to the practitioner's registered email address. No password stored. No magic links. No third-party SSO.

---

## 3. Scope and Methodology

### 3.1 In Scope

- Collection, use, storage, and disclosure of practitioner authentication data
- Transient processing of clinical images during capture and FHIR commit
- Generation and retention of `medtech_image_commit_audit` log
- Data flows between the BFF proxy, Supabase, and the ALEX API
- Cross-border data flows (NZ BFF to AU Supabase; NZ BFF to ALEX API)
- Responsibilities and accountability as operator under the APPs

### 3.2 Out of Scope

- Patient personal information held within Medtech Evolution (governed by Medtech Global and the GP practice as controllers)
- Medtech Global's own privacy obligations
- Patient consent for clinical photography (governed by clinical governance at the GP practice)
- NZ Privacy Act 2020 compliance (separate analysis required)

### 3.3 Methodology

This PIA was prepared by the operator (NexWave Solutions Limited) using the OAIC 10-step framework and PIA tool structure. It draws on the architectural documentation for ClinicPro Capture, the commercial arrangement with Medtech Global, and Supabase and AWS infrastructure specifications. External legal review is required before finalisation.

---

## 4. Stakeholder Consultation

| Stakeholder | Role | Consultation Status |
|---|---|---|
| Ryo (NexWave Solutions Limited) | Operator and product owner | Involved throughout |
| Lawrence Peterson (Medtech Global) | Distributor and commercial partner | Not yet consulted on privacy obligations |
| GP practice end users | Practitioners using the app | Not consulted (no customer yet at draft stage) |
| Supabase Inc. | Auth and database infrastructure provider | Reviewed DPA / terms of service |
| AWS | Underlying cloud infrastructure | Standard AWS data processing agreement applies |
| Australian legal counsel | Privacy Act compliance | TBC — required before finalisation |

**Gap:** Lawrence Peterson / Medtech Global have not been formally consulted on their privacy obligations in the distribution chain. The PIA should be shared with Medtech Global's legal team. Medtech Global may be a co-regulated entity or downstream processor; this needs legal clarification.

---

## 5. Information Flow Mapping

### 5.1 Data Types Collected

| Data Field | Category | Sensitivity | Retained By ClinicPro |
|---|---|---|---|
| Email address | Personal information | Medium | Yes (Supabase auth) |
| Practitioner ID (`practitionerId`) | Personal information (professional) | Medium | Yes (Supabase auth + audit log) |
| Facility ID (`facilityId`) | Organisational identifier | Low | Yes (Supabase auth) |
| OTP code (6-digit) | Authentication credential | High (transient) | No (not stored; delivered by Supabase email) |
| Clinical image (photo/upload) | Health information (sensitive) | Very high | No (zero retention; see 5.3) |
| Audit log entry (`medtech_image_commit_audit`) | Health-adjacent metadata | High | Yes (Supabase database) |

### 5.2 Authentication Flow

1. Practitioner opens ClinicPro Capture in browser (served via Vercel CDN).
2. Practitioner enters email. OTP is generated and sent by Supabase to that email.
3. Practitioner enters OTP. Supabase validates and issues session token.
4. Session token held in browser memory / secure cookie for the session.

Data path: browser -> Vercel CDN -> Supabase AU (ap-southeast-2)

### 5.3 Image Capture and Commit Flow

1. Practitioner captures or uploads image in browser.
2. Image is sent from browser to the BFF proxy (NZ Lightsail instance) over HTTPS.
3. BFF proxy forwards image to the ALEX FHIR API as a `DocumentReference` POST request.
4. ALEX API commits the image to the patient's Medtech Evolution record.
5. BFF proxy writes a commit record to `medtech_image_commit_audit` in Supabase AU.
6. Image is not written to Supabase. No copy is retained by ClinicPro infrastructure.

Data path: browser -> BFF (NZ, Lightsail) -> ALEX API (AU) -> Medtech Evolution (AU)
Side path: BFF -> Supabase AU (audit log only, no image)

**Key privacy-positive design feature:** Images transit NZ infrastructure only in memory during the BFF proxy step. They are not written to disk, logged, or retained. The zero-retention design is the primary risk control for clinical image data.

### 5.4 Audit Log Schema (`medtech_image_commit_audit`)

Fields retained:
- `practitionerId`
- `facilityId`
- `timestamp`
- `fhir_document_reference_id` (returned by ALEX API on successful commit)
- `commit_status` (success / failure)

Fields not retained:
- Image content, file, or URL
- Patient identifier (no patient ID is stored by ClinicPro)
- Patient name or date of birth

**Note:** The audit log links a practitioner to a FHIR document reference ID. Depending on the FHIR implementation, the document reference ID may be reversible to patient identity by a party with ALEX API access. This is inherent to the FHIR audit design and is not a flaw in ClinicPro's implementation, but it means the audit log is health-adjacent sensitive data and must be treated as such.

---

## 6. Privacy Impact Analysis (APP-by-APP)

### APP 1 — Open and Transparent Management of Personal Information

**Requirement:** Maintain a current privacy policy; have systems to handle enquiries and complaints.

**Assessment:** NexWave Solutions Limited does not currently have a public AU-facing privacy policy covering ClinicPro Capture. The white-labelled deployment under a Medtech Global domain increases the risk that end users cannot identify or contact the operator.

**Gap:** No AU-facing privacy policy exists. No AU contact address or registered agent. **High priority item for legal.**

---

### APP 2 — Anonymity and Pseudonymity

**Requirement:** Where lawful and practicable, allow individuals to deal anonymously or pseudonymously.

**Assessment:** Practitioners must authenticate with a real email address to receive an OTP. Anonymity is not practicable given the audit and accountability requirements of clinical image commit. Pseudonymity is not available in the current design. This is a reasonable limitation given the clinical context, but should be documented in the privacy policy.

**Assessment: Compliant by exception (clinical necessity).**

---

### APP 3 — Collection of Solicited Personal Information

**Requirement:** Only collect personal information reasonably necessary for the entity's functions.

**Assessment:**
- Email: necessary for OTP auth.
- `practitionerId` and `facilityId`: necessary for ALEX API authorisation and audit.
- Clinical images: collected to fulfil the core function (image-to-record commit). Zero retention limits privacy impact.
- Audit log: reasonably necessary for accountability, debugging, and potential medico-legal requirements.

The collection of clinical images constitutes collection of sensitive information (health information) under s 6 of the Privacy Act. Collection is lawful if the individual has consented or if another exception applies (e.g. collection is necessary to provide a health service the individual has requested). In this context, collection is at the practitioner's explicit action and serves the provision of health services. Consent is implicit in practitioner use, but explicit patient consent for clinical photography must be managed at the GP practice level.

**Assessment: Likely compliant. Explicit consent framework needs documentation.**

---

### APP 4 — Dealing with Unsolicited Personal Information

**Requirement:** If personal information is received that was not solicited, determine if it could have been collected under APP 3; if not, destroy or de-identify it.

**Assessment:** Not directly applicable. The system is designed to receive only specified information. No mechanism exists for unsolicited collection. The image capture interface is scoped to a structured commit workflow.

**Assessment: Not applicable / low risk.**

---

### APP 5 — Notification of Collection

**Requirement:** At or before collection, take reasonable steps to notify the individual of specified matters (identity of collector, purposes, etc.).

**Assessment:** No current in-app notification or privacy collection notice is presented at sign-in or first use. The white-label deployment further obscures the identity of the collecting entity.

**Gap:** Collection notice required at or before OTP authentication. Must identify NexWave Solutions Limited as operator, state purpose of collection, and provide contact details for access/correction requests. **Medium priority item for legal and product.**

---

### APP 6 — Use or Disclosure of Personal Information

**Requirement:** Use or disclose personal information only for the primary purpose of collection, or secondary purposes with consent or applicable exception.

**Assessment:**
- Auth data: used for authentication (primary purpose). Not disclosed to third parties beyond Supabase (processor).
- Audit log: used for operational logging (primary purpose). Accessible to NexWave Solutions Limited staff.
- Images: immediate disclosure to ALEX API for FHIR commit is the primary purpose. No secondary disclosure.
- Medtech Global: as distributor, does Medtech Global have access to auth data or audit logs? This must be clarified contractually. If Medtech Global has database access, that is a secondary disclosure requiring justification.

**Gap:** Medtech Global's data access rights are not formally defined in a data processing agreement. This must be resolved. **High priority item for legal.**

---

### APP 7 — Direct Marketing

**Requirement:** Do not use or disclose personal information for direct marketing without consent (with exceptions).

**Assessment:** No direct marketing use of collected data is intended. Email addresses collected for OTP authentication are not used for marketing.

**Assessment: Compliant. No direct marketing use.**

---

### APP 8 — Cross-Border Disclosure of Personal Information

**Requirement:** Before disclosing personal information to an overseas recipient, take reasonable steps to ensure the recipient does not breach the APPs. The disclosing entity remains accountable.

**Assessment:** This is a primary risk area.

**Flow 1: BFF proxy (NZ) to ALEX API (AU)**
The image transits a NZ-based infrastructure component before reaching the AU ALEX API. NZ is not on the OAIC's approved "whitelist" for cross-border disclosure as of April 2026 (the whitelist mechanism introduced by the Privacy and Other Legislation Amendment Act 2024 had not produced a final approved country list as of the knowledge cutoff). However, New Zealand has substantially equivalent privacy protections under the Privacy Act 2020 (NZ). The operator may rely on the "substantially similar laws" pathway under APP 8.2(a) if NZ is determined to meet that threshold, or may rely on APP 8.2(b) (the individual consents) or APP 8.2(c) (required or authorised by law).

The safest path is to contractually document this flow and seek legal advice on whether NZ qualifies under the post-2024 framework.

**Flow 2: Supabase Inc. (US-incorporated) hosting AU data**
Supabase operates the AU Supabase instance on AWS ap-southeast-2 (Sydney). Data physically resides in AU. However, Supabase is a US-incorporated entity. Staff access, support, and administrative tooling may involve US-based access to AU-hosted data. Review of Supabase's current DPA is required to confirm AU data is not accessed from outside AU without controls.

**Gap: APP 8 analysis incomplete. Legal review required for both flows. High priority.**

---

### APP 9 — Adoption, Use, or Disclosure of Government Related Identifiers

**Requirement:** Do not adopt, use, or disclose a government-related identifier as own identifier.

**Assessment:** No government identifiers (Medicare number, provider number) are collected or used by ClinicPro Capture. `practitionerId` is a Medtech Evolution internal identifier, not a government identifier.

**Assessment: Compliant.**

---

### APP 10 — Quality of Personal Information

**Requirement:** Take reasonable steps to ensure personal information is accurate, up to date, and complete.

**Assessment:** Auth data accuracy depends on the practitioner's own registration. No mechanism currently validates that the email or practitioner ID is current. If a practitioner leaves a practice, their account should be deprovisioned; this process is not formally defined.

**Gap:** Account deprovisioning process needs documentation (likely managed via Medtech Global's onboarding/offboarding workflow).

---

### APP 11 — Security of Personal Information

**Requirement:** Take reasonable steps to protect personal information from misuse, interference, loss, and unauthorised access. Destroy or de-identify when no longer needed.

**Assessment:**

| Control | Status |
|---|---|
| HTTPS in transit (browser to Vercel, Vercel to BFF, BFF to ALEX) | In place |
| Supabase at rest encryption (AES-256, managed by Supabase/AWS) | In place |
| OTP auth (no passwords stored) | In place |
| Image zero retention | In place |
| BFF proxy: TLS in transit | In place |
| BFF proxy: image not written to disk | In place (to be verified) |
| Audit log access controls (row-level security or equivalent) | Status unknown — needs verification |
| Supabase auth data retention / deletion policy | Not defined |
| BFF instance hardening (patching, access controls) | Status unknown — needs verification |
| Incident response plan | Does not exist |

**Gap:** No formal incident response plan. No defined retention period or deletion policy for auth data or audit logs. BFF proxy security posture needs formal review. **High priority.**

---

### APP 12 — Access to Personal Information

**Requirement:** On request, give individuals access to their personal information.

**Assessment:** No formal mechanism exists for a practitioner to request access to their auth data or audit log entries. No process has been designed.

**Gap:** Access request process needed. Must include contact point, response timeframe (30 days per Act), and method of providing access. **Medium priority.**

---

### APP 13 — Correction of Personal Information

**Requirement:** On request, correct personal information that is inaccurate, out of date, incomplete, irrelevant, or misleading.

**Assessment:** No correction mechanism defined.

**Gap:** Correction process needed. **Medium priority.**

---

## 7. Risk Register

| ID | Risk | Likelihood | Impact | Severity |
|---|---|---|---|---|
| R1 | Clinical image intercepted in transit through NZ BFF proxy | Low | Very High | High |
| R2 | No AU legal entity: OAIC cannot reach operator; legal accountability gap | Medium | High | High |
| R3 | Supabase auth data default region not confirmed as Sydney at project creation | Medium | High | High |
| R4 | BFF proxy on NZ Lightsail: cross-border flow not covered by formal APP 8 analysis | Medium | High | High |
| R5 | No privacy policy or collection notice for AU users | High | Medium | High |
| R6 | Medtech Global data access rights undefined; potential unauthorised disclosure | Medium | High | High |
| R7 | No incident response plan; data breach notification obligations under Part IIIC not met | High | High | Critical |
| R8 | Audit log treated as low-sensitivity; actual sensitivity is health-adjacent | Low | High | Medium |
| R9 | No practitioner account deprovisioning process | Medium | Medium | Medium |
| R10 | Supabase Inc. US staff may access AU-hosted data (support access) | Low | Medium | Medium |
| R11 | Image retained in BFF process memory longer than needed (timing attack surface) | Low | High | Medium |

---

## 8. Recommendations and Mitigations

### R1 — Image in transit (BFF proxy)

**Mitigation:**
- Enforce TLS 1.2+ on all BFF connections (verify in Lightsail config).
- Confirm image data is not logged or written to disk at any point in the BFF handler.
- Keep image in-memory pipeline as short as possible (receive, forward, discard).
- Document this architecture in the privacy policy as a "transient processing" disclosure.
- Consider whether the BFF proxy can be migrated to AU infrastructure (removes APP 8 complexity for this flow).

**Owner:** Ryo. **Priority:** High.

---

### R2 — No AU legal entity

**Mitigation:**
- Register an Australian entity (Pty Ltd or branch) before commercial launch, or
- Appoint an AU-based registered agent for OAIC correspondence and privacy complaints as an interim measure.
- Add NexWave Solutions Limited's NZ contact details to the privacy policy in the interim, with explicit acknowledgement that the operator is a foreign entity.

**Owner:** Ryo (legal and corporate advisory required). **Priority:** Critical before launch.

---

### R3 — Supabase AU region confirmation

**Mitigation:**
- Confirm in the Supabase dashboard that the AU production project is set to `ap-southeast-2` (Sydney). Document this with a screenshot dated at project creation.
- If a new project was created without explicitly selecting AU region, verify current region and migrate if needed.
- Review Supabase DPA to confirm data residency guarantees for Sydney region.

**Owner:** Ryo. **Priority:** High.

---

### R4 — BFF proxy cross-border flow (APP 8)

**Mitigation:**
- Obtain legal advice on whether NZ qualifies as a substantially similar jurisdiction under APP 8.2(a) post-2024 reforms.
- If NZ does not qualify, consider: (a) migrating BFF to an AU instance (AWS ap-southeast-2 EC2 or equivalent), which eliminates the cross-border flow entirely; or (b) obtaining explicit practitioner consent at first use covering the NZ transit leg.
- Document the cross-border flow in the privacy policy regardless of which path is taken.

**Owner:** Ryo (legal advice required). **Priority:** High.

---

### R5 — Privacy policy and collection notice

**Mitigation:**
- Draft an AU-compliant privacy policy covering ClinicPro Capture. Must include: identity and contact of operator, purposes of collection, how personal information is held and protected, overseas disclosure details, and access/correction process.
- Add an in-app collection notice presented at or before first OTP authentication.
- Coordinate with Medtech Global on how the privacy policy is surfaced given the white-label domain arrangement.

**Owner:** Ryo (legal drafting required). **Priority:** High.

---

### R6 — Medtech Global data access

**Mitigation:**
- Execute a formal data processing agreement (DPA) with Medtech Global before launch.
- DPA must specify: what data Medtech Global can access, for what purposes, and what security obligations apply.
- Clarify whether Medtech Global is a processor (acting on NexWave's instructions) or a separate controller (with independent obligations). This classification has significant APP implications.

**Owner:** Ryo and Lawrence Peterson (Medtech Global). **Priority:** Critical before launch.

---

### R7 — Incident response plan

**Mitigation:**
- Draft a data breach response plan covering: detection, containment, assessment, notification to OAIC (Part IIIC: Notifiable Data Breaches scheme), and notification to affected individuals.
- Note: The NDB scheme applies where a breach is likely to result in serious harm. Auth data breach (email + practitioner ID) likely meets this threshold for practitioners in a clinical setting.
- Implement breach logging and alerting (Supabase logs, BFF access logs) as detection inputs.

**Owner:** Ryo. **Priority:** Critical before launch.

---

### R8 — Audit log sensitivity

**Mitigation:**
- Apply the same access controls to `medtech_image_commit_audit` as would be applied to health records (row-level security, audit of admin access).
- Define a retention period for audit log entries (suggest: 7 years, consistent with clinical record retention obligations, or as advised by legal counsel for AU).
- Include audit log in the privacy policy as a retained data type.

**Owner:** Ryo. **Priority:** Medium.

---

### R9 — Practitioner account deprovisioning

**Mitigation:**
- Define and document the offboarding process with Medtech Global: who triggers deprovisioning, what is the SLA, and what data is deleted versus retained for audit purposes.
- Implement a Supabase user deactivation workflow (disable auth, retain audit log per retention policy).

**Owner:** Ryo and Medtech Global. **Priority:** Medium.

---

### R10 — Supabase US staff access

**Mitigation:**
- Review Supabase's current DPA and SOC 2 Type II report to understand staff access controls for AU-hosted data.
- Confirm whether Supabase implements data residency controls that restrict support access to AU region.
- If not, disclose in privacy policy that the infrastructure provider's staff may access data for support purposes.

**Owner:** Ryo. **Priority:** Medium.

---

### R11 — Image in BFF process memory

**Mitigation:**
- Confirm in code review that the BFF handler does not buffer images to disk, does not log image bytes, and does not retain image data beyond the ALEX API POST response.
- Consider explicitly zeroing the buffer in the image handling code path after forward completes.

**Owner:** Ryo. **Priority:** Medium.

---

## 9. Residual Risks and Items Requiring Legal Review

The following items cannot be resolved by technical or operational controls alone. Legal advice is required before commercial launch.

| Item | Description | Priority |
|---|---|---|
| L1 | AU entity or registered agent | Is a foreign operator required to have an AU entity or agent for OAIC purposes? What is the minimum viable structure? | Critical |
| L2 | APP 8 — NZ as substantially similar jurisdiction | Does NZ qualify under the post-2024 whitelist framework? If not, what is the compliant path for the BFF proxy? | High |
| L3 | Medtech Global classification | Is Medtech Global a processor or co-controller? What are the DPA obligations between the parties? | High |
| L4 | Privacy policy — white label context | How must the privacy policy be presented when the app is white-labelled under a Medtech domain? Who is the disclosed collector? | High |
| L5 | NDB scheme scope | Does ClinicPro Capture's data holdings fall within the Notifiable Data Breaches scheme? What is the threshold for "serious harm" in this context? | High |
| L6 | Health Records Act (Vic) and state equivalents | Do any state-level health records laws apply in addition to the federal APPs? | Medium |
| L7 | Audit log retention period | What is the legally required retention period for clinical image audit records in AU? | Medium |
| L8 | Patient consent for clinical photography | Is ClinicPro required to collect or verify patient consent, or is this entirely the GP practice's responsibility? | Medium |

---

## 10. Review and Monitoring Plan

| Trigger | Action |
|---|---|
| Before commercial launch | Legal review of this PIA, resolve all Critical and High items |
| On execution of Medtech Global DPA | Update Section 6 (APP 6 and APP 8) with confirmed data access terms |
| On AU entity registration | Update operator details throughout; update privacy policy |
| On any change to BFF infrastructure or deployment region | Reassess APP 8 and R1, R4 |
| On any Supabase plan or region change | Reassess R3, R10 |
| Annually | Full review of APPs compliance; update for any Privacy Act reform commencement |
| On any suspected data breach | Activate incident response plan; assess NDB notification obligations |

---

## Appendix A — Applicable Law

| Instrument | Relevance |
|---|---|
| Privacy Act 1988 (Cth) | Primary governing legislation |
| Australian Privacy Principles (Schedule 1, Privacy Act) | APP obligations assessed in Section 6 |
| Privacy and Other Legislation Amendment Act 2024 (Cth) | 2024 reforms: whitelist mechanism for cross-border disclosure, new children's privacy provisions, new enforcement powers |
| Notifiable Data Breaches scheme (Part IIIC, Privacy Act) | Breach notification obligations |
| State health records legislation (Vic, NSW, QLD, etc.) | May apply in addition to federal APPs; legal advice required |
| My Health Records Act 2012 (Cth) | Not currently applicable (ClinicPro Capture does not interface with My Health Record) |

---

## Appendix B — Definitions

| Term | Definition |
|---|---|
| APP entity | An organisation or government agency bound by the Australian Privacy Principles |
| BFF | Backend-for-Frontend: a server-side proxy layer between the frontend app and backend services |
| FHIR | Fast Healthcare Interoperability Resources: an international standard for exchanging healthcare data |
| ALEX API | Medtech Global's FHIR-compliant API for integrating with Medtech Evolution |
| OTP | One-Time Password: a 6-digit authentication code delivered by email |
| NDB | Notifiable Data Breaches (scheme under Part IIIC of the Privacy Act) |
| OAIC | Office of the Australian Information Commissioner |

---

*Sources used in preparing this PIA:*
- [OAIC Guide to Undertaking Privacy Impact Assessments](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/privacy-impact-assessments/guide-to-undertaking-privacy-impact-assessments)
- [OAIC 10 Steps to Undertaking a PIA](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/privacy-impact-assessments/10-steps-to-undertaking-a-privacy-impact-assessment)
- [OAIC PIA Tool](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/privacy-impact-assessments/privacy-impact-assessment-tool)
- [OAIC APP 8 Cross-border disclosure guidance](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information)
- [Privacy and Other Legislation Amendment Act 2024](https://www.aph.gov.au/Parliamentary_Business/Bills_LEGislation/Bills_Search_Results/Result?bId=r7249)
- [MinterEllison: Privacy and Other Legislation Amendment Act 2024 now in effect](https://www.minterellison.com/articles/privacy-and-other-legislation-amendment-act-2024-now-in-effect)
