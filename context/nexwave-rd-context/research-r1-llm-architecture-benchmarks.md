---
title: "R1 — Clinical LLM Architecture Benchmarks (2024–2026)"
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-10
status: final
---

# R1 — Clinical LLM Architecture Benchmarks for Document Classification (2024–2026)

**Sprint 2 research deliverable.** Empirical literature review covering LLM architecture approaches, published benchmarks, recall-optimisation techniques, long-document handling, GP inbox triage studies, real-world failure modes, and cost/latency/throughput for clinical document classification. Produced by Claude Code research agents (5 parallel searches, 280+ web sources consulted).

---

## 1. Executive Summary

Five findings that matter most for our architecture shortlist:

1. **Fine-tuned small models dramatically outperform zero-shot large models for classification.** With just 200–500 labelled examples, LoRA fine-tuned 8B models achieve F1 0.95–0.97 vs F1 0.34–0.40 for zero-shot SLMs on the same tasks (arXiv 2504.21191). An 8B fine-tuned model (UrgentSFT-8B) outperforms GPT-OSS 120B on patient message triage (PMR-Bench, arXiv 2601.13178). This means our 300–500 synthetic items may be sufficient for a competitive fine-tune.

2. **The dominant failure mode is contextual reasoning, not factual errors — 6:1 ratio.** The NHS primary care medication review (arXiv 2512.21127, GPT-oss-120b, Oct–Nov 2025) found 153 contextual failures vs 25 factual errors across 148 patients. The model knew the medicine but failed to apply it in context — overconfidence, failure to adjust for individual patients, misunderstanding delivery workflows, unsafe intervention sequences. This pattern is replicated across the literature (MIT Media Lab: 64–72% of residual hallucinations are causal/temporal reasoning failures).

3. **Chain-of-thought prompting DEGRADES clinical text performance in 86% of models.** A landmark study of 95 LLMs on 87 clinical text tasks (arXiv 2509.21933) found 86.3% of models suffered consistent performance degradation with CoT. Only the most capable models remained robust. Do not use CoT for classification by default.

4. **Knowledge-practice gap is massive.** LLMs score 84–90% on knowledge benchmarks (USMLE-style) but only 45–69% on practice benchmarks (JMIR 2025 review of 39 benchmarks). Vignette-to-dialogue accuracy drops 19.3 percentage points. Real-world ED triage at scale (39,375 patients, JCM 2026): best model (Claude Sonnet 4) achieves only kappa 0.467.

5. **No published benchmark exists for GP inbox document triage** (heterogeneous document types classified by urgency). Patient message triage is well-studied; GP inbox triage of labs + radiology + discharge summaries + specialist letters is a genuine research gap we will partially fill.

---

## 2. Architecture-by-Architecture Empirical Summary

### 2.1 Zero-Shot Prompting with Frontier LLMs

| Study | Task | Model | Result |
|---|---|---|---|
| Computers in Biology and Medicine 2025 | Clinical phenotyping (20 conditions) | GPT-4o | Recall 0.97, macro F1 0.92 |
| BMC Cancer 2024 | Breast cancer pathology | GPT-4 | Macro F1 0.83 (vs LSTM 0.75) |
| JMIR 2024 (Sorich et al.) | 48 clinical vignettes, triage | Claude 3.5 Sonnet | Triage accuracy 94% (45/48) |
| JMIR 2024 (Sorich et al.) | 48 clinical vignettes, triage | GPT-4o | Triage accuracy 92% (44/48) |
| arXiv 2504.08040 | MIMIC-IV ICD-10 classification | Non-reasoning models | Accuracy 68%, F1 60% |

**Bottom line:** Zero-shot with frontier models achieves F1 0.75–0.92 on clinical classification depending on task complexity. Sufficient for prototyping, unlikely to meet ≥99% sensitivity targets without enhancement. Over-triage is the common error pattern (safer direction).

### 2.2 Few-Shot In-Context Learning

| Study | Task | Technique | Improvement |
|---|---|---|---|
| JAMIA 2025 | Clinical note section classification | Dynamic few-shot (embedding retrieval) | +39.3% macro F1 over zero-shot; +21.1% over static few-shot |
| J Med Syst 2025 (Xu et al.) | 48 vignettes, 4 triage levels, 8 LLMs | Structured prompting (47 exemplars) | 76.82% → 86.20% triage accuracy |
| BRIDGE benchmark 2025 | 87 clinical tasks, 95 LLMs | Few-shot vs zero-shot | 43.8% → 55.5% (best model, +26.7%) |

**Bottom line:** Dynamic few-shot with embedding-based retrieval of similar classified documents is the most effective prompting strategy. Build a curated exemplar bank of 50–100 documents per urgency level, retrieve 3–5 most similar at inference. Expect 20–40% F1 improvement over zero-shot.

### 2.3 RAG (Retrieval-Augmented Generation)

| Study | Task | Result | Notes |
|---|---|---|---|
| Nature 2025 (npj) | Medical fitness assessment + guidelines | 96.4% accuracy (vs 86.6% human), 0% hallucination | GPT-4 with international guideline RAG |
| JAMIA 2025 (Chen et al.) | Emergency detection in patient messages | Accuracy 0.99, Sensitivity 0.98, Specificity 0.99 | GPT-4o + Knowledge Graph RAG |
| npj Digital Medicine 2025 | 2,000 MIMIC cases triage | RAG-Assisted Claude 3.5 Sonnet best on exact-match triage | 30M PubMed abstracts |
| CLPsych 2025 | Mental health classification | 47–56% accuracy; 64% with high-quality retrievals, 31% with poor | RAG unreliable for classification |
| arXiv 2505.20320 | Clinical NLP cost reduction | >90% cost reduction, no accuracy loss (p > 0.05) | "Less Context, Same Performance" |

**Bottom line:** RAG excels for knowledge grounding and justification but is unreliable as the primary classification mechanism. Best used to inject current NZ clinical guidelines into the reasoning layer for ambiguous cases. The Chen et al. KG-RAG result (0.99 accuracy, 0.98 sensitivity on emergency detection) is exceptional but used a curated triage knowledge graph, not generic retrieval.

### 2.4 Fine-Tuning (LoRA, QLoRA, Domain-Specific Models)

| Study | Task | Finding |
|---|---|---|
| arXiv 2406.08660 | Multiple classification tasks | Fine-tuned RoBERTa-large outperforms zero-shot GPT-4/Claude at N=200 training samples |
| arXiv 2504.21191 | Healthcare classification | Zero-shot SLM F1 0.34–0.40; fine-tuned SLM F1 0.95–0.97. Saturates at ~200 labels |
| arXiv 2503.21349 | Cardiology reports, LoRA on Llama3-8B | Notable gains at 200–300 training examples |
| npj Digital Medicine 2025 | Perioperative complication detection, LoRA | F1 >0.64 across all doc lengths; human performance declined from 0.73 to 0.45 on long docs |
| arXiv 2506.10896 | BioClinical ModernBERT (150M/396M params) | SOTA on 4/5 clinical NLP tasks, 8,192 token context, trained on 53.5B clinical tokens |
| JMIR AI 2025 (CLEVER) | Clinical text tasks | 8B domain-specific model (MedS) preferred over GPT-4o by physicians 45–92% more often |
| JMIR 2025 | SFT + DPO on Llama3/Mistral2 | +7–8% clinical reasoning accuracy over SFT alone |
| Springer 2025 | BLURB benchmark, LoRA/QLoRA | Improved macro scores using only 30–32M trainable params (vs 3B full), 60% less GPU memory |

**Bottom line:** This is the strongest approach for classification. With 200–500 labelled examples per class (800–2,000 total), LoRA fine-tuned models will likely outperform zero-shot frontier models. BioClinical ModernBERT (396M params, 8K context) is a strong encoder candidate — fast, cheap, SOTA on clinical NLP. The minimum viable dataset of 200 per class is achievable from our synthetic data budget.

### 2.5 Hybrid Rules + LLM

| Study | Task | Finding |
|---|---|---|
| Research Square 2025 | Acute ischemic stroke treatment | +18.9% treatment accuracy over standalone LLMs; safety score 4.36/5; low hallucination (10.9%) |
| Cell Press 2025 | Medication safety across 16 specialties | Human+LLM co-pilot superior to either alone |
| Computers in Biology and Medicine 2025 | Clinical phenotyping | Rules: precision 0.92, recall 0.36. LLM: recall 0.97, precision lower. Combined optimises both |
| UK GP Triage (Smart Triage) | Real-world GP inbox | 73% reduction in waiting times, 47% fewer phone calls at peak; 30+ NHS ICBs |

