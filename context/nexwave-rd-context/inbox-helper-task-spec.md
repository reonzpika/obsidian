---
title: Inbox Helper — Task Specification
type: context
project: nexwave-rd
objective: obj-1
step: step-1
created: 2026-04-03
status: final
---

# Inbox Helper — Task Specification

**Objective 1, Step 1 deliverable.** This document defines the Inbox Helper classification task in precise, testable terms. It is the foundation for all architecture evaluation, synthetic data design, and prototype work in Objective 1, and constitutes primary evidence for the MBIE Step 1 deliverable under contract CONT-109091-N2RD-NSIWKC.

---

## 1. Task Overview

The Inbox Helper reads incoming clinical documents in a New Zealand GP's Medtech inbox and assigns each an urgency level so the GP can prioritise their review queue. The AI surfaces information faster. The GP makes every clinical decision.

The system is assist-only. It never takes autonomous action, never contacts patients, and never modifies records. Its sole output is a structured urgency classification with a brief rationale.

---

## 2. In-Scope Input Types

| Document Type | Examples |
|---|---|
| Laboratory results | Biochemistry, haematology, microbiology, serology |
| Radiology reports | X-ray, CT, MRI, ultrasound |
| Discharge summaries | Hospital admissions, ED visits |
| Specialist / outpatient letters | Clinic letters, outpatient review letters, referral responses |
| Patient messages | Portal messages, staff-relayed patient queries (where enabled by practice) |

**Out of scope for MVP:** ACC correspondence, pharmacy / medication reviews, referral acknowledgements, screening recalls, inter-practice administrative messages.

---

## 3. Urgency Taxonomy

| Level | Label | Clinical Definition |
|---|---|---|
| 1 | **Immediate** | Requires review and action today. Risk to patient life or safety if not actioned same day. |
| 2 | **Urgent** | Requires action within 1–3 working days. Significant finding warranting early follow-up or contact. |
| 3 | **Routine** | Requires action at next scheduled contact or within 2 weeks. Clinically relevant but not time-critical. |
| 4 | **Information only** | No active clinical action required. Review, acknowledge, and file. |

**Design principle:** The system is recall-optimised, not accuracy-optimised. When content is ambiguous and urgency cannot be determined with confidence, the system classifies at the higher urgency level. Over-triage is the acceptable trade-off. Missing a critical result is not.

---

## 4. Document-Type Classification Criteria

### 4.1 Laboratory Results

Criteria aligned with the RCPA/AACB harmonised alert list for Australia and New Zealand (Campbell, Lam, and Horvath, 2019).

| Urgency | Criteria |
|---|---|
| Immediate | Critical values: K+ <2.5 or >6.2 mmol/L; Na <120 or >155 mmol/L; glucose <2.5 mmol/L; positive blood cultures (any organism); positive CSF cultures; detection of notifiable organisms. Any result meeting laboratory-defined critical value thresholds. |
| Urgent | Significant risk results: above reference range but below critical threshold; unexpected new abnormality not consistent with known condition; significant delta change from prior result (K+ absolute change ≥3.0 mmol/L; creatinine or glucose percentage change per lab-specific RCV thresholds); new microbiology growth below critical threshold. |
| Routine | Mild to moderate abnormality in the context of a known managed condition; result within target range for a chronic condition (e.g. HbA1c within agreed management target); expected variation consistent with prior results. |
| Information only | Normal result; result confirming stable managed condition within target range. |

### 4.2 Radiology Reports

Criteria aligned with the UK Academy of Medical Royal Colleges / RCR "Alerts and Notification of Imaging Reports: Recommendations" (October 2022) and ESR guidelines.

| Urgency | Criteria |
|---|---|
| Immediate | CRITICAL findings: tension pneumothorax, acute aortic dissection, intracranial haemorrhage, bowel perforation, ectopic pregnancy, spinal cord compression, acute pulmonary embolism with haemodynamic compromise, other findings explicitly marked critical by radiologist. |
| Urgent | CANCER alert: new malignancy or cancer recurrence detected. Significant amended report (addendum) that alters clinical management. Any unexpected serious finding not at the Immediate threshold. |
| Routine | Unexpected finding requiring follow-up per organ-specific guidelines (e.g. incidental pulmonary nodule ≥6mm per Fleischner Society 2017 guidelines; ACR Incidental Findings Committee guidance for renal, adrenal, liver, thyroid, adnexal). |
| Information only | Normal. Incidental finding below the threshold for follow-up per current guidelines. |

