# ClinicPro Capture: Australian Privacy Policy

> DRAFT -- for legal review before publication. Not yet in effect.

---

## 1. Who we are

ClinicPro is a product of NexWave Solutions Limited, a New Zealand company (referred to as "we", "us", or "ClinicPro"). ClinicPro Capture is a clinical image capture application for GP practices running Medtech Evolution practice management software.

We operate in Australia and handle information in accordance with the Privacy Act 1988 (Cth) and the Australian Privacy Principles (APPs).

**Note on the small business operator exemption:** The Privacy Act exempts businesses with annual turnover under AUD 3 million. However, that exemption does not apply to health service providers. ClinicPro is a health software vendor, not a health service provider. Our exemption status requires legal confirmation before publication. We treat the APPs as binding regardless.

Contact: ryo@clinicpro.co.nz

---

## 2. What information we collect

ClinicPro Capture collects a limited set of information to operate the service:

**Authentication data**
- Phone number or email address used to sign in via one-time passcode (OTP).
- No passwords are stored.

**Audit log data**
- A record of each capture event: which staff member performed the capture, when, and the patient ID from the practice's Medtech system.
- No patient name, date of birth, address, or clinical content is stored in our system.

**Practice configuration data**
- Tenant setup details: practice name, Medtech instance identifiers, and staff user records.

**Clinical images**
- We do not store clinical images. Images captured through the app are transmitted directly to the practice's Medtech Evolution system via the ALEX FHIR API and are never written to ClinicPro infrastructure.

---

## 3. Why we collect it

| Data | Purpose |
|---|---|
| Authentication data | To verify staff identity and control access to the app |
| Audit log | To provide practices with a record of capture activity for governance and compliance |
| Practice configuration | To operate the service for each practice tenant |

We collect only what is necessary for these purposes (APP 3 -- collection of solicited personal information).

---

## 4. How we use and disclose it

We use your information only for the purposes described above. We do not sell, rent, or share personal information with third parties for marketing.

We may disclose information to:

- **Medtech Global** -- to pass capture events through the ALEX FHIR API to your practice's Medtech system. Medtech Global is the data processor for your clinical record system.
- **Infrastructure subprocessors** -- AWS (Sydney, ap-southeast-2) and Supabase (AU region, subject to confirmation) for hosting and data storage. Vercel for frontend delivery.
- **Legal or regulatory bodies** -- if required by law, court order, or regulatory authority.

We do not disclose audit log data to other practices or third parties.

---

## 5. Cross-border disclosure

Our company is based in New Zealand. Some system components involve cross-border data flows:

- **New Zealand:** Our backend-for-frontend (BFF) server operates in New Zealand. Authentication and audit log data may transit through NZ infrastructure.
- **Medtech Global:** Medtech Evolution is a New Zealand product. API calls to the ALEX FHIR endpoint may route through Medtech Global's NZ infrastructure.

New Zealand has been recognised as having comparable privacy protections to Australia's framework. Where personal information is disclosed overseas, we take reasonable steps to ensure recipients handle it in a way consistent with the APPs (APP 8).

---

## 6. Storage and security

- Data is stored in Australia where technically possible. Auth and audit data: AWS ap-southeast-2 (Sydney) and Supabase AU region (TBC at launch).
- We retain authentication and audit log data for [7 years, TBC -- align with health record retention norms and legal advice].
- Security measures include: OTP-only authentication (no passwords), encrypted data in transit (TLS), encrypted data at rest, and access controls limiting staff to their own practice data.
- We do not retain clinical images at any point.

---

## 7. Your rights

Under the Privacy Act 1988 (Cth), you have the right to:

- **Access** personal information we hold about you (APP 12). Submit a request to ryo@clinicpro.co.nz. We will respond within 30 days.
- **Correct** personal information that is inaccurate, out of date, or incomplete (APP 13). Contact us at the same address.
- **Complain** about our handling of your personal information (see below).

If you believe we have interfered with your privacy, contact us first. If we do not resolve your complaint within 30 days, or you are not satisfied with our response, you may complain to the Office of the Australian Information Commissioner (OAIC):

