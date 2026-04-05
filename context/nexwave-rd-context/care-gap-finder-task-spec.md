---
title: Care Gap Finder — Task Specification
type: context
project: nexwave-rd
objective: obj-1
step: step-1
created: 2026-04-05
status: final
---

# Care Gap Finder — Task Specification

**Objective 1, Step 1 deliverable.** This document defines the Care Gap Finder detection and calculation tasks in precise, testable terms. It is the foundation for all architecture evaluation, synthetic data design, and prototype work in Objective 1, and constitutes primary evidence for the MBIE Step 1 deliverable under contract CONT-109091-N2RD-NSIWKC.

---

## 1. Task Overview

The Care Gap Finder scans a GP's enrolled patient register and identifies patients who are overdue for specific health monitoring or clinical assessments. It operates on the patient list — not on incoming documents. It is a population health tool, not an inbox tool.

The system is assist-only. It surfaces a prioritised list of care gaps to the GP or practice nurse. The practice decides who to contact, when, and how. The AI does not contact patients, does not modify records, and does not take autonomous clinical action.

**Design principle:** The system is recall-optimised, not precision-optimised. Missing a genuine care gap (false negative) is the unacceptable outcome. False positives — flagging a patient who turns out not to need outreach — cost the practice a brief phone call. False negatives cost the patient a missed diagnosis or deterioration.

---

## 2. In-Scope Care Gaps

### 2.1 MVP scope (Objective 1 prototype + Objective 2/3 deployment)

| Care Gap | Condition | Obj 1 synthetic prototype | Notes |
|---|---|---|---|
| HbA1c monitoring | Type 2 diabetes (and Type 1) | Yes | Detection rule: interval-based |
| Diabetes annual review components | Type 2 diabetes (and Type 1) | Yes | Detection rule: interval-based per component |
| CVDRA eligibility and recall | All patients meeting age/ethnicity/risk criteria | Yes | Detection rule: eligibility matrix + last assessment date |
| CVDRA calculation | Patients due for CVDRA | **Yes — ≥95% accuracy target** | Deterministic Python; grant-committed Obj 1 target |
| Blood pressure monitoring | Hypertension | Yes | Detection rule: interval + medication status |

### 2.2 Deferred (Objective 2 or later)

| Care Gap | Reason deferred |
|---|---|
| Cervical screening recall | National screening programme overlap; PMS data linkage unreliable for Obj 1 |
| Bowel screening recall | FIT kit return data not in GP PMS |
| Childhood immunisation | AIR linkage required; out of Obj 1 scope |
| COPD / asthma annual review | Low data structuring in PMS; higher free-text dependency |
| Heart failure monitoring | Small prevalence; complex comorbidity interactions |
| CKD monitoring (standalone) | Partially covered under diabetes and hypertension rules |
| Medication review (polypharmacy) | No structured NZ guideline interval; requires medication list analysis |

---

## 3. Sub-Task Architecture

The Care Gap Finder comprises three functionally distinct sub-tasks. These are not interchangeable — they have different architectures, different accuracy targets, and different R&D uncertainty profiles.

| Sub-task | Description | Architecture | R&D uncertainty |
|---|---|---|---|
| **A — Gap detection** | Determine whether a patient is overdue for a specific monitoring item. Rule-based logic against structured PMS fields (diagnosis codes, lab dates, demographic fields). | Deterministic rules engine | Low on clean data; high when PMS data is incomplete or inconsistently coded |
| **B — Variable extraction** | Extract PREDICT equation input variables from PMS records. Most variables are in structured fields; some (family history, NZDep) require derivation. Handles missing, stale, or ambiguous values. | Structured extraction + fallback logic | Moderate: 15 required variables; 3 are commonly missing or under-coded in NZ GP records |
| **C — CVDRA calculation** | Compute the 5-year CVD risk percentage from extracted variables using the NZ Primary Prevention Equations (PREDICT v.2019). Deterministic given complete inputs. | Python implementation of HISO 10071:2025 equations | Low on complete data; moderate when variables are missing and estimation is required |

**The ≥95% accuracy target in the grant applies to Sub-task C** (CVDRA calculation) on clean synthetic data. The primary R&D challenge is Sub-task B (variable extraction) on real-world PMS data with missing and inconsistently coded fields.

---

## 4. Gap Detection Logic

### 4.1 Type 2 Diabetes — HbA1c Monitoring

**Patient identification:**

| Coding system | Codes to include |
|---|---|
| Read v2 (Medtech Evolution) | `C10F.` and all descendants (C10F0–C10FQ): T2DM root and subtypes. Include `C10FJ` (insulin-treated T2DM). |
| SNOMED CT | `44054006` (Diabetes mellitus type 2) and descendants |
| ICD-10 | E11.x range — for hospital record linkage only; NOT used in GP problem lists |
| Type 1 (separate tracking) | Read `C10E.` and descendants; SNOMED `46635009` |

Treatment modality (diet-controlled, oral, insulin) is inferred from the medication list, not from distinct problem list codes.

**HbA1c monitoring rules:**

