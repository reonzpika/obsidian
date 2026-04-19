# Deep Research Brief: Clinical Dashboard for NZ General Practice

## 1. Executive summary

**All three domains are technically feasible with current LLM capabilities and the Medtech ALEX FHIR API, but none has a direct NZ precedent — the builder would be first-to-market in every category.** The highest-leverage design opportunity is action item capture, where no EHR system globally tracks "soft" follow-up actions embedded in clinical free text, and the patient safety evidence is strongest. NZ billing optimisation is the easiest to implement (smallest NLP surface area, highest signal-to-noise ratio in structured data) and would generate immediate, measurable ROI. Inbox triage carries the largest existing evidence base on the problem but faces the steepest NLP generalisation challenge, particularly for specialist correspondence.

### Key findings

- **Follow-up failure rates of 6.8–62% for lab results** (Callen et al., 2012) and documented safety-netting advice in only 46.3% of problems discussed (Edwards et al., 2019) make action tracking the strongest patient safety case. No major EHR — Epic, Oracle Health, or Athena — systematically captures or tracks "soft" follow-up actions recorded in clinical free text.
- **ACC dual-billing (consultation + procedure code in a single visit) is explicitly supported** but commonly missed. No published NZ data quantifies the revenue gap, but ACC's own fact sheet (ACC1520, June 2024) singles out this as a billing education priority. The NLP task is narrow: detect procedure keywords in free text and cross-reference patient demographics for rate tier.
- **GPs process ~77 inbox notifications/day, spending 85 minutes daily** (Murphy et al., 2016; Arndt et al., 2017). RadBERT and ClinicalBERT++ achieve **F1 > 0.95 on internal test sets** for critical finding detection in radiology reports, but external generalisation drops significantly (recall 0.54 on Mayo Clinic data for ClinicalBERT++). Specialist letter triage is a near-complete research gap.
- **Medtech ALEX provides a production-ready FHIR API** (v2.9, September 2025) across 1,000+ NZ primary care sites, supporting Patient, Condition, Observation, DocumentReference, and Consultation resources. Medtech AI (launched 2025) already handles ambient clinical documentation via the same integration layer.
- **LLM API costs are now trivial**: processing 10,000 consultation notes/day through a mid-tier model costs ~$600 NZD/month. Zero-shot and few-shot prompting approaches achieve clinical extraction accuracy of 78–90% without fine-tuning (Agrawal et al., 2022; Reategui-Rivera et al., 2025).
- **Regulatory gap is real but navigable**: NZ currently has no pre-market SaMD framework, and the Medical Products Bill remains in development. The Waitematā DHB AI Governance Framework (published in *npj Digital Medicine*, 2023) and Health NZ's internal AI policy both require clinician review of all AI outputs — design for human-in-the-loop from day one.

### Feasibility and risk matrix

| Domain | Technical feasibility | Data availability | Revenue case | Safety case | Regulatory risk |
|--------|----------------------|-------------------|--------------|-------------|-----------------|
| Action item capture | High (LLM extraction) | High (ALEX API) | Indirect (retention, safety) | **Strongest** | Low (decision support, not autonomous) |
| Billing completeness | **Highest** (narrow NLP task) | High (structured + free text) | **Strongest** (direct $ recovery) | Moderate | Low |
| Inbox triage | Moderate (radiology strong, letters weak) | High (lab/radiology via ALEX) | Moderate (time savings) | High | Moderate (prioritisation influences action) |

### Highest-leverage design implications

Build billing completeness first — it is the simplest NLP problem, generates immediate measurable value, and creates the practice-level trust needed for adoption of the two higher-complexity modules. Action item capture should follow, targeting the gap no incumbent fills. Inbox triage is the hardest to differentiate from emerging Medtech AI features and carries the highest NLP generalisation risk.

---

## 2. Domain deep-dives

---

### AREA 1: Clinical action item capture and tracking

#### Evidence base

**The safety net is the most studied and least systematised concept in primary care.** Roger Neighbour defined safety netting in *The Inner Consultation* (1987) as three questions: "If I'm right, what do I expect to happen?", "How will I know if I'm wrong?", and "What would I do then?" This was formalised by Almond, Mant, and Thompson (*BJGP*, 2009) through a Delphi consensus study, and comprehensively reviewed by Jones et al. (*BJGP*, 2019) across 47 studies — yet no consensus exists on when safety netting should be used or what it must contain.

