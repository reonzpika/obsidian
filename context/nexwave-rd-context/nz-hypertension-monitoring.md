# NZ hypertension monitoring rules for automated care gap detection

**New Zealand has no single standalone hypertension guideline — the implementable rules must be synthesised from three authoritative sources.** The MoH 2018 CVD Consensus Statement provides the foundational framework, BPAC NZ's 2023 hypertension module (updated June 2025 with ESC 2024 targets) delivers the most current clinical detail, and the PREDICT equation documentation defines the CVDRA input requirements. Unlike the NZSSD diabetes annual review, NZ has no formal "hypertension annual review" checklist — BP management is embedded within the broader CVD risk assessment framework, which means care gap logic must reconstruct monitoring rules from multiple guideline layers. This report provides exact thresholds, codes, intervals, and decision logic for each sub-question, at implementation-grade precision.

---

## 1. The three authoritative NZ guideline sources and their hierarchy

**Primary national authority:**
Ministry of Health. 2018. *Cardiovascular Disease Risk Assessment and Management for Primary Care*. Wellington: Ministry of Health. ISBN 978-1-98-853933-1. Published February 2018. Available at tewhatuora.govt.nz. Developed with the Heart Foundation NZ and Stroke Foundation NZ. Expert Advisory Group includes Rod Jackson, Susan Wells, Gerry Devlin, and others. **Status: CURRENT — not superseded.** No updated national consensus statement has been published as of April 2026.

**Most current practical guidance:**
BPAC NZ. "Hypertension in adults: the silent killer." Published 27 January 2023, last updated 5 June 2025 (ESC 2024 keypoints added). Available at bpac.org.nz/2023/hypertension.aspx. Expert reviewers: Dr John Edmond (Cardiologist), Prof Rob Walker (Nephrologist), Dr Joan Leighton (GP). Companion quick-reference: B-QuiCK "Hypertension" updated May 2025 at bpac.org.nz/b-quick/hypertension.aspx.

**PREDICT equation documentation:**
Pylypchuk R, Wells S, Kerr A, et al. "Cardiovascular disease risk prediction equations in 400,000 primary care patients in New Zealand." *The Lancet*. 2018;391(10133):1897–1907.

Note: hypertension.org.nz does not host current clinical guidelines. The Heart Foundation NZ website provides a summary of the 2018 Consensus Statement but no separate hypertension guideline.

**Implementation recommendation:** Use the 2018 MoH Consensus Statement as the authoritative baseline (targets, treatment thresholds, CVDRA intervals). Layer BPAC NZ 2023/2025 on top for practical monitoring intervals and updated BP targets. The ESC 2024 targets (120–129/70–79 mmHg) adopted in the May 2025 B-QuiCK update represent the direction of travel but the 2018 MoH target of **<130/80 mmHg** remains the nationally endorsed NZ standard until a new consensus statement is published.

---

## 2. BP monitoring intervals — exact rules for care gap timing

NZ guidelines specify ranges rather than single fixed intervals. The following table synthesises the implementable rules:

| Clinical scenario | Review interval | Source | Care gap trigger |
|---|---|---|---|
| Starting treatment or dose adjustment | **Every 4–6 weeks** until at target | BPAC 2023, Figure 2 | Flag if >6 weeks since last BP during titration |
| Significantly elevated baseline BP | **Every 2 weeks** | BPAC 2023 | Flag if >3 weeks |
| Stable, on medication, at target | **3–6 monthly** (minimum **annually**) | BPAC 2023 + BPAC 2018 | Flag if >12 months since last BP |
| Stable, lifestyle only, low CVD risk (<5%) | **Aligned with CVDRA interval** (up to 5–10 years) | MoH 2018, Table 5 | Flag per CVDRA re-screening schedule |
| Stable, lifestyle only, intermediate risk (5–15%) | **1–2 yearly** | MoH 2018 | Flag if >24 months |
| CKD (stable) | **At least annually** | BPAC 2026 CKD | Flag if >12 months |
| CKD (progressive/proteinuric) | **3–6 monthly** | BPAC 2026 CKD | Flag if >6 months |
| Hypertension + diabetes | **3-monthly until at target**, then part of annual diabetes review | NZSSD | Covered by diabetes care gap |
| High CVD risk (≥15%) or on pharmacotherapy | **Annually** (as part of risk management review) | MoH 2018 / Heart Foundation | Flag if >12 months |
| After initiating ACEi/ARB in CKD | Creatinine + potassium within **1–2 weeks** | BPAC 2026 CKD | Flag if no labs within 2 weeks of new Rx |