Source: NZSSD Type 2 Diabetes Management Guidance 2021/2023; BPAC NZ Diabetes Toolbox, updated July 2025.

| Patient HbA1c status | Monitoring interval | Care gap trigger | Flag threshold |
|---|---|---|---|
| Last HbA1c **above target** (≥53 mmol/mol) | Every 3 months | Last HbA1c > 4 months ago | High priority |
| Last HbA1c **at target** (<53 mmol/mol) | Every 6 months | Last HbA1c > 7 months ago | Routine priority |
| **No HbA1c ever recorded** | Immediate | No HbA1c result in patient record | High priority |

**HbA1c target threshold:** <53 mmol/mol for most adults. Individualised targets apply — see Boundary Case 4.1.A.

**Diagnostic threshold change from 1 July 2026:** The diagnostic threshold lowers from ≥50 to ≥48 mmol/mol (National Diabetes Roadmap, announced 25 March 2026). The monitoring target threshold (<53 mmol/mol) is unchanged. Systems must apply the correct diagnostic threshold based on assessment date.

**Urgent escalation flags** (flag separately from standard care gap — require GP review, not just routine recall):

| HbA1c value | Flag |
|---|---|
| ≥75 mmol/mol | Urgent — very poor glycaemic control |
| >90 mmol/mol + symptoms | Immediate — insulin initiation indicated |

### 4.2 Diabetes Annual Review Components

Source: BPAC NZ 2021 ("The annual diabetes review," updated August 2025); NZSSD 2021/2023; MoH Quality Standards for Diabetes Care 2020.

Each component below should be completed at least once per 12-month period, unless a shorter interval applies. The annual review components may be completed across multiple consultations — the system checks whether each component has been done within the relevant period, not whether a single "annual review" appointment occurred.

**Lab-based components (structured PMS data — electronic lab results):**

| Component | Standard interval | Escalated interval | Trigger condition |
|---|---|---|---|
| **uACR** | 12 months | 3–6 months if abnormal | Last uACR > 13 months ago; or > 7 months if ACR >3 mg/mmol |
| **Serum creatinine / eGFR** | 12 months | See eGFR/ACR matrix below | Last result > 13 months ago |
| **Non-fasting lipid panel** (TC, HDL-C, LDL-C, TG) | 12 months | — | Last lipid panel > 13 months ago |
| **Liver function tests** (AST, ALT) | 12 months | — | Last LFTs > 13 months ago |

**eGFR and uACR monitoring escalation matrix** (KDIGO 2013, BPAC NZ 2019):

| eGFR (mL/min/1.73m²) | ACR <3 mg/mmol | ACR 3–30 mg/mmol | ACR >30 mg/mmol |
|---|---|---|---|
| **≥60** | Annually | Annually | 6-monthly |
| **45–59** | Annually | 6-monthly | 4-monthly |
| **30–44** | 6-monthly | 4-monthly | 4-monthly |
| **<30** | 3-monthly | 3-monthly | 3-monthly |

**eGFR <30:** Flag for nephrology referral in addition to monitoring gap.

**NZ-specific note:** NZSSD uses sex-specific microalbuminuria thresholds — >2.5 mg/mmol (males), >3.5 mg/mmol (females) — for clinical decision-making. The KDIGO staging threshold of 3 mg/mmol is used for monitoring interval decisions.

**Observation-based components (structured PMS vital signs / classified fields):**

| Component | Standard interval | Care gap trigger |
|---|---|---|
| **Blood pressure** | 12 months (3-monthly if above target) | Last BP > 13 months ago; or > 7 weeks if above target and on treatment |
| **Weight / BMI** | 12 months | Last weight > 13 months ago |
| **Smoking status** | 12 months | No smoking status recorded in past 13 months |
| **CVD risk assessment** | Per CVDRA recall schedule (see 4.3) | Overdue per 4.3 rules |

**Examination / referral components (partially structured):**

| Component | Standard interval | Care gap trigger | PMS data note |
|---|---|---|---|
| **Foot examination** | 12 months | Last foot exam code > 13 months ago | May be free-text — absence of code does not confirm absence of examination. Flag with `context_required: true`. |
| **Retinal photoscreening** | 24 months (standard); 36 months (low risk); more frequent if HbA1c >64, eGFR <45, ACR >100 | Last retinal screen > 25 months ago | Screen results often NOT in GP PMS — see Boundary Case 4.2.A. |

**Type 1 diabetes — retinal screening start rule:** T1D: within 5 years of diagnosis (not at diagnosis as for T2D).

### 4.3 CVDRA Eligibility and Recall

Source: MoH 2018 Cardiovascular Disease Risk Assessment and Management for Primary Care (ISBN 978-1-98-853933-1); BPAC NZ 2018/2023.

**Screening initiation thresholds (age and sex by ethnicity):**

| Population group | Men | Women |
|---|---|---|
| **European / Other** (no additional risk factors) | 45 years | 55 years |
| **Māori** | 30 years | 40 years |
| **Pacific peoples** | 30 years | 40 years |
| **South Asian peoples** (Indian incl. Fijian Indian, Sri Lankan, Afghani, Bangladeshi, Nepalese, Pakistani, Tibetan) | 30 years | 40 years |
| **Any ethnicity with personal or family risk factors†** | 35 years | 45 years |
| **Diabetes (Type 1 or Type 2)** | From diagnosis | From diagnosis |
| **Severe mental illness‡** | 25 years | 25 years |

