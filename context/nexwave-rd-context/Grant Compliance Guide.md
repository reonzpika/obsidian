# Grant Compliance Guide
## NZ-Sovereign Clinical LLM for GP Workflow

> **Purpose:** Operational reference for grant compliance obligations. Covers quarterly reporting, record-keeping, capability development requirements, and NZ regulatory context.
> **Source documents:** MBIE N2RD Funding Agreement (example), Capability 5 (Project Management), Capability 6 (R&D Information Management).
> **Last updated:** March 2026

---

## 1. Quarterly Obligations — Non-Negotiable

**Claims must be submitted at least once per quarter.** Cannot be less frequent. Can be more frequent.

Each quarterly submission must include:

- **GST Invoice** for Approved Eligible Costs being claimed
- **Progress report** covering:
  - Performance of R&D and Capability Development to date against the approved application
  - Costs incurred to date in Excel format against the approved Cost Template
  - Any matter that may affect ability to complete R&D or Capability Development
  - Supporting invoices for any expenditure over NZ$2,500
- **R&D documentation** sufficient to demonstrate systematic investigation (experiment logs, decisions, results)

**If the quarterly report is not received, Callaghan Innovation is not obliged to make payment.**

### Quarterly schedule

| Quarter | Period | Claim due |
|---|---|---|
| Q1 | 12 Mar–11 Jun 2026 | End June 2026 |
| Q2 | 12 Jun–11 Sep 2026 | End September 2026 |
| Q3 | 12 Sep–11 Dec 2026 | End December 2026 |
| Q4 | 12 Dec 2026–11 Mar 2027 | End March 2027 |
| Q5 | 12 Mar–11 Jun 2027 | End June 2027 |
| Q6 | 12 Jun–11 Sep 2027 | End September 2027 |
| Q7 | 12 Sep–11 Dec 2027 | End December 2027 |
| Q8 | 12 Dec 2027–11 Mar 2028 | End March 2028 |

**Final claim and final report:** Due no later than 3 months after contract end date (11 March 2028), so by 11 June 2028. If not received by due date, Callaghan Innovation is not liable to make final payment.

---

## 2. Record-Keeping Requirements

You must keep full, accurate, up-to-date records for:

- All R&D activities and decisions (experiment design, methodology, results, conclusions)
- All Capability Development activities (training undertaken, skills gained, systems set up)
- All expenditure with supporting documentation
- Any cost variances from the approved Cost Template

**Retention period: 7 years from expiry or termination of the agreement.**

Records must be available for audit by Callaghan Innovation or authorised agents on request, at no cost to them, in any format they reasonably require.

---

## 3. Change Event Obligations

A Change Event must be reported immediately if any of the following occur:

