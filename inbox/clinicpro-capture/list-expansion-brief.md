---
title: AU practice mailing list expansion brief
created: 2026-04-26
status: draft
---

> **First draft for human review. All estimates, tactics, and compliance guidance require Ryo's review before acting on any of them.**

---

## Summary

Top 3 sources ranked by reachable yield with low or zero budget:

1. **Healthdirect NHSD + AHPRA cross-reference** (data.gov.au supplemented): free, yields a complete AU GP practice list (~7,400 practices), filterable by state. Medtech verification is indirect but achievable via follow-on LinkedIn/web scraping. Estimated quality contacts after Medtech filter: 400-700.
2. **LinkedIn Sales Navigator targeted search**: paid tool (~AUD 110/month), but yields pre-qualified GP principals and practice managers. Medtech-relevant practices can be inferred from profile keywords. Estimated reachable contacts: 100-250 in first pass.
3. **GPCE conference attendee/exhibitor network**: Medtech Global exhibits at GPCE (Sydney May 2026, Melbourne July 2026). Their booth attendees are definitionally Medtech Evolution users. Networking plus public exhibitor and CPD attendance lists yields 50-150 warm contacts per event.

Estimated total reachable list size across all sources: **300-700 quality contacts** in the Medtech Evolution subset, filtered to GP principals and practice managers.

Timeline to 100+ contacts: 2-3 weeks of part-time work if NHSD and LinkedIn are pursued in parallel. Timeline to 400+: 4-6 weeks including GPCE Sydney (May 2026).

---

## Source breakdown

| Source | Effort (1-5) | Est. yield | Medtech-verified? | Notes |
|---|---|---|---|---|
| Healthdirect NHSD (API or AURIN dataset) | 3 | 500-1,000 raw contacts; 400-700 after Medtech filter | Indirect (requires web/LinkedIn scrub per practice) | Free dataset. ~7,400 GP practices. No EMR field in NHSD, so Medtech verification requires secondary lookup. |
| AHPRA register | 2 | 10,000+ GP names and registration numbers | No | Gives GP names by state; no contact details or practice affiliation. Useful as cross-reference, not standalone. |
| data.gov.au GP workforce/facility datasets | 2 | 7,400 practice locations | No | Geospatial and workforce data. No EMR field. Use to build state-filtered practice list; verify EMR separately. |
| LinkedIn Sales Navigator | 3 | 100-250 targeted contacts | Partial (keyword inference only) | Best tool for "GP Principal" + "Medtech" keyword in bio. ~AUD 110/month. Not free. |
| GPCE conference network (Sydney May 2026, Melbourne Jul 2026) | 3 | 50-150 per event | High (Medtech booth attendees) | Medtech Global exhibits at GPCE. Their session attendees and booth visitors are likely Evolution users. Public attendee list not available; requires in-person outreach or pre-event LinkedIn targeting of registered attendees. |
| Direct PHN outreach | 4 | Variable; 20-80 per PHN region | Indirect | 31 PHNs exist. Some publish practice lists; most require a request. PHNs are likely to share lists if framed as a clinical tool (not marketing). Slow. |
| Reddit/Facebook GP groups (AU) | 2 | 20-60 opt-in leads | No | "GP Down Under" Facebook group, Sermo AU, RACGP community forums. Post as a GP peer, not marketer. Slow burn but high trust. |
| Medtech Global partner/customer event | 2 | 30-80 high-quality contacts | Very high | Lawrence Peterson can share or introduce Ryo to the AU Evolution practice community as part of the bundle deal. Zero cost. Gated on bundle deal closing. |
| GP Jobs/recruitment sites (HPG, Prospect Health) | 1 | 20-40 practice manager contacts | No | Job listings name the practice and sometimes the contact. Niche; not scalable. |

---

## Tactics per source

### 1. Healthdirect NHSD + data.gov.au