†Personal risk factors triggering earlier screening: current smoking, atrial fibrillation (ECG-confirmed), BMI ≥30 or waist ≥102 cm (men) / ≥88 cm (women), history of gestational diabetes, HbA1c 41–49 mmol/mol, eGFR <60 on two or more occasions.

Family risk factors: first-degree relative hospitalised or died from MI or stroke before age 50; diabetes in first-degree relative; familial hypercholesterolaemia.

‡Severe mental illness: schizophrenia, major depressive disorder, bipolar disorder, schizoaffective disorder.

The PREDICT equations are validated for ages 30–74. For patients screened below age 30 (e.g., severe mental illness from age 25), the Consensus Statement notes risk estimates remain clinically useful.

**CVD risk equivalents — suppress CVDRA calculation, flag for intensive management instead:**

These patients are automatically classified as high risk (≥15% 5-year CVD risk). Calculating a risk score is not appropriate or necessary.

- Prior cardiovascular event: angina, CABG, PCI, MI, peripheral vascular disease, stroke, TIA
- Familial hypercholesterolaemia (Read `C320.` or SNOMED `398919000`)
- Congestive heart failure (Read `G58..` or SNOMED `84114007`)
- **Diabetes with eGFR <45 mL/min/1.73m²** (NZ-specific CVD equivalent)
- Stage 4+ CKD (eGFR <30)
- TC:HDL-C ratio ≥8
- Persistent BP ≥180/100 mmHg (isolated extreme — triggers drug treatment regardless of risk score)

**Recall intervals (risk-stratified):**

| Last calculated 5-year CVD risk | Repeat CVDRA interval | Care gap trigger |
|---|---|---|
| **<3%** | 10 years | Last CVDRA > 10 years ago |
| **3–5%** | 5 years | Last CVDRA > 5 years ago |
| **5–9%** | 5 years | Last CVDRA > 5 years ago |
| **10–14%** | 2 years | Last CVDRA > 2 years ago |
| **≥15% or on CVD pharmacotherapy** | Annually | Last CVDRA > 13 months ago |
| **T2DM (any risk)** | Annually | Last CVDRA > 13 months ago (also covered by diabetes annual review) |
| **Severe mental illness, <15% risk** | Every 2 years | Last CVDRA > 25 months ago |
| **Established CVD / CVD equivalent** | Annual management review — no calculation | Annual management review gap if not coded |
| **No prior CVDRA, patient meets eligibility criteria** | Immediate | Flag at eligibility age |

**Prerequisite gap — BP required for CVDRA:** If a patient is due for CVDRA but has no BP recorded within 12 months, two simultaneous care gaps exist: the CVDRA recall gap and the BP prerequisite gap. Flag the BP gap as the higher-priority actionable item. Resolving it enables the CVDRA calculation.

### 4.4 Hypertension — Blood Pressure Monitoring

Source: MoH 2018 CVD Consensus Statement; BPAC NZ "Hypertension in adults" 2023, updated June 2025.

**Patient identification:**

| Coding system | Codes to include |
|---|---|
| Read v2 | `G20..` (Essential hypertension), `G201.` (Benign essential hypertension), `G20z.` (Essential hypertension NOS), `G2...` (Hypertensive disease parent), `G2z..` (Hypertensive disease NOS) |
| SNOMED CT | `59621000` (Essential hypertension) — primary concept; `38341003` (Hypertensive disorder) as parent |
| White coat hypertension | Read `246M.` / SNOMED `697930002` — include on separate lower-priority track |

There are no separate Read v2 codes for "controlled" vs "uncontrolled" hypertension. Control status is determined algorithmically from the most recent BP reading compared against the applicable target.

**BP targets by patient risk group:**

| Patient group | BP target (clinic) | Notes |
|---|---|---|
| **High risk:** diabetes, CKD eGFR <60, established CVD, age ≥65, 5-year CVD risk ≥15% | **<130/80 mmHg** | MoH 2018 national standard |
| **Lower risk:** none of the above | **<140/90 mmHg** | MoH 2018 |
| **Frailty, age ≥85, limited life expectancy** | Individualised; consider deprescribing | Age alone does not justify de-intensification — assess frailty |

**BP recording codes:** Read `2469.` (systolic) and `246A.` (diastolic). SNOMED `271649006` (systolic) and `271650006` (diastolic). The date of the most recent entry under these codes is the "last BP date" for interval calculations.

**Monitoring intervals and care gap triggers:**

| Scenario | Flag threshold | Priority |
|---|---|---|
| Coded hypertensive **on antihypertensive** (dispensed in prior 6 months) + **no BP in >12 months** | >12 months | High — treatment without monitoring |
| Coded hypertensive + **last BP above target** + last BP >6 weeks ago | >6 weeks | High — in titration phase |
| Coded hypertensive + **high CVD risk (≥15%)** + no BP in >12 months | >12 months | High |
| Coded hypertensive + **intermediate CVD risk (5–15%)** + no BP in >24 months | >24 months | Routine |
| Coded hypertensive + **low CVD risk (<5%)**, lifestyle only + no BP in >5 years | >5 years | Low |
| **White coat hypertension** (confirmed) + no BP in >12 months | >12 months | Low — annual assessment recommended |

