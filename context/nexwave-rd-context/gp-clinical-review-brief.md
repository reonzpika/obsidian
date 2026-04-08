---
title: NexWave Health — GP Clinical Review Brief
type: context
project: nexwave-rd
objective: obj-1
created: 2026-04-08
status: active
---

# NexWave Health — GP Clinical Review Brief

**Thank you for taking the time to do this.** This brief is the only document you need to read. It takes 20–30 minutes to work through and respond to. You do not need to review any other documents.

**What this is not:** This is not a request for College endorsement, ethical approval, or formal consulting. It is clinical input from one GP to another — validating that the logic we have designed matches real-world NZ practice before we build anything.

**What we are building:** Two AI-assisted tools for NZ GP practices, funded by MBIE under the New to R&D programme. Both tools are assist-only. The AI surfaces information. The GP makes every decision.

---

## Tool 1 — Inbox Helper

**The problem it solves:** A busy GP inbox contains 100-200 items per session. The PMS flags abnormal lab values, but a critical result can still sit unreviewed until the afternoon inbox session. Other document types — radiology reports, specialist letters with action requests, and discharge summaries — carry no urgency signal at all.

**What it enables:** Once items are triaged by urgency, Immediate and Urgent items surface to the top. Routine items and Information-only correspondence can be delegated to a nurse or HCA for filing. The GP plans the day around what actually needs attention, rather than working through the queue in arrival order.

Reads incoming documents in your Medtech inbox (lab results, radiology reports, discharge summaries, specialist letters, patient messages) and assigns each an urgency level.

**The output looks like this:**

> *Creatinine 198 umol/L, above reference range. Significant rise if new — requires assessment.* **[Urgent]** *GP to confirm whether this represents a change from the patient's established baseline.*

### Urgency Taxonomy

| Level | Label | Meaning | Example |
|---|---|---|---|
| 1 | **Immediate** | Review and action today. Risk to life or safety if not actioned same day. | K+ 6.8 mmol/L. Positive blood culture. Intracranial haemorrhage on CT. Acute suicidal ideation with plan. |
| 2 | **Urgent** | Action within 1–3 working days. Significant finding requiring early follow-up. | New malignancy on radiology. Creatinine rise above reference range. Pending culture result from a recent discharge. New serious diagnosis in a specialist letter. |
| 3 | **Routine** | Action at next scheduled contact or within 2 weeks. Clinically relevant but not time-critical. | HbA1c within agreed target range. Post-discharge follow-up with no time-bound action items. Standard outpatient review with ongoing management recommendation. |
| 4 | **Information only** | No active clinical action needed. Review, acknowledge, and file. | Normal result. Stable chronic condition confirmed within target range. Routine specialist review letter with no GP action required. |

**Design choice we want you to validate:** When a result is ambiguous and we cannot determine urgency with confidence, the system defaults to the *higher* urgency level. We have accepted over-triage as the trade-off. Missing a critical result is the outcome we are designing against.

### Question 1

> **Do the four urgency levels feel right in practice?**
> Are there common document types or clinical scenarios where you would classify something differently to what the table suggests? Please give a specific example if so.

---

## Tool 2 — Care Gap Finder

**The problem it solves:** Nurses and HCAs already do this work — pulling manual reports from the PMS to identify patients overdue for monitoring. But it is a point-in-time snapshot, not continuous monitoring. Patients fall due between report runs and are missed until someone remembers to pull the report again. Each outreach requires manual identification and manual patient contact.

**What it enables:** Continuous monitoring flags patients as they fall due, not only when a report is run. This helps practices stay on top of PHO enrolment targets without nursing staff time being consumed by periodic manual audits. It also creates the foundation for automated patient outreach — portal messages, SMS recalls — reducing the manual contact load further.

Scans your enrolled patient register and surfaces patients who are overdue for specific health monitoring. It is a population health tool — it works across your patient list, not on individual documents.

### Care Gaps in Scope (MVP)

| Care Gap | Condition | Trigger |
|---|---|---|
| HbA1c monitoring | T2DM / T1DM | Last HbA1c >4 months ago (if above target, ≥53 mmol/mol) or >7 months ago (if at target) |
| Diabetes annual review | T2DM / T1DM | Any of: uACR, creatinine/eGFR, lipid panel, LFTs, or LDL-C not done in past 13 months |
| Foot exam | T2DM / T1DM | No foot exam documented in past 13 months |
| CVDRA eligibility and recall | Age/ethnicity criteria per MoH 2018 | No CVDRA assessment within recall interval (5 years low risk; 1–2 years moderate/high risk) |
| Blood pressure monitoring | Hypertension (on treatment) | No BP recorded in past 6 months |

**Escalation flags** (surfaced separately as requiring GP review, not just routine recall):

| Condition | Flag |
|---|---|
| HbA1c ≥75 mmol/mol | Urgent — very poor glycaemic control |
| HbA1c >90 mmol/mol + symptoms | Immediate — insulin initiation likely indicated |

**Priority ordering logic:** If a patient with hypertension is also due for CVDRA but has no recent BP, the system flags the BP gap first — because a current BP is required to complete the CVDRA calculation. We flag the prerequisite ahead of the downstream task.

### Question 2

> **Do these care gap triggers and intervals match your practice rhythm?**
> Are there intervals you would adjust — either because they would generate too many low-value alerts, or because they would miss genuinely important cases? Are there any gaps in this list that you consider higher priority than what we have included?

---

## Question 3 — Blind Spots

> **Is there anything in either tool's logic that looks wrong, or something important we have not thought of?**
> This is deliberately open. You know your practice. We do not.

---

## How to Respond

Reply to this email with your answers to the three questions. A few sentences per question is enough — you do not need to write a report. If it is easier to talk through, happy to schedule a 20-minute call instead.

**There is no formal reimbursement for this review. As a small thank-you for your time, I would like to offer a $50 Prezzy card on receipt of your feedback.**

Questions or clarifications: ryo@clinicpro.co.nz

Ngā mihi,
Ryo Eguchi
GP | Founder — NexWave Health / ClinicPro
