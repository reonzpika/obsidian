# Manual care gap monitoring in NZ general practice: where AI fits

**NZ general practices manually track a substantial and growing set of care gaps — yet the process is fragmented, labour-intensive, and systematically failing the populations who need it most.** Practice nurses and HCAs bear the bulk of this work, running PMS queries, reviewing PHO-provided lists, and contacting patients one by one. No dedicated AI care gap detection system exists in New Zealand today. The closest precedents are rule-based RPA tools from Health Accelerator and the ageing DrInfo audit platform. The equity stakes are severe: Māori cardiovascular risk assessment coverage sits at roughly **46%** against a 90% target, cervical screening coverage for Māori and Pacific peoples lags European rates by nearly 20 percentage points, and Māori childhood immunisation at 24 months is just **69%**. An AI system scanning a practice's patient list against guideline-recommended intervals would directly address the highest-burden, highest-impact gaps — provided it is designed to reduce rather than entrench these disparities.

---

## How care gap monitoring actually works in a NZ practice

The typical NZ general practice divides care gap monitoring across three roles. **Practice nurses** are the primary workforce: they run PMS recall searches, manage chronic disease registers, lead diabetes annual reviews, perform cardiovascular risk assessments, and coordinate screening recall. **Health care assistants (HCAs)** handle an expanding share of routine recall tasks — contacting patients overdue for CVD checks, flu vaccinations, and simpler screening recalls — always under the delegation of a registered nurse. **GPs** are generally not performing front-line recall work; RNZCGP's 2024 "Your Work Counts" study found **44% of GP workload is non-patient-facing**, consumed by inbox management, correspondence, and clinical oversight rather than population health scanning.

The standard workflow runs in five steps: (1) generate a patient list from the PMS recall module, DrInfo audit tool, or a PHO-provided population health report; (2) a nurse or HCA reviews the list for accuracy and clinical relevance; (3) contact the patient via bulk SMS, phone call, or ManageMyHealth portal message; (4) book the appropriate appointment; (5) deliver the care and reset the recall date. Health Care Home practices — now numbering over **300 nationally** — add a risk stratification layer, using algorithms to identify the top 7% of adults at risk of hospital admission. But many smaller practices still rely on manual, ad hoc PMS queries with no systematic population-level scanning.

**No published NZ study directly quantifies hours per week** spent on care gap monitoring. The data gap itself is telling. What is known: the RNZCGP 2022 Workforce Survey reported average GP hours of **35.9 per week**, with 48% rating themselves as highly burnt out. A University of Otago study found average PMS feature usage at only **35.7%**, with user knowledge rated **2.2 out of 5** — meaning practices are underutilising the tools they already have.

---

## Diabetes monitoring: the most complex and highest-burden gap

**Guidelines and scope.** The NZSSD/MoH Type 2 Diabetes Management Guidance (2021) mandates an annual review including HbA1c, uACR, serum creatinine/eGFR, LFTs, non-fasting lipids, blood pressure, weight, neurovascular foot examination, retinal photoscreening (every 2 years), CVD risk assessment, smoking status, mental health assessment, immunisation status, and cancer screening status. Patients not at target require **3–6 monthly** HbA1c and renal function monitoring. This is the most data-intensive care gap in general practice.

**Who and how.** Practice nurses typically lead the diabetes annual review, running DrInfo or PMS register queries to identify patients overdue. HCAs may handle initial recall contact. The PHO Performance Programme historically tracked HbA1c, microalbumin, creatinine, and lipid completion rates, with PHOs supplying practice-level reports. Completion rates reached only **65.8%** against an 80% target as of available audit data — and that figure measures testing, not the full comprehensive review.

**Equity impact.** Diabetes prevalence among Pacific peoples is **12.5%** — more than double the NZ European rate of 5.4%. Māori prevalence is **7.0%**. The glycaemic control gap is stark: Māori and Pacific patients have HbA1c levels **11–13 mmol/mol higher** than NZ Europeans even after adjusting for management and demographics. This disparity has persisted for 25 years. Māori aged 45–64 have diabetes death rates **9 times higher** than non-Māori of the same age, and Māori and Pacific peoples account for **67% of end-stage renal disease** due to diabetic kidney disease versus 31% for others.

**Current tools.** Medtech Evolution's Recalls and Screening module, Query Builder, and IPIF Management reports. DrInfo provides diabetes-specific audit reports covering government health programme compliance. PHOs supply quarterly performance data.