**Hypertension + diabetes:** BP monitoring is merged into the diabetes annual review. Do not create a duplicate hypertension care gap if the patient is already being tracked under the diabetes annual review. If the diabetes annual review itself is overdue (>13 months), flag the diabetes gap — it subsumes the hypertension BP monitoring requirement.

**Annual review components for hypertension (BPAC 2023 — reconstructed, no formal NZ checklist exists):**

| Component | Notes |
|---|---|
| BP measurement | Primary monitoring item |
| Serum creatinine / eGFR | Medication monitoring and CKD screening |
| Urine ACR | Explicitly recommended for hypertension without diabetes; under-utilised in NZ |
| Fasting lipid profile | CVDRA input variable |
| HbA1c | CVDRA input; screens for incident diabetes |
| CVDRA (if due) | Per recall schedule |
| Medication review | Adherence, adverse effects, dose appropriateness |

---

## 5. CVDRA Calculation Logic

This section specifies Sub-task C — the deterministic calculation of 5-year CVD risk from extracted variables.

**Calculator:** NZ Primary Prevention Equations v.2019 (with BMI), codified in HISO 10071:2025. Published by Pylypchuk R, Wells S, Kerr A et al. in *The Lancet* 2018;391(10133):1897–1907. Available under CC-BY 4.0.

**Reference implementation:** `github.com/VIEW2020/PredictRiskScores` (R, GPL-3.0). A free Health NZ CVDRA REST API is available for production use at `api.cvdriskassessment.min.health.nz/open-api/`.

**Trademark note:** "PREDICT" is a registered trademark of Enigma Solutions Ltd. Any external-facing tool must use a different name for the calculator while citing the underlying equations.

**Two separate equations:** The correct equation is selected based on diabetes status.

### 5.1 General population equation (no diabetes) — 15 input variables

| # | Variable | Type | Implementation notes |
|---|---|---|---|
| 1 | **Age** | Continuous (years) | Valid range: 30–74. For patients outside this range, see Boundary Case 5.A. |
| 2 | **Sex** | Binary (M/F) | Selects sex-specific Cox equation and baseline survival |
| 3 | **Ethnicity** | 5 categories | Māori / Pacific / Indian-South Asian / Chinese-Other Asian / European-Other. Use NZ prioritised ethnicity from patient record. |
| 4 | **NZDep quintile** | Ordinal 1–5 | Derived from residential address using NZ Census meshblock deprivation data. If address unavailable, see Boundary Case 5.B. |
| 5 | **Smoking status** | 3 levels | Never / Ex-smoker / Current smoker. Binary encoding is insufficient — the equation uses three-level encoding. |
| 6 | **Family history of premature CVD** | Binary (0/1) | First-degree relative hospitalised or died from MI or stroke before age 50. Often free-text in GP records — see Boundary Case 5.C. |
| 7 | **Atrial fibrillation** | Binary (0/1) | ECG-confirmed AF (paroxysmal, persistent, or permanent). Read `G573.` / SNOMED `49436004`. AF is a direct equation input, not a post-hoc multiplier. β = 0.6250 (men), 0.9293 (women) — approximately equal to smoking in predictive weight. |
| 8 | **Diabetes** | Binary (0/1) | Type 1 or Type 2. If diabetes present, use diabetes-specific equation (Section 5.2). |
| 9 | **Systolic BP (mmHg)** | Continuous | Mean of two seated measures. Use the most recent BP recording in the PMS. Validity period: 12 months. |
| 10 | **TC:HDL-C ratio** | Continuous | Computed as total cholesterol ÷ HDL-C from non-fasting lipid panel. Use the most recent result. |
| 11 | **BMI** | 7 categories | <18.5 / 18.5–24.9 / 25–29.9 / 30–34.9 / 35–39.9 / ≥40 / Unknown. Calculated from height and weight in PMS vitals. |
| 12 | **BP-lowering medication** | Binary (0/1) | Dispensed in prior 6 months. In PMS context without PHARMS linkage: use current prescriptions as proxy. Drug classes: ACE inhibitors, ARBs, beta-blockers, calcium channel blockers, thiazides. |
| 13 | **Lipid-lowering medication** | Binary (0/1) | Dispensed in prior 6 months. Statins, ezetimibe, fibrates. |
| 14 | **Antithrombotic medication** | Binary (0/1) | Dispensed in prior 6 months. Antiplatelet (aspirin, clopidogrel) or anticoagulant (warfarin, DOACs). |
| 15 | **Interaction terms** | Derived | Age × Diabetes; Age × SBP; BP-med × SBP. Computed internally — not separate inputs. |

**Formula:** 5-year CVD risk (%) = (1 − S₀^exp(Σ(β × (x − mean)))) × 100, where S₀ is the sex-specific baseline survival (men: 0.9712501; women: published in HISO 10071:2025), β values are the published Cox regression coefficients, and x values are centred by subtracting published means.