### 4.3 Discharge Summaries

**Important structural note:** NZ hospital discharge summaries do not follow a consistent machine-readable format. A dedicated "message for GP" section is often present when follow-up is required but is not universal. Action requests may appear in the plan section, the clinical body, or embedded in narrative prose. Full-document semantic reading is required. Structural extraction of a single section is insufficient.

| Urgency | Criteria |
|---|---|
| Immediate | Pending microbiology culture result with pathogen identified requiring urgent antibiotic action. Pending result returned after discharge that requires same-day clinical intervention. |
| Urgent | Any pending test result requiring GP action (e.g. pending pathology, pending imaging, pending cultures not yet grown); new serious diagnosis requiring early GP-initiated management; medication change requiring close monitoring (e.g. new anticoagulant, new drug with narrow therapeutic window); explicit instruction for GP follow-up within a specified number of days; patient discharged with unresolved clinical issue requiring early community review. RACGP recommends GP review within 7 days of most hospital admissions — any discharge summary indicating this need is Urgent. |
| Routine | Standard post-discharge GP follow-up with no time-bound action items; elective referral placed by secondary care; medication change for information with no monitoring requirement; stable management of known chronic condition. |
| Information only | Uncomplicated admission with no pending results and no GP action indicated; administrative discharge communication; no new clinical issues identified. |

### 4.4 Specialist / Outpatient Letters

**Important structural note:** NZ specialist letters have no standard section markers, urgency flags, or keyword conventions. A new serious diagnosis, urgent recommendation, or urgent medication change may appear in the summary at the top, within the body, or at the end of the letter. Location and phrasing are unpredictable across clinicians, specialties, and hospitals. Full-document semantic reading is required.

| Urgency | Criteria |
|---|---|
| Immediate | Rare. Explicit same-day GP action requested. Life-threatening finding requiring immediate intervention by GP. |
| Urgent | New malignant or serious diagnosis (found anywhere in the letter, regardless of framing); urgent investigation or urgent referral recommended; urgent medication change or initiation required by GP; explicit request for early GP action with or without a timeframe. |
| Routine | Standard outpatient follow-up letter; investigation results reviewed by specialist with standard ongoing management recommendation; ongoing management continuing under specialist care with no immediate GP action required. |
| Information only | Routine review letter; no GP action required; for information only. |

### 4.5 Patient Messages

**Important contextual note:** NZ patient portals (MyIndici, ManageMyHealth) are explicitly designed for non-urgent communication. Patients are directed to call 111 or phone the clinic for urgent matters. Accordingly, the prevalence of Immediate and Urgent messages in this category will be low. Content varies substantially by practice: some practices do not enable patient messaging at all.

| Urgency | Criteria |
|---|---|
| Immediate | Acute emergency symptoms described (chest pain, severe dyspnoea, acute confusion, active suicidal ideation with plan). These should be rare given portal design, but must not be missed. |
| Urgent | Symptoms or a clinical situation requiring assessment within days; medication urgency requiring a clinical decision; a patient safety concern requiring early GP response. |
| Routine | Script / prescription requests; appointment requests; non-urgent clinical queries; home monitoring data submission (e.g. home BP records, glucose diary). |
| Information only | Administrative messages; information requests; acknowledgements; practice-related correspondence with no clinical content. |

---

## 5. Boundary Cases and Handling Rules

### 5.1 Expected abnormals

The AI does not have access to a patient's prior results or diagnosis history at classification time. It cannot determine whether an abnormal result is expected in the context of a known chronic condition.

**Rule:** Classify based on the absolute result value against RCPA/AACB thresholds. Do not default to Information only based on assumed chronicity. Set `context_required: true` with the note: "result is abnormal — GP to confirm whether this represents a change from the patient's established baseline."

**Rationale:** The medico-legal risk of under-triaging a genuinely new deterioration in a chronic condition outweighs the cost of the GP spending 10 seconds confirming an expected value.

### 5.2 Already-actioned results