**AI substitutability: HIGH.** The diabetes annual review is a rule-based, data-rich task with clearly defined intervals, measurable lab values, and structured coding in the PMS. An AI system can scan for: last HbA1c date and value, last uACR, last creatinine/eGFR, last lipid panel, last retinal screening date, last foot check documentation, and time since last comprehensive review. Prioritisation can layer clinical urgency (HbA1c trending upward, declining eGFR) with equity weighting (Māori/Pacific patients, high deprivation). This is the single highest-value target for automation.

---

## Cardiovascular risk assessment: the largest equity gap

**Guidelines and scope.** The 2018 MoH/Heart Foundation Consensus Statement sets differentiated age thresholds: screening begins at **age 30 for Māori, Pacific, and South Asian men** and **age 40 for women** in these groups — compared with 45/55 for European/Other without risk factors. Reassessment is 5-yearly for low-risk and annual for high-risk (>15% 5-year CVD risk). The assessment requires blood pressure, non-fasting lipids, HbA1c or fasting glucose, serum creatinine/eGFR, smoking status, BMI, and family history.

**Who and how.** CVDRA is predominantly nurse-led, often as a standalone clinic or opportunistic assessment during other consultations. Health Accelerator's RPA "digital assistant" already automates parts of CVDRA processing on Indici PMS, saving **5.67 minutes per file**. PHOs track CVDRA completion as a key performance indicator.

**Equity impact.** National CVDRA coverage rose from below 20% to over 67% between 2008 and 2013 following PHO Performance Programme incentives, but this still falls well short of the **90% target**. A study of 72,351 adults found the Māori CVDRA rate at guideline-indicated age was only **46%**, and when assessed, **38% of Māori were at high cardiovascular risk**. Māori are **4 times more likely** to be hospitalised with heart failure and **twice as likely** to die from CVD compared with Europeans. Studies show only about half of high-risk patients receive evidence-based dual therapy (statin plus antihypertensive), with Māori and Pacific peoples more likely to miss out.

**AI substitutability: HIGH.** CVDRA eligibility is deterministic — it depends on age, ethnicity, sex, and the presence of risk factors, all of which are coded in the PMS. An AI system can identify every enrolled patient who has reached their guideline-indicated age without a recorded CVDRA, and flag those with known risk factors who should have been assessed earlier. The differentiated age thresholds by ethnicity make this a gap where manual systems commonly fail because staff must remember different rules for different populations.

---

## Cancer screening recall: three programmes, one fragmented process

**Cervical screening.** Since September 2023, New Zealand uses HPV primary screening every **5 years** for people with a cervix aged 25–69. The GP practice is responsible for recall, though the NCSP Register sends backup notifications. Coverage: **Māori 55.0%**, Pacific 55.9%, NZ European/Other **74.6%**. Māori have approximately **twice the cervical cancer incidence and mortality** of European/Other women.

**Breast screening.** BreastScreen Aotearoa provides 2-yearly mammography for women aged 45–69 (extending to 74 by 2029). The GP's role is primarily to encourage enrolment and identify under-screened women. Coverage: Māori **62.4%**, Pacific 67.8%, European/Other **72.3%**.

**Bowel screening.** The National Bowel Screening Programme sends FIT kits every 2 years to those aged 58–74. GP practices promote uptake and follow up positive results. Participation: NZ European/Other **62%**, Māori **50.2%**, Pacific **38.7%**. Māori and Pacific peoples have a **47% and 59% five-year mortality** from colorectal cancer respectively, versus 38% for other groups.

**Who and how.** Cancer screening recall is a shared responsibility: practice nurses and HCAs run PMS queries to identify unscreened and under-screened patients; PHOs supply screening status reports; and national registers provide backup. The RNZCGP Foundation Standard (Indicator 7.1) requires practices to maintain a documented recall procedure with **ethnicity-differentiated audit data** and to demonstrate approaches to achieving equitable screening rates.

**AI substitutability: HIGH for cervical and bowel; MODERATE for breast.** For cervical and bowel screening, the AI can cross-reference PMS data against last screening date and age eligibility — straightforward rule-based logic. For breast screening, the practice's role is more limited because BSA manages its own invitation system, so the AI's value is in identifying women who are enrolled in the practice but not in BSA. The key equity value is in systematically identifying Māori and Pacific patients who have never been screened or are overdue — precisely the patients most likely to be missed by manual processes.

---

## Chronic respiratory disease: under-structured and practice-dependent

**Asthma** guidelines recommend at minimum an annual review covering symptom control (ACT score), inhaler technique, adherence, trigger management, written action plan, and exacerbation history. **COPD** guidelines recommend review every 6–12 months including spirometry, mMRC dyspnoea assessment, exacerbation history, smoking cessation support, and self-management plan review. Unlike diabetes, there is no national structured recall programme for respiratory disease — monitoring is entirely practice-driven using disease registers and ad hoc recalls.