The failure rates are stark. Callen et al.'s systematic review (*JGIM*, 2012) of 19 studies found **laboratory follow-up failure rates of 6.8% to 62%** and radiology follow-up failure at 1.0% to 35.7%. Bowie et al. (*BMJ Open*, 2015) found system hazards in **83% of 647 UK GP practices**, with half of 50 clinical negligence claims involving failure to notify patients of abnormal results. Singh et al. (*BMJ Quality & Safety*, 2014) estimated that **1 in 20 US adult outpatients experiences a diagnostic error annually**, more than half with potential for harm.

Six failure modes dominate in the literature:

- **Laboratory results** — widest documented failure range and highest volume
- **Radiology/imaging** — lower volume but higher consequence per missed finding
- **Referral responses** — fragmented tracking across primary-secondary interface
- **Safety-netting advice to patients** — recorded for only 46.3% of problems discussed (Edwards et al., *BJGP*, 2019) and "seldom documented in the medical record" (Colliers et al., 2022)
- **Tests pending at discharge** — high-risk during care transitions
- **Incidental findings** — no owner, no tracking system, no natural follow-up prompt

Nicholson et al. (*BJGP*, 2018) conducted qualitative interviews with 25 UK GPs and found they use **"bespoke personal strategies, often developed from past mistakes, without knowledge of their colleagues' practice."** GPs selectively safety-net patients perceived to be at higher risk, while patients with "low-risk-but-not-no-risk symptoms" receive less robust or absent follow-up. Singh et al. (2016) documented extensive workarounds in VA primary care: personal paper lists, electronic reminders, diary entries — creating "parallel hybrid paper-electronic systems with numerous non-standard workflows." Belgian OOH video observations confirmed safety-netting advice was "limited, unspecific, and not documented in the medical record."

**The fundamental problem is that no EHR system anywhere captures or tracks "soft" follow-up actions.** Epic, Oracle Health, and Athena all track *ordered* tests (structured order → result → notification). But "review in 2 weeks if no better," "repeat bloods in 6 weeks," or "if rash doesn't settle, refer to dermatology" — the actions most prone to being lost — exist only in free-text narrative. This is the gap the dashboard must fill.

#### NLP approaches and benchmarks

LLM-based clinical information extraction has matured rapidly. Agrawal, Hegselmann, Lang, Kim, and Sontag (EMNLP, 2022) demonstrated that InstructGPT performs well at zero- and few-shot clinical extraction, achieving **86% accuracy at zero-shot clinical acronym disambiguation**, rising to 90% with additional methods. Fine-tuned Llama-3.1 8B achieved **90.0% ± 1.7 average exact match accuracy** across four clinical datasets with LoRA fine-tuning, requiring ≤100 training reports and a single desktop GPU (*Scientific Reports*, 2025). GPT-4o achieved 78% precision in general sign/symptom extraction and 87% for organ-specific tasks (Reategui-Rivera et al., 2025). The CLINES agent (2025 medRxiv preprint) achieved entity extraction F1 of 0.69–0.87 and assertion status F1 of 0.84–0.93 on MIMIC-III and 4CE datasets.

Prompt strategies that work include few-shot prompting with 5 clinical examples (Agrawal et al.), chain-of-thought reasoning, heuristic prompts tailored to task-specific patterns (Gundabathula & Deepa, *JMIR Medical Informatics*, 2024), and structured output prompting that forces the model to produce lists and source references (Lang et al., MIT CSAIL, 2022). An MIT study (2024) specifically tested GPT-4 extraction of patient "to-do list" action items from clinical notes, with participants showing improved understanding of follow-up requirements.

**What fails in clinical note NLP** deserves specific attention for dashboard design. Clinical abbreviations remain challenging — "pt will dc vanco due to n/v" requires contextual disambiguation. Implicit actions ("repeat bloods in 6 weeks" buried in narrative) and conditional instructions ("if no improvement, consider referral") are the hardest to extract reliably. Negation handling — distinguishing "no need for follow-up" from "follow-up needed" — was identified as "still an open problem" in the 2022 n2c2 shared task. Copy-paste artefacts in notes introduce noise, though LLM preprocessing has shown improvements in downstream F1 (MDPI *Information*, 2025).

**Critical gap: no published benchmark dataset specifically targets clinical action item extraction from primary care consultation notes.** The closest are n2c2 2022 Track 3 (assessment and plan reasoning) and MIT's to-do-list augmentation work. The n2c2 2022 Track 1 (contextualised medication event extraction) found NER performance was high but **event and context classification performance was "much lower"** — highlighting that understanding what actions are embedded in clinical text remains harder than entity recognition. Building an internal gold-standard annotation set of 100–300 NZ GP notes will be necessary for validation.

#### High-reliability industry parallels