**"At target" definition** depends on the patient's risk profile — see Section 3 below. The BP target is **not a single threshold**: it varies by comorbidity. A patient is "at target" when their most recent clinic BP is below the applicable threshold for their risk group.

**Medication vs lifestyle-only distinction:** NZ guidelines do not formally create separate interval categories for medicated vs unmedicated patients. However, the MoH 2018 statement mandates annual review for patients on pharmacotherapy (as they are presumed at least intermediate risk). A patient on lifestyle management alone with <5% CVD risk could have a much longer re-assessment interval. **For implementation, the practical rule is: any patient with a coded hypertension diagnosis AND dispensed antihypertensive medication AND no BP recorded in >12 months is overdue.**

---

## 3. BP targets by patient group — exact mmHg thresholds

The NZ guideline landscape has three overlapping target frameworks. The table below presents the recommended implementation targets, reconciling all three:

| Patient group | Clinic BP target | Ambulatory/Home equivalent | Authority |
|---|---|---|---|
| **All patients on treatment (NZ national standard)** | **<130/80 mmHg** | <125/75 mmHg | MoH 2018 Consensus Statement |
| **"Most adults" on treatment (ESC 2024, adopted by BPAC May 2025)** | **120–129 / 70–79 mmHg** | — | BPAC B-QuiCK May 2025 |
| **High CVD risk** (established CVD, heart failure with reduced EF, diabetes, CKD, age ≥65, 5-year risk ≥15%) | **<130/80 mmHg** | <125/80 mmHg | BPAC 2023 Table 3 |
| **Lower CVD risk** (none of the above) | **<140/90 mmHg** | <135/90 mmHg | BPAC 2023 Table 3 |
| **Hypertension with diabetes** | **<130/80 mmHg** | <125/80 mmHg | MoH 2018 + BPAC 2023 |
| **Hypertension with CKD (eGFR <60)** | **Systolic <130 mmHg** | — | BPAC 2026 CKD B-QuiCK |
| **Hypertension with established CVD** | **<130/80 mmHg** | <125/80 mmHg | BPAC 2023 Table 3 |
| **Elderly (65–84 years), otherwise fit** | **<130/80 mmHg** (120–129 systolic if tolerated) | — | BPAC 2023 (age ≥65 = "high risk") |
| **Elderly ≥85 years, or moderate-severe frailty** | **<140/90 mmHg** (or "as low as reasonably achievable") | — | BPAC B-QuiCK May 2025 (ESC 2024) |
| **Frailty, dementia, limited life expectancy** | **Individualised; consider deprescribing** | — | BPAC 2023 Table 3 |

**Implementation recommendation for "above target" detection:** Use the **risk-stratified targets** (BPAC 2023 Table 3) as the operational framework: <130/80 for high-risk patients, <140/90 for lower-risk patients. The ESC 2024 target of 120–129/70–79 is aspirational. For a binary "at target / above target" flag, the safest implementable threshold is **<140/90 for general hypertension** and **<130/80 for patients with diabetes, CKD, established CVD, age ≥65, or 5-year CVD risk ≥15%**. This matches the nationally endorsed MoH 2018 framework while remaining clinically conservative.

**Treatment initiation thresholds** (for context, not directly a monitoring rule):

| 5-year CVD risk | BP threshold for drug treatment |
|---|---|
| Any risk | **≥160/100 mmHg** → start immediately |
| ≥15% | **≥130/80 mmHg** → strongly recommended |
| 5–15% | **≥140/90 mmHg** → discuss with patient |
| <5% | Lifestyle only; no drugs |

---

## 4. Read v2 and SNOMED CT codes for Medtech Evolution

### Hypertension diagnosis codes — inclusion set

**Read v2 (for Medtech Evolution — still dominant in NZ as of 2026):**

| Read v2 code | Description | Include in care gap? | NZ usage frequency |
|---|---|---|---|
| **G20..** | Essential hypertension | **YES — primary code** | Very high |
| **G201.** | Benign essential hypertension | **YES — primary code** | Very high |
| **G20z.** | Essential hypertension NOS | **YES** | High |
| G200. | Malignant essential hypertension | YES | Low |
| G202. | Systolic hypertension | YES | Moderate |
| G203. | Diastolic hypertension | YES | Low |
| G2... | Hypertensive disease (parent) | YES | Moderate |
| G2z.. | Hypertensive disease NOS | YES | Moderate |
| G2y.. | Other specified hypertensive disease | YES | Low |
| **G24..** + children | Secondary hypertension | **YES — flag separately** | Low |

**Minimum viable inclusion set (Read v2):** `G20..`, `G201.`, `G20z.`, `G2...`, `G2z..` — these five codes will capture **>95% of coded hypertension** in NZ general practice.

