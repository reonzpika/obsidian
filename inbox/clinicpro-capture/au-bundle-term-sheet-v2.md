# AU Bundle Term Sheet — ClinicPro Capture

_Draft v2 — 25 April 2026_
_Self-drafted for legal review. Do not send to counterparty without review by legal counsel._
_All output is a first draft pending Ryo's detailed review. Not final. Not ready to send._

---

## 1. Parties

**Licensor:** NexWave Solutions Limited, a company incorporated in New Zealand (NZBN to be inserted), trading as ClinicPro, with its registered office at [address to be inserted], Auckland, New Zealand ("ClinicPro").

**Licensee:** Medtech Global Pty Ltd [FLAG: legal entity name not confirmed. Lawrence's emails show "Medtech Global" but the AU entity name and ACN have not been provided in writing. Confirm before signing.], a company incorporated in Australia (ACN to be inserted), with its registered office at [address to be inserted], Australia ("Medtech Global").

---

## 2. Effective date

This Term Sheet takes effect on the date both parties have signed below ("Effective Date").

[FLAG: Effective date left blank for execution. Do not pre-fill.]

---

## 3. Background

3.1 ClinicPro has developed ClinicPro Capture, a mobile web application that photographs clinical images and commits them to patient records via the Medtech ALEX API (FHIR DocumentReference POST endpoint).

3.2 Medtech Global is launching Medtech Evolution Australia ("Evolution AU") and wishes to bundle ClinicPro Capture as a value-add feature for Australian general practices.

3.3 The parties wish to record the principal commercial terms on which ClinicPro will provide ClinicPro Capture for distribution by Medtech Global under this arrangement.

---

## 4. Product scope

4.1 **Included in scope:**
- ClinicPro Capture mobile web application (image capture and server-side processing)
- ALEX API integration via ClinicPro's backend for financial function (BFF) layer: specifically, FHIR DocumentReference POST to Medtech ALEX
- User authentication (Supabase OTP)
- Audit logging
- Deployment on Sydney AWS region (ap-southeast-2) with AU data residency
- White-label configuration for Medtech Global's domain via CNAME (domain to be provided by Medtech Global)
- Initial support enablement: runbook, escalation matrix, training sessions (cadence and scope to be agreed in the full agreement)

4.2 **Explicitly excluded from scope:**
- Any features beyond image capture and ALEX DocumentReference POST
- Management dashboard or tenancy/licence administration tooling (separate engagement, to be scoped and priced after Medtech Global provides written requirements)
- Any additional PMS integrations beyond Medtech ALEX
- NexWave Health programme products: Inbox Helper, Care Gap Finder, or any other tools developed under the NexWave R&D programme
- My Health Record integration [FLAG: not discussed with Lawrence. Include unless Lawrence confirms it is in scope for the ALEX backend side only.]

4.3 Any request by Medtech Global to add functionality, integrate additional data sources, or extend the ALEX API scope beyond clause 4.1 constitutes a change request and will be scoped and priced separately.

---

## 5. Commercial terms

### 5.1 Subscription fee

AUD 30.00 per active practice per month ("Subscription Fee").

The Subscription Fee is inclusive of ClinicPro's cloud infrastructure costs. No separate infrastructure charge applies.

### 5.2 Definition of active practice

An "active practice" is a general practice that has at least one enrolled user who has logged in to ClinicPro Capture and performed at least one successful image capture transaction committed to Medtech ALEX in the relevant billing month. Practices onboarded but not yet active in a given billing month do not count toward the minimum for that month.

[FLAG: Definition agreed in principle. Confirm with Lawrence before finalising — this definition affects minimum billing calculations and Lawrence's internal reporting obligations.]

### 5.3 Minimum practice commitment

Medtech Global commits to a minimum of [TBD: 40 or 50] active practices per month, equivalent to a minimum annual payment of AUD [TBD: 14,400 (40 practices) or 18,000 (50 practices)] per year ("Annual Minimum"), for each year of the Initial Term.

[FLAG: Lawrence verbally indicated 50 practices is too high and is taking the question to his boss. Ryo's floor is 40 practices. Exact number pending Lawrence's response. Do not finalise this clause until confirmed. If minimum is below 40 at AUD 30, the deal economics do not work on central-case cost model — review pricing before accepting.]

Where the number of active practices in any month exceeds the minimum, the full Subscription Fee applies to all active practices, with no cap.

Where the number of active practices in any month falls short of the minimum, the Annual Minimum payment still applies, invoiced as a shortfall true-up at year end [FLAG: alternative is to bill the minimum monthly floor each month regardless. Decide with legal counsel which is operationally simpler and confirm with Lawrence.]

### 5.4 Billing cycle and payment terms

Medtech Global will be invoiced monthly in arrears, based on the active practice count for the preceding billing month, with the Annual Minimum floor applied.

Payment terms: net 30 days from invoice date.

All amounts are in Australian dollars (AUD), exclusive of GST where applicable.

Late payment interest: [FLAG: standard NZ/AU commercial rate is 2% per month above the NZ bank bill rate or similar benchmark. Legal counsel to draft.]

### 5.5 Setup fee

A one-off setup fee will apply to cover AU regionalisation engineering (including NHI to IHI identifier handling, AU facility ID configuration, AU privacy copy, and white-label deployment to Medtech Global's domain). The setup fee will be agreed between the parties and inserted into the full agreement once the auth model (clause 7.2) and update control approach (clause 7.3) are confirmed.

[FLAG: Setup fee quantum not yet agreed. Verbally acknowledged by Lawrence in 22 April meeting. Ryo to quote once auth model and update control are resolved. Signal to Lawrence: "not large, but real engineering work is required."]

### 5.6 Withholding tax (WHT) treatment

[FLAG: This clause is a placeholder. The WHT structure must be resolved with professional tax advice before this clause is finalised. Do not send this term sheet to Lawrence until WHT is resolved. Helen Yu (helen@hscg.co.nz) briefing is pending — task medtech-20260423-002.]

All fees payable to ClinicPro under this agreement are intended to be received by ClinicPro as net AUD 30.00 per active practice per month. The parties will structure the commercial arrangement as a services fee for supply of software-as-a-service (not a royalty or licence fee) to the extent that such characterisation minimises withholding tax exposure under the Australia-New Zealand Double Tax Agreement and/or the ATO's draft ruling TR 2024/D1.

In the event that any withholding tax is nevertheless required by law to be deducted or withheld from any payment:
- The Licensee will gross up the payment so that the Licensor receives the full contractual amount it would have received absent the withholding; or
- [FLAG: Alternative: shared WHT burden. Legal counsel and Helen to advise on preferred structure.]

The parties agree that the net commercial intent is for ClinicPro to receive AUD 30.00 per active practice per month regardless of withholding treatment. Final WHT language to be drafted by legal counsel after professional tax advice.

---

## 6. Term

### 6.1 Initial term

Three (3) years from the Effective Date ("Initial Term").

### 6.2 Renewal

On expiry of the Initial Term, this agreement will automatically renew for successive one-year periods ("Renewal Term") unless either party gives not less than 90 days' written notice of non-renewal prior to the expiry of the then-current term.

[FLAG: Auto-renewal on 1-year basis is Ryo's preferred position. Lawrence may prefer mutual-consent renewal. Legal counsel to advise on AU/NZ commercial norms.]

### 6.3 Termination for cause

Either party may terminate this agreement with immediate effect on written notice if the other party:
- commits a material breach of this agreement and fails to remedy that breach within 30 days of receiving written notice of the breach; or
- enters administration, liquidation, receivership, or becomes insolvent.

### 6.4 Termination for convenience

Either party may terminate this agreement for any reason on 90 days' written notice.

### 6.5 Consequences of termination

On termination or expiry:
- Medtech Global's right to distribute ClinicPro Capture ceases. Practices lose access within 30 days of the termination date.
- ClinicPro retains all integration IP. No source code transfer obligation arises.
- Any amounts accrued but unpaid as at the termination date remain payable.
- The Annual Minimum for the year in which termination occurs is payable in full unless termination is by ClinicPro for cause.

[FLAG: 6-month wind-down period for early Medtech termination was noted in v1. Legal counsel to advise whether a run-off period is standard in AU PMS bundle agreements and whether a reduced fee applies during run-off.]

---

## 7. Technical terms

### 7.1 Hosting and data residency

ClinicPro Capture for AU will be hosted in the Sydney AWS region (ap-southeast-2). All Australian patient data processed under this agreement will remain within Australia. ClinicPro will not transfer AU patient data outside Australia without Medtech Global's prior written consent.

### 7.2 Auth model

[FLAG: Not confirmed. Options are Supabase OTP (current NZ model), Medtech SSO, or a separate auth layer. Must be resolved before engineering begins. Affects setup fee quantum.]

### 7.3 Update control

[FLAG: Not confirmed. ClinicPro's preference is auto-deploy (same release cadence as NZ). Medtech Global may require approval gating before updates reach AU practices. Must be resolved before engineering begins. Affects setup fee quantum and SLA language.]

### 7.4 ALEX API access

Medtech Global will provide ClinicPro with access to the ALEX API (including the FHIR DocumentReference POST endpoint and required AU sandbox credentials) necessary for ClinicPro to develop, test, and maintain the integration under this agreement.

Medtech Global will use reasonable efforts to maintain ALEX API uptime. A specific SLA will be included in the full agreement.

[FLAG: ALEX uptime SLA not discussed with Lawrence. Legal counsel to draft a reasonable uptime obligation — suggest 99.5% monthly availability with a carve-out for scheduled maintenance.]

### 7.5 White-label deployment

Medtech Global may deploy ClinicPro Capture under its own branding within Evolution AU. White-label configuration will be delivered via CNAME to a domain provided by Medtech Global, with brand configuration managed via environment variables in the ClinicPro deployment.

Branding approach (full white-label or light ClinicPro attribution) to be agreed. ClinicPro has no strong preference on attribution.

---

## 8. Distribution commission (Alex Cauble-Chantrenne)

[FLAG: This clause covers Ryo's obligation to Alex Cauble-Chantrenne under his separate integration/commission arrangement. It is included here for completeness and to avoid ambiguity between the two Medtech counterparty relationships. Legal counsel to advise whether this clause belongs in the AU bundle agreement with Medtech Global, or solely in a separate side-letter/commission agreement with Alex directly. The two contracts must remain strictly separate.]

15% flat commission on all NZ and AU subscription revenue is payable to Alex Cauble-Chantrenne ("Commission") as consideration for distribution and integration services. Commission is calculated on gross subscription revenue received by ClinicPro (before WHT, if any) and paid monthly within 14 days of ClinicPro receiving payment.

[FLAG: Commission rate and calculation basis to be confirmed once Alex Cauble-Chantrenne's integration contract terms are finalised. 15% flat is the current working figure. The double-dipping carve-out — preventing commission being owed on the same practice under both the AU bundle and a direct-sales arrangement simultaneously — must be operationally defined before either contract is signed. Definitions of "bundle practice" vs "direct-sales practice" are open.]

---

## 9. Responsibilities

### 9.1 ClinicPro

- Product development, maintenance, and updates for ClinicPro Capture
- ALEX API integration maintenance and BFF operation
- Level 2 and Level 3 technical support (escalations from Medtech Global tier-1)
- AU regionalisation engineering (pre-launch)
- SaMD regulatory compliance (see clause 11)
- AU data residency and privacy compliance (Privacy Act 1988 (Cth), Australian Privacy Principles)
- Provision of compliance artefacts: privacy policy, privacy impact assessment, incident response plan, pentest evidence (timelines to be agreed in the full agreement)
- Quarterly usage reporting to Medtech Global (active practice counts, billing basis)

### 9.2 Medtech Global

- Distribution and go-to-market of ClinicPro Capture within Evolution AU
- Level 1 end-user support for AU practices
- Practice introduction and onboarding coordination
- All AU marketing (ClinicPro has no direct marketing obligation under this agreement)
- Provision of ALEX API access and sandbox credentials
- Provision of white-label domain (CNAME)
- Confirmation of AU vendor security requirements (pentest, PIA, ISO 27001 or equivalent) in writing before contract execution

---

## 10. Intellectual property

10.1 Each party retains ownership of its own IP existing prior to or developed independently of this agreement.

10.2 ClinicPro retains ownership of all IP in ClinicPro Capture, including source code, architecture, integrations, and documentation.

10.3 Medtech Global retains ownership of all IP in the ALEX API, Medtech Evolution, and associated Medtech platforms.

10.4 No IP is transferred from either party to the other under this agreement. This agreement grants Medtech Global a non-exclusive, non-transferable, revocable licence to distribute ClinicPro Capture to AU practices during the term only.

10.5 No exclusivity. ClinicPro retains the right to sell ClinicPro Capture to AU general practices independently of this agreement, and to integrate with other AU PMS vendors. Medtech Global has no exclusive territory or exclusive right to distribute ClinicPro Capture in Australia.

[FLAG: Lawrence may push back on no-exclusivity. Ryo's position is that no-exclusivity is non-negotiable. ClinicPro's post-term right to approach bundle practices directly is preserved in clause 10.6.]

10.6 Post-term direct sales. On expiry or termination of this agreement, ClinicPro retains the unrestricted right to offer ClinicPro Capture directly to any practice previously covered by this bundle, on its own pricing and terms.

---

## 11. Regulatory conditions precedent

> **PROMINENT FLAG: This clause must be included and must not be watered down.**

11.1 This agreement is conditional on ClinicPro receiving satisfactory advice from Bell Gully (or equivalent NZ regulatory counsel) that ClinicPro Capture does not constitute a medical device or Software as a Medical Device (SaMD) requiring registration under the Medicines Act 1981 (NZ) and/or the Therapeutic Goods Act 1989 (Cth) (AU), or that any applicable regulatory requirements have been met ("SaMD Condition Precedent").

11.2 ClinicPro will use reasonable endeavours to satisfy the SaMD Condition Precedent within [FLAG: 30 days / 60 days] of the Effective Date.

11.3 If the SaMD Condition Precedent is not satisfied within the agreed period, either party may terminate this agreement without liability.

11.4 Pending satisfaction of the SaMD Condition Precedent, neither party is obliged to commence engineering or distribution activities under this agreement.

[FLAG: Bell Gully SaMD classification Phase 1 is not yet complete as at 25 April 2026. ClinicPro's current internal assessment is that Capture is excluded from TGA medical device registration as a pure image pass-through with no clinical analysis. However, this is an internal assessment only, not formal legal advice. Do not rely on this clause as satisfied — it is a live condition precedent. Legal counsel to confirm appropriate timeframe and fallback language.]

---

## 12. No-exclusivity and right to direct AU sales

See clause 10.5 and 10.6 above.

---

## 13. Confidentiality

13.1 Each party agrees to keep the other party's confidential information strictly confidential and not to disclose it to any third party without the prior written consent of the disclosing party, except as required by law.

13.2 "Confidential information" means all non-public business, technical, and commercial information disclosed by one party to the other in connection with this agreement, including pricing terms, API documentation, product roadmaps, patient data, and the terms of this agreement.

13.3 Confidentiality obligations survive termination or expiry of this agreement for a period of [FLAG: 3 years / 5 years — legal counsel to advise].

13.4 Each party is permitted to disclose confidential information to its employees, directors, legal counsel, and accountants on a need-to-know basis, provided they are bound by equivalent confidentiality obligations.

---

## 14. Liability

14.1 Liability cap: each party's aggregate liability to the other under or in connection with this agreement is limited to the total Subscription Fees paid or payable in the 12 months immediately preceding the event giving rise to the claim.

[FLAG: Liability cap quantum and structure are significant. Legal counsel must draft this. ClinicPro's position: cap at 12 months' fees paid. Medtech Global may push for unlimited liability on data breach or clinical harm scenarios. Ryo's position on clinical liability: ClinicPro Capture is a pure image transport layer with no clinical analysis or decision support. Clinical risk sits with the practitioner and the PMS, not ClinicPro. This position must be defensible in the contract.]

14.2 Neither party will be liable to the other for indirect, consequential, special, or punitive loss or damage, including loss of profits, loss of data, or loss of business.

14.3 The liability cap and exclusion in clauses 14.1 and 14.2 do not apply to:
- death or personal injury caused by a party's negligence
- fraud or wilful misconduct
- [FLAG: legal counsel to advise whether AU data breach notification obligations under the Privacy Act 1988 (Cth) or clinical harm scenarios require a carve-out from the cap]

---

## 15. Governing law and dispute resolution

15.1 This agreement is governed by the laws of New Zealand.

[FLAG: v1 listed this as TBD pending legal advice. Ryo's stated preference is New Zealand law (Auckland jurisdiction). Lawrence may prefer Australian law (Victoria or NSW, given Medtech Global's AU domicile). Legal counsel to advise on negotiating position and practical difference. If Medtech Global insists on AU law, consider whether Auckland International Arbitration Centre (AIAC) or the Australian International Disputes Centre (AIDC) is appropriate for dispute resolution.]

15.2 Any dispute arising out of or in connection with this agreement will be referred to senior representatives of each party for resolution before either party commences legal proceedings.

---

## 16. Representations and warranties

16.1 Each party represents and warrants that:
- it has full authority to enter into this agreement
- entering into this agreement does not breach any obligation to a third party
- it will comply with all applicable laws in the performance of its obligations

16.2 ClinicPro represents and warrants that:
- ClinicPro Capture will perform materially as described in clause 4.1
- it will maintain AU data residency as required by the Australian Privacy Principles
- it holds (or will obtain before go-live) professional indemnity and cyber/technology liability insurance covering AU operations with limits appropriate to the deal value [FLAG: Insurance is not yet in place. Ryo must obtain a combined PI + cyber policy with AU territorial extension before signing. Apollo Insurance Brokers or Gallagher NZ to be approached. Budget NZD 4,000-6,000/year for combined policy. Must confirm clinical/medical software exclusion is not applicable.]

---

## 17. Execution

This Term Sheet is not legally binding on its own. It records the principal commercial terms agreed between the parties. The parties intend to execute a formal agreement incorporating these terms and such additional provisions as legal counsel may advise, and do so as soon as reasonably practicable.

Notwithstanding the above, the parties agree to be bound by the confidentiality obligations in clause 13 from the date of execution.

---

**NEXWAVE SOLUTIONS LIMITED**

Signed by: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Name: Dr Ryo Eguchi

Title: Director / Founder

Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**MEDTECH GLOBAL PTY LTD** [FLAG: entity name to be confirmed]

Signed by: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Name: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Title: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Consolidated flags requiring resolution before finalising

The following items must be resolved before this document is finalised or sent to Medtech Global. Items marked **BLOCK** must be resolved before any version is sent to the counterparty.

| # | Clause | Item | Status | BLOCK? |
|---|---|---|---|---|
| 1 | 1 | Medtech Global AU legal entity name and ACN | Not confirmed | Yes |
| 2 | 5.3 | Minimum practice count: 40 or 50 | Lawrence taking to boss post 22 Apr. Floor is 40. | Yes |
| 3 | 5.5 | Setup fee quantum | Pending auth model (cl 7.2) and update control (cl 7.3) confirmation | Yes |
| 4 | 5.6 | WHT treatment structure | Helen briefing pending (task medtech-20260423-002). Do not send until resolved. | Yes |
| 5 | 7.2 | Auth model | Not confirmed | Yes |
| 6 | 7.3 | Update control | Not confirmed | Yes |
| 7 | 8 | Alex commission clause placement | Should this clause be in this agreement or in a separate side-letter to Alex only? Legal counsel to advise. | Yes |
| 8 | 11 | SaMD Condition Precedent — Bell Gully Phase 1 completion | Not yet complete | Yes |
| 9 | 16.2 | Insurance: PI + cyber policy with AU territorial extension | Not yet in place | Yes |
| 10 | 4.2 | My Health Record integration exclusion | Not discussed with Lawrence | No |
| 11 | 6.2 | Auto-renewal period (1-year vs mutual consent) | Legal counsel to advise | No |
| 12 | 13.3 | Confidentiality tail period (3 vs 5 years) | Legal counsel to advise | No |
| 13 | 14.1 | Liability cap structure and clinical harm carve-out | Legal counsel to draft | No |
| 14 | 15.1 | Governing law: NZ vs AU | Legal counsel to advise | No |
| 15 | 7.4 | ALEX API uptime SLA | Not discussed with Lawrence | No |

---

_First draft, 25 April 2026. Drafted by Claude Code for Ryo Eguchi, NexWave Solutions Limited. All output is a first draft only. This document is not final, not ready to send to any counterparty, and not ready to sign. Ryo must review every clause and every flag before this document is shared with legal counsel or Medtech Global. Legal counsel review required before any version is sent externally._