James Reason's Swiss Cheese Model (*Human Error*, 1990; *BMJ*, 2000) provides the theoretical foundation: relying on individual vigilance is inherently unreliable; effective safety requires designed systems. Aviation's **closed-loop communication** (read-back/hear-back) maps directly — every clinical action item should be captured, tracked, and verified as complete. Aviation checklists evolved over 70+ years around principles of brevity, logical categorisation, and regular training (Thomassen et al., *Scandinavian Journal of Trauma, Resuscitation and Emergency Medicine*, 2011). The WHO Surgical Safety Checklist reduced surgical mortality from 1.5% to 0.8% (Haynes et al., *NEJM*, 2009) but required "complex, cultural and organisational change efforts, not just the checklist itself" (Clay-Williams & Colligan, *BMJ Quality & Safety*, 2015). Nuclear power's **Corrective Action Programmes** — where all identified issues enter a formal tracking system with deadlines and verification of closure — are the closest operational analogy to a GP pending actions dashboard.

Key adaptation requirement: aviation and nuclear operate in real-time with co-located crews; GP follow-up spans days to months with distributed responsibility. The dashboard must handle **temporal distribution** of open loops across varying timeframes and multiple responsible clinicians.

#### Design implications for the dashboard

**The product should capture three categories of action item:**

- **Structured-trackable**: ordered tests and referrals (already have a digital trail; the task is surfacing and closing the loop)
- **Semi-structured**: coded recalls and diary entries (exist in PMS but may not be systematically tracked)
- **Unstructured-extractable**: soft follow-up actions in free-text notes (the novel NLP task)

**Design the loop as: Capture → Assign → Track → Escalate → Close.** Each action item should have an owner (defaulting to the consulting clinician), a due date (extracted or inferred from "in 2 weeks", "6 weeks", "3 months"), and a status. Overdue items should escalate — not to management, but to a practice-level safety view that enables peer oversight. This mirrors nuclear power's Corrective Action Programme without creating a punitive surveillance tool.

NLP extraction should use few-shot prompted LLM calls against consultation notes accessed via Medtech ALEX's DocumentReference endpoint. **Start with high-specificity extraction** (fewer false positives, missing some actions) and iterate toward higher recall as clinician trust builds. Present extracted actions as suggestions requiring one-click confirmation, not auto-created tasks — this aligns with NZ regulatory expectations for human-in-the-loop AI and reduces alert fatigue.

---

### AREA 2: NZ billing completeness

#### Evidence base

**ACC explicitly supports dual-billing of a consultation and a procedure code on a single visit, but awareness appears low.** The ACC1520 fact sheet (June 2024) states: "If you're a general practitioner, nurse, or nurse practitioner and are invoicing us under Cost of Treatment Regulations, we can contribute to two parts of your treatment services — a consultation rate and a procedure code. Here's how to make sure you're invoicing for both the consultation and procedure, if administered."

The billing framework is governed by the **Accident Compensation (Liability to Pay or Contribute to Cost of Treatment) Regulations 2003**, amended most recently in 2024 (effective 1 June 2024). Fee increases effective June 2024: **3.56% for GPs, 4.17% for combined GP + nurse consultations, 7.90% for nurses alone**. When both a nurse and GP treat the same patient in a single visit, a **combined/joint consultation rate** applies — the full registered nurse rate plus 50% of the nurse rate. This combined rate was simplified in the 2022 MBIE consultation to reduce under-claiming from the previously complex itemisation requirement.

Procedure codes billable alongside consultations include wound care/dressings (MW codes), suturing, fracture management/plaster casting, bandaging, minor surgical procedures, and injury-related injections. ACC uses its own item codes defined in the CoTR Regulations schedule — not CPT, not ICD-10, and not Read Codes. Read codes are used for *diagnosis* coding; ACC procedure item codes are used for *billing*.

**Capitation is the other major funding stream.** Te Whatu Ora pays PHOs per enrolled patient per annum, stratified by age, gender, and HUHC status. Rates from 1 July 2025 range from **$90.02 (male, 15–24, non-HUHC) to $737.88 (0–4, HUHC) per patient per year** — a nearly eightfold range. The June 2025 agreement delivered the **largest uplift in general practice funding in more than a decade: $180 million in new funding**, including a 6.43% capitation uplift, $60 million in contingent capitation, and $30 million for immunisation performance.

**CarePlus, HUHC, and CSC interact in specific ways that affect both patient fees and practice revenue:**

