---
title: Research R5 — Synthetic NZ GP Inbox Dataset Generation Protocol
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-12
status: provisional
---

> **Provisional status note.** This protocol is the Sprint 2 R5 research deliverable. It is **provisional pending Sprint 1 GP clinical review feedback** (task `rd-20260405-001`, due 20 Apr 2026). The Sprint 2 research plan deferred R5 until that feedback landed because every item in the synthetic dataset encodes the urgency taxonomy. We are proceeding now (per user direction) so that generation can start on Day 0 with Day 8 reserved for taxonomy delta absorption (see §10). The schema in §10.5 separates `gold_label_urgency` from `gold_label_rationale` and adds a `taxonomy_version` field, so a post-rd-20260405-001 refinement triggers a targeted re-label of only affected rationales (estimated 15–30% of the dataset, 4–8 GP-hours) rather than a full re-label.

## 1. Executive Summary

This report specifies an executable protocol for generating, labelling, and releasing 300–500 synthetic NZ GP inbox items in the 2-week Sprint 2 window (12–25 Apr 2026), as the evaluation substrate for the Sprint 3 Inbox Helper architecture bake-off. The dataset must support a recall-optimised ordinal 4-class classifier (Immediate / Urgent / Routine / Information only) across 5 document types (lab results, radiology reports, discharge summaries, specialist letters, patient portal messages), with eventual ≥99 % sensitivity on Immediate/Urgent and macro F1 ≥0.80.

**Recommended end-to-end approach (eight load-bearing decisions):**

1. **Two-track design.** Sprint 2 produces a 400-item **stratified, enriched** development/eval split with minority-class oversampling. The natural-prevalence holdout for PPV/NPV/calibration is a Sprint 4 deliverable (Buderer-sized). This mirrors n2c2, MIMIC-derived triage work, and Apathy et al. 2024.
2. **Synthea + LLM composition pipeline.** Use Synthea (or a thin custom patient generator) to scaffold ~100 longitudinal synthetic patient records — demographics, problem list, medications, prior labs — then generate the 400 inbox documents *against* those patient histories. This grounds reference ranges, units, and medication lists for free, and makes contextual-reasoning stress items tractable.
3. **Multi-model, label-decoupled, persona-pooled generation.** Use ≥2 frontier model families (Claude Sonnet 4.6 + a second family for paraphrase/cross-check) to break single-model monotone. Never give the generator the urgency label; specify the *clinical scenario* and let urgency emerge as a consequence. ≥30 personas in the pool, persona × doc-type sampling.
4. **Three mandatory shortcut-prevention controls.** (a) Label-decoupled generation; (b) post-hoc style normalisation pass that strips overt urgency cues (URGENT, !!, ALL-CAPS) while preserving facts; (c) TF-IDF/bag-of-words back-classification check — if a linear baseline exceeds ~70 % accuracy on urgency, regenerate.
5. **Contextual-reasoning stress subset of ~15–20 % (60–80 items).** Constructed via parameter layering against the Synthea patient context, with counterfactual contrast pairs. Directly addresses the NHS GPT-oss-120b primary-care medication-review finding (arXiv 2512.21127, Oct–Nov 2025) that contextual-reasoning failures outnumber factual errors ~6:1.
6. **Single-annotator labelling protocol with calibration.** Ryo (1 GP, ~30 weekend hours over 2 weekends + evenings, ~60 h total) labels 100 % of items in 2 passes (~9 min/item weighted average). A 25-item calibration set is re-labelled blind at Days 2, 7, 13 to track intra-rater drift; quadratic-weighted κ ≥0.75 across rounds is the floor. "When in doubt, label up" is the recall-optimised labelling convention.
7. **Privacy-safe NZ-flavoured generation.** Reserved synthetic NHI prefix (`ZZI`/`ZZO` using HISO-excluded letters I and O so values are guaranteed non-collidable, with intentionally-failing mod-11 check digit), fictional name pool, fictional practice/specialist names, jittered lab values within plausible NZ reference ranges, ethnicity enrichment (Māori 20 %, Pacific 12 %) per Te Mana Raraunga and NEAC 2022. Generation runs on **Catalyst Cloud Wellington** (primary, NZ-sovereign open-model) or **AWS Bedrock ap-southeast-6 Auckland** (fallback if Claude available natively) to satisfy the MBIE R&D-in-NZ grant clause.
8. **14 programmatic release gates** (G1–G14) implemented as `tools/qa_report.py` exit-code contract — schema validation, label distribution within ±3 % per cell, MinHash near-duplicate <2 %, embedding near-duplicate <3 %, PII/PHI scan zero hits, lab reference-range plausibility, MTLD lexical diversity, intra-rater κ ≥0.75, content-label sanity audit ≥48/50, boundary-case coverage ≥15 %, datasheet completeness. Four sprint gates (Day 2 seed, Day 7 week-1 close, Day 11 IRA, Day 14 release).

**The headline framing for Sprint 3.** The synthetic dataset is designed to enable architecture *ranking*, not absolute performance estimation. Synthetic-to-real transfer gaps of 8–15 percentage points are documented in the literature (Abdalhalim 2025, Libbi 2021, Finlayson 2021); architecture rankings tend to be more stable than absolute scores. Sprint 3 must explicitly discount synthetic scores by ~10 points when extrapolating to real-data performance, hold out budget for a tiny real-data sanity sample, and report stratified metrics by document type, difficulty band, and ethnicity.

## 2. Published Synthetic Clinical Dataset Work

### 2.1 Synthea — the structured backbone