- Website: www.oaic.gov.au
- Phone: 1300 363 992
- Post: GPO Box 5218, Sydney NSW 2001

---

## 8. Cookies and analytics

ClinicPro Capture is a progressive web app (PWA). We use minimal analytics. Vercel Analytics may collect anonymised page-level usage data (no personal identifiers). We do not use advertising cookies or third-party tracking pixels.

---

## 9. Contact us

Privacy enquiries, access requests, and correction requests:

**ClinicPro / NexWave Solutions Limited**
Email: ryo@clinicpro.co.nz

---

## 10. Updates to this policy

We may update this policy from time to time. Material changes will be notified to practice administrators by email before they take effect. The current version will always be available at clinicpro.co.nz/au/privacy (URL TBC).

Last reviewed: [Date TBC -- insert before publication]

---

---

# ClinicPro Capture: Incident Response Plan -- Notifiable Data Breaches (NDB Scheme)

> DRAFT -- for legal review before publication. Not yet in effect.

Version: 0.1 | Status: Draft | Owner: Ryo (Founder/CTO), NexWave Solutions Limited

---

## 1. Purpose and scope

This plan sets out how ClinicPro responds to actual or suspected data breaches involving personal information held in the ClinicPro Capture system.

**Scope:** All personal information processed by ClinicPro Capture, including authentication data, audit logs, and practice configuration data. Clinical images are out of scope (ClinicPro does not retain them).

**Legal basis:** Part IIIC of the Privacy Act 1988 (Cth) -- the Notifiable Data Breaches (NDB) scheme.

---

## 2. What is a notifiable data breach

An **eligible data breach** exists when all three of the following apply:

1. There has been unauthorised access to, or unauthorised disclosure of, personal information held by ClinicPro; or personal information has been lost in circumstances where unauthorised access or disclosure is likely.
2. The information concerns one or more individuals who can be identified.
3. The breach is likely to result in **serious harm** to any of those individuals.

Serious harm is assessed against factors including the sensitivity of the information, the likelihood of harmful use, and the vulnerability of affected individuals. Health information (including patient IDs linked to a health context) is treated as inherently sensitive and raises the threshold for what constitutes serious harm risk.

**Not every incident is an NDB.** Security events that are contained before any information is accessed, or that affect de-identified data only, are unlikely to be eligible data breaches. Assessment (Section 6) determines this.

---

## 3. Roles and responsibilities

ClinicPro is a solo founder company. Roles are concentrated accordingly.

| Role | Person | Responsibility |
|---|---|---|
| Incident Lead | Ryo (Founder/CTO) | Owns detection, assessment, containment, notification, and post-incident review |
| Legal counsel | TBC -- engage on confirmation of eligible breach | Advises on notification obligations, drafts comms |
| Affected practice contact | Practice Manager (per tenant) | First point of contact for affected practice notification |

Engage legal counsel as soon as an eligible data breach is confirmed or considered likely. Do not delay notification pending counsel if the 30-day assessment window is at risk.

---

## 4. Detection and initial assessment

**Sources of detection:**
- Automated alerts from AWS CloudWatch or Supabase logs (anomalous access patterns, auth failures, unusual query volumes)
- User or practice reports
- Third-party security researchers
- Routine log review

**When a potential breach is identified:**

1. Log the date and time of detection. The **30-day assessment clock starts from the day you first suspect an eligible data breach may have occurred** (s26WA Privacy Act).
2. Assign severity: Low (likely no personal information affected), Medium (personal information may be affected), High (personal information confirmed affected or likely).
3. Escalate immediately to Incident Lead (Ryo).
4. Do not delete, modify, or overwrite any logs or infrastructure state until assessment is complete.

---

## 5. Containment steps

Act immediately on confirmation of a suspected breach. Containment is not admission of an NDB.

**Technical containment:**
- Revoke compromised credentials or API keys.
- Disable affected user accounts or tenant access.
- Rotate Supabase service role keys and BFF internal secrets if potentially exposed.
- Isolate affected infrastructure if the breach is active.
- Preserve logs: export and archive CloudWatch logs, Supabase audit logs, and Vercel access logs before any remediation steps that might overwrite them.