**Bottom line:** Recommended safety architecture. Route deterministic cases via rules (lab flags → Urgent, routine referral ack → Information only). Use LLM only for ambiguous cases requiring semantic reading. Provides audit trails, explainability, and regulatory defensibility. The UK Smart Triage deployment is the closest real-world precedent.

### 2.6 Chain-of-Thought / Extended Thinking / Self-Consistency

| Study | Task | Finding |
|---|---|---|
| arXiv 2509.21933 (landmark) | 95 LLMs, 87 clinical text tasks, 9 languages | **86.3% of models degraded with CoT prompting.** Only the most capable remained robust |
| Health and Technology 2026 | ICD-10 classification, 8 LLMs | Reasoning models: 71% acc / 67% F1; non-reasoning: 68% acc / 60% F1. But non-reasoning more consistent (91% vs 84%) |
| Nature Communications 2025 | Self-consistency on clinical cases | Correct responses avg 2.25 unique answers vs 2.91 incorrect (Cohen's d=0.90). Useful as confidence signal |
| medRxiv 2025 (BiasMedQA) | Cognitive bias, 1,273 vignettes | Forewarning decreased bias by only 6.9% despite 50% longer responses discussing biases 100x more |

**Bottom line:** Do NOT use CoT prompting by default for classification — the 86.3% degradation risk is unacceptable. Consider: (a) self-consistency voting (3–5 samples) as a confidence calibration mechanism for borderline cases only, (b) CoT during fine-tuning rather than inference, (c) reasoning models selectively for ambiguous cases flagged by the primary classifier.

### 2.7 Agentic / Multi-Agent Architectures

| Study | Task | Finding |
|---|---|---|
| Nature Cancer 2025 | Oncology decision-making | GPT-4 alone: 30.3% accuracy; agentic with tools: 87.2% (+56.9pp). Tool use accuracy 87.5% |
| npj Health Systems 2026 | Clinical workload scaling | Multi-agent: 90.6% accuracy at 5 tasks, 65.3% at 80 tasks. Single-agent: 73.1% → 16.6% at 80 tasks. Token usage reduced up to 65-fold |
| NEJM AI 2025 (MedAgentBench) | 300 EHR tasks, 12 LLMs | Best: Claude 3.5 Sonnet v2 at 69.67%. Retrieval tasks (85.33%) outperformed action tasks |
| arXiv 2603.04421 (2026) | Mixed-vendor multi-agent diagnosis | Mixed-vendor configurations outperformed single-vendor; complementary biases surface missed diagnoses |

**Bottom line:** Lightweight agentic architecture is appropriate for the full inbox triage pipeline: (1) document type classifier, (2) content extraction, (3) urgency classification, (4) verification/confidence. The 65-fold token reduction under load and 56.9pp accuracy boost from tool use are compelling. However, for the core classification task alone, single-model fine-tuning is simpler and sufficient. Reserve multi-agent for the end-to-end pipeline.

### 2.8 Summary: "Fine-Tune for Format, RAG for Knowledge"

The 2025–2026 consensus is confirmed across multiple production guides and research papers:

- **Fine-tune for:** classification logic, output format, document type recognition, routing decisions
- **RAG for:** evolving clinical guidelines, drug interaction databases, protocol updates, NZ-specific triage criteria
- **Agents for:** multi-step workflows, tool use, verification, pipeline orchestration

This separation means guidelines can be updated without retraining, while classification behaviour remains consistent.

---

## 3. Published Clinical Document Classification Benchmarks (2024–2026)

### 3.1 BRIDGE — Comprehensive Clinical LLM Benchmark

**Wu et al., arXiv 2504.19467 (Apr 2025); Harvard Medical School / Brigham and Women's Hospital.**

- 87 tasks, 9 languages, >1 million samples, 14 clinical specialties, 8 task types, 6 clinical stages, 20 applications including triage and referral
- 95 LLMs tested (DeepSeek-R1, GPT-4o, Gemini series, Qwen3 series, etc.)
- **Best overall: Gemini-1.5-Pro at 55.5% (few-shot), up from 43.8% (zero-shot) — +26.7% improvement**
- Best medically fine-tuned: Baichuan-M1-14B-Instruct (36.08 zero-shot, 48.3 few-shot)
- Open-source models comparable to proprietary; older fine-tuned medical LLMs underperform updated general models
- Few-shot is the most effective inference strategy across the board
- Per-task triage breakdowns are in the BRIDGE Medical Leaderboard on HuggingFace

### 3.2 Structured Prompting Triage Vignettes — Most Directly Comparable

**Xu, Zhao, Huang. J Med Syst 49(141), 2025. DOI: 10.1007/s10916-025-02284-y.**

- 48 single-turn clinical vignettes, **4 triage levels (Emergent / 1-day / 1-week / Self-care)** — exact match to our urgency taxonomy
- 8 LLMs: ChatGPT-4, ChatGPT-o1, DeepSeek-V3, DeepSeek-R1, Gemini-2.0, Copilot, Grok-2, Llama-3.1
- Method: 47-of-48 leave-one-out exemplar provision (structured prompting)
- **Mean triage accuracy: 76.82% → 86.20% with structured prompting**
- Mean diagnostic accuracy: 89.84% → 91.67%
- Best diagnostic: 93.75% (ChatGPT-o1, DeepSeek-R1, Grok-2 with prompting)
- Safety of advice: 89.06% → 94.53%
- **Over-triage rose 53.15% → 65.62% (favours safety)**

### 3.3 ICPC-2 Coding Benchmark — Direct NZ GP Relevance

**de Almeida et al., arXiv 2507.14681 (Jul 2025); accepted at NeurIPS 2025.**

- 437 Brazilian Portuguese clinical expressions; semantic search over 73,563 ICPC-2 concepts
- 33 LLMs evaluated
- **28 models F1 > 0.8; 10 exceeded 0.85**
- Top performers: gpt-4.5-preview, o3, gemini-2.5-pro
- Smaller models (<3B) struggled with formatting and input length
- Retriever optimisation can add up to 4 points
- **Highly relevant:** ICPC-2+ is the standard classification used in most NZ PMS systems

### 3.4 PMR-Bench — Patient Portal Message Triage (most directly relevant)

**Gatto, Seegmiller, Burdick et al., arXiv 2601.13178 (Jan 2026).**

- Novel pairwise ranking formulation: "which message is more urgent?" tournament-style inbox re-sort
- **1,569 unique messages, 2,000+ test pairs** (PMR-Reddit, PMR-Synth, PMR-Real)
- Two model classes: UrgentReward (Bradley-Terry) and UrgentSFT (supervised fine-tuning)
- **UrgentSFT-8B: +15 point boost on inbox sorting metrics over off-the-shelf 8B models**
- **UrgentReward-8B: +16 point boost**
- **UrgentReward-8B outperforms GPT-OSS 120B on this task — small fine-tunes can beat very large open models**
- Achieves 95% of larger fine-tuned LLM performance
- Open dataset and code available

### 3.5 LCD Benchmark — Long Clinical Documents

**Yoon, Chen, Gao, Dligach, Bitterman, Afshar, Miller. medRxiv 2024.03.26; published JAMIA 32(2), Feb 2025.**

- 7,568 patients from MIMIC-IV v2.28; discharge notes median 1,687 words (~2,250 tokens)
- Severe class imbalance (negative:positive ~26:1) — 30-day mortality
- Models: SVM (BoW), CNN, hierarchical transformer, Mixtral-8x7B (zero-shot), GPT-4 (zero-shot)
- **Best supervised F1: 28.9% (CNN). GPT-4 zero-shot F1: 32.2% — outperformed all supervised baselines**
- Mixtral-8x7B zero-shot F1: 22.3%
- The paper notes "benchmark datasets targeting long clinical document classification tasks are absent" — confirming a gap

### 3.6 EHRNoteQA — Long-Context Clinical QA

**Kweon et al., NeurIPS 2024 Datasets & Benchmarks Track. arXiv 2402.16040.**

- 962 QA pairs over MIMIC-IV discharge summaries; questions span multiple admissions
- **Level 1 (~4k tokens) vs Level 2 (~8k tokens)**
- 8 clinical topics; QA generated by GPT-4, refined by 3 clinicians; 27 LLMs tested
- **GPT-4: 97.16% (L1 multi-choice), 95.15% (L2 multi-choice), 91.30% (L1 open-ended), 89.61% (L2 open-ended)**
- Performance decreases with multi-note synthesis
- **Highest correlation with clinician-evaluated performance of any benchmark (Spearman 0.78, Kendall 0.62)**

### 3.7 CLEVER — Clinical LLM Evaluation by Expert Review

**Kocaman, Kaya, Feier, Talby (John Snow Labs). JMIR AI 2025, e72153.**

- 500 test cases curated by 4 medical experts; blind randomised preference-based evaluation
- GPT-4o vs MedS (8B) and MedM (70B) from John Snow Labs
- 3 dimensions: factuality, clinical relevance, conciseness
- **Physicians preferred MedS (8B) over GPT-4o by 45%–92% across dimensions**
- Validated via interannotator agreement, ICC, washout periods
- **Demonstrates small on-premise domain models can outperform large general-purpose LLMs for clinical NLP**

### 3.8 Frontier LLM Triage Accuracy (Sorich et al.)

**Sorich, Mangoni, Bacchi, Menz, Hopkins. JMIR 2024, e67409.**

- 48 Levine et al. clinical vignettes; GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Triage accuracy: GPT-4o 92%, Claude 3.5 Sonnet 94%, Gemini 1.5 Pro 92%**
- Top-3 diagnostic: GPT-4o 98%, Claude 3.5 Sonnet 100%, Gemini 1.5 Pro 98%
- Frontier LLMs (92.4%) comparable to PCPs (91.3%), much better than lay (74.1%)
- **Most common error: overestimating urgency (over-triage)**

### 3.9 LLM Triage at Scale — 39,375 Patients

**JCM 15(4):1512, AHEPA University Hospital Greece (Jun 2024 – Jul 2025).**

- 7 LLMs: ChatGPT-5 Thinking/Instant, Gemini 2.5, Qwen 3, Grok 4.0, DeepSeek v3.1, Claude Sonnet 4
- **Best: DeepSeek and Claude Sonnet 4 (κ_w ~0.467; raw ESI accuracy 61.7%)**
- Claude Sonnet 4 best for clinic referral (67.1%, κ=0.619)
- ChatGPT-5 Instant: κ_w 0.176 (near-random)
- Ophthalmology subgroup: up to 81% accuracy
- **Demonstrates the brutal gap between vignette accuracy (92–94%) and real-world ED performance (~62%)**
- Better in anatomically-defined and paediatric cases; struggled with severity-based triage

### 3.10 Knowledge-Embedded LLMs for ED Triage

**Knowledge-Based Systems 2025; Sequential Domain and Task Adaptation (SDTA) on Qwen2.5-72B.**

- MIMIC-IV + MIETIC corpus
- **ESI-1/ESI-2 (critical): perfect recall (1.00)**
- **ESI-3 (moderate): F1 = 0.92**
- **ESI-4/ESI-5 (non-urgent): precision = 0.95**
- Fine-tuned models surpassed emergency nurse and physician-level accuracy
- **This is the architecture template for our ≥99% sensitivity Immediate/Urgent target**

### 3.11 GPT-4 Pairwise Acuity — JAMA Network Open

**JAMA Network Open, May 2024. 251,401 ED visits, balanced 10,000 pairs.**

- **GPT-4 correctly inferred higher-acuity patient: 89% (8,940/10,000)**
- 500-pair clinician subsample: LLM 88% vs physician 86%
- GPT-4 assigned lower median ESI (2.0) vs humans (3.0) — overestimates severity (safer)

### 3.12 ChatGPT Health Triage Stress Test

**Nature Medicine, Feb 2026. 60 vignettes, 21 domains, 16 factorial conditions, 960 responses.**

- **Inverted U-shaped failure pattern: nonurgent 35% error, emergency 48% error**
- **52% of gold-standard emergencies undertriaged**
- Anchoring bias: when family minimised symptoms, triage shifted less-urgent (OR=11.7, 95% CI 3.7–36.6)
- Crisis intervention messages activated unpredictably across suicidal ideation cases
- Classical emergencies (stroke, anaphylaxis) correctly triaged

### 3.13 HealthBench (OpenAI, May 2025)

**arXiv 2505.08775. 5,000 multi-turn conversations, 48,562 rubric criteria, 262 physicians.**

- **GPT-3.5 Turbo: 16% — GPT-4o: 32% — o3: 60%**
- Safety performance (54.7% ± 26.1%) lower than effectiveness (62.3% ± 22.3%)
- Emergency referrals and tailored communication are relative strengths

### 3.14 Reasoning vs Non-Reasoning LLMs for ICD-10 Classification

**Mustafa et al., arXiv 2504.08040 / Health and Technology 2026.**

- 8 LLMs on MIMIC-IV discharge summaries
- Reasoning models: 71% accuracy, 67% F1
- Non-reasoning models: 68% accuracy, 60% F1
- **Best: Gemini 2.0 Flash Thinking at 75% accuracy, 76% F1**
- Non-reasoning models showed greater consistency (91% vs 84%)

### 3.15 Knowledge-Practice Gap Systematic Review

**JMIR 2025, e84120. 39 benchmarks analysed (2017–2025).**

- Knowledge-based benchmarks: 21 (54%); Practice-based: 15 (38%); Hybrid: 3 (8%)
- **Knowledge benchmarks performance: 84–90%**
- **Practice benchmarks performance: 45–69%**
- Specific: DiagnosisArena 45.82%, MedAgentBench 69.67%, HealthBench 60%
- **Diagnostic accuracy drops from 82% (vignettes) → 62.7% (multi-turn dialogues): −19.3 percentage points**
- 26% of benchmarks had incomplete methodological reporting

### 3.16 MedAgentBench — Virtual EHR Environment

**NEJM AI 2025. 300 tasks, 100 patient profiles, 700,000+ FHIR data elements.**

- 12 LLMs evaluated
- **Best: Claude 3.5 Sonnet v2 at 69.67% success rate**
- Retrieval tasks (85.33%) significantly better than action tasks
- Useful proxy for our care gap detection task (FHIR resource navigation)

### 3.17 Note: No Care Gap Detection Benchmark Found

Despite extensive searching, **no dedicated benchmark exists for LLM-based care gap detection**. MedAgentBench's FHIR-navigation tasks are the closest proxy. This is a research gap our Care Gap Finder partially addresses.

---

## 4. Recall-Optimisation Techniques for Safety-Critical Classification

Our targets are ≥99% sensitivity on Immediate and Urgent classes — well above what zero-shot LLMs reliably achieve. Published techniques for pushing recall to safety-critical levels fall into five families.

### 4.1 Asymmetric and Focal Loss Functions

- **Focal Loss (Lin et al., ICCV 2017, still the dominant baseline 2024–2026)** — down-weights well-classified examples so training focuses on hard minority-class items. Standard for class imbalance in clinical classification.
- **Unified Focal Loss / Focal Tversky Loss (Yeung et al. 2022, widely adopted in clinical NLP 2024–2025)** — combines Tversky index (asymmetric FN/FP weighting) with focal exponent. Allows explicit penalty multiplier for false negatives — directly relevant for our recall-optimised constraint.
- **Asymmetric Loss (Ridnik et al. 2021, applied to clinical multi-label 2024–2026)** — separate γ for positive vs negative examples; can be tuned to drive sensitivity to ≥99% at controlled precision cost.
- **Cost-sensitive learning** (Springer AI Review 2024 survey, "Cost-sensitive learning for imbalanced medical data: a review") — explicit class-weighted cross-entropy with cost ratios derived from the clinical cost matrix (missed urgent ≫ over-triage). Standard recommendation for safety-critical recall.

### 4.2 Calibration and Threshold Tuning

- **Per-class threshold tuning** — train with standard cross-entropy, then post-hoc adjust class-specific decision thresholds on a held-out calibration set to achieve target sensitivity. Simpler than asymmetric loss; widely used in clinical triage.
- **Platt scaling / temperature scaling / isotonic regression** — calibrate raw model logits before threshold tuning. JMIR Medical Informatics 2025 found LLMs systematically miscalibrated on clinical tasks (verbalised confidence inversely correlated with accuracy, r ≈ −0.40), making post-hoc calibration mandatory before threshold-based recall optimisation.
- **Specialty-aware calibration** (Hagmann et al., EACL 2026, arXiv 2506.10769) — calibration parameters fitted per clinical specialty; substantially reduced ECE on medical QA vs global calibration.

### 4.3 Selective Prediction, Abstention, and Conformal Prediction

- **MedAbstain (arXiv 2601.12471, 2026)** — fine-tunes a small abstention head on top of a frozen LLM to refer hard cases to human review. Demonstrated safe operation at recall thresholds infeasible without abstention. Directly applicable to our "GP reviews everything but borderline cases get a second-opinion flag" workflow.
- **Conformal prediction for clinical NLP** (Angelopoulos et al., NeurIPS 2024 tutorial; multiple 2024–2026 clinical applications) — produces statistically guaranteed prediction sets at a chosen confidence level (e.g. 99%). Provides distribution-free recall guarantees. Standard recommendation for safety-critical clinical AI in 2025–2026.
- **Selective prediction with learned rejection** (JAMIA 2024 survey on LLM safety in clinical NLP) — combines abstention with calibrated confidence; achieves target sensitivity by deferring the bottom k% of confident-but-wrong predictions to human review.
- **I-CALM (Iterative Clinical-Aware Loss Modulation, arXiv 2604.03904, 2026)** — combines focal loss with iterative reweighting based on per-epoch error patterns; reported sensitivity gains of 4–8 points on minority clinical classes vs baseline focal loss.

### 4.4 Ensemble and Verification Architectures

- **Multi-model ensembles** — independent classifiers (different bases or different prompts) combined by max-recall voting. Standard recall booster; cost multiplier 2–5×.
- **Self-consistency** (Wang et al., ICLR 2023; clinical applications 2024–2025) — sample N CoT traces and majority-vote. Improves robustness but can mask high-confidence wrong answers. **Caution:** NHS GPT-oss-120b study found self-consistency did not catch contextual reasoning failures because the model was wrong with high consistency.
- **Verification agent / second-opinion architectures** (multiple 2025 multi-agent papers) — primary classifier outputs label + reasoning; verifier agent independently checks reasoning against retrieved evidence. Adds latency but is the strongest published mitigation for the contextual reasoning failure mode (Section 7).
- **Hybrid rules + LLM with rule-mandated escalation** — deterministic rules over critical fields (e.g. critical lab thresholds from RCPA/AACB) trigger Immediate regardless of LLM output. Removes the worst-case LLM miss for cases where the rule fires. Recommended baseline for our Inbox Helper.

### 4.5 Ordinal Classification Methods (relevant to our 4-level urgency)

- **CORAL / CORN ordinal regression** (Cao, Mirjalili, Raschka, Pattern Recognition Letters 2020 / 2023; clinical applications 2024–2025) — replaces categorical cross-entropy with rank-consistent binary classifiers. Preserves ordinal structure (Immediate > Urgent > Routine > Information), produces monotonic probabilities, improves QWK by 5–15% over flat classification on benchmarks.
- **Ordinal focal loss** — focal loss adapted to ordinal labels via cumulative link models. Useful when distance-aware penalty matters (under-triage by 2 levels worse than by 1).
- **Distance-weighted loss** — assigns penalty proportional to distance between predicted and true urgency level. Aligns training objective with QWK evaluation metric.

### 4.6 Data-level Recall Boosters

- **Oversampling minority classes** (SMOTE for tabular; back-translation, paraphrase augmentation, LLM-generated synthetic minority examples for text) — established practice; gains 2–5 points sensitivity on minority classes.
- **Stratified enriched training set** — what our Sprint 2 synthetic dataset already does (100–150 per class per doc type). Confirmed best practice for safety-critical minority classes (Sun et al. 2024 systematic review of clinical NLP class imbalance).
- **Hard negative mining** — train, identify false negatives in held-out set, oversample similar items in next epoch. Useful for boundary cases.

### 4.7 Recommended Recall-Optimisation Stack for Inbox Helper

Based on the evidence, the recommended Sprint 3 baseline for hitting ≥99% sensitivity is:

1. **Asymmetric / focal loss** (Unified Focal or Asymmetric Loss with FN penalty 5–10×) — training-time
2. **Per-class threshold tuning** on a held-out calibration set — post-training
3. **Conformal prediction wrapper** for distribution-free recall guarantees at 99% — inference-time
4. **Hybrid rule overlay** — RCPA/AACB critical lab thresholds force Immediate regardless of LLM output
5. **Verification agent** for borderline cases (LLM confidence below threshold) — inference-time
6. **CORAL ordinal head** for native 4-level ordinal output — architectural

Each layer is independently published; the combination is not, so Sprint 3 evaluation should ablate each layer.

---

## 5. Long-Document and Unstructured Clinical Text Handling

Three of our five Inbox Helper document types (discharge summaries, specialist letters, patient messages) require full-document semantic reading. Discharge summaries in particular can run 5–15k tokens. The published evidence on long-context LLM behaviour is consistent and unflattering.

### 5.1 The "Lost in the Middle" Effect (Liu et al., TACL 2024)

The single most-cited paper on long-context degradation. Key findings replicated repeatedly through 2025–2026:

- LLMs are most accurate when relevant information is at the **beginning or end** of the context window
- Accuracy drops **>30 percentage points** when relevant information is in the middle of a long document
- The effect is present in all models tested, including GPT-4 and Claude
- Effect worsens with longer context, even far below the model's nominal limit

**Implication for Inbox Helper:** Discharge summary action items often appear in narrative middle (Plan section, Day 3 of stay, embedded in a medication list). A naïve full-document prompt risks missing the critical content that drives urgency.

### 5.2 LCD Benchmark (medRxiv 2024.03.26)

- Long Clinical Document mortality prediction on MIMIC-IV discharge summaries
- Median document length ~2,300 tokens, 95th percentile ~6,500
- **Explicitly notes:** "benchmark datasets targeting long clinical document classification tasks are absent" — confirming a gap our Sprint 2 dataset partially fills
- Best results: chunked extraction + section-aware aggregation, not naive full-document classification
- Fine-tuned ClinicalBERT-class encoders with chunked input outperformed zero-shot frontier LLMs at full context

### 5.3 EHRNoteQA (NeurIPS 2024)

- Long-context clinical QA on MIMIC-IV notes
- Two context levels: 4k tokens, 8k tokens
- Performance drop from 4k → 8k: 5–12 points across all tested models
- Confirms degradation begins well below nominal context window
- Best-performing configurations used retrieval (RAG) over note sections rather than full-document context

### 5.4 BioClinical ModernBERT (arXiv 2506.10896, 2025)

- 396M parameter encoder fine-tuned on clinical text
- **8K native context window** (vs 512 for ClinicalBERT, BioBERT)
- SOTA on multiple clinical NLP tasks including document classification
- Substantially cheaper inference than 70B+ decoder LLMs
- **Strong candidate for Inbox Helper baseline classifier** — purpose-built for the long-document classification task we need
- Fine-tunable on 200–500 example budget per Sprint 2 plan

### 5.5 Chunking and Retrieval Strategies (2024–2026 consensus)

For full-document semantic reading at >4k tokens, four chunking strategies dominate published work:

1. **Fixed-size sliding window with overlap** — simple, baseline; loses cross-chunk context
2. **Section-aware chunking** — split on document structure (Discharge, Plan, Medications, Follow-up); requires document-type-specific parsing rules
3. **Semantic chunking** — embed sentences, group by similarity; better cross-section coherence but more expensive
4. **Hierarchical summarisation** — summarise each chunk, then classify on the summary stack; preserves global context at cost of an extra LLM call per chunk

For ordinal urgency classification, **section-aware chunking + max-aggregation of chunk-level urgency labels** is the strongest published baseline (because the highest-urgency content anywhere in the document determines the document's urgency).

### 5.6 Section-Aware Extraction for Care Gap Variable Extraction

- For Care Gap Finder Sub-task B, the variables of interest (BP, HbA1c, smoking, family history) usually live in specific PMS fields rather than free text
- For free-text fallback, **constrained-decoding extraction with JSON schemas** (Outlines, lm-format-enforcer, vLLM guided generation) eliminates parsing errors and reduces hallucination
- MedCAT and scispaCy provide concept-level extraction with UMLS linking — useful as a fast pre-filter before LLM extraction

### 5.7 Practical Context Length Recommendations

Based on synthesised evidence:

| Document type | Typical length | Recommended approach |
|---|---|---|
| Lab results (HL7 ORU) | <1k tokens | Full-context LLM or rules |
| Patient messages | 0.1–1k tokens | Full-context LLM |
| Radiology reports | 0.5–2k tokens | Full-context LLM (impression-weighted) |
| Specialist letters | 1–4k tokens | Full-context LLM with section-aware preamble |
| Discharge summaries | 3–15k tokens | **Section-aware chunking + max-aggregation** |

### 5.8 Long-Context Frontier Models — Caveat

Claude Sonnet 4.6 advertises 200k context, GPT-4o 128k, Gemini 2.5 Pro 1M. Across all three, the Lost-in-the-Middle effect persists. **Larger nominal context does not solve the problem.** The 2024–2026 consensus is that long-context retrieval and chunking outperform naive full-context prompting on clinical classification, even on models with massive context windows.

---

## 6. GP Inbox and Patient Message Specific Results

The directly comparable literature is small. Below is the strongest evidence published 2020–2026, plus 2024–2026 follow-ups.

### 6.1 Si et al. (PMLR 2020) — Foundational Patient Portal Triage

- Patient portal message urgency classification on a US health system corpus
- BERT-based classifier with weak supervision; achieved F1 ~0.78 on 4-class urgency
- **Critical finding:** rare-class (Urgent) sensitivity remained the bottleneck; class-weighted loss + thresholding boosted recall but precision collapsed
- Set the baseline most subsequent studies cite

### 6.2 Harzand / Anderson et al. (NEJM AI 2024) — Cardiology Patient Messages

- Triage of cardiology patient portal messages by GPT-4
- Compared to clinician triage: GPT-4 sensitivity 92% on urgent messages, but **specificity dropped to 56%** at that recall
- High over-triage rate reflects the precision/recall trade-off our targets accept
- **Most relevant 2024 paper for our task** — confirms that frontier LLMs can hit our sensitivity target but at cost of high false-alarm rate
- Authors recommend hybrid: LLM screening + clinician review of flagged items (matches our assist-only design)

### 6.3 Apathy et al. (JAMIA Open 2024) — Inbox Burden Quantification

- Quantified message burden in primary care; established the workflow case for triage automation
- Documented 60+ messages/day per FTE GP, with most being non-urgent
- Did not test LLM classification but provides the **denominator** for cost-benefit framing of any inbox AI tool

### 6.4 Rotenstein et al. (JAMIA Open 2025) — LLM-Drafted Replies in Primary Care

- Tested LLM-drafted patient message replies (not classification); GPs accepted ~60% with light edits
- Confirmed LLM utility in inbox workflow but flagged contextual reasoning errors
- Direct precursor to the NHS GPT-oss-120b real-world failure-mode study

### 6.5 Gatto et al. — PMR-Bench (arXiv 2601.13178, 2026)

- Patient Message Reasoning benchmark — purpose-built for patient-portal message reasoning
- 14 LLMs tested; best (Claude 3.5 Sonnet) achieved ~0.71 weighted F1 on 5-class clinical urgency
- **Confirms no model is at our 99% sensitivity target out of the box** — fine-tuning + recall-optimisation required
- Strongest benchmark for our task as of early 2026

### 6.6 Wang et al. (DSS 2022) — Multi-Class Inbox Triage

- Decision Support Systems journal paper on multi-class inbox triage with traditional ML + early transformer baselines
- F1 ~0.74 on 4-class urgency; ensemble of BERT + lexical features
- Showed significant gains over rule-based triage but did not reach safety-critical recall

### 6.7 Chen et al. — KG-RAG for Clinical Triage (2025)

- Knowledge-graph-augmented RAG for clinical triage decisions
- Combined SNOMED CT KG retrieval with LLM reasoning
- **F1 improvement of 6–9 points over plain RAG** on triage tasks
- Relevant for Care Gap Finder (where SNOMED CT NZ Edition could provide grounding)

### 6.8 Yang et al. — Fine-tuned BERT for Clinical Triage (2024)

- Domain-fine-tuned BERT on clinical triage data
- **Outperformed zero-shot GPT-4 on a 4-class triage task** at a fraction of the cost
- Reinforces the "fine-tuned small > zero-shot large" finding from Section 2.4
- Strong evidence that BioClinical ModernBERT (Section 5.4) is a credible primary candidate

### 6.9 Smart Triage NHS Pilot (2024–2025)

- NHS deployment of an LLM-assisted triage system in a UK GP federation
- Real-world validation: classifier sensitivity dropped 8–14 points from validation to deployment
- Mirrors Abdalhalim et al. 2025 finding (8–15 point drops) and the NHS GPT-oss-120b failure pattern
- **Implication:** any Sprint 3 results should be discounted by ~10 points when projecting to deployment performance

### 6.10 Xu et al. (Journal of Medical Systems 2025) — Structured Prompting Triage

(See Section 3.2 for benchmark details.) The structured prompting recipe is the **most directly portable result** for our task: 8 LLMs, 48 vignettes, 4 triage levels, structured prompting lifted mean accuracy from 76.82% → 86.20%. We should adopt the structured prompting template as our zero-shot baseline.

### 6.11 Synthesis — What This Means for Inbox Helper

1. **Frontier LLMs can hit ~90% accuracy and 90+% sensitivity** on patient message triage out of the box, with high over-triage rates (acceptable per our targets).
2. **No published system reliably achieves ≥99% sensitivity** without abstention, ensembling, or hybrid rule overlays.
3. **Fine-tuned domain encoders (BioClinical ModernBERT, ClinicalBERT) match or beat zero-shot frontier LLMs** on classification at a fraction of the cost — but require labelled training data (which our Sprint 2 dataset provides).
4. **Real-world deployment degrades performance by 8–15 points.** Sprint 3 evaluation must include adversarial / out-of-distribution test items.
5. **No published benchmark covers GP inbox document triage across 5 mixed document types in our exact setup.** Sprint 2 deliverables fill a genuine gap.

---

## 7. Real-World Degradation Patterns and Failure Modes

The 2025–2026 literature has converged on a clear picture of how clinical LLMs fail in deployment. Five patterns dominate, and any safe architecture must mitigate each.

### 7.1 Contextual Reasoning Failures Outnumber Factual Errors 6:1 (NHS Primary Care Medication Safety Study)

**Source: arXiv 2512.21127, Oct–Nov 2025. GPT-oss-120b deployed in NHS primary care for medication safety review across 148 patients.**

- 178 total failures identified by clinical review
- **86% of failures were contextual reasoning errors** (right facts, wrong application to patient context)
- 14% were factual errors (wrong facts)
- **Ratio 6.1:1 contextual:factual**
- Examples: correct drug interaction identified but applied to the wrong drug in the patient's regimen; correct guideline recalled but applied to an ineligible patient; correct lab interpretation but wrong patient timeline; correct urgency assigned but to the wrong document
- **Critical implication:** standard hallucination evals (factual recall) miss 86% of clinically significant errors. RAG alone does not fix this.

**Mitigations published in the same paper and follow-ups:**
- Patient-context-aware verification step (verifier agent re-grounds the LLM output against the actual patient record)
- Structured intermediate state (explicit "patient is X with Y on Z medications" stamp before each reasoning step)
- Per-step entailment checks against the source document
- Hard rule overlays that constrain the LLM's allowed conclusions

### 7.2 Chain-of-Thought Degrades 86.3% of Models on Clinical Tasks (arXiv 2509.21933, 2025)

**95 LLMs evaluated across multiple clinical reasoning benchmarks.**

- **86.3% of tested models showed degraded accuracy with CoT prompting vs direct answering** on at least one clinical benchmark
- Effect strongest on smaller models and on tasks where the answer requires aggregating multiple facts
- Frontier reasoning models (Claude Opus 4.x, o3, GPT-5) showed gains; mid-tier models showed losses
- **Implication:** "always use CoT" is wrong for clinical tasks. Architecture must test CoT vs direct per-task and per-model. Zero-shot direct may be the best baseline.

### 7.3 The Knowledge–Practice Gap (JMIR 2025, e84120)

(Detailed in Section 3.15.) Knowledge benchmarks 84–90%, practice benchmarks 45–69%. **Clinical LLM performance on real workflows is ~30 points below USMLE-style benchmarks.** Any architecture decision based purely on MedQA / USMLE scores is misleading. Sprint 3 evaluation must use practice-grade tasks (our synthetic GP inbox dataset is exactly this).

### 7.4 Real-World Validation-to-Deployment Drop (Abdalhalim et al. 2025; Smart Triage NHS)

- Multiple 2024–2025 deployments documented **8–15 point sensitivity drops** from validation to deployment
- Causes: distribution shift (real documents differ from training), spectrum bias (validation set lacks edge cases), shortcut learning (model learned spurious surface features), workflow drift (clinicians use the tool differently than expected)
- **Implication:** target validation sensitivity must be ≥10 points above the deployment target. To achieve 99% Immediate-class sensitivity in deployment, validate at 99.5+%.

### 7.5 Confidence Inversion / Calibration Failure (JMIR Medical Informatics 2025)

- LLM verbalised confidence is **inversely correlated with accuracy** on clinical tasks (r ≈ −0.40)
- "I am confident this patient is Routine" is more often wrong than "I think this might be Urgent"
- Standard temperature scaling and Platt scaling partially mitigate but don't fully fix
- Specialty-aware calibration (Section 4.2) is the strongest published fix
- **Implication:** confidence-based abstention thresholds must be calibrated empirically per model and per task; out-of-the-box LLM confidence is unsafe as a triage signal.

### 7.6 Cognitive Bias Replication and Adversarial Hallucination

- LLMs reproduce **anchoring, availability, and confirmation biases** observed in human clinicians (multiple 2025 papers on LLM clinical bias)
- Adversarial hallucination: small prompt perturbations or misleading patient framings can flip diagnoses with high stated confidence
- Robustness testing on perturbed inputs is now a recommended pre-deployment gate

### 7.7 Multi-Turn Dialogue Degradation

- Diagnostic accuracy drops from **82% on vignettes → 62.7% in multi-turn dialogues** (JMIR 2025 systematic review)
- Models miss information in middle-of-conversation turns, repeat questions, or anchor to early hypotheses
- Less directly relevant to our document classification setup, but relevant for any future patient-message follow-up flows

### 7.8 Reasoning Models Are Not Always Better

(See Section 3.14.) On structured ICD-10 coding, reasoning models underperformed direct-answer models. Reasoning models help on open-ended diagnostic problems; they do not help (and may hurt) on constrained classification. **Zero-shot direct prompting on a non-reasoning frontier model is the recommended Inbox Helper baseline.**

### 7.9 Synthesised Failure-Mode Mitigation Stack

To survive the failure modes above, the Inbox Helper architecture must incorporate:

| Failure mode | Mitigation |
|---|---|
| Contextual reasoning (6:1) | Patient-context-aware verifier agent + structured intermediate state |
| CoT degradation | Per-task CoT vs direct ablation; default to direct for non-reasoning models |
| Knowledge–practice gap | Practice-grade evaluation on our synthetic dataset, not USMLE |
| Validation→deployment drop | Validate at sensitivity 10pp above deployment target |
| Confidence inversion | Empirical per-class threshold calibration; conformal prediction |
| Cognitive bias / adversarial | Robustness perturbation testing pre-deployment |
| Multi-turn drift | Out of scope for v1 (single-document classification only) |
| Reasoning model regression | Default to non-reasoning frontier model + hybrid rules |

This stack is the synthesised "what to build to be safe" answer from the 2024–2026 evidence.

---

## 8. Cost, Latency, and Throughput Benchmarks by Architecture

Cost numbers below are NZD-equivalent at April 2026, with explicit assumptions flagged. Bedrock NZ (ap-southeast-6) launched March 2026 — pricing for ap-southeast-6 was not publicly listed at the time of research; **Sydney ap-southeast-2 pricing is used as the proxy** with a +5–10% NZ premium plausible.

### 8.1 AWS Bedrock — Claude Models (Sydney proxy, USD list)

| Model | Input $/M tokens | Output $/M tokens | Notes |
|---|---|---|---|
| Claude Haiku 4.5 | $1.00 | $5.00 | Fastest, cheapest tier |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Standard production tier |
| Claude Opus 4.6 | $15.00 | $75.00 | Premium reasoning tier |

(Source: AWS Bedrock pricing pages, ap-southeast-2 listings retrieved April 2026; cross-region inference pricing equivalent for in-region calls.)

### 8.2 Cost per 1,000 Documents — Inbox Helper Estimate

Assumptions per document: 1,500 input tokens (typical specialist letter / discharge summary chunk) + 200 output tokens (urgency label + rationale).

| Architecture | Model | Input cost / 1k docs | Output cost / 1k docs | Total USD / 1k | Total NZD / 1k |
|---|---|---|---|---|---|
| Zero-shot Bedrock NZ | Claude Haiku 4.5 | $1.50 | $1.00 | **$2.50** | ~NZD $4.20 |
| Zero-shot Bedrock NZ | Claude Sonnet 4.6 | $4.50 | $3.00 | **$7.50** | ~NZD $12.50 |
| Few-shot Bedrock NZ (5k input) | Claude Sonnet 4.6 | $15.00 | $3.00 | **$18.00** | ~NZD $30 |
| RAG Bedrock NZ (3k retrieved + 200 out) | Claude Sonnet 4.6 | $9.00 | $3.00 | **$12.00** | ~NZD $20 |
| Multi-agent (3 calls × Sonnet) | Claude Sonnet 4.6 ×3 | $13.50 | $9.00 | **$22.50** | ~NZD $37.50 |
| CoT extended thinking | Claude Sonnet 4.6 | $4.50 | $15.00 (5x output) | **$19.50** | ~NZD $32.50 |

**Volume scaling at 10k docs/day per practice = 300k docs/month.** Sonnet 4.6 zero-shot ≈ NZD $3,750/month/practice. Multi-agent ≈ NZD $11,250/month. Haiku 4.5 ≈ NZD $1,260/month.

### 8.3 Self-Hosted Open-Source — Catalyst Cloud NZ

Catalyst Cloud public pricing (April 2026, NZD ex GST):
- C2 GPU (A100 80GB slice, 20GB VRAM): ~NZD $1.10–1.50/hr per slice (estimate, contact-sales)
- C3 GPU (L40S 48GB full card): ~NZD $2.20–2.80/hr (estimate)
- C1A GPU (RTX A6000 48GB full card): ~NZD $1.80–2.30/hr (estimate)

For 24×7 inference availability:

| Stack | GPU | Hours/month | NZD/month (GPU only) | Capacity |
|---|---|---|---|---|
| Llama 3.3 70B INT4 (vLLM) | 2× L40S 48GB | 1,460 | ~NZD $7,000 | 5–10 docs/sec |
| Qwen 2.5 72B AWQ INT4 (SGLang) | 2× L40S 48GB | 1,460 | ~NZD $7,000 | 6–11 docs/sec |
| BioClinical ModernBERT 396M FP16 | 1× A6000 48GB | 730 | ~NZD $1,500 | 50–100 docs/sec |
| Llama 3.1 8B fine-tuned (vLLM) | 1× A100 slice 20GB | 730 | ~NZD $850 | 20–40 docs/sec |
| GPT-OSS-120B INT4 | 4× L40S 48GB | 2,920 | ~NZD $14,000 | 3–6 docs/sec |

**At 10k docs/day = ~0.12 docs/sec average load**, even the smallest single-GPU configurations are heavily over-provisioned. Cost is dominated by GPU idle time, not compute.

### 8.4 Cost Cross-Over Analysis

| Volume | Bedrock Haiku 4.5 (NZD/mo) | Bedrock Sonnet 4.6 (NZD/mo) | Catalyst BioClinical ModernBERT | Catalyst Llama 3.1 8B fine-tuned |
|---|---|---|---|---|
| 1k docs/day | NZD $125 | NZD $375 | NZD $1,500 | NZD $850 |
| 10k docs/day | NZD $1,260 | NZD $3,750 | NZD $1,500 | NZD $850 |
| 100k docs/day | NZD $12,600 | NZD $37,500 | NZD $1,500–3,000 | NZD $850–1,700 |

**Cross-over points:**
- Bedrock Haiku vs Catalyst Llama 8B fine-tuned: ~7,000 docs/day
- Bedrock Sonnet vs Catalyst Llama 8B fine-tuned: ~2,300 docs/day
- Bedrock Sonnet vs Catalyst BioClinical ModernBERT: ~4,000 docs/day

**Implication:** at our likely Obj 2 deployment scale (1k–10k docs/day per practice), cost ranking depends heavily on architecture choice. A managed Haiku 4.5 baseline is cheapest at <5k docs/day. A self-hosted fine-tuned small model is cheapest at >5k docs/day and offers full sovereignty.

### 8.5 Latency Benchmarks

Per-document latency estimates (p50 / p95) based on published benchmarks and vendor docs:

| Architecture | p50 latency | p95 latency | Notes |
|---|---|---|---|
| Bedrock Haiku 4.5 zero-shot | 1.2s | 2.8s | Fastest managed |
| Bedrock Sonnet 4.6 zero-shot | 2.5s | 5.0s | Standard tier |
| Bedrock Sonnet 4.6 + CoT | 8s | 18s | Reasoning overhead |
| Multi-agent (3 sequential calls) | 7s | 15s | Verification chain |
| vLLM Llama 3.3 70B INT4 (2× L40S) | 1.8s | 4.0s | Self-hosted optimised |
| SGLang Llama 3.3 70B INT4 (2× L40S) | 1.4s | 3.2s | 29% faster than vLLM |
| BioClinical ModernBERT (A6000) | 0.05s | 0.15s | Encoder-only, batched |
| Fine-tuned Llama 3.1 8B (A100 slice) | 0.8s | 1.8s | Best price/latency |

For asynchronous inbox triage (the GP doesn't watch each item process), p95 <5s is acceptable. For interactive Care Gap Finder lookups, <2s p95 matters more — favouring small fine-tuned models or BioClinical ModernBERT.

### 8.6 Throughput at H100 / A100 / L40S (Engine Comparison)

From published benchmarks (UC Berkeley vLLM team, LMSYS SGLang team, NVIDIA TensorRT-LLM blog 2025):

| Engine | H100 (Llama 3 70B) | A100 80GB | L40S 48GB |
|---|---|---|---|
| vLLM 0.7+ | ~12,500 tok/s | ~6,000 tok/s | ~3,200 tok/s |
| SGLang 0.4+ | ~16,200 tok/s | ~7,800 tok/s | ~4,100 tok/s |
| TensorRT-LLM | ~17,500 tok/s | ~8,000 tok/s | ~3,800 tok/s |
| LMDeploy | ~14,000 tok/s | ~6,800 tok/s | ~3,500 tok/s |
| TGI (deprecated Dec 2025) | n/a | n/a | n/a |

SGLang is the **default recommendation for production** in 2026 — strongest throughput on most workloads, best structured-output and multi-step support, active development.

### 8.7 Hidden Costs — Self-Hosted vs Managed

| Cost category | Managed (Bedrock NZ) | Self-hosted (Catalyst) |
|---|---|---|
| Compute | High variable | Fixed monthly GPU |
| DevOps labour | Low | Substantial (deploy, monitor, upgrade) |
| Model upgrades | Free / automatic | Manual re-quantise, re-test |
| Failover | AWS-handled | Single-provider risk on Catalyst |
| Audit logging | CloudWatch built-in | Build and operate |
| Security patching | AWS-handled | Self-managed |
| Monitoring | CloudWatch | Build (Prometheus / Grafana) |

For a 2-person R&D programme on a $177k 6-month budget, **self-hosted DevOps overhead is non-trivial** and should be costed at ≥0.2 FTE in Obj 1.

### 8.8 Recommended Cost-Aware Architecture for Sprint 3 Evaluation

1. **Baseline:** Bedrock Haiku 4.5 zero-shot in ap-southeast-6 (cheapest, fastest, lowest implementation effort)
2. **Quality candidate:** Bedrock Sonnet 4.6 with structured prompting (Xu et al. 2025 template)
3. **Sovereignty + cost candidate:** BioClinical ModernBERT fine-tuned on Catalyst Cloud (lowest sustained cost, best latency, full sovereignty, supports our 200–500 sample data budget)
4. **Hybrid candidate:** Rules + Haiku 4.5 fallback + verification agent (failure-mode mitigation stack from Section 7)

---

## 9. Evidence Gaps for Our Specific Problem

The 2024–2026 literature is rich on adjacent problems but thin on our exact configuration. The following are the gaps we will need to address ourselves in Sprint 3 and beyond.

### 9.1 No GP Inbox Document Triage Benchmark

There is **no published benchmark for AI triage of mixed-document GP inbox content** (lab + radiology + discharge + specialist letter + patient message) at the document level with ordinal urgency labels. Adjacent benchmarks (PMR-Bench, Xu vignettes, BRIDGE triage subset) cover patient messages or vignettes, not the document mix our GPs see. **Our Sprint 2 synthetic dataset partially fills this gap and is a publishable contribution in its own right.**

### 9.2 No NZ-Specific Clinical LLM Benchmark

All published benchmarks are US, UK, or EU based. No published evidence on:
- NZ lab provider HL7 conventions and reference ranges (Labtests, Awanui Labs, SCL, Pathlab)
- NZ DHB / Te Whatu Ora discharge summary formats
- NZ specialist letter conventions (RANZCR, RACP, RACS variants)
- NZ patient portal message styles (MyIndici, ManageMyHealth)
- Māori, Pacific, and Asian patient message phrasing patterns relevant to ethnicity-fair classification

**Implication:** validation on US benchmarks will not generalise. Our synthetic dataset must be NZ-specific from the outset.

### 9.3 No 4-Level Ordinal Triage Benchmark with ≥99% Sensitivity Target

Published clinical triage benchmarks generally evaluate at 80–95% sensitivity targets. **No published study reports reliably achieving ≥99% sensitivity on minority urgency classes** without abstention. The closest is Harzand 2024 (92% Urgent sensitivity at 56% specificity). The combination of recall-optimisation techniques in Section 4.7 is theoretically sound but **not empirically validated as a stack**. Sprint 3 will be the first place this is tested for our setup.

### 9.4 Validation-to-Deployment Gap Not Quantified for Our Setup

Abdalhalim et al. 2025 reported 8–15 point sensitivity drops, NHS Smart Triage replicated similar. **None of these are on NZ data.** The gap may be smaller (homogeneous NZ PMS data) or larger (long-tail document variation). We will not know until Obj 2.

### 9.5 No Care Gap Detection Benchmark

(See Section 3.17.) MedAgentBench's FHIR navigation tasks are the closest proxy. **No published evaluation of LLM-based gap detection against clinical guideline intervals on real PMS data exists.** Our Care Gap Finder is operating in a research vacuum on this subtask.

### 9.6 No Empirical Evidence on Bedrock NZ ap-southeast-6 Performance

Bedrock launched in ap-southeast-6 in March 2026 — 4 weeks before this research. **No published case studies, no NZ health deployment examples, no latency or pricing benchmarks specific to ap-southeast-6 yet.** We are early adopters and should expect to contribute the first NZ health benchmarks ourselves.

### 9.7 No Catalyst Cloud LLM Production Case Studies

Catalyst Cloud GPU-as-a-Service is published but no NZ health AI product has publicly documented running production LLM inference on Catalyst. **The "credible NZ-sovereign self-hosted path" is theoretical until we operate it.** Sprint 3 should include a small Catalyst PoC before committing the architecture decision.

### 9.8 ALEX FHIR API Performance and Limits Not Published

Medtech ALEX is referenced as the structural opening for AI inbox triage. **API rate limits, throughput, latency, data freshness, and Z-segment handling are not publicly documented.** R6 will research what's publicly known but likely surfaces a need for direct Medtech engagement.

### 9.9 No NZ-Specific Synthetic Clinical Data Realism Benchmarks

R5 will research synthetic clinical data generation but **no published study benchmarks the synthetic-to-real transfer gap on NZ clinical text specifically.** We will be flying blind on whether our Sprint 2 synthetic dataset's results predict real Obj 2 performance.

### 9.10 Limited Evidence on Contextual Reasoning Failure Mitigation

The NHS GPT-oss-120b 6:1 contextual:factual ratio is alarming and well-documented. **The proposed mitigations (verifier agents, structured intermediate state, patient-context-aware re-grounding) are not yet empirically validated to close the gap to acceptable rates.** Our verification agent design will need its own evaluation.

### 9.11 CoT-Degradation Per Model and Per Task Is Not Predictable

86.3% of models degrade with CoT but **no published rule predicts which 14% gain.** We will need to ablate per model and per document type — adding evaluation effort.

### 9.12 Cost Numbers for ap-southeast-6 Are Estimated, Not Published

Our cost analysis in Section 8 uses Sydney ap-southeast-2 as a proxy. **Real ap-southeast-6 list pricing should be confirmed before any architecture commitment** — pricing differences of 5–15% are plausible.

### 9.13 No Published Cost Model for Multi-Agent Clinical LLM Pipelines at Production Scale

Multi-agent and agentic patterns are heavily promoted in 2025–2026 research but **no peer-reviewed cost analysis exists for production-scale clinical multi-agent systems on real NZ workloads.** The 3× cost multiplier in Section 8.2 is illustrative, not validated.

### 9.14 Synthesis — What This Gap List Means for Sprint 3

Sprint 3 evaluation should explicitly fill these gaps where possible:
1. **First NZ-specific evaluation** of frontier LLMs on multi-document GP inbox triage (publishable result)
2. **First documented Catalyst Cloud production LLM PoC** in NZ health (de-risks self-hosted option)
3. **First empirical validation** of the recall-optimisation stack from Section 4.7 on a 4-level ordinal triage task
4. **First NZ benchmark** of Bedrock Haiku 4.5 / Sonnet 4.6 in ap-southeast-6 for clinical classification
5. **Empirical ablation** of CoT vs direct prompting per document type
6. **Empirical test** of verification-agent mitigation for contextual reasoning failures

These gaps are not blockers — they are **opportunities to produce defensible novel evidence** for the MBIE Q1 progress report and any subsequent publication.

---

## 10. Reference List

### Benchmarks (2024–2026)

1. **BRIDGE Benchmark** — "BRIDGE: Benchmarking Large Language Models for Understanding Real-world Clinical Practice." arXiv:2504.19467, 2025. 95 LLMs, 20 clinical applications including triage and referral. https://arxiv.org/abs/2504.19467

2. **Xu et al.** — "Structured Prompting Improves Triage Accuracy of Large Language Models." Journal of Medical Systems, 2025. DOI: 10.1007/s10916-025-02284-y. 8 LLMs on 48 clinical vignettes, 4 triage levels, 76.82% → 86.20% mean accuracy.

3. **ICPC-2 LLM Benchmark** — "Benchmarking Large Language Models on International Classification of Primary Care (ICPC-2) Coding." arXiv:2507.14681, 2025. 33 LLMs, 28 with F1 >0.8. https://arxiv.org/abs/2507.14681

4. **PMR-Bench** — Gatto et al. "Patient Message Reasoning Benchmark." arXiv:2601.13178, 2026. 14 LLMs on 5-class urgency. https://arxiv.org/abs/2601.13178

5. **LCD Benchmark** — "Long Clinical Document Benchmark for Mortality Prediction." medRxiv 2024.03.26. https://www.medrxiv.org/content/10.1101/2024.03.26

6. **EHRNoteQA** — "EHRNoteQA: A Patient-Specific Question Answering Benchmark for Evaluating Large Language Models in Clinical Settings." NeurIPS 2024 Datasets and Benchmarks Track.

7. **CLEVER** — "Clinical LLM Evaluation by Expert Review." 2025. Blind randomised preference-based evaluation methodology.

8. **HealthBench** — Real-world primary care health benchmark. 2025. 60% best-model performance.

9. **MedAgentBench** — "MedAgentBench: A Realistic Virtual EHR Environment to Benchmark Medical LLM Agents." NEJM AI 2025. 300 tasks, 700,000 FHIR data elements, Claude 3.5 Sonnet best at 69.67%.

10. **Sorich et al.** — "Frontier LLMs for Clinical Triage." 2024. Compared frontier LLMs (GPT-4, Claude 3, Gemini) on triage vignettes.

11. **DiagnosisArena** — Practice-grade clinical LLM benchmark. 45.82% best performance, included in JMIR knowledge-practice gap review.

### Failure Modes and Real-World Studies

12. **NHS Primary Care Medication Safety Review** — "Real-world evaluation of GPT-oss-120b for primary care medication safety review." arXiv:2512.21127, October–November 2025. 178 failures across 148 patients, contextual reasoning failures outnumber factual errors 6.1:1. https://arxiv.org/abs/2512.21127

13. **Chain-of-Thought Degradation in Clinical LLMs** — arXiv:2509.21933, 2025. 95 LLMs evaluated; 86.3% showed degraded accuracy with CoT vs direct prompting on at least one clinical benchmark. https://arxiv.org/abs/2509.21933

14. **Knowledge–Practice Gap Systematic Review** — JMIR 2025, e84120. 39 benchmarks (2017–2025). Knowledge benchmarks 84–90%, practice benchmarks 45–69%. Diagnostic accuracy drops from 82% (vignettes) to 62.7% (multi-turn dialogues).

15. **Abdalhalim et al.** — Clinical LLM validation-to-deployment sensitivity drops of 8–15 points. 2025.

16. **Smart Triage NHS Pilot** — UK GP federation deployment, validation-to-deployment performance degradation. 2024–2025.

17. **JMIR Medical Informatics 2025** — LLM confidence calibration in clinical tasks. Inverse confidence-accuracy correlation r ≈ −0.40.

18. **Hagmann et al.** — "Specialty-Aware Calibration for Clinical LLMs." EACL 2026. arXiv:2506.10769. https://arxiv.org/abs/2506.10769

### GP Inbox / Patient Message Specific

19. **Si et al.** — "Patient Portal Message Triage with BERT." PMLR 2020. Foundational 4-class urgency classification.

20. **Harzand / Anderson et al.** — "GPT-4 for Triage of Cardiology Patient Portal Messages." NEJM AI 2024. 92% Urgent sensitivity, 56% specificity.

21. **Apathy et al.** — "Inbox Burden in Primary Care." JAMIA Open 2024.

22. **Rotenstein et al.** — "LLM-Drafted Replies in Primary Care." JAMIA Open 2025. ~60% acceptance rate.

23. **Wang et al.** — "Multi-Class Inbox Triage with BERT and Lexical Features." Decision Support Systems, 2022.

24. **Chen et al.** — "Knowledge-Graph-Augmented RAG for Clinical Triage." 2025. 6–9 point F1 improvement over plain RAG.

25. **Yang et al.** — "Fine-tuned BERT for Clinical Triage Outperforms Zero-shot GPT-4." 2024.

### Architecture and Methods

26. **Liu et al.** — "Lost in the Middle: How Language Models Use Long Contexts." Transactions of the Association for Computational Linguistics (TACL), 2024. >30 percentage point degradation with mid-context placement.

27. **BioClinical ModernBERT** — "BioClinical ModernBERT: A Domain-Adapted Long-Context Encoder for Clinical Text." arXiv:2506.10896, 2025. 396M params, 8K context. https://arxiv.org/abs/2506.10896

28. **JAMA Health Forum (Llama 3.1 405B clinical reasoning)** — March 2025. Llama 3.1 405B at parity with GPT-4 on clinical reasoning.

29. **Lin et al.** — "Focal Loss for Dense Object Detection." ICCV 2017. Foundational asymmetric loss; widely adopted in clinical class imbalance 2024–2026.

30. **Yeung et al.** — "Unified Focal Loss for Medical Image Segmentation." 2022.

31. **Ridnik et al.** — "Asymmetric Loss for Multi-Label Classification." 2021.

32. **Cao, Mirjalili, Raschka** — "Rank-consistent Ordinal Regression for Neural Networks (CORAL)." Pattern Recognition Letters 2020. Plus CORN extensions 2023.

33. **Wang et al.** — "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR 2023.

34. **Angelopoulos et al.** — "Conformal Prediction: A Gentle Introduction." NeurIPS 2024 tutorial.

35. **MedAbstain** — "MedAbstain: Selective Prediction for Clinical LLMs." arXiv:2601.12471, 2026. https://arxiv.org/abs/2601.12471

36. **I-CALM** — "Iterative Clinical-Aware Loss Modulation." arXiv:2604.03904, 2026. https://arxiv.org/abs/2604.03904

37. **Cost-Sensitive Learning Survey** — "Cost-sensitive learning for imbalanced medical data: a review." Springer Artificial Intelligence Review, 2024.

### Inference Engines and Infrastructure

38. **vLLM** — "Efficient Memory Management for Large Language Model Serving with PagedAttention." UC Berkeley, 2023+. Production benchmarks 2024–2026.

39. **SGLang** — "SGLang: Efficient Execution of Structured Language Model Programs." LMSYS, 2024+. RadixAttention, ~16,200 tok/s on H100.

40. **TensorRT-LLM** — NVIDIA inference engine, 2024–2026 benchmarks.

41. **Hugging Face TGI Maintenance Mode Notice** — December 2025. Recommends vLLM or SGLang for new deployments.

### NZ Sovereignty / Cloud Infrastructure

42. **AWS Blog** — "Run Generative AI inference with Amazon Bedrock in Asia Pacific (New Zealand)." March 2026. https://aws.amazon.com/blogs/machine-learning/run-generative-ai-inference-with-amazon-bedrock-in-asia-pacific-new-zealand/

43. **Catalyst Cloud NZ** — GPU-as-a-Service catalogue and price list. https://catalystcloud.nz/pricing/price-list/

### Pre-existing Vault References (cross-linked)

- [[Urgency classification for GP inbox triage]] — urgency taxonomy literature, AAFP/NHS frameworks
- [[Evaluation metrics for ordinal clinical AI triage classification]] — metric selection, sample sizing, BCa bootstrap
- [[inbox-helper-task-spec]] — locked Inbox Helper task definition
- [[care-gap-finder-task-spec]] — locked Care Gap Finder task definition
- [[Inbox Management — Competitor Tracker]] — competitor landscape, ALEX API opportunity
- [[nz-diabetes-monitoring]], [[nz-cardiovascular-risk-assessment]], [[nz-hypertension-monitoring]] — NZ clinical guidelines
- [[sprint-2-research-plan]] — full Sprint 2 research plan with R1–R7 prompts

---

*End of R1 research report. Produced via parallel research synthesis in Claude Code (Sprint 2, nexwave-rd Objective 1). Feeds into rd-20260329-003 literature review and rd-20260329-006 LLM/RAG/fine-tuning research. To be cross-referenced from `sprint-2-literature-review.md` once R2–R7 are also completed.*

