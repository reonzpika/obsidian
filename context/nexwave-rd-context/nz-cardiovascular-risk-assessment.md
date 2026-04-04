# NZ cardiovascular risk assessment: the definitive implementation guide

**The PREDICT-derived NZ Primary Prevention Equations are the sole officially endorsed CVD risk calculator for New Zealand general practice.** Published in *The Lancet* (Pylypchuk et al., 2018) and codified in the HISO 10071:2025 data standard under a CC-BY 4.0 licence, these equations replaced the older Framingham-based risk charts following the 2018 Ministry of Health Consensus Statement. They output a **5-year CVD risk percentage** using up to **15 input variables** (not 8), classified against thresholds of **<5% (low), 5–15% (intermediate), and ≥15% (high)**. For a clinical AI implementation, the equations should be implemented deterministically in code — a reference R implementation exists on GitHub (VIEW2020/PredictRiskScores, GPL-3.0), and Health NZ operates a free national CVDRA REST API.

---

## 1. Two tools, one lineage: risk charts vs PREDICT equations

The two tools referenced in NZ primary care share a direct lineage but differ significantly in methodology and capability.

**The old NZ CVD Risk Charts** (used pre-2018) were adapted Framingham equations — derived from the US Framingham Heart Study cohort of the 1960s–70s, with crude adjustments for NZ populations (a flat 5% upward adjustment for Māori and Pacific peoples). They used **6 core variables**: age, sex, smoking, blood pressure, TC:HDL ratio, and diabetes status. Ethnicity was handled as a post-hoc adjustment rather than an intrinsic predictor. Risk thresholds were <10% (low), 10–20% (intermediate), and ≥20% (high). These charts significantly overestimated risk — by approximately **40% in men and 60% in women** — because they were calibrated to a different population and era.

**The NZ Primary Prevention Equations** (PREDICT-derived) were developed by the VIEW/VAREANZ research group at the University of Auckland from the PREDICT cohort — an open primary care cohort of **400,728 NZ patients aged 30–74**, enrolled 2002–2015, with 1.69 million person-years of follow-up and 15,386 CVD events. These equations are sex-specific Cox proportional hazards models incorporating **15 predictor variables** including NZ-specific factors like prioritised ethnicity (5 categories), NZ Index of Deprivation (NZDep) quintile, atrial fibrillation, family history, and current preventive pharmacotherapy. A separate, more detailed equation exists for patients with type 2 diabetes, adding HbA1c, eGFR, albuminuria, diabetes duration, and hypoglycaemic medications.

The 2018 Ministry of Health Consensus Statement (*Cardiovascular Disease Risk Assessment and Management for Primary Care*, ISBN 978-1-98-853933-1) formally endorsed the PREDICT equations as the replacement, stating: *"It is no longer possible to use paper charts to estimate CVD risk due to the increased number of predictors in the new equations."*

---

## 2. BPAC NZ recommends PREDICT with a pragmatic transition

BPAC NZ's May 2018 article (*"What's new in cardiovascular disease risk assessment and management for primary care clinicians"*, bpac.org.nz/2018/cvd.aspx) established the official position: the NZ Primary Prevention equations are the recommended foundation. At publication in 2018, BPAC acknowledged these equations were not yet available in practice software and advised clinicians to *"classify patients as low, intermediate or high risk using existing Framingham-based equations, and follow the appropriate management recommendations for the same risk category in the 2018 CVD consensus statement."*

By 2021 (BPAC statins article, bpac.org.nz/2021/statins.aspx), BPAC confirmed the transition was complete: *"Risk calculators based on New Zealand PREDICT equations are now incorporated into decision support software."* BPAC directs clinicians to the bestpractice Decision Support module or an online calculator at chd.bestsciencemedicine.com.

**The recommendation does not differ between initial screening and ongoing management** — the same PREDICT equations are used for both. However, BPAC and the Consensus Statement explicitly state that **patients with established CVD or CVD risk equivalents should NOT have risk calculated** — they are automatically classified as high risk (≥15%). CVD risk equivalents include prior cardiovascular events, familial hypercholesterolaemia, congestive heart failure, diabetes with eGFR <45 mL/min/1.73m², and stage 4 CKD (eGFR <30).