**Equity impact.** Māori and Pacific peoples have higher rates of COPD and asthma hospitalisation. The absence of a structured national programme means respiratory monitoring is more dependent on practice capability, creating wider variation and greater scope for inequity.

**AI substitutability: MODERATE.** The AI can identify patients coded with asthma or COPD who have not had a documented review within the guideline interval. The challenge is that respiratory reviews are less standardised in their documentation — there is no single lab test equivalent to HbA1c — so the system must rely on consultation coding and structured data entry, which is inconsistent across practices. PMS data quality is the binding constraint.

---

## Immunisation recall: strong data infrastructure, poor outcomes

Childhood immunisations follow the NZ National Immunisation Schedule with milestone ages at 6 weeks, 3, 5, 12, and 15 months, 4 years, and 11–12 years. Adult immunisations include annual influenza (funded for over-65s, pregnant women, and chronic conditions), COVID-19 seasonal boosters, and pneumococcal vaccination. Practices are linked to the **Aotearoa Immunisation Register (AIR)**, which provides population-level coverage data.

**Equity impact.** National immunisation at 24 months is **83%** against a 95% herd-immunity target. Māori rates are **69%**. At 6 months, Māori babies in Counties Manukau were only **32.4%** up to date. RNZCGP has stated that "primary care has consistently failed to deliver equitable childhood immunisation."

**AI substitutability: MODERATE-HIGH.** Immunisation data is well-structured (dates, vaccine codes, schedule milestones) and linkable via NHI to the national register. The AI can identify overdue children and adults with chronic conditions who have not received funded influenza vaccination. The Western Bay of Plenty PHO demonstrated that targeted outreach using data dashboards and immunisation champions raised Māori 24-month rates from **57.3% to 78.5%** — a 21 percentage-point gain — suggesting that systematic identification and proactive outreach are the key levers.

---

## Why manual monitoring fails: systemic failure modes

HDC cases reveal recurring patterns. In one case, a patient's HbA1c of 50 mmol/mol (pre-diabetic) was discussed but **no recall was set**; when the GP subsequently left the practice, the patient went 15 months without monitoring and was discovered with an HbA1c of **89 mmol/mol**. In another (18HDC01371), a cervical screening register misalignment caused a patient to miss her second annual smear, leading to cervical cancer — the patient had "slipped through the cracks." HDC found that missed or delayed diagnosis was the primary issue in **15% of complaints** across the health system.

The systemic drivers of failure cluster into five categories. First, **PMS data quality**: inconsistent coding, free text instead of structured Read codes, and average PMS feature utilisation at only 35.7%. Second, **staff turnover**: when a GP or nurse leaves, outstanding recalls and follow-up responsibilities are not systematically transferred. Third, **enrolment gaps**: approximately **20% of the population is unenrolled** in some regions, predominantly Māori, making them invisible to practice-based recall systems. Fourth, **time pressure**: practice nurses and HCAs are managing growing lists with limited hours, and recall work competes with acute clinical demand. Fifth, **lack of accountability**: Wai 2575 found "no consequences for PHOs or practices for ineffective implementation" of equity targets.

---

## What tools practices already have — and what is missing

**Medtech Evolution** dominates the NZ PMS market at **75–85% of practices**. It includes a Recalls and Screening module, Query Builder for custom population health searches, and IPIF Management reports. However, these are tools that require manual operation — someone must build the query, run it, export the list, and action it.

**DrInfo**, used by approximately **50% of practices**, is the closest thing to an automated care gap scanner. It audits PMS data against government health programmes (diabetes, CVD, vaccinations, screening) and generates patient lists for bulk recall. Medtech Global acquired DrInfo in 2021 and is modernising it in partnership with DataCraft Analytics, with the stated goal of "automating data entry and recall processes." This modernisation is the most direct competitor to any new AI tool.

**PHO-provided dashboards** deliver practice-level performance data. DataCraft's **Thalamus** platform, used by 23 PHOs, extracts PMS data and presents equity-focused dashboards. PHOs like ProCare, Pinnacle, and Compass Health supply regular population health lists to practices, particularly for CVDRA and screening targets.

**Health Accelerator**, a joint venture of four major PHOs, deploys rule-based **RPA "digital assistants"** for CVDRA processing, FIT result filing, and ACC claims — saving measurable time per task but operating on only one PMS (Indici) to date. These are not AI systems; they follow predefined steps without learning or adaptation.

What is missing is a **unified, intelligent system** that continuously scans the full patient register against all guideline intervals, prioritises by clinical urgency and equity need, and generates the recall action — without requiring a nurse to manually run each query domain separately.

---

## The realistic AI task and how to define it