**Risk category thresholds (NZ Primary Prevention Equations, current):**

| Category | 5-year CVD risk | Clinical action |
|---|---|---|
| **Low** | **<5%** | CVD medicines generally not recommended; lifestyle advice |
| **Intermediate** | **5–15%** | Discuss benefits and risks of BP- and lipid-lowering medicines; consider treatment at higher end of range |
| **High** | **≥15%** | BP- and lipid-lowering treatment strongly recommended |

Two override rules apply regardless of calculated risk: persistent BP ≥160/100 mmHg triggers drug treatment; TC:HDL-C ratio ≥8 triggers lipid treatment.

### 5.2 Diabetes-specific equation — additional input variables

For patients with diabetes (T1D or T2D), use the diabetes-specific PREDICT equation instead of the general equation. All 15 variables above apply, plus:

| Variable | Type | Notes |
|---|---|---|
| **HbA1c** | Continuous (mmol/mol) | Most recent value |
| **eGFR** | Continuous (mL/min/1.73m²) | CKD-EPI equation; auto-calculated by most NZ labs |
| **Urinary ACR** | Continuous (mg/mmol) | Most recent uACR |
| **Diabetes duration** | Continuous (years) | Calculated from diagnosis date in problem list |
| **Oral hypoglycaemic medication** | Binary | Metformin, sulfonylureas, DPP-4 inhibitors, SGLT-2 inhibitors, GLP-1 agonists |
| **Insulin** | Binary | Any insulin formulation |
| **BMI** | Continuous (kg/m²) | In the diabetes equation, BMI is continuous rather than categorical |

---

## 6. Data Requirements

### 6.1 Fields required per care gap (Medtech Evolution)

| Care gap | Required PMS fields | Derivation method | Data risk |
|---|---|---|---|
| T2DM identification | Problem list: Read C10F. / SNOMED 44054006 | Direct lookup | Medium — inconsistent coding between T1D and T2DM in older records |
| HbA1c interval | Lab results: HbA1c result + date | Electronic lab feed (HL7) | Low — well-structured lab data |
| Annual review labs | Lab results: uACR, creatinine/eGFR, lipid panel, LFTs | Electronic lab feed | Low |
| BP | Observations/vitals: Read 2469. (systolic), 246A. (diastolic) + date | Classified data | Low |
| Retinal screening | Incoming correspondence / regional screening feed | Unreliable electronic feed | HIGH — often absent from PMS; see Boundary Case 4.2.A |
| Foot examination | Consultation coding or free text | Coded or free text | HIGH — frequently free-text only |
| CVDRA eligibility | Demographics: DOB, sex, ethnicity; Problem list: AF, SMI, diabetes, CVD diagnoses, FH | Multiple sources | Medium |
| NZDep quintile | Patient address → meshblock → NZDep lookup table | Derived (external lookup) | Medium — address completeness varies |
| TC:HDL-C ratio | Lab results: total cholesterol + HDL-C from same lipid panel | Computed from lab fields | Low |
| Medication flags (3) | Current prescriptions / dispensing history | Prescription records | Medium — dispensing ≠ prescribing; PHARMS data not in PMS |
| Family history (CVD) | Free-text family history section or structured family history field | Structured field or NLP | HIGH — inconsistently documented |
| Hypertension identification | Problem list: Read G20.. / SNOMED 59621000 | Direct lookup | Low |

### 6.2 Data completeness expectations

Based on NZ PMS research (University of Otago 2021, average PMS feature utilisation 35.7%):

| Variable | Expected completeness in NZ GP records |
|---|---|
| Diagnoses (coded) | High — PHO Performance Programme historically incentivised coding |
| Lab results (electronic) | High — NZ labs transmit electronically via HL7 |
| BP readings | Moderate — recorded at consultation but gaps between consultations |
| Smoking status | Moderate — incentivised by PHO but documentation inconsistent |
| BMI | Moderate |
| Family history | Low — frequently absent or free-text only |
| NZDep quintile | Derived — address completeness varies |
| Retinal screening date | Low — often not in GP PMS |
| Foot examination | Low — frequently free-text |

---

## 7. Boundary Cases and Handling Rules

### 7.1 Missing CVDRA variables

**Rule:** The PREDICT equation requires all 15 variables. For each missing variable, the system must apply a documented fallback strategy rather than returning an error or silently imputing.

| Variable | Missing data handling |
|---|---|
| NZDep quintile | Impute quintile 3 (national median) if address unavailable. Set `data_completeness_score` accordingly. |
| Family history of premature CVD | Default to 0 (absent) if not documented. Set `context_required: true` with note: "Family history not recorded — GP to confirm before accepting risk score." |
| BMI | If height or weight missing, use category "Unknown" (HISO 10071:2025 permits this). |
| TC:HDL-C ratio | If no lipid panel in past 12 months, flag lipid panel as a prerequisite gap. Do not impute. |
| Smoking status | If not documented, default to "Never" only if the patient is >75 and has no coded or noted smoking history. Otherwise flag as a data gap. |
| Medication flags | If PHARMS data unavailable, derive from current prescriptions. Note approximation in `context_note`. |

