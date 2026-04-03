# Urgency classification for GP inbox triage: a comprehensive evidence review

**No standardised urgency classification framework exists for triaging clinical documents in the GP inbox — despite this being one of the most safety-critical daily tasks in general practice.** This gap spans all major jurisdictions: New Zealand, Australia, the United Kingdom, and the United States. Professional bodies mandate that practices *have* systems for managing incoming results and correspondence, but none prescribe specific urgency levels, labels, or classification criteria. What exists instead is a patchwork of practice-developed protocols, vendor-configurable systems, and informal clinician heuristics — supplemented by domain-specific guidance from pathology and radiology colleges on communicating critical findings. This report synthesises the available evidence across six research domains to inform the design of a purpose-built GP inbox urgency classification framework.

---

## 1. The framework gap: no jurisdiction has standardised GP inbox triage

The most significant finding from this review is the absence of any published, validated urgency classification framework designed specifically for incoming clinical documents in general practice. This contrasts sharply with emergency department triage, where five-level systems (ESI, CTAS, MTS, ATS) are globally standardised with extensive inter-rater reliability data.

**NHS England's GP Forward View Correspondence Management Programme** (2016–2021, £45 million national programme) is the closest approximation to a system-level intervention. It funded training for reception and clerical staff to manage incoming correspondence using practice-developed protocols. Case studies from participating practices — such as Northgate Medical Centre achieving a **78% reduction** in correspondence reaching GPs, and Parkview Surgery saving one hour of clinician time daily — demonstrate the feasibility of structured document workflow. However, NHS England explicitly left protocol development to individual practices, prescribing no urgency taxonomy.

The **RNZCGP Foundation Standard** (Indicator 2.4) requires practices to maintain a "documented policy that describes how laboratory results, imaging reports, investigations and clinical correspondence are tracked and managed," and stipulates that "all incoming test results or other investigations are sighted and actioned by the team member who requested them or by a designated deputy." The **RACGP Standards for General Practices** (5th Edition, Criterion C1.2) similarly requires communication and triage systems. Neither body prescribes specific urgency levels. **BPAC NZ** published "Taking responsibility for test results" (*Best Tests*, August 2014), which discusses protected inbox time and tracking systems but offers no classification scheme. The **BMA** guidance on acting upon electronic test results implies a three-tier approach for laboratory results (critical/life-threatening → abnormal → normal) without formalising it as a triage framework.

In the academic literature, **Apathy et al.** ("Inbox message prioritization and management approaches in primary care," *JAMIA Open*, 2024;7(4):ooae135) studied 11 primary care physicians using Cerner and identified three informal heuristic categories: messages requiring follow-up, quick-action messages, and informational messages. **Rotenstein et al.** ("Primary care physicians' experiences with inbox triage," *JAMIA Open*, 2025;8(5):ooaf105) found that at UW Health (using Epic), inbox prioritisation is "continuous," "multi-factorial," and based on clinical urgency, time constraints, and team member involvement — with no formal classification framework in use. Both studies explicitly call for development of structured triage guidelines.

---

## 2. Three to five levels predominate across existing implementations

Despite the absence of a standard, converging evidence suggests that **three urgency levels** form the dominant mental model in current practice, with some implementations extending to four or five levels when routing and action-type categories are included.

**EHR vendor systems do not impose urgency taxonomies.** Medtech Evolution (used by over 75% of NZ GP practices) categorises inbox items by message type (LAB, RSD, GP2GP, HDOCS) and provides a configurable Task Manager with urgent flagging capability, but leaves classification to each practice. Epic's In Basket organises messages by type-based folders (Results, Rx Requests, Patient Advice Requests) with a "Priority Items" section where team members can route high-priority messages — effectively a two-level system. Cerner offers similar type-based folders with priority flagging. Best Practice Software (AU/NZ) and Genie Solutions provide inbox management functionality but publish no urgency classification documentation. **OneAdvanced's Docman GP Workflow Assistant** (dominant in NHS England) uses AI to extract "urgency" from documents, but the classification scheme is not publicly documented.

