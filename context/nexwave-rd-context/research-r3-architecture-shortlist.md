---
title: Research R3 — Architecture Shortlist for Inbox Helper + Care Gap Finder
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-11
status: final
---

# Research R3 — Architecture Shortlist for Inbox Helper + Care Gap Finder

> **Scope.** Synthesises [[research-r1-llm-architecture-benchmarks]] (clinical LLM empirical results), [[research-r2-nz-sovereign-hosting-regulatory]] (NZ sovereign hosting + regulatory posture), and [[research-r7-open-source-llm-self-hosted]] (open-source self-hosted architecture options) into 4 concrete architecture candidates, each scored against Inbox Helper (5 doc types) and Care Gap Finder (3 sub-tasks) requirements. This is the **Sprint 2 deliverable for rd-20260329-010** and the evidence base for the Goal B architecture decision due end April.
>
> **Method.** R3 is a synthesis task, not a fresh research run. R1/R2/R7 already produced the empirical evidence, sovereignty analysis, and stack specification. This report applies them to the locked task specifications in [[inbox-helper-task-spec]] and [[care-gap-finder-task-spec]] and produces a ruling-criteria-ready candidate slate for Sprint 3 evaluation.

---

## 1. Executive summary

This report shortlists **four architecture candidates** for Sprint 3 evaluation, covering the full design space from closed-frontier managed API through open-source self-hosted to rules-first hybrid and agentic multi-step. Every candidate preserves the **AI reasoning + clinical accuracy + ALEX FHIR integration** differentiator called out in the NexWave competitor tracker, and every candidate can in principle meet the ≥99% Immediate/Urgent sensitivity and ≥90% weighted accuracy targets with appropriate recall-optimisation treatment.

| # | Candidate | Core model | Hosting | One-line rationale |
|---|---|---|---|---|
| **C1** | **Bedrock NZ Claude (tiered Haiku 4.5 + Sonnet 4.6)** | Claude Haiku 4.5 as primary classifier + Claude Sonnet 4.6 as arbiter | AWS Bedrock `ap-southeast-6` (Auckland, launched March 2026) | Managed, fastest iteration, highest closed-model clinical ceiling (Sonnet 4.6 on JMIR 2024 triage vignettes: 94%), cheapest at small volume. Sovereignty posture depends on R2 §2 confirmation of native-in-region model availability. |
| **C2** | **Catalyst NZ Llama 3.3 70B + SGLang (three-tier cascade)** | Llama 3.3 70B AWQ INT4 main + BioClinical ModernBERT pre-classifier + MedGemma 27B-IT arbiter | Catalyst Cloud C1A RTX A6000 48GB, NZ-sovereign | Strongest sovereignty posture (NZ-owned, ISO 27001/27017, three NZ data centres), deterministic inference, full control over upgrade path. R7 Stack A. JAMA Health Forum March 2025: Llama 3.1 405B ~70% vs GPT-4 ~64% on NEJM — open-model clinical parity is established. |
| **C3** | **Hybrid rules-first + small fine-tuned LLM** | Python rules engine for structured lab/radiology flags + **BioClinical ModernBERT 396M (fine-tuned)** pre-classifier + **UrgentSFT-style Llama 3.1 8B LoRA** for unstructured doc types | Catalyst Cloud C1A A6000 (can also run on Bedrock via Claude Haiku 4.5 for unstructured) | **Most defensible safety + explainability posture.** Rules route deterministic cases (lab critical flags → Urgent); small fine-tuned models handle the rest. R1 finding: fine-tuned 8B can outperform zero-shot 120B (arXiv 2504.21191; UrgentSFT-8B on PMR-Bench). UK NHS Smart Triage real-world precedent: 73% waiting time reduction. |
| **C4** | **Agentic multi-step pipeline** | Extraction agent (Meditron3-8B QLoRA) → classifier agent (Claude Haiku 4.5 or Llama 3.3 70B) → verification agent (MedGemma 27B-IT or Claude Sonnet 4.6) with tool calls and structured JSON | Bedrock NZ or Catalyst C1A depending on model mix | **Targets the NHS 6:1 contextual-reasoning failure pattern most directly** — explicit role separation, explicit tool calls, explicit verification pass. Higher latency and cost but highest defensibility against contextual errors. |

**Shortlist composition satisfies the R3 prompt constraints:**
- ✅ At least one **Bedrock-NZ-hosted Claude candidate** (C1 primary; C4 optional Claude path).
- ✅ At least one **Catalyst-Cloud-NZ-hosted open-model candidate** (C2 primary; C3 optional Catalyst path; C4 optional Catalyst path).
- ✅ At least one **hybrid rules + LLM candidate** (C3).
- ✅ At least one **agentic / multi-agent candidate** (C4).

**Headline recommendation — start evaluation with C3 (hybrid) first.** Three reasons:

1. **R1 finding #1 is decisive at our data scale.** Fine-tuned small models (200–500 labelled examples) outperform zero-shot large models on classification (arXiv 2504.21191: F1 0.95–0.97 vs 0.34–0.40; UrgentSFT-8B on PMR-Bench arXiv 2601.13178 outperforms GPT-OSS-120B). Our entire Sprint 2 synthetic dataset is 300–500 items — right in the sweet spot.
2. **R1 finding #3 rules out the "big model + CoT" design pattern** that C1/C2/C4 lean on. The arXiv 2509.21933 study (95 LLMs × 87 clinical text tasks) found **86.3% of models degraded with CoT prompting**. Candidates that rely on chain-of-thought as the primary reasoning lever are therefore risky; candidates that use rules + fine-tuning as the primary lever (C3) are safer.
3. **C3 provides the most regulatory-defensible audit trail.** Rules-first routing with explicit decision tables is directly auditable by GPs and clinical reviewers; fine-tuned small models have fewer moving parts than agentic pipelines. For the TGA Class IIa + HIPC 2020 + Medical Products Bill transitional regime (see R2), this is the easiest posture to defend.

**However, the shortlist is deliberately four candidates deep because clinical accuracy is the final arbiter.** C1 has the highest published closed-model ceiling on triage vignettes. C2 has the strongest sovereignty story. C4 most directly targets the dominant real-world failure mode. Sprint 3 evaluation on the synthetic dataset will pick the winner on per-class sensitivity, macro F1, QWK, and operational fit — not on this recommendation's priors.

**All four candidates preserve the ALEX differentiator.** ALEX FHIR API integration is an infrastructure-layer concern (the PMS data path), not a model-layer concern — see [[research-r6-data-standards-pms-integration]] (forthcoming). The four candidates differ in how they *use* the data that ALEX provides, not in whether they can consume it.

**Budget posture.** All four candidates fit inside the NZD $177k Objective 1 envelope. C3 is cheapest to evaluate in Sprint 3 (tiny fine-tune budget; most compute goes to inference). C1 is cheapest to run at small scale (1k docs/day) but most expensive per-million-tokens at scale; see R7 §7 for the head-to-head cost curve. The cross-over point between Bedrock NZ Haiku 4.5 and Catalyst C1A self-hosted is ~20,000 documents/day — below, Bedrock wins on cost; above, self-hosted wins.

---

## 2. Candidate C1 — Bedrock NZ Claude (tiered Haiku 4.5 + Sonnet 4.6)

### 2.1 Architecture overview

A managed, closed-frontier stack using **two-tier Claude on Bedrock `ap-southeast-6`**:

- **Tier 1 — Claude Haiku 4.5** handles the main flow: reads each incoming document, returns a structured JSON object with urgency, rationale, document type, and confidence. Input assembly: system prompt (locked, version-pinned) + dynamic few-shot retrieval (5 exemplars from a 200-item exemplar bank indexed by embedding similarity) + patient context from ALEX FHIR (current problem list, recent labs, medications) + the document itself.
- **Tier 2 — Claude Sonnet 4.6** is invoked only as an arbiter on low-confidence items (abstention-gated by Tier 1 confidence score ≤ 0.85 or when Tier 1 returns Immediate/Urgent — always verify upward-triage). Sonnet 4.6 receives the same input plus Tier 1's output and rationale, and returns a verified urgency + short rationale.
- **Prompt optimisation:** DSPy MIPROv2 runs over the 300–500 synthetic items to learn the best system prompt + few-shot exemplar selector. This is parameter-free from the model's perspective (no weight updates) and works equally well on closed and open models (Khattab et al. arXiv 2407.10930).
- **Structured output:** Anthropic's tool-use API enforces JSON schema compliance natively; no XGrammar layer needed on Bedrock.

### 2.2 Handling each Inbox Helper document type