**Step 1: Get the practice list.**
- Option A (fastest): Download the AURIN dataset "Healthdirect NHSD Services Directory 2023" from https://data.aurin.org.au/dataset/healthdirect_nhsd_services_directory_2023. Free, no API credentials required.
- Option B (freshest): Register for NHSD API access at https://developers.nhsd.healthdirect.org.au. FHIR R4 endpoints. Requires a brief approval process (days, not weeks). Returns GP practice name, address, phone, and sometimes practice email for ~7,400 practices.
- Filter to practice type: "GP (General Practice)."
- Filter by state: Victoria, Queensland, Western Australia (see targeting criteria below for rationale).

**Step 2: Medtech verification.**
- For each practice, run a Google/LinkedIn search: "[Practice name] Medtech" or "[Practice name] EMR."
- Medtech Global lists practice case studies and blog posts naming AU Evolution customers. Scrape these first.
- Cross-reference with the Medtech GPCE exhibitor page: https://www.gpce.com.au/melbourne/en-gb/exhibitor-details.org-e9b14ce3-0e43-4d25-bbe6-42a045f4c709.html
- Target: verify 80-100 practices before sending any email. Do not email unverified practices with Medtech-specific copy.

**Step 3: Find the decision-maker.**
- For verified Medtech practices, search LinkedIn or the practice website for "Practice Manager" or "GP Principal."
- Fallback: use the practice's general contact email with `{{role}}` personalisation ("Hi, I'm writing to the practice manager at [practice]").

---

### 2. LinkedIn Sales Navigator

**Search query structure:**
```
Title: "Practice Manager" OR "GP Principal" OR "General Practitioner"
Keywords: "Medtech" OR "Medtech Evolution"
Location: Australia
```
Secondary search without Medtech keyword, filtered by practice size (solo or small group, 1-10 employees).

**Connection approach:**
- Do not cold connect. Send InMail only.
- Frame as GP-to-GP peer message, identical tone to champion-email-v1.md.
- Mention ALEX API and "cloud Medtech" to signal legitimate insider knowledge; filters out non-users quickly.
- Volume: 20-30 InMails per week on Sales Navigator (within platform limits).
- Expected reply rate from GP peer message: 5-15% based on NZ equivalent.

**Cost:** AUD ~110/month for Sales Navigator Core. One month is sufficient for an initial pass.

---

### 3. GPCE Sydney (15-17 May 2026)

**Pre-event:**
- Search GPCE Sydney attendee list or event app (if published) for GPs and practice managers.
- LinkedIn search: "[person] GPCE 2026" or filter by "attending GPCE" in event RSVPs.
- Reach out to 30-50 attendees before the event via LinkedIn with a short peer message.

**At the event:**
- Medtech Global will exhibit (confirmed: GPCE Melbourne exhibitor page). Visit their booth. Ask Lawrence or his team to introduce you to attending Evolution practices. This is a low-cost tactic if the bundle deal is in motion.
- Collect business cards. Any GP who stops at the Medtech booth is a confirmed Evolution user.

**Post-event:**
- Follow up within 48 hours via LinkedIn or email. Reference the specific session or booth conversation.
- Expected yield: 50-100 warm contacts per event, 60-80% verifiable Medtech users.

---

### 4. PHN direct outreach

**Which PHNs to contact first (based on Medtech AU concentration, see targeting criteria):**
- Western Victoria PHN
- Gippsland PHN (Victoria)
- Metro North PHN (Queensland)
- WA Primary Health Alliance

**Framing:**
- Do not frame as a marketing request. Frame as: "We are launching a clinical image capture tool for Medtech Evolution practices. We would like to notify practices in your region. Can you share your practice list or forward on our behalf?"
- PHNs are often willing to forward vendor communications to member practices if the tool is clinically relevant and vendor is credentialled.
- Offer a short clinical brief (not a sales sheet) for the PHN to assess.

**Expected response:** variable. Some PHNs publish lists publicly (check individual PHN websites). Others will forward on your behalf. Expect 2-4 week turnaround.

---

### 5. Medtech Global as a channel (bundle deal dependency)

This is the highest-yield zero-cost tactic, but it is gated on Lawrence signing the bundle deal.