- **CarePlus** provides $289.18 per eligible patient (those with ≥2 chronic conditions, terminal illness, or high utilisation). Funding allows for 5% of the NZ population.
- **HUHC** requires 12+ visits in 12 months for an ongoing condition. It provides a subsidy equivalent to the CSC rate; capitation is substantially higher for HUHC patients.
- **CSC** is income-tested, reduces patient co-payments, and triggers higher ACC consultation rates and capitation.
- **HUHC + CSC**: Te Whatu Ora states "there is no advantage in having a HUHC if you already have a CSC because the subsidy is the same" — but HUHC triggers higher capitation, so there may be a practice-level revenue difference.
- **ACC + CSC**: ACC pays a higher rate for CSC holders. **If CSC status is not correctly recorded in the PMS, the lower standard ACC rate is claimed.**
- **Triple stack (CSC + CarePlus + ACC)**: possible and legitimate — ACC covers the injury visit, CarePlus capitation covers chronic condition management, CSC enhances both the ACC consultation rate and general capitation tier.

#### Documented billing errors

**There is a significant absence of published NZ-specific research on billing errors.** No peer-reviewed study quantifying under-billing in NZ general practice was found. An OIA request (GOV-044915, February 2026) sought ACC's provider billing integrity and audit data for 2019–2025 but was only "partially successful," with detailed data not released publicly.

The commonly missed items inferred from ACC guidance and practice-level sources include:

- **Procedure codes not billed alongside consultations** — the primary dual-billing gap
- **Nurse consultations not billed** — school nurse forums confirm many nurses "don't feel it merits a claim" for wound checks and re-dressings
- **Joint GP + nurse rate not claimed** — the combined rate is higher than the GP-only rate, but the pre-2022 itemisation complexity led to under-claiming
- **CSC-enhanced ACC rates not applied** — depends on correct PMS recording of patient CSC status
- **Under-14 zero-fees rate not claimed** — ACC compensates at a higher rate
- **Missing ACC claims entirely** — treating injury patients without lodging an ACC45 claim form
- **Immunisation administration fees not claimed** — $46.05 for childhood immunisations, $37.50 for influenza/COVID, $20.52 for co-administration

US data suggests 15–25% of claims are inaccurately submitted each month (Empeek). While NZ's system is structurally simpler than US insurance billing, the principle of performed-but-not-billed clinical work applies universally.

#### Existing AI charge capture tools

The US market has multiple ambient AI tools with billing features: **Nuance DAX Copilot** ($500–1,500/month), **Suki AI** (~$399/month), **Abridge** (~$250/month, deep Epic integration), **Regard** (chart review focus), **Nabla** (~$120/month), and **ENTER** (dedicated RCM AI). These tools compare clinical documentation against ICD-10/CPT code sets, extract billable entities via NER, and flag discrepancies between documented and billed services.

**None works with NZ ACC billing codes or Read Codes.** Adaptation for NZ requires:

- Replacing the ICD-10/CPT mapping layer with an ACC item code mapper
- NZ has no E&M (Evaluation & Management) visit levels — ACC pays a flat consultation rate, eliminating the most complex US charge capture task
- The NLP task in NZ is narrower: detect whether a procedure was performed (from free text), identify provider type (GP/nurse/combined), and verify patient funding category (CSC/HUHC/CarePlus/age) — then check whether the corresponding billing codes were submitted
- Read Code → ACC eligibility mapping (is this an injury?) draws on structured diagnosis data already in the PMS

In Australia and the UK, **Heidi Health** and **Ardens** respectively offer workflow-integrated tools, but neither provides ACC-equivalent charge capture. No commercially available tool for NZ ACC billing optimisation was identified.

#### Design implications for the dashboard

**The billing checklist module is the simplest of the three to build and the fastest to generate ROI.** The minimum viable signal set combines:

**Structured data (from Medtech ALEX):**
- Read/SNOMED code for diagnosis → ACC eligibility check (is this an injury?)
- Provider type recorded → consultation rate tier (GP / nurse / combined)
- Patient demographics → age (under-14 rate), CSC status, HUHC status
- Encounter timestamp → after-hours flag
- ACC claim number → confirms ACC-funded visit exists

**Unstructured data (NLP on clinical notes):**
- Procedure keywords: "dressed wound," "sutured," "plastered," "injected," "nurse performed," "both GP and nurse"
- Injury keywords triggering ACC claim check: "fell," "sprain," "fracture," "accident"
- Chronic condition mentions triggering CarePlus eligibility check
- Visit frequency patterns triggering HUHC eligibility check (12+ visits in 12 months)

**Architecture:** Read Code tells you *what* was treated; free text tells you *how* and *who treated it*. Both are needed to determine correct billing. The tool should present a post-consultation billing checklist: "You documented a wound dressing — procedure code MW not billed. Add?" This is a high-confidence, low-risk suggestion that requires minimal NLP sophistication.