**Implementation recommendation:** Commit to the PREDICT NZ Primary Prevention Equations (v.2019 with BMI). The Framingham pathway is legacy only.

---

## 3. Medtech Evolution relies on third-party integrations, not a native calculator

**Medtech Evolution has no built-in CVD risk calculator.** Medtech Global's own documentation contains zero references to cardiovascular risk assessment. Instead, CVD risk is delivered through three third-party decision support tools that integrate with Medtech Evolution:

**Enigma Solutions' PREDICT-CVD** is the primary integration, operational since 2005 (initially in Medtech32, subsequently Medtech Evolution). The Health Research Council confirms: *"PREDICT has been integrated into MedTech, the leading New Zealand medical records system."* Enigma's "Your Heart Engine" (YHE) implements the PREDICT equations (current production code: YHE-2019-BMI-DM). It auto-populates patient data from the EHR, sends it to a central server, and returns the calculated 5-year risk score with management recommendations, writing results back to the patient record.

**bestpractice Decision Support** (by BPAC Inc) offers a CVD Management module that integrates with Medtech Evolution. Its public documentation historically references Framingham equations, though it now supports the NZ PREDICT equations.

**Mōhio CVD** (National Hauora Coalition) is a third option, ready for integration with Medtech Evolution, MyPractice, and Medtech32.

Critically, **Health New Zealand now operates a national CVDRA REST API** (free, Azure-hosted) that implements the HISO 10071:2025 equations. Any PMS — or any clinical AI system — can integrate with this API directly. Technical documentation is available at api.cvdriskassessment.min.health.nz/open-api/.

**Implementation recommendation:** For a clinical AI system, either implement the equations locally using the published HISO coefficients or call the Health NZ CVDRA API. Do not depend on Medtech's third-party integrations.

---

## 4. Exact input variables: 15 for general population, not 8

The 8-variable model described in the question (age, sex, ethnicity, BP, total cholesterol, HDL cholesterol, smoking, diabetes) is **insufficient for the NZ Primary Prevention Equations**. The full variable set is substantially larger.

### General population equation (non-diabetes) — 15 mandatory variables:

| # | Variable | Type | Details |
|---|----------|------|---------|
| 1 | **Age** | Continuous | Whole years (valid range 30–74) |
| 2 | **Sex** | Binary | Male/Female (selects sex-specific equation) |
| 3 | **Ethnicity** | Categorical, 5 levels | Māori, Pacific, Indian/South Asian, Chinese/Other Asian, European/Other |
| 4 | **NZDep quintile** | Ordinal, 1–5 | NZ Index of Socioeconomic Deprivation |
| 5 | **Smoking status** | 3 categories | Never / Ex-smoker / Current smoker |
| 6 | **Family history of premature CVD** | Binary | First-degree relative hospitalised/died from MI or stroke before age 50 |
| 7 | **Atrial fibrillation** | Binary | ECG-confirmed AF (yes/no) |
| 8 | **Diabetes** | Binary | Type 1, Type 2, or type unknown (yes/no) |
| 9 | **Systolic blood pressure** | Continuous (mmHg) | Mean of two seated measures |
| 10 | **TC:HDL-C ratio** | Continuous | Non-fasting total cholesterol ÷ HDL cholesterol |
| 11 | **BMI** | Categorical, 7 levels | <18.5 / 18.5–24.9 / 25–29.9 / 30–34.9 / 35–39.9 / ≥40 / Unknown |
| 12 | **BP-lowering medication** | Binary | Dispensed in prior 6 months |
| 13 | **Lipid-lowering medication** | Binary | Dispensed in prior 6 months |
| 14 | **Antithrombotic medication** | Binary | Antiplatelet or anticoagulant dispensed in prior 6 months |
| 15 | **Interaction terms** (3) | Derived | Age×Diabetes, Age×SBP, BP-med×SBP |