| Document type | Structure | Tier 1 approach | Tier 2 invocation rate (expected) |
|---|---|---|---|
| **Lab results** | HL7 ORU (structured values, flags, reference ranges) | Haiku 4.5 reads the structured fields + impression section; RCPA/AACB critical flag detection logic is encoded in the prompt | ~5% (boundary cases with multiple abnormal values) |
| **Radiology reports** | Semi-structured (impression + findings + clinical context) | Haiku 4.5 reads the full text with explicit attention to RCR red-flag language | ~10% (ambiguous language, non-specific findings) |
| **Discharge summaries** | Unstructured narrative | Haiku 4.5 reads full text (up to 200k context), flags "action items" scattered across body/plan | ~20% (the hardest class — action items often implicit) |
| **Specialist letters** | Unstructured narrative | Haiku 4.5 reads full text, flags critical findings in any position | ~15% (phrasing variation between specialists) |
| **Patient messages** | Short free text | Haiku 4.5 reads + applies published emergency detection logic (Chen et al. JAMIA 2025 KG-RAG 0.99 accuracy, 0.98 sensitivity) | ~8% (emotional or ambiguous language) |

**Expected overall Tier 2 invocation rate: ~10–12% of all documents.** At 10k docs/day that's ~1,000–1,200 Sonnet 4.6 calls/day — non-trivial cost driver.

### 2.3 Handling Care Gap Finder sub-tasks

| Sub-task | Approach |
|---|---|
| **A. Gap detection** (deterministic rules) | Python rules engine outside the LLM — not a Claude task. Same as all other candidates. |
| **B. Variable extraction** (PREDICT CVDRA inputs from free text) | Claude Haiku 4.5 via tool use / structured output. 15 variables, mostly structured; 3 commonly missing (family history, NZDep, AF confirmation) use few-shot extraction prompts with explicit "unknown" fallback. |
| **C. CVDRA calculation** | Pure Python implementation of HISO 10071:2025 PREDICT v.2019 equations. Not an LLM task. |

### 2.4 Expected accuracy ceiling (grounded in R1)

- **Triage vignettes (most comparable benchmark):** JMIR 2024 Sorich et al. reported Claude 3.5 Sonnet at **94% on 48 clinical vignettes** with 4 triage levels (45/48 correct). Claude Sonnet 4.6 is a generation newer and should match or exceed; Claude Haiku 4.5 should be within 3–5 points of Sonnet on this task class.
- **Clinical classification generally:** R1 §2.1 reports zero-shot frontier models at F1 0.75–0.92 depending on task complexity.
- **With dynamic few-shot (JAMIA 2025):** +39.3% macro F1 over zero-shot is the published ceiling. Expect our MIPROv2-optimised few-shot prompt to land in the top-third of that gain.
- **Emergency detection in patient messages (Chen et al. JAMIA 2025):** 0.99 accuracy / 0.98 sensitivity with GPT-4o + KG-RAG. Claude Haiku 4.5 + our exemplar bank should match within 1–2 points.

**Target:** macro F1 ~0.88–0.92, per-class sensitivity ≥99% on Immediate/Urgent (achieved via the Tier 2 arbiter + abstention-on-upward-triage rule).

### 2.5 Contextual reasoning failure mitigation (NHS 6:1 finding)

The NHS GPT-oss-120b study found contextual reasoning failures outnumber factual errors 6:1 in primary care LLM deployments (arXiv 2512.21127). C1 mitigations:

1. **Always-invoke Tier 2 arbiter on upward triage.** Any Tier 1 Immediate or Urgent classification is automatically verified by Sonnet 4.6 with the full input + Tier 1 output. Sonnet 4.6's agreement ≥99% sensitivity on upward triage.
2. **Explicit patient context injection.** ALEX FHIR provides current problem list, recent labs, active medications. These are placed in the prompt prefix (cacheable). This gives the model the "who is this patient" context that the NHS study found missing in 6-of-7 failures.
3. **Few-shot exemplar retrieval is contextual, not generic.** The 5 retrieved exemplars are selected by embedding similarity to the incoming document and patient context, so the model sees examples that share the operative context.
4. **DSPy MIPROv2 over a training set that includes NHS-style contextual stress items** (see R5 synthetic dataset design — R5 is briefed to deliberately include items where the raw facts look benign but context escalates urgency).
5. **No CoT as primary reasoning lever.** Per R1 §2.6 (arXiv 2509.21933, 86.3% CoT degradation), we rely on structured output + Tier 2 verification, not verbose reasoning.

### 2.6 Cost (per R7 §7.2 and §7.4)

At 10k docs/day with 2,000 tokens/document and 10% Tier 2 arbiter invocation:
- **Tier 1 Haiku 4.5:** ~NZD $1,512/month (from R7 §7.2 modelling)
- **Tier 2 Sonnet 4.6 at ~10% invocation:** Sonnet 4.6 is ~5× Haiku = ~NZD $750/month
- **Total:** ~**NZD $2,260/month at 10k docs/day**
- **At 1k docs/day:** ~NZD $226/month — much cheaper than any self-hosted option at small scale

### 2.7 Latency

- **Tier 1 Haiku 4.5:** p50 ~1.5s, p95 ~3s per document (published Bedrock latency for Haiku class)
- **Tier 2 Sonnet 4.6 on ~10% of items:** adds ~4–6s on those items; end-to-end p95 on arbitrated items ~8s
- **Overall p95 across all items:** ~5s (inflated by the Tier 2 tail)
- **Async inbox processing tolerates this comfortably.**

### 2.8 Sovereignty fit

See [[research-r2-nz-sovereign-hosting-regulatory]] §2. Bedrock in `ap-southeast-6` launched March 2026 and is the lowest-friction NZ-hosted option. **Open question:** are Haiku 4.5 and Sonnet 4.6 natively available in `ap-southeast-6`, or cross-Region routed to `ap-southeast-2` (Sydney)? R2 §11 flags this as the #1 escalation to AWS NZ — must be resolved before committing. If cross-Region only, the sovereignty story requires a cross-Region inference profile that keeps data within the ANZ geographic boundary, and must be disclosed in the DPIA (R2 §8).

### 2.9 Implementation effort

**~2 engineer-weeks for Sprint 3 stand-up.** Bedrock SDK integration + prompt templates + DSPy MIPROv2 run + Tier 2 arbiter wiring + logging. Fastest to stand up of all four candidates.

### 2.10 Key failure modes

1. **Cross-Region inference routing surprise** — see R2 §2 and §9. Data residency implications if not pinned to `ap-southeast-6` natively.
2. **Opaque guardrail bypass** — Anthropic's safety filters can block legitimate clinical queries; the Heidi Health March 2026 Mindgard disclosure (R2 §9) showed 3 prompts can bypass NZ health AI guardrails. Not Claude-specific but the defensibility posture applies.
3. **Vendor deprecation risk** — Anthropic deprecates Claude versions on its own schedule; our pinned version may need re-validation at short notice.
4. **Per-token pricing volatility** — Anthropic can raise prices mid-grant; no backup until we've stood up a self-hosted stack.
5. **Knowledge-practice gap** — R1 finding #4 (JMIR 2025): LLMs score 84–90% on knowledge but 45–69% on practice benchmarks. Zero-shot Claude on our synthetic data may hit a ceiling below target sensitivity without aggressive few-shot + arbitration.

### 2.11 Risks / unknowns

- Native vs cross-Region model availability in `ap-southeast-6` (highest priority — R2 §11 escalation).
- Real NZD pricing for Haiku 4.5 in `ap-southeast-6` (Sydney pricing is the modelling proxy).
- Tier 2 invocation rate on real clinical data may exceed 10% (would blow out cost projections).
- DSPy MIPROv2 effectiveness on Claude via Bedrock is less well-documented than on OpenAI/Anthropic direct API.

### 2.12 Ruling criteria

**Rule in if:** Tier 1 + Tier 2 reaches ≥99% sensitivity on Immediate/Urgent on the synthetic eval set, macro F1 ≥ 0.85, QWK ≥ 0.75, end-to-end p95 latency ≤ 8s, AWS confirms `ap-southeast-6` native Claude availability or cross-Region inference within an acceptable data-residency profile.

**Rule out if:** Bedrock cross-Region routing cannot be pinned to ANZ geography (hard sovereignty fail); sensitivity ceiling <99% on Immediate/Urgent after MIPROv2 tuning; Tier 2 invocation rate >25% on real data (cost blow-out); Anthropic deprecates Haiku 4.5 or Sonnet 4.6 before Sprint 4 (forces re-validation).

---

## 3. Candidate C2 — Catalyst NZ Llama 3.3 70B + SGLang three-tier cascade

**One-line:** Open-model, 100% NZ-sovereign, three-tier cascade (BioClinical ModernBERT pre-classifier → Llama 3.3 70B AWQ INT4 main classifier on SGLang deterministic mode → MedGemma 27B-IT arbiter), self-hosted on Catalyst Cloud C1A RTX A6000 48GB instances. This is R7 Stack A lifted verbatim into the shortlist.