If ≥3 mandatory variables are missing simultaneously, do not compute a risk score. Return a "CVDRA incomplete — data prerequisite gaps" flag specifying which variables are needed.

### 7.2 Patients outside the PREDICT validation range (age <30 or >74)

**Rule:** The PREDICT equations are validated for ages 30–74.

For patients aged <30 meeting eligibility criteria (e.g., severe mental illness from age 25), compute the score and flag it as `outside_validated_range: true` with note: "Patient below validated age range — risk estimate is approximate; use clinical judgement."

For patients aged ≥75, do not compute a PREDICT score. Flag for clinical review: "Patient above validated age range for PREDICT equations. Use clinical judgement for cardiovascular risk management." Annual management review gap should still be flagged if the patient is on CVD pharmacotherapy.

### 7.3 CVD risk equivalents — suppress calculation

**Rule:** Patients with established CVD or a CVD risk equivalent (see Section 4.3) should not have a CVDRA calculation performed. They are automatically high risk. Generate a "high-risk annual management review" care gap instead.

Suppress CVDRA calculation flag and substitute: "Patient has established CVD / CVD equivalent — annual risk factor management review indicated; risk score calculation not required."

This includes the NZ-specific rule: **diabetes with eGFR <45 = CVD equivalent.** This threshold is lower than most international standards (which use eGFR <30 for non-diabetic CKD).

### 7.4 Retinal screening data not in PMS

**Rule:** Regional retinal screening databases are not consistently linked to GP PMS systems in NZ. Absence of a retinal screening date in the PMS does not confirm the patient was not screened.

Set `context_required: true` with note: "Retinal screening date not found in practice records — GP to confirm whether screening has been completed via regional screening programme."

**Do not suppress the care gap** on absence of data alone — national coverage data shows approximately 62% of eligible patients received biennial screening, meaning a substantial proportion of unflagged patients genuinely are overdue.

### 7.5 Foot examination in free text

**Rule:** Foot examination documentation in NZ GP records is frequently free-text. Absence of a coded foot examination does not confirm absence of examination.

Set `context_required: true` with note: "No coded foot examination recorded in the past 12 months — GP to confirm whether examination was performed and documented."

This is a known system limitation analogous to the Inbox Helper's "normal but actionable" boundary case (Section 5.3 of the Inbox Helper spec).

### 7.6 Newly diagnosed diabetes patients

**Rule:** Allow a 3-month grace period after a new T2DM diagnosis before flagging annual review component gaps. Baseline investigations take time to schedule; immediate flagging on diagnosis day generates noise and GP alert fatigue. HbA1c monitoring (3-monthly until at target) begins immediately.

### 7.7 Patient formally declined screening

**Rule:** If a patient has a coded clinical finding of declined screening (Read `8IEp.` or equivalent coded refusal), suppress the specific care gap for 12 months and set `declined_by_patient: true`. Re-flag annually — clinical circumstances may change.

**Do not permanently suppress.** Documenting a declined screening does not eliminate the underlying clinical need; it creates a record of the GP's duty of care being discharged.

### 7.8 Diabetes + established CVD — dual suppression

**Rule:** Patients with both T2DM and established CVD have two suppression rules operating simultaneously:

1. Suppress CVDRA calculation (CVD risk equivalent — see 7.3)
2. Continue all diabetes annual review components (HbA1c monitoring, uACR, eGFR, retinal screening, foot exam, etc.) — these are not suppressed

Generate an "intensive CVD risk factor management" reminder in place of the CVDRA care gap, referencing the annual cardiovascular review.

### 7.9 July 2026 diagnostic threshold change

**Rule:** From 1 July 2026, the NZ diagnostic HbA1c threshold for diabetes lowers from ≥50 to ≥48 mmol/mol (National Diabetes Roadmap, 25 March 2026). Approximately 34,500 patients will be reclassified from prediabetes to diabetes.

The system must apply the correct threshold based on the assessment date:
- Assessment before 1 July 2026: diagnostic threshold ≥50 mmol/mol
- Assessment from 1 July 2026: diagnostic threshold ≥48 mmol/mol

A one-time sweep of patients with HbA1c 48–49 mmol/mol coded as prediabetes will be required from 1 July 2026 — these patients become newly eligible for the diabetes care gap programme.

### 7.10 Type 1 diabetes — different retinal screening start rule

**Rule:** T1D retinal screening begins within 5 years of diabetes diagnosis, not at diagnosis as for T2D. T1D patients should be flagged separately from T2D patients in the care gap output to allow practices to apply the correct start rule.

---

## 8. Output Schema

The Care Gap Finder generates a list of care gap records. Each record represents one overdue gap for one patient.

**Per-gap output:**