- Something prevents (or is likely to prevent) you from meeting grant obligations
- Loss of co-funding (including Ting's shareholder reserve)
- Scientific or technical approach changes significantly
- Loss of critical resources (key people, infrastructure)
- Change in control of Nexwave Solutions Limited
- Anything that puts your ability to complete R&D or Capability Development at serious risk

**If a Change Event occurs:** notify Callaghan Innovation in writing immediately. Do not wait for the quarterly report.

### R&D Change Request
If you want to redirect unclaimed funds to different R&D than described in the application, submit an R&D Change Request. Approved at MBIE's sole discretion.

### Capability Development Change Request
If you want to add additional Capability Development activities, submit a Capability Development Change Request. Note: Approved Eligible Costs cannot be increased for R&D, only for Capability Development.

---

## 4. Capability Development — What Success Looks Like

You selected three capability development areas. MBIE expects you to demonstrate genuine capability building, not just spend the budget.

### Capability 5: Project Management ($8,000 | Feb 2026–Jun 2027)

**What MBIE expects you to demonstrate:**

- Budget management systems in place and being used
- Resource management processes documented
- Roadmaps/plans visualising tasks across the project lifecycle
- Periodic reviews conducted and documented
- Documentation of project progress, budget/schedule changes and rationale
- Risk register maintained with mitigation plans

**How this maps to your project:**
The `rd-programme-tracker.md` file directly satisfies this requirement — it tracks milestones, records decisions with rationale, and logs open questions. Ensure Ting (Operations Lead) is demonstrably involved in maintaining it and that budget tracking is documented alongside R&D progress.

### Capability 6: R&D Information Management ($10,000 | Feb–Sep 2026)

**What MBIE expects you to demonstrate:**

- Centralised experiment tracking system set up and in use
- Model registry and dataset lineage workflows established
- Research outputs (experiments, results, conclusions) stored centrally and accessibly
- Trend tracking across research metrics possible from the system
- Data privacy protections in place for the information management system

**How this maps to your project:**
The experiment tracking system (likely MLflow or equivalent) and dataset lineage tooling to be set up in Obj 1 directly satisfy this. The technical consultant engaged under this capability should train you in industry-standard MLOps practices. Deliverable: a working experiment tracking system with documented methodology by September 2026.

### Regulatory & Compliance ($18,000 | Feb 2026–Jul 2027)

**What MBIE expects you to demonstrate:**

- Genuine capability uplift in regulatory knowledge, not just consultant fees
- Documented learnings from each engagement
- Compliance frameworks and templates built that apply beyond this project
- DPIA methodology learned and applied

**How this maps to your project:**
Each regulatory engagement should produce a documented output (gap analysis, compliance framework, risk assessment) that you retain and can demonstrate to MBIE. Not just invoices for consultant time.

---

## 5. Publicity Obligations

Any media release or public statement that refers to Callaghan Innovation or MBIE, or includes quotes from their staff, must be approved in writing by them at least 48 hours before publication.

Any public statement relating to your Total Eligible Costs must reference your participation in the New to R&D Grant Scheme.

Notify Callaghan Innovation of any media enquiries about your R&D or Capability Development.

---

## 6. NZ Regulatory Context — SaMD and AI

### Current status (March 2026)

NZ's regulatory framework for Software as a Medical Device (SaMD) is in flux. The key facts:

- The Therapeutic Products Act 2023 (TPA) was passed but subsequently repealed before taking effect. The TPA would have required pre-market approval for SaMD based on risk classification.
- Under the current Medicines Act 1981, there is no general pre-market approval requirement for medical devices. Devices can be supplied via a simple notification to the WAND database (Web Assisted Notification of Devices).
- A Medical Products Bill is in progress. It is expected to include SaMD regulation aligned with IMDRF international standards. Timeline unclear as at March 2026.
- NZ does not currently require adverse event reporting for SaMD, meaning there are minimal regulatory barriers to market for your current development phase.

### What this means for your project

- **For the R&D programme (Jan 2026–Jan 2028):** Current low-barrier environment gives you runway to develop and validate before formal regulatory obligations apply. Use this time to build compliant documentation practices.
- **Assist-only classification:** Your product's assist-only design (AI supports GP, never replaces clinical judgement) is the right positioning for minimising regulatory risk under any future framework.
- **Watch closely:** The Medical Products Bill may pass during your grant period. If it includes SaMD pre-market approval requirements, you will need to factor in compliance pathways before commercial launch.
- **TGA (Australia) precedent:** The Australian TGA explicitly regulates LLMs with a medical purpose as medical devices. NZ is likely to follow a similar approach under future legislation. Design your product with this in mind from the start.

### Action item
Engage the regulatory compliance consultant (budgeted, Obj Capability Development) early in 2026 to monitor the Medical Products Bill and advise on proactive compliance positioning. Do not wait until the Bill passes.

---

## 7. Co-Funding Reminder

The 40/60 grant split means for every dollar you spend on eligible R&D, MBIE pays 40 cents and you must demonstrate 60 cents of your own money.

Your Required Co-Funding must not come from any public sector agency or entity. The approved sources are:
- GP clinical income ($11,117/month)
- Opening bank balance ($111,477.62)
- Term deposit ($30,270.87, matured March 2026)
- Shareholder reserve — Ting ($100,000 available; $35,000 drawn Month 12)

**Do not let the co-funding balance fall below the required 60% at any point.** This is a clawback risk.