### 3.1 Architecture overview

- **Tier 0 (pre-classifier):** **BioClinical ModernBERT 396M** (MIT licence, arXiv 2504.10724) — fine-tuned on our synthetic dataset as a 4-class ordinal head. Runs CPU-side or on a shared A6000. Purpose: cheap first-pass triage and confidence scoring. Confidence ≥0.90 routes straight to a deterministic output; lower confidence escalates to Tier 1. Expected to handle ~60% of documents (mostly structured labs and clear-cut routine/information-only).
- **Tier 1 (main LLM):** **Llama 3.3 70B Instruct, AWQ INT4 quantised**, served on **SGLang deterministic mode** (batch-invariant deterministic inference works on SM 8.6; see R7 §3.4). Structured JSON output via XGrammar (default in SGLang). Few-shot retrieval bank + optional LoRA adapter fine-tuned on the synthetic set.
- **Tier 2 (arbiter):** **MedGemma 27B-IT** (R7 §2.3) invoked only on (a) Tier 1 abstention, (b) Tier 1 classification flagged "Immediate" or "Urgent" with calibrated confidence <0.95, (c) Tier 1 / Tier 0 disagreement by ≥2 levels. Second-opinion verification targets the NHS 6:1 contextual-reasoning failure mode directly.
- **Recall-optimisation cocktail (R1 §4, R7 §6.5):** weighted focal loss on Tier 0 LoRA head, temperature scaling (Guo 2017) post-hoc calibration, per-class conformal prediction (Angelopoulos & Bates arXiv 2107.07511) for confidence-gated abstention.
- **Hardware:** single Catalyst C1A RTX A6000 48GB per production replica; 2 replicas for HA at deployment. Llama 3.3 70B AWQ INT4 fits in ~40GB VRAM; MedGemma 27B-IT fits on the same card time-sharing or a second shared A6000.
- **Inference engine decision:** SGLang over vLLM because vLLM's batch-invariant deterministic mode requires SM ≥9.0 (Hopper), and A6000 is SM 8.6 (Ampere). SGLang deterministic mode works on SM 8.6 at ~30% throughput cost. This is the architectural reason C2 is SGLang, not vLLM. See R7 §3.

### 3.2 Inbox Helper handling per document type

| Doc type | Tier 0 (ModernBERT) | Tier 1 (Llama 3.3 70B) | Tier 2 (MedGemma) |
|---|---|---|---|
| **Lab results (HL7 ORU)** | Structured features from LOINC/value/flag → ~80% handled at Tier 0 with ≥0.95 confidence | Rare; only when lab context (delta interpretation, medication interaction) triggers escalation | Only on Immediate/Urgent calls with low confidence |
| **Radiology reports** | Impression-section features → ~50% at Tier 0 | Most radiology escalates — semantic reading of narrative impression required | Any "acute" finding flagged Immediate/Urgent |
| **Discharge summaries** | Length + keyword features → Tier 0 mostly as screening only | All discharge summaries go to Tier 1 by policy (R1 §5 recall bias) | Invoked on any action-item detection flagged Urgent/Immediate |
| **Specialist letters** | Tier 0 provides section-less screening | All specialist letters → Tier 1 | Arbiter always invoked on Immediate calls (sub-5% volume) |
| **Patient messages** | Intent-style classification; low base-rate Urgent | All patient messages → Tier 1 (portal content variance is high) | Mandatory arbiter on any Urgent flag; NHS 6:1 pattern hits hardest here |

### 3.3 Care Gap Finder sub-task handling

- **Sub-task A (rules engine):** deterministic Python; no LLM involvement. Identical across all 4 candidates.
- **Sub-task B (variable extraction):** Llama 3.3 70B with SGLang XGrammar-constrained JSON output. 70B size overkill for structured-field extraction but necessary for free-text derivation (family history, NZDep, AF narrative confirmation). LoRA adapter trained on synthetic extraction examples. Hallucination control via XGrammar grammar + post-hoc schema validation + confidence gating → GP review for uncertain extractions.
- **Sub-task C (CVDRA calculation):** deterministic Python; no LLM. Same module as C1.

### 3.4 Expected accuracy ceiling

- **Llama 3.3 70B** on primary-care triage — R1 §2 and R7 §2.2 cite BRIDGE (arXiv 2504.19467) top-quintile performance and JAMA Health Forum March 2025 (Llama 3.1 405B ~70% vs GPT-4 64% on NEJM cases). Llama 3.3 70B at AWQ INT4 preserves ~99% of BF16 quality on classification tasks per Kurtic et al. ACL 2025 (arXiv 2411.02355).
- **With three-tier cascade + arbitration:** extrapolating from Chen et al. JAMIA 2025 (KG-RAG emergency detection: 0.99 accuracy, 0.98 sensitivity), and UrgentSFT-8B beating GPT-OSS-120B on PMR-Bench (R1 §2, arXiv 2601.13178), we expect this stack can reach ≥0.85 macro F1 and ≥0.95 sensitivity on Immediate/Urgent with the synthetic dataset. **Reaching the hard ≥99% sensitivity target likely requires the Tier 2 arbiter carrying the tail risk.**
- **Ordinal QWK target ≥0.75** should be achievable given the explicit 4-level classification target and focal-loss training on Tier 0.

### 3.5 Contextual reasoning failure mitigation (NHS 6:1 pattern)