Once signed, Lawrence's team manages the AU Evolution practice community. Ask Lawrence to:
- Include ClinicPro Capture in Medtech's existing AU customer newsletter.
- Host a 30-minute webinar for AU practices on Capture as part of the bundle launch.
- Share the onboarding link with practice managers in the AU Evolution portal.

If this channel opens, it bypasses the entire list-building problem. **Prioritise closing the bundle deal before investing >20 hours in list building.**

---

## Targeting criteria

### Role
Priority 1: Practice Manager (controls purchasing decisions, manages workflows, handles new tools)
Priority 2: GP Principal / GP Owner (clinical champion, clinical sign-off, often the same person)
Priority 3: GP registrar or staff GP (referrer only, lower conversion)

### Practice size
Target: 3-10 GPs (medium-sized). Rationale: solo practices have low volume justification for Capture; very large practices (>15 GPs) have longer procurement cycles and IT gatekeepers.

### Geography: AU states with highest Medtech Evolution penetration
Medtech Evolution is predominantly used in Victoria, Queensland, and Western Australia based on Medtech Global's historical AU market entry (NZ-origin product, VIC was the initial AU beachhead). NSW is dominated by Best Practice and MedicalDirector.

**Assumption (confidence ~70%):** Medtech AU practice distribution skews VIC/QLD/WA. This is an inference from Medtech Global's AU company presence and conference footprint, not published market share data. Confirm with Lawrence before weighting list-building effort.

Priority states: Victoria, Queensland, Western Australia.
Deprioritise: New South Wales, South Australia (Best Practice and MD dominate).

### Urban vs regional
Lean urban/suburban (metro and outer metro). Rationale:
- Higher practice density makes list-building efficient.
- Cloud Medtech adoption tends to be higher in urban practices (better connectivity, newer infrastructure).
- Regional practices are more likely on on-premise Medtech which may behave differently with ALEX.
Do not exclude regional entirely: QLD and WA regional practices often have higher Medtech penetration than the national average.

---

## Medtech verification approach

The NHSD and AHPRA datasets contain no EMR field. Verification is a manual or semi-automated step.

**Tier 1 verification (high confidence):**
- Practice is named in a Medtech Global case study, press release, or GPCE exhibitor material.
- GP's LinkedIn profile mentions "Medtech" or "Medtech Evolution."
- Practice website references Medtech Evolution in its technology or patient information pages.

**Tier 2 verification (medium confidence):**
- Practice is located in a state with high Medtech penetration (VIC, QLD, WA) and is of a size/vintage consistent with Evolution usage (established practice, not a new startup likely on Bp Premier cloud).
- Practice lists "online bookings via HotDoc" (HotDoc has a Medtech Evolution integration; practices using both are verified Evolution users with high probability).

**Tier 3 (speculative, use with caution):**
- Practice is in a VIC/QLD/WA suburb with a cluster of known Evolution practices nearby.

**Recommendation:** only send the full Medtech-specific champion email (with ALEX API language) to Tier 1 and Tier 2 verified contacts. For unverified contacts, use a softer variant that does not assume Medtech usage: "if your practice uses Medtech Evolution..."

---

## AU Spam Act compliance checklist

The Spam Act 2003 (Cth) applies. ACMA guidance as of July 2024 is the current standard.

| Requirement | Detail | Status for this campaign |
|---|---|---|
| Consent | Express or inferred. For B2B cold outreach to published business email addresses: **inferred consent is permissible if** (a) the email address is conspicuously published online AND (b) the message is directly related to the recipient's role or function AND (c) there is no "no commercial messages" statement alongside the address. | Permissible for practice email addresses published on practice websites, healthdirect, or NHSD. NOT permissible for personal Gmail/Hotmail addresses harvested from AHPRA. |
| Sender identification | Every email must clearly identify the sender and their contact details. | Include: Dr Ryo Eguchi, ClinicPro, ryo@clinicpro.co.nz. Do not send from a generic or masked address. |
| Unsubscribe mechanism | Every commercial email must include a functional unsubscribe mechanism. Recipient must be removed within 5 working days of request. No account creation required to unsubscribe. | Mailmeteor (currently used for NZ campaign) supports one-click unsubscribe. Confirm before AU send. |
| Unsubscribe list maintenance | Once a contact unsubscribes, they must not be re-contacted. Maintain a suppression list. | Create and maintain an AU suppression list separate from NZ. |
| Content | Must not be false or misleading. | Champion email copy is accurate. Review before AU adaptation: remove NHI references, replace with IHI. Remove "referral-images" reference (not an AU product). |
| Penalties | Up to AUD 220,000 per breach for a single infraction. Serious/repeat: up to AUD 2.1M. Pizza Hut fined AUD 2.5M (2024). CBA fined AUD 7.5M (2024). | Low risk at 100-500 emails if consent basis is sound and unsubscribe is functional. Risk increases sharply if you re-contact after unsubscribe. |