The **AAFP** recommends three informal levels for inbox items: **emergent** (immediately interrupt physician/triage nurse), **urgent** (leave note on desk that won't be missed), and **routine** (handle in batches during admin time). NHS practices in the correspondence management programme typically implemented three to five routing levels: Urgent GP Action → Routine GP Review → Delegate to Other Staff → Admin Action → File Only. The UK **National Early Warning Score** (NEWS) uses three clinical risk categories (low/medium/high), and nurse telephone triage in primary care typically operates with four dispositions: emergency, urgent, non-urgent, and self-care (scoping review, PMC12372265, 2025).

| Source | Context | Levels | Labels |
|--------|---------|--------|--------|
| AAFP/AMA guidance | US EHR inbox | 3 | Emergent / Urgent / Routine |
| BMA test results guidance | UK lab/imaging | 3 | Critical / Abnormal / Normal |
| NHS practice protocols | UK correspondence | 3–5 | Urgent GP / Routine GP / Delegate / Admin / File |
| Epic In Basket | US EHR | 2 | Priority Items / Standard |
| Medtech Evolution | NZ PMS | Configurable | Practice-defined |
| Apathy et al. (2024) | US academic | 3 | Follow-up / Quick-action / Informational |
| GP telephone triage | AU/NZ/UK | 4 | Emergency / Urgent / Non-urgent / Self-care |

---

## 3. Clinical rules differ fundamentally by document type

### Laboratory results follow the best-defined urgency hierarchy

The **RCPA/AACB Consensus Statement for Management and Communication of High Risk Laboratory Results** (*Clinical Biochemistry Reviews*, 2015;36(4):97–105, PMC4745612) establishes the clearest framework, distinguishing three tiers. **Critical risk results** are "imminently life-threatening" and require verbal notification within one hour. **Significant risk results** are "not imminently life-threatening but signify significant risk to patient well-being" and require attention within a clinically appropriate timeframe. Routine abnormal results — those outside reference intervals but not at critical thresholds — follow standard electronic delivery.

The **RCPA/AACB harmonised alert list** (Campbell, Lam, and Horvath, "An evidence- and risk-based approach to a harmonized laboratory alert list in Australia and New Zealand," *Clinical Chemistry and Laboratory Medicine*, 2019;57(1):89–94) provides NZ/AU-specific critical thresholds using a six-step evidence and risk assessment process. Representative thresholds include **potassium <2.5 or >6.2 mmol/L**, **sodium <120 or >155 mmol/L**, and **glucose <2.5 mmol/L**. Microbiology critical results include positive blood cultures (any organism), positive CSF cultures, and detection of notifiable organisms. The **NPAAC Tier 3A Requirements** (Australian Government, 2020) mandate that pathology laboratories have procedures for communication of high-risk results, though they deliberately do not prescribe specific threshold values.

Significant variability exists between laboratories: surveys show sodium low-critical thresholds ranging from **110–130 mmol/L** and glucose high-critical thresholds ranging from **15.0–40.0 mmol/L** across institutions (Higgins, "Critical values in laboratory medicine," acutecaretesting.org, 2011). Delta checks — flagging significant changes from previous results — represent an additional urgency signal independent of absolute thresholds, particularly relevant for trending results in chronic disease monitoring.

### Radiology reports use a three-tier alert classification

The most comprehensive framework is the **UK Academy of Medical Royal Colleges / RCR "Alerts and Notification of Imaging Reports: Recommendations"** (October 2022). It defines three alert categories. **CANCER alerts** cover new cancer diagnoses or detected recurrences, triggering digital notification immediately upon report completion. **CRITICAL alerts** cover findings where clinical management is time-critical — including tension pneumothorax, acute aortic dissection, intracranial haemorrhage, bowel perforation, and ectopic pregnancy — requiring verbal communication. **SIGNIFICANT ADDENDA** track amended reports that may alter clinical management. The system mandates a 48-hour escalation interval for unacknowledged alerts.

The **ESR guidelines** (*Insights into Imaging*, 2012;3(1):1–3, PMC3292650) similarly distinguish emergency findings (immediate harm if unactioned), unexpected findings (significant abnormality such as suspected malignancy), and incidental findings (not of urgent significance). **RANZCR Standards of Practice** (v.12.0, 2025) set requirements for report communication in NZ/AU practice but do not publish a standardised alert classification equivalent to the RCR system.

A scoping review by **Corallo et al.** ("Classification and Communication of Critical Findings in Emergency Radiology," *Journal of the American College of Radiology*, 2024) analysed 76 resources including 16 societal guidelines and confirmed that **three-tier stratification based on time sensitivity and severity is the most common approach** across radiology communication frameworks.

### Discharge summaries and specialist letters lack formal urgency criteria

No validated urgency classification for GP inbox triage of discharge summaries was identified. However, the literature identifies clear urgency signals. **Pending test results** affect up to 41% of discharges, with 9–43% requiring management changes, yet only 12–16% are communicated in discharge summaries (Roy et al., *Annals of Internal Medicine*, 2005; Kantor et al., *Journal of General Internal Medicine*, 2014, PMC4351274). **Medication changes** are the element GPs are most dissatisfied with — 65.5% of GPs reported dissatisfaction with documentation of reasons for medication changes (**Weetman et al.**, "Processing of discharge summaries in general practice," *BJGP*, 2018, PMC6058631). That study also found that **46% of discharge summaries requiring action had at least one processing failure**, with harm occurring in 8% of failures.

The **ACSQHC National Guidelines for Presentation of Electronic Discharge Summaries** (revised 2024/2025) specify 17 mandatory components and have moved "Recommendations for primary care provider" toward the top of the document to improve visibility. The **RACGP** explicitly recommends post-discharge GP appointments "within seven days of hospital admissions" (Improving GP Workflows guide, July 2025). New Zealand lacks an equivalent national discharge summary content standard — a notable gap, though **HDC decision 21HDC00557** established that hospitals have a duty to document GP review recommendations, target parameters, and follow-up planning.

For specialist letters and patient messages, no formal urgency frameworks exist. The NLP literature on patient portal message classification has converged on **three to five functional categories** — with Si et al. (*PMLR*, 2020) using three urgency levels (urgent/medium/non-urgent) and Harzand et al. (*NEJM AI*, 2024) using five routing categories (urgent/clinician/prescription/schedule/form).

---

## 4. Four boundary cases expose the limits of simple classification

### Expected abnormals and the alert fatigue problem

No existing GP inbox triage framework explicitly creates a category for "expected abnormal results" — elevated creatinine in known CKD, low haemoglobin in chronic anaemia, or elevated HbA1c in poorly controlled diabetes. The clinical decision support literature addresses this extensively through the lens of alert fatigue. **Singh et al.** (*American Journal of Medicine*, 2010;123(3):238–44, PMC2878665) found that alerts for known diagnoses were significantly less likely to lack follow-up than alerts for new diagnoses (OR 7.35, 95% CI 4.16–12.97), and that 17.4% of alerts arose from redundantly ordered tests. **Ancker et al.** (*BMC Medical Informatics and Decision Making*, 2017;17(1):36) demonstrated that repeated alerts for the same patient were a primary driver of alert fatigue, with clinicians becoming progressively less likely to accept alerts as volume increased.

**Gani et al.** ("Understanding 'Alert Fatigue' in Primary Care," *Journal of Medical Internet Research*, 2025;27(1):e62763, PMC11845892) conducted a systematic review of nine studies (predominantly UK and Australia) finding that GPs raised concerns about "the potential loss of benefits derived from their clinical experience and consideration of individual patient context." The key clinical question for triage frameworks is whether a result represents **a change from the patient's established baseline** rather than whether it falls outside population reference ranges — the concept of patient-specific reference ranges is discussed in informatics literature but has not been codified into inbox protocols.

### Already-actioned results still require formal acknowledgement

Laboratory policies commonly suppress repeat critical value notifications within **48–72 hours** of an initial call. A University of Rochester Medical Center policy states that "if a similarly abnormal value was reported within the past two days, the repeat critical value will not be treated as an emergency." However, **documentation obligations persist** regardless of prior action. The Joint Commission (NPSG.02.03.01), CAP, and RCPA all require documented acknowledgement including time, date, result, reporter identity, and receiver identity. For the GP inbox, the principle is that viewing a result in the inbox creates a record that must be formally closed — documenting that the result was received, had already been actioned (by whom, when, what action), and whether additional primary care follow-up is needed.

### Normal results that still demand clinical action

No framework explicitly creates a "normal but actionable" triage category. Examples include normal troponin in a patient with ongoing chest pain workup, normal PSA with persistent urinary symptoms warranting further investigation, or a normal screening test where pre-test probability still warrants further assessment. The **AHRQ PSNet** addresses this from a patient safety perspective under the principle that "no news may not be good news" — the assumption that patients who don't hear results can assume they are normal creates safety risks when normal results require action. **Cole's Medical Practice in New Zealand** (Chapter 14) stipulates that if practice policy is not to notify normal results, patients must be informed and consent obtained. The triage system must consider the **clinical question that prompted the test**, not just the result itself.

### Incidental findings impose uncertain responsibility on GPs

The **Fleischner Society 2017 Guidelines** (*Radiology*, 2017;284(1):228–243) provide the most widely used framework for incidental pulmonary nodules, raising the minimum threshold for follow-up from 4mm to **6mm** to reduce unnecessary surveillance. The **ACR Incidental Findings Committee** has published organ-specific management white papers covering renal masses, adrenal incidentalomas, liver lesions, thyroid nodules, and adnexal masses. **O'Sullivan et al.** (*British Journal of General Practice*, 2016;66(648):346–347, PMC4917024) found that GPs are often expected to manage incidental findings discovered in hospital or research settings — describing this as "an imposition" — with 20–40% of CT examinations containing at least one incidental finding. Only **17% of incidental findings** receive appropriate follow-up in some settings (RSNA News, March 2025). Multiple **NZ HDC decisions** (including 15HDC01204 and 15HDC01387) have found against GPs for failure to follow up incidental findings, particularly where multiple clinicians each assumed another was responsible.

---

## 5. New Zealand's medico-legal framework creates an inbox accountability trap

### Te Whatu Ora's four principles define — but don't resolve — responsibility

The foundational NZ document is **"Transfer of Care and Test Results Responsibility"** (Health New Zealand / Te Whatu Ora, Ministry of Health, and Te Aka Whai Ora, 19 March 2024, signed by Dr Joe Bourne CMO, Dr Rawiri McKree Jansen CMO, and Dr Richard Sullivan CCO). Its four principles establish that:

- **Principle 1:** The ordering clinician retains responsibility for results regardless of subsequent transfer of care, unless explicitly agreed and documented otherwise. Where a clinician is copied into results, "the recipient also has responsibility to ensure results of significant clinical importance have been acted upon."
- **Principle 2:** Copying results is appropriate but "clear separate communication is required if the recipient is expected to act," with documented handover involving closed-loop communication.
- **Principle 3:** "Any clinician copied into a result which is significantly abnormal needs to ensure appropriate action has been taken" — and if you view a report, "this action establishes a clinical relationship between yourself and the person."
- **Principle 4:** Requirements for regular monitoring must be agreed between referring and receiving clinicians.

Critically, the guidance states that **"copying of results is not a transfer of care"** and results should not be routinely copied. Yet routine copying remains widespread practice.

### The NZMJ 2025 survey confirms a knowledge gap and unsustainable burden

The **NZMJ** published "Transfer of care and inbox management in primary care: a survey on medico-legal responsibility awareness and administrative burden in Aotearoa New Zealand" (Vol 138, No 1622, 19 September 2025, DOI: 10.26635/6965.6952). The survey confirmed a **significant medico-legal knowledge gap** in the primary care workforce regarding test result responsibility. One GP reported spending "10–15 minutes a day just dealing with copied inpatient radiology reports from the hospital; that's at least 60 minutes a week and 48 hours a year." Most doctors preferred *not* to receive results they did not order, as this creates confusion about identifying the responsible clinician. **Four out of five** respondents supported closed-loop communication before responsibility transfer. GP respondents reported stronger retirement intention than the 2024 RNZCGP workforce survey — **30% versus 21%** within three years — driven partly by administrative burden.

### HDC decisions have built a case-law standard for inbox management

**Cole's Medical Practice in New Zealand** (MCNZ, Chapter 14) establishes eight principles for clinical investigation management, anchored by: "If you order investigations, it is your responsibility to review, interpret and act on the results." The **RNZCGP Policy Brief No. 6** (April 2016) synthesises HDC case law, noting the principle that "the primary responsibility for following up abnormal results rests with the clinician who ordered the tests."

Several HDC decisions have direct implications for inbox triage system design:

- **21HDC00619** (August 2023): A GP filed an amended discharge summary without checking it, assuming it was a duplicate. The third version contained a CT finding of a **17cm neck mass** and ENT referral recommendation. Cancer diagnosis was delayed by over 2.5 years. Deputy Commissioner Carolyn Cooper held that "the onus was on the GP to check the summaries for new information before filing them away" — establishing that **every inbox item requires individual review**, even apparent duplicates.
- **18HDC01066** (2020): A GP failed to inform a patient of a histology report showing incomplete BCC excision. The GP noted that the results management system required "only one click to file results, making it too easy to inadvertently file a result with a misstep of the mouse." The decision found the results management policy "not sufficiently robust."
- **14HDC00894** (2016): A significantly abnormal haemoglobin result (82 g/L) went unactioned for two months. The patient had a malignant stomach tumour and died later that year. Both GPs involved breached the Code, and both practices were criticised for lacking written test result management policies.
- **99HDC11494**: The landmark case — a GP failed to follow up missing mammography results for a patient with suspected malignancy. The HDC stated that "any test ordered where the doctor has reason to suspect a cancer diagnosis requires a proactive follow-up by the referring doctor." This decision prompted the RNZCGP to develop its "Managing Patient Test Results — Minimising Error" guidance.

New Zealand's **ACC no-fault compensation scheme** means patients cannot sue for medical negligence in tort, making HDC decisions the primary medico-legal accountability mechanism. **Dovey and Wallis** (*PMID 21228439*, 2011) analysed 6,007 primary care treatment injury claims and found that while delay in diagnosis caused only **2% of all injuries**, it accounted for a disproportionate **16% of serious and sentinel injuries and 50% of deaths**.

---

## 6. Three to four levels optimise reliability for document triage

### The ED triage evidence supports five levels — but with caveats

The landmark comparison by **Travers et al.** ("Five-level triage system more effective than three-level in tertiary emergency department," *Journal of Emergency Nursing*, 2002) found that the five-level ESI achieved **weighted kappa of 0.68** versus 0.53 for a three-level system at the same site, with under-triage rates dropping from 28% to 12%. Modern five-level ED systems with structured algorithmic support achieve substantially higher reliability: ESI v.3 kappa of **0.89**, ESI v.4 ranging from 0.72 to 0.96 across international validation studies. However, historical three-level systems without structured decision support produced kappa values of only **0.35–0.46** — suggesting that the improvement comes primarily from the algorithmic structure, not merely the number of levels.

### Cognitive science bounds the practical range

**Miller's Law** (1956) sets an upper bound of approximately 7±2 categories for absolute judgment tasks. **Cowan's revision** (2001) places the practical working memory limit at approximately **four chunks** for adults under cognitive load. For rapid triage decisions under time pressure — which characterises GP inbox processing — the literature suggests **3–5 categories** as the effective range. Fewer than three provides insufficient discrimination (the three-level triage problem of concentrating most items in the middle category). More than five exceeds practical cognitive capacity without algorithmic support and produces diminishing returns for discrimination.

### The NLP literature converges on three urgency categories

The most relevant AI/NLP work for GP inbox triage uses classification schemes ranging from binary to five levels. **Si et al.** ("Students Need More Attention: BERT-based Attention Model for Small Data," *PMLR*, 2020) used **three categories** (urgent/medium/non-urgent) for patient portal message classification. **Harzand et al.** (*NEJM AI*, 2024) used five functional categories but combined urgency with routing intent. **Gatto et al.** ("Medical Triage as Pairwise Ranking," arXiv 2601.13178, January 2026) introduced the **PMR-Bench** dataset of 1,569 patient messages and argued that "a binary higher- versus lower-urgency comparison involves simpler comparison semantics than an ordinal set of three or more urgency categories" — proposing pairwise ranking as an alternative to categorical classification entirely.

One study found that five-class ESI prediction achieved AUC of **0.59–0.78** per class, improving to **0.72–0.84** when collapsed to three classes — suggesting that ML models perform better with fewer categories. No study was found that directly compares inter-rater reliability for different numbers of urgency levels in **clinical document** triage specifically. All available kappa data derives from ED patient triage or chart review contexts.

### A statistical nuance on kappa and category count

An important methodological caveat: as the number of categories increases, chance agreement decreases, which can paradoxically *inflate* kappa values relative to actual agreement rates. **Weighted kappa** is recommended for ordinal urgency scales, as it gives partial credit for near-miss classifications. The higher kappa values observed in five-level versus three-level ED systems therefore reflect both genuinely better discrimination *and* a statistical artefact of the kappa formula. The **Travers finding should be interpreted as evidence that structured algorithmic decision support improves reliability**, rather than as evidence that five levels is inherently superior to three or four for all triage contexts.

---

## Conclusion: designing a fit-for-purpose GP inbox classification

This review identifies a clear **market and evidence gap** — the most safety-critical daily classification task in general practice has no standardised framework, no validated inter-rater reliability data, and no published annotation studies specific to clinical document triage. The evidence supports several design principles for filling this gap.

**Three to four urgency levels** represent the optimal range for GP inbox document triage, balancing discrimination against cognitive load and inter-rater agreement. A three-level system (urgent/routine/information-only) aligns with the dominant clinician mental model documented by Apathy et al. and the most common NLP classification scheme. A fourth level — separating time-critical urgent items from semi-urgent items requiring action within days — may improve discrimination for the specific demands of clinical documents without exceeding practical agreement limits.

**Classification criteria must be document-type-specific.** Laboratory results benefit from the most mature urgency hierarchy (RCPA/AACB critical risk → significant risk → abnormal → normal). Radiology reports follow the RCR three-tier alert model (critical → cancer/urgent → incidental). Discharge summaries and specialist letters lack equivalent frameworks and require urgency signals derived from content elements — pending results, new serious diagnoses, medication changes, and time-bound action requests.

**Boundary cases require explicit handling rules.** Expected abnormals should be triaged based on deviation from patient-specific baseline rather than population reference ranges. Already-actioned results must still be formally acknowledged with documentation. Normal results triggered by clinical questions where action remains warranted cannot be auto-filed. Incidental findings require organ-specific management pathways (Fleischner, ACR) with clear responsibility assignment.

**The NZ medico-legal environment demands conservative design.** Te Whatu Ora's 2024 guidance and successive HDC decisions establish that viewing a result creates a clinical relationship, every inbox item requires individual review, copying is not transfer of care, and GPs retain a secondary duty to ensure significantly abnormal copied results have been actioned. A triage framework must be designed to support — not circumvent — these obligations, providing structured decision support that makes safe classification faster while maintaining the documentation trail that HDC scrutiny demands.

**Structured algorithmic decision support matters more than category count.** The strongest signal from the ED triage literature is that the improvement from three-level to five-level systems is primarily attributable to embedded decision algorithms, not the number of levels per se. Any GP inbox triage framework should therefore incorporate explicit decision rules — including document-type-specific criteria, critical value thresholds, and boundary case protocols — rather than relying on unstructured clinical judgment to assign urgency labels.