**Start with ACC dual-billing detection** (consultation + procedure gap) as the first feature. Expand to CSC/HUHC rate verification (checking PMS demographics against billed rates) and CarePlus eligibility flagging. Immunisation administration fee reminders are a quick win requiring only coded data.

---

### AREA 3: Clinical inbox triage

#### Evidence base

**There is no standardised, published prioritisation framework for GP inbox triage anywhere in the world.** Watson et al. (*BJGP*, 2022) found GP methods of communicating and actioning test results varied between doctors even within the same practice, based on "habits, unwritten heuristics, and personal preferences rather than protocols." No RNZCGP or RCGP guideline specifically addresses result prioritisation or inbox processing workflows.

The problem is well-quantified. Murphy et al.'s landmark study (*JAMA Internal Medicine*, 2016) analysed 276,207 notifications from 92 physicians and found **PCPs received a mean of 76.9 notifications per day** versus 29.1 for specialists (p < .001). Arndt et al. (*Annals of Family Medicine*, 2017) found family medicine physicians spent **5.9 hours/day in the EHR — 85 minutes (23.7%) on inbox management alone**. Tai-Seale et al. (*Health Affairs*, 2017) documented a near-equal split: **3.08 hours on office visits and 3.17 hours on "desktop medicine" per day**. Rotenstein et al. (*JAMA Network Open*, 2024) found total EHR time per visit was **36.2 minutes** for a 30-minute scheduled visit — more time on EHR than with the patient.

The burden is growing. Post-pandemic, PCP inbox time increased by 15.6% and patient medical advice requests surged 104.9% (Nath et al., *JAMIA*, 2024). System-generated messages — almost half of all inbox messages — were associated with **40% higher burnout probability** and **38% higher intent to reduce clinical time** (Tai-Seale et al., *Health Affairs*, 2019). Singh et al. (2013) found that **one-third of VA PCPs reported personally or knew a colleague who had missed an abnormal result** due to information overload. Alert fatigue is extreme: clinicians override safety alerts **49–96%** of the time (Phansalkar, Harvard Medical School).

#### NLP for urgency detection

**Radiology report triage is the most tractable NLP task within inbox triage.** The ACR Actionable Reporting Work Group (Larson et al., *JACR*, 2014) defines three urgency categories: Category 1 (minutes — e.g., tension pneumothorax, acute PE), Category 2 (hours — e.g., intracranial haemorrhage, appendicitis), and Category 3 (days — e.g., suspicious nodule, incidental renal mass).

Model performance is strong on internal data:

- **RadBERT** (Yan et al., *Radiology: AI*, 2022), pre-trained on 2.16–4.42 million VA radiology reports, achieved **>97.5% accuracy and >95.0 F1** for abnormal sentence classification. RadBERT-RoBERTa significantly outperformed all baseline models including BERT, BioBERT, ClinicalBERT, and BlueBERT.
- **ClinicalBERT++** (Banerjee et al., *J Digital Imaging*, 2023), fine-tuned on 3 million radiology reports, achieved **F1 = 0.96 on internal data** but dropped to **0.81 precision and 0.54 recall on external (Mayo Clinic) data** — a significant generalisation gap.
- **Rule-based NLP** (Lakhani et al., 2012) achieved **sensitivity 97.2% and specificity 95.2%** for nine critical findings using keyword lists with negation exclusion — a remarkably competitive baseline.
- **GPT-4 with dynamic few-shot prompting** (AJR, 2025) offered nuanced, context-dependent classifications without fine-tuning, representing a potential rapid-deployment approach.

Linguistic markers that distinguish urgency include "urgent," "new finding," "malignancy suspected," "acute" (critical) versus "stable," "unchanged," "incidental," "benign-appearing" (routine). Hedging language — "cannot exclude," "may represent," "correlate clinically" — is the primary NLP challenge, as is the fact that **36.4% of pulmonary nodules are documented in "Findings" but not "Impression" sections**.

**Specialist letter triage is a near-complete research gap.** No published NLP model specifically addresses urgency classification of specialist correspondence. Linguistic signals exist — "please arrange," "please commence," "urgent review needed" versus "for your information," "no further action required" — but these are buried in semi-structured text with enormous variation across specialties and individual clinicians. Weak supervision approaches (Wang et al., *BMC Med Inform Decis Mak*, 2019) achieving F1 of 0.92–0.97 on institutional classification tasks suggest a viable path, but no validation for letter triage exists.

#### Cognitive load and decision fatigue

Cognitive load measurably impacts clinical decisions. A Berkeley/UCSF study (2024) found physicians in the **top decile of cognitive load ordered 42% more diagnostic tests** and were **28% more likely to admit patients** compared to the same physician at baseline. A systematic review (*Health Psychology Review*, 2025) confirmed decision fatigue as "the tendency towards making less effortful decisions as the cumulative mental burden of effortful decision-making increases."

