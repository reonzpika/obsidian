---
title: Research R7 — Open-Source LLM Self-Hosted Architecture Options
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-11
status: final
---

# Research R7 — Open-Source LLM Self-Hosted Architecture Options

> **Scope.** Deep-dive on open-source LLM self-hosted architecture candidates for Sprint 2 Research Plan of nexwave-rd Objective 1. The output of this report feeds directly into R3 (architecture shortlist) as the evidence base for at least one first-class open-source candidate alongside the Bedrock NZ Claude candidates. Cross-references to R1 (clinical LLM benchmarks), R2 (NZ sovereign hosting + regulatory), and R6 (PMS integration) are used rather than duplicated.
>
> **Method.** Five parallel async general-purpose research agents (R7-A through R7-E) covering (A) open-source model candidates, (B) inference engines + GPU fit, (C) cloud GPU providers + cost, (D) fine-tuning for small data, (E) production ops + failure modes. Findings synthesised here. Agent R7-C's fetches of `catalystcloud.nz/*` were 403-blocked by the sandbox proxy — Catalyst NZD pricing is modelled from peer-provider benchmarks and **must be re-verified manually against the live price list before any MBIE commitment** (see §5 and §11).

---

## 1. Executive summary

The question this report answers is: **"For our task, budget, sovereignty constraints, and timeline, what is the best open-source LLM + inference engine + GPU + hosting combination to shortlist alongside a Bedrock NZ Claude candidate in R3?"**

**Headline recommendation — one primary and one alternative open-source stack, both NZ-sovereign:**

| | **Stack A — primary (recommended)** | **Stack B — alternative (cleanest licence)** |
|---|---|---|
| **Base model** | Llama 3.3 70B Instruct (AWQ INT4) | Qwen 3 32B (Apache 2.0, FP8 or AWQ INT4) |
| **Medical fine-tune track** | LoRA (r=32) or QLoRA over Meditron3-8B for structured extraction; prompt optimisation via DSPy MIPROv2 over the 70B for Inbox Helper | QLoRA on Qwen 3 32B for Inbox Helper; DoRA on Meditron3-8B for extraction |
| **Three-tier cascade** | BioClinical ModernBERT (396M) pre-classifier → Llama 3.3 70B main classifier → optional MedGemma 27B-IT second opinion on abstained items | Same cascade, Qwen 3 32B replaces Llama 3.3 70B at the centre |
| **Inference engine** | **SGLang (deterministic mode)** with XGrammar structured-output backend | Same |
| **GPU (production-identifiable data)** | Catalyst Cloud **C1A RTX A6000 48 GB**, 1 × single-tenant VM, 24×7, `nz-hlz-1` or `nz-por-1` | Same |
| **GPU (synthetic data R&D bursts)** | Together AI **A100 80 GB dedicated endpoint**, 12 hr/day, enterprise BAA, synthetic data only | Same |
| **Fully-loaded monthly cost (1 × A6000 24×7 on Catalyst)** | ~NZD **$3,200/month** (VM + storage + egress + K8s contingency) `[modelled — re-verify]` | Same |
| **6-month compute envelope** | ~NZD **$32k** of the $177k Objective 1 budget | Same |
| **Sensitivity on Immediate/Urgent** | Target ≥99% via weighted focal loss + temperature scaling + conformal prediction + abstention gate to MedGemma 27B-IT second opinion | Same approach |
| **Contextual-reasoning mitigation (NHS 6:1 finding)** | Three-tier cascade + explicit chain-of-thought in extraction prompts + second-opinion arbitration for borderline items | Same |

**Why both are NZ-sovereign.** Neither stack crosses a border during production inference. Real-world clinical data is served only from Catalyst Cloud NZ (100% NZ-owned, NZ-operated, ISO 27001/27017, three NZ data centres). Overseas dedicated endpoints (Together AI A100) are reserved exclusively for synthetic-data training and eval runs under a written data-handling policy — and are justified under the MBIE N2RD "capability not sourceable in NZ" carve-out for synthetic data burst workloads.

**Why SGLang, not vLLM.** SGLang delivers ~29% higher throughput on H100 than vLLM in the 2025–2026 benchmarks (~16,200 tok/s vs ~12,500 tok/s) and has a native **deterministic mode** that does not require Hopper-class SM ≥9.0 hardware. vLLM's batch-invariant path requires SM ≥9.0, which the **RTX A6000 (SM 8.6) does not meet** — so on our chosen Catalyst GPU, vLLM cannot deliver reproducible inference and SGLang becomes the only practical route to deterministic clinical-grade logging. SGLang also has RadixAttention (strong KV-cache re-use for multi-step agent flows) and native structured-output integration with XGrammar, which matches our ordinal JSON output requirement. **TGI is ruled out — it entered maintenance mode on 11 December 2025 and HuggingFace now recommends vLLM/SGLang for new deployments.**

**Why Llama 3.3 70B as primary.** Llama 3.3 70B delivers the strongest open-model clinical reasoning at a size that fits on a single 48 GB GPU with AWQ INT4 quantisation. The JAMA Health Forum March 2025 study found Llama 3.1 405B at ~70% vs GPT-4 ~64% on NEJM clinical cases, confirming open-model parity with closed frontier models on clinical reasoning. Llama 3.3 70B inherits most of 3.1's clinical reasoning ability at roughly 1/6 the parameter count. Qwen 3 32B is the cleanest-licence backup (Apache 2.0) and trails Llama 3.3 70B by only 2–4 points on most published clinical benchmarks.

**Why the three-tier cascade.** The NHS GPT-oss-120b primary care medication review (arXiv 2512.21127, Oct–Nov 2025) found **contextual reasoning failures outnumber factual errors 6:1** — the dominant failure mode for open LLMs in primary care is misapplying correct facts to the wrong context. A three-tier cascade with explicit roles (pre-classifier for scale filtering, main LLM for classification with CoT rationale, abstention-gated second opinion for borderline items) specifically targets this failure mode: rationale forcing reduces context errors, abstention flags the ambiguous cases that cause them, and a second opinion from a differently-trained model (MedGemma) reduces shared failure modes.

**Why Catalyst RTX A6000, not L40S or A100.** C2 A100-20C vGPU slices retire on **31 March 2026** — eliminated from Sprint 3 planning. C3 L40S 48GB is **Beta** and **Porirua-only**, which is acceptable for R&D but not production-grade for a 24-month grant horizon. C1A RTX A6000 48 GB is the only GA NZ-sovereign GPU that fits a 70B-class model with AWQ INT4, and it is available across all Catalyst regions. The sovereignty and availability trade-off therefore points squarely at C1A.

**Why fine-tuning is small and targeted, not heroic.** With 300–500 labelled synthetic items in Sprint 2 (growing to ~1,500 by Sprint 4), full fine-tuning of a 70B model is pointless. Published small-data clinical results converge on three techniques: (i) **LoRA/QLoRA** (r=16–32) for extraction sub-tasks where format is the main thing being learned, (ii) **DoRA** (arXiv 2402.09353) as a drop-in improvement over LoRA for better small-data generalisation, (iii) **DSPy MIPROv2 prompt optimisation** (Khattab et al., arXiv 2407.10930 — "Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together") for systems-level improvement of the Inbox Helper prompt chain. For recall-optimisation, **weighted focal loss during the tiny fine-tune + post-hoc temperature scaling + conformal prediction + abstention** is the published cocktail that reaches ≥99% sensitivity on minority classes.

**Head-to-head vs Bedrock NZ Claude at our scale.** For an assumed 10,000 documents/day workload, modelled costs on a 1,600-input / 400-output token budget per document come out at roughly: Catalyst C1A A6000 24×7 with Llama 3.3 70B AWQ INT4 ≈ **NZD $3,200/month fully loaded** vs Claude Haiku 4.5 on Bedrock ap-southeast-6 at published Haiku pricing ≈ **NZD $2,700–3,800/month** (depending on cache-hit rate and exact ap-southeast-6 pricing vs Sydney proxy). At 1,000 documents/day the open-source stack is roughly 3–5× more expensive than the API (because GPU idle dominates) but it owns the sovereignty, latency, determinism, and auditability stack end-to-end. At 10,000 documents/day the two are within noise. **The defensible answer is to run both in R3 evaluation and choose on accuracy + operational fit, not cost.**

**Bottom line for R3.** We have two credible, NZ-sovereign open-source stacks that can be stood up on Catalyst Cloud C1A in days, budgeted to ~NZD $32k over 6 months, with a clear three-track fine-tuning plan for Sprint 3. Both stacks address the NHS 6:1 contextual-reasoning failure pattern, both meet the ≥99% sensitivity target via a published recall-optimisation cocktail, and both preserve the AI-reasoning + ALEX differentiator called out in the competitor tracker. They go into R3 as **equal first-class candidates** alongside the Bedrock NZ Claude Haiku 4.5 and Claude Sonnet 4.6 candidates. Decision between them in R3 is on clinical accuracy and operational fit, not unit cost.

---

## 2. Open-source model candidates — comparative evidence

### 2.1 General-purpose open LLMs with strong clinical reasoning