The v.2019 equation adds **BMI** compared to the original Lancet 2018 publication, which had only 14 variables. The HISO 10071:2025 standard specifies the v.2019 (with BMI) as the current production equation.

### Diabetes-specific equation — additional variables:

All of the above, plus **HbA1c** (mmol/mol), **eGFR** (CKD-EPI, mL/min/1.73m²), **urinary albumin:creatinine ratio** (mg/mmol), **diabetes duration** (years), **oral hypoglycaemic medication** (binary), and **insulin** (binary). BMI becomes continuous rather than categorical.

The three variables missing from the user's proposed 8-variable model that are **critical for implementation** are: **NZDep quintile**, **family history of premature CVD**, and **current preventive pharmacotherapy** (three medication binary flags). Without these, the equation cannot be computed. NZDep can be derived from the patient's residential address using the NZ Census meshblock-level deprivation data.

---

## 5. Screening initiation thresholds by age, sex, and ethnicity

The 2018 Consensus Statement (Table 4) and BPAC (Table 2) specify identical thresholds. These were updated from the 2013 guidelines, notably lowering the age for Māori, Pacific, and South Asian peoples by 5 years.

| Population subgroup | Men | Women |
|---|---|---|
| **European/Other without known risk factors** | **45 years** | **55 years** |
| **Māori** | **30 years** | **40 years** |
| **Pacific peoples** | **30 years** | **40 years** |
| **South Asian peoples*** | **30 years** | **40 years** |
| **Personal or family risk factors present†** | **35 years** | **45 years** |
| **Diabetes (type 1 or 2)** | **From diagnosis** | **From diagnosis** |
| **Severe mental illness‡** | **25 years** | **25 years** |

*South Asian is explicitly defined as: Indian (including Fijian Indian), Sri Lankan, Afghani, Bangladeshi, Nepalese, Pakistani, Tibetan.

†Personal risk factors triggering earlier screening include: current smoking, AF (new in 2018), BMI ≥30 or waist ≥102 cm (men)/≥88 cm (women), gestational diabetes, HbA1c 41–49 mmol/mol, eGFR <60 on ≥2 occasions. Family risk factors include: first-degree relative hospitalised/died from MI or stroke before age 50, diabetes in first-degree relative, familial hypercholesterolaemia (new in 2018).

‡Severe mental illness includes schizophrenia, major depressive disorder, bipolar disorder, schizoaffective disorder. This category was **new in 2018**.

The PREDICT equations are validated for ages **30–74**. For patients screened before age 30 (e.g., severe mental illness from age 25, or diabetes diagnosed young), the Consensus Statement notes risk estimates are approximations but "still clinically useful."

---

## 6. Output format: 5-year risk with three-tier thresholds

NZ uniquely uses a **5-year risk horizon**, unlike most international guidelines that use 10-year horizons. The Consensus Statement provides four reasons: most RCTs use ≤5 years of treatment data; median PREDICT follow-up was ~5 years; risk and management change materially over a decade; and NZ practitioners are accustomed to this timeframe.

The predicted outcome is the combined probability of hospitalisation or death from **ischaemic heart disease** (including unstable angina), **stroke**, **TIA**, **heart failure**, **peripheral vascular disease**, and **other ischaemic CVD-related deaths**.

### Current risk category thresholds (NZ Primary Prevention Equations):

| Category | 5-year CVD risk | Clinical action |
|---|---|---|
| **Low** | **<5%** | CVD medicines generally not recommended; lifestyle advice |
| **Intermediate** | **5–15%** | Discuss benefits/risks of BP- and lipid-lowering medicines; consider treatment, particularly at higher end |
| **High** | **≥15%** | BP- and lipid-lowering treatment strongly recommended; aspirin considered if <70 years |

**Population distribution:** approximately **74%** of assessed patients fall into low risk, **24%** into intermediate, and **2%** into high risk.

Two important override rules exist regardless of calculated risk: persistent office BP **≥160/100 mmHg** triggers drug treatment, and TC:HDL-C ratio **≥8** triggers lipid treatment.