- **Structural answer: second-opinion arbitration.** MedGemma 27B-IT is a different architecture family (Gemma 3) trained on different data to Llama 3.3 — cross-family disagreement is a stronger contextual-reasoning check than a same-model self-reflection (which NHS study flagged as failing on contextual errors).
- **Deterministic inference** (SGLang deterministic mode) enables reproducible replay of failing cases for post-incident analysis — a significant regulatory-audit advantage.
- **Knowledge-practice gap (R1 finding #4):** addressed by few-shot retrieval of *similar past clinical scenarios*, not just guideline text — grounds reasoning in context, not just facts.
- **Known residual risk:** contextual reasoning cannot be fully eliminated; see §3.10.

### 3.6 Cost at production scale

Per R7 §5 and §7 (grounded in Catalyst Cloud Aotearoa price list, April 2026):

| Workload | GPU fleet | Monthly NZD (fully loaded) | Per-1k docs NZD |
|---|---|---|---|
| 1,000 docs/day | 1 × C1A A6000 (dev + inference) | ~NZD $3,200/mo | ~NZD $107 / 1k docs |
| 10,000 docs/day | 2 × C1A A6000 (HA) | ~NZD $6,400/mo | ~NZD $21 / 1k docs |
| 20,000+ docs/day | 3 × C1A A6000 | ~NZD $9,600/mo | ~NZD $16 / 1k docs |

**Cross-over:** C2 becomes cheaper than C1 (Bedrock Haiku 4.5) at approximately **20,000 docs/day**. Below that volume, C1 is cheaper; above it, C2 is cheaper and the gap grows. Per R7 §7, the 6-month Sprint 2–4 compute envelope for C2 evaluation is approximately **NZD $19,200** (6 months × $3,200/mo), comfortably within the $177k grant budget.

### 3.7 Latency

- **Tier 0 ModernBERT 396M on A6000:** ~50–80 ms per document.
- **Tier 1 Llama 3.3 70B AWQ INT4 SGLang deterministic:** ~1.5–3 s per doc (deterministic mode adds ~30% over default; R7 §3).
- **Tier 2 MedGemma 27B-IT (when invoked):** ~1–2 s per doc.
- **End-to-end p50:** ~0.5 s (Tier 0 absorbs most); **p95 (with Tier 1 + Tier 2):** ~5–7 s.
- Acceptable for inbox triage (async, not interactive clinical decision point).

### 3.8 Sovereignty fit

- **Strongest-possible sovereignty posture.** Catalyst Cloud NZ: 100% NZ-owned, NZ-operated, three NZ data centres, ISO 27001 + ISO 27017 certified (R7 §5, R2 §3). Data never leaves Aotearoa. MBIE N2RD grant clause ("R&D undertaken outside New Zealand is not eligible") is satisfied by construction, with no ambiguity.
- **Fully defensible under HIPC 2020 and Privacy Act 2020** (R2 §5). No cross-border disclosure to argue about, no Privacy Commissioner correspondence required before standing it up.
- **Single-provider concentration risk:** Catalyst is the only credible NZ-sovereign GPU provider as of April 2026 (R7 §5). Disaster recovery plan required in §3.11.

### 3.9 Implementation effort

**~5 engineer-weeks for Sprint 3 stand-up.** Longer than C1 because of:
- SGLang deployment + deterministic mode configuration on Catalyst C1A
- AWQ INT4 quantisation of Llama 3.3 70B (use Red Hat AI / Neural Magic published quant or re-run with AutoAWQ)
- Tier 0 ModernBERT fine-tuning (~1 week including label prep)
- Tier 2 arbiter wiring + conformal prediction calibration
- MedGemma deployment (smaller but second model on same or separate instance)
- Observability: Arize Phoenix + Prometheus + Grafana (R7 §8)

### 3.10 Key failure modes

1. **Contextual reasoning residuals survive arbitration** — if MedGemma and Llama share failure modes on the same context, arbitration doesn't help. NHS 6:1 pattern is the dominant concern.
2. **AWQ INT4 accuracy cliff on clinical edge cases** — quantisation is ~99% faithful on average but can fail on tail cases (QM-ToT arXiv 2504.12334). Mitigation: reserve option to run BF16 on 2 × A6000 if INT4 underperforms (Kurtic et al. "Give Me BF16 or Give Me Death", arXiv 2411.02355).
3. **Catalyst GPU availability** — A6000 capacity is shared; production replicas may need advance reservation.
4. **Single-provider failure** — Catalyst regional outage has no failover within NZ.
5. **Open-model drift** — Llama 3.3 → Llama 4 upgrade requires re-quantisation, re-calibration, potential re-fine-tune of Tier 0.

### 3.11 Risks / unknowns

- Catalyst C1A instance availability at production scale (2–3 replicas on-demand is the known case; burst capacity less clear).
- SGLang deterministic mode stability at high concurrent batch sizes.
- BioClinical ModernBERT fine-tuning quality on a 300–500 sample set (likely insufficient alone — may need data augmentation or larger synthetic generation).
- Whether MedGemma 27B-IT licence permits commercial clinical use without Google-specific terms negotiation.
- DR plan: secondary NZ provider or cross-Tasman Bedrock failover — neither is fully sovereign; §3.10 risk #4 remains.

### 3.12 Ruling criteria

**Rule in if:** three-tier cascade reaches ≥0.95 sensitivity on Immediate/Urgent on synthetic eval with ≤10% Tier 2 invocation rate, macro F1 ≥0.80, QWK ≥0.72, end-to-end p95 ≤8s, Catalyst confirms sustainable A6000 availability for a 2-replica production footprint.

**Rule out if:** Tier 1 sensitivity ceiling below 0.90 after LoRA + few-shot tuning (arbiter cannot save it); AWQ INT4 quality regression >3 percentage points on macro F1 vs BF16 baseline; Catalyst cannot guarantee A6000 availability beyond dev scale; SGLang deterministic mode unstable at our batch sizes.

---

## 4. Candidate C3 — Hybrid rules-first + small fine-tuned LLM (**recommended first to evaluate**)

**One-line:** Rules engine handles everything a rule can handle (labs against RCPA/AACB thresholds, structured radiology flags, protocol-matched specialist follow-ups); everything else routes to a **small, heavily fine-tuned 8B-class LLM** (UrgentSFT-style Llama 3.1 8B LoRA, or alternatively fine-tuned BioClinical ModernBERT as the sole classifier for tier 1). Maximally auditable; cheapest and fastest to evaluate; strongest regulatory defensibility.

### 4.1 Why this is the recommended first-to-evaluate candidate

Three R1 findings converge on this shape:

1. **R1 Finding #1 — fine-tuned small models outperform zero-shot large models.** arXiv 2504.21191 reports fine-tuned small models hitting F1 0.95–0.97 vs zero-shot large models at 0.34–0.40 on clinical document tasks. UrgentSFT-8B (a Llama 3.1 8B LoRA fine-tuned for urgency triage) beats GPT-OSS-120B zero-shot on PMR-Bench (arXiv 2601.13178). **A 8B fine-tune can credibly meet our sensitivity target at a fraction of the compute cost of C1 or C2.**
2. **R1 Finding #3 — 86.3% of models *degrade* with chain-of-thought** on clinical classification (arXiv 2509.21933). Big-model-with-CoT designs (which C1 partially relies on via Claude Sonnet 4.6 arbitration) carry a measurable downside. A small fine-tuned classifier with no CoT avoids that trap.
3. **Regulatory defensibility.** The combination of (a) explicit rules that a GP can read and audit, (b) a small classifier whose training data is our own labelled synthetic set, and (c) no frontier-model dependency is the cleanest TGA Class IIa / HIPC DPIA story of any candidate. Every decision path is reproducible, every training input is known, every rule is human-readable.

### 4.2 Architecture overview

- **Layer 1 — Deterministic rules engine** (Python, DMN-style or plain decision tables; see R4 §2). Handles:
  - All lab results where RCPA/AACB critical thresholds apply (immediate flag straight through).
  - All structured radiology flags (PI-RADS 4/5, BI-RADS 4/5, Lung-RADS 4X, acute haemorrhage keywords).
  - All care gap detection (sub-task A — structured PMS query against interval rules).
- **Layer 2 — Fine-tuned small LLM classifier.** Two viable model choices evaluated in parallel:
  - **Option 2a: Llama 3.1 8B Instruct + LoRA** on our synthetic dataset (UrgentSFT pattern, arXiv 2601.13178). 4-class ordinal head with focal loss, temperature-scaled calibration, conformal abstention gate.
  - **Option 2b: BioClinical ModernBERT 396M + classification head** (MIT licence, arXiv 2504.10724). Smaller, cheaper, sometimes matches the 8B on narrow classification.
  - Sprint 3 evaluates both in a head-to-head on the synthetic set.
- **Layer 3 — Abstention + GP review gate.** Any document the rules don't match AND the classifier returns with conformal confidence below threshold → flagged "uncertain — GP review" (recall-safe abstention).
- **Hosting:** Either Catalyst Cloud C1A A6000 (8B LoRA fits on a single GPU in FP16 with plenty of headroom) or, at smallest scale, CPU-only for ModernBERT 396M. This is the cheapest-to-host candidate.

### 4.3 Inbox Helper handling per document type

| Doc type | Layer 1 (rules) | Layer 2 (8B LoRA or ModernBERT) | Abstention rate (expected) |
|---|---|---|---|
| **Lab results (HL7)** | ~90% handled purely by rules (RCPA/AACB thresholds + delta flags) | Remaining 10% (complex multi-analyte, missing reference ranges) | <2% |
| **Radiology reports** | ~30% handled (structured impression codes, clear critical flags) | ~60% narrative handled by classifier | ~10% |
| **Discharge summaries** | Minimal rule coverage (keyword triggers only) | Primary workload for classifier | ~15% — GP review gate is biggest here |
| **Specialist letters** | ~20% (protocol-matched follow-up detection) | Primary workload | ~10% |
| **Patient messages** | ~5% (explicit keywords only) | Primary workload; classifier on short text is well-studied | ~8% |

### 4.4 Care Gap Finder sub-task handling

- **Sub-task A:** Rules engine (same as all candidates).
- **Sub-task B (variable extraction):** Hybrid. Structured PMS fields extracted via deterministic parsing; the 3 problem variables (family history, NZDep, AF narrative) handled by a small *extraction-fine-tuned* model (same 8B base as the classifier or a separate extraction head on ModernBERT). XGrammar-constrained JSON if using 8B on SGLang; pydantic-validated if using ModernBERT.
- **Sub-task C:** Deterministic CVDRA calculation (same as all candidates).

### 4.5 Expected accuracy ceiling

- **Layer 1 rules** on lab results and structured radiology: near 100% accuracy by construction (rules match exactly or they don't).
- **Layer 2 8B fine-tune on full-text docs:** UrgentSFT-8B on PMR-Bench (R1 §2, arXiv 2601.13178) reports macro F1 in the 0.85–0.92 range on clinical urgency tasks with a few hundred labelled examples. R1 LoRA results on 200–500 example datasets hit F1 0.64–0.95 (arXiv 2504.21191, JMIR 2025).
- **Composite accuracy target:** ≥0.88 macro F1 achievable, ≥0.97 sensitivity on Immediate/Urgent achievable *with* Layer 3 abstention carrying the tail (abstention shifts risk from false-negative to GP-review-load).
- **Headline:** hardest to prove ≥99% sensitivity on Immediate/Urgent without abstention load blowing out; the evaluation question is whether abstention rate stays ≤12% at the 99% sensitivity point.

### 4.6 Contextual reasoning failure mitigation (NHS 6:1 pattern)

- **Structural answer: rules catch most of the high-stakes factual cases; classifier is asked to judge only what rules can't.** This narrows the classifier's decision surface and reduces the contextual reasoning load.
- **Confidence-gated abstention + GP review** is the primary backstop — if the classifier is uncertain, a human reads it. The R1 finding that small fine-tunes + good calibration beat large zero-shot models on clinical tasks applies directly.
- **No CoT reasoning** in Layer 2 (classifier is a direct-output model) — sidesteps the R1 finding #3 CoT-degradation trap.
- **Weakness:** when the classifier is *confidently wrong* on a context-sensitive case, there is no second-model arbiter (unlike C1 and C2). This is the principal trade-off of choosing auditability over ensemble diversity.

### 4.7 Cost at production scale

| Workload | Hosting | Monthly NZD (fully loaded) | Per-1k docs NZD |
|---|---|---|---|
| 1,000 docs/day | 1 × C1A A6000 (dev + inference shared) | ~NZD $3,200/mo | ~NZD $107 / 1k docs |
| 10,000 docs/day | 1 × C1A A6000 (classifier has ample headroom for 8B) | ~NZD $3,200/mo | ~NZD $11 / 1k docs |
| 20,000+ docs/day | 2 × C1A A6000 (HA) | ~NZD $6,400/mo | ~NZD $11 / 1k docs |

**Sprint 3 evaluation cost is the lowest of any candidate.** Llama 3.1 8B LoRA training runs complete in hours on a single A6000; ModernBERT fine-tuning runs in under an hour on CPU or GPU. Total Sprint 3 compute bill for C3 evaluation is estimated at **~NZD $500–1,500**, including a handful of LoRA/hyperparameter sweeps.

### 4.8 Latency

- **Layer 1 rules:** <10 ms per document.
- **Layer 2 Llama 3.1 8B on SGLang A6000:** ~200–400 ms per doc with JSON-constrained output.
- **Layer 2 BioClinical ModernBERT on A6000:** ~30–60 ms per doc.
- **End-to-end p50:** ~50 ms; **p95:** ~500 ms. **Fastest of any candidate.**

### 4.9 Sovereignty fit

- **Fully NZ-sovereign** when hosted on Catalyst Cloud (same posture as C2). 8B on a single A6000 means the minimum-viable Catalyst footprint is smaller than C2. Can optionally run on lighter C1A SKUs if available.
- **Fully MBIE N2RD grant compliant** with no cross-border cloud ambiguity.
- **Audit trail:** strongest of any candidate — rules are human-readable, classifier training data is our own labelled set, no frontier-model API dependency. The cleanest DPIA story.

### 4.10 Implementation effort

**~3 engineer-weeks for Sprint 3 stand-up.** Breakdown:
- Rules engine (Python + test harness) — ~1 week.
- Llama 3.1 8B LoRA fine-tune loop (Unsloth/Axolotl) — ~3 days including sweep.
- BioClinical ModernBERT fine-tune (parallel evaluation) — ~2 days.
- Calibration + conformal abstention + ruling criteria evaluation — ~3 days.
- Integration + observability (minimal stack: Arize Phoenix + Prometheus) — ~2 days.

### 4.11 Key failure modes

1. **Abstention rate blow-out** — if the classifier's confidence is diffuse, the GP-review gate triggers too often and the product becomes a worklist generator instead of a triage helper.
2. **Classifier confidently wrong** — no second-model arbiter; a context-sensitive miss goes through.
3. **Rules drift** — clinical thresholds (RCPA/AACB, BPAC guidance) change; rules engine needs ongoing maintenance. Less of a model problem than a process problem.
4. **Tiny training set risk** — 300–500 synthetic items may be insufficient to reach the sensitivity target; data augmentation or synthetic-expansion may be required.
5. **BioClinical ModernBERT caps out earlier than 8B** — evaluation must include both to avoid early-committing to the cheaper option.

### 4.12 Risks / unknowns

- Whether UrgentSFT-style LoRA is reproducible on 300–500 items (the published result used more data).
- Whether abstention + GP-review-gate is clinically acceptable to GPs (to be tested in Sprint 1 GP review feedback — see rd-20260405-001 dependency).
- ModernBERT 396M clinical classifier ceiling on long docs (>1024 tokens) — discharge summaries may need chunking.
- Rules engine framework selection (plain Python vs DMN vs CQL) — see R4 §1.

### 4.13 Ruling criteria

**Rule in if:** Layer 1 + Layer 2 reaches ≥0.97 sensitivity on Immediate/Urgent with abstention rate ≤12%, macro F1 ≥0.85, QWK ≥0.75, end-to-end p95 ≤500 ms, rules engine covers ≥80% of lab results by construction.

**Rule out if:** sensitivity ceiling <0.95 on Immediate/Urgent even with aggressive abstention; abstention rate >20% at target sensitivity (worklist problem); no measurable gain from 8B vs ModernBERT (indicates task is dominated by rules and we don't need LLM at all — a result worth knowing).

---

## 5. Candidate C4 — Agentic multi-step pipeline (extraction → classifier → verification)

**One-line:** Explicit multi-agent workflow where a cheap extraction agent pulls structured fields from the document, a classifier agent decides urgency based on *extracted structured facts* (not raw text), and a verification agent cross-checks the classifier's output against the extracted facts and the original document. Each agent is a discrete tool-calling LLM call with its own prompt, eval, and audit trail.

### 5.1 Architecture overview

- **Agent 1 — Extraction agent.** Small LLM (Llama 3.1 8B or Claude Haiku 4.5, configurable) with XGrammar/tool-calling-constrained output. Pulls: document type, named clinical findings, numeric values with units, time references, mentioned medications, mentioned conditions, stated action items, patient demographics if present. Output is a strict JSON schema.
- **Agent 2 — Classifier agent.** Mid-size LLM (Llama 3.3 70B on Catalyst, or Claude Sonnet 4.6 on Bedrock) receiving **only the extracted structured facts + a guideline-retrieval bank** (RAG over RCPA/AACB thresholds, BPAC NZ guidelines, NZSSD, MoH CVDRA). Classifier decides urgency from facts, not raw narrative. Output: label + rationale linking each rationale clause to an extracted fact and a retrieved guideline reference.
- **Agent 3 — Verification agent.** Same size class as classifier (can be a smaller model). Inputs: extracted facts, classifier output with rationale, a re-reading of the original document. Task: "does the classifier's rationale match the document?" Binary pass/fail + reason. On fail, route to GP review (abstention).
- **RAG backbone** (Chen et al. JAMIA 2025, R1 §2, KG-RAG 0.99 accuracy 0.98 sensitivity emergency detection): guideline + critical-threshold retrieval is the highest-leverage R1 finding for this design. Knowledge graph over BPAC / NZSSD / RCPA / AACB / HISO 10071.
- **Hosting:** Either Bedrock NZ (C4a variant: Haiku + Sonnet + Sonnet) or Catalyst NZ (C4b variant: 8B + 70B + 27B MedGemma). Both variants evaluated; cost model varies significantly between them.

### 5.2 Inbox Helper handling per document type

All document types follow the same 3-agent pipeline. The key difference vs C1/C2/C3 is that **the classifier never sees raw narrative text** — it only sees extracted structured facts. This is simultaneously the strongest argument for and against C4:

- **For:** narrows the decision surface, makes rationale auditable, allows guideline-retrieval grounding, addresses NHS 6:1 contextual-reasoning failure by forcing the classifier to reason over facts not prose.
- **Against:** any extraction error cascades into the classifier; performance is capped by the extraction agent; complex narrative context (timeline drift, comorbidity interactions) is flattened out before classification.

### 5.3 Care Gap Finder sub-task handling

- **Sub-task A:** rules engine (same as all candidates).
- **Sub-task B:** Care Gap Finder variable extraction is the **natural home for C4's extraction agent** — agentic extraction over the 15 PREDICT variables, with confidence scoring per variable and explicit "missing/ambiguous" flags. Strongest of any candidate for this sub-task.
- **Sub-task C:** deterministic Python.

### 5.4 Expected accuracy ceiling

- **KG-RAG grounding** (Chen et al. JAMIA 2025) reported 0.99 accuracy, 0.98 sensitivity on emergency detection in a retrieval-augmented clinical LLM — directly analogous to our task. This is the strongest published evidence of a candidate hitting the ≥99% sensitivity target.
- **Multi-agent pipelines** introduce compounding-error risk: if extraction is 95% accurate and classification is 95% accurate on extracted facts, end-to-end is ~0.90. Verification agent is meant to catch those but adds latency.
- **Net expected ceiling:** macro F1 ≥0.87, sensitivity ≥0.98 on Immediate/Urgent when verification agent is aggressive. **Strongest ceiling of any candidate if and only if extraction is reliable.**

### 5.5 Contextual reasoning failure mitigation (NHS 6:1 pattern)

- **Strongest structural answer of any candidate.** By forcing the classifier to reason over extracted structured facts with explicit guideline retrieval, C4 attacks the contextual-reasoning failure mode at its root — the NHS 6:1 pattern arose because models got facts right but misapplied them in context. C4's architecture makes fact-to-reasoning traceability explicit.
- Verification agent provides a second-model cross-check (as in C2), with the additional advantage of reasoning over the extracted rationale rather than re-reading the whole document.
- **Residual risk:** extraction agent failure modes are themselves contextual ("did the discharge summary say the patient stopped the anticoagulant on day 3 or continued it?"). Extraction errors can be subtle.

### 5.6 Cost at production scale

| Workload | Variant | Monthly NZD | Per-1k docs NZD |
|---|---|---|---|
| 1,000 docs/day | C4a Bedrock (Haiku+Sonnet+Haiku) | ~NZD $400/mo | ~NZD $13 |
| 1,000 docs/day | C4b Catalyst (8B+70B+27B) | ~NZD $3,200/mo | ~NZD $107 |
| 10,000 docs/day | C4a Bedrock | ~NZD $4,000/mo | ~NZD $13 |
| 10,000 docs/day | C4b Catalyst | ~NZD $6,400/mo | ~NZD $21 |

C4 is **roughly 2× more expensive per doc than C1** because three model calls per doc instead of one (C1 mostly stays at Tier 1) or two. At the same scale on the same hosting, C4 is the most expensive candidate per-document.

### 5.7 Latency

Three sequential model calls per doc:
- **Extraction (Agent 1):** ~500 ms – 2 s.
- **Classification (Agent 2):** ~1.5 – 3 s.
- **Verification (Agent 3):** ~1 – 2 s.
- **End-to-end p50:** ~3 s; **p95:** ~8 – 12 s. **Slowest of any candidate.**

### 5.8 Sovereignty fit

- **C4a Bedrock variant:** same posture as C1 (awaits R2 §2 open question on native `ap-southeast-6` Claude availability).
- **C4b Catalyst variant:** same posture as C2/C3 (fully NZ-sovereign).

### 5.9 Implementation effort

**~6 engineer-weeks for Sprint 3 stand-up.** The most complex candidate. Requires:
- Three separate agent prompts, each with its own eval harness.
- KG-RAG index build over BPAC / NZSSD / RCPA / AACB / HISO (requires R4 guideline-ingestion work).
- Structured schema design for the extraction-to-classification interface.
- Agent orchestration framework choice (LangGraph, DSPy, or hand-rolled).
- Observability across three agents — more moving parts to debug.

### 5.10 Key failure modes

1. **Extraction error cascade** — if Agent 1 misses a key fact, Agent 2 cannot recover it.
2. **Rationale hallucination** — classifier generates a plausible-sounding rationale linked to wrong extracted facts; verification agent may not catch if the error is subtle.
3. **Latency blow-out** — three sequential calls don't parallelise easily.
4. **Retrieval quality** — KG-RAG requires a well-curated guideline corpus; if retrieval is noisy, classifier quality degrades.
5. **Complexity debt** — debugging a three-agent pipeline is significantly harder than a two-tier classifier; in a 2-person team this is real.

### 5.11 Risks / unknowns

- Whether extraction-then-classify materially outperforms direct-classify on our task with only 300–500 labelled items.
- KG-RAG corpus curation effort (BPAC, NZSSD, RCPA, AACB, HISO 10071) — likely 1–2 engineer-weeks beyond model implementation.
- Verification agent's ability to catch subtle context errors without introducing false rejections.
- Orchestration framework choice — DSPy supports agent workflows but maturity varies; LangGraph is more mature but heavier.

### 5.12 Ruling criteria

**Rule in if:** three-agent pipeline reaches ≥0.98 sensitivity on Immediate/Urgent, macro F1 ≥0.87, verification agent catches ≥60% of Agent-2 errors in error-injection testing, end-to-end p95 ≤12 s, KG-RAG grounded rationale traceability is acceptable to the GP reviewer.

**Rule out if:** extraction-error cascade drops composite accuracy >5 points below C1/C3; p95 latency >15 s; implementation effort >8 engineer-weeks (consumes sprint budget); verification agent provides no measurable improvement over direct-classify (indicates complexity is not earning its keep).

---

## 6. Cross-candidate trade-off table

| Dimension | C1 Bedrock Claude tiered | C2 Catalyst Llama 3.3 70B cascade | C3 Hybrid rules + 8B fine-tune | C4 Agentic 3-step pipeline |
|---|---|---|---|---|
| **Accuracy ceiling (macro F1)** | 0.85–0.90 | 0.83–0.88 | 0.85–0.92 | 0.87–0.92 |
| **Sensitivity ceiling (Immediate/Urgent)** | ≥0.95 (Tier 2 carries tail) | ≥0.95 (arbiter carries tail) | ≥0.97 (abstention carries tail) | ≥0.98 (verification carries tail) |
| **Latency p95 (end-to-end)** | ~5 s | ~5–7 s | **~500 ms** ✅ | ~8–12 s |
| **Cost at 1k docs/day (NZD/mo)** | **~$226** ✅ | ~$3,200 | ~$3,200 | $400 (Bedrock) / $3,200 (Catalyst) |
| **Cost at 10k docs/day (NZD/mo)** | **~$2,260** | ~$6,400 | **~$3,200** ✅ | $4,000 / $6,400 |
| **Cost at 20k+ docs/day** | blows out linearly | ~$9,600 ✅ | ~$6,400 ✅ | blows out linearly |
| **Cost crossover vs C1** | — | ~20k docs/day | ~15k docs/day | — |
| **Sovereignty fit** | awaits R2 §2 clarification on native `ap-southeast-6` | **strongest — 100% NZ** ✅ | **strongest — 100% NZ** ✅ | depends on variant |
| **Implementation effort (eng-weeks)** | **~2** ✅ | ~5 | ~3 | ~6 |
| **Sprint 3 evaluation cost (NZD)** | ~$400 (API calls) | ~$3,200 (compute envelope) | **~$500–1,500** ✅ | ~$4,000+ |
| **Maintainability** | low burden (vendor handles) | moderate (SGLang + quant) | **lowest (rules + small model)** ✅ | highest burden (3 agents + KG) |
| **Auditability / explainability** | moderate (Claude rationale) | moderate (Llama rationale) | **highest (rules are human-readable)** ✅ | high (explicit fact chain) |
| **Data efficiency (needs how much training data?)** | zero (zero-shot) ✅ | modest (LoRA on 300–500) | **strongest fit for 300–500** ✅ | modest (LoRA + RAG corpus build) |
| **Regulatory defensibility (TGA + HIPC)** | moderate (black-box vendor) | strong (self-hosted, deterministic) | **strongest (rules + own classifier)** ✅ | strong (traceable rationale) |
| **Vendor-lock risk** | high (Anthropic deprecation) | low (open weights) | **lowest** ✅ | variant-dependent |
| **NHS 6:1 contextual-failure mitigation** | Tier 2 arbiter | MedGemma cross-family arbiter | narrower decision surface + abstention | **strongest (fact-based reasoning)** ✅ |
| **Matches R1 Finding #1 (small-fine-tune beats zero-shot-large)?** | No (zero-shot large) | Partial (LoRA on 70B) | **Yes (8B LoRA)** ✅ | Partial |
| **Matches R1 Finding #3 (no CoT degradation)?** | risk (CoT-style reasoning) | risk (can be CoT) | **Yes (no CoT)** ✅ | risk (agents can CoT) |
| **Risk of Sprint 3 failing to reach target** | moderate | moderate | **low** ✅ | moderate-high (compounding errors) |
| **Preserves AI reasoning + ALEX differentiator?** | Yes | Yes | Yes (rules + reasoning) | **strongest (explicit reasoning chain)** ✅ |

Ticks mark the best-in-class cell for each row (ties allowed). **C3 wins or ties on 9 dimensions; C1 wins on 3 (small-scale cost, fastest stand-up, zero-shot data efficiency); C2 wins on 2 (sovereignty, open-model scalability); C4 wins on 3 (accuracy ceiling, sensitivity ceiling, fact-traceability).**

---

## 7. Recommended first candidate to evaluate — **C3**

**Recommendation:** Start Sprint 3 with Candidate C3 (Hybrid rules-first + small fine-tuned LLM). Evaluate C1 (Bedrock Claude tiered) in parallel during Sprint 3 as a reference baseline, since it's cheap and fast to stand up (~2 engineer-weeks). Defer C2 and C4 until Sprint 4 unless C3 and C1 both fail to meet ruling criteria.

### 7.1 Rationale

1. **R1 Finding #1 points directly at C3.** arXiv 2504.21191 and UrgentSFT-8B on PMR-Bench (arXiv 2601.13178) show fine-tuned small models reaching F1 0.95–0.97 on clinical document tasks with a few hundred labelled examples, while zero-shot large models hit 0.34–0.40. **Our synthetic dataset size (300–500 items) is exactly the regime where small-fine-tune wins.** Testing a design we have evidence will likely succeed is a better first move than testing designs whose evidence is weaker.
2. **R1 Finding #3 rules out big-model + CoT designs as the first bet.** 86.3% of models degrade with CoT (arXiv 2509.21933) on clinical classification. C3's classifier is a direct-output model — it sidesteps this trap entirely. C1 and C4 both carry some CoT risk; C2 carries moderate risk.
3. **Strongest regulatory defensibility.** TGA Class IIa assist-only + HIPC DPIA + MBIE R&D justification all benefit from the rules-readable + own-classifier + reproducible-training-data story. C3 gives us the cleanest audit trail of any candidate — which matters for the Goal B architecture decision document due end April and for the MBIE Q1 progress report due 31 May.
4. **Lowest Sprint 3 evaluation cost and fastest iteration loop.** ~NZD $500–1,500 compute envelope + ~3 engineer-weeks stand-up + hour-long fine-tune cycles. If C3 hits ruling criteria, Sprint 3 closes on time with money and weeks to spare. If C3 falls short, we still have budget to evaluate C1 or C2 as a fallback in Sprint 4.
5. **Strongest sovereignty posture with the lowest operational burden.** Catalyst Cloud single-A6000 footprint; no frontier vendor dependency; no cross-Region data-residency ambiguity (as in C1); smaller operational footprint than C2 or C4. MBIE N2RD grant clause is satisfied unambiguously.
6. **Fails fast in a useful way.** If C3 fails, we learn exactly which parts of the task rules *can't* handle and which parts the 8B *can't* handle — this result is directly useful for choosing between C1/C2/C4 as the fallback, rather than a generic "the hybrid approach didn't work."

### 7.2 Parallel C1 evaluation rationale

C1 evaluation is cheap (~NZD $400 compute + ~2 engineer-weeks). Running it in parallel gives us:
- A frontier-model reference ceiling for every doc type — important for the sensitivity-gap diagnosis if C3 falls short.
- A fallback candidate already ready to go if C3 rules out and Sprint 4 needs a quick pivot.
- Concrete NZD cost numbers for Bedrock ap-southeast-6 vs the theoretical pricing in R7 §7 — directly answers an R2 open question.
- Validation of whether Bedrock ap-southeast-6 hosts Claude Haiku 4.5 and Sonnet 4.6 natively (R2 §2 open question).

### 7.3 Sequence

- **Sprint 3 Week 1 (26 Apr – 2 May):** Stand up C3 rules engine + Llama 3.1 8B LoRA training loop + BioClinical ModernBERT baseline. Parallel: stand up C1 Bedrock SDK + Claude Haiku 4.5 prompt templates.
- **Sprint 3 Week 2 (3 – 9 May):** Run full evaluation on synthetic set for both C3 and C1. Compare against ruling criteria. Write results into architecture decision document.
- **Sprint 4 (10 – 23 May):** If C3 passes → proceed to extension (more training data, fine-tune refinement, prepare for Obj 2). If C3 fails → evaluate C2 or C4 based on which failure mode dominated.

---

## 8. Sprint 3 evaluation protocol per candidate

### 8.1 Shared evaluation harness (all candidates)

All candidates run against the same 300–500 item synthetic dataset (R5 deliverable). Metrics computed on the stratified enriched eval split (~100–150 per class per doc type) and the natural-prevalence holdout (~300–500 items). Single evaluation harness, configurable by candidate adapter, Python + scikit-learn + jurymax-style bootstrap. Metrics:

- **Per-class sensitivity** (recall) with BCa-bootstrap 95% CIs — Immediate, Urgent, Routine, Information only
- **Per-class PPV** with BCa-bootstrap CIs
- **Macro F1** with BCa CI
- **Weighted accuracy** with BCa CI
- **Quadratic weighted kappa (QWK)** with CI
- **PR-AUC** per high-urgency class
- **MCC** (Matthews correlation)
- **Calibration (ECE)** per class
- **Confusion matrix**
- **Latency percentiles (p50, p90, p95, p99)** per doc type
- **NZD cost per 1k docs** from metered inference log
- **Error taxonomy**: per failure case, tag as factual vs contextual-reasoning (per NHS 6:1 framework)
- **Spectrum audit**: separate metrics on clear-cut vs borderline subsets

### 8.2 Per-candidate baselines

| Candidate | Baseline to compare against |
|---|---|
| C1 Bedrock Claude tiered | Claude Haiku 4.5 zero-shot (no Tier 2); Claude Sonnet 4.6 zero-shot |
| C2 Catalyst Llama 3.3 70B cascade | Llama 3.3 70B zero-shot (no cascade); Tier 0 ModernBERT alone |
| C3 Hybrid rules + 8B fine-tune | Rules-only (no LLM); Llama 3.1 8B zero-shot (no LoRA); ModernBERT alone |
| C4 Agentic 3-step pipeline | Single-call classifier (no extraction-then-classify); no-verification 2-agent variant |

The baselines matter because each candidate's ruling criterion is partly "does the added complexity earn its keep". If Llama 3.3 70B alone reaches 0.90 macro F1 and the cascade reaches 0.88, the cascade is *worse*.

### 8.3 Ruling gate sequence

1. **Hard rule-out**: sensitivity <0.90 on Immediate OR sensitivity <0.90 on Urgent OR weighted accuracy <0.80. Candidate cannot be the architecture.
2. **Target check**: does the candidate reach its own §2.12/§3.12/§4.13/§5.12 ruling-criterion thresholds?
3. **Practicality check**: p95 latency acceptable, cost acceptable, implementation effort within budget.
4. **Differentiator preservation**: AI reasoning + ALEX differentiator intact (automatic for all four candidates by construction).
5. **Error-mode check**: does error taxonomy show NHS 6:1 pattern mitigated? If >50% of remaining errors are contextual-reasoning failures, the mitigation isn't working.

### 8.4 Sprint 3 deliverable

- `sprint-3-architecture-evaluation.md` — table of each evaluated candidate vs ruling criteria, error taxonomy, cost/latency measured, recommendation for Sprint 4 direction.
- `sprint-3-candidate-c3-results.md` (and c1, c2, c4 as relevant) — per-candidate deep dive with full metrics, CIs, confusion matrices, failure case examples.

---

## 9. Assumptions to validate before Sprint 3 (cheap sanity checks)

These are all checkable in under a day each. Any failure shifts the recommendation.

1. **[R2 §2 open question] AWS Bedrock `ap-southeast-6` native Claude availability.** 1-hour check: log into AWS console, attempt a Haiku 4.5 call pinned to `ap-southeast-6`. If the model is only available via cross-Region inference to Sydney, C1 sovereignty posture materially changes and the recommendation to run C1 in parallel must be re-assessed.
2. **[R7 §5 open question] Catalyst Cloud C1A A6000 availability at dev scale.** 1-hour check: contact Catalyst support, provision a C1A instance, run a Llama 3.1 8B + BioClinical ModernBERT inference sanity test. Confirm real latency matches R7 §7 estimates.
3. **Rules-engine coverage estimate for lab results.** 2-hour check: manually walk 30 synthetic lab results through a draft rules set against RCPA/AACB thresholds; confirm ≥80% match a rule unambiguously. If below 60%, rules layer is weaker than C3 assumes and the classifier carries more load.
4. **BioClinical ModernBERT long-document capability.** 2-hour check: run ModernBERT against a 4k-token synthetic discharge summary; confirm it processes without degradation. If it caps at 1k tokens effectively, discharge summaries require chunking logic and Sprint 3 effort increases.
5. **Llama 3.1 8B LoRA feasibility with 300 items.** 4-hour check: on a single A6000, run an Unsloth LoRA training loop on a 300-item stub dataset (can be placeholder data). Confirm training completes, loss decreases, and output is schema-valid. This is the "does the training loop work at all" check, not a quality check.
6. **Bedrock SDK + structured output on Haiku 4.5.** 2-hour check: write a minimal Bedrock Python client using Tool Use for structured JSON output. Confirm it matches C1's expected interface.
7. **Synthetic dataset spectrum coverage.** 2-hour check: once R5 protocol is complete, sample 50 items and confirm that ≥20% are borderline (as the spec calls for); if not, classifier ceiling estimates will be inflated.
8. **GP review load model (C3 abstention gate).** 30-min spreadsheet: project abstention rate × daily document volume × minutes-per-review; confirm the number is operationally tolerable for a single GP. If C3 requires GPs to review >30 docs/day, the abstention-gate model is not clinically acceptable regardless of accuracy.
9. **MedGemma 27B-IT licence for clinical commercial use.** 1-hour check: read the Gemma 3 licence terms + MedGemma card; confirm commercial clinical use is permitted without bespoke Google agreements. If not, C2's arbiter needs to be swapped for an alternative (Llama-3.3-Nemotron medical variant, or another 27B-class open medical model).
10. **SGLang deterministic mode on SM 8.6 stability.** 4-hour check: deploy SGLang deterministic build on the dev A6000 instance from sanity check #2; run 1,000 parallel inference requests and verify bit-exact determinism. If deterministic mode is flaky at throughput, C2 and C3 lose their audit story.

---

## 10. Risks and unknowns (programme-level)

1. **Sensitivity target ≥99% on Immediate/Urgent may be unreachable without unsupportable abstention rates.** R1 §6 notes no published benchmark for GP inbox document triage. The target is an *aspiration* derived from ACS-COT <5% undertriage + clinical safety arguments — it may not be achievable with 300–500 synthetic items. **Mitigation:** plan for Sprint 4 data augmentation from R5 protocol; plan for "sensitivity at abstention rate ≤X%" as the real shipping metric if the hard ≥99% cannot be hit.
2. **Synthetic dataset quality may cap all candidates.** If the synthetic data is too clean (no spectrum of borderline cases), all candidates will over-fit and ceiling estimates are inflated. **Mitigation:** R5 protocol explicitly mandates borderline case proportion; Sprint 3 evaluation must report spectrum-audit metrics separately (§8.1).
3. **GP review feedback from Sprint 1 rd-20260405-001 is due 20 Apr** — *after* Sprint 2 ends on 25 Apr. Late changes to the urgency taxonomy or classification criteria would force rework of the synthetic dataset and all candidate prompts/fine-tunes. **Mitigation:** stage R5 dataset generation to start 13 Apr *before* the feedback deadline with the current taxonomy, and plan a dataset revision day in Sprint 3 Week 1 if feedback changes anything.
4. **NHS 6:1 contextual-reasoning pattern may not be fully mitigatable** by any of the four candidates. The pattern is a structural property of LLM reasoning, not a mitigation target that any architecture fully defeats. **Mitigation:** accept that error mode, require abstention + GP review gate on uncertain contextual cases, document this in the DPIA as the primary residual risk.
5. **Single-provider sovereign hosting (Catalyst Cloud) creates concentration risk** for C2/C3. Regional outage has no in-NZ failover. **Mitigation:** document DR story explicitly in architecture decision; evaluate Bedrock ap-southeast-6 as a secondary NZ-adjacent failover; raise with Lisa Pritchard / MBIE in the regulatory liaison channel.
6. **Frontier model deprecation risk (C1).** Anthropic deprecates models on its own schedule. A model we've pinned and validated could be deprecated mid-grant. **Mitigation:** maintain C2 or C3 as the open-model fallback architecture throughout Objective 1.
7. **MBIE audit defensibility.** MBIE Q1 progress report (due 31 May) must show a defensible architecture decision with sourced evidence. **Mitigation:** the architecture decision document referenced in Sprint 2 literature review must cite R1/R2/R3/R7 by name and include the §6 trade-off table and §7 ruling rationale.
8. **ALEX FHIR API availability for Sprint 3+**. R3 cannot evaluate against real PMS data until R6 confirms Medtech ALEX sandbox access. **Mitigation:** all Sprint 3 evaluation is on synthetic data, which does not depend on ALEX; ALEX integration is a Sprint 4/5 milestone.
9. **Fine-tuning data sufficiency.** Published small-fine-tune wins (R1 Finding #1) typically use 500–5000 items, not 300. **Mitigation:** R5 aims for the upper end (500) and the Sprint 4 plan includes a data expansion option to ~1,500 items before the architecture decision is locked.
10. **Latency unmeasured under NZ clinical network conditions.** All latency estimates are from provider benchmarks or inference-engine papers, not end-to-end from a NZ GP practice. **Mitigation:** sanity check #6 (Bedrock client) and sanity check #2 (Catalyst dev instance) include a real latency measurement step.

---

## 11. Reference list and cross-references

### 11.1 Companion research reports in this vault

- `research-r1-llm-architecture-benchmarks.md` — empirical benchmark evidence grounding candidate accuracy ceilings (Findings #1–#5, Architecture tables §2, Chen et al. JAMIA 2025, JMIR 2024 Sorich et al., BRIDGE, ICPC-2, NHS GPT-oss-120b medication safety)
- `research-r2-nz-sovereign-hosting-regulatory.md` — NZ sovereignty posture, Bedrock ap-southeast-6 status, Catalyst Cloud assessment, HIPC + Privacy Act, Medical Products Bill status check, DPIA methodology
- `research-r7-open-source-llm-self-hosted.md` — open-source model selection (§2), inference engine selection (§3), GPU-to-model fit (§4), Catalyst Cloud pricing (§5), fine-tuning approach (§6), cost head-to-head (§7), production operational considerations (§8), recommended Stack A (§10 — the basis for C2 in this report)

### 11.2 Companion research still pending (Sprint 2 Week 2)

- R4 — Care Gap Finder sub-task architectures (rules engine + variable extraction + CVDRA calculation) — feeds C1/C2/C3/C4 Care Gap Finder sections
- R5 — Synthetic dataset protocol — feeds the Sprint 3 evaluation harness (§8)
- R6 — Medtech ALEX / Indici / HL7 / FHIR / NZ code sets — feeds sanity check #0 (ALEX API capability) and the data-flow layer of each candidate

### 11.3 Internal vault references

- `context/nexwave-rd-context/inbox-helper-task-spec.md` — locked task spec, Step 1 deliverable
- `context/nexwave-rd-context/care-gap-finder-task-spec.md` — locked task spec, Step 1 deliverable
- `context/nexwave-rd-context/Urgency classification for GP inbox triage.md` — urgency taxonomy literature review (locked)
- `context/nexwave-rd-context/Evaluation metrics for ordinal clinical AI triage classification.md` — evaluation metrics literature review (locked)
- `context/nexwave-rd-context/Inbox Management — Competitor Tracker.md` — differentiator validation (ALEX FHIR API opening, RPA/rule-based competitors)
- `projects/nexwave-rd-obj-1.md` — Objective 1 roadmap, Goal B (Architecture Decision) deadline
- `sprints/active/2026-04-rd-sprint-2.md` — active sprint

### 11.4 External references cited (cross-linked from R1 and R7)

- arXiv 2504.19467 — BRIDGE clinical LLM benchmark (95 LLMs, 20 applications)
- arXiv 2504.21191 — Fine-tuned small models vs zero-shot large models on clinical document tasks (F1 0.95–0.97 vs 0.34–0.40)
- arXiv 2601.13178 — PMR-Bench + UrgentSFT-8B beats GPT-OSS-120B zero-shot
- arXiv 2509.21933 — 86.3% of models degrade with chain-of-thought on clinical classification
- arXiv 2507.14681 — ICPC-2 coding benchmark (33 LLMs)
- arXiv 2512.21127 — NHS GPT-oss-120b primary care medication safety review (contextual reasoning failures 6:1 vs factual, 178 failures 148 patients)
- arXiv 2504.10724 — BioClinical ModernBERT 396M (MIT licence)
- arXiv 2411.02355 — Kurtic et al. ACL 2025 "Give Me BF16 or Give Me Death" (BF16 vs quant trade-offs)
- arXiv 2504.12334 — QM-ToT quantisation + medical reasoning
- arXiv 2305.14314 — QLoRA
- arXiv 2402.09353 — DoRA
- arXiv 2407.10930 — Khattab et al. "Fine-Tuning and Prompt Optimization" (DSPy + MIPROv2)
- arXiv 1708.02002 — Lin et al. focal loss
- arXiv 1706.04599 — Guo et al. temperature scaling for calibration
- arXiv 2107.07511 — Angelopoulos & Bates conformal prediction gentle introduction
- Chen et al. JAMIA 2025 — KG-RAG emergency detection (0.99 accuracy, 0.98 sensitivity)
- JMIR 2024 — Sorich et al. Claude 3.5 Sonnet 94% on 48 triage vignettes
- JMIR 2025 — Knowledge-practice gap (84–90% on knowledge vs 45–69% on practice)
- JAMA Health Forum March 2025 — Llama 3.1 405B ~GPT-4 parity on clinical reasoning
- Journal of Medical Systems 2025 (DOI 10.1007/s10916-025-02284-y) — structured prompting triage study (76.82% → 86.20%)
- El-Yaniv & Wiener 2010 — selective prediction with guaranteed error rate
- Red Hat AI / Neural Magic AWQ INT4 quantisation reference implementations
- Catalyst Cloud Aotearoa price list + ISO 27001/27017 certifications (2026)
- AWS Bedrock ap-southeast-6 launch blog (March 2026)

---

*End of Research R3 report.*