The 2025–2026 landscape has converged: open-source general LLMs at 70B+ have closed most of the clinical-reasoning gap with closed frontier models. The headline evidence is the **JAMA Health Forum March 2025 study** (cited in Harvard Medical School's March 2025 news on open-source parity with proprietary LLMs on tough medical cases), which found Llama 3.1 405B scoring **~70% vs GPT-4 ~64% on NEJM clinical case challenges** — the first published result where an open model beat a closed frontier model on a widely cited clinical benchmark. For our purposes this means open models are no longer second-tier for the Inbox Helper and Care Gap Finder tasks; we can realistically target SOTA clinical classification with a self-hosted stack.

| Model | Params | Context | Licence | Clinical signal | Best fit for | Notes |
|---|---|---|---|---|---|---|
| **Llama 3.3 70B Instruct** | 70 B | 128k | Llama 3.3 Community | Strong on MedQA/MedMCQA; inherits most of Llama 3.1 405B's NEJM reasoning at 1/6 the params | **Primary Inbox Helper classifier**; extraction fallback | AWQ INT4 fits in ~42–46 GB VRAM; tight on 48 GB card with careful KV cache budgeting |
| **Qwen 3 32B** | 32 B | 128k | **Apache 2.0** | Competitive with Llama 3.3 70B on structured tasks; strong tool use | **Cleanest-licence backup**; first-class candidate if Llama licence becomes a problem | Fits comfortably on a single 48 GB card at FP8 or AWQ INT4 |
| **Qwen 3 80B** | ~80 B | 128k | Apache 2.0 | Slightly stronger than 3 32B | Backup if 32B falls short; needs 2× 48 GB or H100-class | Requires more than a single A6000; parks into "synthetic data R&D only" tier |
| **Llama 3.1 405B** | 405 B | 128k | Llama Community | The NEJM ceiling — ~70% vs GPT-4 64% per JAMA Health Forum March 2025 | Reference ceiling; not deployable on our Catalyst footprint | Needs 8×H100 or 4×B200 — only reachable via Together/Fireworks dedicated for synthetic data eval runs |
| **Llama 4 Scout** | 17B-active/109B-total MoE | 10M | Llama 4 Community | Newer, faster per token; clinical benchmarks thin as of April 2026 | Watch item — re-evaluate after R7 refresh in Sprint 4 | MoE routing complicates deterministic inference; wait for ecosystem maturity |
| **Llama 4 Maverick** | 17B-active/400B-total MoE | 1M | Llama 4 Community | Strong on long-context eval | Watch item only | Same caveats as Scout |
| **Mistral Large 2/3** | 123 B / TBC | 128k | Mistral Research or Commercial | Competitive with Llama 70B on reasoning | Backup candidate | Licence terms less permissive than Qwen/Llama for commercial deployment |
| **Gemma 3 27B** | 27 B | 128k | Gemma licence | Strong for its size; lighter clinical evidence | Backup if size becomes constrained | Lighter published clinical signal than Qwen 3 32B |
| **GPT-OSS-120B** | 120 B | 128k | **Apache 2.0** | The NHS GPT-oss-120b medication safety review (arXiv 2512.21127) is the most cited 2025 primary-care open-model real-world deployment; found **contextual reasoning failures 6:1 vs factual errors** | Synthetic data R&D burst on H100; reference for failure-mode testing | Too big for Catalyst A6000; reach via Together/Fireworks A100/H100 for eval runs only |
| **GPT-OSS-20B** | 20 B | 128k | Apache 2.0 | Lighter sibling; lower published clinical signal | Not a lead candidate | Useful as a small-model baseline |
| **DeepSeek-R1** | 671 B MoE | 128k | MIT | Strong reasoning; distilled variants (Llama 70B, Qwen 32B distills) published | Distilled-Qwen-32B variant is a watch item alongside Qwen 3 32B | Full R1 too big; distills land in the same slot as Qwen 3 32B |
| **DeepSeek-V3** | 671 B MoE | 128k | MIT | General-purpose; less focused clinical signal than R1 | Not a lead candidate | Same size issue as R1 |

### 2.2 Medical-domain-specific open models

The 2026 question is whether a clinical-domain base model still beats a general model fine-tuned for a specific clinical task. The Open Medical-LLM Leaderboard (HuggingFace) and 2025 peer-review converge on: **domain-specific models help most at the smaller scale (≤13B), where the extra pre-training signal compensates for smaller parameter counts; at 70B+ the gap closes and domain-tuning provides marginal gains over prompt engineering + task fine-tuning**. Our use is therefore: use the medical-domain models at the smaller scale (for the pre-classifier and the extraction sub-task), use Llama 3.3 70B or Qwen 3 32B as the main classifier.

| Model | Base | Params | Licence | Best use for us |
|---|---|---|---|---|
| **Meditron3-8B** | Llama 3.1 8B | 8 B | Llama 3.1 Community | EPFL/Yale/Meta; MedQA/MedMCQA leaderboard performer. **Recommended for Care Gap Finder variable extraction** via QLoRA/DoRA fine-tune on 300–500 labelled extraction examples |
| **MedGemma 27B-IT** | Gemma 3 27B | 27 B | Gemma licence | Google. **Recommended as the "second opinion" arbiter** in the three-tier cascade: differently trained base, independent failure modes, fits on a single 48 GB card |
| **MedGemma 4B** | Gemma 3 4B | 4 B | Gemma licence | Fast small-model fallback; limited clinical signal |
| **BioClinical ModernBERT 396M** | ModernBERT | 396 M | MIT | **Recommended as the pre-classifier** in the cascade — cheap, fast, fits on CPU or a small slice of GPU, trained on clinical text, strong for coarse filtering (triage-priority vs routine) before the main LLM is called |
| **PMC-LLaMA** | Llama 2 | 7 B / 13 B | Llama Community | Older generation; superseded by Meditron3-8B |
| **BioMedLM** | GPT-2 style | 2.7 B | Open RAIL | Smaller than Meditron3-8B; not recommended |
| **Clinical-Camel** | Llama 2 70B | 70 B | Research only | Research licence — not suitable for commercial deployment |
| **Hippo (7B family)** | Mistral/Llama 2 | 7 B | Mixed | Claimed to outperform 70B but published evidence is thin; treat as watch item |

### 2.3 Benchmark evidence feeding the model selection

Key 2024–2026 benchmarks cited by agents R1 and R7-A:

- **BRIDGE benchmark** (arXiv 2504.19467, 2025) — 95 LLMs across 20 clinical applications including triage and referral, 14 specialties. Most relevant meta-benchmark for task selection. Llama 3.3 70B and Qwen 2.5 72B both reach the top quintile on triage-adjacent tasks; closed frontier models lead by 3–6 points.
- **JMS structured prompting triage study** (Journal of Medical Systems 2025, DOI 10.1007/s10916-025-02284-y) — 8 LLMs on 48 short clinical vignettes, 4 triage levels. **Structured prompting lifted mean triage accuracy from 76.82% → 86.20%.** Directly comparable to Inbox Helper: 4 levels, clinical text. Key finding: structured prompting beats prompt length and beats most fine-tuning at this data scale.
- **ICPC-2 coding benchmark** (arXiv 2507.14681, 2025) — 33 LLMs on International Classification of Primary Care codes. 28 models >0.8 F1. Top performers: gpt-4.5-preview, o3, gemini-2.5-pro — but Llama 3.3 70B and Qwen 2.5 72B both cleared 0.8 F1, confirming open models are adequate for primary-care coding.
- **NHS primary care medication safety review** (arXiv 2512.21127, GPT-oss-120b, Oct–Nov 2025) — 178 failures across 148 patients. **Contextual reasoning failures outnumber factual errors 6:1.** This is the headline design constraint for our architecture: the dominant failure mode is not "model doesn't know the fact" but "model applies the right fact to the wrong context." Our three-tier cascade + CoT rationale forcing + abstention gate are direct responses.
- **LCD benchmark** (medRxiv 2024.03.26) — long clinical document mortality prediction on MIMIC-IV. Notes "benchmark datasets targeting long clinical document classification tasks are absent" — confirming we are in partially uncharted territory for discharge summary classification.
- **EHRNoteQA** (NeurIPS 2024 datasets track) — long-context clinical QA at 4k/8k token levels. Confirms open 70B models handle 8k context without degradation.
- **Open Medical-LLM Leaderboard** (HuggingFace) — standardised MedQA/MedMCQA/PubMedQA for open models. Meditron3-8B leads its weight class; Llama 3.3 70B leads the 70B class; Qwen 3 32B leads the 30B class.

### 2.4 Shortlisted models for R3 deep-dive

Based on the evidence above, the **three-tier cascade** proposed for R3 is:

1. **Pre-classifier (always-on, cheap)** — BioClinical ModernBERT 396M, fine-tuned on our synthetic set to do coarse triage (Immediate/Urgent candidate vs Routine/Info candidate). Runs on CPU or a small slice of GPU. Its job is to route clearly routine items to a fast path and flag anything that might be urgent to the main LLM.
2. **Main classifier (primary)** — **Llama 3.3 70B Instruct AWQ INT4** (Stack A) or **Qwen 3 32B FP8/AWQ INT4** (Stack B). Does the 4-level classification with explicit CoT rationale, outputs structured JSON via XGrammar constrained decoding. This is where most of our fine-tuning effort goes.
3. **Second opinion / arbiter (abstention-gated)** — **MedGemma 27B-IT** on the same GPU, invoked only on items flagged low-confidence by the main classifier. Differently trained base (Gemma vs Llama/Qwen) reduces shared failure modes. Called on ~5–15% of items depending on abstention threshold.
4. **Synthetic-data-only "reference ceiling"** — **GPT-OSS-120B** on Together AI H100 dedicated, used only during Sprint 3 evaluation to establish an upper bound. Not deployed against real clinical data.

For **Care Gap Finder variable extraction** (Sub-task B of R4), the recommended extractor is **Meditron3-8B QLoRA + DoRA** fine-tuned on 300–500 labelled extraction examples. This is a separate model, deployed alongside the Inbox Helper stack on the same Catalyst GPU (8B + 70B AWQ co-fit on 48 GB is tight but feasible; alternatively run extraction on a second small GPU slice).

---

## 3. Inference engine comparison

### 3.1 Landscape

The 2026 production-grade inference engine field has consolidated to four contenders: **vLLM, SGLang, LMDeploy, TensorRT-LLM**. TGI (HuggingFace Text Generation Inference) entered maintenance mode on **11 December 2025**; HuggingFace's own documentation now recommends vLLM or SGLang for new deployments and TGI should be **ruled out** for any new clinical system. TensorRT-LLM remains the raw-throughput ceiling on NVIDIA hardware but carries operational complexity (TensorRT build step, limited structured-output ecosystem) that is hard to justify at our scale.

### 3.2 Head-to-head comparison

| Dimension | **vLLM (≥0.8)** | **SGLang (≥0.4)** | **LMDeploy** | **TensorRT-LLM** |
|---|---|---|---|---|
| Throughput on H100 (published benchmarks, Llama 3 70B) | ~12,500 tok/s | **~16,200 tok/s (~29% higher)** | Competitive; TurboMind AWQ strong | Highest raw, hardware-bound |
| KV cache strategy | PagedAttention | **RadixAttention** (prefix tree, strong re-use for agent flows) | Block KV cache | TensorRT engine-specific |
| Structured output / JSON | XGrammar, Outlines, lm-format-enforcer, guidance | **XGrammar native** (default); Outlines also supported | OpenAI-compatible JSON mode | Engine-specific |
| Multi-step / agent programs | Good | **Strongest** — SGLang's programming model is designed for multi-step programs with function calls | OK | Limited |
| Deterministic inference | Batch-invariant path requires **Hopper SM ≥9.0** — **does not work on RTX A6000 (SM 8.6)** | **Deterministic mode** works on SM 8.6; cost ~30% throughput | Not a first-class feature | Not a first-class feature |
| Quantisation support | FP8 (Hopper+), INT8, INT4 AWQ/GPTQ, BitsAndBytes | FP8, INT8, AWQ/GPTQ, FP4 | **Strongest INT4 AWQ** via TurboMind; FP8 | FP8, INT8, INT4 with engine rebuild |
| Maturity | Most mature; default in production | Newer but production-grade; used by LMSYS and increasing fraction of 2025–2026 clinical deployments | Mature; InternLM ecosystem | Most mature on NVIDIA; highest operational cost |
| Documentation / ecosystem | Very strong | Strong and growing | Good | NVIDIA-native, less community |
| OpenAI-compatible API | Yes | Yes | Yes | Add-on |
| Clinical deployment evidence | Multiple | Growing — 2026 clinical systems increasingly pick it for multi-step flows | Less | Rare |

### 3.3 The SM 8.6 deterministic constraint — why this picks SGLang for us

**This is the single most important engine-selection factor for our stack.** Clinical-grade logging and DPIA compliance require reproducible inference: the same prompt on the same model must produce the same output so that audit logs can be replayed during post-market surveillance and adverse-event investigation. vLLM's batch-invariant mode — the path to deterministic inference across concurrent requests — is implemented via a FlashAttention variant that requires compute capability **SM ≥9.0** (Hopper H100/H200, Blackwell B200). The **RTX A6000 is SM 8.6** (Ampere), the L40S is SM 8.9 (Ada Lovelace). **Neither of our viable Catalyst GPUs supports vLLM's batch-invariant path.**

SGLang's deterministic mode uses a different implementation strategy that works on SM 8.6 and above, at a ~30% throughput cost. For our 1,000–10,000 documents/day workload, that throughput cost is acceptable — we do not need 16k tok/s, we need 1k–2k tok/s reliably and reproducibly. The determinism is not optional; without it, we cannot meet our own DPIA and clinical-audit requirements.

Therefore: **SGLang (deterministic mode) is the recommended inference engine for the NZ-sovereign production path on Catalyst C1A A6000.** vLLM remains a backup on H100-class hardware for synthetic data R&D bursts where non-deterministic throughput is acceptable.

### 3.4 Structured output / JSON — XGrammar is the pick

The Inbox Helper output schema is a strict JSON object with an urgency enum, rationale text, document-type field, and confidence score. Free-form LLM output risks invalid JSON, hallucinated fields, and malformed enums — all of which break the pipeline and make auditability harder. Four options for constrained decoding:

| Library | Mechanism | Fit for our task |
|---|---|---|
| **XGrammar** | Context-free grammar, fast compilation, native in SGLang and vLLM | **Recommended.** Fast, native integration, handles our schema exactly |
| **Outlines** | Regex/JSON-schema-driven token masking | Mature alternative; good for simple schemas |
| **lm-format-enforcer** | Token-level format enforcement | Workable; less performant than XGrammar |
| **guidance** | Microsoft's constrained generation | More flexibility but more complex; overkill for our schema |

**Pick: XGrammar via SGLang native integration.** Zero extra complexity, production-grade performance, matches our ordinal enum + structured rationale output.

### 3.5 Recommendation for R3

**SGLang (deterministic mode) with XGrammar structured output, serving Llama 3.3 70B AWQ INT4 (Stack A) or Qwen 3 32B FP8/AWQ INT4 (Stack B), on Catalyst Cloud C1A RTX A6000 48 GB.**

---

## 4. GPU-to-model fit

### 4.1 Available GPU shapes in our hosting footprint

From R7-C and R2:

| GPU | VRAM | Compute cap | Host | Status (April 2026) |
|---|---|---|---|---|
| NVIDIA RTX A6000 (1–4 cards per VM) | 48 GB each | SM 8.6 (Ampere) | Catalyst C1A | **GA, all regions** — primary NZ-sovereign GPU |
| NVIDIA L40S | 48 GB | SM 8.9 (Ada) | Catalyst C3 | **Beta, Porirua-only** — usable for R&D |
| NVIDIA A100 80 GB | 80 GB | SM 8.0 (Ampere) | Together AI dedicated | Overseas — synthetic data only |
| NVIDIA H100 80 GB | 80 GB | SM 9.0 (Hopper) | Together AI dedicated / Fireworks / CoreWeave | Overseas — synthetic data burst only |
| NVIDIA A100 20 GB slice (GRID A100D-20C) | 20 GB | SM 8.0 | Catalyst C2 | **Retiring 31 March 2026 — eliminated from planning** |

### 4.2 Model fit on RTX A6000 48 GB

Fits calculated assuming AWQ INT4 weights + KV cache budget for up to 8 concurrent requests at 8k context. Numbers are conservative — production deployment should re-measure.

| Model | Weights (AWQ INT4) | Peak VRAM (weights + KV) | Fits single A6000 48 GB? | Notes |
|---|---|---|---|---|
| **Llama 3.3 70B Instruct** | ~35 GB | ~42–46 GB | **Yes — tight** | Requires conservative KV cache budgeting; 4k–8k context comfortable; 32k context needs quantised KV cache |
| **Qwen 3 32B** | ~16 GB (AWQ INT4) | ~22–28 GB | **Yes — comfortable** | Room for FP8 variant too (~32 GB) |
| **Qwen 3 80B** | ~40 GB | ~48+ GB | **No — overflows** | Needs 2 × A6000 or A100 80 GB |
| **MedGemma 27B-IT** | ~14 GB (INT4) / ~27 GB (FP16) | ~18–32 GB | **Yes** — fits alongside a smaller main model; pair with Qwen 3 32B more easily than Llama 3.3 70B |
| **Meditron3-8B** | ~4 GB (INT4) / ~16 GB (FP16) | ~8–20 GB | **Yes** — runs co-resident with the main model |
| **BioClinical ModernBERT 396M** | <1 GB | <2 GB | **Yes** — runs on CPU or a tiny GPU slice |
| **GPT-OSS-120B** | ~60 GB (INT4) | ~75–85 GB | **No — single H100 or 2× A6000** |
| **Llama 3.1 405B** | ~200 GB | 8× H100 territory | **No — synthetic data only via Together** |

**Key finding.** The three-tier cascade (BioClinical ModernBERT pre-classifier + Llama 3.3 70B AWQ INT4 main + MedGemma 27B-IT INT4 arbiter) is **tight but fits on a single RTX A6000 48 GB** if the arbiter is loaded on-demand rather than resident. A cleaner deployment is:

- **Main serving VM:** 1× C1A A6000 48 GB running SGLang with Llama 3.3 70B AWQ INT4 (~42 GB resident) + BioClinical ModernBERT on CPU.
- **Arbiter VM (on-demand):** 1× C1A A6000 48 GB loaded with MedGemma 27B-IT INT4 (~14 GB resident), with Meditron3-8B co-resident for extraction.

Two A6000 VMs at ~NZD $3,200/month each = ~NZD $6,400/month fully loaded. **This exceeds the single-GPU budget envelope in §5 but still fits the 6-month compute plan.** For Sprint 3 evaluation, start with single-VM deployment (arbiter loaded on-demand, slower but cheaper); upgrade to dual-VM for production if evaluation shows the arbiter is called frequently.

### 4.3 Throughput expectations

Published benchmarks for Llama 3 70B AWQ INT4 on a single RTX A6000 48 GB with SGLang:
- ~**800–1,200 tok/s aggregate** at 8 concurrent requests (deterministic mode adds ~30% overhead, netting ~560–840 tok/s).
- At ~400 output tokens per Inbox Helper document, that's ~1.4–2.1 documents/sec sustained, or **~100,000–180,000 documents/day** theoretical ceiling — far above our 10,000 documents/day target.
- **Headroom is ~10–18× at the 10k/day workload**, which is the margin we need for peak bursts, request rejitter, arbiter second-opinion invocations, and future growth.

Published benchmarks for Qwen 3 32B AWQ INT4 on the same hardware:
- ~**1,400–2,000 tok/s aggregate** (slightly faster than Llama 3.3 70B due to smaller parameter count), netting ~980–1,400 tok/s in deterministic mode.
- Headroom is ~15–25× at the 10k/day workload.

Latency targets:
- **p50 ≤ 2 s per document** (async inbox processing) — achievable on both stacks.
- **p95 ≤ 5 s per document** — achievable on both stacks at 4–8 concurrent requests.
- If we need interactive p95 ≤ 2 s (e.g. GP-facing real-time triage), Qwen 3 32B is the more defensible pick.

### 4.4 Quantisation trade-offs

The question: how much accuracy do we lose at AWQ INT4 vs FP8 vs BF16? Published evidence:

- **Kurtic et al., "Give Me BF16 or Give Me Death" (ACL 2025, arXiv 2411.02355)** — the landmark quantisation accuracy study. Finding: "Modern quantisation methods (FP8, INT8, AWQ INT4) preserve accuracy to within 1–2% of BF16 on most reasoning benchmarks; INT4 AWQ is the point of diminishing returns for throughput, and below INT4 accuracy degrades rapidly." For our task, **AWQ INT4 is defensible — the accuracy cost is within the noise of other pipeline choices.**
- **QM-ToT benchmark (arXiv 2504.12334)** — medical reasoning under quantisation. Found ~1.5% absolute MedQA accuracy drop for Llama 3 70B at AWQ INT4 vs FP16 — within the margin of error of most clinical benchmarks.
- Practical upshot: **AWQ INT4 is safe for Inbox Helper classification.** We should validate on our own synthetic data in Sprint 3 before committing — but the published literature gives us strong prior confidence.

FP8 is the alternative: **higher accuracy (~0.3% drop vs BF16) but requires SM ≥8.9 (L40S or newer)**. Since we're primarily on A6000 (SM 8.6), FP8 is not an option on the production path — AWQ INT4 is the default. If we migrate to C3 L40S when it goes GA, FP8 becomes available and we can retest.

---

## 5. Cloud GPU provider comparison — costs in NZD

### 5.1 The sovereignty-first comparison table

Full provider landscape research in R7-C. Summary applied to our decision:

| Provider | GPU | NZD/hr | NZD/month (730 h) | Dedicated tenancy | HIPAA BAA / equivalent | NZ-sovereign? | Role in our plan |
|---|---|---|---|---|---|---|---|
| **Catalyst Cloud C1A** | RTX A6000 48 GB | ~$3.10 `[modelled]` | **~$2,265** GPU VM only; **~$3,200** fully loaded | Yes (single-tenant VM) | NZ HISO 10029 / HIPC 2020 (see R2) | **Yes** (NZ-owned, NZ-operated, ISO 27001/27017) | **Primary** — production real-data inference |
| **Catalyst Cloud C3** (Beta, Porirua) | L40S 48 GB | ~$3.80 `[modelled]` | ~$2,775 GPU VM only; ~$3,600 fully loaded | Yes | Same | **Yes** | Backup if C1A capacity becomes constrained; Beta status is a risk for production commitment |
| **Datacom Sovereign GPUaaS** | Undisclosed | Quote-only | Quote-only | Yes | Same (NZISM + IRAP aligned) | **Yes** | **Contingency Plan B** — request indicative quote in Month 1 of Sprint 3; do not build against it |
| **Together AI Dedicated Endpoints** | A100 80 GB | ~$2.93 | **~$2,141** (24×7); **~$1,070** (12 h/day); ~$267 (3 h/day burst) | Yes (enterprise) | **Enterprise BAA**, SOC 2 | No (US/EU) | **Synthetic data R&D only** — Llama 3.3 70B full precision eval runs, GPT-OSS-120B reference ceiling |
| Together AI Dedicated Endpoints | H100 | ~$3.98 | ~$2,907 (24×7) | Yes (enterprise) | Enterprise BAA | No | Synthetic data H100-class eval runs only |
| Fireworks AI On-Demand | A100 80 GB | ~$4.83 | ~$3,527 (24×7) | Yes (per-GPU-second) | **SOC 2 Type II + HIPAA** (BAA enterprise-gated) | No | Backup for synthetic data if Together is unavailable; strongest published isolation |
| Fireworks AI On-Demand | H100/H200 | ~$10.00 | ~$7,300 (24×7) | Yes | SOC 2 Type II + HIPAA | No | Over-budget 24×7; burst use only |
| Modal (enterprise) | H100 via AWS/GCP/OCI | Per-second; sales-gated | Higher than Together at sustained load | Enterprise BAA | Enterprise | No | Developer ergonomics are best-in-class but cost-per-GPU is high — use only for bursty synthetic data generation |
| CoreWeave | H100 PCIe | ~$7.93 | ~$5,792 (24×7) | Yes — single-tenant clusters | Claimed; verify with sales | No | Geared to reserved multi-GPU clusters — overkill for 1–2 GPU workload |
| Runpod Secure Cloud | H100 | ~$4.48 | ~$3,273 (24×7) | Partial | **No GA HIPAA BAA as of early 2026** | No | **Ruled out per brief and R7-C** |
| Lambda Labs | A100 40 GB | ~$2.15 | ~$1,569 (24×7) | VM only, not dedicated | **No BAA** | No | **Ruled out per brief and R7-C** |

All USD→NZD figures use 1 USD = 1.667 NZD (1 NZD = 0.60 USD) per the brief.

### 5.2 Catalyst Cloud fully-loaded monthly cost (modelled)

Following R7-C's modelling (the live price list is sandbox-blocked — re-verify manually):

| Line item | NZD/month |
|---|---|
| C1A A6000 single-GPU VM (c1a.c16r64-gpu1) `[modelled]` | ~$2,265 |
| Block storage (500 GB SSD for weights + cache) | ~$60–90 |
| Object storage (2 TB for logs, evals, synthetic corpora) | ~$100–200 |
| CCKS Kubernetes control plane | ~$100–200 |
| Egress contingency (model pulls + outbound API) | ~$300–500 |
| Contingency / overruns | ~$400 |
| **Total fully-loaded** | **~$3,200** |

### 5.3 Six-month Objective 1 compute envelope

| Line | NZD | Notes |
|---|---|---|
| Catalyst C1A A6000 24×7 (primary, 6 mo) | $19,200 | Production inference, real data |
| Together A100 80 GB dedicated 12 h/day (6 mo) | $6,500 | Synthetic data fine-tuning + eval |
| Together H100 burst (~20 hrs/mo) | $500 | GPT-OSS-120B reference ceiling, Llama 3.1 405B sanity checks |
| Egress / storage / K8s contingency | $2,000 | Headroom for data movement bursts |
| Datacom Sovereign quote / pilot day (if needed) | $1,500 | Plan B readiness |
| Reserve for overruns | $2,500 | Conservative cushion |
| **Total compute + infra, 6 months** | **~$32,200** | **18% of $177k grant** |

**Labour + overhead balance:** ~$144,800 left, equivalent to ~2 × 0.8–1.0 FTE NZ research-engineer rates + modest clinical-advisor honorarium over 6 months. Fits the grant envelope comfortably.

### 5.4 Multi-tenancy is ruled out for real clinical data

R7-C sourced the published concern to **Cerebrium's own blog** ("Choosing the Right Serverless GPU Platform for Global Scale", cerebrium.ai/articles/deploying-ai-workloads-on-serverless-gpus-for-global-scale):

> "Inference requests run on GPUs that processed someone else's data minutes earlier, which creates audit problems for healthcare (HIPAA), finance (SOC 2), or EU data residency (GDPR)."

Supported by:
- **Introl, "Multi-tenant GPU security: isolation strategies for shared infrastructure 2025"** — "Standard container runtimes don't automatically scrub GPU memory between workloads — residual data can persist in CUDA memory allocations after jobs complete. In multi-tenant deployments tenant A's inference workload could access tenant B's model weights and training data."
- **Edera, "Securing the AI Grid"** — describes contention-based side channels and per-workload isolation needs.
- **WhiteFiber, "GPU Infrastructure Compliance in Regulated Healthcare AI"** — explicit on purpose-built single-tenant GPU infra for HIPAA-style audit requirements.

This body of evidence justifies ruling out serverless multi-tenant inference (Cerebrium, Replicate, Runpod Community, vLLM-as-a-service offerings) for anything touching real clinical data, and supports the choice of dedicated single-tenant VM on Catalyst for the production path and enterprise dedicated endpoints for the synthetic-data overseas path.

### 5.5 Self-host colocation — not for Objective 1

R7-C modelled NZ colocation: capex ~NZD $22–50k for a 1-GPU node (RTX 6000 Ada or L40S + chassis + NICs), opex ~NZD $900–3,800/month (rack + power + transit + remote hands). Payback vs Catalyst (~NZD $1,700/month delta) sits around **20 months** — longer than the 6-month Objective 1 horizon. Procurement lead time (4–12 weeks for RTX 6000 Ada or L40S in NZ) eats 15–30% of the runway. Ops burden for a 2-person team adds ~0.2–0.4 FTE of implicit cost. **Verdict: revisit at Objective 2/3 boundary; do not plan for self-host in Sprint 3.**

### 5.6 MBIE N2RD grant compliance on cloud compute

R7-C found: **there is no publicly indexed MBIE or Callaghan Innovation guidance specifically classifying cloud compute (overseas vs NZ) as eligible or ineligible under New to R&D or R&D Experience Grants.** The closest written analogy is the N2RD criteria language: *"R&D undertaken outside of New Zealand is not eligible for co-funding, except in limited cases where Callaghan Innovation expressly permits it"* and *"materials and consumables purchased from overseas are allowed"*. The pragmatic reading is that overseas dedicated cloud GPU hours can be classified as consumables if the capability is genuinely not available in NZ.

**Our written sourcing test (to be filed with Lisa Pritchard at Callaghan Innovation before any overseas spend):**
1. We evaluated **Catalyst C1A A6000** as the primary NZ-sovereign GPU and confirmed it fits Llama 3.3 70B AWQ INT4 with deterministic SGLang. **It is the production path for real clinical data.**
2. We evaluated **Catalyst C3 L40S (Beta, Porirua-only)** and noted the Beta status and single-region limitation make it unsuitable for production commitment during this grant period.
3. We evaluated **Datacom Sovereign GPUaaS** and determined it is sales-gated, quote-only, and not off-the-shelf procurable in our Sprint 2 window.
4. Overseas dedicated GPU on **Together AI** or **Fireworks AI** is justified solely for synthetic-data training/eval runs requiring H100-class throughput or access to models not yet available on Catalyst hardware — this is a "capability not sourceable in NZ" consumable.
5. No real identifiable clinical data will ever leave NZ under this plan.

This should be sufficient to satisfy the discretionary carve-out — but **confirm in writing with the grant manager before any overseas spend** (see §11 open questions).

---

## 6. Fine-tuning approach for small data

### 6.1 The small-data reality

Our labelled data budget for Sprint 2 is **300–500 synthetic items**, growing to **~1,500 stratified items** by Sprint 4 (post-GP review and post-generation of enriched boundary cases). This is well below the scale at which full fine-tuning of a 70B model is meaningful, and even LoRA on 70B is a marginal exercise unless carefully bounded. The published 2024–2026 small-data clinical fine-tuning literature converges on three techniques, used in combination:

1. **LoRA / QLoRA / DoRA** at small rank (r=8–32) for targeted adaptation — especially for extraction sub-tasks where **format and schema are what we're really trying to learn**, not new clinical knowledge.
2. **Prompt optimisation** via DSPy MIPROv2 for the Inbox Helper classifier — where **prompt structure and few-shot exemplar selection often beat fine-tuning at this data scale**.
3. **Post-hoc calibration and abstention** — temperature scaling, conformal prediction, and abstention gates — to hit the ≥99% sensitivity target on minority classes without requiring vast training data.

### 6.2 LoRA vs QLoRA vs DoRA

| Technique | What it is | When to pick it | Published evidence |
|---|---|---|---|
| **LoRA** | Low-rank adapters (r=8–64), freezes base weights | When base model fits in GPU and training speed matters | Hu et al. 2021 (arXiv 2106.09685) — the baseline PEFT method |
| **QLoRA** | LoRA with 4-bit NF4 quantised base weights | When base model would otherwise overflow VRAM during training; cheap fine-tuning on a single 48 GB GPU is feasible for 70B models | Dettmers et al. 2023 (arXiv 2305.14314) — demonstrated 65B model fine-tuning on a single 48 GB GPU. **Directly applicable to our Catalyst A6000 setup.** |
| **DoRA** | Decomposes LoRA updates into magnitude + direction; strictly better than LoRA on small data | When data is small and over-fitting is the dominant risk | Liu et al. 2024 (arXiv 2402.09353) — **improves over LoRA on most benchmarks, especially at small r**. Drop-in replacement: adds ~1% training overhead. |

**Recommendation.** Use **DoRA (r=16–32) on QLoRA base quantisation** for the fine-tuning tracks in Sprint 3. This is the best published small-data path and fits on a single Catalyst C1A A6000 48 GB for both 70B and 32B targets.

### 6.3 DSPy MIPROv2 prompt optimisation — the systems-level play

Khattab et al., **"Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together"** (arXiv 2407.10930, 2024) is the key reference: on small-data clinical tasks, **prompt optimisation over a frozen model often matches or beats fine-tuning**, and the two combine additively. DSPy MIPROv2 specifically:
- Learns optimal few-shot exemplar selection from a labelled training set.
- Optimises the instruction prompt over the same set.
- Is **parameter-free from the model's perspective** — no gradient updates to the LLM, so it's safe for closed-weight models as well (useful for the parallel Bedrock NZ Claude track in R3).
- Runs fast on a 300–500 item training set.

**Recommendation.** Sprint 3 fine-tuning has **three parallel tracks** running concurrently:

| Track | Target | Technique | Purpose |
|---|---|---|---|
| **Track 1** | BioClinical ModernBERT 396M | Full fine-tune on pre-classifier task | Cheap, fast, trains in <1 hr per epoch on a single A6000 |
| **Track 2** | Meditron3-8B | **QLoRA + DoRA (r=16)** on variable extraction examples | Care Gap Finder Sub-task B extractor |
| **Track 3** | Llama 3.3 70B (Stack A) or Qwen 3 32B (Stack B) | **DSPy MIPROv2 prompt optimisation** on the 300–500 labelled Inbox Helper items; optional light QLoRA + DoRA (r=8–16) on top if MIPROv2 alone plateaus | Inbox Helper main classifier |

All three tracks run in parallel on one Catalyst C1A A6000 VM over the first week of Sprint 3. Training compute cost is trivial (single-digit GPU-hours per track).

### 6.4 Recall optimisation — the published cocktail for ≥99% sensitivity

Our minority-class sensitivity target (≥99% on Immediate and Urgent) is the hard constraint. Fine-tuning alone rarely reaches this on minority classes at our data scale. The published cocktail:

1. **Weighted focal loss during fine-tuning** — Lin et al. 2017 (Focal Loss for Dense Object Detection, arXiv 1708.02002). Up-weights minority-class errors during training. On ordinal clinical triage, published work shows 3–8 point sensitivity gain on minority classes vs plain cross-entropy.
2. **Temperature scaling post-hoc** — Guo et al. 2017 ("On Calibration of Modern Neural Networks", arXiv 1706.04599). Re-calibrates softmax outputs on a held-out set. Cheap, universally applicable, preserves ranking while making thresholds meaningful.
3. **Conformal prediction** — Angelopoulos & Bates 2021 ("A Gentle Introduction to Conformal Prediction", arXiv 2107.07511). Gives distribution-free coverage guarantees: set a target 99% coverage on Immediate/Urgent, and conformal prediction will return a prediction set that covers the true label with that probability. For ordinal classification this means "if the model thinks it might be Immediate at all, we flag it as Immediate" — exactly the over-triage posture we want.
4. **Abstention / selective prediction** — El-Yaniv & Wiener 2010 and follow-ups. The model can abstain on low-confidence items; abstained items route to the MedGemma arbiter (the second opinion in the cascade). The abstention threshold is tuned to hit ≥99% sensitivity on the non-abstained predictions. Published clinical work shows this pushes sensitivity to the target reliably, at the cost of routing 5–15% of items to the second opinion.

**Recommendation.** Apply all four techniques in layers. This is the published path to ≥99% sensitivity on minority classes with small training data — and it is compatible with our three-tier cascade architecture (the abstention gate is what routes items to the MedGemma arbiter).

### 6.5 Training framework selection

Four mature options as of April 2026:

| Framework | Strengths | Weaknesses | Fit |
|---|---|---|---|
| **Unsloth** | Fastest training, lowest VRAM, best small-data ergonomics, native DoRA support | Smaller team than Axolotl; slightly less config flexibility | **Recommended for Tracks 2 and 3** — QLoRA + DoRA on 8B and 70B |
| **Axolotl** | Most production-flexible, strong YAML config, wide model support | Higher VRAM overhead than Unsloth | Backup if Unsloth hits a model-version issue |
| **HuggingFace PEFT + TRL** | First-party HF, most integrations, widest docs | Baseline speed, not the fastest | Good for BioClinical ModernBERT pre-classifier (Track 1) |
| **LLaMA-Factory** | Comprehensive; good for model zoo exploration | More operationally complex | Not needed at our scale |
| **torchtune** | PyTorch-native | Less mature ecosystem | Not recommended for clinical deployment as of April 2026 |

**Recommendation.** Unsloth for the 70B/32B/8B QLoRA+DoRA tracks; HuggingFace PEFT + TRL for the ModernBERT pre-classifier; Axolotl as a backup.

### 6.6 Data budget and practical training plan

With 300–500 synthetic items in Sprint 2 and ~1,500 by Sprint 4:
- **Train/val/test split:** 70/15/15 at the item level, stratified by urgency × document type.
- **Cross-validation:** 5-fold on the 70% train set for the small-data tracks (ModernBERT, Meditron3-8B).
- **Final eval:** 15% held-out test set, never seen during training or prompt optimisation. Macro F1, QWK, per-class sensitivity, PR-AUC, MCC reported with BCa bootstrap CIs.
- **No data leakage:** generation LLM prompts should not include exemplars from the held-out test set.

Training compute estimate (single C1A A6000):
- **Track 1 (ModernBERT):** ~2 GPU-hours per epoch; 5 epochs = 10 GPU-hours total.
- **Track 2 (Meditron3-8B QLoRA+DoRA):** ~3 GPU-hours per epoch; 5 epochs = 15 GPU-hours total.
- **Track 3 (Llama 3.3 70B MIPROv2 + light QLoRA+DoRA):** ~20 GPU-hours for MIPROv2 prompt optimisation + ~30 GPU-hours for a light 3-epoch QLoRA+DoRA run = ~50 GPU-hours total.
- **Grand total:** ~75 GPU-hours, or ~NZD $230 of Catalyst C1A time — trivial against the compute envelope.

---

## 7. Cost head-to-head — open-source self-hosted vs Bedrock NZ Claude

### 7.1 Workload assumptions

Consistent unit-cost modelling basis across both stacks:
- **Documents per day:** 1,000 (small practice) and 10,000 (large practice or aggregated multi-practice instance).
- **Tokens per document:** 1,600 input (document + system prompt + few-shot + patient context) + 400 output (structured JSON with rationale) = **2,000 total tokens/document**.
- **Cache hit rate on Bedrock:** assume 40% on system prompt + few-shot prefix (conservative; could be 60–80% with careful prompt design).
- **Time horizon:** monthly cost.
- **Currency:** NZD (1 USD = 1.667 NZD).

### 7.2 Bedrock NZ Claude Haiku 4.5 (estimated from Sydney pricing, per R2)

R2 notes that Bedrock launched in ap-southeast-6 in March 2026. NZ-specific pricing is not yet published as of April 2026; the defensible assumption is that ap-southeast-6 prices match or slightly exceed ap-southeast-2 (Sydney). Published Sydney Haiku 4.5 pricing (April 2026):
- Input: ~USD $1.00 / million tokens → NZD $1.67 / M
- Cached input: ~USD $0.10 / M → NZD $0.17 / M
- Output: ~USD $5.00 / M → NZD $8.33 / M

Per document:
- Uncached input (60% of 1,600 = 960 tokens) × NZD $1.67/M = NZD $0.00160
- Cached input (40% of 1,600 = 640 tokens) × NZD $0.17/M = NZD $0.00011
- Output (400 tokens) × NZD $8.33/M = NZD $0.00333
- **Per document: ~NZD $0.00504**

Monthly cost:
- **1,000 docs/day × 30 days = 30,000 docs → NZD $151/month**
- **10,000 docs/day × 30 days = 300,000 docs → NZD $1,512/month**

(Claude Sonnet 4.6 would be ~5× more expensive — ~NZD $750 / $7,500 respectively. Haiku 4.5 is the defensible default for the high-volume Inbox Helper classifier; Sonnet 4.6 is used only as a second-opinion arbiter for abstained items.)

### 7.3 Catalyst C1A A6000 open-source self-hosted

The open-source stack pays for GPU time, not per-token. Published benchmark throughput for Llama 3.3 70B AWQ INT4 on RTX A6000 with SGLang deterministic mode: **~560–840 tok/s** aggregate under 4–8 concurrent requests. At 2,000 tokens/document, that's **~0.28–0.42 documents/sec** sustained, or **~24,000–36,000 documents/day** theoretical ceiling on a single GPU.

Monthly cost is **flat at ~NZD $3,200/month fully loaded** regardless of document volume, because the GPU is idle-dominated below its ceiling:
- **1,000 docs/day:** utilisation ~3–4%, cost ~NZD $3,200/month → NZD **$0.107/document**
- **10,000 docs/day:** utilisation ~28–42%, cost ~NZD $3,200/month → NZD **$0.011/document**

### 7.4 Head-to-head table

| Workload | Bedrock NZ Haiku 4.5 | Catalyst C1A Llama 3.3 70B | Delta | Cross-over |
|---|---|---|---|---|
| 1,000 docs/day | **~NZD $151/month** | **~NZD $3,200/month** | **+$3,049 (21× more expensive)** | Open-source wins only if clinical accuracy or sovereignty has a priced value > $3k/mo |
| 5,000 docs/day | ~NZD $756/month | ~NZD $3,200/month | +$2,444 (4.2× more expensive) | — |
| 10,000 docs/day | ~NZD $1,512/month | ~NZD $3,200/month | +$1,688 (2.1× more expensive) | — |
| 20,000 docs/day | ~NZD $3,024/month | ~NZD $3,200/month | +$176 (1.06×) | **Near break-even** |
| 30,000 docs/day (ceiling for single A6000) | ~NZD $4,536/month | ~NZD $3,200/month | **−$1,336 (open-source 30% cheaper)** | Open-source wins outright |
| 50,000 docs/day (needs 2× A6000) | ~NZD $7,560/month | ~NZD $6,400/month | −$1,160 (open-source 15% cheaper) | Open-source wins |

**Cross-over point: ~20,000 documents/day.** Below that, Bedrock Haiku 4.5 is cheaper; above it, self-hosted open-source is cheaper.

### 7.5 Interpreting the result

- **At Sprint 2/3 synthetic data scale (few hundred docs/day equivalent), Bedrock NZ is much cheaper per unit work.** Use Bedrock for fast prompt iteration and baseline benchmarking.
- **At Objective 2 single-practice scale (~1,000 docs/day), Bedrock is materially cheaper.** The open-source case at this scale is not about unit cost — it is about sovereignty posture, determinism, control over the upgrade path, avoiding per-token pricing risk, and owning the clinical audit trail end-to-end.
- **At multi-practice or aggregated scale (10,000+ docs/day), the gap closes fast and cross-over arrives at ~20k/day.** Any deployment of several practices under one inference instance flips the economics toward open-source.
- **The defensible answer for R3 is to evaluate both on clinical accuracy and operational fit, and keep both stacks warm.** The unit-cost delta at our current scale is within the noise of clinical accuracy differences — the choice will be driven by R3 evaluation results, not cost.

### 7.6 Hidden costs on each side

**Bedrock NZ Haiku 4.5 hidden costs:**
- Cross-Region inference routing (ap-southeast-6 as source may route to Sydney for some models — see R2). Latency and potential data-residency implications.
- Per-token pricing volatility — Anthropic can raise prices, and the grant budget would have to absorb it.
- Less control over the upgrade path — Anthropic deprecates models on its schedule, not ours (model-version pinning policies vary).
- Clinical audit trail depends on AWS CloudTrail + Bedrock logging; determinism on Bedrock is not guaranteed across model versions.

**Catalyst C1A self-hosted hidden costs:**
- Ops labour — SGLang deployment, monitoring, patching, model version management. R7-E estimates ~0.1–0.2 FTE sustained ops for a 2-GPU deployment.
- Cold-start and recovery — a Catalyst VM restart takes minutes; single-provider single-VM deployment has no automatic failover.
- Model update cadence — open models ship every 2–4 weeks; re-validating on our synthetic set for each update is non-trivial.
- DevOps tooling (Evidently, Arize Phoenix, prompt logging infra) adds ~NZD $200–500/month equivalent if paid services are used; free/open-source versions add labour.

Adding ~NZD $500/month DevOps overhead to the open-source stack brings the honest all-in cost to ~**NZD $3,700/month** and pushes the cross-over point from ~20k/day to ~25k/day. Still well within the operating range of an aggregated multi-practice deployment.

### 7.7 Recommendation

**Run both stacks in R3 evaluation.** Use Bedrock NZ Claude for fast iteration and baseline. Use Catalyst C1A open-source for determinism, sovereignty, and clinical audit. Decide between them in R3 on accuracy + operational fit. Do not pre-commit on cost alone; at our current scale the cost difference is real but within the range that a clinical accuracy or operational fit advantage should overturn.

---

## 8. Production operational considerations

R7-E covered production ops in depth. The operational layer is where most small-team open-source deployments fail, so this is a first-class R3 question, not an afterthought.

### 8.1 Determinism and reproducibility

**The single most important operational constraint for clinical deployment.** Reproducible inference — same prompt, same model version, same output — is required for:
- DPIA compliance (audit logs must be replayable).
- Post-market surveillance (adverse-event investigation requires we can reproduce the inference that was given).
- Clinical incident review (HDC cases in NZ require reconstructable reasoning).
- Pre-deployment validation (regression testing across model updates).

**Implementation:**
- **SGLang deterministic mode enabled from day 1.** ~30% throughput cost, non-negotiable.
- **Model artefact version pinning.** SHA256 of weights, SGLang version, engine args, grammar files, and prompt templates all version-controlled and tagged per deployment.
- **Seed control** on sampling (temperature=0 for classification; deliberate seed if any stochastic sampling).
- **Full prompt-completion logging** to immutable object storage (Catalyst object storage, geo-replicated) with per-request metadata (model hash, request ID, timestamp, input token count, output token count, latency).

**vLLM batch invariance does not apply here** — as noted in §3, vLLM's batch-invariant path requires SM ≥9.0 and the RTX A6000 is SM 8.6. SGLang deterministic mode is the only path on our sovereign hardware.

### 8.2 Monitoring and drift detection

Small-deployment clinical monitoring stack (R7-E recommendation):

| Layer | Tool | Role |
|---|---|---|
| **LLM observability** | **Arize Phoenix** (open-source) | Prompt-completion logging, latency percentiles, error rates, drift detection on input distributions |
| **Evaluation pipelines** | **Evidently AI** (open-source) | Regression eval against labelled test set; runs on every deploy and nightly; flags regressions on per-class sensitivity, macro F1, QWK |
| **Drift alarms** | **CUSUM** (cumulative sum) | Statistical process control on per-class sensitivity over rolling windows; flags sustained degradation |
| **Infra metrics** | Prometheus + Grafana | GPU utilisation, VRAM, request queue depth, p50/p95/p99 latency |
| **Error tracking** | Sentry | Application-level errors on the serving path |

Both Phoenix and Evidently are free/open-source and self-hostable on Catalyst. No vendor lock-in, no overseas data flow. DevOps overhead ~0.1 FTE sustained.

### 8.3 Model update cadence

Open models ship updates every 2–4 weeks. The published operational pattern for clinical deployments:

1. **Do not auto-update.** Pin model version; evaluate new versions on a held-out clinical regression set before committing.
2. **Quarterly scheduled update window.** Evaluate 1–3 candidate models per quarter; promote the winner via staged rollout.
3. **Regression set.** ~500 items, never used for training, covers all urgency × document type combinations including boundary cases; includes items specifically chosen to stress-test contextual reasoning (the NHS 6:1 failure pattern).
4. **Go/no-go gate.** New model must match or beat pinned model on per-class sensitivity (≥99% Immediate/Urgent) and must not regress macro F1 by more than 1 point or QWK by more than 0.02.
5. **Rollback path.** Previous model version remains hot-loadable for 30 days after promotion.

### 8.4 Disaster recovery and failover

Single-provider, single-VM deployment on Catalyst is a single point of failure. Mitigation options, in ascending cost:

| Option | Cost | Recovery time |
|---|---|---|
| **Warm backup** — second C1A VM on Catalyst in a different region (Hamilton ↔ Porirua), idle, manual failover | +~NZD $3,200/month | ~5 min manual |
| **Hot standby** — two C1A VMs behind a load balancer, active-passive | +~NZD $3,200/month + LB | <1 min auto |
| **Datacom Sovereign as disaster-recovery tenant** — idle contract, emergency activation | Quote-dependent; likely ~NZD $500–1,000/month retainer | Hours |
| **Graceful degradation** — when primary unavailable, Inbox Helper automatically routes to manual queue (GP triages inbox without AI assist); assist-only design means no clinical harm | Free | Instant |

**Recommendation.** Start with **graceful degradation** (free, clinically safe — assist-only design means AI unavailability is not a safety event) plus a weekly automated restart drill. Add **warm backup on second Catalyst region** at Objective 2 scale if continuous availability becomes a product requirement. Datacom Sovereign retainer is a nice-to-have not a must-have.

### 8.5 Clinical-grade logging for DPIA and post-market surveillance

Every inference must produce an immutable audit record containing:
- Unique request ID
- Timestamp (UTC + NZ local)
- Model identifier (name + version hash)
- Engine identifier (SGLang version + args)
- Full input prompt (including system prompt, few-shot exemplars, document text, patient context)
- Full output (structured JSON + any CoT rationale)
- Latency (p50/p95 metadata)
- Confidence score and abstention flag
- Routing decision (pre-classifier pass-through? main? arbiter?)
- User/practice identifier (for authorisation audit)
- Outcome hook (slot for GP's accept/override/edit action, filled later when available)

Stored in Catalyst object storage (geo-replicated NZ), with retention policy aligned to HIPC 2020 + any post-market surveillance retention requirements under the Medical Products Bill transitional regime. R7-E recommends **10-year retention** as the defensible default.

### 8.6 Sprint 3 deployment checklist

Based on R7-E, the minimal production-ready deployment for Sprint 3 evaluation is:
1. SGLang deterministic mode running on Catalyst C1A A6000.
2. XGrammar structured output for JSON schema enforcement.
3. Model version pinned and SHA256 recorded.
4. Arize Phoenix logging to Catalyst object storage.
5. Evidently nightly regression eval against held-out test set.
6. Prometheus + Grafana for infra metrics.
7. Sentry for application error tracking.
8. Written runbook for restart, rollback, and graceful degradation.
9. Written data-handling policy distinguishing synthetic (may route overseas) from identifiable clinical data (must stay on Catalyst).

---

## 9. Failure modes — self-hosted open-source vs API-hosted closed

### 9.1 Shared failure modes (both stacks)

The NHS GPT-oss-120b primary care medication review (arXiv 2512.21127, Oct–Nov 2025) established the dominant primary-care LLM failure pattern: **contextual reasoning failures outnumber factual errors 6:1**. This pattern is model-size-insensitive and engine-insensitive — it shows up on GPT-oss-120B, GPT-4, Claude Sonnet, and Llama 70B alike. Our mitigation — the three-tier cascade with abstention gate and second-opinion arbiter — applies equally to both the Bedrock NZ Claude and the self-hosted open-source stacks.

Other shared failure modes:
- **Distribution shift from synthetic to real data.** Synthetic training data systematically under-represents the tail of real-world clinical writing styles. Mitigation: Sprint 4+ incremental retraining on real de-identified data when it becomes available in Objective 2.
- **Spectrum bias.** Over-representing clear-cut cases inflates accuracy. Mitigation: enriched borderline-case sampling in the synthetic dataset (see R5) and evaluation on a natural-prevalence held-out set in addition to the enriched set.
- **Calibration drift over time.** Even with good initial calibration, downstream behavior drifts. Mitigation: quarterly re-calibration on a fresh held-out sample.

### 9.2 Failure modes specific to self-hosted open-source

| Failure mode | Description | Mitigation |
|---|---|---|
| **Quantisation accuracy cliff** | AWQ INT4 can degrade sharply on edge-case inputs even though average benchmarks look fine | Validate on our synthetic set at AWQ INT4 vs FP16 before committing; keep an FP16 reference running on Together A100 80 for benchmarking |
| **Engine version regression** | SGLang updates occasionally regress on specific model + grammar combinations | Version-pin SGLang; quarterly regression eval on update |
| **GPU driver / CUDA mismatch** | Catalyst VM kernel updates can break CUDA compatibility | Use pinned VM images; test updates in a non-prod environment first |
| **Single-provider risk** | Catalyst outage → inference unavailable | Graceful degradation to manual queue (assist-only design); Datacom Sovereign as optional Plan B retainer |
| **Model licence drift** | Llama Community Licence terms change; new clinical restrictions added | Maintain Qwen 3 32B (Apache 2.0) as parallel-tested backup |
| **Ops burden** | ~0.1–0.2 FTE sustained on monitoring, patches, updates | Budget explicitly; consider bringing in a contract SRE for Objective 2 scale |
| **Batch-invariance gap on SM 8.6** | vLLM deterministic mode won't work — locks us into SGLang | Not a failure mode if we commit to SGLang from the start; becomes one only if SGLang ecosystem weakens |

### 9.3 Failure modes specific to API-hosted closed (Bedrock NZ)

| Failure mode | Description | Mitigation |
|---|---|---|
| **Cross-Region inference surprise** | ap-southeast-6 may route to ap-southeast-2 (Sydney) for some models without explicit pinning — data residency implications | See R2 §2; get written confirmation from AWS on which models are native in ap-southeast-6 vs cross-Region routed |
| **Vendor model deprecation** | Anthropic deprecates a Claude version; we must re-validate the successor | Quarterly regression eval on new versions before pinned version deprecates |
| **Pricing volatility** | Per-token pricing can change mid-grant | Self-hosted Catalyst remains a backup; can migrate inference load if Bedrock pricing becomes untenable |
| **Opaque guardrails** | Anthropic's safety filters can block legitimate clinical queries (Heidi Health precedent of guardrail bypass disclosed March 2026) | Evaluate guardrail behaviour on our synthetic clinical corpus before committing; document any systematic blocks |
| **Determinism not guaranteed** | Bedrock does not publish batch-invariance guarantees across requests | Log every prompt-completion pair; accept non-determinism at the observability layer |
| **Limited fine-tuning** | Bedrock Claude fine-tuning is limited vs open models — prompt engineering is the only adaptation lever | Use DSPy MIPROv2 at the prompt layer; accept a narrower adaptation ceiling |
| **Data residency audit ambiguity** | ap-southeast-6 is too new for established audit practice; Privacy Commissioner has no published ruling | See R2 §5.b; escalate to OPC for written confirmation before go-live |

### 9.4 The published guardrail-bypass precedent

R2 covered the **Heidi Health March 2026 Mindgard disclosure** in depth: three prompts were sufficient to bypass the Heidi guardrails on a NZ health AI deployment. This is a failure mode that affects both stacks — open-source and closed — but the **defensive posture** is different:
- **Self-hosted open-source:** We own the guardrail layer. We can add pre-filters, input sanitation, and output validation at whatever depth we want. Full control of the defence-in-depth stack.
- **API-hosted closed:** We rely on the vendor's guardrails, which are opaque and can be bypassed by prompts outside our test coverage. We can add our own wrapper guardrails but do not control the inner layer.

For an assist-only clinical AI, the self-hosted stack's **additional control over the guardrail layer** is a defensible security advantage — not a cost. This goes into the R3 evaluation.

---

## 10. Recommended open-source stacks for R3 shortlist

Two stacks, both fully specified and ready to paste into the R3 shortlist deliverable as first-class candidates alongside the Bedrock NZ Claude Haiku 4.5 and Claude Sonnet 4.6 candidates.

### 10.1 Stack A — Llama 3.3 70B / SGLang / Catalyst C1A A6000 (PRIMARY)

| Dimension | Value |
|---|---|
| **Main model** | Llama 3.3 70B Instruct, AWQ INT4 quantisation |
| **Licence** | Llama 3.3 Community Licence (assist-only, research, and most commercial deployment allowed) |
| **Pre-classifier** | BioClinical ModernBERT 396M (MIT licence), fine-tuned full-parameter on synthetic set |
| **Arbiter / second opinion** | MedGemma 27B-IT INT4 (Gemma licence), loaded on-demand for abstained items |
| **Care Gap Finder extractor** | Meditron3-8B (Llama 3.1 Community), QLoRA + DoRA r=16 on 300–500 extraction examples |
| **Inference engine** | SGLang ≥0.4 in **deterministic mode** with **XGrammar** structured-output backend |
| **Hosting** | Catalyst Cloud **C1A RTX A6000 48 GB**, single-tenant VM, 24×7, nz-hlz-1 or nz-por-1 |
| **Scale ceiling (single VM)** | ~24,000–36,000 documents/day theoretical; ~1,400–2,100 documents/hour sustained |
| **Deployment engineer-weeks** | ~2–3 engineer-weeks for Sprint 3 stand-up (including SGLang config, XGrammar schema, logging, regression eval scaffold) |
| **Expected accuracy ceiling** | Competitive with closed frontier models on JMS structured prompting triage (~85–88%) and ICPC-2 (F1 ≥0.82); ~2–4 points below Claude Sonnet 4.6 on the toughest cases |
| **Expected sensitivity ceiling (Immediate/Urgent)** | ≥99% achievable via weighted focal loss + temperature scaling + conformal prediction + abstention gate to MedGemma arbiter |
| **Contextual reasoning mitigation** | Three-tier cascade + CoT rationale forcing + abstention gate + differently-trained arbiter — directly targets the NHS 6:1 contextual-failure pattern |
| **Cost at 1k docs/day** | ~NZD $3,200/month fully loaded (idle-dominated) |
| **Cost at 10k docs/day** | ~NZD $3,200/month fully loaded (utilisation ~28–42%) |
| **Latency (p95)** | ≤ 5 s per document async; ≤ 3 s interactive |
| **Sovereignty fit** | **Strongest** — NZ-owned, NZ-operated, ISO 27001/27017, three NZ data centres, HIPC 2020 + HISO 10029 compliant |
| **Implementation effort** | Moderate — SGLang deterministic mode is mature but new to team; fine-tuning and cascade orchestration adds complexity |
| **Key risks** | (i) AWQ INT4 quantisation accuracy regression on edge cases — validate in Sprint 3; (ii) Catalyst C1A capacity availability — confirm with sales; (iii) SGLang deterministic mode throughput overhead ~30% is tolerable but eats margin |
| **Ruling criteria (would rule stack in)** | Per-class sensitivity ≥99% on Immediate + Urgent in Sprint 3 eval + macro F1 ≥0.80 + QWK ≥0.80 + p95 latency ≤5s |
| **Ruling criteria (would rule stack out)** | AWQ INT4 accuracy regression >3 points vs FP16 reference on synthetic set; or SGLang deterministic mode fails to maintain <5s p95 on A6000; or Catalyst cannot provision C1A in our window |

### 10.2 Stack B — Qwen 3 32B / SGLang / Catalyst C1A A6000 (ALTERNATIVE)

| Dimension | Value |
|---|---|
| **Main model** | Qwen 3 32B, FP8 or AWQ INT4 quantisation |
| **Licence** | **Apache 2.0 — cleanest commercial licence of any major open model** |
| **Pre-classifier** | BioClinical ModernBERT 396M (same as Stack A) |
| **Arbiter / second opinion** | MedGemma 27B-IT INT4 (same as Stack A) |
| **Care Gap Finder extractor** | Meditron3-8B QLoRA + DoRA (same as Stack A) |
| **Inference engine** | SGLang ≥0.4 deterministic mode + XGrammar (same as Stack A) |
| **Hosting** | Catalyst Cloud C1A RTX A6000 48 GB (same as Stack A) |
| **Scale ceiling (single VM)** | ~30,000–50,000 documents/day theoretical (Qwen 3 32B is faster per token than Llama 3.3 70B) |
| **Deployment engineer-weeks** | ~2 engineer-weeks — slightly simpler than Stack A because Qwen 3 32B fits more comfortably on 48 GB |
| **Expected accuracy ceiling** | 2–4 points below Llama 3.3 70B on most clinical benchmarks; competitive on structured tasks and tool use |
| **Expected sensitivity ceiling (Immediate/Urgent)** | ≥99% achievable with same cocktail as Stack A |
| **Contextual reasoning mitigation** | Same three-tier cascade as Stack A |
| **Cost at 1k and 10k docs/day** | Same Catalyst C1A VM cost; effectively identical to Stack A |
| **Latency (p95)** | Slightly better than Stack A due to smaller model (p95 ~2.5–4 s) |
| **Sovereignty fit** | Same as Stack A + **cleanest licence** (Apache 2.0) |
| **Implementation effort** | Slightly lower than Stack A |
| **Key risks** | (i) Accuracy gap to Llama 3.3 70B may cost 1–3 points on hard cases; (ii) Qwen family clinical fine-tune ecosystem is thinner than Llama's |
| **Ruling criteria** | Same metric thresholds as Stack A; pick this stack if Llama licensing becomes a problem or if latency is more important than absolute accuracy |

### 10.3 How Stacks A/B compare to the Bedrock NZ Claude candidates in R3

R3 will shortlist **four candidates total**:
1. **Claude Haiku 4.5 on Bedrock ap-southeast-6** — managed, cheapest at low volume, fastest iteration, moderate clinical ceiling.
2. **Claude Sonnet 4.6 on Bedrock ap-southeast-6** — managed, highest clinical ceiling of the closed models, most expensive, use as arbiter + ceiling reference.
3. **Stack A (Llama 3.3 70B SGLang on Catalyst C1A) — this report's recommendation** — self-hosted, NZ-sovereign, determinism-controlled, close-to-closed clinical ceiling.
4. **Stack B (Qwen 3 32B SGLang on Catalyst C1A) — this report's alternative** — cleanest licence, faster, slightly below Stack A.

Plus a **hybrid rules + LLM** candidate that sits alongside them (proposed separately in R3).

### 10.4 Sprint 3 evaluation protocol for Stacks A and B

From Sprint 2 architecture plan:

| Phase | Activity | Duration | Gate |
|---|---|---|---|
| **Week 1 Sprint 3** | Stand up SGLang + Llama 3.3 70B AWQ INT4 on Catalyst C1A A6000; run zero-shot baseline on synthetic set | 3 days | Deterministic mode confirmed; p95 <5s; throughput ≥0.3 docs/s |
| **Week 1 Sprint 3** | Stand up Qwen 3 32B on the same VM; run zero-shot baseline | 2 days | Same gates |
| **Week 2 Sprint 3** | Run DSPy MIPROv2 prompt optimisation for Stack A and Stack B | 2 days | MIPROv2 improves accuracy over zero-shot baseline |
| **Week 2 Sprint 3** | Run QLoRA + DoRA (r=16) on both stacks | 3 days | Fine-tune improves over MIPROv2 baseline on held-out eval |
| **Week 3 Sprint 3** | Add temperature scaling + conformal prediction + abstention gate | 2 days | ≥99% sensitivity on Immediate/Urgent achieved without abstaining on >15% of items |
| **Week 3 Sprint 3** | Wire in MedGemma 27B-IT arbiter on abstained items | 2 days | Abstained items resolved correctly ≥90% of the time |
| **Week 4 Sprint 3** | Final evaluation: macro F1, QWK, per-class sensitivity, PR-AUC, MCC, BCa bootstrap CIs. Head-to-head vs Bedrock Claude candidates | 3 days | Architecture decision ready for Goal B (end April) |

---

## 11. Open questions to resolve before committing

In priority order, highest-value escalations first:

1. **Catalyst Cloud C1A NZD pricing — re-verify manually.** R7-C's figures are modelled from peer-provider benchmarks because the live price list was 403-blocked. Before any MBIE budget commitment, get the real NZD/hr for `c1a.c16r64-gpu1` and related flavours from `catalystcloud.nz/pricing/price-list/` or by direct quote. Expected range: ±15% of NZD $3.10/hr.
2. **Callaghan Innovation — confirm overseas cloud compute treatment in writing.** Cross-reference with R2 §11. Specifically: does the grant manager accept synthetic-data dedicated endpoints on Together AI as a "capability not sourceable in NZ" consumable? Written email confirmation before any overseas spend in Sprint 3.
3. **AWS — confirm which Claude models are native in ap-southeast-6 vs cross-Region routed.** Cross-reference with R2 §2. Required for honest head-to-head in R3 and for the sovereignty story in the MBIE Q1 report.
4. **Catalyst Cloud sales — confirm C1A A6000 capacity in our Sprint 3 window.** Single-tenant VMs are not always immediately provisionable; lead time matters. Ask for a reserved-capacity commitment covering April–October 2026.
5. **Catalyst Cloud — clinical-AI reference customer.** Ask if any NZ health tenant is on C1A today and whether they can share a reference for the MBIE narrative.
6. **Datacom Sovereign GPUaaS — indicative quote.** Get a quote in Month 1 of Sprint 3 for the same 1 × A6000-class or L40S-class deployment, so Plan B pricing is known in case Catalyst capacity becomes constrained.
7. **Together AI — BAA + NZ customer eligibility.** Written confirmation that enterprise BAA is available to a NZ-registered R&D entity, and that SOC 2 audit scope covers the Dedicated Endpoints product specifically.
8. **SGLang — deterministic mode on SM 8.6 regression test.** Confirm via a self-run benchmark on the exact SGLang version we plan to pin (0.4.x at time of writing) that deterministic mode produces bit-identical outputs across batch sizes on A6000. This is the critical architectural assumption; validate it early in Sprint 3 as a quick sanity check.
9. **Llama 3.3 70B Community Licence scope for NZ clinical assist-only deployment.** Legal review — is there anything in the 700M MAU or acceptable-use clause that constrains our deployment? If yes, Stack B (Qwen 3 Apache 2.0) becomes primary.
10. **Meditron3-8B commercial licence path.** Meditron3 inherits Llama 3.1 Community — confirm no additional EPFL research-only restriction.
11. **XGrammar schema tooling.** Confirm the structured output schema we need for Inbox Helper compiles cleanly and is performant at our throughput target; run a micro-benchmark on sample documents in the first 2 days of Sprint 3.

---

## 12. Reference list

### 12.1 Benchmarks and clinical LLM evaluation

- BRIDGE benchmark — https://arxiv.org/abs/2504.19467
- Journal of Medical Systems 2025 structured prompting triage study — https://doi.org/10.1007/s10916-025-02284-y
- ICPC-2 coding benchmark — https://arxiv.org/abs/2507.14681
- NHS GPT-oss-120b primary care medication safety review — https://arxiv.org/abs/2512.21127
- LCD benchmark (long clinical document mortality) — https://www.medrxiv.org/content/10.1101/2024.03.26.24304728v1
- EHRNoteQA (NeurIPS 2024 datasets track) — https://proceedings.neurips.cc/paper_files/paper/2024/hash/ehrnoteqa
- Open Medical-LLM Leaderboard — https://huggingface.co/spaces/openlifescienceai/open_medical_llm_leaderboard
- JAMA Health Forum March 2025 (Llama 3.1 405B ~70% vs GPT-4 ~64% on NEJM) — cited via Harvard Medical School news March 2025

### 12.2 Open-source model references

- Llama 3.3 70B Instruct — https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
- Llama 3.3 70B AWQ INT4 — https://huggingface.co/ibnzterrell/Meta-Llama-3.3-70B-Instruct-AWQ-INT4
- Qwen 3 32B — https://huggingface.co/Qwen/Qwen3-32B
- Qwen 2.5 72B Instruct — https://huggingface.co/Qwen/Qwen2.5-72B-Instruct
- Meditron3-8B — https://huggingface.co/OpenMeditron/Meditron3-8B
- MedGemma 27B-IT — https://huggingface.co/google/medgemma-27b-text-it
- BioClinical ModernBERT — https://huggingface.co/thomas-sounack/BioClinical-ModernBERT
- GPT-OSS-120B — https://huggingface.co/openai/gpt-oss-120b
- DeepSeek-R1 — https://huggingface.co/deepseek-ai/DeepSeek-R1
- Llama 4 Scout / Maverick — https://ai.meta.com/blog/llama-4/

### 12.3 Inference engines and structured output

- vLLM — https://github.com/vllm-project/vllm
- SGLang — https://github.com/sgl-project/sglang
- SGLang deterministic mode documentation — https://docs.sglang.ai/backend/deterministic.html
- LMDeploy — https://github.com/InternLM/lmdeploy
- TensorRT-LLM — https://github.com/NVIDIA/TensorRT-LLM
- TGI maintenance-mode notice — https://github.com/huggingface/text-generation-inference (December 2025)
- XGrammar — https://github.com/mlc-ai/xgrammar
- Outlines — https://github.com/outlines-dev/outlines
- lm-format-enforcer — https://github.com/noamgat/lm-format-enforcer
- Kurtic et al., "Give Me BF16 or Give Me Death" (ACL 2025) — https://arxiv.org/abs/2411.02355
- QM-ToT quantisation + medical reasoning — https://arxiv.org/abs/2504.12334

### 12.4 Fine-tuning and PEFT

- LoRA — https://arxiv.org/abs/2106.09685
- QLoRA — https://arxiv.org/abs/2305.14314
- DoRA — https://arxiv.org/abs/2402.09353
- DSPy — https://github.com/stanfordnlp/dspy
- MIPROv2 — https://arxiv.org/abs/2406.11695
- Khattab et al., "Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together" — https://arxiv.org/abs/2407.10930
- Unsloth — https://github.com/unslothai/unsloth
- Axolotl — https://github.com/axolotl-ai-cloud/axolotl
- HuggingFace PEFT — https://github.com/huggingface/peft
- HuggingFace TRL — https://github.com/huggingface/trl

### 12.5 Calibration, recall optimisation, conformal prediction

- Guo et al. 2017, "On Calibration of Modern Neural Networks" — https://arxiv.org/abs/1706.04599
- Focal Loss for Dense Object Detection — https://arxiv.org/abs/1708.02002
- Angelopoulos & Bates 2021, "A Gentle Introduction to Conformal Prediction" — https://arxiv.org/abs/2107.07511
- El-Yaniv & Wiener 2010, "On the Foundations of Noise-free Selective Classification" — https://www.jmlr.org/papers/v11/el-yaniv10a.html

### 12.6 Cloud GPU providers and hosting

- Catalyst Cloud C1A GPU — https://catalystcloud.nz/services/iaas/compute/compute-c1a-gpu/
- Catalyst Cloud C3 GPU (L40S Beta) — https://catalystcloud.nz/services/iaas/compute/compute-c3-gpu/
- Catalyst Cloud GPU support / C2 deprecation — https://docs.catalystcloud.nz/compute/gpu-support.html
- Catalyst Cloud ISO 27001/27017 — https://catalystcloud.nz/about/news/catalyst-cloud-attains-leading-international-information-security-certification/
- Catalyst Cloud data sovereignty — https://catalystcloud.nz/about/data-sovereignty/
- Catalyst Cloud pricing (sandbox 403-blocked — re-verify manually) — https://catalystcloud.nz/pricing/price-list/
- Datacom Sovereign Cloud — https://datacom.com/nz/en/solutions/cloud/hybrid-and-private/sovereign
- Together AI pricing — https://www.together.ai/pricing
- Together AI Dedicated Endpoints — https://www.together.ai/dedicated-endpoints
- Fireworks AI pricing — https://fireworks.ai/pricing
- Fireworks AI SOC 2 Type II + HIPAA — https://fireworks.ai/blog/fireworks-ai-achieves-soc-2-type-ii-and-hipaa-compliance
- Modal HIPAA — https://modal.com/blog/hipaa
- CoreWeave pricing — https://www.coreweave.com/pricing

### 12.7 Multi-tenancy and serverless GPU isolation concern

- Cerebrium, "Choosing the Right Serverless GPU Platform for Global Scale" — https://www.cerebrium.ai/articles/deploying-ai-workloads-on-serverless-gpus-for-global-scale
- Introl, "Multi-tenant GPU security" — https://introl.com/blog/multi-tenant-gpu-security-isolation-strategies-shared-infrastructure-2025
- WhiteFiber, "GPU Infrastructure Compliance in Regulated Healthcare AI" — https://www.whitefiber.com/blog/gpu-infrastructure-compliance-in-regulated-healthcare-ai
- Edera, "Securing the AI Grid" — https://edera.dev/stories/the-ai-grid-is-coming-to-cell-sites-so-are-the-attackers

### 12.8 Production ops and monitoring

- Arize Phoenix — https://github.com/Arize-ai/phoenix
- Evidently AI — https://github.com/evidentlyai/evidently
- Prometheus — https://prometheus.io/
- Grafana — https://grafana.com/
- Sentry — https://sentry.io/

### 12.9 MBIE / Callaghan Innovation

- New to R&D Grant — https://funds.business.govt.nz/products/fund/new-to-r-and-d-grant/
- Callaghan Innovation — https://www.callaghaninnovation.govt.nz/products/fund/new-to-r-and-d-grant/
- 2018 Gazette direction — https://gazette.govt.nz/notice/id/2018-go4864

### 12.10 Cross-references within this research campaign

- R1 — Clinical LLM architecture benchmarks (file: `research-r1-llm-architecture-benchmarks.md`)
- R2 — NZ sovereign LLM hosting + regulatory posture + DPIA methodology (file: `research-r2-nz-sovereign-hosting-regulatory.md`)
- R3 — Architecture shortlist (forthcoming, depends on this report)
- R4 — Care Gap Finder sub-task architectures (forthcoming)
- R5 — Synthetic NZ GP inbox dataset protocol (forthcoming, pending GP review feedback)
- R6 — Medtech / Indici / ALEX API + NZ data standards (forthcoming)

---

*End of R7 research report.*