| Field | Type | Description |
|---|---|---|
| `patient_nhi` | String | NHI identifier |
| `care_gap_type` | Enum | `hba1c_interval` / `diabetes_annual_review` / `cvdra_recall` / `cvdra_calculation` / `bp_monitoring` / `hypertension_annual_review` |
| `care_gap_component` | String | Specific component within the type (e.g., `uacr`, `egfr`, `lipids`, `retinal_screening`, `foot_exam`, `bp`) |
| `priority` | Integer (1–3) | See priority taxonomy below |
| `priority_label` | String | "High" / "Routine" / "Advisory" |
| `days_overdue` | Integer | Days since monitoring interval was exceeded. 0 if no prior record exists. |
| `last_check_date` | ISO date / null | Date of last relevant measurement. Null if no record exists. |
| `last_check_value` | String / null | Last measurement value where clinically relevant (e.g., "HbA1c 58 mmol/mol", "BP 148/92"). |
| `recommended_action` | String (≤40 words) | What the practice should do (e.g., "Order HbA1c and arrange diabetes review appointment"). |
| `equity_priority` | Boolean | True if patient is Māori, Pacific, or South Asian — earlier CVDRA screening ages apply; equity weighting for outreach prioritisation. |
| `data_completeness_score` | Float (0–1) | Proportion of required input variables available for CVDRA calculation. Not applicable to rule-based gaps. |
| `outside_validated_range` | Boolean | True if patient age is outside the PREDICT validation range (30–74). |
| `context_required` | Boolean | True when the gap flag may change with clinical context not visible in structured PMS data. |
| `context_note` | String / optional | Present when `context_required` is true. Specifies what context is needed and why. |

**Priority taxonomy:**

| Priority | Label | Definition |
|---|---|---|
| 1 | **High** | Monitoring gap AND last known value was severely abnormal (e.g., HbA1c ≥75); OR patient is on treatment with no monitoring for >12 months; OR no prior record exists for a high-risk patient |
| 2 | **Routine** | Standard interval exceeded; clinical outreach warranted; no immediate safety concern |
| 3 | **Advisory** | Gap approaching but not yet exceeded; or gap flagged with significant data quality uncertainty |

**CVDRA calculation output (additional fields when `care_gap_type = cvdra_calculation`):**

| Field | Type | Description |
|---|---|---|
| `cvd_risk_5yr_pct` | Float | Calculated 5-year CVD risk percentage |
| `risk_category` | Enum | `low` / `intermediate` / `high` |
| `equation_version` | String | `PREDICT-NZ-v2019-BMI-DM` or `PREDICT-NZ-v2019-BMI` |
| `variables_available` | Integer | Number of the 15 variables with observed values |
| `variables_imputed` | List[String] | Variables that were imputed or defaulted (e.g., `["nzdep_quintile", "family_history"]`) |
| `next_assessment_due` | ISO date | Derived from risk category and recall schedule |

**Example output — high-priority HbA1c gap:**
```
patient_nhi: ZXY1234
care_gap_type: hba1c_interval
care_gap_component: hba1c
priority: 1
priority_label: High
days_overdue: 47
last_check_date: 2025-11-18
last_check_value: HbA1c 61 mmol/mol (above target)
recommended_action: Order HbA1c — above target, 3-monthly monitoring overdue by 47 days.
equity_priority: true
context_required: false
```

**Example output — CVDRA with incomplete data:**
```
patient_nhi: ZXY5678
care_gap_type: cvdra_recall
care_gap_component: cvdra
priority: 2
priority_label: Routine
days_overdue: 312
last_check_date: 2023-08-04
last_check_value: 5-year CVD risk 7.2% (intermediate)
recommended_action: CVDRA overdue — last assessment 2023. Order fasting lipids and BP measurement first.
equity_priority: true
context_required: true
context_note: TC:HDL-C ratio unavailable — no lipid panel in past 12 months. Lipid panel required before CVDRA calculation can proceed. Family history not recorded — confirm before accepting final risk score.
data_completeness_score: 0.73
```

---

## 9. Success Criteria

### 9.1 Primary accuracy metrics (grant-committed targets)

| Metric | Target | Basis |
|---|---|---|
| **CVDRA calculation accuracy** | **≥95%** vs reference Python PREDICT implementation | Grant CONT-109091-N2RD-NSIWKC, Obj 1 deliverable; Obj 3 validation on ≥1,000 real patient records |
| **Care gap detection agreement** | **≥85%** agreement with GP audit | Grant Obj 3 target; measured against GP-reviewed patient cohort |

### 9.2 Gap detection metrics

Gap detection is rule-based. On well-structured synthetic data, near-perfect accuracy is expected. The meaningful measure is performance degradation when PMS data is incomplete or inconsistently coded.

| Metric | Target | Purpose |
|---|---|---|
| Sensitivity (true care gap correctly flagged) | ≥99% on complete synthetic data | Missing a real gap is the unacceptable outcome |
| Specificity (non-gap patient not incorrectly flagged) | ≥85% on complete synthetic data | Alert fatigue is the primary usability risk |
| False negative rate on incomplete data | Reported | Quantifies impact of missing PMS fields |
| Per-care-gap breakdown | Required | Aggregate accuracy masks gaps with low data completeness |

### 9.3 CVDRA calculation metrics (Sub-task C)