A result that has already been actioned (e.g. a critical K+ in a patient who has since been admitted) still appears in the GP inbox and still requires formal acknowledgement. The AI cannot determine whether prior action has been taken.

**Rule:** Classify based on the result value and content as if no prior action has been taken. Set `context_required: true` with the note: "this result may already have been actioned — GP to confirm and document." Viewing a result creates a clinical relationship and documentation obligation under Te Whatu Ora's 2024 guidance on transfer of care.

### 5.3 Normal result requiring clinical action

The AI cannot reliably determine the clinical question that prompted a test without access to the patient record. A normal troponin in a chest pain workup, or a normal PSA with persistent urinary symptoms, may still require action.

**Rule:** Classify as Information only by default. Document this as a known system limitation: the Inbox Helper cannot identify "normal but actionable" results without clinical context. The GP retains responsibility for interpreting results in the context of the clinical question.

### 5.4 Incidental findings on radiology

**Rule:** Apply organ-specific guideline thresholds. Fleischner Society 2017 guidelines apply for pulmonary nodules (nodule ≥6mm in a patient without prior malignancy requires surveillance → Routine). ACR Incidental Findings Committee white papers apply for renal, adrenal, liver, thyroid, and adnexal findings. Findings below the follow-up threshold → Information only.

### 5.5 Ambiguous or uncertain documents

**Rule:** When content is ambiguous and urgency cannot be determined with confidence, classify at the higher of the two candidate urgency levels. Never default to Information only under uncertainty. Set `context_required: true`.

---

## 6. Output Schema

For each inbox item, the system returns:

| Field | Type | Description |
|---|---|---|
| `urgency_level` | Integer (1–4) | 1 = Immediate, 2 = Urgent, 3 = Routine, 4 = Information only |
| `urgency_label` | String | Human-readable label matching the urgency level |
| `rationale` | String (≤50 words) | Brief explanation of the classification. Enables GP to verify the decision in under 5 seconds without re-reading the document. |
| `context_required` | Boolean | True when classification may change with patient-specific context (prior results, diagnosis history). |
| `context_note` | String (optional) | Present when `context_required` is true. Specifies what context is needed and why. |

**Example output — Urgent lab result with context flag:**
```
urgency_level: 2
urgency_label: Urgent
rationale: Creatinine 198 umol/L, above reference range. Significant rise if new — requires assessment.
context_required: true
context_note: Result is abnormal — GP to confirm whether this represents a change from the patient's established baseline creatinine.
```

---

## 7. Success Criteria

### 7.1 Primary safety metrics (hard requirements)

| Metric | Target | Basis |
|---|---|---|
| Sensitivity — Immediate class | >99% | ACS-COT <5% undertriage standard; medico-legal obligations; HDC case law |
| Sensitivity — Urgent class | >99% | Same rationale: results requiring action within 1–3 days cannot be missed |

**On specificity:** No fixed floor. Over-triage (Routine items classified as Urgent) is the designed trade-off to achieve >99% sensitivity. The GP review cost of a false positive is low. The clinical and medico-legal cost of a false negative is high.

**On real-world degradation:** Published clinical AI literature documents validation sensitivity degrading 8–15 percentage points in real-world deployment. Validation targets for this system are therefore set above the minimum clinically acceptable deployment threshold. Ongoing performance monitoring is required post-deployment.

### 7.2 Secondary metrics

| Metric | Target | Purpose |
|---|---|---|
| Overall weighted accuracy | ≥90% | Grant language — CONT-109091-N2RD-NSIWKC Objective 1 target |
| Macro F1 | ≥0.80 | Exposes failure on minority classes (weighted F1 would conceal poor Immediate/Urgent performance) |
| Quadratic weighted kappa (QWK) | Reported | Penalises large ordinal errors proportionally — Immediate misclassified as Information only costs 9× more than Immediate misclassified as Urgent |
| PR-AUC per high-urgency class | Reported | More informative than ROC-AUC for imbalanced class distributions |
| Full 4×4 confusion matrix | Reported | Required for MBIE evidence and future TGA regulatory submission |
| MCC | Reported | Robust to class imbalance; summary of all four confusion matrix quadrants |

### 7.3 Test set design