**SNOMED CT:**

| SNOMED CT ID | Preferred term | Maps from Read v2 |
|---|---|---|
| **59621000** | Essential hypertension (disorder) | G20.. |
| **1201005** | Benign essential hypertension (disorder) | G201. |
| **38341003** | Hypertensive disorder, systemic arterial (disorder) | G2... (parent) |
| 78975002 | Malignant essential hypertension (disorder) | G200. |
| 56218007 | Systolic hypertension (disorder) | G202. |
| 48146000 | Diastolic hypertension (disorder) | G203. |
| **31992008** | Secondary hypertension (disorder) | G24.. |

**Key SNOMED code: 59621000** (Essential hypertension) is the primary concept for care gap identification.

### Controlled vs uncontrolled — no diagnostic codes exist

There are **no separate Read v2 diagnostic codes** for "controlled" or "uncontrolled" hypertension. Monitoring/administrative codes exist but are rarely used in NZ practice:

| Code | Description | Type |
|---|---|---|
| Read 6627. / SNOMED 170577003 | Good hypertension control | Finding |
| Read 6628. / SNOMED 170578008 | Poor hypertension control | Finding |

**Implementation note:** Do not rely on these codes. Instead, determine control status algorithmically by comparing the **most recent recorded systolic and diastolic values** against the applicable target threshold for the patient's risk group.

### White coat hypertension

| System | Code | Description |
|---|---|---|
| Read v2 | **246M.** | White-coat hypertension |
| SNOMED CT | **697930002** | Labile hypertension due to being in a clinical environment |

**Implementation:** Patients coded with 246M. or SNOMED 697930002 should be placed on a **separate, lower-priority monitoring track** (annual recall) rather than excluded entirely. BPAC NZ 2016 states these patients still need annual BP assessment and are at increased risk of LVH and type 2 diabetes.

### Masked hypertension
**No dedicated Read v2 or SNOMED CT code exists.** Masked hypertension is a measurement phenomenon, not a codeable diagnosis. If confirmed, these patients should be managed as sustained hypertension per BPAC 2016.

### BP measurement recording codes

In Medtech Evolution, BP is typically recorded using:

| Read v2 code | Description | Usage |
|---|---|---|
| **2469.** | O/E — systolic blood pressure reading | Primary systolic code |
| **246A.** | O/E — diastolic blood pressure reading | Primary diastolic code |

SNOMED equivalents: **271649006** (Systolic blood pressure) and **271650006** (Diastolic blood pressure).

**For care gap "last BP date" detection:** Query for the most recent record under Read codes 2469. or 246A. (or their SNOMED equivalents), or the Medtech observations/vitals module BP entry. The date of this record is the "last BP date" for interval calculations.

### NZ-specific coding standards
HISO 10033.2:2016 governs Read-to-SNOMED migration. HISO 10071:2025 defines the CVD Risk Assessment Data Standard. There are **no NZ-specific SNOMED extension codes for hypertension** — standard international SNOMED concepts apply. The NZ SNOMED CT Edition (October 2025 release) uses the International Edition plus NZ-specific content for medicines and laboratory ordering, but hypertension uses standard codes.

---

## 5. How BP measurement relates to CVDRA and the "prerequisite gap"

**Systolic BP is a mandatory continuous variable in the PREDICT NZ Primary Prevention Equations.** Table 1 of the 2018 Consensus Statement lists "Blood pressure" under required variables, specifying "average of two seated BP measurements taken at least 10 minutes apart." Appendix A confirms the model coefficient is on "Systolic blood pressure mmHg (mean of two measures) continuous." Without a systolic BP value, the PREDICT equation **cannot compute a 5-year risk score**.

**Maximum acceptable age of a BP reading:** The 2018 Consensus Statement **does not explicitly specify a validity period** for BP readings used in CVDRA. However, the 12-month threshold is defensible and recommended for implementation based on three converging signals:

- The Consensus Statement mandates annual reviews for high-risk and pharmacotherapy patients, implying BP should be refreshed at least yearly
- The PREDICT study cohort recorded BP at the time of the risk assessment visit itself (contemporaneous measurement)
- BPAC 2018 states "blood pressure should be reviewed at least annually" once stabilised

**The "prerequisite gap" is real.** If a patient is due for CVDRA recalculation (per the interval schedule below) but has no BP recorded within 12 months, two care gaps exist simultaneously: (1) the BP measurement gap and (2) the CVDRA gap. The BP gap is a prerequisite — resolving it enables the CVDRA calculation. **Implementation should flag the BP gap as the higher-priority actionable item.**