| Metric | Target | Notes |
|---|---|---|
| **Exact match (±0.5%)** with reference PREDICT implementation | ≥95% on complete synthetic records | Primary Obj 1 target |
| **Risk category agreement** (low / intermediate / high) | ≥99% | Clinical decision is based on category, not exact percentage |
| Performance on records with 1–2 missing variables | Reported | Quantifies imputation strategy accuracy |
| Performance on records with ≥3 missing variables | Reported | Should fall below production threshold; flag for data quality action |
| Edge case accuracy | 100% | Patients outside age range, CVD equivalents, diabetes equation routing |

### 9.4 Equity validation metrics

| Metric | Target |
|---|---|
| Māori patients flagged at correct CVDRA initiation age (30M / 40F) | 100% |
| Pacific patients flagged at correct CVDRA initiation age (30M / 40F) | 100% |
| South Asian patients flagged at correct initiation age (30M / 40F) | 100% |
| Diabetes + eGFR <45 correctly classified as CVD equivalent (suppress CVDRA) | 100% |
| No systematic under-flagging of Māori or Pacific patients vs European patients | Confirmed by per-ethnicity sensitivity analysis |

### 9.5 Test set design (Objective 1 — synthetic data)

| Set | Size | Composition |
|---|---|---|
| **CVDRA calculation set** | ≥1,000 synthetic patients | Complete inputs: 200; 1 variable missing: 200; 2 variables missing: 200; diabetes equation patients: 200; CVD equivalents / exclusions: 200 |
| **Gap detection set** | ≥500 patients per care gap type | True gaps: ~60%; no gap: ~40%; with Māori/Pacific over-representation for equity validation |
| **Boundary case set** | ≥100 per boundary case category | Age <30, age >74, T1D vs T2D retinal start, formal refusal, July 2026 threshold edge, CVD equivalents, missing BP prerequisite |

All test patients require GP-reviewed ground truth labels for care gap detection. CVDRA ground truth is the reference Python implementation.

---

## 10. MBIE Evidence Statement

This document constitutes the Step 1 deliverable for Objective 1 of the NexWave R&D programme under contract CONT-109091-N2RD-NSIWKC: "Clear written definition of both tasks with success criteria."

**Development basis:**
- NZSSD / MoH Type 2 Diabetes Management Guidance (2021, updated 2023) — HbA1c intervals, annual review checklist, diabetes coding, eGFR/ACR monitoring matrix
- BPAC NZ Diabetes Toolbox (July 2021, updated July 2025) — practical annual review implementation
- MoH Quality Standards for Diabetes Care 2020 — 16-component quality framework
- MoH Cardiovascular Disease Risk Assessment and Management for Primary Care (2018, ISBN 978-1-98-853933-1) — CVDRA eligibility thresholds, recall intervals, CVD risk equivalents, equity provisions
- BPAC NZ "Hypertension in adults: the silent killer" (January 2023, updated June 2025) — BP targets, monitoring intervals, annual review components
- HISO 10071:2025 — NZ CVDRA data standard specifying PREDICT v.2019 equations and all coefficients
- Pylypchuk R et al. *The Lancet* 2018;391(10133):1897–1907 — PREDICT NZ Primary Prevention Equations development and validation (N=400,728, 1.69 million person-years)
- VIEW2020/PredictRiskScores — reference R implementation (GitHub, GPL-3.0)
- BPAC NZ "Slowing progression of renal dysfunction in patients with diabetes" (June 2019) — eGFR/ACR monitoring matrix
- NZ 2018 CVD Consensus Statement Table 4 — ethnicity and sex-stratified CVDRA initiation thresholds
- National Diabetes Roadmap (25 March 2026) — July 2026 diagnostic threshold change
- HQSC Frailty Care Guides 2023 — HbA1c targets for frail older people
- MoH "Diabetic Retinal Screening, Grading, Monitoring and Referral Guidance" (March 2016) — screening intervals and start rules
- NZ Read v2 code hierarchy and SNOMED CT NZ Edition (October 2025) — coding standards
- Clinical input from a practising New Zealand GP (programme director and clinical domain expert)

**Success criteria basis:** The ≥95% CVDRA calculation accuracy target is grounded in the Obj 1 grant deliverable specifying "prototypes on synthetic data: ≥95% CVDRA accuracy" under contract CONT-109091-N2RD-NSIWKC. The ≥85% care gap GP audit agreement target is from Obj 3. The recall-optimised design principle (prioritising sensitivity over specificity) is consistent with the clinical safety framework applied in the Inbox Helper specification.

**Regulatory note:** A system that both detects care gaps and computes clinical risk scores likely meets the TGA definition of clinical decision support software that is NOT exempt from medical device regulation (TGA guidance October 2025). The CVDRA calculation component in particular — producing a quantitative risk output intended to inform treatment decisions — almost certainly classifies as a Class IIa medical device under the Software as a Medical Device (SaMD) framework. Evidence documentation in this specification is designed to be compatible with TGA ARTG inclusion requirements and IMDRF GMLP principles. Under the Trans-Tasman Mutual Recognition Arrangement, TGA approval facilitates NZ market entry pending the Medical Products Bill (Cabinet decisions July 2025).
