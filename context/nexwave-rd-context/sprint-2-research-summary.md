---
title: Sprint 2 — Research Summary
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-12
status: final
---

# Sprint 2 — Research Summary

**Sprint:** [[2026-04-rd-sprint-2]] (12–25 Apr 2026)
**Objective:** obj-1 — Literature review and architecture research
**Goal B deadline:** Architecture decision made and documented, end of April 2026

This document summarises the 7 research deliverables (R1–R7) produced during Sprint 2 for nexwave-rd Objective 1. Each report is filed in `context/nexwave-rd-context/` and linked below. Together they form the evidence base for the Goal B architecture decision and the MBIE Q1 progress report (due 31 May 2026).

**Total research output:** 6,077 lines across 7 reports, covering clinical LLM benchmarks, NZ sovereignty, architecture shortlisting, care gap finder design, synthetic data protocol, PMS integration, and open-source self-hosted options.

---

## R1 — Clinical LLM Architecture Benchmarks

**File:** [[research-r1-llm-architecture-benchmarks]] (911 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-003 (literature review), rd-20260329-006 (LLM/RAG/fine-tuning research)

Empirical literature review of LLM architecture approaches for clinical document classification (2024–2026), covering 280+ web sources across 7 architecture families (zero-shot, few-shot, RAG, fine-tuning, hybrid rules+LLM, extended thinking, agentic/multi-agent).

**Key findings:**
- **Fine-tuned small models (8B) dramatically outperform zero-shot large models (120B) on classification** with just 200–500 labelled examples (F1 0.95–0.97 vs 0.34–0.40). Our 300–500 synthetic items sit in the sweet spot.
- **Contextual reasoning failures outnumber factual errors 6:1** in deployed primary care LLMs (NHS GPT-oss-120b real-world study, arXiv 2512.21127). This is the dominant failure mode to design against.
- **Chain-of-thought prompting DEGRADES clinical text performance in 86% of models** (arXiv 2509.21933, 95 LLMs on 87 tasks). Do not use CoT for classification by default.
- **Knowledge-practice gap is massive** — LLMs score 84–90% on knowledge benchmarks but only 45–69% on practice benchmarks. Vignette-to-dialogue accuracy drops 19.3 percentage points.
- **No published benchmark exists for GP inbox document triage** (heterogeneous document types classified by urgency) — a genuine research gap we will partially fill.

---

## R2 — NZ Sovereign Hosting and Regulatory Posture

**File:** [[research-r2-nz-sovereign-hosting-regulatory]] (987 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-003 (literature review)

Deep-dive on the sovereignty trade-off between AWS Bedrock NZ (ap-southeast-6, Auckland, launched March 2026) and Catalyst Cloud NZ (100% NZ-owned, ISO 27001), plus the current NZ regulatory landscape (Privacy Act 2020, HIPC 2020, Medical Products Bill status, DPIA methodology).

**Key findings:**
- **AWS Bedrock in Auckland is real but models run via AU geographic cross-Region inference** (Auckland + Sydney + Melbourne). No documented "NZ-only pinning" option exists — data stays in ANZ geography but not guaranteed to stay in NZ on every call.
- **Catalyst Cloud NZ is the only 100% NZ-sovereign GPU option.** However, A100 slices retire 31 March 2026 and L40S is Beta-only. **RTX A6000 48GB is the only GA production GPU** — and it fits every model we care about.
- **Every other NZ provider (CCL/Spark, 2degrees, Datacom, Umbrellar, Kordia) is contact-sales or non-existent** for GPU workloads. Datacom Sovereign Cloud is worth a sales call as Plan B.
- **Medical Products Bill is irrelevant during our grant period** — not expected to commence until ~2030. Current binding layer is Privacy Act 2020 + HIPC 2020 + OPC 2023 AI guidance + Privacy Amendment Act 2025 (IPP 3A, in force May 2026).
- **Recommended DPIA structure:** OPC PIA Toolkit + ICO AI DPIA extensions + NIST AI RMF overlay + NEAC Maori data sovereignty layer + NHS DCB0129-style clinical safety case.

---

## R3 — Architecture Shortlist

**File:** [[research-r3-architecture-shortlist]] (640 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-006 (LLM/RAG research), rd-20260329-010 (architecture shortlist)

Synthesis of R1, R2, and R7 into 4 concrete architecture candidates scored against both Inbox Helper (5 doc types) and Care Gap Finder (3 sub-tasks).

**The 4 candidates:**

| # | Candidate | Core model | Hosting |
|---|---|---|---|
| **C1** | Bedrock NZ Claude (tiered Haiku 4.5 + Sonnet 4.6) | Claude Haiku 4.5 primary + Sonnet 4.6 arbiter | AWS Bedrock ap-southeast-6 |
| **C2** | Catalyst NZ Llama 3.3 70B + SGLang (three-tier cascade) | Llama 3.3 70B + BioClinical ModernBERT + MedGemma 27B-IT | Catalyst Cloud C1A A6000 |
| **C3** | Hybrid rules-first + small fine-tuned LLM | Python rules + BioClinical ModernBERT 396M + Llama 3.1 8B LoRA | Catalyst Cloud or Bedrock |
| **C4** | Agentic multi-step pipeline | Extraction → classifier → verification agents | Bedrock NZ or Catalyst |

**Headline recommendation: start evaluation with C3 (hybrid rules-first).** Fine-tuned 8B outperforms zero-shot 120B at our data scale, CoT degrades 86% of models, and rules-first provides the most auditable and regulatory-defensible posture. All four candidates preserve the AI reasoning + ALEX FHIR differentiator. Cost cross-over between Bedrock Haiku 4.5 and Catalyst self-hosted is ~20,000 documents/day.

---

## R4 — Care Gap Finder Sub-Task Architectures

**File:** [[research-r4-care-gap-finder-subtasks]] (738 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-010 (architecture shortlist), rd-20260329-011 (data requirements)

Design reference for the three Care Gap Finder sub-tasks: (A) deterministic rules engine, (B) variable extraction from NZ PMS records, (C) CVDRA calculation per HISO 10071:2025.

**Key findings:**
- **Sub-task A (rules engine): build a thin custom YAML-defined interpreter (~500–1000 LoC).** Every credible off-the-shelf Python option is dormant, GPL-encumbered, or lacks temporal-interval primitives. Adopt the CMS eCQM four-layer pattern (Initial Population → Denominator → Exclusions → Numerator) with tri-state outcomes (GAP / NO_GAP / INSUFFICIENT_DATA).
- **Sub-task B (variable extraction): this is a routing problem, not an LLM problem.** 12 of 15 PREDICT inputs are deterministic structured-field lookups. Only family history genuinely needs free-text NLP (~19% structural completeness in NZ). Recommended extractor: BioClinical ModernBERT 396M fine-tuned, with Llama 3.3 70B constrained-decoding verifier. Do not use CoT for extraction.
- **Sub-task C (CVDRA calculation): no published Python implementation exists.** Clean-room reimplementation from HISO 10071:2025 required (VIEW R package is GPL-3.0). Fail-closed architecture: hard-suppress on CVD equivalents, never impute age/sex/ethnicity (Berkelmans 2022), conservative over-estimation for binary modifiers in recall mode.

---

## R5 — Synthetic NZ GP Inbox Dataset Generation Protocol

**File:** [[research-r5-synthetic-data-protocol]] (1,107 lines)
**Status:** Provisional (pending Sprint 1 GP clinical review rd-20260405-001)
**Feeds tasks:** rd-20260329-022 (synthetic dataset schema), rd-20260329-023 (synthetic dataset generation)

Executable protocol for generating, labelling, and releasing 300–500 synthetic NZ GP inbox items in the 2-week Sprint 2 window, as the evaluation substrate for the Sprint 3 architecture bake-off.

**Key findings:**
- **Two-track design:** Sprint 2 produces a 400-item stratified enriched dev/eval split; natural-prevalence holdout is Sprint 4. 5×4 stratification grid across doc types and urgency levels.
- **Multi-model, label-decoupled generation** with 3 mandatory shortcut-prevention controls (label-decoupled prompting, style normalisation, TF-IDF back-classification probe scoring <70%).
- **15–20% contextual-reasoning stress items** (60–80 items) addressing the NHS 6:1 failure finding, using parameter layering and counterfactual contrast pairs.
- **Single-annotator calibration protocol:** 25-item calibration set re-labelled blind at Days 2/7/13; quadratic-weighted Cohen's kappa >= 0.75 floor. "When in doubt, label up."
- **NZ-sovereign generation pathway:** Catalyst Cloud Wellington primary (Llama 3.3 70B Instruct) / Bedrock ap-southeast-6 fallback (Claude Sonnet 4.6). Privacy-safe NHI placeholders using reserved `ZZI`/`ZIO` prefix (HISO-excluded letters).
- **14 programmatic QA release gates (G1–G14)** and 4 sprint gates (Day 2/7/11/14).
- **10-point synthetic-to-real discount rule** — architecture scores interpreted conservatively; dataset enables ranking, not absolute performance estimation.

---

## R6 — Data Standards and PMS Integration

**File:** [[research-r6-data-standards-pms-integration]] (886 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-011 (data requirements)

Comprehensive data requirements reference covering Medtech ALEX FHIR API, Indici, HL7 v2.4 in NZ primary care, NZ FHIR profiles, clinical code sets, document arrival patterns, and a variable-by-variable mapping for the 15 PREDICT inputs.

**Key findings:**
- **ALEX is FHIR-shaped, not FHIR-conformant.** ~261 endpoints, Azure AD OAuth + static IP allowlist, no `$export`, no Subscriptions — everything is pull-based via `_lastUpdated`. Partner NDA required for substantive documentation.
- **Indici is substantially more closed.** No public developer portal, no public OpenAPI. Sprint 4+ scope.
- **HL7 v2.4 is the substrate.** Labs are >95% structured ORU. Discharge summaries and specialist letters arrive as PDF blobs in MDM messages. Only 40–55% of discharge summaries are structured CDA nationally.
- **~110 inbox items/day per median 2,500-patient practice** (60% labs, 10% radiology, 7% discharge, 13% specialist, 5% portal, 5% other).
- **Combined Inbox Helper + Care Gap Finder on Claude Haiku 4.5 via Bedrock: NZD 6–10/month/practice.** Self-hosted Llama 3.3 70B is uneconomic single-tenant (~NZD 2,000/month); pooled break-even at ~200 practices.
- **The strategic ALEX opening holds** — no competitor is using ALEX FHIR API for AI-driven inbox triage.

---

## R7 — Open-Source LLM Self-Hosted Architecture Options

**File:** [[research-r7-open-source-llm-self-hosted]] (808 lines)
**Status:** Final
**Feeds tasks:** rd-20260329-006 (LLM/RAG research), rd-20260329-010 (architecture shortlist)

Evidence-based deep-dive on open-source LLM candidates, inference engines, GPU fit, cloud providers, fine-tuning approaches, and cost modelling for self-hosted deployment as a first-class alternative to Bedrock NZ.

**Key findings:**
- **Two recommended stacks:** (A) Llama 3.3 70B Instruct AWQ INT4 on SGLang (primary), (B) Qwen 3 32B Apache 2.0 (cleanest-licence backup). Both on Catalyst Cloud C1A RTX A6000 48GB.
- **SGLang over vLLM** — ~29% higher throughput, native deterministic mode that works on A6000 (SM 8.6), and native structured-output via XGrammar. vLLM's deterministic path requires SM >=9.0 (Hopper). TGI ruled out (maintenance mode since Dec 2025).
- **Open-source clinical parity established:** JAMA Health Forum March 2025 found Llama 3.1 405B scored ~70% vs GPT-4 ~64% on NEJM clinical cases.
- **Three-tier cascade** (BioClinical ModernBERT pre-classifier → Llama 3.3 70B classifier → MedGemma 27B-IT second opinion) directly targets the NHS 6:1 contextual-reasoning failure pattern.
- **Fully-loaded monthly cost:** ~NZD $3,200/month on Catalyst C1A 24x7; ~NZD $32k over 6-month Objective 1.
- **Head-to-head vs Bedrock:** at 1,000 docs/day, Bedrock Haiku is 3–5x cheaper (GPU idle dominates); at 10,000 docs/day, costs converge within noise. Decision should be on accuracy + operational fit, not cost.
- **Fine-tuning for 300–500 items:** LoRA/QLoRA (r=16–32) for extraction sub-tasks, DSPy MIPROv2 prompt optimisation for the main classifier. Weighted focal loss + temperature scaling + conformal prediction + abstention for recall-optimisation.

---

## Cross-cutting themes

### Sovereignty
Two credible NZ-hosted paths exist as of April 2026. Neither is perfect: Bedrock NZ cross-routes to ANZ geography (not NZ-only), Catalyst Cloud's only GA production GPU is RTX A6000 48GB. The architecture shortlist includes candidates on both paths.

### The ALEX opening
No competitor (Health Accelerator RPA, Medtech AI, Inbox Magic, BPAC CS, Heidi Health) is using the Medtech ALEX FHIR API for AI-driven inbox triage. This structural opening is validated as of April 2026 and all 4 architecture candidates preserve the AI reasoning + ALEX differentiator.

### Dominant failure mode
Contextual reasoning failures (not factual errors) are the 6:1 dominant failure mode in deployed primary care LLMs. Every architecture candidate and the synthetic dataset protocol are designed to mitigate this finding.

### Synthetic-to-real gap
Sprint 3 architecture evaluation on synthetic data enables ranking, not absolute performance estimation. A 10-point discount applies when extrapolating to real-data performance. The decision Sprint 3 makes is "which architecture wins", not "what will the accuracy be".

---

## Next steps

These 7 research reports feed the following Sprint 2 synthesised deliverables (to be produced in a fresh session):

| Deliverable | Source reports | Task |
|---|---|---|
| `sprint-2-literature-review.md` | R1 + R2 | rd-20260329-003 |
| `sprint-2-architecture-shortlist.md` | R3 + R4 + R7 | rd-20260329-010 |
| `sprint-2-data-requirements.md` | R6 + R4 | rd-20260329-011 |
| `sprint-2-synthetic-dataset-schema.md` | R5 | rd-20260329-022 |