**Key compliance risk for this campaign:**
The NZ champion email explicitly references "you've been using referral-images." This is a relationship-based consent basis (existing ClinicPro user). The AU list has no such existing relationship. AU contacts will require inferred consent based on conspicuous publication plus role relevance. This is a weaker consent basis. Mitigate by:
1. Only emailing addresses published on practice websites or NHSD (not scraped from personal social profiles).
2. Including a clear unsubscribe link from the first email.
3. Keeping volume low and targeted (100-500 total, not bulk blast).
4. Adapting the email to not claim an existing relationship: open with context about what ClinicPro Capture does, not "you've been using X."

**Assumption (confidence ~85%):** role-relevant B2B outreach to publicly published practice email addresses qualifies for inferred consent under the Spam Act. This is based on ACMA guidance and multiple legal commentaries, but has not been confirmed by AU legal counsel. Recommend a brief email to Helen's AU tax contact or a commercial law firm (Corrs, Addisons, Norton Rose) to confirm before sending at scale.

---

## Recommended next step

**Immediate (this week):**
1. Prioritise closing the Lawrence bundle deal. If it closes, Medtech becomes the channel and list-building effort drops significantly.
2. Download the AURIN NHSD dataset (free, no approval needed): https://data.aurin.org.au/dataset/healthdirect_nhsd_services_directory_2023. Filter to GP practices in VIC, QLD, WA.
3. Adapt the champion email for AU: remove NHI/referral-images references, add IHI context, change consent framing from existing-relationship to role-relevant inferred.

**Week 2-3:**
4. Manual Medtech verification pass: identify 80-100 Tier 1/2 verified Medtech practices from the NHSD list.
5. Find practice manager or GP principal contact for each via LinkedIn or practice website.
6. Send AU champion email batch 1 (15-20/day in Mailmeteor, personal Gmail account as per NZ plan).

**Before GPCE Sydney (15 May 2026):**
7. Register for GPCE Sydney (or attend as a vendor with Medtech if bundle deal is signed).
8. Pre-target 30-50 confirmed attendees via LinkedIn.

---

## Assumptions

1. Medtech Evolution is used by 500-800 AU practices (provided in brief). No public source confirmed this figure. Confidence ~65%. If lower (200-400), total reachable list is 150-350, not 400-700.
2. VIC/QLD/WA have higher Medtech Evolution penetration than NSW/SA/TAS. Inferred from Medtech Global's AU company footprint and conference presence. Confidence ~70%. Confirm with Lawrence.
3. Inferred consent via conspicuous publication is valid for this campaign. Based on ACMA guidance and legal commentary. Not confirmed by AU legal counsel. Confidence ~85%. Get a written opinion before sending at scale.
4. AURIN NHSD dataset (2023 vintage) is sufficiently current for practice contact details. Some practices will have moved or closed. Expect 10-20% dead addresses.
5. HotDoc/Medtech Evolution co-use is a reliable Tier 2 Medtech verification signal. Based on known integration; not independently verified for AU. Confidence ~75%.
6. Sales Navigator InMail reply rate of 5-15% for GP peer messaging. Extrapolated from NZ champion email expectations in the existing brief. AU cold contacts will likely perform lower end (5-8%). Confidence ~60%.
7. GPCE Sydney 2026 is confirmed for 15-17 May 2026. Source: gpce.com.au. Confidence ~95%.