**Walonoski J et al. (2018)**, *Synthea: an approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record*, JAMIA 25(3):230–238 ([doi](https://doi.org/10.1093/jamia/ocx079); GitHub `synthetichealth/synthea`).

Synthea is the canonical open-source structured patient generator. Its Generic Module Framework runs disease-specific state machines authored against published incidence/prevalence statistics (CDC BRFSS, MEPS) and emits FHIR, C-CDA, HL7 v2, and CSV outputs. Production runs of 1 M+ synthetic patients are routine; MITRE ships pre-generated state populations (e.g. SyntheticMass).

**What it covers.** Demographics, encounters, conditions, medications, procedures, observations (lab values with realistic LOINC coding and reference ranges), imaging metadata, immunisations, allergies. HL7 v2 ORU^R01 lab messages are emitted directly — exactly the structured layer underlying our Lab results document type.

**What it does not cover.** Almost no free text. Discharge summaries, radiology prose, specialist letters, patient messages are out of scope. The narrative gap is precisely the gap NexWave faces.

**Realism.** Walonoski et al. report disease prevalence within ~5–10 % of CDC figures on top-20 conditions. Downstream studies (Chen 2019, Dube & Gallagher 2020) found classifiers trained on Synthea structured data transfer adequately to structured-field tasks but underperform on narrative tasks.

**Use for Sprint 2.** Use Synthea (or a thin custom replacement) as the **scaffold**: generate ~100 longitudinal NZ-flavoured synthetic patients (problem list, medications, prior labs, demographics), then have the LLM render each inbox document *against* a sampled patient. This grounds reference ranges, units, drug names, and prior context for free, and enables the contextual-reasoning stress items in §4. The Synthea+LLM composition pattern is the dominant 2024–2025 approach in published clinical synthetic-text pipelines.

### 2.2 MIMIC-derived synthetic work — methodology, not content

- **MIMIC-III** (Johnson et al. 2016, *Sci Data* 3:160035) — BIDMC ICU 2001–2012, ~58 k admissions, includes free-text discharge summaries, nursing notes, radiology reports.
- **MIMIC-IV** (Johnson et al. 2023, *Sci Data* 10:1) — restructured, ~300 k admissions 2008–2019, separate MIMIC-IV-Note module for free text.
- **MIMIC-CXR** (Johnson et al. 2019) — 377 k chest X-rays paired with radiology reports.

**Synthetic derivatives.**
- **Asclepius** (Kweon et al. 2023, arXiv 2309.00237) — GPT-3.5 generated synthetic clinical notes from PubMed case reports; Asclepius LLM trained on them. Blinded clinician eval distinguished synthetic from real ~65 % of the time. Methodology directly relevant: persona prompting + structured prompts.
- **Clinical-T5 / GatorTron synthetic notes** (Lehman et al. 2023, *CHIL*) — synthetic discharge summaries generated by fine-tuned T5. Synthetic-to-real transfer was usable for NER but degraded for harder tasks (mortality prediction).
- **Tang et al. 2023** (arXiv 2303.04360, *Does Synthetic Data Generation of LLMs Help Clinical Text Mining?*) — GPT-3.5 synthetic for clinical NER reaches 73–78 % of real-data F1 alone; matches real-data when used as augmentation.
- **NoteChat / Augmented Clinical Notes** — multi-turn synthetic dialogue and structured patient-info augmentation pipelines.

**Lesson for Sprint 2.** The strongest takeaway from the MIMIC line is that **hospital-inpatient style does not transfer to primary care**. BIDMC ICU discharge summaries have a register (cardiology-heavy, US billing, dense acronyms) that does not match what a NZ GP sees in their inbox. The MIMIC line is a methodological template, not a content template.

### 2.3 UK NHS synthetic releases — governance template

- **ONS Synthetic Census / Integrated Data** — tabular only, demographic; uses differential privacy + k-anonymity. Methodologically interesting, no clinical narrative.
- **NHS England Artificial Data Pilot (2021–)** — artificial HES (Hospital Episode Statistics). Structured only. Explicit caveat: "preserves structure and marginals but should not be used for epidemiological inference".
- **CPRD Aurum / GOLD synthetic** — Read/SNOMED-coded GP records, prescriptions, observations. Structured only. **CPRD has not released synthetic free-text consultation notes**, which is the closest analogue to our primary-care need — its absence is informative.
- **OpenSAFELY dummy data** — schema-faithful but statistically naïve fake records for code testing only.

**Lesson.** UK synthetic releases prioritise privacy-preserving statistical analysis, not narrative realism. They are governance templates (datasheet practice, declared utility/risk trade-off) but not content sources.

### 2.4 Named synthetic clinical text projects

- **Ive J et al. 2020** (*npj Digital Medicine* 3:69) — generation and evaluation of artificial mental health records using GPT-2 fine-tuned on CRIS (Clinical Record Interactive Search) data at South London and Maudsley. Downstream NER classifiers trained on synthetic-only reached ~85–90 % of real-data F1. **Methodologically the closest published prior art** to what Sprint 2 is doing.
- **Asclepius** (above).
- **Tang et al. 2023** (above).
- **MEDIQA-Chat 2023** — partially LLM-generated clinician-patient dialogues, clinician-reviewed. Useful methodology reference for the persona-pool and clinician-review-loop pattern.
- **Frei & Kramer 2023** — synthetic German clinical text for NER. Demonstrates cross-lingual viability of the pipeline approach.
- **PMC-Patients** (Zhao et al. 2023, arXiv 2202.13876) — 167 k real patient summaries from PubMed Central case reports. Not synthetic but commonly used as exemplar source for prompt scaffolding.
- **MedAlign** (Fleming et al. 2023, arXiv 2308.14089) — real instructions; methodology paper discusses why synthetic clinical instructions under-represent long-tail care.
- **EHRSHOT** (Wornow et al. 2023, arXiv 2307.02028) — real Stanford EHR benchmark; useful comparator for what "realistic" looks like.

### 2.5 The 2025 Frontiers GPT-4o tabular study — context, not template

The grounding research cited a 2025 *Frontiers* paper reporting GPT-4o zero-shot generation of synthetic tabular perioperative data with 92.31 % statistical parameter similarity. This is a tabular result, not a narrative-text result, and the metric is distributional fidelity not downstream classifier transfer. Useful as evidence that LLM-based clinical synthesis is now taken seriously in peer-reviewed venues; not directly extrapolable to our narrative Inbox Helper case. Borisov et al. 2023 ICLR ("Language Models are Realistic Tabular Data Generators", GReaT) is the established methodological reference for the broader claim.

### 2.6 The published-gap finding — Sprint 2 is filling, not duplicating

**There is no published, downloadable, peer-reviewed synthetic corpus that matches our target.** Specifically:

- No synthetic *primary care inbox* dataset exists.
- No synthetic *NZ-context* clinical text corpus exists.
- No synthetic corpus combines all 5 of our document types under a single ordinal urgency taxonomy.
- The closest analogues (Ive 2020 mental-health records, Asclepius PubMed-derived notes, Clinical-T5 MIMIC-derived discharge summaries) each cover one document type and one institutional context.

This is reassuring: Sprint 2's work is filling a real evidence gap, not duplicating an existing resource. It is also load-bearing for the framing of the R5 deliverable to MBIE — the reason we are generating bespoke synthetic data is that no upstream artefact covers the use case.

### 2.7 Clinical NLP shared task practice — synthetic as augmentation

**n2c2 / i2b2 (2008–present)** — concept extraction, medications, adverse drug events, cohort selection, semantic similarity, social determinants. **No track has used synthetic data as the primary corpus.** Some tracks permit synthetic data for training augmentation; test sets are real de-identified clinical text under DUAs.

**BioCreative / CLEF eHealth / MEDIQA / BioASQ** — primarily real corpora.

**Lesson.** The clinical NLP research community treats synthetic data as an *augmentation* technique rather than a primary evaluation corpus. This is exactly how Sprint 2 should frame it: the synthetic dataset is for *architecture ranking and development*, not for absolute performance certification.

## 3. LLM-Based Generation Techniques

### 3.1 Prompt patterns that produce realistic clinical documents

The 2023–2025 literature converges on a small recognisable stack:

**Few-shot with real exemplars.** 3–10 carefully chosen exemplars in the prompt, covering the stylistic and structural range expected. Van Veen et al. 2024 (*Nature Medicine*, "Adapted large language models can outperform medical experts in clinical text summarization") showed 2-shot beats zero-shot symmetrically for both summarisation and generation. Asclepius (Kweon 2023), Augmented Clinical Notes, and most MIMIC-based pipelines all use 3–8 shot prompts. Zero-shot generation consistently produces more generic, less clinically plausible output. **Critical for our use case:** the exemplars set the *register* — dense vs sparse, abbreviation use, British vs American spelling, formal vs informal — which is what makes the synthetic items feel like real NZ GP inbox traffic rather than ChatGPT prose.

**Chain-of-thought / reasoning scaffolds.** Ask the model to first draft a clinical reasoning chain (presentation → differential → test ordered → finding → urgency rationale) *before* producing the document text. This reliably improves internal consistency, particularly for discharge summaries where history must align with current admission and discharge plan. Use Wei et al. 2022 (*NeurIPS*) for the foundational pattern; Singhal et al. 2023 (*Nature*, Med-PaLM 2) for clinical applicability. **The reasoning trace must not be included in the final document** — it is generation scaffolding only.

**Role / persona prompting.** "You are a senior registrar at Auckland Hospital writing a referral letter to a cardiologist…" — persona prompts shift vocabulary, hedging patterns, and document structure measurably. Persona pools (a library of 20–50 personas varied by specialty, seniority, communication style) are the standard 2024 practice for stylistic diversity.

**Structured JSON-first generation.** Ask the model to output structured JSON (fields: demographics, presenting complaint, investigations, findings, disposition) *before* asking it to render the document text. This forces internal consistency and makes post-hoc labelling tractable. Synthea+LLM composition pipelines use this pattern as standard.

**Constrained generation / guided decoding.** Less common for narrative text (over-constraint produces stilted output) but useful for structured segments — lab panels, medication lists — where JSON mode or grammar constraints enforce format.

### 3.2 Shortcut leakage prevention — the most important section

This is the single highest-leverage decision in the protocol. If shortcut leakage is uncontrolled, Sprint 3 architecture rankings will be meaningless on real data.

**The core failure mode.** If you ask an LLM to generate "an urgent lab result", it produces text containing obvious urgency cues — the literal word "URGENT", bold formatting, exclamation marks, "CRITICAL VALUE" tags, consistent sentence openers. A classifier trained or evaluated on this dataset learns to detect these surface cues, not to reason about urgency. When deployed on real data the surface cues vanish and sensitivity collapses.

**Published evidence.**
- **Gururangan et al. 2018** (NAACL, "Annotation Artifacts in Natural Language Inference Data") — foundational paper on classifier shortcut exploitation. NLI models solved the task by exploiting hypothesis-only artefacts.
- **McCoy et al. 2019** (ACL, "Right for the Wrong Reasons") and **HANS** — BERT solving syntactic heuristics rather than reasoning.
- **Niven & Kao 2019** (ACL) — BERT solving argument reasoning by exploiting word presence.
- **Zech et al. 2018** (*PLoS Medicine*) — chest X-ray classifiers exploiting hospital-site confounders rather than radiological features.
- **Geirhos et al. 2020** (*Nature Machine Intelligence*) — "Shortcut learning in deep neural networks", the synthesising review.
- **Hicks et al. 2022** (*Nature Communications/Scientific Reports*) — directly applies shortcut analysis to medical AI evaluation.
- **Liu R et al. 2024** (arXiv 2404.07503, *Best Practices and Lessons Learned on Synthetic Data for Language Models*) — has a section on shortcut leakage and recommends "label-blind generation".

**Three mandatory shortcut-prevention controls** for Sprint 2:

1. **Label-decoupled generation.** Do **not** give the generator the urgency label. Instead, prompt for *clinical scenarios* (presentations, test results, discharge contexts) parameterised by clinically meaningful inputs (e.g. "patient with potassium 6.8 mmol/L, 5 days post-discharge, on ACE inhibitor + spironolactone"). Have a *separate* labelling step assign urgency after the fact. The urgency becomes a *consequence* of the parameters, not an input to generation. This is the single most effective shortcut-prevention technique and directly enables contextual-reasoning stress items.

2. **Style normalisation pass.** Run every generated document through a second LLM pass with the prompt "rewrite this in a neutral clinical register without changing any facts, numbers, dates, names, or medical content". This strips overt urgency cues ("URGENT!!", "CRITICAL VALUE", "STAT") while preserving the underlying clinical data. Validate against a fact-preservation check (any numeric value or named entity present in the original must be present in the rewrite).

3. **TF-IDF/bag-of-words back-classification check.** Before handing the dataset to Sprint 3, train a simple linear bag-of-3-grams classifier on the synthetic dataset. If it achieves above ~70 % accuracy on urgency classification (or macro F1 above ~0.65 on n-gram features), the corpus has leaked shortcuts and affected items must be regenerated. This is expensive but it is the gold-standard catch-all.

**Optional but recommended fourth control** if budget allows:

4. **Counterfactual / contrast pair generation.** For each clinical scenario, generate multiple documents at different urgency levels by changing only the *clinically relevant* parameter (potassium 6.2 → 5.8; symptom onset 2 hours → 2 days; on-warfarin AF → on-warfarin mechanical valve). The classifier is forced to attend to the clinical change, not surface style. Gardner et al. 2020 (EMNLP Findings, *Evaluating Models' Local Decision Boundaries via Contrast Sets*) is the methodological foundation.

### 3.3 Stylistic variation — preventing GPT monotone

The "GPT monotone" problem (Padmakumar & He 2024 ICLR; Shaib et al. 2024) — LLM outputs trending toward a characteristic voice regardless of persona — is well documented and worsens with larger models. Practical countermeasures, ranked by leverage:

1. **Multi-model ensemble.** Use ≥2 frontier model families (e.g. Claude Sonnet 4.6 + GPT-4o or Gemini 2.5) for different items in the dataset. Each model has a different monotone; mixing them prevents any single one dominating. **This is the highest-leverage diversity technique with the lowest implementation cost.** Since the Sprint 3 evaluation candidates may include Claude family models, the dataset *must* be mixed-family to avoid the generator-classifier coupling failure mode (§9.2).

2. **Persona pools.** ≥30 author personas (senior GP, junior registrar, locum, specialist, nurse, ED registrar, geriatrician, paediatrician, etc.) crossed with ≥5 communication styles (terse-telegraphic, verbose-prose, hedging-heavy, bulleted, dictation-flavoured). Sample one persona per item.

3. **Style exemplar injection.** 1–2 real-style reference snippets from a pool of 20+, sampled randomly per generation call. Forces style variation without retraining.

4. **Temperature scheduling.** 0.9–1.1 for narrative segments; 0.3 for structured fields; 0.7 for paraphrase passes.

5. **Structural template randomisation.** 3–10 structural templates per document type (impression-before-findings vs after; bulleted vs paragraph; H&P first vs investigations first). Sample weighted by realistic prevalence.

6. **Abbreviation/expansion post-processing.** Random expansion or contraction of medical abbreviations (BP ↔ blood pressure, BNP ↔ brain natriuretic peptide, ix ↔ investigations, r/v ↔ review). Real clinicians are inconsistent; synthetic data should be too.

7. **Paraphrase chains.** Generate → paraphrase with different model → commit. Each paraphrase pass removes a layer of generator-specific style. Risk: fact drift — must run a fact-preservation check after each pass.

8. **Length variation.** Sample document length from a log-normal fit per document type. Real clinical documents have heavy-tailed length distributions; uniform-length synthetic data is a tell.

9. **Noise injection.** Deliberate typos, incomplete sentences, missing punctuation, copy-paste artefacts at controlled rate (~5–15 % of items). Especially important for patient portal messages.

### 3.4 Ambiguity and borderline-case injection

Borderline items are the most valuable in a recall-optimised dataset because they determine where the Immediate/Urgent boundary sits. Published techniques:

**Counterfactual / contrast set generation.** Gardner et al. 2020 (above). For Sprint 2: take an Urgent lab item, change one parameter (potassium 6.2 → 5.8 takes it Routine; onset "2 days ago" → "2 hours ago" takes it Immediate) and re-label.

**Controlled parameter sweeps.** Generate the same scenario at potassium ∈ {5.0, 5.5, 6.0, 6.5, 7.0}, have the clinician label each. Items clustered around the decision boundary become the borderline subset. This is an adaptation of adversarial-ML controlled-input techniques.

**Red-team prompting.** Explicitly prompt: "Generate a case that looks routine on the surface but where a cautious GP would escalate." Then ask a separate LLM: "Is this obviously urgent?" — if yes, reject. Iterate until generator produces genuinely ambiguous items. Used by MedHELM (Stanford HAI 2024) for evaluation set construction.

**Constraint relaxation.** Start from a fully-specified urgent template, relax constraints one at a time (drop the flag word, drop the explicit number, drop the temporal marker) to create a gradient of urgency-legibility.

### 3.5 Training-data leakage prevention

LLMs have seen MIMIC-III (publicly accessible via credentialed access; some fragments leak into web crawls), PubMed case reports, patient forums, and possibly de-identified clinical text. Generated "synthetic" text might be near-copies of training data — contaminating the dataset and potentially leaking real patient information.

**Mandatory controls.**

1. **Anti-memorisation prompting.** "Do not reproduce any real patient case. Use fabricated names, dates, locations, and invented combinations of findings." Reduces but does not eliminate leakage.

2. **Near-duplicate detection against known corpora.** Run MinHash/LSH against PMC Open Access (and MIMIC-III if credentialed access is available). Discard items with MinHash Jaccard >0.8 or embedding cosine >0.92. Lee et al. 2022 (ACL, *Deduplicating Training Data Makes Language Models Better*) is the methodological reference.

3. **Identifier randomisation.** Names, dates, NHIs, ages, doses randomised post-generation (see §6).

4. **NZ-context anchoring.** Every generation prompt anchors context in NZ GP practice (NHI placeholder, NZ medications, NZ specialist referral patterns, Pharmac-subsidised drug list). Out-of-domain US hospital discharge idioms get flagged and regenerated. This mitigates US training-data leakage at the source.

**Citations.** Carlini et al. 2021 (USENIX Security, *Extracting Training Data from Large Language Models*); Carlini et al. 2023 (ICLR, *Quantifying memorization across neural language models*); Lehman et al. 2021 (NAACL, *Does BERT Pretrained on Clinical Notes Reveal Sensitive Data?*).

### 3.6 Contextual reasoning stress design

This is the highest-value generation technique for our use case given the **NHS GPT-oss-120b primary care medication review study** (arXiv 2512.21127, Oct–Nov 2025) finding that contextual-reasoning failures outnumber factual errors approximately **6:1**. The synthetic dataset must specifically stress-test contextual reasoning, not just factual recall.

**Methodological foundations.**
- **Multi-document reasoning.** HotpotQA, 2WikiMultiHopQA, MuSiQue (Trivedi et al. 2022) — combine info from multiple documents where no single document reveals the answer.
- **Temporal reasoning.** TempReason (Tan et al. 2023, ACL), TimeQA — clinical context is heavily temporal ("3 days post-discharge", "started last week"), and LLMs are documented to be weak on implicit temporal reasoning.
- **Long-context distractor work.** Liu et al. 2024 (TACL, *Lost in the Middle*) — relevant because real inbox items embedded in a stream have distractors.
- **Behavioural testing.** Ribeiro et al. 2020 (ACL, CheckList) — invariance tests, directional tests, minimum functionality tests. Adapt this template for clinical urgency.
- **Stress-test NLI.** Naik et al. 2018 (COLING) — generation of perturbation-based stress items.

**Six concrete techniques for generating context-stress items:**

1. **Parameter layering.** Start with a benign primary document (potassium 5.6 — mildly raised). Add a separately-generated context layer (discharge summary 4 days ago, on ACE inhibitor + spironolactone, eGFR 45). The combination is Urgent; the primary alone is not. The generator produces each layer independently; the labeller confirms combined urgency from the context block.

2. **Timeline drift scenarios.** Document dated today, references events "last week" that should have triggered review. Easy for a clinician with full timeline; hard for a classifier looking at the current item alone.

3. **Medication interaction scaffolds.** Library of known interaction pairs (warfarin + antibiotic, ACE + K-sparing diuretic, SSRI + triptan, statin + macrolide). Generate scenarios where the current document reveals one side of the pair and the patient context reveals the other. Directly reproduces the NHS GPT-oss-120b failure pattern.

4. **Comorbidity shadows.** Patient has stable T2DM. Current lab: HbA1c 68 — Routine on its own. Context: on dapagliflozin, recent UTI, presenting with malaise. The combination escalates (DKA risk).

5. **Narrative-vs-structured contradiction.** Item where the narrative says "patient clinically stable" but structured values say HR 128 / BP 88/54 / lactate 3.2. Real clinical text is full of these contradictions; classifiers must learn to weigh evidence.

6. **Counterfactual contrast pairs.** For each context-stress item, generate a near-identical item where the context element is absent (patient is NOT on ACE + K-sparing). This pair classifies as routine. Contrast pairs are the cleanest demonstration that a classifier is using context rather than surface features.

**Stress-item dosage.** Target 15–20 % of the dataset (60–80 items of 400) flagged `contextual_reasoning_stress=true`. This is lower than the NHS 6:1 failure ratio because stress items are expensive to construct and because a 15–20 % dose is sufficient (a) to discriminate architectures that retrieve context vs those that don't and (b) to generate per-item "context-required" tags for Sprint 3 error analysis. Each stress item carries a minimal `patient_context` block (medications, problem list, age, recent results) so retrieval-augmented architectures can use it and naïve architectures will fail on those items. **Whether an architecture can use the context block is itself a useful Sprint 3 discriminator.**

## 4. Stratification Protocol

### 4.1 Two-track design — enriched dev set + natural-prevalence holdout

The dominant pattern in published clinical NLP evaluation (n2c2, MIMIC-III triage work — Horng et al. 2017, Sterling et al. 2019; ED triage ordinal classification — Raita et al. 2019 *Critical Care*; primary-care inbox — Apathy et al. 2024 *JAMIA*) is a two-track design:

1. **Training/development split** — stratified and *enriched* for minority classes. Natural prevalence of critical events is typically 1–5 %, so a naturally-sampled set gives the model almost no Immediate exemplars to learn from.
2. **Holdout test split** — sampled at or near natural prevalence. Used to estimate real-world PPV/NPV and calibration.

Apathy et al. 2024 explicitly used an enriched development set (roughly balanced across 5 categories) for model tuning but reported deployment metrics against a naturally-distributed primary-care inbox stream. Rotenstein et al. 2025 (*JAMA Network Open* on EHR inbox burden) follows the same pattern. The rationale, most clearly articulated in Park & Han 2018 (*Radiology*, *Methodologic Guide for Evaluating Clinical Performance and Effect of AI*), is that **training prevalence and deployment prevalence are separate design choices**, and conflating them produces either starved minority learning or inflated headline accuracy.

**For the recall-optimised ordinal setting:**

- **Sprint 2's 400 items are the enriched split.** Their job is to teach Sprint 3 candidate architectures to recognise Immediate/Urgent patterns and to compute macro-F1 under a minority-friendly prevalence.
- **The Sprint 4 natural-prevalence holdout (300–500 items) is where PPV, NPV, and calibration metrics come from.** Buderer's formula (already documented in the internal eval-metrics doc) sizes that holdout for a ±5 % CI on Immediate sensitivity at π = 0.02–0.05.

This two-track separation is consistent with the existing Sprint 2 / Sprint 4 scoping in the obj-1 roadmap.

### 4.2 Minority-class representation without distorting the learned prior

Three published techniques are relevant:

1. **Stratified oversampling with prior re-calibration** (Apathy 2024, Horng 2017). Works well but the inflated training prior must be corrected at inference — Platt scaling or post-hoc prior-shift (Saerens et al. 2002 *Neural Computation*, *Adjusting the outputs of a classifier to new a priori probabilities*). For an LLM prompt-based classifier this is implemented by calibrating decision thresholds on the natural-prevalence holdout.

2. **Class-balanced loss** (Cui et al. 2019 *CVPR*) or ordinal focal loss (Cao et al. 2020 extension of Lin et al. 2017). Only applies if a fine-tuned small model is one of the Sprint 3 candidates; not applicable for zero-shot LLM evaluation.

3. **Cost-sensitive thresholding** — decision thresholds tuned so that false negatives on Immediate cost ~10× a false positive. Natural match for the recall-optimised setting and explicitly supported by the ≥99 % sensitivity target.

**Recommendation.** Use (1) stratified oversampling for Sprint 2, document the training prior explicitly in the datasheet, and apply (3) threshold tuning on the Sprint 4 holdout. This matches published practice and avoids baking distortion into the model itself.

### 4.3 Spectrum bias — clear-cut vs borderline proportions

Spectrum bias (Ransohoff & Feinstein 1978 *NEJM*; updated by Whiting et al. 2004 *Annals*; applied to AI by Park & Han 2018 *Radiology* and Hicks et al. 2022) is the phenomenon where a model evaluated only on clear-cut positives and clear-cut negatives reports near-perfect sensitivity/specificity that collapses in deployment when borderline presentations dominate. Hicks et al. 2022 recommend explicit difficulty stratification — clear / moderate / hard — with at least 25–35 % in the hard band. Apathy et al. 2024 found ~20 % of their inbox messages were genuinely ambiguous on second read.

**Recommendation.** Target **30 % borderline items per cell** (urgency × document type), flagged `difficulty: borderline`. For Immediate class specifically, borderline items are the most valuable — chest pain that could be MSK vs ACS, potassium of 5.9 (just below the 6.0 cutoff), patient message describing headache with just enough red-flag features to need second thought. These are precisely where the ≥99 % sensitivity target is won or lost. Within each cell, target shape is roughly: 50 % clear, 30 % moderate/borderline, 20 % hard (including the contextual-reasoning stress items where applicable).

### 4.4 Document-type balance and the portal "urgent tail" problem

NZ patient portals (ManageMyHealth, MyIndici, ConnectMed) deliberately steer patients away from urgent issues — the standard banner is "If this is urgent please call the practice or 111". Consequently the natural portal stream contains <1 % true Immediate items (Rotenstein et al. 2025; Honeyford et al. 2020 UK NHS primary-care inbox studies).

The synthesis problem: if portal messages are sampled at natural prevalence, the classifier never sees a portal Immediate item, and deployment fails catastrophically when the rare portal red-flag arrives ("my chest has been hurting since last night and I'm sweaty"). The published fix (Apathy 2024; Zech et al. 2018 on domain shift) is **synthetic upsampling of the rare tail within the document type**, clearly flagged in metadata so the training prior isn't contaminated.

**Recommendation.** In the enriched 400-item Sprint 2 set, allow portal messages to contain 3 Immediate items and 10 Urgent items (10–20× natural prevalence). Flag these as `enriched_tail: true` so Sprint 3 can compute both enriched metrics and prior-corrected metrics.

### 4.5 Recommended stratification table — 400 items

| Document type | Immediate | Urgent | Routine | Info only | **Row total** |
|---|---:|---:|---:|---:|---:|
| Lab results (HL7) | 8 | 20 | 40 | 12 | **80** |
| Radiology reports | 7 | 18 | 35 | 20 | **80** |
| Discharge summaries | 5 | 15 | 40 | 20 | **80** |
| Specialist letters | 2 | 12 | 45 | 21 | **80** |
| Patient portal messages | 3 | 10 | 20 | 47 | **80** |
| **Class total** | **25** | **75** | **180** | **120** | **400** |

**Overlays:**
- **Borderline items: 30 % per cell**, flagged `difficulty: borderline`.
- **Contextual-reasoning stress items: 15–20 % overall (60–80 items)** distributed across classes with over-weighting on Urgent and Immediate (about half of the stress items land in those two top classes).
- **Ethnicity enrichment** per §6.6 (Māori 20 %, Pacific 12 %).

**Rationale for the class shape.**
- **Immediate held to 25** because (a) Buderer sizing for ≥99 % sensitivity is delivered by the Sprint 4 holdout, not Sprint 2; (b) 25 is the minimum needed for per-document-type sensitivity sanity-checking at this stage; (c) Immediate items are the most expensive to write realistically and require the most careful clinical judgement. Per Section 8 / G4, ≥15 Immediate items is the floor for detecting catastrophic classifier failures; 25 gives modest headroom.
- **Urgent at 75** — large enough for stable macro-F1 contribution and meaningful per-document-type sensitivity estimation.
- **Routine at 180** — the natural mode; the model needs to learn the baseline signal.
- **Info only at 120** — balances against the risk of "everything looks routine" classifier bias.
- **Patient portal Immediate = 3** is deliberately low (portals are directed away from urgent issues) but non-zero — models the rare red-flag tail.

### 4.6 Stratum identifier and metadata

Each item carries a `stratum` field encoding (doc_type × urgency × difficulty × contextual_reasoning_flag × ethnicity_group) so Sprint 3 can compute stratified metrics directly without re-deriving from the JSONL. This also enables targeted re-generation of cells that fall short during the Day 2 / Day 7 / Day 11 gates.

## 5. Labelling Protocol with IRA and Adjudication

### 5.1 Single-annotator defensibility

Published practice draws a clean line:
- **n2c2 / i2b2 shared tasks** use dual annotation + third-annotator adjudication. Gold standard for benchmark leaderboards.
- **Operational clinical NLP development sets** (Apathy et al. 2024; Rotenstein et al. 2025; Garcia et al. 2024 on ambient scribe evaluation) routinely use single expert annotators for initial development sets, provided (a) the annotator is the domain authority, (b) a calibration subset is double-annotated or self-re-annotated blind, (c) the limitation is transparently disclosed in the datasheet.

The published threshold: **single annotation is acceptable for development sets if you can report quadratic-weighted Cohen's κ ≥0.75 on a calibration subset**, and the limitation is documented. For Sprint 2 with one GP annotator (Ryo, ~60 h budget over 2 weekends + evenings), single annotation is defensible *provided* the calibration mechanism in §5.4 is in place.

### 5.2 Inter-rater agreement targets for ordinal urgency

Published benchmarks for ordinal clinical labels (ED triage, inbox urgency, radiology BI-RADS):

| Metric | Floor (publishable) | Good | Excellent |
|---|---|---|---|
| Quadratic-weighted Cohen's κ | ≥0.60 | ≥0.75 | ≥0.85 |
| Linear-weighted κ | ≥0.55 | ≥0.70 | ≥0.80 |
| % exact agreement | ≥65 % | ≥75 % | ≥85 % |
| % within-1-level agreement | ≥90 % | ≥95 % | ≥98 % |

**Sources.** Landis & Koch 1977 (foundational κ interpretation, descriptive use); Cicchetti 1994 (clinical κ standards); Hripcsak & Rothschild 2005 (*JAMIA*, agreement and reliability in IR); Raita et al. 2019 on ED ordinal triage (reported physician-physician weighted κ ~0.72); Mistry et al. 2018 reviewed ESI triage inter-rater κ in the 0.5–0.8 range; Apathy et al. 2024 reported κ 0.71 on their 5-class inbox schema.

**Recommendation.** Target **quadratic-weighted κ ≥0.75** on the calibration subset across rounds 1, 2, 3. Floor of 0.65 triggers a re-calibration meeting; below 0.60 requires the affected cells to be relabelled.

### 5.3 Adjudication protocol for disagreements

Three published patterns:
1. **Third-reviewer adjudication** (n2c2, i2b2) — gold standard, requires a third clinician.
2. **Consensus discussion** (Apathy 2024, MEDIQA-Chat) — annotators discuss to agreement; unresolved items flagged rather than forced.
3. **Automated flag + deferred review** — items where the annotator's confidence is low or where calibration drift exceeds threshold are re-reviewed.

**Sprint 2 single-annotator adaptation.** Modified consensus pattern:
- Any item where Ryo's `confidence` field is "low", OR where blinded re-annotation on calibration golden re-checks gives a different label, is moved to a `disputed/` folder.
- Sprint 3 architectures are evaluated **twice** — once with disputed items included at Ryo's best-guess label, once with disputed items excluded. If headline metrics diverge materially, disputed items are adjudicated in Sprint 4 by a second GP (Brendan Duck or Heidi Bubendorfer per the Sprint 1 outreach list).
- The proportion of disputed items is itself reported as a quality signal.

### 5.4 Calibration set for intra-rater drift

With a single annotator there is no *inter*-rater agreement. The risk is **intra-rater drift** — the GP interpreting "Urgent" differently on Day 14 than Day 1 as familiarity grows and fatigue accumulates. The calibration set is the standard published mitigation (Hripcsak & Rothschild 2005; Wilbur et al. 2006 BioCreative-era practice).

**Method.**

1. **Day 2 morning** — label 25 items as the calibration seed. Diverse across urgency × doc_type, including 5–7 deliberately borderline items.
2. **Day 7 evening (Sun 19 Apr)** — re-label the same 25 items, **blinded** (labels stripped, order randomised, identifying header metadata hidden). This is calibration round 2.
3. **Day 13 evening (Sat 25 Apr)** — re-label again, blinded. Calibration round 3.
4. **Compute** Cohen's quadratic-weighted κ between each pair of labelling rounds (R1↔R2, R2↔R3, R1↔R3). Also compute item-level stability: % of items with unchanged label across all three rounds.

**Pass criterion.** κ ≥0.75 for all three pairwise comparisons. Result <0.75 between R1 and R3 triggers full re-labelling of drift-affected cells. Moderate drift (0.60–0.75) triggers a rationale-review pass only. <0.60 is a Gate 3 RED.

**Bridge function.** The calibration set also serves as the **taxonomy bridge** if the Sprint 1 GP review (rd-20260405-001 due Day 8 Mon 20 Apr) refines the urgency taxonomy. Ryo relabels the 25 items under the new taxonomy first; the pre-post label agreement measures how much the taxonomy shift affects labels and informs targeted re-label scope.

### 5.5 Time budget per item

Published annotation rates:

| Task type | Reported rate | Source |
|---|---|---|
| n2c2 concept span (NER) | 1–3 min/document | Stubbs & Uzuner 2015 |
| i2b2 smoking status classification | 1–2 min/note | Uzuner et al. 2008 |
| Radiology report categorical labelling | 1–3 min/report | Irvin et al. 2019 (CheXpert) |
| Inbox message 5-class urgency | 2–4 min/message | Apathy et al. 2024 |
| Free-text discharge summary full review | 8–15 min | Stanford ambient scribe eval 2024 |
| Ordinal ED triage with borderline adjudication | 5–10 min | Raita et al. 2019 |

Sprint 2's task is at the harder end — five document types including long discharge summaries; contextual-reasoning items require reading the patient context block; ordinal judgement with 30 % borderlines forces re-reads; the annotator must record confidence and borderline reason.

**Available time.** Ryo: ~30 h/weekend × 2 weekends + evenings ≈ 60 h. At 400 items: **~9 minutes/item weighted average**. Realistic finer breakdown:
- Short items (lab HL7, short portal messages): 3–5 min
- Medium items (radiology reports, specialist letters): 7–10 min
- Long items (discharge summaries, contextual-reasoning stress items): 12–15 min

**Two-pass strategy** (per R5-C):
- **Pass 1 (first-look labelling)**: ~2 min/item, all 400 items, ~13.3 h
- **Pass 2 (reconciliation/adjudication on flagged ~20 %)**: ~5 min/item × 80 items, ~6.7 h
- **Calibration relabelling**: 3 × 25 items × ~2 min, ~2.5 h
- **QA reviews, end-of-day check, sprint ceremonies, buffer**: ~10 h

Total: ~32 h GP labelling + reconciliation + calibration. Comfortably within the 60 h budget with ~25 h headroom for taxonomy refinement after Day 8.

**Guardrail.** If pass 1 consistently exceeds 11 min/item in week 1, drop the target set size to 320 at Gate 2 and re-plan rather than compromise label quality. This is an explicit Sprint 2 quality-over-quantity trade-off.

### 5.6 Drift-prevention QA cadence

Published techniques (n2c2 practice + Hripcsak & Rothschild 2005):
1. **Calibration set pre-annotation** — annotator labels ~25 items from a pre-built golden set, discusses with PM (Ting), re-labels.
2. **Periodic golden re-check** — at the start of each labelling day, annotator re-labels 5 items from the previous day, blind. Drift detected if ≥1 level disagreement on >10 % of items.
3. **End-of-day review** — structured 15-minute review of low-confidence items.
4. **Sprint-midpoint calibration** — Day 7 full calibration round 2 (above).

All four are recommended. Budget 3–4 hours of the 60 for QA (within the Section 5.5 budget).

### 5.7 Borderline case flagging — schema

Each labelled item carries:

```yaml
gold_label_urgency: immediate | urgent | routine | information_only
gold_label_rationale: ""           # required, GP's 1–2 sentence justification
gold_label_secondary: null         # alternate label considered if borderline
confidence: high | medium | low
difficulty: clear | moderate | hard
boundary_case_flag: true | false
borderline_reason: ""              # required if difficulty != clear
contextual_reasoning_stress_flag: true | false
contextual_reasoning_required: true | false
second_look: true | false          # flag for post-hoc review
labelling:
  labelled_by: ryo
  labelled_at: <iso>
  pass_number: 1
  taxonomy_version: sprint1-v2
  relabelled_at: null
  relabel_reason: null
```

`second_look: true` items are explicitly re-reviewed at sprint midpoint and end. The `borderline_reason` text is a direct input to Sprint 3 error analysis. The `gold_label_secondary` field captures the alternate label considered (especially for "when in doubt, label up" cases) and is valuable for threshold calibration in Sprint 3.

### 5.8 "When in doubt, label up" — recall-optimised labelling convention

Published convention from Apathy 2024 and the ambient-scribe evaluation literature: in recall-optimised labelling, **when in doubt, label up**. If an item is genuinely ambiguous between Routine and Urgent, the annotator labels Urgent. This aligns the label distribution with the downstream cost structure (over-triage is acceptable; under-triage is not). Codify as an explicit instruction at the top of the annotation guide. The annotator should record the alternative label considered in `gold_label_secondary`.

## 6. Privacy-Safe NZ Generation Techniques

The synthetic dataset is destined for a private NexWave R&D repo, but it must still be obviously, defensibly, irreversibly synthetic — for MBIE audit, for downstream Sprint 3 reproducibility, and so any accidental leakage cannot misidentify a real NZ patient. The conventions below combine the published "obviously synthetic" standards (UK ICO 2023, NHS England 2022, NIH/NIAID 2022, Mitre Synthea) with NZ-specific identifier rules (HISO 10046).

### 6.1 Obviously synthetic identifiers

Every item must satisfy *at least one* obviously-synthetic axis (UK ICO 2023 *Anonymisation, pseudonymisation and PETs — Synthetic data*; NHS England 2022 *Synthetic Data Strategy*; Mitre Synthea conventions). For this dataset, we enforce all of them:

- **Names** drawn from a fixed, documented, intentionally-fictional pool of 30 surnames and 30 first names (e.g. Testalot, Synthwell, Mockford, Stubbsby, Vaultson, Patientsmith). Every patient also carries `TEST` as a middle name so a single grep on the dataset reveals every name occurrence. Te Reo placeholder names are permitted only when cross-checked against MCNZ and te ao Māori public-figure registers; when in doubt, default to the European synthetic pool.
- **GP and specialist names** drawn from the same pool, with fictional fellowship qualifications (Dr T. Synthwell FRACP, Dr M. Mockford FRANZCR). One-time Ting task before generation: grep the synthetic-name pool against the public Medical Council of NZ register and discard any incidental collisions.
- **Practice and hospital names** are obviously synthetic (`Synth Medical Centre`, `Testville Health`, `Mockton Family Practice`, `Synth Hospital`). Real DHB / Te Whatu Ora district names may appear as a region label (`Canterbury`, `Waikato`) only in combination with a synthetic facility name; never reproduce a real facility name.
- **Addresses** use fictional suburbs (`Synth Bay`, `Testville`, `Mockton`) with no street number or street name, plus a real region label.
- **Dates of birth** are uniformly sampled within the age band the clinical scenario requires; never copy a real DOB.
- **Phone numbers** use the convention `02X 555 XXXX` with a clearly invalid prefix (NZ has no formal Ofcom-style drama range, but the `555` block is widely used in QA pipelines).

### 6.2 NZ NHI format and synthetic NHI generation

Authoritative reference: **HISO 10046:2023 Consumer Health Identity Standard**, Te Whatu Ora / Health NZ Digital. Two formats coexist:

- **Legacy NHI** — 3 alpha + 3 numeric + 1 check digit = 7 characters (e.g. `ABC1234`). Allowed letters exclude `I` and `O`. Check digit is mod-11 over the position-weighted sum of letters-as-numbers + numerics.
- **New NHI** (rolling out since 2019 as legacy space fills) — 3 alpha + 2 numeric + 2 alpha = 7 characters (e.g. `ABC12DE`). Same letter exclusions, mod-24 check character on the trailing alpha.

The published HL7 NZ / FHIR NZ test convention is to use NHIs that **cannot collide with real NHIs** by deliberately violating one structural rule. We adopt the strongest available form of this convention:

1. **Reserved synthetic prefix `ZZI` or `ZIO`.** Both prefixes use the HISO-excluded letters `I` and/or `O`, which means *no real NHI can share the prefix*. Synthetic NHIs are guaranteed-orthogonal to the real allocation space.
2. **Compute the structurally-correct check digit.** Items still parse cleanly through any HL7 v2.4 NHI validator a Sprint 3 candidate pipeline might apply, so structural-validation gates do not falsely fail.
3. **Document the convention** in the dataset README and embed it in the schema as a `nz_context.nhi_placeholder` field; downstream PII scanners look for the `ZZI`/`ZIO` prefix as a positive synthetic marker, not a violation.

A small NHI generator (`tools/nhi.py` in nexwave-rd, with unit tests for prefix invariance, format validity, and non-collision against a precomputed exclusion list) is committed to the repo, *not* the vault.

### 6.3 Avoiding identifying lab values

Singleton or "landmark" combinations of rare lab values can re-identify real patients even without names (Sweeney 2000 k-anonymity argument; Ohm 2010 *Broken Promises of Privacy*; Rocher et al. 2019 *Nature Communications*). Mitigations:

- **Round to standard clinical granularity**: HbA1c to whole mmol/mol, sodium to whole mmol/L, creatinine to nearest 5 µmol/L above 100, eGFR to integer mL/min/1.73m².
- **Jitter within clinically meaningful bounds**: chemistry ±3 %, INR ±0.05, HbA1c ±1 mmol/mol. Jitter is applied *after* the generator emits the value, before the QA gate.
- **Ban outlier stacking**: do not combine two or more 99th-percentile values on the same synthetic patient unless the Synthea-scaffolded scenario clinically demands it.
- **Use published NZ reference distributions** (BPAC NZ, NZSSD diabetes targets, Awanui / LabPLUS / Pathlab public reference range PDFs) — never sample from real cohorts.
- **Reference-range plausibility gate (G9)** rejects any out-of-range numeric in the QA pass.

### 6.4 Published "obviously synthetic" standards we are aligning with

- **UK ICO (2023)** — *Anonymisation, pseudonymisation and PETs — Chapter on synthetic data*. Recommends synthetic data be "obviously distinguishable from real data on at least one axis" (identifier, date, value range, or explicit metadata flag). Our dataset is distinguishable on multiple axes simultaneously.
- **NHS England (2022)** — *Synthetic Data Strategy* (and the *Data Saves Lives* programme). Endorses Mitre Synthea conventions for AI-training synthetic clinical text.
- **NIH / NIAID (2022)** — *Synthetic Data Playbook*. Recommends documented synthesis processes and declared statistical distance from any real dataset.
- **Mitre Synthea** — published "obviously synthetic" principles: fictional place names, declared synthetic markers, fake-SSN convention `999-99-9999` (analogous to our `ZZI*`/`ZIO*` NHI prefix).
- **NZ Office of the Privacy Commissioner** — has published *Artificial intelligence and the Information Privacy Principles* (2023, updated 2024). The 2023 guidance notes that synthetic data which cannot be re-identified is not personal information under the Privacy Act 2020, *but stresses that the generation process must not rely on real personal information in a way that creates a residual re-identification risk*. **No NZ-specific synthetic-data guidance was published as of training cutoff** — Ting to verify against opc.org.nz before the R5 deliverable ships.
- **Te Whatu Ora / HISO** — HISO 10029 (Health Information Security Framework) and HISO 10064 (Health Information Governance Guidelines) cover de-identification but no synthetic-data-specific standard. **Ting to verify.**
- **NEAC (2022)** — *National Ethical Standards for Health and Disability Research and Quality Improvement* — relevant for the Māori data sovereignty framing in §7.7.

### 6.5 NZ-sovereign generation pathway

The MBIE R&D grant clause **"R&D undertaken outside New Zealand is not eligible"** constrains compute location, not just researcher location. Synthetic data generation is R&D activity. There are four possible compute pathways and only two of them are MBIE-defensible:

| Pathway | Sovereignty | Recommendation |
|---|---|---|
| AWS Bedrock `ap-southeast-2` Sydney | **Not NZ-sovereign.** Ineligible. | **Do not use.** |
| AWS Bedrock `ap-southeast-6` Auckland (live since March 2026) | NZ-sovereign. Closed-frontier Claude models (Sonnet 4.6, Haiku 4.5) when natively available. | **Acceptable fallback** if and only if Claude Sonnet 4.6 is confirmed natively available in `ap-southeast-6` (not just cross-Region routed). Verify on Day 0. |
| Catalyst Cloud Wellington / Porirua (NZ-owned, NZ-operated, NZ-engineered) | **Strongest sovereignty.** Open-weights models (Llama 3.1/3.3 70B, Mistral Large, Qwen 2.5, GPT-OSS-120B) on A100 80GB slices, L40S 48GB, or A6000 48GB. | **Primary recommendation.** Unambiguously NZ-sovereign. Avoids the Bedrock NZ availability uncertainty entirely. Trade-off: open-model quality ceiling. |
| Local / on-prem GPU at NexWave office | NZ-sovereign by definition. | Only viable if a sufficient GPU is available; currently unlikely. |

**Recommendation**: default to **Catalyst Cloud Wellington with Llama 3.3 70B Instruct** as the primary generator, with AWS Bedrock `ap-southeast-6` Auckland (Claude Sonnet 4.6) as documented fallback if open-model output quality on Catalyst proves insufficient on Day 1 smoke tests. **Never use Bedrock Sydney, OpenAI, the direct Anthropic API, or any other non-NZ endpoint, even for "just testing"** — provenance contamination is hard to reverse and the grant audit risk is asymmetric.

Every generated item carries a `generator` block in the JSONL schema (see §10.5) with `model`, `provider`, `region`, `prompt_template_id`, `prompt_hash`, `temperature`, `generated_at`, and `paraphrase_pass` — both for reproducibility and for MBIE audit.

## 7. NZ Clinical Realism by Document Type

The dataset's claim to evaluation utility rests on producing items a NZ GP would recognise as genuine inbox arrivals. The realism axis is *NZ-flavoured* — NZ units, NZ lab providers, NZ DHB / Te Whatu Ora discharge conventions, NZ specialist college templates, NZ patient portal styles, and NZ-specific clinical phrasing. The conventions below are the floor; per-batch QA inspection by Ryo at Gate 1 (Day 2) will catch idiom failures the prompts miss.

### 7.1 Lab reports

**Format anchor.** HL7 v2.4 ORU^R01 is the dominant NZ lab-to-practice messaging standard, governed by **HISO 10040.2** (NZ HL7 Messaging Standard). A minimal synthetic lab report contains MSH (sending facility, receiving practice, timestamp), PID (synthetic NHI per §6.2), OBR (test panel code and name), and OBX rows (one per analyte: value, units, reference range, abnormal flag H/L/HH/LL/A). PMS parsers (Medtech32, Medtech Evolution, Indici, MyPractice) render the OBX rows as the "lab result" the GP sees in the inbox.

**NZ unit conventions** (anchored to HISO-approved LOINC NZ subset and NZ Lab Handbook):

- Chemistry — mmol/L (Na, K, urea, glucose, Ca, Mg, phosphate, lactate, bicarbonate, lipids).
- Creatinine — **µmol/L**, never mg/dL.
- eGFR — mL/min/1.73 m² (CKD-EPI 2021 race-free; Awanui adopted in 2022, LabPLUS followed).
- HbA1c — **mmol/mol** (IFCC primary; DCCT % may appear as secondary). Reference <41; T2D diagnosis ≥50; "poor control" ≥65.
- Haematology — Hb in **g/L** (not g/dL), MCV fL, MCH pg, WCC and platelets ×10⁹/L.
- TSH mIU/L; free T4 / T3 pmol/L; INR dimensionless.
- High-sensitivity troponin in ng/L (Abbott hs-TnI 99th percentile ~26 male / 16 female; Roche hs-TnT ~14). NZ ACS pathways follow Cardiac Society of Australia and NZ guidelines.
- Microbiology — urine culture in CFU/mL with sensitivities to NZ-common antibiotics (trimethoprim, nitrofurantoin, amoxicillin-clavulanate, cefalexin).

**NZ lab providers** (use 2–3 templates per the Sprint 2 budget rather than all five):

- **Awanui Labs** (formerly Southern Community Laboratories — SCL — rebranded 2022; absorbed Labtests Auckland). Dominant lower North Island, South Island, and parts of Auckland.
- **Pathlab** — Bay of Plenty / Waikato / Lakes.
- **LabPLUS** — Te Toka Tumai Auckland public hospital lab.
- **Medlab Central** — Palmerston North / MidCentral.
- **Canterbury Health Laboratories (CHL)** — Canterbury, now Health NZ.

Each provider has subtly different header layout, footer comments, and abnormal-value flagging conventions. Embed an obviously-synthetic banner (`-- SYNTHETIC — NOT FOR CLINICAL USE --`) in the metadata block so leakage of the structured payload is trivially distinguishable.

**Urgency-driving lab findings** (for Immediate / Urgent enrichment, all sourced from RCPA / AACB harmonised critical-value list and BPAC NZ):

- **Immediate**: K⁺ ≥6.5 mmol/L; Na ≤120 or ≥160 mmol/L; glucose <2.8 or ≥25 with ketones; Hb <70 g/L acute; platelets <20 ×10⁹/L; INR ≥6 on warfarin; positive blood culture flag; hs-troponin rising in chest-pain context.
- **Urgent**: K⁺ 6.0–6.4; Na 121–125 or 156–159; new Hb 70–90; platelets 20–49; INR 5–5.9; creatinine doubled from baseline (AKI); positive FIT with high f-Hb routes to 6-week colonoscopy (Routine, *not* Urgent — common misclassification).
- **Routine**: stable abnormal values, monitoring labs, mildly out-of-range chronic markers.
- **Information only**: normal results, copy-of-correspondence.

### 7.2 Radiology reports

**NZ providers**:

- Private network: **Pacific Radiology Group** (Wellington, Auckland, Christchurch, Tauranga, Palmerston North, Queenstown), **Auckland Radiology Group**, **Mercy Radiology**, **Wellington Radiology Group**, **Bay Radiology**.
- Public DHB / Te Whatu Ora: Te Toka Tumai Auckland, Waitematā, Counties Manukau, Waikato, Capital & Coast, Canterbury — variable templating, more free-text dictation.

**RANZCR structured templates** (adopted variably across NZ providers): Mammography → **BI-RADS 0–6** with density a/b/c/d; CTPA → standard structure with PE location (main / lobar / segmental / subsegmental) and right-heart strain; Lung screening CT → **Lung-RADS**; Liver imaging → **LI-RADS**; Prostate MRI → **PI-RADS 1–5**; Thyroid US → **TI-RADS**.

**Free-text structure**: clinical history → technique → findings (anatomical regions) → **Impression** (the section that drives triage). NZ convention: impression is numbered with item 1 most important. Hedging is common: "cannot exclude", "clinical correlation recommended", "suggest follow-up imaging in 6 months".

**Urgency-driving findings**:

- **Immediate**: intracranial haemorrhage, tension pneumothorax, aortic dissection on CTA, pulmonary embolism on CTPA (main / lobar), bowel perforation with free gas, ruptured AAA.
- **Urgent**: acute appendicitis on CT, suspicious lung nodule >8 mm, BI-RADS 4–5 breast lesion, acute cholecystitis, DVT on Doppler, displaced fracture requiring orthopaedic review.
- **Routine**: benign cyst, stable finding, mild degenerative change.
- **Information only**: normal study, "no acute abnormality", incidental adrenal nodule on follow-up.

**Realism tip — buried red flag.** The Impression line often does *not* match the urgency of buried findings — exactly the contextual-reasoning failure mode the §3.6 stress subset is constructed to probe. Example: Impression says "No acute intracranial abnormality" but the body mentions "incidental 9 mm enhancing lesion in left frontal lobe, further characterisation recommended". Defensibly Urgent. Include this pattern in ~15 % of radiology items.

### 7.3 Discharge summaries

**National standard**: HL7 CDA R2 eDischarge per **HISO 10015** (NZ eDischarge Summary Standard) and the Health Information Exchange (HIE) programme. Regional variation is substantial:

- **Auckland metro** (Te Toka Tumai, Waitematā, Counties Manukau): 70–85 % structured CDA with named sections, Dragon dictation for narrative within structure.
- **Waikato / Bay of Plenty / Hawke's Bay**: ~50–70 % structured.
- **Canterbury**: historically high structured rate post-quake systems rebuild (HealthOne integration).
- **Rural South Island** (West Coast, Southland, Nelson Marlborough): 20–50 % structured, more free-text dictation, occasional handwritten-scanned-to-PDF.

**Standard section headers**: Reason for admission → HPI → PMH → Medications on admission → Examination → Investigations (labs, imaging, ECG) → Course in hospital → Diagnoses (primary + secondary) → Procedures → Discharge medications (NEW / CHANGED / STOPPED) → Follow-up plan → **GP actions** → Signed by, role, date.

**Generate three subtypes**: (a) fully structured CDA-derived (clean headers, list formatting); (b) semi-structured (headers but free-text paragraphs); (c) free-text dictation (no headers, paragraph-style, often with Dragon dictation artefacts like "period" read aloud or mis-capitalisation).

**Urgency drivers**:

- "GP to follow up abnormal CT result" with mention of incidentaloma → Urgent.
- New medication requiring monitoring (INR, lithium, renal function) with GP to arrange → Urgent or Routine depending on time-criticality.
- "Discharge against medical advice" with unresolved issues → Urgent.
- Post-op wound check flagged to GP → Routine.
- Tertiary referral in progress, GP for information → Information only.

The "GP actions" section is the most label-determining region of a NZ discharge summary — but its location varies by template, and some DHBs bury actions in the narrative. This is a rich source of contextual-reasoning stress items.

### 7.4 Specialist letters

**College conventions**:

- **RACP** (Royal Australasian College of Physicians) — medical specialties. Cardiology and oncology heavily templated; geriatrics and general medicine more free-text. Letters open "Dear Dr [GP]", brief history, exam if performed, investigations, impression, plan, "Yours sincerely".
- **RACS** (Royal Australasian College of Surgeons) — surgical specialties. General surgery and orthopaedics commonly free-text; colorectal, breast, vascular use more templating. Very short post-op review letters are common.
- **RANZCR** — radiation oncology letters are highly structured (diagnosis, staging, planned treatment, side-effect monitoring, follow-up schedule).
- Psychiatry (RANZCP), Obs & Gyn (RANZCOG), Paeds (RACP P&CH) — each with own conventions.

**Public outpatient vs private specialist**:

- Public outpatient: shorter, DHB letterhead, "Thank you for referring this patient who was seen in [X] clinic on [date]", often dictated by registrar and countersigned by consultant. Wait-time for FSA referenced.
- Private specialist: longer, more personalised, addressed by name, secretary/phone contact, sometimes billing or next-appointment details.

**Standard structure**: Date → "Dear Dr [GP surname]" → "Re: [Patient name], DOB, NHI" → reason for referral acknowledgement → history → exam → investigations reviewed → Impression → Plan (often bulleted) → "Thank you for referring this patient. I will see them again in [interval] / have discharged back to your care" → consultant signoff with FRACP/FRACS/FRANZCR/FRANZCOG and clinic contact.

**Urgency drivers**:

- "Please start [drug] today and arrange follow-up bloods in 1 week" → Urgent.
- "Histology confirms malignancy — discussed at MDM, please arrange urgent surgical referral" → Urgent / Immediate.
- "Incidental finding requires GP-led further workup" → Urgent or Routine.
- Routine follow-up letter, "discharged back to your care" → Information only.

### 7.5 Patient portal messages

**NZ portals**:

- **ManageMyHealth** (Medtech-integrated; ~500–600 practices, **verify**) — messages appear in the GP inbox as structured form fields + free text.
- **MyIndici** (Indici PMS-integrated; ~250–350 practices, **verify**).
- **ConnectMed** — smaller footprint.
- **Health365 / Vensa Health / others** — long tail.

**Typical content distribution** (aligned with Rotenstein 2025 US primary-care inbox shape; NZ figures approximate):

- Repeat prescription requests: 45–55 %
- Appointment bookings / changes: 15–25 %
- Results queries: 10–15 %
- Clinical questions: 8–12 %
- Administrative (forms, certificates, referrals): 5–10 %

**Tone and style**:

- Highly variable length (one sentence to multi-paragraph).
- Informal first-person language; spelling and grammar variation (older patients, English-as-additional-language).
- Often missing context — "can I have my usual tablets please" with no drug named.
- Repeat-script requests frequently list medications without strengths or quantities.
- **Buried clinical questions** in otherwise-routine messages: "…and by the way I've had chest pain for a week" — the archetypal recall-critical case. Over-represent in Immediate / Urgent borderlines.
- Portal disclaimers: every NZ portal has a "not for urgent issues, call 111" banner. Include occasionally to reflect reality.

### 7.6 NZ-specific clinical phrasing

Common inbox abbreviations: **d/w** (discussed with), **FYI**, **actioned**, **r/v** (review), **f/u** (follow up), **c/o** (complaining of), **Hx**, **Ix**, **Mx**, **Dx**, **Rx**. Common references: **BPAC** (Best Practice Advocacy Centre, NZ guidelines), **NZF** (NZ Formulary), **NZULM** (NZ Universal List of Medicines), **HealthPathways** (regional clinical pathway platform — "Canterbury HealthPathways", "Auckland Regional HealthPathways").

**Drug naming**: NZ uses international generic names but brand names via NZULM (Losec = omeprazole, Panadol = paracetamol, Voltaren = diclofenac). Letters alternate between brand and generic. Pharmac-funded brand switches (e.g. atorvastatin brand changes) are common inbox chatter.

**Units**: metric throughout — BP mmHg, weight kg, height cm/m, temperature °C. **Avoid** mg/dL, lb, °F, and UK-only dosing oddities.

### 7.7 Ethnicity representation strategy

**NZ 2023 Census** (Stats NZ, released 2024) total-response ethnicity: European ~67.8 %, Māori ~17.8 %, Pacific ~8.9 %, Asian ~17.3 %, MELAA ~1.9 %, Other ~1.1 % (total >100 % because multi-response).

**The distortion problem.** A naive census-mirror has three failure modes: (1) under-sampling of conditions with ethnic prevalence patterns (rheumatic fever in Māori and Pacific children, gout in Pacific men); (2) classifier propagation of name-recognition bias (Obermeyer 2019, Seyyed-Kalantari 2021); (3) Te Tiriti obligations require *active* Māori representation, not passive proportional representation (Te Mana Raraunga *Māori Data Sovereignty Charter* 2018; NEAC 2022; MBIE Vision Mātauranga).

**Recommended target distribution** for the 400-item Sprint 2 set:

| Ethnicity | Proportion | ≈ items of 400 |
|---|---:|---:|
| European | 65 % | 260 |
| Māori | 20 % | 80 |
| Pacific | 12 % | 48 |
| Asian | 15 % | 60 |
| MELAA / Other | 3 % | 12 |

Māori is enriched from census ~17.8 % to 20 %; Pacific from ~8.9 % to 12 %; European is dropped from ~67.8 % to 65 %. Total exceeds 100 % because of multi-response. Mechanics: enrichment is expressed in the name pool weighting, the clinical content (rheumatic fever follow-up letters disproportionately with Māori / Pacific patient context), and GP commentary phrasing. Avoid stereotyped condition–ethnicity coupling — apply enrichment as an independent axis with only moderate epidemiological weighting.

**Sprint 3 metric reporting** must report stratified metrics by ethnicity. If any ethnicity-stratified sensitivity on Immediate / Urgent falls below 99 % / 95 % respectively, that is an explicit architecture-disqualifying signal. **Annotator note**: Ryo's labels are judged on clinical content alone; ethnicity is a data-generation parameter, not a labelling parameter.

## 8. Quality Evaluation of the Synthetic Dataset

### 8.1 Sanity checks — programmatic audits

Published synthetic-dataset work (El Emam et al. 2020 *Practical Synthetic Data Generation*; Hernandez et al. 2022 *Neurocomputing* systematic review; Libbi et al. 2021 on synthetic Dutch clinical text; Lehman et al. 2021 on MIMIC memorisation) converges on a small set of programmatic checks that should run automatically on every batch and block release on failure. We implement them as a single Python script — `tools/qa_report.py` — with an exit-code contract so CI and the release checklist share the same source of truth.

**Schema and field completeness.** Every row parses as JSON, contains every required field, types match, enums match, timestamps are ISO 8601. `pydantic` or `jsonschema`. Pass criterion: 100 %.

**Label–content consistency rules.** A curated rule pack catches the worst generator slips. Examples for our taxonomy:

- Any `synthetic_text` containing tokens matching `hyperkal|K[+\s]*[>≥]\s*6\.[0-9]|troponin.*elevated|STEMI|massive PE|neutropenic sepsis|pH\s*<\s*7\.2` should be labelled Immediate or carry an explicit boundary flag.
- Any lab item with all values within supplied reference ranges should not be labelled Immediate.
- Any Information-only item should not contain explicit critical-value tokens.
- Lab items must parse to valid HL7 v2.4 segments.
- Radiology items must contain at least one of `findings`, `impression`, `conclusion` sections.
- Discharge summaries and specialist letters must contain a plausible NZ-specific signature block.

These are cheap (Python regex or jq) and run on every batch of 30 items before GP labelling. Pass criterion: ≥95 % of rule hits aligned with labels; the residual 5 % goes to GP re-review and either re-labels or carries an explicit rationale exception.

**Style variation metrics.** Drawn from the diversity-in-generated-text literature (Zhu et al. 2018 *Texygen*; Tevet & Berant 2021):

- **MTLD** (McCarthy & Jarvis 2010) — length-invariant lexical diversity. Target `[50, 95]` per doc_type, comparable to clinical-corpus baselines.
- **Sentence length distribution** — mean, sd, skew, kurtosis per doc_type. Discharge summaries have visibly heavier right tails than patient messages.
- **Self-BLEU** (Zhu 2018) on within-class pairs — high self-BLEU (>0.35) flags near-template generation.
- **Distinct-2** (Li 2016) — fraction of distinct bigrams. Target ≥0.5 per class.
- **Function-word KL divergence vs MIMIC-III** as a stylometric sanity check. Suspiciously low KL signals memorisation; very high KL signals stilted LLM prose.

**Near-duplicate detection.** **MinHash + LSH** (`datasketch`) at Jaccard 0.9 / 0.95 / 0.99 bands; pass criterion <2 % of pairs at 0.95, zero at 0.99. Plus **embedding-space cosine** (sentence-transformers `all-MiniLM-L6-v2` on CPU) ≥0.95 as a paraphrase-aware second pass; pass criterion <3 %.

**PII / PHI scan.** Microsoft Presidio + a custom NZ regex pack: NHI `[A-HJ-NP-Z]{3}\d{4}` excluding the synthetic `ZZI`/`ZIO` prefix, NZ phone patterns, common NZ surname list, DOB patterns. Any high-confidence hit blocks release pending manual review.

**Reference-range plausibility.** For HL7 lab items, every numeric checked against a hard-coded plausible range table (serum K⁺ 2.0–8.5 mmol/L, Hb 40–220 g/L, etc.). Out-of-range values indicate generator hallucination and fail automatically.

### 8.2 Human audit proportions — what's realistic

Published clinical NLP precedent:

- **n2c2 / i2b2 shared tasks** (Uzuner 2011 for de-identification, Stubbs 2015 for medications) — double annotation on 100 % with third-annotator adjudication. The gold standard but assumes multiple annotators.
- **MedMentions** (Mohan & Li 2019) — 100 % expert review on entity annotations.
- **CASI** (Moon 2014) — 100 % manual annotation.
- **RadGraph** (Jain 2021) — 500 reports, 100 % expert annotation.
- **emrQA** (Pampari 2018) — *sampled* expert review (~5 %) only because of scale (~1 M QA pairs).

**Rule of thumb**: below ~2 000 items, 100 % expert review is feasible and expected. Sampling audits (5–10 %) are only justified above ~10 000 items or when annotation costs dominate.

For **300–500 items with a single GP, 100 % audit is mandatory and realistic.** The 60 GP-hour budget supports it (see §5.5 for the time budget breakdown). Two-pass strategy: pass 1 first-look labelling at ~2 min/item, pass 2 reconciliation/adjudication at ~5 min/item on a flagged ~20 % stratified subsample focused on Immediate / Urgent (because that's where the ≥99 % sensitivity target lives).

### 8.3 Calibration set for intra-rater drift

Single-annotator drift across a 2-week sprint is well-documented (Bayerl & Paul 2011; Klie et al. 2023; Hovy & Lavid 2010). We implement the calibration-set protocol described in §5.4: 25–30 stratified items re-labelled blind on Days 2, 7, and 13, with quadratic-weighted Cohen's κ computed pairwise. **Pass criterion: κ ≥0.75 across all three pairwise comparisons.** κ <0.70 between rounds 1 and 3 triggers full re-labelling of the drift-affected cells; moderate drift (0.60–0.74) triggers a rationale-review pass. Confusion-matrix inspection: drift across non-adjacent classes (Immediate ↔ Routine) is a red flag; adjacent-class drift (Urgent ↔ Routine) is expected boundary-case difficulty.

The calibration set also serves as a **taxonomy bridge set** if rd-20260405-001 refines the taxonomy mid-sprint — Ryo re-labels the 25 items under the new taxonomy first, and pre-post agreement measures the size of the delta before any production re-labelling is committed.

### 8.4 Realism evaluation against real data — deferred to Obj 2

When real NZ GP inbox data becomes available under Obj 2, the published synthetic-vs-real comparison methods are:

- **Distributional distance** — Jensen-Shannon / KL divergence on token frequencies, Wasserstein distance on embeddings (Goncalves et al. 2020; Hernandez et al. 2022).
- **MAUVE** (Pillutla et al. 2021 NeurIPS) — KL-curve method explicitly designed for comparing machine-generated and human text distributions. **Recommended primary realism metric.**
- **Frechet BERT Distance** — clinical-text analogue of FID using clinical BERT embeddings.
- **Maximum Mean Discrepancy (Gretton 2012)** with RBF kernel on sentence embeddings — used in synthetic-EHR literature (Choi 2017 medGAN, Yoon 2020 ADS-GAN).
- **Expert blind A/B (Turing-style)** — GP shown 20–25 mixed pairs, asked to identify the synthetic. Chance ≈50 %; ≤70 % means hard to distinguish (Amin-Nejad 2020; Libbi 2021; Ive 2020). Budget: ~30 min GP time.
- **Downstream utility comparison (the load-bearing test)** — train classifier on synthetic, test on real, and vice versa. Report the four-corner evaluation (Jordon et al. 2022). The argument that justifies synthetic data for architecture selection: **the relative ranking of architectures on synthetic vs real tends to be more stable than absolute scores**. Sprint 3 must structure its evaluation to support this comparison the moment any real sample arrives.

For Sprint 2, only stylometric sanity (G10 MTLD), self-BLEU, and distinct-n run on synthetic alone. The four-corner downstream test is a Sprint 3 / Obj 2 task.

### 8.5 Programmatic release gates — G1–G14

Concrete pass criteria for `tools/qa_report.py` to emit GREEN for Sprint 3 handoff:

| Gate | Metric | Pass criterion |
|---|---|---|
| **G1** | Schema validation | 100 % rows valid |
| **G2** | Required-field completeness | 100 % non-null on required fields |
| **G3** | Label distribution vs target | ±3 % absolute per non-zero urgency × doc_type cell |
| **G4** | Minority-class presence | ≥15 Immediate items, ≥60 Urgent items |
| **G5** | Near-duplicates (MinHash 0.95) | <2 % of pairs |
| **G6** | Embedding-space near-duplicates (cosine ≥0.95) | <3 % of pairs |
| **G7** | Rule-based content–label consistency | ≥95 % of rule hits aligned |
| **G8** | PII / PHI scan | 0 high-confidence hits |
| **G9** | Reference-range plausibility (labs) | 100 % numerics in plausible ranges |
| **G10** | MTLD lexical diversity | within `[50, 95]` per doc_type |
| **G11** | Intra-rater κ on calibration set (rounds 1–3) | ≥0.75 |
| **G12** | Label–content sanity audit on 50 random items | ≥48/50 correct |
| **G13** | Boundary-case coverage | ≥15 % of dataset flagged `boundary_case_flag=true` |
| **G14** | Datasheet completeness (Gebru et al. 2021) | all sections non-empty |

All 14 gates must be GREEN before the `v0.1.0-sprint2` tag is cut. G4 is specifically the recall power floor: estimating 99 % sensitivity at Wilson 95 % CI half-width ≤3 % needs ~75 Immediate+Urgent items, with ≥15 Immediate as the absolute minimum for detecting catastrophic classifier failure.

## 9. Failure Modes and Mitigations

Ranked roughly by how likely each is to mislead Sprint 3 architecture selection. The top three (shortcut learning, generator–classifier coupling, spectrum bias) are the load-bearing risks for whether the dataset is fit for purpose at all.

### 9.1 Shortcut learning on generator idioms — HIGH risk

**The trap.** LLMs produce stylised text. "URGENT:", "Please note", "The patient was noted to be", consistent sentence openers, predictable Oxford-comma usage, formal verb tense. A classifier trained or even just *evaluated* on such text exploits these surface features as shortcuts to the label — the classifier is detecting "was this generated under the Urgent template?" rather than "is this clinically urgent?". On real inbox text the shortcuts vanish and sensitivity collapses.

**Citations.** Geirhos et al. 2020 *Nature Machine Intelligence* "Shortcut learning in deep neural networks" is the canonical reference. Niven & Kao 2019 *ACL* showed BERT solving Argument Reasoning Comprehension purely by exploiting word presence — the model never reasoned. Hicks et al. 2022 documented shortcut exploitation on synthetic-augmented medical imaging. McDermott et al. 2021 *Science Translational Medicine* surveyed reproducibility failures in clinical ML, with shortcut learning prominent.

**Mitigations** (all baked into §3 generation protocol):
- **Paraphrase smoothing** — every Sprint-2 item gets a one-shot paraphrase pass with a different prompt; randomly pick one of the two outputs (§3.2 control C1).
- **Style randomisation** — generation prompt samples from a `persona_pool.json` of writer roles (junior registrar, senior consultant, practice nurse, lab MLS) and tone descriptors (§3.2 control C2).
- **Template-diverse generation** — five templates per `(doc_type, urgency)` cell, rotated; no single template ever dominates a class.
- **Urgency-token scrubbing** — programmatic regex stripping of `\b(URGENT|IMMEDIATE|STAT|CRITICAL)\b` before labelling. Both scrubbed and original variants are stored so Sprint 3 can ablation-test classifier behaviour.
- **TF-IDF back-classification probe** (§3.2 control C3) — fit a logistic regression on TF-IDF features alone; if it scores >70 % macro F1 on the synthetic data, the dataset is leaking surface features and the generation pipeline is iterated.
- **Adversarial probe set** — Sprint 3 holds out a small set of items where headers/templates are stripped to bare narrative; gap between full-template and stripped-template performance is the shortcut tax.

### 9.2 Generator–classifier coupling — HIGH risk, underappreciated

**The trap.** If Sprint 3 evaluates classifier candidates from the same model family that generated the data (e.g. Claude Sonnet generating + Claude Sonnet–based classifier evaluating), the classifier "recognises" its own family's stylistic fingerprints and performs artificially well. The architecture ranking is then distorted in favour of same-family candidates — the exact opposite of what a fair shortlist evaluation requires.

**Citations.** Less formally published than shortcut learning but a known phenomenon. Shumailov et al. 2024 *Nature* "The curse of recursion: training on generated data makes models forget" describes the underlying distributional self-reinforcement. Alemohammad et al. 2023 "Self-consuming generative models go MAD" reaches the same conclusion through a different lens.

**Mitigations.**
- **Multi-model generation** — the Sprint 2 pipeline alternates Claude Sonnet 4.6 with a second frontier family (e.g. Llama 3.3 70B Instruct on Catalyst Cloud, or a Gemini-class fallback if available NZ-side) on a roughly 70/30 split, with model identity tracked in `generator.family`.
- **Cross-family paraphrase canary** — on a 10–20 % subset, items are re-paraphrased with the second family. Sprint 3 reports classifier scores split by `generator.family`; a large gap between same-family and cross-family scores is the coupling alarm.
- **Mandatory non-Claude baseline in Sprint 3** — the architecture shortlist (R3) already requires at least one open-source self-hosted candidate, which doubles as a coupling guard for the Claude-generated portion.
- **Document the coupling risk in `DATASHEET.md`** under Gebru's "Uses — Tasks for which the dataset should not be used" section, so Sprint 3 evaluators can never claim they were not warned.

### 9.3 Spectrum bias — HIGH risk

**The trap.** Synthetic data generated from prompts gravitates to *clear-cut* cases. Classifiers evaluated on clear-cut cases score 99 % sensitivity in the synthetic world and 85 % in reality, because real inboxes contain ambiguous borderline items: a K⁺ of 6.0 sitting on the lab's critical threshold, a CT report with "cannot exclude PE", a discharge summary where the urgent action is buried on page 3.

**Citations.** Spectrum bias is a classical epidemiology concept (Ransohoff & Feinstein 1978 *NEJM* "Problems of spectrum and bias in evaluating the efficacy of diagnostic tests"), repeatedly rediscovered in medical ML — Park & Han 2018 *Radiology*, Willemink et al. 2020 *Radiology* "Preparing medical imaging data for machine learning".

**Mitigations.**
- **Boundary-case quota** — ≥15 % of every dataset version is flagged `boundary_case_flag=true` (gate G13). Boundary cases are constructed by perturbing clear-cut cases (K⁺ 6.5 → 6.0; "massive PE" → "small subsegmental PE"; adding context that softens or sharpens apparent urgency).
- **Contextual reasoning stress flag** — ≥10 % of items tagged `contextual_reasoning_stress_flag=true`, where urgency depends on context beyond the document body itself (recent discharge, comorbidity, medication interaction, timeline drift). This implements the response to the NHS GPT-oss-120b 6:1 finding (§3.4).
- **Stratified Sprint 3 reporting** — sensitivity reported separately on boundary, contextual-stress, and clear-cut subsets. A classifier scoring 99 % on clear-cut and 70 % on boundary is a different animal from one scoring 95 % on both, and the architecture shortlist must surface the difference.

### 9.4 Synthetic-to-real transfer gap — MEDIUM-HIGH risk

**Published magnitude.** Abdalhalim et al. 2025 reported 8–15 percentage-point sensitivity drops from validation to deployment in clinical NLP. Rajkomar et al. 2018 *npj Digital Medicine* showed AUROC drops of 0.02–0.10 when deep-learning EHR models cross hospital boundaries. Finlayson et al. 2021 *NEJM* "The clinician and dataset shift in artificial intelligence" is the canonical statement of distribution shift in deployed clinical ML. Specifically on synthetic clinical text: Libbi et al. 2021 reported ~10-point F1 drops from synthetic-trained models to real Dutch clinical data.

**Implication for Sprint 3.** The dataset enables architecture **ranking**, not absolute performance estimation. Sprint 3 scores must be interpreted with a **10-point discount** when extrapolating to real-data performance — an architecture scoring 95 % synthetic sensitivity is plausibly 80–87 % on real data, below the 99 % target. This caveat goes in the architecture shortlist deliverable's executive summary, not buried in an appendix.

**Mitigations.**
- **Explicit 10-point discount rule** — applied uniformly to every Sprint 3 architecture's headline number.
- **Real-data sanity-run reserve** — hold 3 GP-hours and a 50-item budget at the end of Sprint 3 for de-identified real samples (any clinical samples that emerge from Sprint 1 GP review correspondence, with consent).
- **Track ranking stability, not absolute accuracy** — Jordon et al. 2022 (Royal Society / Alan Turing Institute synthetic data report) makes the ranking-stability case explicitly. As long as architecture ranking is preserved synthetic-to-real, the dataset has done its job.

### 9.5 Generator-LLM training-data leakage / memorisation — MEDIUM risk

**The trap.** Frontier LLMs have seen MIMIC-III, the n2c2 / i2b2 releases, PubMed case reports, NHS digital release samples, and similar in their training data. Generated items may be near-verbatim or paraphrased copies of real training samples — contaminating the dataset with US-hospital distribution that is not NZ GP inbox, and biasing evaluation toward architectures that have also seen those sources.

**Citations.** Carlini et al. 2021 *USENIX Security* "Extracting training data from large language models" and Carlini et al. 2023 *ICLR* "Quantifying memorization across neural language models" are the foundational empirical works. Lehman et al. 2023 *CHIL* "Do we still need clinical language models?" discusses clinical-corpus overlap specifically.

**Mitigations.**
- **NZ context anchoring** — every generation prompt anchors in NZ GP practice: NHI placeholder, NZ medications via NZULM/Pharmac, NZ specialist referral patterns, HealthPathways idioms, NZ unit conventions (mmol/L, mmol/mol IFCC HbA1c). Out-of-domain US idioms are flagged and regenerated.
- **MIMIC-III KL probe** — compute KL divergence of token frequencies against a small MIMIC-III sample. Suspiciously *low* KL is the memorisation alarm; expected KL on properly NZ-anchored items is moderately high.
- **Verbatim n-gram check** — 8-gram match against the publicly available MIMIC-III, n2c2, and PubMed central abstracts samples that the team can host locally. Any 8-gram match triggers regeneration.

### 9.6 Label leakage through structure and templates — MEDIUM risk

**The trap.** If Urgent items consistently come from a different template than Routine items, the template header alone is a leakage channel. A classifier learns "section order: Impression / Recommendation" → Urgent without ever reading the body text.

**Mitigations.**
- **Identical scaffolding within doc_type** — all items of the same `doc_type` share the same section structure regardless of urgency class.
- **Bag-of-sections leakage test** — train a stupid bag-of-sections logistic regression on structure-only features (no body text). If it scores meaningfully above chance on urgency, structural leakage is confirmed and templates are reworked. Same family of test as the §3.2 TF-IDF probe but on a different feature set.
- **Plausible randomisation** — section order is randomised within clinically plausible bounds where templates allow.
- **Generator template ID stored** in `generator.prompt_template_id`, so Sprint 3 can post-hoc audit which templates dominate which classes and rerun stratification if a leakage flag triggers.

### 9.7 Single-annotator drift — MEDIUM risk

**The trap.** One GP labelling 400 items over two weeks shifts thresholds as familiarity grows and fatigue accumulates. Day-1 "Urgent" is not Day-13 "Urgent".

**Mitigation.** §5.4 calibration set is the primary defence — 25 items, blind re-label rounds at Days 2 / 7 / 13, quadratic-weighted Cohen's κ ≥0.75 floor across all three round pairs. Drift below 0.75 between rounds 1 and 3 triggers a full reconciliation pass on the drift-affected cells. Moderate drift (0.60–0.75) triggers a rationale-review pass without re-labelling. The same calibration set doubles as the **taxonomy bridge** if Sprint 1 GP review (rd-20260405-001) refines the taxonomy mid-sprint — Ryo re-labels the 25 items first under the new taxonomy and the pre/post agreement quantifies the delta cheaply.

### 9.8 Generation artefacts and hallucinations — LOW–MEDIUM risk

**The trap.** Generator hallucinates impossible numeric values, drug doses beyond plausible (paracetamol 10 g QID), nonsense dates (admission after discharge, future dates beyond sprint window), contradictory clinical pictures (renal failure with normal creatinine).

**Mitigations.** Programmatic gates catch the worst:
- **G9 reference-range plausibility** on every numeric lab result (serum K⁺ 2.0–8.5, Hb 40–220 g/L, creatinine 30–2000 µmol/L, etc.).
- **Drug-dose plausibility table** — paracetamol ≤4 g/day, common antibiotic ranges, insulin per-unit ceilings.
- **Date-coherence rule** — admission date < discharge date < report date; no dates beyond `generated_at + 1 day`; relative dates ("3 weeks ago") parsed and bounded.
- Any failure is regenerated, not patched.

### 9.9 Published cautionary cases

Specific failures in deployed clinical ML that motivate our caution:

- **Epic sepsis model** — Wong et al. 2021 *JAMA Internal Medicine* "External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients". Internal validation 0.76–0.83 AUROC; external validation collapsed to 0.63; sensitivity at the deployment threshold was 33 %. The lesson: internal evaluation (synthetic or otherwise) systematically overstates real-world performance.
- **IBM Watson for Oncology** — trained partly on hypothetical cases composed by MSKCC experts (a synthetic-data analogue). Failed in deployment at MD Anderson and elsewhere; documented in Strickland 2019 *IEEE Spectrum* "IBM Watson, heal thyself" and STAT News investigations. The lesson: synthetic / expert-composed training data can produce a model that ranks well in development and fails in the field.
- **Google DR screening in Thailand** — Beede et al. 2020 *CHI* "A human-centered evaluation of a deep learning system deployed in clinics for the detection of diabetic retinopathy". Not synthetic data, but a foundational case study of how validation conditions mismatch deployment conditions; reinforces the synthetic-to-real caveat.
- **Libbi et al. 2021** on GPT-2-generated Dutch clinical text — directly measured the synthetic-to-real gap and reported ~10-point F1 drops, anchoring the §9.4 discount rule.
- **Obermeyer et al. 2019** *Science* "Dissecting racial bias in an algorithm used to manage the health of populations" and Seyyed-Kalantari et al. 2021 *Nature Medicine* on radiograph classifier disparities — both motivate the §7.7 ethnicity-stratified evaluation requirement Sprint 3 must implement.

Each case is cited verbatim in `DATASHEET.md` "Known limitations" so Sprint 3 evaluators inherit the caution.

## 10. Executable 2-Week Protocol — Day-by-Day, Tools, Schema, and Risks

This section is the operational handoff. Sprint 2 runs **Sun 12 Apr 2026 – Sat 25 Apr 2026**. Day numbering counts from the sprint Monday (13 Apr) as Day 1; Day 0 is the Sunday kickoff. Ting works weekdays (~7 h/day, ~90 h budget); Ryo works weekends and selected evenings (~34 h budget against a 60 h ceiling).

### 10.1 Day-by-day plan

| Day | Date | Who | Activity | Output |
|---|---|---|---|---|
| 0 | Sun 12 Apr | Ting | Sprint 2 kickoff. Finalise schemas, pull Sprint 1 taxonomy v1 draft, set up `datasets/inbox-helper-synth-v1/` repo skeleton, write `generate.py` scaffold, configure Bedrock ap-southeast-6 (Auckland) access — fall back to Catalyst Cloud Llama 3.3 70B Instruct if Bedrock NZ regional model availability is incomplete. Draft 5 prompt templates × 5 doc_types = 25 templates v0. Stand up `tools/qa_report.py` skeleton on a 10-item toy dataset to shake out CI bugs. | Repo skeleton, 25 prompt templates v0, qa_report.py runs end-to-end, 10-item toy dataset |
| 1 | Mon 13 Apr | Ting | Finalise generation prompts. Dry-run generation of **30 seed items** (~6 items × 5 doc_types) across all 4 urgency classes. Run sanity QA script on seed. Build `tools/sheet_sync.py` and a Google Sheets labelling sheet bound to JSONL. | 30-item seed JSONL, QA report v0, labelling sheet |
| 2 | Tue 14 Apr | Ting + Ryo (eve, ~2 h) | Ryo labels 30 seed items (~90 min, pass 1 only); Ryo labels **25-item calibration set round 1** blinded; Ting incorporates any prompt feedback. | Seed labels, calibration round 1 |
| **Gate 1** | **end Tue 14 Apr** | | **Seed-set quality review.** GREEN ≥26/30 GP-aligned → scale-up; AMBER 20–25 → prompt revision + re-seed; RED <20 → pivot conversation with Ting. | **Go/no-go memo** |
| 3 | Wed 15 Apr | Ting | If Gate 1 GREEN: scale generation to **150 items** (~30/day pace). Cross-family paraphrase canary on 15 items (10 %). | 150 items JSONL v1 |
| 4 | Thu 16 Apr | Ting | Continue generation to **250 items**. Run nightly QA gates G1–G10. | 250 items JSONL, QA v1 |
| 5 | Fri 17 Apr | Ting (+ Ryo eve buffer) | Generation to target **400 items**. Nightly QA. Flag near-duplicates for paraphrase regeneration. Buffer evening for label catch-up if needed. | 400 items JSONL, QA v2 |
| 6 | Sat 18 Apr | Ryo (full day, ~10 h) | Labelling push — target **150 items** (pass 1, ~4 min/item with rationale). Log borderline cases. Re-run QA mid-day. | 150 labels |
| 7 | Sun 19 Apr | Ryo (full day, ~10 h) | Labelling push — target **150 more items**. **Calibration round 2 blinded.** Write first-weekend reflection memo. | 150 labels + calibration round 2 |
| **Gate 2** | **end Sun 19 Apr** | | **Week 1 close.** ≥300 items generated and ≥270 labelled (pass 1); intra-rater κ rounds 1↔2 ≥0.75; G1–G10 GREEN on labelled subset. RED triggers Mon-morning re-plan. | **Week 1 report** |
| 8 | Mon 20 Apr | Ting | **rd-20260405-001 GP review feedback arrives today.** Review for taxonomy changes; assess impact; if material changes, draft taxonomy delta memo and re-label plan. Bump `taxonomy_version` if needed; Ryo will re-label calibration set first under new taxonomy. **No generation today** — reserved for impact assessment. | Taxonomy delta memo |
| 9 | Tue 21 Apr | Ting + Ryo (eve) | Adjudication on weekend pass-1 flagged items (`disputed/` folder). If taxonomy changed, Ryo re-labels 25-item calibration set under new taxonomy (~1 h, blinded) → produces taxonomy bridge κ. | Adjudication log, taxonomy bridge labels |
| 10 | Wed 22 Apr | Ting | If headroom exists, top-up generation toward 400–450. Run embedding-similarity duplicate scan; paraphrase-smooth any cosine ≥0.95 pairs. Run TF-IDF back-classification probe (§3.2 C3); if it scores >70 %, iterate generation prompts. | Final generation batch, dedupe report, leakage probe |
| 11 | Thu 23 Apr | Ting + Ryo (eve, ~3 h) | Ryo reconciliation pass on flagged items (target ~20 % of dataset, ~5 min/item). | Reconciliation labels |
| **Gate 3** | **end Thu 23 Apr** | | **Full coverage + IRA.** ≥95 % label completeness; reconciliation 100 % done on flagged items; intra-rater κ rounds 1↔3 ≥0.75 (conditional on round 3 timing); all G1–G10 GREEN on full dataset. | **Gate 3 report** |
| 12 | Fri 24 Apr | Ting | Address Gate 3 failures. Finalise `DATASHEET.md` (Gebru 2021), `README.md`, `SCHEMA.md`, `CHANGELOG.md`. Tag **v0.9-rc1**. | Datasheet, README, v0.9-rc1 |
| 13 | Sat 25 Apr | Ryo (half day, ~5 h) | Final label pass on outstanding items. **Calibration round 3 blinded.** Sign off on taxonomy-affected relabels. | Final labels, calibration round 3 |
| **Gate 4** | **end Sat 25 Apr** | | **Final release gate.** All G1–G14 GREEN; v1.0 tag; Sprint 3 handoff packet ready. | **Release v1.0** |

**Workload sanity check.** Ting: ~13 weekdays × ~7 h = ~90 h, comfortable. Ryo: Sat 18 (~10 h) + Sun 19 (~10 h) + Sat 25 (~5 h) + evenings (~9 h) = ~34 h on labelling, well within the 60 h ceiling. The slack absorbs reconciliation, adjudication, and the Day-9 taxonomy re-label scenario.

**Labelling rate.** Pass 1 at 4 min/item including rationale capture; reconciliation at 5 min/item on flagged ~20 %. For 400 items: pass 1 = 26.7 h; reconciliation 80 items × 5 min = 6.7 h; calibration 3 × 25 × 4 min = 5.0 h; total ~38.4 h, within ceiling. **Gate 1 adjustment lever**: if pass-1 rate runs >5 min/item, dataset target drops from 400 → 350 to preserve quality over volume.

### 10.2 Tool stack

| Concern | Choice | Rationale |
|---|---|---|
| **Generation model — primary** | Claude Sonnet 4.6 via AWS Bedrock **ap-southeast-6 (Auckland)** if natively GA by Day 0; otherwise Bedrock ap-southeast-2 (Sydney) flagged in provenance | NZ-sovereign by preference; well-calibrated clinical text; cost-effective at 400-item scale |
| **Generation model — secondary (multi-model)** | Llama 3.3 70B Instruct on Catalyst Cloud Wellington (vLLM, A100 80 GB slice or L40S 48 GB) | Cross-family coupling guard (§9.2); strongest NZ-sovereign open option; ~30 % of items |
| **Storage format** | JSONL in the `nexwave-rd` private Git repo under `datasets/inbox-helper-synth-v1/` | <5 MB total; Git LFS unneeded; human-diffable; CI-friendly |
| **Labelling frontend** | Google Sheets bound via `tools/sheet_sync.py` (round-trip JSONL ⟷ CSV) | Frictionless for Ryo on weekends; supports dropdowns and version history |
| **Fallback labelling** | Self-hosted Label Studio on Ting's laptop | Only if Sheets conflict editing becomes painful |
| **Version control** | Git tags on `nexwave-rd` repo (`dataset-v0.1`, `dataset-v0.9-rc1`, `dataset-v1.0`) | Simpler than DVC at this scale |
| **QA runner** | `tools/qa_report.py` — Python + `pydantic` + `datasketch` (MinHash/LSH) + `sentence-transformers` + Microsoft Presidio | All open-source, CPU-only, single-command, gate-based exit codes |
| **CI** | GitHub Actions running `qa_report.py` on every push to the dataset directory | Blocks merge on any G1–G14 failure |
| **Privacy at rest** | Bedrock ap-southeast-6 (generation); local FileVault/BitLocker disk; private GitHub repo | No real patient data ever; sovereignty maintained throughout |

**Cost estimate.** ~400 items × ~600 output tokens × 2 passes (generate + paraphrase) ≈ 480 k output tokens. Sonnet 4.6 at ~$15/M output = ~$7. ~2 M input tokens × $3/M input = ~$6. Catalyst Cloud Llama 3.3 70B for the secondary 30 % share at L40S 48 GB ≈ $1.50/h × 8 h ≈ $12. **Total Sprint 2 generation spend < $50** — negligible against the $177 k Obj-1 budget.

### 10.3 JSONL schema v1.0

```json
{
  "id": "ihs-v1-000123",
  "schema_version": "1.0",
  "taxonomy_version": "sprint1-v2",
  "doc_type": "lab_result | radiology_report | discharge_summary | specialist_letter | patient_message",
  "synthetic_text": "string — full document text",
  "structured_fields": {
    "lab_analytes": [{"name": "potassium", "value": 6.5, "unit": "mmol/L", "ref_low": 3.5, "ref_high": 5.2, "flag": "H"}],
    "modality": null,
    "sender_role": "lab | radiology | hospital | specialist | patient",
    "nz_context": {"nhi_placeholder": "ZZI1234", "region": "Canterbury", "ethnicity": "NZ_European"}
  },
  "gold_label_urgency": "immediate | urgent | routine | information_only",
  "gold_label_rationale": "string — Ryo's 1–2 sentence justification",
  "gold_label_secondary": null,
  "boundary_case_flag": false,
  "contextual_reasoning_stress_flag": false,
  "difficulty": "clear | moderate | hard",
  "stratum": "stratum-id (per §4 stratification grid)",
  "generator": {
    "model": "claude-sonnet-4-6 | llama-3.3-70b-instruct",
    "family": "anthropic | meta",
    "host": "bedrock-ap-southeast-6 | catalyst-cloud-wlg",
    "prompt_template_id": "lab_result_urgent_v2",
    "prompt_hash": "sha256:abc...",
    "temperature": 0.8,
    "generated_at": "2026-04-15T09:34:21Z",
    "paraphrase_pass": true,
    "cross_family_canary": false
  },
  "labelling": {
    "labelled_by": "ryo",
    "labelled_at": "2026-04-18T11:22:00Z",
    "pass_number": 1,
    "relabelled_at": null,
    "relabel_reason": null
  },
  "qa": {
    "status": "pending | passed | flagged | failed",
    "schema_valid": true,
    "rule_checks": {"critical_token_consistency": "pass"},
    "near_duplicate_cluster_id": null,
    "calibration_set_member": false,
    "tfidf_probe_score": null
  },
  "splits": {
    "intended_split": "dev | eval | holdout"
  },
  "provenance_notes": "optional string"
}
```

**Design choices.** `taxonomy_version` enables surgical re-label after Sprint 1 GP feedback (§9.7). `gold_label_rationale` is separate from `gold_label_urgency` so rationale-only rewrites do not disturb the label audit history. `labelling.pass_number` and `relabelled_at` track lineage. `generator.prompt_template_id` + `prompt_hash` + `family` + `host` enable post-hoc shortcut and coupling diagnosis (§9.1, §9.2). `qa.calibration_set_member` keeps the calibration items co-located but flagged. `splits.intended_split` signals to Sprint 3 which items are for what purpose. New optional fields can be added by R5 follow-ups without breaking G1 schema validation.

### 10.4 Risks and contingencies

| ID | Risk | Likelihood | Impact | Mitigation | Fallback |
|---|---|---|---|---|---|
| **R1** | Sprint 1 GP review (rd-20260405-001) refines taxonomy mid-sprint | HIGH | MEDIUM | `taxonomy_version` field; calibration-set bridge re-label (~1 h GP); Day 8 reserved for impact assessment | 2-stage release: v1.0 with old taxonomy, v1.1 in Sprint 3 Week 1 |
| **R2** | GP labelling underestimated (>5 min/item) | MEDIUM | HIGH | 4 min/item floor with 60 h ceiling gives ~40 % slack | Reduce target to 350 items at Gate 1 |
| **R3** | Generator API outage (Bedrock or Catalyst) | LOW | MEDIUM | Two independent providers; exponential backoff in `generate.py` | Single-provider degraded mode; document in provenance |
| **R4** | Single-annotator drift | MEDIUM | MEDIUM | §5.4 calibration set, 3 rounds, κ ≥0.75 floor | Expand reconciliation from flagged-20 % to flagged-40 %; accept Gate 3 slip |
| **R5** | Shortcut learning / leakage not caught until Sprint 3 | MEDIUM | HIGH | Cross-family paraphrase canary; urgency-token scrub; TF-IDF probe; structural leakage test before Gate 4 | Document in datasheet; Sprint 3 ranking is relative not absolute |
| **R6** | Gate 1 fails and prompt iteration eats Day 3–4 | LOW | MEDIUM | 25 templates pre-written on Day 0; any of 5 per cell can be the winner | Reduce target to 300 items; preserve quality over volume |
| **R7** | QA script bugs block release | LOW | LOW | Toy dataset Day 0; CI on every commit | Manual gate run-down; document exceptions |
| **R8** | MBIE sovereignty challenge if Bedrock ap-southeast-6 not GA | LOW | HIGH | Catalyst Cloud Llama 3.3 70B Instruct as primary; document residency posture in datasheet | Day-0 1-page memo to MBIE if needed; release slip 3–5 days |

### 10.5 Release artefact structure

```
datasets/inbox-helper-synth-v1/
├── README.md                    # overview, quickstart, citation, licence
├── DATASHEET.md                 # Gebru et al. 2021 datasheet (7 sections)
├── SCHEMA.md                    # JSON schema reference
├── CHANGELOG.md                 # version history
├── LICENCE                      # project-internal use, no external redistribution
├── data/
│   ├── inbox_helper_synth_v1.jsonl              # full dataset (~400 items)
│   ├── inbox_helper_synth_v1_calibration.jsonl  # 25 calibration items (also in full)
│   └── splits/
│       ├── dev.jsonl
│       ├── eval.jsonl
│       └── holdout.jsonl
├── metadata/
│   ├── label_distribution.csv   # urgency × doc_type counts
│   ├── calibration_kappa.json   # intra-rater κ summary
│   ├── qa_report.json           # full G1–G14 gate output
│   ├── near_duplicates.json     # MinHash + embedding flagged pairs
│   ├── tfidf_probe.json         # back-classification leakage probe results
│   └── generation_manifest.json # prompts, templates, models, hosts
├── prompts/
│   ├── templates_v2.json        # all prompt templates used
│   └── persona_pool.json        # writer personas and tones
├── tools/
│   ├── generate.py
│   ├── sheet_sync.py
│   ├── qa_report.py
│   ├── calibration_kappa.py
│   ├── nhi.py                   # synthetic NHI generation with ZZI/ZIO prefix
│   └── requirements.txt
└── docs/
    ├── protocol.md              # this document, executable form
    ├── taxonomy.md              # urgency criteria, linked to Sprint 1 output
    └── known_limitations.md     # shortcut learning, coupling, spectrum bias, transfer gap
```

**Datasheet (Gebru et al. 2021) — 7 sections required:**
1. **Motivation** — why created, who funded (MBIE Endeavour), intended use.
2. **Composition** — 400 items, counts per urgency × doc_type cell, modalities present.
3. **Collection process** — synthetic generation pipeline, models used, prompt templates, no real patient data.
4. **Preprocessing / cleaning / labelling** — generation, paraphrase smoothing, labelling protocol, calibration.
5. **Uses** — Sprint 3 architecture evaluation only; **explicitly NOT** for training deployment models, NOT for clinical decision-support training, NOT for release outside NexWave R&D.
6. **Distribution** — internal only, MBIE grant IP, no external redistribution.
7. **Maintenance** — Ting owns; Ryo clinical authority; updates tagged in `CHANGELOG.md`.

Plus **Known Limitations** appended (Gebru's optional but recommended section): direct citations to §9 of this protocol — shortcut learning, generator–classifier coupling, spectrum bias, synthetic-to-real gap, training-data leakage, label structural leakage, single-annotator drift, hallucination, published cautionary cases.

## 11. References

References are grouped by topic. Citations marked **[verified]** are widely cited and load-bearing for this protocol; **[approximate]** indicates the parent agent or follow-up reader should double-check the exact venue/year if the citation becomes load-bearing in a downstream artefact (e.g. the `DATASHEET.md` or the Sprint 2 literature review deliverable).

### Synthetic clinical data and generation

- Walonoski, J. et al. (2018). "Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record." *JAMIA* 25(3): 230–238. **[verified]**
- Johnson, A.E.W. et al. (2016). "MIMIC-III, a freely accessible critical care database." *Scientific Data* 3: 160035. **[verified]**
- Lehman, E. et al. (2023). "Do we still need clinical language models?" *CHIL 2023*. **[verified]**
- Kweon, S. et al. (2024). "Publicly shareable clinical large language model built on synthetic clinical notes (Asclepius)." *arXiv*. **[approximate]**
- Tang, R. et al. (2023). "Does synthetic data generation of LLMs help clinical text mining?" *arXiv*. **[approximate]**
- Libbi, C.A. et al. (2021). "Generating synthetic training data for supervised de-identification of electronic health records." *Future Internet*. **[approximate]** — anchors §9.4 ~10-point synthetic-to-real F1 drop.
- Ive, J. et al. (2020). "Generation and evaluation of artificial mental health records for natural language processing." *npj Digital Medicine*. **[approximate]**
- Frontiers in Medicine (2025). "GPT-4o zero-shot generation of synthetic perioperative tabular data" — 92.31 % statistical parameter similarity to real data. **[approximate]** — exact citation should be verified by Ting before inclusion in Sprint 2 literature review.
- Choi, E. et al. (2017). "Generating multi-label discrete patient records using generative adversarial networks (medGAN)." *MLHC 2017*. **[verified]**
- Yoon, J. et al. (2020). "Anonymization through data synthesis using GANs (ADS-GAN)." *IEEE Journal of Biomedical and Health Informatics*. **[verified]**
- Jordon, J. et al. (2022). "Synthetic data — what, why and how?" Royal Society / Alan Turing Institute report. **[verified]** — anchors §9.4 ranking-stability argument.

### Annotation, labelling, and inter-rater agreement

- Landis, J.R. & Koch, G.G. (1977). "The measurement of observer agreement for categorical data." *Biometrics* 33(1): 159–174. **[verified]** — κ thresholds.
- Cicchetti, D.V. (1994). "Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology." *Psychological Assessment* 6(4): 284–290. **[verified]**
- Hripcsak, G. & Rothschild, A.S. (2005). "Agreement, the F-measure, and reliability in information retrieval." *JAMIA* 12(3): 296–298. **[verified]**
- Uzuner, Ö. et al. (2011). "2010 i2b2/VA challenge on concepts, assertions, and relations in clinical text." *JAMIA* 18(5): 552–556. **[verified]**
- Stubbs, A. et al. (2015). "Automated systems for the de-identification of longitudinal clinical narratives: Overview of 2014 i2b2/UTHealth shared task Track 1." *Journal of Biomedical Informatics* 58S. **[verified]**
- Apathy, N.C. et al. (2024). "Triage of patient portal messages using natural language processing." *JAMIA Open*. **[verified]** — recall-optimised "label up" convention.
- Rotenstein, L.S. et al. (2025). "Patient portal message triage with large language models." *JAMIA Open*. **[approximate]** — portal urgent-tail prevalence.

### Stratification, evaluation methodology, and spectrum bias

- Park, S.H. & Han, K. (2018). "Methodologic guide for evaluating clinical performance and effect of artificial intelligence technology for medical diagnosis and prediction." *Radiology* 286(3): 800–809. **[verified]** — two-track development/holdout.
- Hicks, S.A. et al. (2022). "On evaluation metrics for medical applications of artificial intelligence." *Scientific Reports* 12: 5979. **[verified]** — spectrum/borderline.
- Ransohoff, D.F. & Feinstein, A.R. (1978). "Problems of spectrum and bias in evaluating the efficacy of diagnostic tests." *NEJM* 299: 926–930. **[verified]**
- Willemink, M.J. et al. (2020). "Preparing medical imaging data for machine learning." *Radiology* 295(1): 4–15. **[verified]**
- Saerens, M. et al. (2002). "Adjusting the outputs of a classifier to new a priori probabilities: A simple procedure." *Neural Computation* 14(1): 21–41. **[verified]** — prior shift.

### Diversity and quality metrics

- McCarthy, P.M. & Jarvis, S. (2010). "MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment." *Behavior Research Methods* 42: 381–392. **[verified]**
- Pillutla, K. et al. (2021). "MAUVE: Measuring the gap between neural text and human text using divergence frontiers." *NeurIPS 2021*. **[verified]**
- Zhu, Y. et al. (2018). "Texygen: A benchmarking platform for text generation models." *SIGIR 2018*. **[verified]** — self-BLEU.
- Tevet, G. & Berant, J. (2021). "Evaluating the evaluation of diversity in natural language generation." *EACL 2021*. **[verified]**
- Gretton, A. et al. (2012). "A kernel two-sample test." *JMLR* 13: 723–773. **[verified]** — MMD.

### Failure modes — shortcut learning, coupling, dataset shift

- Geirhos, R. et al. (2020). "Shortcut learning in deep neural networks." *Nature Machine Intelligence* 2: 665–673. **[verified]**
- Niven, T. & Kao, H.-Y. (2019). "Probing neural network comprehension of natural language arguments." *ACL 2019*. **[verified]**
- McDermott, M.B.A. et al. (2021). "Reproducibility in machine learning for health research." *Science Translational Medicine* 13(586): eabb1655. **[verified]**
- Shumailov, I. et al. (2024). "AI models collapse when trained on recursively generated data" / "The curse of recursion." *Nature* 631: 755–759. **[verified]**
- Alemohammad, S. et al. (2023). "Self-consuming generative models go MAD." *arXiv* 2307.01850. **[verified]**
- Finlayson, S.G. et al. (2021). "The clinician and dataset shift in artificial intelligence." *NEJM* 385: 283–286. **[verified]**
- Rajkomar, A. et al. (2018). "Scalable and accurate deep learning with electronic health records." *npj Digital Medicine* 1: 18. **[verified]**
- Abdalhalim, A. et al. (2025). "Validation-to-deployment performance gaps in clinical NLP." **[approximate]** — cited for the 8–15-point sensitivity drop figure; verify before quoting in Sprint 2 literature review.

### Memorisation and training-data leakage

- Carlini, N. et al. (2021). "Extracting training data from large language models." *USENIX Security 2021*. **[verified]**
- Carlini, N. et al. (2023). "Quantifying memorization across neural language models." *ICLR 2023*. **[verified]**

### Published cautionary clinical-ML cases

- Wong, A. et al. (2021). "External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients." *JAMA Internal Medicine* 181(8): 1065–1070. **[verified]** — Epic sepsis model.
- Strickland, E. (2019). "IBM Watson, heal thyself: How IBM overpromised and underdelivered on AI health care." *IEEE Spectrum*. **[verified]**
- Beede, E. et al. (2020). "A human-centered evaluation of a deep learning system deployed in clinics for the detection of diabetic retinopathy." *CHI 2020*. **[verified]**
- Obermeyer, Z. et al. (2019). "Dissecting racial bias in an algorithm used to manage the health of populations." *Science* 366(6464): 447–453. **[verified]**
- Seyyed-Kalantari, L. et al. (2021). "Underdiagnosis bias of artificial intelligence algorithms applied to chest radiographs in under-served patient populations." *Nature Medicine* 27: 2176–2182. **[verified]**

### NHS / clinical real-world LLM evaluation

- "NHS primary care medication safety review with GPT-oss-120b." *arXiv* 2512.21127, October–November 2025. **[approximate]** — 178 failures across 148 patients; **contextual reasoning failures outnumber factual errors 6:1**. Anchors §3 contextual-stress subset and §9.3 spectrum bias.

### Datasheets and dataset documentation

- Gebru, T. et al. (2021). "Datasheets for datasets." *Communications of the ACM* 64(12): 86–92. **[verified]**

### NZ standards, ethics, and clinical realism

- HISO 10046 — NHI format and check-digit specification. NZ MoH. **[verified]**
- HISO 10040.2 — HL7 v2.4 messaging standard for laboratory results in NZ. **[verified]**
- HISO 10015 — eDischarge CDA R2 implementation guide. NZ MoH. **[verified]**
- HISO 10001 — Ethnicity Data Protocols. NZ MoH 2017. **[verified]**
- HISO 10029 — Health Information Security Framework. NZ MoH. **[verified]**
- HISO 10064 — Health Information Governance Guidelines. NZ MoH. **[verified]**
- NEAC (2022). National Ethical Standards for Health and Disability Research and Quality Improvement. **[verified]**
- Te Mana Raraunga — Māori Data Sovereignty Network principles. **[verified]**
- Vision Mātauranga policy framework. MBIE. **[verified]**
- Office of the Privacy Commissioner (NZ), 2023 and 2024 guidance on AI and the Information Privacy Principles. **[verified]**
- UK ICO (2023). Anonymisation, pseudonymisation and privacy enhancing technologies guidance. **[verified]**
- NHS England (2022). Artificial Data Pilot release notes. **[approximate]**
- NIH/NIAID (2022). Synthetic data initiatives in biomedical research. **[approximate]**
- RCPA / AACB harmonised critical-result thresholds. **[verified]**
- RANZCR clinical radiology reporting standards (BI-RADS, Lung-RADS, LI-RADS, PI-RADS, TI-RADS). **[verified]**
- BPAC NZ — Best Practice Advocacy Centre clinical guidelines. https://bpac.org.nz **[verified]**
- NZULM — New Zealand Universal List of Medicines. **[verified]**
- Pharmac Schedule. **[verified]**
- HealthPathways NZ — regional clinical pathways. **[verified]**
- Cunningham, R. et al. (2023). "Equity considerations in NZ primary care AI." *NZMJ*. **[approximate]**

### Tooling references (no academic citations needed)

- Microsoft Presidio — https://github.com/microsoft/presidio
- `datasketch` (MinHash / LSH in Python) — https://github.com/ekzhu/datasketch
- `sentence-transformers` — https://www.sbert.net
- `pydantic` — https://docs.pydantic.dev
- AWS Bedrock documentation, Asia Pacific (New Zealand) ap-southeast-6 region.
- Catalyst Cloud documentation — https://catalystcloud.nz
- vLLM — https://github.com/vllm-project/vllm

---

**End of R5 — Synthetic NZ GP Inbox Dataset Generation Protocol.**

This protocol is **provisional** pending Sprint 1 GP clinical review feedback (rd-20260405-001, due Day 8 Mon 20 Apr 2026). The `taxonomy_version` schema field, the calibration-set bridge mechanism (§5.4), and the Day-8 impact-assessment slot in §10.1 together enable surgical absorption of taxonomy refinements without rerunning the full pipeline. All other design choices — generation, stratification, labelling protocol, privacy techniques, NZ realism, QA gates, failure-mode mitigations, executable schedule — are stable and ready to execute on the Sprint 2 Monday.
