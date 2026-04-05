# NZ diabetes monitoring rules for automated care gap detection

**The NZSSD/MoH Type 2 Diabetes Management Guidance (2021, updated 2023) is the authoritative source, supplemented by BPAC NZ and the MoH Quality Standards for Diabetes Care 2020.** These documents collectively define every threshold, interval, and component needed to implement automated care gap detection in a New Zealand GP practice management system. A critical change effective **1 July 2026** will lower the diagnostic HbA1c threshold from ≥50 to **≥48 mmol/mol**, aligning NZ with WHO/ADA standards and reclassifying approximately 34,500 people from prediabetes to diabetes. This report provides exact, code-ready specifications for each sub-question with source citations and conflict flags.

---

## SUB-QUESTION 1: The authoritative NZ guideline and its current status

The primary authoritative document is:

**"Type 2 Diabetes Management Guidance"**
- **Authors:** New Zealand Society for the Study of Diabetes (NZSSD) / Ministry of Health (MoH)
- **Publication date:** 18 January 2021
- **URL:** https://t2dm.nzssd.org.nz/
- **Updated:** 2023 (titled "Updated 2023 Recommendations from the NZSSD," available at https://t2dm.nzssd.org.nz/File-2.html)
- **Status as of April 2026:** Current, NOT superseded. It is a living document with periodic content updates (most recently March–May 2025 for medication funding changes). The NZSSD explicitly does not cover Type 1 diabetes or diabetes in children.

Supporting documents that clinicians and systems should also reference:

- **BPAC NZ Diabetes Toolbox** — seven articles published 5 July 2021, last updated 7 July 2025. Key article: "The annual diabetes review: screening, monitoring and managing complications" (https://bpac.org.nz/2021/diabetes-review.aspx). BPAC explicitly cites the NZSSD 2021 guidance as its primary source.
- **MoH Quality Standards for Diabetes Care 2020** — sets the annual review as a quality standard of care; 18 standards covering all aspects of diabetes care. Hosted at tewhatuora.govt.nz.
- **HQSC Frailty Care Guides 2023 — Diabetes/Mate Huka** — provides specific targets for frail older people (HbA1c up to 70 mmol/mol).
- **National Diabetes Roadmap** — released 25 March 2026 by Health Minister Simeon Brown. Sets a 5–10-year strategic direction, including the diagnostic threshold change effective 1 July 2026 and plans for a National Diabetes Register. Does not replace or supersede the NZSSD clinical guidance.

The predecessor guideline was the NZGG "Management of Type 2 Diabetes" (2011), now fully superseded. **No entirely new replacement guideline has been published in 2022–2026.** The 2021/2023 NZSSD guidance remains current.

**Recommendation for implementation:** Use the NZSSD 2021/2023 guidance as the primary rule source, cross-referenced with BPAC 2021 for the annual review checklist and the MoH Quality Standards 2020 for the quality framework.

---

## SUB-QUESTION 2: Exact HbA1c monitoring intervals by glycaemic control status

### Target threshold

There is **no single universal HbA1c threshold** separating "at target" from "not at target." The target is individualised per patient, with **<53 mmol/mol** as the default for most adults. For implementation purposes, **53 mmol/mol is the recommended default threshold** unless the patient has a documented individualised target.

### Monitoring interval framework

| Patient status | Interval | Source (exact quote) |
|---|---|---|
| **Not at target / treatment recently changed** | **Every 3 months** | NZSSD Glycaemic Targets section: "Should be measured 3 monthly until to target" |
| **At target / stable control** | **Every 6 months** | NZSSD Glycaemic Targets section: "6 monthly if stable control" |
| **Stable, well-controlled long-term** | **Annual (minimum floor)** | BPAC 2021 diabetes-management.aspx: "An annual check is sufficient for patients with stable, well controlled HbA1c levels" |

### Third tier (newly diagnosed / treatment changed)

No explicitly named third tier exists. The **3-monthly interval applies to both** newly diagnosed patients (being titrated to target) and patients with recent treatment changes. The NZSSD management algorithm states: "Repeat HbA1c testing every three months and escalate treatment if the target is not met."

### Type 1 vs Type 2 differences

The NZSSD T2DM guidance "does not cover the management of type 1 diabetes." However, the same 3-monthly (not at target) and 6-monthly (stable) framework is generally applied to both types in NZ primary care. BPAC older resources use the generic term "diabetics" for both types.

### Conflict flag

BPAC states "annual check is sufficient" for very stable patients, while NZSSD says "6 monthly if stable control." These are not contradictory — **6-monthly is the standard recommendation; annual is the minimum floor for the most stable patients**. For a care gap system, recommend: flag at **7 months** if last HbA1c was at target; flag at **4 months** if last HbA1c was above target.

---

## SUB-QUESTION 3: Full diabetes annual review component list

Per BPAC 2021 ("The annual diabetes review," updated 25 August 2021), NZSSD 2021 (Annual Diabetes Review section), and MoH Quality Standards for Diabetes Care 2020. The principle stated by BPAC: "Components of the 'annual diabetes review' may be performed at different times throughout the year, but all components should be performed at least once per year."

### Lab-based components (structured PMS data — electronic lab results)

| Component | Frequency | Lab test | Notes |
|---|---|---|---|
| **HbA1c** | 3–6 monthly (see SQ2) | Glycated Haemoglobin; LOINC 4548-4 | Returned electronically via HL7 |
| **uACR** | At least annually; 3–6 monthly if abnormal | Urine Albumin:Creatinine Ratio; LOINC 9318-7 | Thresholds: microalbuminuria >2.5 mg/mmol (males), >3.5 mg/mmol (females); macroalbuminuria >30 mg/mmol (NZSSD) |
| **Serum creatinine / eGFR** | At least annually; 3–6 monthly if abnormal | Serum Creatinine + eGFR (CKD-EPI); LOINC 2160-0 (creatinine), 33914-3 (eGFR) | eGFR auto-calculated by lab |
| **Non-fasting lipid panel** | At least annually | Total Cholesterol, HDL-C, LDL-C, Triglycerides; LOINC 2093-3, 2085-9, 13457-7, 2571-8 | Target: LDL <1.8 mmol/L if CVD risk >15% |
| **Liver function tests** | At least annually | LFTs (AST, ALT, GGT) | NAFLD association; confirmed by BPAC 2021 |

### Observation-based components (structured PMS data — vital signs / classified fields)

| Component | Frequency | PMS recording | Notes |
|---|---|---|---|
| **Blood pressure** | Minimum annually; each visit if hypertensive | Classified/observation data (vital signs) | Targets: <130/80 if complications or CVD risk >15%; <140/90 otherwise (NZSSD) |
| **Weight / BMI** | At least annually | Classified data (weight, height) | Waist circumference recommended but "not essential" (BPAC 2021) |
| **Smoking status** | At least annually | Coded data; NZ SNOMED reference set 72741000210106 | Part of CVD risk factor assessment |
| **CVD risk assessment** | At least annually | PREDICT calculator integrated into most PMS; stored as calculated value | Skip if established CVD (see SQ8) |

### Examination / referral components (partially structured or free-text)

| Component | Frequency | PMS recording | Notes |
|---|---|---|---|
| **Foot examination (neurovascular)** | At least annually | Partially structured; may be coded in bestpractice module; detailed findings typically free text | Includes peripheral pulses, sensation (monofilament), skin, nails, deformity |
| **Retinal photoscreening** | **Every 2 years** (not annual) | Not a lab result; recorded as incoming correspondence or separate screening database. Inconsistent electronic feeds | See SQ7 for detail |
| **Immunisation status** | At least annually | NIR/CIR data accessible; immunisation records in PMS | Influenza (funded annually), pneumococcal (recommended, not funded), COVID-19 |
| **Mental health / wellbeing** | At least annually | Partially; PHQ-9/GAD-7 scores may be stored via bestpractice module | MoH Quality Standard 5 |
| **Cancer screening status** | At least annually | Partially; National Screening Unit data linkable | Cervical, breast, bowel screening currency |
| **Medication review** | At least annually | Current medications structured; review notes free text | MoH Quality Standard 6 |
| **Dental health** | At least annually | Free text only | Teeth and gums examination; referral if periodontal disease |
| **Self-management education** | Ongoing; reviewed annually | Free text | MoH Quality Standard 4 |

### Additional components identified from BPAC/NZSSD (not in original list)

- **Alcohol intake and recreational drug use** — at least annually (BPAC 2021)
- **Contraception / pregnancy planning** — for women of reproductive age; at least annually (BPAC 2021)
- **Other complications review** — sexual dysfunction, recurrent skin/genitourinary infections, autonomic neuropathy (BPAC 2021; NZSSD lists gout, PCOS, frozen shoulder, dementia, fatty liver)

### Key note on LOINC codes

**NZ labs do not formally use LOINC codes in their reporting.** Lab results are exchanged via HL7 v2 messages with local test codes. The LOINC codes listed above are international standards useful for mapping but are not the native NZ lab coding system.

---

## SUB-QUESTION 4: Coding systems for identifying Type 2 diabetes patients

### Critical finding: NZ general practice does NOT use ICD-10 for problem lists

| Coding system | Where used in NZ | Status |
|---|---|---|
| **Read Codes Version 2** | GP PMS (Medtech32, Medtech Evolution) problem lists | Legacy — final release April 2016; still widely present in existing data |
| **SNOMED CT (NZ Edition)** | Mandated replacement for Read codes in primary care | Implementation ongoing; NZ Edition released April and October annually |
| **ICD-10-AM (Australian Modification)** | NZ hospitals — inpatient coding (NMDS) | NOT used in GP problem lists |

**Medtech Evolution** (>75% NZ GP market share) historically used **Read Codes Version 2** as the primary coding system for problem list diagnoses. The mandated direction is SNOMED CT, but as of 2026 many practices still have Read v2 coded data. ACC still translates SNOMED to Read codes because "our systems are not yet able to accept SNOMED CT directly" (ACC, updated 16 May 2025).

### Read codes for Type 2 diabetes (Read v2)

| Read Code | Description |
|---|---|
| **C10..** | Diabetes mellitus (root code — captures all types) |
| **C10F.** | Type 2 diabetes mellitus (primary T2DM hierarchy) |
| **C10F0** | T2DM with renal complications |
| **C10F1** | T2DM with ophthalmic complications |
| **C10F2** | T2DM with neurological complications |
| **C10F3** | T2DM with multiple complications |
| **C10F4** | T2DM with ulcer |
| **C10F5** | T2DM with gangrene |
| **C10F6** | T2DM with retinopathy |
| **C10F7** | T2DM — poor control |
| **C10F9** | T2DM without complication |
| **C10FJ** | Insulin-treated T2DM |
| **C10FQ** | T2DM with exudative maculopathy |

For Type 1 (exclusion purposes): **C10E.** and children (C10E0–C10EQ).

### SNOMED CT concepts for Type 2 diabetes

| SNOMED CT ID | Preferred term |
|---|---|
| **44054006** | Diabetes mellitus type 2 |
| **313436004** | Type 2 diabetes mellitus without complication |
| **237599002** | Insulin treated Type II diabetes mellitus |
| **190388001** | T2DM with renal complications |
| **190389009** | T2DM with ophthalmic complications |

### Treatment-specific codes

Read v2 has **C10FJ** for insulin-treated T2DM but **no specific code for "diet-controlled" T2DM**. SNOMED CT has **237599002** for insulin-treated T2DM but no pre-coordinated concept for diet-controlled T2DM. Treatment modality (diet, oral, insulin) is typically inferred from the medication list rather than coded distinctly.

### ICD-10 codes (for hospital data linkage only)

The full E11.x range (E11.0–E11.9 with subcategories) applies in NZ hospital data using ICD-10-AM. Key codes: **E11.9** (T2DM without complications), **E11.2** (with kidney complications), **E11.3** (with ophthalmic complications). Supplementary codes: **Z79.4** (long-term insulin use), **Z79.84** (oral hypoglycaemic drugs).

**Implementation recommendation:** Query the problem list using **Read code prefix C10F** (all children) OR **SNOMED concept 44054006 and descendants**. Exclude C10E (T1DM) from T2DM-specific rules. For practices still on Read v2, the C10F hierarchy is the reliable identifier.

---

## SUB-QUESTION 5: HbA1c target thresholds

### General target

**<53 mmol/mol** (equivalent to <7.0%) for most adults with Type 2 diabetes. Source: NZSSD Glycaemic Targets section — "The target HbA1c in most patients with diabetes is <53 mmol/mol" (bolded in original).

### Individualised targets

| Target (mmol/mol) | Patient group | Source |
|---|---|---|
| **<48** | Young patients (<40 years); low hypoglycaemia risk (not on insulin/sulfonylureas); planning pregnancy; existing microvascular complications | NZSSD Glycaemic Targets; BPAC Table 1 |
| **<53** | Most patients — "reasonable balance between reduction in microvascular risk and treatment risks" | NZSSD; BPAC |
| **54–70** | Frail elderly with cognitive impairment; functionally dependent; previous severe hypoglycaemia; significant hypoglycaemic unawareness; limited life expectancy | NZSSD; BPAC |
| **58–64** | Older people (not frail) | HQSC Frailty Care Guides 2023 |
| **Up to 70** | Older people with frailty | HQSC Frailty Care Guides 2023 |

NZSSD notes: "Hypoglycaemia usually only occurs in patients treated with insulin and/or sulfonylureas."

### Diagnostic thresholds

**Current (until 30 June 2026):**
- **Diabetes:** HbA1c **≥50 mmol/mol** (NZ-specific, higher than WHO ≥48 to maximise specificity)
- **Prediabetes ("at-risk"):** HbA1c **41–49 mmol/mol**
- **Normal:** **≤40 mmol/mol**
- Symptomatic: one HbA1c ≥50 sufficient for diagnosis
- Asymptomatic: two abnormal tests required (HbA1c ≥50 OR fasting glucose ≥7 mmol/L), same day or subsequent test without delay

**From 1 July 2026 (National Diabetes Roadmap, announced 25 March 2026):**
- **Diabetes:** HbA1c **≥48 mmol/mol** (aligned with WHO/ADA)
- **Prediabetes:** HbA1c **42–47 mmol/mol**
- **Normal:** **<42 mmol/mol**
- **No confirmatory test required** if HbA1c **>53 mmol/mol**
- Approximately **34,500 New Zealanders** will be reclassified from prediabetes to diabetes

Source: Pinnacle Practices "Diabetes changes are coming" (published 11 March 2026); Beehive.govt.nz "National diabetes action plan launched" (25 March 2026).

### Action thresholds (for urgent review)

| HbA1c (mmol/mol) | Action | Source |
|---|---|---|
| **>64 at diagnosis** | Start TWO glucose-lowering medicines simultaneously | NZSSD management algorithm |
| **≥75** | "Very poor glycaemic control. Warrants immediate action" | BPAC BPJ 42 (2012), Table 3 |
| **>80–90** | Insulin initiation recommended at any stage | NZSSD 2021/2023; BPAC 2021 |
| **>90 with symptoms** | Immediate insulin initiation | NZSSD management algorithm |

**Implementation recommendation:** Flag HbA1c **≥75 mmol/mol** for urgent GP review. Flag **>64 mmol/mol at diagnosis** for treatment escalation. Flag **>90 mmol/mol** for immediate clinical attention.

---

## SUB-QUESTION 6: eGFR and uACR thresholds for diabetic kidney disease

### Diagnostic thresholds (NZ aligns with KDIGO)

Diabetic kidney disease (DKD) is diagnosed when a patient with diabetes has **albuminuria (ACR >3 mg/mmol) AND/OR eGFR <60 mL/min/1.73m²**, in the absence of alternative causes. Two positive ACR samples are required for first diagnosis of persistent albuminuria.

Source: NZSSD t2dm.nzssd.org.nz Section 106 ("Management of diabetic kidney disease"); BPAC NZ "Slowing progression of renal dysfunction in patients with diabetes" (June 2019).

### Albuminuria staging

| Stage | ACR (mg/mmol) | Description |
|---|---|---|
| A1 | <3 | Normal to mildly increased |
| A2 | 3–30 | Moderately increased (microalbuminuria) |
| A3 | >30 | Severely increased (macroalbuminuria) |

Note: NZSSD uses sex-specific thresholds for microalbuminuria screening: **>2.5 mg/mmol (males), >3.5 mg/mmol (females)**. The KDIGO-aligned staging above uses **3 mg/mmol** uniformly.

### Monitoring frequency by eGFR and ACR stage

Adapted from KDIGO 2013, published for NZ primary care in BPAC NZ (June 2019, Table 3):

| eGFR (mL/min/1.73m²) | ACR <3 | ACR 3–30 | ACR >30 |
|---|---|---|---|
| **≥90** | Annually | Annually | 6-monthly |
| **60–89** | Annually | Annually | 6-monthly |
| **45–59** | Annually | 6-monthly | 4-monthly |
| **30–44** | 6-monthly | 4-monthly | 4-monthly |
| **15–29** | 4-monthly | 4-monthly | 3-monthly |
| **<15** | 3-monthly | 3-monthly | 3-monthly |

### Key inflection points for implementation

- **eGFR <60:** DKD diagnosis threshold; any albuminuria triggers more frequent monitoring
- **eGFR <45:** Monitoring increases to at least 6-monthly even with normal ACR; metformin dose adjustment required (max 1g/day if CrCl 30–60); **diabetes + eGFR <45 = CVD equivalent** in NZ guidelines (2018 NZ CVD Consensus Statement, BPAC 2018) — this is NZ-specific
- **eGFR <30:** Referral to nephrologist recommended; 4-monthly or more frequent monitoring
- **eGFR decline >10 mL/min per year or >1 mL/min per month:** Urgent referral to renal team (NZSSD)
- **ACR >30 mg/mmol (overt nephropathy):** Automatically confers >20% five-year CVD risk per NZ 2003 CVDRA guideline

### NZ-specific deviations from KDIGO

NZ **largely aligns with KDIGO** with these exceptions:

1. **Units:** NZ uses mg/mmol for ACR (not mg/g as in US). **3 mg/mmol ≈ 30 mg/g** — a unit conversion difference, not a clinical threshold difference.
2. **CVD equivalence:** The 2018 NZ CVD Consensus Statement defines **diabetes AND eGFR <45** as a CVD equivalent — more aggressive than international standards that typically use eGFR <30 for non-diabetic CKD.
3. **Nephrology referral thresholds** vary by region: NZSSD recommends referring at eGFR <45 and falling; some regions specify <30 (BPAC 2019).
4. **NZSSD CVD/ESRD risk calculator** at nzssd.org.nz/cvd_renal/ includes an end-stage renal disease risk component alongside CVD risk — this is NZ-specific for adults with T2DM without previous CVD.

---

## SUB-QUESTION 7: Retinal screening organisation and GP recording

### Programme structure

Retinal screening is **NOT run by individual GP practices or PHOs.** It is a regionally organised programme under **Health NZ / Te Whatu Ora districts** (previously DHBs). Each region has a central coordinator responsible for appointment invitations, recalls, attendance tracking, and referrals. A designated lead clinical ophthalmologist oversees quality and clinical governance in each region. The governing document is the MoH "Diabetic Retinal Screening, Grading, Monitoring and Referral Guidance" (March 2016, ISBN 978-0-947491-66-6).

There is **no single centralised national screening database** — this was identified as a gap in multiple publications (including a 2023 University of Auckland study in PMC10194990). The National Diabetes Roadmap (March 2026) plans to address this.

### Screening intervals

| Patient group | Interval | Source |
|---|---|---|
| **Standard (most T2DM patients)** | **Every 2 years** | MoH 2016 Guidance Section 4; BPAC 2021 |
| **Low risk (no DR detected, HbA1c consistently ≤64, no clinical modifiers)** | Can extend to **3 years** | MoH 2016 Guidance Table 1 |
| **Higher risk** — HbA1c >64, diabetes >10 years, BP ≥160/95, eGFR <45, ACR >100, foot ulcers | **More frequent** (risk-stratified) | MoH 2016 Guidance Table 1 |
| **Pregnancy (established T1D/T2D)** | First trimester, then minimum 3-monthly | MoH 2016 Section 3.1 |

Starting points: **T2DM — at diagnosis.** T1DM — within 5 years of diagnosis. Gestational diabetes does NOT require retinal screening.

### Recording in Medtech Evolution

Retinal screening results are **NOT recorded as a lab result** in the traditional sense. They typically appear as:
- An **incoming correspondence/letter** from the screening service
- Some regions provide electronic feeds to PMS, but this is **inconsistent** across NZ
- The primary screening database is held by the **regional Health NZ screening service**, not in the GP PMS

**Critical implication for care gap detection:** If no retinal screening record appears in the GP PMS, the patient **may still have been screened** — the result could exist only in the regional screening database. A care gap system should flag the absence but note this limitation. National coverage data shows only **~62% of eligible people** received biennial screening nationally (2006–2019 data, PMC10194990), so absence genuinely indicates missed screening in many cases.

---

## SUB-QUESTION 8: Exclusion and special-case rules

### Type 1 diabetes patients

T1D patients should **NOT be excluded** from care gap monitoring. They share the same annual review components: HbA1c, ACR, eGFR, retinal screening, foot check, BP, lipids, CVD risk assessment, mental health. Key differences are:

- **Retinal screening start:** T1D within 5 years of diagnosis (vs at diagnosis for T2D)
- **Specialist oversight:** T1D is typically co-managed with secondary care
- **CVD risk calculator:** PREDICT requires specifying diabetes type as an input variable
- **Glycaemic monitoring:** T1D may use CGM (Freestyle Libre 2 funded from October 2024)

**Implementation recommendation:** Apply shared annual review components to T1D patients but flag them separately and adjust retinal screening start rules.

### Established CVD patients and CVDRA

**Patients with diabetes AND established CVD should skip the CVD Risk Assessment calculation.** This is explicitly stated in multiple NZ sources:

BPAC NZ (May 2018, "What's new in cardiovascular disease risk assessment"): *"In patients with pre-existing CVD or a CVD risk equivalent, assertive risk management and lifestyle modification is strongly recommended. Using risk equations for these patients is NOT necessary."*

CVD risk equivalents that also skip CVDRA include:
- Prior cardiovascular event (angina, CABG, MI, PCI, PVD, stroke, TIA)
- Familial hypercholesterolaemia
- Congestive heart failure
- **Diabetes with eGFR <45 mL/min/1.73m²**
- Stage 4+ CKD (eGFR <30)
- Coronary artery calcium score >400
- Isolated extreme risk factor (TC ≥8, TC:HDL ≥8, or BP ≥180/100)

Source: MoH 2018 Cardiovascular Disease Risk Assessment and Management Consensus Statement; BPAC 2018; Heart Foundation CVD Consensus Summary; NZSSD CVD Risk Calculator exclusion list.

**Implementation:** If a patient has a coded CVD diagnosis or CVD equivalent condition, suppress the CVDRA care gap and instead flag for "intensive risk factor management."

### Special cases

**Gestational diabetes history:** Women with prior GDM have up to 50% risk of developing T2D within 5 years postpartum. Post-GDM follow-up: HbA1c at 3 months post-birth, then **annual HbA1c monitoring** thereafter (BPAC July 2015; MoH 2014). GDM alone does NOT qualify for diabetes annual review — only if T2D is subsequently diagnosed. GDM does NOT require retinal screening (MoH 2016 Section 2.2).

**Steroid-induced / secondary diabetes:** No NZ-specific monitoring guideline exists. For retinal screening, secondary diabetes (NODAT, post-pancreatectomy, cystic fibrosis-related) is treated **as per T1D** when there is a defined onset date. When the type or onset date is uncertain, treat **as per T2D with immediate screening** (MoH 2016 Section 3.1).

**MODY:** No NZ-specific MODY monitoring guideline. Typically under specialist care. Same annual review components apply.

**Post-transplant diabetes (NODAT):** Treated as per T1D for retinal screening. Typically under transplant team oversight.

### Revised or removed diagnosis

No specific NZ guideline addresses this. Recommended logic:
- If diabetes diagnosis is removed entirely → remove from diabetes annual review programme and retinal screening
- If reclassified (e.g., T2D to MODY or prediabetes) → adjust monitoring rules accordingly
- Prediabetes patients are explicitly excluded from retinal screening (MoH 2016 Section 2.2) but should have annual HbA1c monitoring (NZSSD)

### Newly diagnosed patients

No explicit NZ "grace period" is defined. For T2D, all annual review components should begin at diagnosis (bloods, retinal screening referral, CVD risk assessment). **Recommended implementation:** allow a 3-month grace period before flagging care gaps for newly diagnosed T2D patients, acknowledging baseline investigations take time to schedule.

---

## SUB-QUESTION 9: PHO Performance Programme metrics and successors

### Historical PHO Performance Programme (2005–~2016)

The PPP had **two specific diabetes indicators** (per DHBNZ Indicator Definitions Version 5):

1. **Diabetes Detection:** 90% of enrolled patients aged 15–79 estimated to have diabetes to be identified and coded (Read code root C10). Weighted 9% of annual PPP payment.
2. **Diabetes Follow-Up After Detection:** 80% of enrolled patients with diabetes aged 15–79 to receive an appropriate annual review. Weighted 9% of annual PPP payment.

The PPP definition of an "appropriate diabetes review" included: HbA1c, microalbuminuria (ACR), lipid profile, CVD risk review, foot examination, retinal screening (every 2 years), and care plan update (BPAC BPJ 41, December 2011).

### Programme evolution

| Period | Framework | Diabetes-specific? |
|---|---|---|
| 2005–~2014 | PHO Performance Programme (PPP) | Yes — detection + annual review indicators |
| ~2014–2016 | "Little IPIF" (transitional) | Essentially rebadged PPP |
| July 2016 onwards | System Level Measures (SLM) Framework | No — high-level outcomes only (e.g., ambulatory-sensitive hospitalisations) |
| 1 July 2025 | Contingent Capitation ($60M) | No — initial focus on data sharing and childhood immunisation |
| 25 March 2026 | National Diabetes Roadmap | Strategic direction; no specific practice-level performance indicators yet |

### Gaps between PHO/performance measures and clinical guidelines

Five significant gaps exist:

1. **No national HbA1c outcome target.** The PPP measured detection and review completion but never implemented a funded indicator measuring the proportion of patients achieving target HbA1c. A planned "Phase 3" measuring patient outcomes was never nationally realised before the programme was superseded.
2. **No nationally available HbA1c results data.** The HQSC explicitly notes HbA1c *results* are not available nationally — only whether the test was ordered. This limits outcome-based quality measurement.
3. **Incomplete component coverage.** The PPP review definition included 7 components, while the clinical guidelines (NZSSD 2023, MoH Quality Standards 2020) recommend at least 16 components. Mental wellbeing, dental health, BMI, eGFR (separate from ACR), neuropathy assessment, and medication review were not all captured in PPP reporting.
4. **Post-PPP vacuum.** After SLMs replaced the PPP in 2016, diabetes-specific pay-for-performance at practice level effectively ceased nationally. PHOs may still locally incentivise diabetes care but this varies.
5. **Retinal screening tracked separately.** Retinal screening has its own monitoring pathway through the regional screening programme, creating potential gaps in reporting integration.

### Impact on PMS data recording

PHO reporting requirements have historically been a **primary driver of structured diabetes coding** in Medtech. The PPP's requirement for specific Read codes (C10 root) drove practices to code diagnoses correctly. BPAC BPJ 41 (2011) noted: "The Programme has helped develop standards for the systematic recording of specific health information, and where necessary, funding changes to practice management systems."

### RNZCGP Foundation Standard

The Foundation Standard is a practice-quality assurance standard, **not a clinical performance measure**. It does not include specific diabetes clinical indicators. Cornerstone CQI modules may involve practice-level audit of chronic conditions, but indicators are determined locally, not prescribed nationally.

### HQSC Atlas of Healthcare Variation

The HQSC tracks: HbA1c testing rates, ACEI/ARB dispensing rates, hypoglycaemic medication dispensing rates, and diabetes-related hospital bed-day occupancy — analysed by ethnicity, deprivation, and district. These are observational analytics, not performance-linked payments.

---

## Conclusion: implementation decision matrix

For an automated care gap detection system in NZ general practice, the operational rules reduce to a surprisingly compact set of triggers. **Use NZSSD 2021/2023 as the primary rule source**, supplemented by BPAC 2021 for the annual review checklist. Identify patients via **Read code C10F (and descendants) or SNOMED 44054006 (and descendants)** on the problem list — not ICD-10, which is hospital-only in NZ.

The core detection logic requires just three tiers: flag HbA1c at **4 months overdue** if above target, **7 months** if at target; flag all annual review labs (ACR, eGFR, lipids, LFTs) at **13 months** since last result; flag retinal screening at **25 months** (not 13, since NZ uses 2-yearly intervals). Apply the eGFR/ACR monitoring matrix from BPAC 2019 for patients with kidney disease. Suppress CVDRA gaps for patients with coded CVD or CVD equivalents. Prepare for the **1 July 2026 diagnostic threshold change** to ≥48 mmol/mol, which will require a one-time sweep of prediabetes patients (HbA1c 48–49) for reclassification.

The biggest implementation risk is not clinical thresholds but **data completeness**: retinal screening results often live outside the GP PMS, foot examination and mental health assessments are frequently free-text only, and the transition from Read v2 to SNOMED CT means coding heterogeneity across practices. A robust system must account for these structural gaps in the data layer, not just the clinical rules.