**Communication containment:**
- Do not make external statements about the incident until the assessment in Section 6 is complete.
- Notify affected practice managers that a security investigation is underway, without confirming breach status.

---

## 6. Assessment: is it an eligible data breach?

Complete the assessment within **30 days** of first suspicion. Document every step.

Answer the following questions:

1. **Was personal information accessed or disclosed without authorisation, or lost in circumstances likely to lead to such access?**
   - If No: incident is not an eligible data breach. Document and close. Continue monitoring.
   - If Yes or unclear: continue.

2. **Can the affected individuals be identified from the information?**
   - ClinicPro audit logs contain staff user IDs and patient IDs. Both are likely identifiable in the context of a specific practice. Answer is typically Yes.

3. **Is the breach likely to result in serious harm?**
   - Consider: sensitivity of information, nature of the unauthorised recipient, steps taken to contain, whether information has been or is likely to be misused.
   - Patient IDs linked to a health context are health-adjacent information. Treat as sensitive. Default to Yes unless there is clear evidence of no harm pathway.

If all three answers are Yes: the breach is an eligible data breach. Proceed to Section 7.

If the assessment cannot be completed within 30 days, notify the OAIC anyway. Do not wait.

---

## 7. OAIC notification (mandatory)

**Trigger:** Confirmation of an eligible data breach.

**Timing:** As soon as practicable after the eligible data breach is confirmed.

**Method:** Submit a statement to the OAIC using Form NDB 1, available at www.oaic.gov.au/privacy/notifiable-data-breaches/report-a-data-breach.

**Required content (s26WB Privacy Act):**
- Identity and contact details of ClinicPro.
- Description of the breach (what happened, when, how).
- Description of the information involved.
- Recommendations for affected individuals on steps they should take.

Submit via the OAIC online portal or by email to the address provided on the form.

Keep a copy of the submitted statement and all supporting documentation.

---

## 8. Individual notification (mandatory)

**Timing:** As soon as practicable after lodging the OAIC statement. The OAIC may also direct the form of individual notification.

**Who to notify:** All individuals whose information was involved in the breach who are at risk of serious harm, or, if not practicable to identify all individuals, all individuals whose information may have been involved.

In a ClinicPro context, this means:
- Staff members whose authentication data was exposed.
- Practices whose patient IDs appeared in an exposed audit log. The practice is the appropriate point of contact for patient notification, as ClinicPro does not hold patient demographics.

**How to notify:**
- Staff users: direct email to the registered email or phone number.
- Practices: email to the practice manager on record. The practice should then determine whether individual patient notification is required at their level.

**Required content of notification:**
- Description of the breach.
- What information was involved.
- What steps ClinicPro has taken or will take.
- Recommended steps for the individual to protect themselves.
- Contact details for ClinicPro and the OAIC.

If the OAIC directs a different notification approach, follow that direction.

---

## 9. Post-incident review

Within 14 days of resolving the incident, conduct a written post-incident review covering:

- Timeline: detection, containment, assessment, notification.
- Root cause analysis.
- What data was exposed, for how long, and to whom.
- Effectiveness of containment.
- Gaps in monitoring, access controls, or process.
- Remediation actions taken and outstanding.
- Process improvements to prevent recurrence.

Share the review with legal counsel. File in the incident register (Section 10).

---

## 10. Record-keeping

Maintain an incident register. Each entry must include:

| Field | Detail |
|---|---|
| Incident ID | Sequential number (e.g. INC-2026-001) |
| Date detected | ISO 8601 |
| Date assessment completed | ISO 8601 |
| Eligible data breach? | Yes / No / Inconclusive |
| OAIC notified | Yes / No / N/A, with date |
| Individuals notified | Yes / No / N/A, with date and method |
| Root cause summary | One paragraph |
| Remediation status | Open / Closed |
| Post-incident review filed | Yes / No, with location |

Retain incident records for a minimum of 7 years.

The OAIC may request access to records at any time. Do not delete or alter records after an incident.

---

*End of document.*