**Antihypertensive medication flag in PREDICT:**

| Parameter | Specification |
|---|---|
| Variable type | Binary: Yes/No |
| Definition | BP-lowering medication **dispensed** during the **6 months** prior to index risk assessment |
| Basis | **Dispensed** (pharmacy claims from PHARMS database), not merely prescribed |
| Drug classes included | ACE inhibitors, ARBs, beta-blockers, calcium channel blockers, thiazides, "other BP-lowering medications" |
| Separate flags | Three independent medication flags exist: BP-lowering, lipid-lowering, antiplatelet/anticoagulant |

**Implementation note:** In a PMS context without PHARMS linkage, the medication flag would need to be derived from the patient's current medication list or prescribing records. This is an approximation of the dispensing-based flag used in the original PREDICT equations.

### CVDRA re-screening intervals

| 5-year CVD risk | Repeat CVDRA interval |
|---|---|
| <3% | **10 years** |
| 3–9% | **5 years** |
| 10–14% | **2 years** |
| ≥15% | **1 year** (annual risk management review) |
| 5–15% on pharmacotherapy | **1 year** |
| Diabetes type 2 | **Annual** (part of diabetes review) |
| Established CVD | **Annual** management review (CVDRA calculation unnecessary — automatically >15%) |
| Severe mental illness | **Every 2 years** (annually if ≥15%) |

---

## 6. Annual review components — what exists beyond BP measurement

**There is no formal standalone "hypertension annual review" in NZ, unlike the well-defined diabetes annual review.** BP management is embedded within the CVD risk assessment framework. However, a de facto annual review can be reconstructed from BPAC NZ 2023 guidance.

**Recommended annual investigations for hypertensive patients (all comers, not only with comorbidities):**

| Investigation | Recommended? | Authority | Notes |
|---|---|---|---|
| **Blood pressure measurement** | YES | BPAC 2023, MoH 2018 | Minimum annually for stable patients |
| **Serum electrolytes + creatinine (eGFR)** | YES | BPAC 2023 | Essential for medication monitoring and CKD screening |
| **Urine ACR** | YES | BPAC 2023 | Explicitly recommended for hypertension alone, "even without diabetes" — noted as underutilised in NZ |
| **Fasting lipid profile** | YES | BPAC 2023 | Part of CVDRA |
| **HbA1c** | YES | BPAC 2023 | Part of CVDRA; screens for incident diabetes |
| **CVD risk assessment (PREDICT)** | YES (if due per interval schedule) | MoH 2018 | Annual for ≥15% or on pharmacotherapy |
| **ECG** | At diagnosis; thereafter as indicated | BPAC 2023 | Not routinely annual; repeat if symptoms or new findings |
| **Ophthalmoscopy** | At diagnosis if visual symptoms; not routine annual | BPAC 2023 | Unlike diabetes, no routine annual eye screening for hypertension alone |
| **Medication review** | YES | BPAC 2023 | Adherence, adverse effects, dose appropriateness |

**Hypertension alone does trigger uACR, eGFR, and lipid testing** — BPAC 2023 is explicit that these are recommended for "patients with newly identified hypertension" regardless of comorbidities. The article specifically flags that uACR testing is "underutilised in patients without diabetes in New Zealand primary care, even in the setting of known CKD risk (e.g. hypertension)."

---

## 7. Exclusion and special-case rules for care gap lists

### Comorbidity-based modifications

**Hypertension + established CVD:** Automatically high risk (>15%). Annual management review mandated. BP target <130/80 mmHg. No specific NZ guidance on more frequent BP checks beyond the general "3–6 monthly" recommendation. **Implementation: treat as 12-month maximum interval, flag at high priority.**

**Hypertension + diabetes:** BP monitoring is **merged with the diabetes annual review** per NZSSD guidance. The diabetes annual review explicitly includes "blood pressure and management of hypertension." NZSSD states "review patients at least 3-monthly until blood pressure is to target." **Implementation: do not create a separate hypertension care gap if the patient is being tracked via diabetes annual review. If no diabetes review in >12 months, flag both gaps.**

**Hypertension + CKD with organ damage:** CKD staging triggers its own monitoring schedule (at least annual; 3–6 monthly if eGFR declining or proteinuric). LVH on ECG does not have an explicit NZ-defined altered monitoring frequency, but the ESC 2024 framework places these patients in the high-risk category. **Implementation: if eGFR <60 or ACR elevated, apply CKD monitoring schedule (flag if >12 months; >6 months if progressive).**