- **Stratified enriched set:** approximately 1,500 total items, targeting 100–150 items per urgency class per document type
- **Natural prevalence holdout:** 300–500 items at natural inbox distribution for calibration and PPV/NPV assessment
- **Confidence intervals:** Bootstrap BCa method with ≥2,000 iterations for per-class metrics on rare Immediate class
- **Spectrum requirement:** Test set must include borderline and ambiguous cases. Evaluating only on clear-cut examples (obvious critical result vs. routine normal) will inflate performance and misrepresent real-world utility.
- **Per-document-type evaluation:** Results reported separately for each of the five document types. Aggregate accuracy masks differences in difficulty across document types.

---

## 8. Document Structure Reality

This section is an input to architecture selection (Objective 1, Steps 2–5).

| Document Type | Structure | Classification Approach |
|---|---|---|
| Lab results | Structured — HL7 messages via Medtech; values, flags, and reference ranges available as discrete fields | Rule-based or structured extraction feasible; LLM beneficial for delta interpretation |
| Radiology reports | Semi-structured — standardised report templates with impression section; varies by radiologist and institution | Hybrid: extract impression section + semantic reading |
| Discharge summaries | Semi-structured — "message for GP" section often present but not universal; action items may appear anywhere in body or plan section | Full-document semantic reading required |
| Specialist letters | Unstructured free prose — no standard section markers; critical findings, diagnoses, and action requests can appear anywhere | Full-document semantic reading required |
| Patient messages | Unstructured free text — variable length, format, and content; highly practice-dependent | Full-document semantic reading required |

**Implication:** A single rule-based or structured-extraction architecture cannot achieve the required sensitivity across all five document types. Three of five document types require semantic full-text understanding. This is the primary driver toward evaluating LLM-based architectures in Step 2.

---

## 9. MBIE Evidence Statement

This document constitutes the Step 1 deliverable for Objective 1 of the NexWave R&D programme under contract CONT-109091-N2RD-NSIWKC: "Clear written definition of both tasks with success criteria."

**Development basis:**
- Systematic literature review of GP inbox management frameworks (RNZCGP Foundation Standard, RACGP Standards 5th Ed., BPAC NZ guidance, BMA test results guidance, NHS GP Forward View Correspondence Management Programme)
- Alignment with RCPA/AACB harmonised alert list for NZ/AU laboratory critical values
- Alignment with RCR/UK Academy of Medical Royal Colleges alert classification for radiology
- Evidence from clinical informatics literature on discharge summary processing (Spencer et al. BJGP 2018; Roy et al. Ann Intern Med 2005; Weetman et al. 2020) and outpatient correspondence management
- NZ medico-legal framework: Te Whatu Ora "Transfer of Care and Test Results Responsibility" (19 March 2024); HDC case law including 21HDC00619, 18HDC01066, 14HDC00894, 99HDC11494
- Clinical input from a practising New Zealand GP (programme director and clinical domain expert), including direct experience of NZ hospital discharge summary and specialist letter structure
- Evaluation metrics framework grounded in published clinical NLP literature (Hicks et al. Scientific Reports 2022; Saito and Rehmsmeier PLOS ONE 2015; Fazekas and Kovács Applied Soft Computing 2023) and regulatory guidance (FDA draft guidance January 2026; TGA AI evidence requirements; IMDRF GMLP 10 guiding principles)

**Success criteria basis:** The >99% sensitivity target for Immediate and Urgent classes is grounded in the ACS-COT <5% undertriage standard (the established clinical benchmark for safety-critical triage), the NZ medico-legal environment establishing that missed significant results constitute a breach of duty, and published evidence that real-world AI triage sensitivity degrades 8–15 percentage points below validation performance.

**Regulatory note:** This system almost certainly requires TGA registration as a Class IIa medical device under the Therapeutic Goods Act 1989, as AI-enabled clinical decision support software explicitly fails the TGA CDSS exemption criteria (TGA guidance, October 2025). The evidence package for this specification is designed to be compatible with TGA ARTG inclusion requirements and IMDRF GMLP principles. Under the Trans-Tasman Mutual Recognition Arrangement, TGA approval facilitates NZ market entry. NZ regulatory requirements are in flux pending the Medical Products Bill (Cabinet decisions July 2025).