The ProSPER system identified five information hazards: **overload, underload, scatter, conflict, and erroneous information**. Holmstrom et al. (*Applied Clinical Informatics*, 2018) found physicians need comprehensive contextual information to triage results — the clinical picture, trend data across time, integration across EHR sections — and struggled to retrieve it. The ClinicalBERT++ finding that incorporating "reason for exam" alongside findings **significantly improved classification accuracy** (e.g., correctly classifying post-operative pneumoperitoneum as expected rather than critical) has direct design implications: the triage display must show why the test was ordered.

#### Existing tools and interventions

Epic InBasket dominates but has documented problems. NYU Langone Health found some physicians receive **>150 messages/day**, with "several types of messages flooding physicians' inboxes that have very low — if any — clinical value." The system has **no native urgency prioritisation**; clinicians reported they "did not prioritize messages due to time constraints and the necessity of attending to all messages, which made any prioritization purely additive to overall inbox time."

Interventions that reduce burden include **team-based pre-processing** (a rotating "InBasket quarterback" model reduced all four participating physicians' burnout), **protected inbox time** (Michigan Medicine's PACE slots — 88% of physicians agreed they reduced after-hours work), and the AMA's STEPS Forward toolkit recommending analysis of inbox composition to redirect low-value notifications. The VHA's nationwide notification optimisation reduced daily alerts by 5.9% but **did not significantly reduce burnout** — suggesting volume alone is insufficient and that content, cognitive load, and presentation matter more.

Design patterns that reduce processing time: pre-sorting by urgency, one-click actions ("Normal — file"), suggested responses, auto-routing by message type, and batch processing by category rather than chronological order. What introduces error: alert fatigue, burying critical items in routine notifications, unclear ownership of results, and note bloat.

#### Design implications for the dashboard

**The inbox triage module should be layered: radiology first, labs second, specialist letters third.**

Radiology is the strongest NLP domain with the clearest urgency taxonomy (ACR categories). A hybrid approach — rule-based keyword detection with LLM-based contextual classification for ambiguous cases — maximises safety while managing cost. The 97.2% sensitivity/95.2% specificity of Lakhani et al.'s simple rule-based system suggests a rule-based first pass with LLM escalation for uncertain cases is both safe and affordable.

For lab results, the triage task is less about NLP (labs are structured data) and more about **contextual presentation**: show the previous values as a trend, highlight the ordering reason, flag the patient's active problem list, and indicate staleness (time since result generated). Delta checking against previous values is computationally trivial and clinically powerful.

For specialist letters, design for **keyword-triggered flagging** (action-required phrases like "please arrange," "please commence") as a minimum viable product, with LLM classification as a later enhancement. Acknowledge this is the least mature NLP domain and set user expectations accordingly.

**Present the inbox as three priority lanes** (critical / action-required / information-only) rather than a single chronological list. Show the minimum contextual information needed per item — patient name, test type, key finding, ordering reason, trend indicator — to enable triage without opening the full result. Every item should have one-click resolution actions. Never allow a critical item to be filed without explicit acknowledgement.

---

## 3. Cross-cutting themes

### AI/NLP feasibility across all three domains

**The technical feasibility question has shifted from "can LLMs extract clinical information?" to "can they do so reliably enough for safety-critical applications in a small, non-US clinical text environment?"** The answer is conditionally yes, with important caveats.

Zero-shot and few-shot commercial LLM performance on clinical text is now competitive with fine-tuned domain-specific models for most extraction tasks. Agrawal et al. (2022) showed InstructGPT significantly outperforms existing baselines with just 5 examples. Fine-tuned open-source models (Llama-3.1 8B) achieve 90% exact match accuracy with ≤100 training reports. LLM API costs have collapsed: **processing 10,000 notes/day through a mid-tier model costs ~$600 NZD/month**, and budget models reduce this to $30–100 NZD/month.

However, **no NZ clinical NLP benchmark exists**. NZ GP notes are distinctive: terse SOAP-format entries, Read Code v2 mixed with emerging SNOMED CT, NZ-specific abbreviations, te reo Māori terms, NZ medication brand names, and NZ English spelling. LLMs trained on US clinical text may not handle these without NZ-specific prompt examples. The builder should create a gold-standard annotation set of **100–300 NZ GP notes** annotated for action items, billing signals, and urgency indicators to validate performance before deployment.

The three domains have different NLP difficulty profiles:

- **Billing**: Easiest. Narrow keyword detection (procedure terms) plus structured data matching. High precision achievable with simple approaches.
- **Action items**: Moderate. Requires understanding implicit and conditional actions, temporal references, and negation. Few-shot LLM prompting is the right approach, with clinician confirmation for all extracted items.
- **Inbox triage**: Hardest for specialist letters, easiest for labs (structured), moderate for radiology (strong existing models but external generalisation drops). Multi-modal: some items need NLP, others need structured data analysis.

**The recommended technical architecture is a hybrid pipeline**: structured data extraction via Medtech ALEX FHIR API → rule-based first-pass detection → LLM API call for ambiguous or complex text → clinician-facing suggestion interface. This maximises safety (rules catch the obvious; LLMs handle nuance; clinicians validate everything) while keeping costs low.

### NZ-specific regulatory and funding constraints

**The regulatory environment is permissive but transitional.** NZ currently has no pre-market SaMD framework — the Therapeutic Products Act 2023 was passed but is being repealed in favour of a Medical Products Bill still in development. Until that Bill is enacted, clinical decision support software faces no formal regulatory barrier beyond the Health Information Privacy Code 2020 and the Code of Health and Disability Services Consumers' Rights. The Waitematā DHB AI Governance Framework (*npj Digital Medicine*, 2023) — NZ's most detailed published clinical AI governance example — provides a practical template: transparency, Te Tiriti partnership, kaitiakitanga, no black-box algorithms, mandatory clinician oversight.

Health NZ's internal AI policy requires that **all AI-generated information impacting patient records or clinical decisions must be reviewed by a responsible clinician**. This aligns with the recommended human-in-the-loop design across all three domains.

Privacy is manageable. The HIPC permits use of health information for directly related purposes (clinical decision support falls within the purpose of improving patient care, though this is legally untested). **Practical mitigations include de-identification before cloud API calls, use of Azure NZ region (Medtech ALEX is already Azure-based), and practice-level consent through the Medtech Partner Programme.** Open-source model deployment on-premise (Llama 3.x on a single GPU) is a fallback for practices with strict data sovereignty requirements.

The **Read Code → SNOMED CT transition** is ongoing with no hard cutoff date. ACC still accepts Read Codes and internally translates SNOMED CT to Read. The dashboard should handle both coding systems using published mapping tables from Health NZ. The capitation formula reform (expected 1 July 2026) may change some billing logic; design for configurability.

### Patient safety implications

Action item capture addresses the most severe safety gap. The evidence is unambiguous: **follow-up failure rates of 6.8–62% for labs, safety-netting documented for fewer than half of clinical problems, GPs relying on personal memory and bespoke workarounds, and no EHR system globally tracking soft follow-up actions.** A well-designed action tracking system moves the locus of safety from person-dependent to system-dependent — the core principle of high-reliability organisations.

Inbox triage has the second-strongest safety case. One-third of GPs report personally experiencing or knowing a colleague who missed an abnormal result due to information overload (Singh et al., 2013). The **49–96% alert override rate** means existing notification systems are failing. A triage layer that surfaces truly critical items while de-emphasising routine normal results could reduce the signal-to-noise ratio without adding to alert fatigue — but only if the prioritisation is accurate enough that clinicians trust it.

Billing completeness has an indirect safety implication: practices that capture appropriate revenue are more financially sustainable, can hire more staff, and can invest in safety systems. Under-billing creates financial pressure that ultimately affects care quality.

### Data availability assumptions

Medtech ALEX (v2.9, September 2025) provides FHIR-based access to **Patient, Condition, AllergyIntolerance, Observation, DocumentReference, Consultation notes, Practitioner, and Appointment/Schedule** resources across 1,000+ NZ primary care sites. The API supports OAuth authentication, requires practice consent, and is governed by a Partner Code of Conduct. **25+ certified partners** are already live, with lab results delivery operational at 64 sites.

The builder should assume:
- **Clinical notes** are accessible via DocumentReference (free text + coded data)
- **Lab results** are available via Observation (structured, real-time via HL7 v2 or FHIR)
- **Radiology reports** are available via DocumentReference (Zed Technologies integration already delivers Horizon Radiology reports via ALEX)
- **Patient demographics** (age, CSC, HUHC status) are available via Patient resource
- **Problem lists and medications** are available via Condition and MedicationStatement
- **ACC claim data** may require separate ACC API integration (not confirmed via ALEX)

The key data gap is **specialist letters and clinical correspondence**, which may not be consistently digitised or available via ALEX. Many specialist letters still arrive via HealthLink as semi-structured HL7 messages or PDF attachments. The inbox triage module for specialist letters will likely need to handle these heterogeneous input formats.

---

## 4. Recommended further reading