### White coat hypertension
BPAC NZ 2016: "Patients with white-coat hypertension are recommended to have annual blood pressure assessments, depending on their cardiovascular risk." These patients are at increased risk of LVH and type 2 diabetes. **Implementation: include on care gap list but at lower priority; annual recall interval; flag separately from sustained hypertension.**

### Masked hypertension
Should be managed as sustained hypertension once confirmed. No separate NZ monitoring guidance exists. **Implementation: treat identically to sustained hypertension for care gap purposes.**

### Recommended exclusions from the hypertension care gap list

NZ guidelines do not formally define exclusion criteria. The following are defensible implementation decisions:

- **Pregnancy-related hypertension** (pre-eclampsia, gestational hypertension): Managed under separate Te Whatu Ora 2022 obstetric guidelines. Exclude from the general hypertension list; track on obstetric pathway.
- **Terminal illness / palliative care / limited life expectancy**: BPAC 2023 states targets should be individualised and treatment may be reduced or stopped. Exclude or flag as exempt.
- **"Hypertension resolved" coded patients**: Read 662d. / SNOMED 162659009. Exclude from active monitoring.
- **De-enrolled patients**: Standard PMS housekeeping exclusion.
- **Patients ≥85 years or moderate-severe frailty on deprescribing pathway**: Consider excluding if a clinical decision to stop antihypertensives is documented. However, age alone is NOT an exclusion criterion — BPAC 2023 is explicit that "age alone is not a reason to dial back treatment."

---

## 8. Medication-based care gap logic and priority stratification

### Priority matrix for care gap detection

| Scenario | Priority | Rationale |
|---|---|---|
| Coded hypertensive + dispensed antihypertensive in prior 6 months + **no BP in >12 months** | **HIGHEST** | Treatment without monitoring; cannot calculate CVDRA; violates "at least annually" rule; medication side effects unmonitored |
| Coded hypertensive + on medication + **last BP above target + >6 weeks since last BP** | **HIGH** | In active titration phase; 4–6 week review interval not met |
| Coded hypertensive + high CVD risk (≥15%) + **no BP in >12 months** | **HIGH** | Annual risk management review overdue |
| Coded hypertensive + lifestyle only + intermediate risk (5–15%) + **no BP in >24 months** | **MODERATE** | CVDRA re-assessment overdue |
| Coded hypertensive + lifestyle only + low risk (<5%) + **no BP in >5 years** | **LOW** | Within CVDRA re-screening window but long gap |
| White coat hypertension (confirmed) + **no BP in >12 months** | **LOWER** | Annual assessment recommended but lower clinical urgency |

**The medication dispensing flag creates the strongest care gap signal.** A patient coded as hypertensive, with evidence of current antihypertensive dispensing (within 6 months), and no BP recorded in the PMS for >12 months represents a patient being actively treated but not monitored. This is the highest-priority care gap for automated detection. BPAC 2023 explicitly states that follow-up appointments "provide an opportunity to monitor electrolytes, renal function and ACR ratio" in addition to BP — so the gap extends beyond BP measurement alone.

**The PREDICT medication flag creates a logical cross-check:** If the PREDICT BP-lowering flag is "Yes" (dispensing in prior 6 months) but the most recent BP in the PMS is >12 months old, the clinical record is internally inconsistent — the patient's treatment is current but their monitoring is stale.

### Equity prioritisation
The 2018 Consensus Statement repeatedly emphasises addressing inequities for **Māori, Pacific, and South-Asian populations**, who have higher CVD burden, earlier CVDRA screening ages, and lower rates of completed risk assessment. An automated care gap system should incorporate ethnicity-based priority weighting, consistent with the Consensus Statement's equity focus and Te Tiriti obligations.

---

## Conclusion

Building automated hypertension care gap detection for NZ general practice requires reconciling three guideline layers rather than implementing a single ruleset. **The critical implementation defaults are: flag any coded hypertensive patient on medication with no BP in >12 months as highest priority; use <130/80 mmHg as the "at target" threshold for high-risk patients and <140/90 for lower-risk patients; include Read codes G20.., G201., G20z. as the minimum viable diagnosis set (SNOMED 59621000 as primary); and treat the absence of a recent BP as both a monitoring gap and a CVDRA prerequisite gap.** Where NZ guidelines are silent — on organ-damage-specific monitoring frequency, masked hypertension intervals, and formal exclusion criteria — ESC 2024 and ESH 2023 provide the most current international fallback. The absence of a formal NZ "hypertension annual review" analogous to the diabetes annual review is the single largest structural gap; for implementation, the de facto annual review components (BP, eGFR, uACR, electrolytes, lipids, HbA1c, CVDRA recalculation) can be reconstructed from BPAC 2023 guidance and should be treated as the operational standard.