The formula is: **5-year CVD risk (%) = (1 − S₀^exp(Σ(β × (x − mean)))) × 100**, where S₀ is the sex-specific baseline survival at 5 years (e.g., **0.9712501** for men in the general equation), β values are the published Cox regression coefficients, and x values are centred by subtracting their published means.

---

## 7. Review intervals are risk-stratified across five tiers

The Consensus Statement and BPAC specify granular recall intervals that subdivide the three risk categories:

### Patients NOT on pharmacological management:

| 5-year CVD risk | Repeat assessment interval |
|---|---|
| **<3%** | **10 years** |
| **3–5%** | **5 years** |
| **5–9%** | **5 years** |
| **10–14%** | **2 years** |
| **≥15%** | **Annually** |

### Patients ON pharmacological management:

All patients on CVD pharmacotherapy (whether high or intermediate risk) require **annual review**, including repeat risk assessment.

### Special populations:

Patients with **severe mental illness** require CVD risk assessment every **2 years**, or **annually** if risk ≥15%. Patients with **diabetes** should have CVD risk assessed as part of their **annual diabetes review**.

For a care gap detection system, the key logic is: last CVDRA date + appropriate interval based on last calculated risk level = due date for next assessment. If no CVDRA has ever been performed and the patient meets age/ethnicity/risk factor eligibility criteria, flag as overdue.

---

## 8. Atrial fibrillation is a direct equation input, not a multiplier

**AF is a binary (0/1) predictor variable built directly into the Cox proportional hazards model** — it is not a separate risk multiplier or post-hoc adjustment. This is a major advantage over the older Framingham equations, which did not include AF at all.

The HISO 10071:2025 standard specifies AF as mandatory, defined as ECG-confirmed atrial fibrillation (paroxysmal, persistent, or permanent). The published coefficients reveal AF is among the strongest predictors in the model:

- **Women, general population:** β = **0.9293** (hazard ratio ≈ 2.53)
- **Men, general population:** β = **0.6250** (hazard ratio ≈ 1.87)
- **Women with diabetes:** β = **0.7865** (hazard ratio ≈ 2.20)
- **Men with diabetes:** β = **0.5285** (hazard ratio ≈ 1.70)

For comparison, current smoking has a coefficient of 0.6829 in women and 0.5318 in men — making AF approximately equal to or stronger than smoking as a CVD predictor.

AF also plays a **second role as a screening trigger**: it was added in 2018 as a personal risk factor that initiates CVDRA at **age 35 for men and 45 for women** (rather than the default 45/55 for the general European/Other population).

Note that AF-related stroke risk for anticoagulation decisions uses the separate **CHA₂DS₂-VASc** scoring system — this is an independent clinical pathway from CVD risk assessment.

---

## Conclusion: implementation recommendations for a clinical AI system

The evidence converges on a clear implementation path. **Use the PREDICT NZ Primary Prevention Equations v.2019 (with BMI)** as specified in HISO 10071:2025. The equations and all coefficients are published under CC-BY 4.0 and can be implemented in any language — a reference R implementation exists at github.com/VIEW2020/PredictRiskScores (GPL-3.0). Alternatively, call the free Health NZ CVDRA REST API for production use.

Three critical implementation facts often missed: the equations require **15 variables**, not 8 — NZDep quintile, family history, and three medication flags are mandatory inputs that many systems overlook. Smoking must be encoded as a **three-level** variable (never/ex/current), not binary. And separate, more complex equations must be routed to for patients with **type 2 diabetes**, requiring HbA1c, eGFR, ACR, and diabetes duration.

For care gap detection, the system must implement the screening eligibility matrix (age × sex × ethnicity × risk factors), the risk-stratified recall intervals (10 years down to annually), and the automatic high-risk classification for patients with established CVD or risk equivalents — who should never have risk calculated but should always be flagged for annual review. The "PREDICT" trademark belongs to Enigma Solutions Ltd, so any external-facing tool should use a different name for the calculator while citing the underlying equations.