**1. Callen JL, Westbrook JI, Georgiou A, Li J. "Failure to follow-up test results for ambulatory patients: a systematic review." *J Gen Intern Med*. 2012;27(10):1334–1348.**
Foundational systematic review establishing the 6.8–62% lab follow-up failure range. Essential evidence base for the action item capture safety case.

**2. Singh H, Spitzmueller C, Petersen NJ, et al. "Information overload and missed test results in electronic health record-based settings." *JAMA Intern Med*. 2013;173(8):702–704.**
Establishes the 63 alerts/day figure and documents information overload as a root cause of missed results. Primary source for the inbox triage problem definition.

**3. Murphy DR, Reis B, Kadiyala H, et al. "Electronic health record-based messages to primary care providers: valuable information or just noise?" *Arch Intern Med*. 2012;172(3):283–285. AND Murphy DR, Meyer AND, Russo E, et al. "The burden of inbox notifications in commercial electronic health records." *JAMA Intern Med*. 2016;176(4):559–560.**
The 76.9 notifications/day and >1 hour daily processing time figures originate here. Critical for quantifying the inbox triage problem.

**4. Jones D, Dunn L, Watt I, Macleod U. "Safety netting for primary care: evidence from a literature review." *BJGP*. 2019;69(678):e70–e79.**
Comprehensive review of 47 studies on safety netting. Demonstrates the concept is widely endorsed but poorly standardised — directly supports the action item module's value proposition.

**5. Agrawal M, Hegselmann S, Lang H, Kim Y, Sontag D. "Large language models are few-shot clinical information extractors." *EMNLP 2022*: 1998–2022.**
Seminal paper proving LLMs can extract clinical information with minimal training examples. Directly informs the NLP architecture for all three domains.

**6. Yan A, McAuley J, Lu X, et al. "RadBERT: adapting transformer-based language models to radiology." *Radiology: AI*. 2022;4(4):e210258.**
Pre-trained on millions of VA radiology reports, RadBERT sets the benchmark for radiology NLP. F1 > 95 for abnormal classification. Key reference for the inbox triage radiology component.

**7. ACC1520 fact sheet: "Medical practitioners, nurse practitioners and nurses: treatment cost rates." ACC, June 2024.**
The primary source for ACC dual-billing rules. Documents consultation rates, procedure codes, and the combined GP + nurse rate. Essential for building the billing module's rule engine.

**8. Te Whatu Ora. "Capitation rates." Last updated 3 November 2025.**
Official source for all capitation rates by age, gender, HUHC status, and funding category. Required data for the billing completeness module's rate verification features.

**9. Waitematā DHB. "Clinical artificial intelligence governance framework." *npj Digital Medicine*. 2023;6:157.**
NZ's most detailed published clinical AI governance framework. Covers Te Tiriti obligations, transparency requirements, and clinician oversight mandates. Template for the dashboard's governance design.

**10. Arndt BG, Beasley JW, Watkinson MD, et al. "Tethered to the EHR: primary care physician workload assessment using EHR event log data and time-motion observations." *Ann Fam Med*. 2017;15(5):419–426.**
Establishes that 85 minutes/day (23.7% of EHR time) is spent on inbox management. Key evidence for the inbox triage ROI calculation.

**11. Reason J. "Human error: models and management." *BMJ*. 2000;320(7237):768–770.**
The Swiss Cheese Model paper. Foundational for the action item module's design philosophy: system-dependent, not person-dependent safety.

**12. Nicholson BD, Mant D, Bankhead C. "Can safety-netting improve cancer detection in patients with vague symptoms?" *BMJ*. 2016;355:i5515. AND Nicholson BD, et al. "Safety netting in primary care: qualitative study." *BJGP*. 2018;68(672):e505–e511.**
Documents GPs' bespoke, inconsistent safety-netting strategies and the selective follow-up of higher-risk patients. Evidence that informal systems fail systematically.

**13. Medtech ALEX API Documentation. Version 2.9, September 2025. alexapidoc.medtechglobal.com.**
Technical documentation for the FHIR API that will serve as the integration layer. Covers authentication, supported resources, and partner programme requirements.

**14. Banerjee I, Rao G, Wawira Gichoya J, et al. "ClinicalBERT++: fine-tuned model for clinical report classification." *J Digit Imaging*. 2023;36:1190–1201.**
Demonstrates strong radiology triage NLP (F1 0.96 internal) but critical generalisation drop on external data (recall 0.54). Essential caution for the inbox triage module's NLP design.

**15. Health Information Privacy Code 2020. Office of the Privacy Commissioner, New Zealand.**
Governs all processing of health data in NZ. Rules 5, 10, and 11 are directly relevant to AI processing of clinical notes. Must-read for compliance design.