International precedents show that care gap detection systems operate at three levels. **Level 1 (gap identification)** scans patient records against clinical rules — "diabetic patient, no HbA1c in 12 months" — and generates a list. This is rule-based, does not require machine learning, and is closest to what DrInfo and PenCS CAT4 (Australia) already do. **Level 2 (prioritisation)** ranks the list by clinical urgency, equity weighting, engagement likelihood, and quality measure impact. This is where AI adds value beyond rules. **Level 3 (recall generation)** automates patient contact via SMS, email, or patient portal, and potentially enables self-booking.

For a **minimum viable product** in NZ, Level 1 is sufficient and achievable. The AI (or more accurately, the rules engine) needs read access to the practice PMS — specifically problem lists, lab results with dates, immunisation records, consultation dates, prescription data, and patient demographics including ethnicity, age, sex, and NHI. It does not need to integrate with national collections for the MVP, though NHI-linked data from the Pharmaceutical Collection, Lab Claims Collection, and screening registers would significantly enrich accuracy at later stages.

**NZ's NHI system is a major enabler** — every patient has a unique identifier that theoretically links PMS data, lab results, pharmacy dispensings, and screening registers. This is a structural advantage over more fragmented systems internationally. The primary barriers are the **fragmented PMS landscape** (vendor rivalry between Medtech and Indici has limited interoperability), the absence of a national primary care clinical dataset, and legacy IT infrastructure.

Privacy considerations are navigable. Scanning patient records for care gaps falls within the Health Information Privacy Code 2020's Rule 10 (use for directly related purposes). Health NZ's stated AI position requires clinician review of any AI output affecting clinical decisions — the care gap list must be a recommendation, not an automated action. Te Tiriti obligations require that any system explicitly addresses Māori data sovereignty and equity, and must not widen existing disparities.

**Alert fatigue is the critical design risk.** International evidence consistently shows that interruptive pop-up alerts are counterproductive — VA primary care clinicians received over 100 alerts per day, with 86.9% reporting excessive burden. The system must use **passive decision support**: asynchronous lists, batch recall workflows, and practice dashboards rather than per-patient pop-ups.

---

## The five care gaps most suitable for AI automation

The following ranking weighs four factors: (1) clinical impact of the gap, (2) equity impact for Māori and Pacific populations, (3) data availability and rule clarity for automation, and (4) current manual burden on practices.

**1. Cardiovascular risk assessment recall.** CVDRA has the largest absolute equity gap (Māori coverage at 46% vs 90% target), clearly defined age-by-ethnicity eligibility rules that are error-prone when applied manually, high clinical stakes (Māori are 4× more likely to be hospitalised with heart failure), and an existing proof point in Health Accelerator's RPA tool. The differentiated screening ages by ethnicity make this the gap where an automated system adds the most value over manual processes.

**2. Diabetes annual review and interval monitoring.** The most data-intensive care gap, with multiple lab values, examination components, and variable monitoring intervals based on clinical status. Completion rates well below target, a 25-year-persistent ethnic disparity in glycaemic outcomes, and extreme downstream consequences (9× diabetes mortality for Māori aged 45–64). The structured, lab-based nature of diabetes monitoring makes it highly amenable to automated scanning.

**3. Cervical screening recall for under-screened populations.** A 20-percentage-point coverage gap between Māori/Pacific and European populations, with twice the cancer incidence and mortality. The shift to 5-yearly HPV screening makes timely recall even more critical — longer intervals increase the risk of patients being lost to follow-up. Rule logic is simple (last screening date, age, eligibility) and PMS integration with the NCSP Register is established.

**4. Childhood immunisation timeliness.** The best-structured data of any care gap (dates, vaccine codes, schedule milestones, AIR linkage), the most severe equity gap in absolute terms (Māori at 6 months as low as 32% in some areas), and proven evidence that systematic outreach dramatically improves rates (WBOP PHO's 21-percentage-point gain for Māori). The barrier is less about identification — the AIR already tracks this — and more about integrating recall into the practice workflow.

**5. Bowel screening participation for Māori and Pacific patients.** Pacific participation at 38.7% is the lowest of any major screening programme, with significantly worse cancer survival. The GP practice's role is to promote uptake and follow up non-responders. An AI system can identify enrolled patients in the eligible age range who have not returned a FIT kit, enabling targeted practice-level outreach to supplement the national programme's postal approach.

Each of these five gaps shares three characteristics: deterministic eligibility rules, structured data in the PMS, and a measurable equity gradient that a well-designed system can explicitly target. The AI does not need to make clinical judgements — it needs to reliably answer the question "which patients are overdue, and which matter most?" That is a task where automation consistently outperforms manual processes, and where the cost of continued manual failure is measured in preventable deaths.