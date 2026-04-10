---
title: Sprint 2 Research Plan — nexwave-rd Objective 1
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-10
status: final
---

# Sprint 2 Research Plan — nexwave-rd Objective 1

## Context

**Why this plan exists.** Sprint 1 of nexwave-rd Objective 1 (`2026-04-rd-sprint-1`, 29 Mar–11 Apr 2026) is almost done. Step 1 of the 5-step roadmap (problem definition) is complete — both task specs (`inbox-helper-task-spec.md` and `care-gap-finder-task-spec.md`) are finalised in `context/nexwave-rd-context/`.

Sprint 2 (`2026-04-rd-sprint-2`, 12–25 Apr 2026) already exists with goal **"Literature review and architecture research"**. It covers Steps 2–3 of the obj-1 roadmap: literature review, architecture shortlist, data requirements, and synthetic data foundations. **Goal B (Architecture Decision Made and Documented) is due end of April** — so Sprint 2 outputs must be sharp enough to enable that decision on time.

The user plans to use **Claude.ai Research mode** to do the heavy lifting, then bring the reports back into the vault to produce Sprint 2 deliverables. This plan specifies:
1. What research needs to be done (scoped around the gaps — not what's already in the vault)
2. Ready-to-paste prompts for Claude.ai Research mode
3. How to ingest the reports back into the vault to generate Sprint 2 outputs

**Strategic framing (from competitor tracker + dashboard):** The vision is **NZ-sovereign clinical AI — built and operated within NZ under Privacy Act constraints, not dependent on overseas cloud infrastructure**. The differentiator against competitors (Health Accelerator RPA bots, Medtech AI, Inbox Magic, BPAC CS) is **AI reasoning + clinical accuracy + ALEX FHIR API integration**. No competitor is currently using ALEX API for AI inbox triage — that is NexWave's structural opening. Research must keep this sovereignty + reasoning + ALEX posture in mind.

---

## Important: what's already in the vault (DO NOT duplicate in Claude.ai research)

Before writing prompts, I audited existing context files. The following topics are **already comprehensively researched** in `context/nexwave-rd-context/`. Research prompts below **avoid** these areas and focus on remaining gaps.

| Already covered | Source file |
|---|---|
| Urgency taxonomy, 3-vs-4-vs-5 level trade-off, NHS GP Forward View, AAFP three-level, NLP classification schemes (Si, Harzand, Gatto, Apathy, Rotenstein) | `Urgency classification for GP inbox triage.md` |
| Evaluation metrics framework (per-class sensitivity, macro F1, QWK, PR-AUC, MCC), Buderer sample-size formula, BCa bootstrap, spectrum bias, shortcut learning, Hicks pitfalls | `Evaluation metrics for ordinal clinical AI triage classification.md` |
| Inbox Helper task definition, urgency criteria per document type, boundary cases, output schema, success criteria | `inbox-helper-task-spec.md` |
| Care Gap Finder task definition, gap detection logic, CVDRA eligibility matrix, 3-subtask architecture (rules / extraction / calculation) | `care-gap-finder-task-spec.md` |
| TGA Class IIa classification, CDSS exemption failure, TTMRA, IMDRF GMLP 10 Principles, FDA Jan 2026 draft guidance, TGA Oct 2025 guidance | `inbox-helper-task-spec.md` §9 and `Evaluation metrics for ordinal clinical AI triage classification.md` §6 |
| NZ clinical guidelines: NZSSD diabetes, BPAC NZ diabetes toolbox, HISO 10071:2025 PREDICT, MoH 2018 CVDRA, RCPA/AACB harmonised alerts | `nz-diabetes-monitoring.md`, `nz-cardiovascular-risk-assessment.md`, `nz-hypertension-monitoring.md` |
| NZ medico-legal framework: Te Whatu Ora 2024 Transfer of Care, HDC case law (21HDC00619, 18HDC01066, 14HDC00894, 99HDC11494), NZMJ 2025 survey | `Urgency classification for GP inbox triage.md` §5 |
| Competitor landscape: Health Accelerator RPA, Medtech AI, Inbox Magic, BPAC CS, Heidi Health. ALEX API as untapped opening. | `Inbox Management — Competitor Tracker.md` |
| Manual care gap monitoring workflows in NZ practices | `manual-care-gap-monitoring.md` |

---

## Grounding research findings (G-series, executed 10 April 2026)

Before drafting the deep R-series research prompts, I ran a grounding pass using WebSearch to validate that the Sprint 2 assumptions still hold and to refresh the state of the world. Six findings materially change the plan — they are baked into the R-prompts below and noted explicitly here so the changes are traceable to evidence.

### G1 — AWS Bedrock is now live in NZ (ap-southeast-6), March 2026

**This is the biggest single update.** AWS opened the Asia Pacific (New Zealand) Region — `ap-southeast-6`, based in Auckland with three Availability Zones — in **September 2025**. **Amazon Bedrock launched in that region in March 2026** (i.e. last month, about 4 weeks before Sprint 2 starts). Auckland is now a source Region for both AU geographic and global cross-Region inference on Bedrock. AWS blog: "Run Generative AI inference with Amazon Bedrock in Asia Pacific (New Zealand)" — `aws.amazon.com/blogs/machine-learning/run-generative-ai-inference-with-amazon-bedrock-in-asia-pacific-new-zealand/`.

**Implications for our plan:**
- The sovereignty story is fundamentally different. Until March 2026 the closest Bedrock region was `ap-southeast-2` (Sydney). Now Claude Haiku/Sonnet can run in Auckland itself — data processed in NZ, under AWS NZ region controls.
- The dashboard's stated posture ("not dependent on overseas cloud infrastructure") no longer automatically rules out AWS — Bedrock NZ is AWS-operated but physically and jurisdictionally in NZ.
- R2 must pivot. The question is no longer "are there any NZ-hosted options at all?" It is **"AWS Bedrock NZ (ap-southeast-6) vs Catalyst Cloud self-hosted vs others — which is the defensible sovereignty posture for clinical data under NZ Privacy Act and MBIE grant terms?"**
- We need to confirm whether Claude Haiku 4.5 and Sonnet 4.6 are live in `ap-southeast-6` specifically (not just routed via cross-Region inference). This is a question for R2 and for the Medtech/Callaghan/Lisa Pritchard conversation.

### G2 — Catalyst Cloud confirmed as credible NZ-sovereign GPU option

Catalyst Cloud (Wellington- and Auckland-based, 100% NZ-owned, approved NZ Government cloud provider) runs three data centres in NZ and has GPU-as-a-Service live. Confirmed instance types:
- **C2 GPU** — slices of NVIDIA A100 80GB (each slice 20GB VRAM, dedicated pipelines)
- **C3 GPU** — full NVIDIA L40S 48GB cards
- **C1A GPU** — NVIDIA RTX A6000 48GB cards with AMD EPYC CPUs

"All customers' data stays safely in Aotearoa, protected by New Zealand laws and data privacy rules" and "the cloud fully managed by engineers located in New Zealand, meaning there is no jurisdictional risk caused by external or overseas engineers having access to their systems." This is the strongest-possible NZ sovereignty posture. Exact NZD hourly pricing not visible publicly — Price List page requires direct lookup; R2 prompt asks for it explicitly.

**Implications:** We now have **two credible NZ-sovereign inference paths**: (a) Bedrock NZ (managed, Claude models, AWS-operated), (b) Catalyst Cloud self-host (open models, full control, NZ-owned). These become candidates 1 and 2 in the R3 architecture shortlist.

### G3 — Claude model family has moved — update all model references

The current Claude model family on Bedrock (as of April 2026) includes **Claude Sonnet 4.6, Claude Opus 4.6, Claude Haiku 4.5, Claude Sonnet 4.5, Claude Opus 4.1, Claude Sonnet 4**. The project stack (`nexwave-rd-obj-1.md` frontmatter) lists `claude-haiku, claude-sonnet` without versions. R1 and R3 prompts should use current model names (**Claude Haiku 4.5** and **Claude Sonnet 4.6**) when naming candidates, so that benchmarks returned are applicable to the models we'd actually deploy.

### G4 — Medical Products Bill not in effect during grant period — simplify R2

Government intends to introduce the Medical Products Bill to Parliament **during 2026**, but commencement is expected **around 2030**. The Bill will regulate SaMD/AI used for therapeutic purposes (Cabinet July 2025 decision, confirmed August 2025). This means **during our grant period (Mar 2026 – Mar 2028) we are operating under the current regime**: Medicines Act 1981 + WAND notification + HIPC 2020 + Privacy Act 2020, plus TGA Class IIa considerations already covered in the vault.

**Implications:** R2 prompt should be narrower on Medical Products Bill — a status check, not a deep dive. The regulatory heavy lifting remains HIPC/Privacy Act + TGA classification (already covered) + DPIA methodology.

Source: MoH briefing "Supporting innovation through the Medical Products Bill" (August 2025), Russell McVeagh insights, NZ Nurses Organisation update.

### G5 — Clinical LLM architecture thinking has moved to "agentic + RAG + fine-tune hybrid"

2025–2026 consensus across multiple peer-reviewed and industry sources: **"fine-tune for format, RAG for knowledge"** is the most cited pattern, and **multi-agent / agentic architectures** that route queries to specialised tools (retrieval, calculation, extraction) are now prominent in clinical LLM research. Key benchmarks and studies discovered:

- **BRIDGE benchmark** (arXiv 2504.19467, 2025) — 95 LLMs tested across 20 clinical applications including triage and referral, spanning 14 specialties. Most relevant meta-benchmark for our task selection.
- **Structured prompting triage study** (Journal of Medical Systems 2025) — 8 contemporary LLMs on 48 vignettes, 4 triage levels (Emergent / 1-day / 1-week / Self-care), structured prompting lifted mean triage accuracy from 76.82% → 86.20%. Directly comparable to our task.
- **ICPC-2 coding benchmark** (arXiv 2507.14681, 2025) — 33 LLMs assigning International Classification of Primary Care codes; 28 models >0.8 F1, top performers gpt-4.5-preview, o3, gemini-2.5-pro. Primary-care relevant.
- **NHS real-world medication safety review** (arXiv 2512.21127, GPT-oss-120b, Oct–Nov 2025) — 178 failures across 148 patients; **contextual reasoning failures outnumber factual errors 6:1**. Critical failure-mode reference for our architecture risk section.
- **LCD benchmark** (medRxiv 2024.03.26, long clinical document mortality prediction on MIMIC-IV) — relevant for long-context handling of discharge summaries. Notes explicitly that "benchmark datasets targeting long clinical document classification tasks are absent" — confirming a gap we may partially fill.
- **EHRNoteQA** (NeurIPS 2024) — long-context clinical benchmark with 4k/8k token levels.

**Implications:**
- **R1 prompt updated** to add an "agentic / multi-agent" architecture axis and explicitly request findings from BRIDGE, the triage vignettes study, ICPC-2, and the NHS real-world study.
- **R3 prompt updated** to include a multi-agent / tool-use candidate alongside the RAG/fine-tune/hybrid candidates.
- **R5 prompt updated** to cite the NHS real-world failure modes study (contextual reasoning failures 6:1) as a design constraint on the synthetic dataset.

### G6 — Competitor landscape refresh (Apr 2026) — differentiator holds

- **Heidi Health** (referenced by dashboard) — now has a Government contract for 1,000 ED clinician licences (Nov 2025, Minister Simeon Brown), being rolled out across NZ's 16 largest EDs. Integrates with NZ EHRs/PMS. Stays focused on **clinical documentation scribing** (notes, summaries, letters to GPs) — **not inbox triage**. Also: newsroom.co.nz 20 March 2026 story about a Health NZ security flaw found in a Heidi-adjacent chatbot (detail worth tracking for competitor-risk purposes). **Our ALEX-driven inbox triage opening is still uncontested.**
- **BPAC CS Inbox Manager** — still rule-based, still Medtech-integrated via legacy pathways. "More tools will be added to BPAC CareSuite through 2026" — worth a watch item, but no semantic-reading AI announced.
- **Health Accelerator RPA** — confirmed scope: CVDRA, ACC claims reconciliation, specialist referral acknowledgement filing, normal FIT result filing. **All rule-based structured tasks** on Medtech PMS. No semantic reading of unstructured documents. No LLM reasoning.
- **Medtech ALEX** — 6 partners live (ConnectMed, Florence Digital, Jayex, Houston Intellimed, Webtools Health, Heartbeat Health). **None are doing AI inbox triage.** Opening holds.

**Implication:** The "AI reasoning + clinical accuracy + ALEX integration" differentiator claim in the dashboard and competitor tracker is validated as of April 2026. R3 candidates must preserve this posture.

### G7 — Open-source LLMs on cloud GPU are a credible first-class alternative to Bedrock

The user explicitly wants the architecture shortlist to stay open-minded about open-source LLMs running on cloud GPU — not just treat Bedrock as the default with open models as a fallback. Grounding research confirms this is warranted:

**Open-source model landscape for clinical work (2025–2026):**
- **Llama 3.1 405B performed on par with GPT-4** on clinical reasoning in a JAMA Health Forum March 2025 study. Open-source is no longer second-tier for clinical tasks.
- **Open Medical-LLM Leaderboard (Hugging Face)** provides standardised benchmarks for open clinical models.
- **Meditron (EPFL / Yale / Meta)** — Llama-3-8B MeditronV1.0 fine-tuned variant; "currently the best-performing open-source LLM for medicine" per leaderboard authors. MedQA, MedMCQA benchmarks.
- **MedGemma** (Google) — Gemma-3 base fine-tuned for medical domain.
- **PMC-LLaMA** — open medical LLM explicitly engineered for medical domain.
- **Hippo (7B family)** — Mistral/Llama2-based continual pre-training + RLHF; claimed to outperform 70B models.
- **GPT-OSS-120B (OpenAI)** — ranked top open-source pick for healthcare / medical diagnosis 2026 in industry reviews. Open weights, Apache/MIT-friendly.
- **DeepSeek-R1** — strong clinical reasoning on open-ended medical Q&A.
- **Qwen 2.5 / Qwen 3 (Alibaba)** — competitive on structured tasks, good tool use, permissive licence.
- **Llama 4** variants — Meta's latest open generation (available 2025–2026).
- **NHS real-world study used GPT-oss-120b** in primary care medication review (arXiv 2512.21127, Oct–Nov 2025) — so open-source at this scale is already being deployed in primary care.

**Production inference stack (2026 consensus):**
- **vLLM** — UC Berkeley origin, PagedAttention, battle-tested, "the default choice for production LLM serving". ~12,500 tok/s on H100.
- **SGLang** — LMSYS origin, RadixAttention, **~16,200 tok/s on H100 (29% throughput advantage over vLLM)**, particularly strong for multi-step programs and structured outputs (very relevant for our task).
- **LMDeploy** — also fast; strong quantisation support.
- **TensorRT-LLM** — NVIDIA native, highest raw throughput when paired with compatible hardware.
- **TGI (Hugging Face Text Generation Inference)** — **entered maintenance mode December 2025**. HF recommends vLLM or SGLang for new deployments. Do not pick TGI.
- Quantisation (FP8, INT8, INT4, AWQ, GPTQ) is the standard production move — can put Llama 3 70B on a single L40S 48GB with AWQ INT4, or on 2×A100 40GB, or full precision on 2×A100 80GB.

**Cloud GPU provider landscape for self-hosted LLMs (April 2026):**
- **Catalyst Cloud NZ** (covered in G2) — only NZ-sovereign option. A100 80GB slices (20GB VRAM per slice), L40S 48GB, A6000 48GB. Limitation: slice-based A100 sharing means limited full-GPU availability.
- **Runpod Secure Cloud** — SOC 2 and **HIPAA eligibility**, $2.69/hr H100, 48% cold starts <200ms with FlashBoot. **Overseas (US) — sovereignty concern for NZ clinical data.**
- **Modal** — $87M Series B Sep 2025, 2–4s cold starts, infrastructure-as-code; best developer experience. Overseas.
- **Lambda Labs** — $1.10/hr A100s, deprecated serverless in Sep 2025, now on-demand VMs only. Overseas.
- **Together AI** — GB200 clusters, API access to many open models ($0.20–0.50/M tokens). API-only, overseas.
- **Fireworks AI** — similar API access to open models, competitive pricing.
- **CoreWeave** — large GPU fleet, enterprise.
- **Vast.ai** — cheapest marketplace; not suitable for clinical data.
- **Key sovereignty caveat** — "serverless platforms share infrastructure across customers, with inference requests running on GPUs that processed someone else's data minutes earlier, which creates audit problems for healthcare (HIPAA)." Serverless is a non-starter for identifiable clinical data without dedicated-tenancy guarantees.

**Implications for the plan:**
1. **Add a new research task R7** — deep-dive on open-source LLM candidates + inference engine + cloud GPU provider combinations, producing an architecture-ready shortlist of 3–4 open-source stacks with benchmarks, cost, throughput, and sovereignty posture.
2. **R3 architecture shortlist is reframed** — the candidate slate must include both Bedrock NZ and open-source self-hosted options as equal first-class options, not one as primary and the other as fallback. The research must produce evidence for a genuine head-to-head.
3. **R2 stays focused on policy/sovereignty** — the open-source provider catalogue moves to R7. R2 covers where data legally can and cannot flow; R7 covers which open-source stacks we could run where.

### Plan updates triggered by grounding research

1. **R2 rewritten** — pivots from "are there NZ-hosted options?" to "Bedrock NZ (ap-southeast-6) vs Catalyst Cloud NZ vs others — defensibility under Privacy Act, HIPC, and MBIE grant". Medical Products Bill becomes a status check, not a deep dive.
2. **R1 augmented** — adds agentic/multi-agent axis; explicitly requests findings from BRIDGE, Journal of Medical Systems 2025 triage vignettes, ICPC-2 benchmark, NHS medication review real-world study, LCD long-doc benchmark, EHRNoteQA.
3. **R3 augmented** — candidate slate must include **both** a Bedrock-NZ-hosted Claude candidate and an open-source self-hosted candidate as **equal first-class options**; model names updated to Claude Haiku 4.5 and Claude Sonnet 4.6.
4. **R5 augmented** — references NHS real-world failure pattern (contextual reasoning failures 6:1) and asks for synthetic data design that stress-tests contextual reasoning specifically.
5. **R7 added (new)** — deep dive on open-source LLM architecture candidates for self-hosted deployment: model selection, inference engine, GPU fit, cloud provider, cost, throughput, sovereignty posture, fine-tuning approach for our data budget.
6. **No changes to R4 and R6** — their scope is unchanged by these findings.

---

## Current state of Sprint 2 (verified)

**File:** `/home/user/obsidian/sprints/active/2026-04-rd-sprint-2.md`
**Dates:** 12–25 Apr 2026 | **Objective:** obj-1 | **Goal:** Literature review and architecture research

**7 open tasks already scaffolded** (all task files are currently bare stubs — frontmatter + title only):

| Task ID | Title | Owner | Priority |
|---|---|---|---|
| rd-20260329-003 | Literature review — clinical NLP/LLM benchmarks and NZ sovereignty requirements | Ting | medium |
| rd-20260329-006 | LLM/RAG/fine-tuning initial research (in-progress) | Ryo | medium |
| rd-20260329-010 | Architecture shortlist and evaluation | Ryo | medium |
| rd-20260329-011 | Data requirements documented | Ting | medium |
| rd-20260329-014 | Evaluate Linear for issue tracking (tool eval — not research) | Ryo | medium |
| rd-20260329-022 | Design synthetic dataset schema | Ryo | high |
| rd-20260329-023 | Generate synthetic NZ GP inbox dataset (300–500 items) | Ryo | high |

These tasks are the **delivery vehicles** — research reports will feed directly into the deliverable documents each task produces. Task rd-20260329-014 (Linear evaluation) is out of scope for deep research.

---

## Sprint 1 dependency that affects Sprint 2 research

**`rd-20260405-001` (GP clinical review outreach, in-progress, due 20 Apr):** `nexwave-rd-obj-1.md` explicitly states: **"Step 2 begins once at least 2 reviewers have responded."** As of 9 Apr, Gareth Roberts reply is scheduled 9 Apr; Brendan Duck and Heidi Bubendorfer held as escalations. If clinical review surfaces refinements to urgency taxonomy or care gap trigger logic, the synthetic dataset (R5) and architecture evaluation (R3) may need to adjust. **Recommendation:** run R1, R2, R3, R4, R6 in parallel with GP review (they are safe — architecture and standards research is independent of minor spec refinement). Defer R5 (synthetic data generation) until clinical review feedback is incorporated, since every item in the dataset encodes the taxonomy.

---

## Research breakdown — 7 focused tasks (refactored to avoid duplication, R7 added for open-source track)

Each research task is scoped to one Claude.ai Research run (target 15–45 min per run). Prompts are written to **explicitly exclude** topics already covered in the vault so Research mode doesn't waste time rehashing them.

| # | Research topic | Feeds tasks | Owner | Depends on |
|---|---|---|---|---|
| **R1** | Clinical LLM architecture benchmarks — empirical results for zero-shot / few-shot / RAG / fine-tune / hybrid / agentic on clinical document classification (2024–2026) | rd-20260329-003, -006 | Ting/Ryo | None |
| **R2** | NZ sovereign LLM hosting (Bedrock NZ ap-southeast-6 vs Catalyst Cloud NZ) + regulatory posture + DPIA methodology | rd-20260329-003 | Ting | None |
| **R3** | Architecture shortlist for Inbox Helper + Care Gap Finder — head-to-head trade-off analysis, Bedrock NZ vs open-source self-hosted as equal first-class candidates | rd-20260329-006, -010 | Ryo | R1, R2, R7 |
| **R4** | Care Gap Finder sub-task architectures — rules engine patterns + variable extraction from NZ clinical text + missing-data handling | rd-20260329-010, -011 | Ryo | R1 |
| **R5** | Synthetic NZ GP inbox dataset generation — protocol, realism, labelling, privacy, contextual-reasoning stress items | rd-20260329-022, -023 | Ryo | GP review feedback |
| **R6** | Medtech / Indici / ALEX API capabilities + NZ FHIR/HL7 profiles + NZ code sets + field mapping | rd-20260329-011 | Ting | None |
| **R7** | **Open-source LLM self-hosted architecture options** — model selection (Llama 4, Qwen 3, GPT-OSS-120B, Meditron, MedGemma, DeepSeek-R1), inference engine (vLLM vs SGLang vs LMDeploy vs TensorRT-LLM), GPU fit, cloud provider, cost, fine-tuning approach, sovereignty posture | rd-20260329-006, -010 | Ryo | None |

**Sequencing guidance for execution:**
- **Week 1 (12–18 Apr)**: Run R1, R2, R4, R6, **R7** in parallel (independent). Start R3 once R1 + R2 + R7 are back.
- **Week 2 (19–25 Apr)**: Run R3 (depends on R1 + R2 + R7 for a credible head-to-head). Run R5 once GP review feedback is in. Synthesise into Sprint 2 deliverable docs.

---

## Claude.ai Research mode — prompt best practices applied below

Key techniques used in the prompts (sources: Anthropic prompting best practices, Claude Help Center Research mode docs, community guides — summarised in my WebSearch earlier in this planning session):

1. **XML structure** — `<context>`, `<objective>`, `<questions>`, `<constraints>`, `<deliverable>`, `<out_of_scope>`. Claude rewards structure and takes instructions literally.
2. **Explicit `<out_of_scope>` block** — critical for this project because the vault already has extensive research. Tells Research mode what NOT to waste time on, and references where that material lives so it doesn't feel it needs to redo the work.
3. **Concrete constraints** — NZ, sovereignty, assist-only, recall-optimised, specific accuracy targets (≥99% sensitivity Immediate/Urgent, ≥90% weighted accuracy triage, ≥95% CVDRA).
4. **Explicit deliverable format** — section list, length guidance, citation requirements. Prevents Research mode from producing a blog-style summary.
5. **Force evidence-before-summary** — ask for citations + specific numeric results, not just claims.
6. **Ask for trade-offs, not just lists** — forces comparison.
7. **Positive framing** — "focus on X" rather than "don't talk about Y" (Pink Elephant problem).
8. **Ready-to-paste** — each prompt is self-contained; no cross-references between prompts.

---

## Ingestion workflow (after all 7 reports are back)

Once the 7 reports are returned from Claude.ai:

1. **Save each report verbatim** into `context/nexwave-rd-context/` as:
   - `research-r1-llm-architecture-benchmarks.md`
   - `research-r2-nz-sovereign-hosting-regulatory.md`
   - `research-r3-architecture-shortlist.md`
   - `research-r4-care-gap-finder-subtasks.md`
   - `research-r5-synthetic-data-protocol.md`
   - `research-r6-data-standards-pms-integration.md`
   - `research-r7-open-source-llm-self-hosted.md`

   This matches the existing vault pattern — research outputs live as reference docs in `context/nexwave-rd-context/`, not inside task bodies.

2. **Start a fresh Claude Code session** in the vault with a short handoff prompt pointing to the 6 files. A new session is better than reusing this one because:
   - Fresh context window (6 reports can be large).
   - This session's planning chatter is noise for the execution step.
   - The new session can cleanly read → synthesise → write deliverable docs.

3. **In the new session, produce these Sprint 2 deliverables** (all filed in `context/nexwave-rd-context/`, linked from task files):
   - `sprint-2-literature-review.md` — synthesises R1 + R2 with links to the existing urgency classification and evaluation metrics docs. **Deliverable for rd-20260329-003.**
   - `sprint-2-architecture-shortlist.md` — 3–4 candidates with trade-offs (from R3 + R4), each scored against Inbox Helper requirements (5 doc types) and Care Gap Finder requirements (3 sub-tasks). **Deliverable for rd-20260329-010.**
   - `sprint-2-data-requirements.md` — data types, volumes, field mapping (from R6 + R4). **Deliverable for rd-20260329-011.**
   - `sprint-2-synthetic-dataset-schema.md` — schema, stratification, labelling protocol (from R5). **Deliverable for rd-20260329-022.**
   - Updates to each of the 4 task files above — append a "Progress" section with a wikilink to the deliverable doc and a short outcome summary.

4. **Update the nexwave-rd dashboard** weekly progress log with Sprint 2 completion entries (Week of 13 Apr, Week of 20 Apr).

5. **(Optional) Run a short "challenge" pass** — ask a fresh Claude Code session to critique the architecture shortlist against the competitor tracker (Health Accelerator RPA, Medtech AI, Inbox Magic) to make sure the shortlist preserves the AI reasoning + ALEX differentiator.

---

## The 6 research prompts

Each prompt below is **ready to paste into Claude.ai with Research mode enabled** (Search and tools → Research). Paste one at a time. Expect 15–45 min per run.

(Prompts inline below — see sections R1 through R6.)

---

### R1 — Clinical LLM architecture benchmarks (empirical results 2024–2026)

**Paste into Claude.ai with Research mode ON.**

```
<context>
I am a New Zealand R&D programme (MBIE New to R&D grant, CONT-109091-N2RD-NSIWKC) building two assist-only AI tools for NZ GPs:

1. Inbox Helper — classifies incoming clinical documents into 4 urgency levels (Immediate / Urgent / Routine / Information only). 5 document types: lab results, radiology reports, discharge summaries, specialist letters, patient messages. 3 of the 5 document types (discharge summaries, specialist letters, patient messages) have no standard structure and require full-document semantic reading.

2. Care Gap Finder — scans patient records for overdue checks (HbA1c, diabetes annual review components, CVDRA, BP). Deterministic rules engine + LLM-based variable extraction from clinical notes.

Targets locked in:
- Triage: ≥99% sensitivity for Immediate and Urgent classes; ≥90% overall weighted accuracy; macro F1 ≥0.80; QWK reported.
- CVDRA calculation: ≥95% accuracy on complete data.
- Recall-optimised (over-triage acceptable, under-triage is not).

Architecture must work under NZ data sovereignty constraints. Two credible NZ-hosted paths exist as of April 2026: **AWS Bedrock in ap-southeast-6 (Auckland)** — Bedrock launched in the NZ region in March 2026; and **Catalyst Cloud NZ GPU-as-a-Service** (A100 80GB slices, L40S 48GB, RTX A6000 48GB). Scale: 300–500 synthetic documents in Sprint 2, then real NZ GP inbox data (thousands/day) in Objective 2.

Current candidate models under consideration include Claude Haiku 4.5 and Claude Sonnet 4.6 (via Bedrock NZ), Llama 3/4 variants and Qwen/Mistral (self-hosted on Catalyst Cloud), clinical encoders, and hybrid rules + LLM pipelines. Research should cite benchmarks for the exact models where possible.
</context>

<objective>
Produce a deep, empirical literature review of LLM architecture benchmarks for clinical document classification, with concrete numbers (accuracy, sensitivity, compute, cost), so I can shortlist 3–4 architectures to evaluate on synthetic data in Sprint 3. I need enough published evidence to justify the shortlist to MBIE.
</objective>

<questions>
1. For clinical document classification (2024–2026), what are the strongest published empirical results for each of the following approaches?
   a. Zero-shot prompting with a closed frontier LLM (Claude Sonnet 4.5/4.6, Claude Haiku 4.5, GPT-4.5/5 class, Gemini 2.5 Pro)
   b. Few-shot in-context learning with structured exemplars
   c. RAG (retrieval of clinical guidelines, exemplar labels, similar past documents)
   d. Fine-tuning an open model (Llama 3/4, Mistral, Gemma, Qwen 2.5, BioBERT/ClinicalBERT-class)
   e. Hybrid: rules + LLM for minority classes, deterministic extraction + LLM fallback
   f. Extended thinking / chain-of-thought / self-consistency at inference
   g. **Agentic / multi-agent architectures** with tool use, task routing, and explicit function calls (e.g. an "extraction agent" feeding a "classification agent" feeding a "verification agent"). Multi-agent patterns for clinical Q&A, care coordination, and document interpretation have been prominent in 2025–2026 work — please include them.
   For each: cite specific papers/benchmarks, report accuracy, per-class sensitivity or F1, dataset size, compute cost if available.

2. What are the 5–10 most relevant published benchmarks or real-world deployments of LLM-based clinical text classification from 2024–2026? Please make sure to cover the following meta-benchmarks and studies I've identified, and include any others you find:
   - **BRIDGE** (arXiv 2504.19467, 2025) — benchmark covering 20 clinical applications including triage and referral, 95 LLMs evaluated across 14 specialties. What does it say about our tasks?
   - **Structured prompting triage study** (Journal of Medical Systems 2025, DOI 10.1007/s10916-025-02284-y) — 8 LLMs on 48 short clinical vignettes, 4 triage levels, structured prompting improved mean triage accuracy from 76.82% to 86.20%. Most directly comparable to our task.
   - **ICPC-2 coding benchmark** (arXiv 2507.14681, 2025) — 33 LLMs selecting International Classification of Primary Care codes, 28 models >0.8 F1, top performers GPT-4.5-preview, o3, Gemini 2.5 Pro.
   - **NHS primary care medication safety review real-world evaluation** (arXiv 2512.21127, GPT-oss-120b, Oct–Nov 2025) — 178 failures across 148 patients, **contextual reasoning failures outnumber factual errors 6:1**. What does this tell us about the dominant failure mode for primary care LLM deployment?
   - **LCD benchmark** (medRxiv 2024.03.26) — long clinical document mortality prediction on MIMIC-IV; notes that benchmark datasets targeting long clinical document classification tasks are absent.
   - **EHRNoteQA** (NeurIPS 2024 datasets track) — long-context clinical QA benchmark with 4k / 8k token levels.
   - **CLEVER** (Clinical LLM Evaluation by Expert Review) — blind randomised preference-based evaluation methodology published 2025.
   - **BPAC CS Inbox Manager** and any Rotenstein / Apathy / Harzand / Si / Gatto / Wang follow-ups published 2025–2026.

3. For safety-critical recall-optimised settings (≥95% or higher sensitivity for high-urgency classes): what techniques have achieved this in published clinical LLM work? Loss functions, calibration, post-hoc threshold tuning, abstention/referral, ensemble methods, hybrid rules+LLM, agent-based verification with a second-opinion step.

4. For the 3 document types that need full-document semantic reading (discharge summaries, specialist letters, patient messages): what's the evidence on context-window handling, long-document processing, section-attention, and chunking strategies for classification? Include findings from LCD benchmark and EHRNoteQA. What is the practical input length most models handle well vs degrade on?

5. For GP-facing or primary-care inbox or patient-portal message triage specifically: what empirical results exist (any country)? I know about Si et al. PMLR 2020, Harzand et al. NEJM AI 2024, Gatto et al. PMR-Bench arXiv 2601.13178, Apathy et al. JAMIA Open 2024, Rotenstein et al. JAMIA Open 2025, Wang et al. DSS 2022. What has been published since, and what are the current SOTA results?

6. What are the real-world performance degradation patterns for clinical LLM triage? Abdalhalim et al. 2025 reported 8–15 point sensitivity drops from validation to deployment. The NHS medication safety study found contextual reasoning failures outnumber factual errors 6:1 — is this pattern replicated elsewhere? What techniques close the gap?

7. Cost / latency / throughput benchmarks: for a workload of ~1,000–10,000 documents/day, what is the real published or practitioner-reported cost per 1k documents on (a) **Claude Haiku 4.5 / Sonnet 4.6 via AWS Bedrock NZ (ap-southeast-6)**, (b) Llama 3/4 70B on A100/H100, (c) fine-tuned small models on L40S/L4, (d) multi-agent RAG pipelines (potentially multiple model calls per document)? Cite sources. Where Bedrock NZ pricing is not yet published, use Sydney ap-southeast-2 as a proxy and flag the assumption.

8. Where are the evidence gaps for our exact setup (NZ GP inbox, ordinal 4-class urgency, ≥99% sensitivity constraint, NZ-hosted inference)? What would we have to prove ourselves?
</questions>

<constraints>
- Prioritise peer-reviewed work and credible preprints (arXiv, medRxiv) from 2024 onwards. Earlier work only if still cited as baseline.
- Cite every empirical claim with paper title, authors, venue, year, link.
- Report specific numbers — accuracy, sensitivity, F1, cost/1k, latency — not vague claims.
- Call out conflicts or disagreements between sources.
- Gather evidence first, then summarise. Do not generalise before citing sources.
- Focus on methods that can realistically run under NZ data sovereignty constraints. Flag any benchmark that depends on data or infrastructure we could not replicate.
</constraints>

<out_of_scope>
Do NOT spend research time on the following — they are already comprehensively documented in our internal reference files and duplication wastes the research budget:
- Urgency taxonomy design, 3-vs-4-vs-5 level justification, ED triage framework comparisons
- Evaluation metric choice (macro F1, QWK, PR-AUC, MCC rationale — already locked in)
- Buderer sample size, BCa bootstrap, spectrum bias, shortcut learning (already covered)
- Hicks et al. 2022 pitfalls
- TGA Class IIa classification, IMDRF GMLP, FDA Jan 2026 guidance (already covered in R2)
- NZ medico-legal case law (HDC decisions, Te Whatu Ora Transfer of Care)
- NZSSD diabetes guidelines, HISO 10071 PREDICT equations, MoH 2018 CVDRA
</out_of_scope>

<deliverable>
A structured research report with these sections:
1. Executive summary (≤ 300 words) — top 5 findings that matter for our architecture shortlist.
2. Architecture-by-architecture empirical summary — for each of the 7 approaches (zero-shot, few-shot, RAG, fine-tune, hybrid rules+LLM, extended thinking, **agentic/multi-agent**), a concise evidence table with papers, tasks, datasets, results, limitations.
3. Published clinical document classification benchmarks 2024–2026 — with explicit coverage of BRIDGE, JMS structured-prompting triage study, ICPC-2 coding benchmark, NHS medication safety real-world study, LCD, EHRNoteQA, CLEVER.
4. Recall-optimisation techniques for safety-critical classification — what achieves ≥95% sensitivity, how.
5. Long-document / unstructured clinical text handling — what works at 8k, 32k, 128k, 200k context.
6. GP inbox and patient message specific results.
7. Real-world degradation patterns and failure modes — including contextual reasoning failures, and mitigations.
8. Cost / latency / throughput benchmarks by architecture, with Bedrock NZ pricing assumptions flagged.
9. Evidence gaps for our specific problem.
10. Full reference list with links.

Length: comprehensive. Prefer too much over too little.
</deliverable>
```

---

### R2 — NZ sovereign LLM hosting (Bedrock NZ vs Catalyst Cloud NZ) + regulatory posture + DPIA methodology

**Paste into Claude.ai with Research mode ON.**

```
<context>
I am building AI-assisted clinical tools for NZ GPs under an MBIE New to R&D grant (24 months, 12 Mar 2026 – 11 Mar 2028). Our stated vision is "NZ-sovereign clinical AI — built and operated within NZ under Privacy Act constraints, not dependent on overseas cloud infrastructure." MBIE grant contract clause: "R&D undertaken outside New Zealand is not eligible" unless pre-approved.

Two important recent developments that frame this research:

1. **AWS Bedrock is now live in the Asia Pacific (New Zealand) Region — API name ap-southeast-6, Auckland, 3 AZs.** AWS launched the NZ Region in September 2025. Amazon Bedrock launched in ap-southeast-6 in March 2026 (about 4 weeks before this research is running). Source: aws.amazon.com/blogs/machine-learning/run-generative-ai-inference-with-amazon-bedrock-in-asia-pacific-new-zealand/. Auckland is now a source Region for AU-geographic and global cross-Region inference on Bedrock. This fundamentally changes our sovereignty options — closed-frontier models (Claude) can now plausibly run inside NZ.

2. **Catalyst Cloud (Wellington/Auckland, 100% NZ-owned, approved NZ Government cloud) offers GPU-as-a-Service** — confirmed instance types C2 (NVIDIA A100 80GB slices, 20GB VRAM per slice), C3 (NVIDIA L40S 48GB), C1A (RTX A6000 48GB). Public statements: "all customers' data stays in Aotearoa, protected by NZ laws" and "the cloud is fully managed by engineers located in New Zealand, meaning there is no jurisdictional risk caused by external or overseas engineers having access to their systems." This is the strongest-possible sovereignty posture for open-model self-hosting.

So my research question is no longer "are there any NZ-hosted options?" — it is **"of the credible NZ-hosted options that exist today (Bedrock NZ, Catalyst Cloud NZ, others I may have missed), which is the defensible sovereignty posture for identifiable NZ clinical data under the Privacy Act 2020, Health Information Privacy Code 2020, and the MBIE R&D grant contract?"**

Product context: Inbox Helper classifies incoming clinical documents into 4 urgency levels; Care Gap Finder does variable extraction + CVDRA calculation. 5 document types. Assist-only — GP decides everything. Deployment target: mid-to-large NZ GP practices (Medtech Evolution ~75% market share, Indici as the other main PMS). Scale: 300–500 synthetic docs in Sprint 2, real inbox data ~1k–10k docs/day/practice in Obj 2, ~2,500 enrolled patients per average practice.

Context I do NOT need (already researched in internal docs):
- TGA Class IIa classification for assist-only AI CDSS (confirmed)
- TGA October 2025 CDSS exemption guidance
- FDA January 2026 draft guidance on AI-enabled device software
- IMDRF GMLP 10 Guiding Principles
- Trans-Tasman Mutual Recognition Arrangement (TTMRA) general mechanics
- NZ HDC case law on test result responsibility
- Te Whatu Ora 2024 Transfer of Care guidance
</context>

<objective>
Produce an authoritative report on (1) the sovereignty posture trade-off between AWS Bedrock NZ (ap-southeast-6) and Catalyst Cloud NZ self-hosting for clinical data, (2) the current status of NZ AI-CDS regulation (Medical Products Bill status check only — not a deep dive), and (3) DPIA methodology for AI-assisted clinical decision support in NZ. These answers will drive the sovereignty and regulatory sections of the Sprint 2 literature review and the architecture shortlist.
</objective>

<questions>
1. **AWS Bedrock in Asia Pacific (New Zealand) — ap-southeast-6 (the critical question):**
   a. As of April 2026, which Anthropic Claude models are live in ap-southeast-6 natively (Sonnet 4.6, Sonnet 4.5, Haiku 4.5, Opus 4.6, Opus 4.1, Sonnet 4)? Distinguish "native in-region" vs "cross-Region inference routed through ap-southeast-6".
   b. For cross-Region inference with ap-southeast-6 as source: which target Regions are used (Sydney ap-southeast-2, Melbourne ap-southeast-4, Tokyo, Singapore)? Is there a way to pin inference to NZ only?
   c. What does AWS publish about data handling during Bedrock inference in ap-southeast-6 — ephemeral memory, zero data retention (ZDR), logging, abuse monitoring?
   d. Is Bedrock in ap-southeast-6 HIPAA-eligible? Is there a BAA offered to NZ customers? What is the legal equivalent under NZ law (the HIPC covers this, but is there a published AWS NZ-specific addendum)?
   e. Has any NZ health product or Te Whatu Ora project publicly deployed Bedrock NZ for identifiable clinical data since March 2026? Any case studies?
   f. What is the Privacy Commissioner / HINZ / Te Whatu Ora public position on AWS as a processor of NZ clinical health information? (The October 2020 Interpretation position on cross-border disclosure is the base case — is there any update post-ap-southeast-6 launch?)

2. **Catalyst Cloud NZ self-hosting assessment:**
   a. What is the full Catalyst Cloud GPU catalogue and published NZD per-hour pricing (C2 A100 slices, C3 L40S, C1A A6000)? Check the Price List page (catalystcloud.nz/pricing/price-list/) and Cost Calculator.
   b. For a production LLM inference workload of 1,000–10,000 clinical documents/day, what is the realistic GPU fleet size and monthly NZD cost on Catalyst?
   c. What open models are realistic on Catalyst's GPU options — Llama 3 8B / 70B, Llama 4, Mistral Small/Medium/Large, Qwen 2.5, Gemma 3? Which fit on A100 20GB slices vs L40S 48GB vs A6000 48GB?
   d. Published NZ health products running on Catalyst Cloud — any case studies?
   e. Security / certification status — ISO 27001, IRAP, PSR, NZISM-aligned, HIPAA equivalent?

3. **Alternative NZ-hosted options beyond Bedrock NZ and Catalyst Cloud:**
   a. CCL (Computer Concepts Limited, now merged with Revera, Spark-owned) — any GPU compute offerings for LLM workloads? Data centre locations?
   b. Datacom — GPU or managed LLM inference services in NZ?
   c. 2degrees Business, Umbrellar, Voyager, BizNet, Kordia — any relevant offerings?
   d. Is there any NZ health-specific sovereign AI cloud (analogous to UK NHS sovereign AI proposals)?
   e. Self-hosted bare-metal in an NZ colocation facility — realistic for an MBIE N2RD-funded R&D programme?

4. **Runpod and other overseas cloud positions (for completeness and grant compliance):**
   a. Runpod's NZ legal status — data residency policy for clinical data, applicable law, jurisdictional risk.
   b. Given Bedrock NZ now exists, is there any remaining case for overseas cloud during R&D? (Budget constraints, model availability, specific features.)
   c. MBIE N2RD grant compliance: the "R&D undertaken outside New Zealand is not eligible" clause — how do other grantees interpret it for cloud infrastructure? Any published MBIE / Callaghan Innovation guidance, correspondence, or case studies?

5. **NZ Privacy Act 2020 + Health Information Privacy Code 2020 for AI-CDS:**
   a. Specific obligations for AI that processes identifiable clinical data — Rule 5 storage, Rule 8 accuracy, Rule 11 disclosure, Rule 12 unique identifiers.
   b. Any Privacy Commissioner AI-specific guidance updates in 2025 or 2026 that go beyond the September 2023 "AI and the Information Privacy Principles" guidance?
   c. Te Whatu Ora / HINZ published positions on cloud hosting of NZ clinical data.
   d. Automated decision-making provisions — how does HIPC frame "assist-only" vs "automated decision"?

6. **Medical Products Bill — STATUS CHECK ONLY (not a deep dive):**
   a. Confirm the commencement expectation (reportedly around 2030) and timing of Parliamentary introduction (reportedly 2026).
   b. Confirm Cabinet July 2025 decision that SaMD including AI-for-therapeutic-purposes is in scope.
   c. Any public signals about pre-commencement transitional arrangements that would affect us in 2026–2028?
   d. No need to deep-dive the Bill content; we expect to operate under the current Medicines Act 1981 + WAND + HIPC + Privacy Act regime for our entire grant period.

7. **DPIA methodology for AI-assisted CDS in NZ:**
   a. MBIE grant Capability Development deliverable requires "DPIA methodology." What templates, frameworks, or published methodologies exist for doing a DPIA on AI-CDS in NZ specifically?
   b. NZ Privacy Commissioner DPIA guidance — is it suitable for AI-CDS or too generic? What adaptations are needed?
   c. UK ICO AI DPIA template / ISO/IEC 42001 / NIST AI RMF — are any of these acceptable bases in NZ? Pros/cons?
   d. Te Whatu Ora / NEAC 2022 health data DPIA guidance — applicable content?
   e. What should a DPIA for an assist-only AI inbox triage + care gap system specifically address that a standard PIA does not?

8. **NZ health AI precedents and sovereignty postures (brief):**
   a. Orion Health, Volpara, Medtech Global (Medtech AI), Heidi Health, Health Accelerator — what have they publicly said about infrastructure, sovereignty posture, and regulatory approach?
   b. The Heidi Health rollout to 1,000 NZ ED clinicians (Nov 2025 Government contract) — what is known about its hosting, data handling, and regulatory posture? Does it use AWS NZ?
   c. The Health NZ / Heidi security flaw reported March 2026 — what was disclosed, and what's the lesson for our design?
</questions>

<constraints>
- Cite primary sources: legislation, government guidance (MoH, Medsafe, Privacy Commissioner, MBIE, Callaghan Innovation), provider documentation (AWS, Catalyst Cloud), and published case studies.
- For provider pricing: cite the provider's public pricing page or a dated quote; flag where pricing is "contact sales".
- Distinguish clearly between "data hosted in NZ", "data processed in NZ", and "data routable through NZ via cross-Region inference". They are not the same.
- For Bedrock ap-southeast-6: be explicit about what is native vs cross-Region. Do not assume native availability of every model.
- Flag anything that is unresolved or requires direct regulator contact (Privacy Commissioner, Medsafe, Callaghan Innovation).
</constraints>

<deliverable>
A structured report with these sections:
1. Executive summary (≤ 400 words) — the recommended sovereignty posture for the Sprint 2 architecture shortlist, with a clear head-to-head on Bedrock NZ vs Catalyst Cloud NZ.
2. AWS Bedrock in ap-southeast-6 — deep dive on model availability, data handling, cross-Region behaviour, healthcare compliance, NZ case studies.
3. Catalyst Cloud NZ — deep dive on GPU catalogue, pricing, realistic production cost for our workload, open-model fit, certifications.
4. Alternative NZ-hosted options — CCL, Datacom, colocation, others.
5. Runpod and overseas cloud residual case — is there any remaining reason to use overseas cloud, and how does the grant clause constrain us?
6. NZ Privacy Act + HIPC obligations for AI-CDS — updated for 2025/2026 guidance if any.
7. Medical Products Bill — short status check (~300 words max).
8. DPIA methodology for AI-assisted CDS — recommended base template and the AI-specific extensions required.
9. NZ health AI precedents — infrastructure and sovereignty postures of Heidi, Medtech AI, Health Accelerator, Orion, Volpara.
10. Recommended sovereignty posture for NexWave — explicit recommendation (single option or hybrid) with defensibility rationale.
11. Open questions to raise directly with the Privacy Commissioner / Medsafe / Lisa Pritchard at Callaghan / AWS NZ team / Catalyst Cloud.
12. Reference list with links.
</deliverable>
```

---

### R3 — Architecture shortlist for Inbox Helper + Care Gap Finder

**Paste into Claude.ai with Research mode ON after R1 and R2 are back.** (R3 depends on their findings to ground the trade-offs.)

```
<context>
I am shortlisting 3–4 AI architectures to evaluate on synthetic data for two assist-only NZ GP tools. I have already done two earlier deep-research runs (R1 clinical LLM benchmarks and R2 NZ sovereign hosting) and will paste their findings into this run if helpful.

Product 1 — Inbox Helper: classify incoming clinical documents into 4 urgency levels (Immediate / Urgent / Routine / Information only). 5 document types: labs, radiology, discharge summaries, specialist letters, patient messages.

Key structural facts from our internal task specification:
- Labs are HL7 structured with values, flags, reference ranges → rule-based or structured extraction feasible; LLM beneficial for delta interpretation.
- Radiology reports are semi-structured with impression sections → hybrid extraction + semantic reading.
- Discharge summaries, specialist letters, patient messages are unstructured → full-document semantic reading required. "Three of five document types require semantic full-text understanding. This is the primary driver toward evaluating LLM-based architectures."
- Targets: ≥99% sensitivity Immediate and Urgent classes (ACS-COT <5% undertriage standard); ≥90% weighted accuracy; macro F1 ≥0.80; QWK reported; PR-AUC per high-urgency class.
- Recall-optimised: over-triage acceptable, under-triage is not.

Product 2 — Care Gap Finder: 3 functionally distinct sub-tasks.
- Sub-task A: Gap detection (deterministic rules engine against structured PMS fields — diagnosis codes, lab dates, demographic fields).
- Sub-task B: Variable extraction (15 PREDICT equation variables from PMS records; most structured, 3 commonly missing / under-coded).
- Sub-task C: CVDRA calculation (Python implementation of HISO 10071:2025 PREDICT equations — deterministic given complete inputs; ≥95% accuracy target).
- Primary R&D uncertainty is in Sub-task B (extraction on real PMS data with missing / inconsistently coded fields).

Constraints:
- **NZ data sovereignty** — two credible NZ-hosted paths as of April 2026: (i) AWS Bedrock in ap-southeast-6 (Auckland, launched March 2026) for Claude Haiku 4.5 / Sonnet 4.6 / Opus 4.6, and (ii) Catalyst Cloud NZ GPU-as-a-Service (A100 80GB slices, L40S 48GB, RTX A6000 48GB) for self-hosted open models. **The shortlist must include at least one candidate on each NZ-hosted path** so we can evaluate the managed-closed-model vs self-hosted-open-model trade-off directly.
- PMS integration: Medtech Evolution (Medtech ALEX FHIR API — no NZ competitor currently uses this for AI inbox triage) and Indici.
- Budget: NZD $177k for the entire 6-month Objective 1 (compute + labour). Model inference must be cost-aware.
- Scale: 300–500 synthetic documents in Sprint 2; real inbox data ~1,000–10,000 documents/day/practice in Obj 2; ~2,500 enrolled patients per average practice.
- Competitor differentiator: AI reasoning + clinical accuracy + ALEX integration (the shortlist must preserve this — ruling out rule-only approaches like Health Accelerator RPA and BPAC CS Inbox Manager).
- Dominant real-world failure mode for primary care LLMs (NHS GPT-oss-120b Oct–Nov 2025 study): **contextual reasoning failures outnumber factual errors 6:1.** Each candidate must describe how it mitigates contextual reasoning failure.
</context>

<objective>
Produce a detailed architecture shortlist document with 3–4 candidate architectures, each scored against Inbox Helper (5 doc types) and Care Gap Finder (3 sub-tasks) requirements. The shortlist must be defensible to MBIE and executable on synthetic data starting Sprint 3 (26 April).
</objective>

<questions>
1. Given the constraints above, propose **exactly 4 credible architecture candidates** for evaluation. The slate must include:
   - At least one **Bedrock-NZ-hosted closed-model candidate** using Claude Haiku 4.5 or Claude Sonnet 4.6 (or a tiered mix) in ap-southeast-6
   - At least one **Catalyst-Cloud-NZ-hosted open-model candidate** (Llama 3/4, Qwen 2.5, Mistral, or similar) fitted to the GPU shapes available (A100 80GB slice, L40S 48GB, A6000 48GB)
   - At least one **hybrid rules + LLM candidate** that makes explicit which decisions are rule-based and which are model-based
   - At least one **agentic / multi-agent candidate** with explicit tool calls (extraction agent → classifier agent → verification agent, or similar) — reflecting the 2025–2026 "fine-tune for format, RAG for knowledge, agents for workflow" pattern

   For each candidate, describe:
   a. The model(s) — specific model version, size, hosting path (Bedrock NZ ap-southeast-6 / Catalyst Cloud C2/C3/C1A / other)
   b. Overall approach (RAG / few-shot / fine-tune / hybrid rules+LLM / multi-agent / multi-stage)
   c. How it handles each of the 5 Inbox Helper document types
   d. How it handles each of the 3 Care Gap Finder sub-tasks
   e. Expected accuracy ceiling (grounded in published benchmarks from 2024–2026 — BRIDGE, JMS triage vignettes, ICPC-2 benchmark where relevant)
   f. Expected sensitivity ceiling on minority classes (Immediate, Urgent) — and the technique that drives it
   g. **Contextual reasoning failure mitigation** (the NHS GPT-oss study showed 6:1 context vs factual failures — what's this candidate's specific mitigation?)
   h. Cost per 1k documents at production scale (published or derived, with Bedrock NZ pricing assumptions flagged)
   i. Latency per document (p50, p95)
   j. Sovereignty fit (Bedrock NZ vs Catalyst Cloud NZ vs other) — and defensibility
   k. Implementation effort in engineer-weeks (rough)
   l. Key failure modes
   m. Key risks / unknowns

2. Trade-off table — side-by-side comparison on: accuracy, sensitivity ceiling, latency, cost, sovereignty fit, implementation effort, maintainability, explainability, data efficiency (how much training data needed), regulatory auditability.

3. For each candidate, specify the evaluation protocol for Sprint 3: what metrics to compute on the 300–500 synthetic items, what baselines to compare against, what success criteria would rule the candidate in or out.

4. Which candidate would you start evaluating first if time and budget were limited? Why?

5. What architectural assumptions should we validate before Sprint 3 starts? (e.g., "we assume full-document semantic reading works for discharge summaries at <10k tokens" — how to sanity-check cheaply.)

6. What architectural risks could kill the programme if discovered late? (e.g., cost blow-up at scale, sensitivity ceiling below target, LLM instability on adversarial clinical inputs, latency unworkable in GP workflow.)

7. How do we preserve the "AI reasoning + ALEX integration" differentiator in each candidate? Rule-only approaches (Health Accelerator RPA, BPAC CS) are ruled out — but hybrid rules+LLM needs to be clear about which parts are rules and which parts are reasoning.

8. Is there a credible path from the chosen architecture in Obj 1 (synthetic data) to Obj 2 (real inbox data) without re-architecture? What data or infrastructure moves must happen in between?
</questions>

<constraints>
- Ground every claim in published benchmarks or credible vendor documentation. No vendor marketing.
- Be specific on model names, versions, sizes, hosting paths, and costs.
- Do not re-derive urgency taxonomy or evaluation metrics — those are locked in.
- Do not re-litigate whether LLM is needed for document classification — the internal spec has decided semantic reading is required for 3 of 5 document types.
- Include hybrid approaches (rules + LLM) seriously. Do not dismiss them as "not reasoning enough."
- The shortlist must include at least one NZ-hostable option.
</constraints>

<out_of_scope>
Do NOT re-cover:
- Urgency taxonomy justification
- Evaluation metric selection (QWK, macro F1, PR-AUC etc. are chosen)
- TGA / IMDRF regulatory posture (already covered)
- Clinical rationale for the 4-level urgency system (already covered)
- Generic "why LLM beats rules" discussion — we've decided, proceed to candidate comparison
</out_of_scope>

<deliverable>
A structured report:
1. Executive summary (≤ 400 words) — the 3–4 shortlisted candidates and a one-line rationale per candidate.
2. Candidate 1 deep dive — sub-sections for architecture, Inbox Helper handling per doc type, Care Gap Finder handling per sub-task, cost/latency, failure modes, evaluation protocol.
3. Candidate 2 deep dive — same structure.
4. Candidate 3 deep dive — same structure.
5. Candidate 4 deep dive — same structure (if four).
6. Cross-candidate trade-off table.
7. Recommended first candidate to evaluate, with rationale.
8. Sprint 3 evaluation plan — per-candidate metrics, baselines, timeline, ruling criteria.
9. Assumptions to validate before Sprint 3 (cheap sanity checks).
10. Risks and unknowns.
11. Reference list with links.
</deliverable>
```

---

### R4 — Care Gap Finder sub-task architectures (rules engine + variable extraction)

**Paste into Claude.ai with Research mode ON.**

```
<context>
I am designing the Care Gap Finder for NZ GPs. It has three sub-tasks with very different architectures. I need published evidence and practitioner patterns to design each correctly.

Sub-task A — Gap detection (deterministic rules engine):
- Input: structured PMS data (diagnosis codes, lab dates, demographics, medications).
- Logic: interval-based monitoring rules. Examples: HbA1c every 3/6/12 months depending on control status; BP monitoring every 3 months if above target; CVDRA every 10/5/2/1 years by prior risk score; eGFR/uACR matrix (KDIGO 2013). Full logic already specified in our internal task spec.
- Output: list of patients with overdue checks, per rule.
- Expected architecture: Python rules engine, decision tables, or DMN.

Sub-task B — Variable extraction from clinical documents and structured fields:
- Input: Medtech / Indici records — mix of structured fields (Read/SNOMED codes, lab values, vital signs) and unstructured free text (problem list notes, letter bodies, consultation notes).
- Variables needed for PREDICT CVDRA: age, sex, ethnicity, diabetes status, smoking status, systolic BP, TC:HDL ratio, antihypertensive therapy, statin therapy, antiplatelet/anticoagulant therapy, family history of premature CVD, AF (ECG-confirmed), NZDep (SES), eGFR, ACR.
- Expected difficulty: 15 variables total; ~12 are in structured PMS fields (Read v2 / SNOMED CT / HL7 lab); 3 (family history, NZDep, AF in some records) are commonly missing, under-coded, or in free text.
- Architecture uncertainty is highest here.

Sub-task C — CVDRA calculation (deterministic):
- Implement NZ Primary Prevention Equations (PREDICT v.2019) per HISO 10071:2025.
- Deterministic Python given complete variables.
- ≥95% accuracy target — this is the grant deliverable.
- Handling missing variables: imputation, prompt for GP input, or suppress calculation.

Structural context:
- NZ PMS platforms: Medtech Evolution (~75% market, Read v2 codes, ALEX FHIR API published), Indici (newer, FHIR-native).
- Care Gap Finder operates on the enrolled patient list (~2,500 patients per average practice), not on the inbox.
- Recall-optimised: false negative (missing a gap) is unacceptable; false positive (flagging a patient who turned out not to need action) costs a phone call.
- Assist-only: practice decides who to contact.
</context>

<objective>
Produce a detailed design reference for each of the three Care Gap Finder sub-tasks, grounded in published work and credible practitioner patterns, so I can specify the architecture and variable extraction pipeline in Sprint 2 and start implementation in Sprint 3.
</objective>

<questions>
1. **Rules engine design for clinical care gap detection (Sub-task A):**
   a. What rules engine frameworks are used in published clinical decision support work? DMN (Camunda, Drools), Clinical Quality Language (CQL), JSON-rules, plain Python decision trees, datalog?
   b. How do people keep rules auditable and version-controlled for clinical safety? What regulatory expectations apply?
   c. How do published systems handle interval rules (every 3 / 6 / 12 months) combined with contextual rules (escalation if HbA1c >75, suppression if active hospice)?
   d. Specific NZ or AU published examples: BPAC Clinical Solutions inbox manager, Health Accelerator RPA, Te Whatu Ora clinical dashboards, DHB care coordination systems. What do they use?
   e. How should the rules be structured so a GP or clinical reviewer can audit them without reading code?

2. **Variable extraction from NZ PMS data (Sub-task B):**
   a. For the 12 structured variables: what are the common pitfalls when extracting from Medtech Evolution and Indici? (Read v2 to SNOMED CT mapping, lab unit variation, historical vs current values, multiple entries per episode.)
   b. For the 3 commonly missing variables (family history, NZDep, AF): what published techniques exist for deriving, inferring, or flagging-as-missing?
   c. NZDep is a census-based deprivation score derived from address. Is it realistically available in NZ PMS records, or does it need to be derived from patient address + NZ Census data? Any published NZ work on this?
   d. Family history of premature CVD: where does this live in NZ PMS records? Is there a standard coding scheme? What is the typical completeness rate?
   e. AF confirmation: ECG-confirmed vs ICD-coded vs self-reported — how do published systems distinguish?
   f. For free-text extraction (when fields are missing): what LLM-based extraction approaches perform best on clinical free text? Function calling, JSON mode, constrained decoding, fine-tuned extractor models (ClinicalBERT, BioBERT, MedCAT, scispaCy)?
   g. Hallucination control for LLM-based variable extraction feeding a safety-critical calculation — what techniques work?

3. **Missing data handling strategy:**
   a. When to impute vs suppress calculation vs prompt GP for input?
   b. Impact of imputation on downstream PREDICT equation accuracy — published error bounds?
   c. How do published clinical decision support systems communicate "calculation not available" to the user without creating a false-negative impression?

4. **CVDRA calculation implementation (Sub-task C):**
   a. Are there published open-source Python implementations of the NZ PREDICT v.2019 equations compliant with HISO 10071:2025?
   b. What are the edge cases that cause calculation errors (age out of equation validity range 30–74, CVD equivalents that suppress calculation, extreme values)?
   c. Validation: how would we validate our implementation against a reference? Is there a test vector set published by MoH or HISO?

5. **Integration with PMS:**
   a. Medtech Evolution: what does the ALEX FHIR API expose for patient records, labs, medications, diagnoses? Rate limits, authentication, data freshness?
   b. Indici: what are the published API capabilities for bulk patient extraction and queries?
   c. For a patient-list scan (~2,500 patients), what is the realistic API throughput and cost profile?

6. **Evaluation of the whole pipeline:**
   a. How do we evaluate end-to-end Care Gap Finder accuracy when gap detection depends on variable extraction quality? What error decomposition methods are published?
   b. How do we benchmark against a human "gold standard" annotator for gap detection?
</questions>

<constraints>
- NZ-specific where possible. NZ PMS platforms, NZ code sets, NZ guideline intervals.
- Cite published clinical decision support work, not vendor marketing.
- For Medtech ALEX and Indici APIs: cite public documentation where it exists; flag where docs are proprietary or require partnership.
- Prioritise auditable, reproducible methods over black-box approaches (MBIE requires working to be shown).
</constraints>

<out_of_scope>
Do NOT re-cover:
- The clinical logic of HbA1c / BP / CVDRA monitoring intervals (already in our internal spec, grounded in NZSSD / BPAC NZ / MoH 2018)
- PREDICT equation parameters (HISO 10071:2025 is the authoritative source)
- Patient identification by Read / SNOMED codes for diabetes, hypertension, CVD (already in our internal spec)
- General CVDRA clinical guideline discussion
</out_of_scope>

<deliverable>
A structured report:
1. Executive summary (≤ 300 words) — recommended architecture for each of the 3 sub-tasks.
2. Sub-task A design — rules engine framework choice, structure, auditability, reference examples.
3. Sub-task B design — variable extraction approach, per-variable strategy for the 15 PREDICT inputs (which are structured, which need extraction, which need derivation).
4. Handling the 3 problem variables (family history, NZDep, AF).
5. Free-text extraction techniques and hallucination control.
6. Missing data handling strategy.
7. Sub-task C — PREDICT v.2019 implementation sources, edge cases, validation.
8. PMS integration — Medtech ALEX and Indici API capabilities and limits.
9. End-to-end evaluation protocol.
10. Reference list with links.
</deliverable>
```

---

### R5 — Synthetic NZ GP inbox dataset generation protocol

**Paste into Claude.ai with Research mode ON. IMPORTANT: defer this until GP clinical review feedback is in (Sprint 1 task rd-20260405-001, due 20 Apr), since every item in the synthetic dataset encodes the urgency taxonomy.**

```
<context>
I am designing and generating a synthetic dataset of 300–500 NZ GP inbox items to evaluate AI architecture candidates for the Inbox Helper (Sprint 2 deliverable, due 25 April 2026). Real GP inbox data arrives in Objective 2 (from May onwards); for Objective 1 we can only use synthetic data.

Target stratification from our internal spec:
- 5 document types: lab results, radiology reports, discharge summaries, specialist letters, patient messages
- 4 urgency levels: Immediate, Urgent, Routine, Information only
- Target: ~100–150 items per urgency class per document type (stratified enriched set of ~1,500 total is the eventual goal; we will start with 300–500 in Sprint 2)
- Plus a natural-prevalence holdout of 300–500 items for calibration and PPV/NPV
- Test set must include borderline and ambiguous cases — evaluating only on clear-cut examples will inflate performance

Key realism constraints from the spec:
- Labs are HL7-structured; values, flags, reference ranges available as discrete fields
- Radiology reports are semi-structured with impression sections; templates vary by radiologist and institution
- Discharge summaries have no consistent "message for GP" section; action items appear anywhere in body/plan/narrative
- Specialist letters have no section markers; critical findings can appear anywhere, in any phrasing
- Patient messages are unstructured; prevalence of Immediate and Urgent messages is low (NZ portals directed away from urgent issues), but Immediate/Urgent must not be missed when they occur
- NZ-specific: NZSSD/BPAC guidelines, RCPA/AACB lab critical thresholds, RCR radiology alert framework, NZ ethnicity distribution, Māori/Pacific patient representation
- Privacy-safe: no real names, NHIs, addresses, or identifiable details; content realistic enough to transfer to real data but obviously synthetic

Labelling:
- Ground truth urgency label per item, per the taxonomy
- Rationale per item (what triggered the classification)
- Boundary case flag (when the item could reasonably be classified at a higher or lower level)
- Document type label

Team: 1 GP (Ryo, 30 hrs/week weekends) + 1 programme manager (Ting, 40 hrs/week weekdays). 2-week sprint window.

**Important failure-mode constraint for dataset design:** the most recent real-world primary care LLM deployment study I am aware of (NHS primary care medication safety review, GPT-oss-120b, Oct–Nov 2025, arXiv 2512.21127) found that **contextual reasoning failures outnumber factual errors 6:1** — i.e. the models got facts right but mis-applied them in context (wrong patient, wrong timeline, wrong comorbidity, wrong urgency in context). Our synthetic dataset must **specifically stress-test contextual reasoning**, not just factual recall. This is a key design constraint on the synthetic item mix.
</context>

<objective>
Produce a detailed, executable protocol for generating and labelling the 300–500 item synthetic NZ GP inbox dataset in Sprint 2. I need it concrete enough that I can start generation on 13 April and have a labelled dataset by 25 April.
</objective>

<questions>
1. **Published synthetic clinical dataset efforts:** What has been done in this space 2022–2026? Synthea for structured records; MIMIC-derived synthetic work; UK NHS synthetic releases (e.g. ONS, CPRD); MedSynD; any clinical NLP community shared tasks? Include the 2025 Frontiers study on **LLM-generated synthetic tabular clinical data with GPT-4o zero-shot** (reported 92.31% statistical parameter similarity to real-world perioperative data) and any similar feasibility studies. For each: approach, scale, evaluation of realism, lessons learned. What transferred from synthetic to real, and what didn't?

2. **LLM-based synthetic clinical text generation (the likely approach for us):**
   a. Prompt patterns that produce realistic clinical documents — few-shot with real exemplars, chain-of-thought, role prompting.
   b. How do you prevent the generating LLM from leaking shortcuts (e.g. always using "URGENT" in the title for urgent cases) that the classifier LLM will exploit?
   c. Techniques to force stylistic variation (phrasing, abbreviations, hedging, document structure) so the dataset isn't homogeneous.
   d. Generation with intentional ambiguity — how to create borderline cases that stress-test the classifier.
   e. How to avoid the generating LLM copying from its training data (which might include real clinical text)?

3. **Stratified sampling for a recall-optimised ordinal classification dataset:**
   a. Target distribution — stratified enriched (100–150 per class per doc type) vs natural prevalence, and the justification.
   b. How to ensure minority class (Immediate) is adequately represented without distorting the classifier's learned prior.
   c. Spectrum requirement — proportion of clear-cut vs borderline cases per class.
   d. Document type balance — patient messages rarely contain urgent items, but we still need synthetic urgent examples. How is this done in published work?
   e. **Contextual reasoning stress-test items** — specifically, items where the raw facts look benign but context escalates urgency (e.g. recent discharge, comorbidity, medication interaction, timeline drift). What proportion of the dataset should be contextual-reasoning-stress items to mirror the NHS 6:1 failure pattern?

4. **Labelling protocol:**
   a. Single annotator vs multiple annotators — when is single acceptable? (We have one GP, 30 hrs/week weekends.)
   b. Inter-rater reliability targets (Cohen's kappa, weighted kappa) for ordinal urgency labels — published benchmarks.
   c. Adjudication protocol for disagreements.
   d. For a 300–500 item set with a single GP annotator, what time budget per item is realistic (1 min? 3 min? 5 min?) and what QA process keeps label drift low?
   e. How are borderline cases flagged for future review?

5. **Privacy-safe generation techniques:**
   a. Obviously synthetic identifiers — name patterns, NHI patterns, address patterns that cannot match real patients.
   b. Avoiding real lab value ranges that would uniquely identify a real case.
   c. Avoiding real place names, real GP names, real specialist names.
   d. Published guidance on "obviously synthetic" standards for NZ clinical data.
   e. Does NZ Privacy Commissioner or Te Whatu Ora publish any synthetic-data guidance relevant to clinical AI training?

6. **NZ clinical realism:**
   a. NZ lab report format — HL7 ORU^R01, NZ reference range conventions, NZ-specific tests (e.g. HbA1c in mmol/mol).
   b. NZ discharge summary format — DHB conventions, eDischarge, Auckland DHB vs Waikato DHB variation.
   c. NZ specialist letter format — RANZCR radiology, RACP medical, RACS surgical letter conventions.
   d. NZ patient portal message format — MyIndici, ManageMyHealth styles.
   e. Ethnicity distribution in the synthetic dataset — should it match NZ 2023 Census (European ~70%, Māori ~17%, Pacific ~8%, Asian ~15%)? What is best practice for representation of minority groups in clinical AI datasets?

7. **Quality evaluation of the synthetic dataset itself:**
   a. Sanity checks — consistency of labels vs content, style variation metrics, lexical diversity.
   b. Human audit protocols — what proportion of the dataset should be audited before release for classifier training?
   c. Realism evaluation against real data (once real data is available in Obj 2) — what methods are published?

8. **Failure modes of synthetic clinical datasets:**
   a. Where do synthetic datasets mislead architecture decisions?
   b. How much does synthetic-to-real transfer gap typically degrade performance?
   c. Published examples of synthetic-trained or synthetic-evaluated models that failed in deployment.

9. **Executable protocol for 2-week sprint, 300–500 items, 1.5 FTE:**
   a. Day-by-day realistic schedule.
   b. Tool choices (which model to generate with, how to store, how to label).
   c. QA gates that prevent the dataset being garbage before architecture evaluation.
</questions>

<constraints>
- Cite published synthetic clinical dataset work, not vendor marketing.
- Prioritise NZ clinical conventions for realism.
- Call out any technique that depends on data we cannot realistically get (e.g. access to real de-identified NZ discharge summaries for exemplars).
- Be specific on effort estimates — hours per item, not vague categories.
</constraints>

<out_of_scope>
Do NOT re-cover:
- Urgency taxonomy (locked — 4 levels)
- Per-document-type classification criteria (already in internal spec)
- Evaluation metrics (locked — macro F1, QWK, per-class sensitivity, PR-AUC, BCa bootstrap)
- Sample size justification (Buderer already applied, targets set)
- RCPA/AACB lab thresholds, RCR radiology alerts, NZSSD diabetes guidelines
</out_of_scope>

<deliverable>
A structured report:
1. Executive summary (≤ 300 words) — recommended end-to-end protocol.
2. Published synthetic clinical dataset work relevant to our task.
3. LLM-based generation techniques — prompt patterns, shortcut prevention, ambiguity injection.
4. Stratification protocol.
5. Labelling protocol with IRA targets and adjudication.
6. Privacy-safe generation techniques for NZ clinical data.
7. NZ clinical realism by document type (lab, radiology, discharge, specialist letter, patient message).
8. Quality evaluation of the synthetic dataset.
9. Failure modes and mitigations.
10. Executable 2-week protocol — day-by-day plan, tools, QA gates.
11. Reference list with links.
</deliverable>
```

---

### R6 — Medtech / Indici / ALEX API + NZ FHIR/HL7 + code sets + field mapping

**Paste into Claude.ai with Research mode ON.**

```
<context>
I am specifying data requirements for two NZ GP AI products (Inbox Helper and Care Gap Finder) that integrate with the two dominant NZ GP practice management systems:
- Medtech Evolution (Medtech Global; ~75% market share in NZ general practice; ALEX FHIR API published; Read v2 codes native)
- Indici (Valentia Technologies; newer; FHIR-native)

Strategic opening we want to validate: our internal competitor tracking notes that "nobody is using the ALEX FHIR API for AI inbox triage yet" — every current competitor is either RPA-based (Health Accelerator), screen-scraping (Inbox Magic), native first-party (Medtech AI), or rule-based without API (BPAC CS). ALEX is NexWave's structural opening. I need to know what ALEX actually exposes, what the limits are, and whether it's sufficient for our use cases.

Variables of interest:
- For Inbox Helper: incoming clinical documents (HL7 ORU for labs, MDM for documents, REF for referrals), plus patient context (demographics, diagnosis list, medication list) when available.
- For Care Gap Finder: enrolled patient list (~2,500 per average practice), structured diagnosis codes (Read v2 / SNOMED CT), lab results (HbA1c, lipids, eGFR, ACR, LFTs), vital signs (BP, weight, smoking status), medications, ethnicity (HISO 10001), family history (if available), NZDep (if available), plus 15 PREDICT equation inputs.

Data I do NOT need researched (already covered in our internal docs):
- NZ clinical guideline intervals for care gaps (NZSSD, BPAC NZ, MoH 2018)
- PREDICT equation parameters (HISO 10071:2025)
- Urgency taxonomy or classification criteria
- Competitor product capabilities (already tracked)
</context>

<objective>
Produce a comprehensive data requirements reference for Sprint 2 deliverable rd-20260329-011 "Data requirements documented." It must cover what data is available from Medtech (especially ALEX FHIR API) and Indici sandboxes, what NZ clinical data standards apply, and a variable-by-variable mapping to sources. This is the foundation for architecture evaluation and for conversations with Medtech and Indici integration teams.
</objective>

<questions>
1. **Medtech Evolution / ALEX FHIR API:**
   a. What is the ALEX FHIR API? When was it launched? Who can access it? What are the published endpoints?
   b. What FHIR resources does ALEX expose (Patient, Observation, Condition, Encounter, DiagnosticReport, MedicationRequest, Organization, Practitioner, DocumentReference)?
   c. What are the authentication, rate limiting, and sandbox access paths? Is there a developer portal?
   d. What is known to be missing or limited in ALEX compared to raw database access?
   e. Has Medtech published a data dictionary or FHIR profile for ALEX?
   f. Any published NZ case studies of products using ALEX?
   g. Historical context — what came before ALEX (MT32 API, Medtech32 database extracts, HL7 interfaces)? Which patterns still work?

2. **Indici (Valentia Technologies):**
   a. What APIs does Indici publish? FHIR-native or proprietary?
   b. Sandbox availability, developer portal, documentation.
   c. Strengths and gaps compared to Medtech ALEX.
   d. Any published NZ case studies.

3. **HL7 v2 in NZ primary care:**
   a. Which HL7 v2 message types are dominant for incoming clinical documents — ORU^R01 (lab results), MDM^T02 (clinical documents), REF^I12 (referrals), ADT^A01 (admit), ORM (orders)?
   b. NZ Z-segments and local customisations — what are the common ones?
   c. NZ lab providers (Labtests, LabPLUS, Awanui Labs, Medlab South, SCL, Pathlab) — their HL7 conventions, differences, consistency.
   d. NZ DHB / Te Whatu Ora eDischarge formats — is this HL7 CDA, FHIR, or PDF-over-HL7?

4. **FHIR AU/NZ profile status:**
   a. HL7 New Zealand FHIR profiles (if any) — what exists, what is in draft.
   b. AU Core FHIR profiles — do they apply in NZ?
   c. HISO FHIR work — any published NZ profiles for primary care?
   d. For Patient, Observation (lab), Observation (vital), Condition, DiagnosticReport, MedicationRequest, Encounter — what are the current NZ conventions for required fields and code system bindings?

5. **NZ clinical code sets:**
   a. SNOMED CT NZ Edition — what is the scope, release cadence, availability, licensing?
   b. Read v2 — legacy but still dominant in Medtech. Mapping to SNOMED CT status.
   c. NZULM (NZ Universal List of Medicines) — authoritative medicines code set.
   d. HISO 10001 ethnicity codes — 2017 standard.
   e. LOINC — for labs. NZ adoption status.
   f. ICD-10 — hospital coding, not used in GP problem lists.
   g. For each variable we care about: which code set is authoritative?

6. **Document arrival patterns in a NZ GP inbox:**
   a. What proportion of lab results arrive as structured HL7 ORU vs scanned PDF vs other?
   b. What proportion of radiology reports arrive as structured vs free text?
   c. Discharge summaries — what is the typical format in NZ (CDA, PDF, HL7 MDM, plain text in HL7)?
   d. Specialist letters — same question.
   e. Patient messages — volume per practice per day, typical content.

7. **Variable-by-variable mapping for Care Gap Finder (15 PREDICT inputs + care gap triggers):**
   For each variable, document: (source field in Medtech / Indici / ALEX, structured vs free-text, typical completeness rate in NZ GP records, known pitfalls).
   Variables: age, sex, ethnicity (HISO 10001), diabetes status (Read C10F / SNOMED), smoking status, systolic BP, diastolic BP, TC, HDL, TC:HDL ratio, antihypertensive therapy, statin therapy, antiplatelet/anticoagulant therapy, family history of premature CVD, AF (ECG-confirmed), NZDep score, eGFR, ACR, HbA1c, weight/BMI, foot exam (diabetes), retinal screening.

8. **Data volume estimates:**
   a. Average NZ GP practice: enrolled population (~2,500), documents/day/inbox, tests/day/patient, patient encounters/day.
   b. Realistic API throughput required for (i) inbox triage in near-real-time, (ii) weekly full patient-list scan.
   c. Cost implications at these volumes.

9. **Sovereignty and compliance:**
   a. Where does data physically reside when accessed via ALEX? Medtech's hosting location?
   b. When ALEX returns data to our AI application, where can we process it?
   c. Privacy Act 2020 and HIPC 2020 implications for this data flow.
   d. Medtech's published requirements for third-party applications using ALEX — certification, data handling, audit.
</questions>

<constraints>
- NZ-specific. Not generic HL7/FHIR tutorials.
- Cite Medtech and Valentia documentation where public; flag where under NDA or partnership-gated.
- Ground volume estimates in NZ primary-care benchmarks (RNZCGP, Te Whatu Ora, GPNZ, published research).
- Flag data that is realistically unavailable so we can design around it.
- Prefer official docs and published NZ case studies over generic commentary.
</constraints>

<deliverable>
A structured report:
1. Executive summary (≤ 300 words) — top-line data availability picture and the ALEX API opportunity assessment.
2. Medtech ALEX FHIR API — deep dive with endpoints, resources, auth, limits, developer portal, published case studies.
3. Indici APIs — deep dive with same structure.
4. HL7 v2 in NZ primary care — message types, Z-segments, lab provider conventions, DHB eDischarge formats.
5. FHIR AU/NZ profile status.
6. NZ clinical code sets reference.
7. Document arrival patterns — structured vs unstructured mix per document type.
8. Variable-by-variable mapping table — one row per variable, columns for Medtech source, Indici source, code system, completeness, pitfalls.
9. Data volume estimates — per practice, per scan, per day.
10. Sovereignty and compliance for ALEX / Indici data flows.
11. Gaps — variables or data types that are not reliably available.
12. Reference list with links.
</deliverable>
```

---

### R7 — Open-source LLM self-hosted architecture options (models + inference engine + GPU + cloud + cost + fine-tune)

**Paste into Claude.ai with Research mode ON.**

```
<context>
I am shortlisting AI architectures for two assist-only NZ GP tools:

1. **Inbox Helper** — classifies incoming clinical documents into 4 urgency levels (Immediate / Urgent / Routine / Information only) across 5 document types: lab results, radiology reports, discharge summaries, specialist letters, patient messages. Three of the five document types (discharge summaries, specialist letters, patient messages) require full-document semantic reading. Targets: ≥99% sensitivity on Immediate and Urgent classes, ≥90% weighted accuracy, macro F1 ≥0.80.

2. **Care Gap Finder** — deterministic rules engine + LLM-based variable extraction from NZ PMS records + CVDRA calculation (≥95% accuracy on complete data). Extraction of 15 PREDICT equation variables from a mix of structured fields and free text.

I am explicitly **open-minded about open-source LLMs on cloud GPU as a first-class option** — not a fallback to Bedrock-hosted Claude. I want a serious, evidence-based answer to the question: **"For our task, budget, sovereignty constraints, and timeline, what is the best open-source LLM + inference engine + GPU + hosting combination to shortlist alongside a Bedrock NZ Claude candidate?"**

Constraints and context:
- **NZ data sovereignty strongly preferred.** The only confirmed NZ-sovereign GPU provider is Catalyst Cloud (NZ-owned, NZ-operated, data stays in Aotearoa) with A100 80GB slices (20GB VRAM per slice), L40S 48GB full cards, and RTX A6000 48GB full cards. Other NZ cloud providers (CCL, Datacom, 2degrees, Umbrellar) may have relevant offerings — include them if you find them.
- **Overseas cloud options are allowed for R&D only if defensible**, with a clear path to NZ-sovereign at deployment. Known candidates: Runpod Secure Cloud (SOC 2, HIPAA eligibility, ~$2.69/hr H100), Modal (Series B Sep 2025, IaC, 2–4s cold starts), Lambda Labs (A100 ~$1.10/hr, on-demand VMs only since Sep 2025), CoreWeave, Together AI (API-only access to open models), Fireworks AI (API-only). Note: "serverless platforms share infrastructure across customers... creates audit problems for healthcare" — dedicated-tenancy or self-hosted required for identifiable clinical data.
- **Budget:** NZD $177k for the entire 6-month Objective 1 (compute + labour for 2 people). Inference cost must be sustainable at scale — target 1,000–10,000 documents/day per practice.
- **Training data budget:** 300–500 synthetic items in Sprint 2, potentially 1,500 stratified items by end of Sprint 4. Real NZ GP inbox data (thousands/day) in Objective 2. This is a very small fine-tuning budget — which techniques work at this scale?
- **Scale target:** ~2,500 enrolled patients per average NZ GP practice; inbox volume ~1,000–10,000 docs/day at full deployment per practice.
- **Assist-only.** Never autonomous clinical decisions. TGA Class IIa under international framework.
- **Recall-optimised** for Immediate/Urgent classes. Over-triage acceptable; under-triage not.
- **The NHS GPT-oss-120b primary care medication review study (arXiv 2512.21127, Oct–Nov 2025)** found contextual reasoning failures outnumber factual errors 6:1. This is directly relevant because GPT-oss-120b is one of the open models we're considering. Please dig into that paper.

Context I do NOT need (covered elsewhere):
- Urgency taxonomy, clinical guideline intervals, evaluation metric choice (already locked in internal specs).
- TGA / IMDRF / FDA regulatory framing (covered elsewhere).
- Medtech ALEX FHIR API details (covered in R6).
- Synthetic dataset generation protocol (covered in R5).
- NZ regulatory sovereignty law (covered in R2).
</context>

<objective>
Produce a detailed, evidence-based report on open-source LLM self-hosted architecture options for our task, concrete enough to support shortlisting 1–2 open-source stacks as first-class candidates in the R3 architecture shortlist (alongside Bedrock NZ Claude candidates). I need specific model recommendations, specific inference engine recommendations, specific GPU-to-model-to-throughput mappings, specific NZD cost estimates at our scale, and specific fine-tuning recommendations.
</objective>

<questions>
1. **Open-source model selection for clinical document classification (primary care / GP inbox / ordinal urgency):**
   a. For 2025–2026, what are the strongest open-source model candidates for clinical document classification with full-document semantic reading? Consider at minimum: Llama 3.1 405B, Llama 3.3 70B, Llama 4 (Scout / Maverick / Behemoth / any clinical fine-tunes), Qwen 2.5 72B, Qwen 3, Mistral Large 2, Mistral Small 3, Gemma 3 27B, GPT-OSS-120B, GPT-OSS-20B, DeepSeek-R1 (full and distilled variants), DeepSeek-V3.
   b. For medical-domain-specific open models: Meditron (Llama-3-8B variant, EPFL/Yale/Meta), MedGemma (Google), PMC-LLaMA, Hippo, BioMedLM, Clinical-Camel. How do they compare to general open models fine-tuned for medical tasks on MedQA, MedMCQA, and PubMedQA? Is a clinical-domain base model still worth using in 2026, or have general models caught up?
   c. Cite findings from: Open Medical-LLM Leaderboard (Hugging Face), MedQA, MedMCQA, PubMedQA, USMLE-style benchmarks, BRIDGE (arXiv 2504.19467), ICPC-2 coding benchmark (arXiv 2507.14681), JAMA Health Forum March 2025 study (Llama 3.1 405B ~GPT-4 parity on clinical reasoning), and Harvard Medical School March 2025 news on open-source parity with proprietary LLMs on tough medical cases.
   d. For each credible candidate, report: base parameter count, context window, licence, any published clinical classification benchmark result, strengths, weaknesses, production deployment evidence.
   e. **Best 3 open-model picks for our task** — clear recommendation with rationale.

2. **Inference engine selection (2026):**
   a. Compare vLLM vs SGLang vs LMDeploy vs TensorRT-LLM on: throughput (tokens/s), latency (TTFT, TPOT), KV cache efficiency, structured output support (JSON mode, grammar constraints), multi-step program support, quantisation support (FP8, INT8, INT4, AWQ, GPTQ), batching strategy, maturity, documentation, ecosystem.
   b. TGI (Hugging Face Text Generation Inference) entered maintenance mode December 2025 — confirm and cite. Should be ruled out for new deployments.
   c. Benchmark references: on H100, SGLang reportedly hits ~16,200 tok/s vs vLLM ~12,500 tok/s — ~29% throughput advantage. What do peer-reviewed or reproduced benchmarks show on A100 and L40S (relevant to Catalyst Cloud)?
   d. For our task (ordinal classification + structured JSON output + optional multi-step agentic flow), which engine is the best fit? Why?
   e. Quantisation trade-offs — at INT4 AWQ, what is the accuracy degradation on MedQA / MedMCQA for 70B-class open models? Is INT8 a safer middle ground?

3. **GPU-to-model-to-throughput mapping for our production workload:**
   a. For each shortlisted open model (likely Llama 3.3 70B, Qwen 2.5 72B, GPT-OSS-120B or similar), what is the minimum viable GPU setup for production inference at 1,000–10,000 documents/day with acceptable latency (<5s p95 per document for async, <2s p95 for interactive)?
   b. Specific GPU fit: which models fit on a single A100 80GB (FP16)? Single A100 40GB? Single L40S 48GB? Single A6000 48GB? What about FP8/INT8/INT4 quantised? What requires 2× or 4× GPUs?
   c. Tensor parallelism / pipeline parallelism trade-offs for our scale (not enough volume to justify multi-node).
   d. Realistic throughput numbers on each configuration — cite benchmarks, not vendor marketing.

4. **Cloud GPU provider comparison for NZ-sovereign or defensible hosting:**
   a. **Catalyst Cloud NZ (primary NZ-sovereign option)** — full catalogue, published NZD pricing, GPU availability (A100 slices vs full cards, L40S, A6000), SLA, ISO 27001 / IRAP / HIPAA-equivalent certifications, realistic production cost for our workload (NZD/month at 1k/day, 10k/day).
   b. **Runpod Secure Cloud (US, HIPAA-eligible)** — SOC 2 Type II, HIPAA BAA availability for NZ customers?, H100 $2.69/hr, cold-start characteristics, dedicated-tenancy guarantees.
   c. **Modal (US, IaC-first)** — cold start 2–4s, $87M Series B Sep 2025, dedicated tenancy? HIPAA BAA?
   d. **Lambda Labs (US, on-demand VMs only since Sep 2025)** — A100 $1.10/hr, H100 pricing, NZ customer eligibility.
   e. **CoreWeave (US)** — enterprise GPU fleet, dedicated clusters.
   f. **Together AI / Fireworks AI (API-only)** — pricing per 1M tokens for our candidate models, enterprise/dedicated tenancy options, HIPAA BAA, NZ eligibility.
   g. **Other NZ cloud providers with GPU** — CCL, Datacom, 2degrees, Umbrellar, Voyager, BizNet, Kordia — any credible offering?
   h. **Self-hosted on colocation** (NZ data centre with our own GPU) — realistic for a 2-person $177k R&D programme? Cost of entry vs monthly opex.
   i. For each provider: a simple NZD/month cost estimate for running our shortlisted model at 1,000 docs/day and 10,000 docs/day.

5. **Fine-tuning approach for our tiny data budget:**
   a. With 300–500 labelled items in Sprint 2 (growing to ~1,500 by Sprint 4), is full fine-tuning, LoRA/QLoRA, DPO/SimPO, or in-context-learning with a few-shot retrieval bank the best approach? Cite published small-data clinical fine-tuning results.
   b. What is the minimum dataset size for LoRA / QLoRA on a 70B base to beat zero-shot on clinical classification? Cite examples.
   c. Prompt optimisation (DSPy, TextGrad, APE) vs fine-tuning at this data scale — which is more efficient for our task?
   d. Published results for **MedQA-tuned Llama 3 / Llama 3.1 / Llama 4** — does fine-tuning on broad medical data help a specific ordinal classification task, or does it hurt it?
   e. For the recall-optimised requirement (≥99% sensitivity on Immediate/Urgent): what loss functions, calibration, threshold tuning, or abstention techniques are published for small-data fine-tunes?

6. **Cost modelling — head-to-head vs Bedrock NZ Claude:**
   a. At 1,000 documents/day: what is the monthly NZD cost of our best open-source stack (model + inference engine + cloud GPU) vs Claude Haiku 4.5 via Bedrock in ap-southeast-6?
   b. At 10,000 documents/day: same comparison.
   c. Cross-over point — at what volume does open-source self-hosted become cheaper than Bedrock API?
   d. What does the comparison look like if we include GPU idle time (we need 24×7 availability for inbox triage)?
   e. Hidden costs — DevOps labour, monitoring, model updates, quantisation re-runs, security patching, failover infrastructure.

7. **Production operational considerations:**
   a. Model updates — how often are open models superseded, and what is the practical upgrade path for a production clinical system?
   b. Drift detection and monitoring at small-deployment scale.
   c. Disaster recovery and failover for a single-provider NZ-sovereign deployment (Catalyst Cloud single-provider risk).
   d. Audit trail and reproducibility — deterministic inference, seed control, version pinning.
   e. Clinical-grade logging of prompts and completions for DPIA and post-market surveillance.

8. **Failure modes specific to open-source self-hosted vs API-hosted:**
   a. The NHS GPT-oss-120b study found contextual reasoning failures 6:1 vs factual errors — is this pattern worse or better for open models vs closed models at similar size?
   b. Published quality regressions when quantising open models for production — what's the real accuracy cost?
   c. What does the production failure-rate literature say about self-hosted vs API-hosted LLMs for clinical tasks?

9. **Recommended open-source stack(s) for R3 shortlist:**
   a. Based on all the above, recommend **1 or 2 complete open-source stacks** (model + inference engine + GPU + cloud provider) for inclusion in the R3 architecture shortlist as first-class candidates.
   b. For each, state: expected accuracy ceiling, sensitivity ceiling on minority classes, cost at 1k/day and 10k/day, sovereignty posture, implementation effort in engineer-weeks, key risks.
   c. Explicitly compare the recommended open-source stack(s) to a Bedrock NZ Claude stack — which is the stronger option, and on what axis?
</questions>

<constraints>
- Cite published benchmarks, peer-reviewed papers, credible preprints (arXiv, medRxiv, bioRxiv), and official provider documentation. No vendor marketing as a primary source.
- Be specific: model versions, parameter counts, context windows, quantisation format, GPU SKU, engine version, NZD cost at stated volumes.
- Distinguish strongly between "can run" (fits in VRAM) and "can run well in production" (acceptable latency, throughput, stability).
- Distinguish "NZ-sovereign" (NZ-owned, NZ-operated, NZ data centre) from "NZ-hosted" (any provider running in NZ) from "NZ-routable" (cross-Region inference through NZ).
- Where benchmarks are not directly available for our specific task, extrapolate cautiously and state the assumption.
- Flag provider pricing that is "contact sales" — we need defensible cost numbers for MBIE.
- Do not duplicate R1 (clinical benchmarks) or R2 (NZ sovereignty policy); cross-reference them instead.
</constraints>

<out_of_scope>
Do NOT re-cover:
- Urgency taxonomy justification (locked)
- Evaluation metric choice (locked)
- TGA / IMDRF / FDA regulatory framing (covered elsewhere)
- NZ clinical guidelines (NZSSD, BPAC NZ, HISO 10071, MoH 2018)
- NZ Privacy Act / HIPC legal analysis (covered in R2)
- Medtech ALEX / Indici FHIR API details (covered in R6)
- Synthetic dataset generation protocol (covered in R5)
- Claude model benchmarks and Claude-specific cost (covered in R1 and R3; compare *to* Claude but do not deep-dive Claude)
</out_of_scope>

<deliverable>
A structured research report with these sections:
1. Executive summary (≤ 400 words) — the recommended open-source stack(s) for the R3 shortlist, with one-line rationale per recommendation.
2. Open-source model candidates — comparative evidence table: model, size, context, licence, clinical benchmark results, cost/1M tokens equivalent, best use case.
3. Inference engine comparison — vLLM vs SGLang vs LMDeploy vs TensorRT-LLM, with specific recommendation for our task.
4. GPU-to-model fit — which model runs on which GPU, at what precision, with what throughput.
5. Cloud GPU provider comparison — with NZD cost at 1k/day and 10k/day for the recommended stack.
6. Fine-tuning approach for small data — concrete recommendation.
7. Cost modelling — head-to-head open-source stack vs Bedrock NZ Claude stack at 1k/day and 10k/day.
8. Production operational considerations — upgrades, monitoring, failover, audit.
9. Failure modes specific to self-hosted open-source vs API-hosted closed.
10. Recommended open-source stack(s) for R3 shortlist — complete specification ready to paste into R3.
11. Open questions to resolve before committing (cheap sanity checks for Sprint 3).
12. Reference list with links.

Length: comprehensive. Prefer too much over too little.
</deliverable>
```

---

## Verification — how to check this plan worked end-to-end

After execution, Sprint 2 should produce the following artefacts, all filed in `context/nexwave-rd-context/`:

1. **6 research reports** saved verbatim from Claude.ai:
   - `research-r1-llm-architecture-benchmarks.md`
   - `research-r2-nz-sovereign-hosting-regulatory.md`
   - `research-r3-architecture-shortlist.md`
   - `research-r4-care-gap-finder-subtasks.md`
   - `research-r5-synthetic-data-protocol.md`
   - `research-r6-data-standards-pms-integration.md`

2. **4 synthesised deliverable documents:**
   - `sprint-2-literature-review.md` — deliverable for rd-20260329-003 (from R1 + R2, cross-referenced to existing `Urgency classification for GP inbox triage.md` and `Evaluation metrics for ordinal clinical AI triage classification.md`)
   - `sprint-2-architecture-shortlist.md` — deliverable for rd-20260329-010 (from R3 + R4, with 3–4 candidates scored against the Inbox Helper + Care Gap Finder requirements)
   - `sprint-2-data-requirements.md` — deliverable for rd-20260329-011 (from R6 + R4, with field mapping table)
   - `sprint-2-synthetic-dataset-schema.md` — deliverable for rd-20260329-022 (from R5, with 2-week generation protocol)

3. **Updated task files** — `rd-20260329-003.md`, `-006.md`, `-010.md`, `-011.md`, `-022.md`, `-023.md` each get a "Progress" section with a wikilink to the deliverable and a short outcome summary.

4. **Dashboard update** — weekly progress log entries in `dashboards/nexwave-rd.md` for Week of 13 Apr and Week of 20 Apr.

**Verification steps:**
- Open `sprints/active/2026-04-rd-sprint-2.md` — the Dataviewjs table should show the 7 tasks with updated statuses; research-track tasks (003, 006, 010, 011, 022) should be `in-progress` or `done`.
- Open `dashboards/nexwave-rd.md` — Sprint 2 should appear in the Sprints Dataviewjs table (auto-queried); the weekly progress log should show Sprint 2 entries.
- Open each of the 4 Sprint 2 deliverable files — each should be self-contained, cite research reports by filename, and be ready to attach to the MBIE Q1 progress report (due 31 May).
- The architecture shortlist (deliverable #3) should be specific enough that Sprint 3 (`2026-05-rd-sprint-1`, 26 Apr – 9 May) can start evaluating candidates on the synthetic dataset on day 1.
- Open `context/nexwave-rd-context/` — the 6 research reports should live alongside the existing `inbox-helper-task-spec.md` and `care-gap-finder-task-spec.md`, forming a coherent evidence package for Goal B (Architecture Decision Made and Documented, due end April).

**Quality gate before sending Q1 report to MBIE (31 May):**
- Architecture shortlist identifies at least one NZ-hostable candidate.
- Data requirements document cites ALEX FHIR API capability (or explicitly flags that we're waiting on Medtech sandbox access).
- DPIA methodology is referenced (Capability Development deliverable, due by Sep 2026 but foundation laid in Sprint 2).
- Every empirical claim is sourced.

---

## Critical files for execution

### Files the new session will read

**Existing context (do NOT duplicate this research):**
- `/home/user/obsidian/context/nexwave-rd-context/inbox-helper-task-spec.md` — Inbox Helper task spec (Step 1 deliverable, final)
- `/home/user/obsidian/context/nexwave-rd-context/care-gap-finder-task-spec.md` — Care Gap Finder task spec (Step 1 deliverable, final)
- `/home/user/obsidian/context/nexwave-rd-context/Urgency classification for GP inbox triage.md` — existing literature review on urgency frameworks
- `/home/user/obsidian/context/nexwave-rd-context/Evaluation metrics for ordinal clinical AI triage classification.md` — existing eval metrics research
- `/home/user/obsidian/context/nexwave-rd-context/Inbox Management — Competitor Tracker.md` — competitor landscape
- `/home/user/obsidian/context/nexwave-rd-context/nz-diabetes-monitoring.md`, `nz-cardiovascular-risk-assessment.md`, `nz-hypertension-monitoring.md` — NZ clinical guidelines
- `/home/user/obsidian/context/nexwave-rd-context/manual-care-gap-monitoring.md` — current NZ workflow context
- `/home/user/obsidian/projects/nexwave-rd-obj-1.md` — Objective 1 spec, 5-step roadmap, Goal B deadline
- `/home/user/obsidian/dashboards/nexwave-rd.md` — programme dashboard, compliance deadlines, open questions, weekly progress log
- `/home/user/obsidian/sprints/active/2026-04-rd-sprint-2.md` — Sprint 2 file (Dataviewjs table, no manual edits needed)

**Sprint 2 task files to update after ingestion (append Progress section):**
- `/home/user/obsidian/tasks/open/rd-20260329-003.md` (literature review)
- `/home/user/obsidian/tasks/open/rd-20260329-006.md` (LLM/RAG/fine-tuning research)
- `/home/user/obsidian/tasks/open/rd-20260329-010.md` (architecture shortlist)
- `/home/user/obsidian/tasks/open/rd-20260329-011.md` (data requirements)
- `/home/user/obsidian/tasks/open/rd-20260329-022.md` (synthetic dataset schema)
- `/home/user/obsidian/tasks/open/rd-20260329-023.md` (synthetic dataset generation)

**Files to be created in `context/nexwave-rd-context/` after ingestion:**
- 7 × `research-r[1-7]-*.md` (raw reports from Claude.ai; R7 is the open-source self-hosted LLM track)
- `sprint-2-literature-review.md`
- `sprint-2-architecture-shortlist.md`
- `sprint-2-data-requirements.md`
- `sprint-2-synthetic-dataset-schema.md`

---

## Existing patterns to reuse

- **Research outputs as context docs, not task bodies** — matches existing convention. See how `Urgency classification for GP inbox triage.md` and `Evaluation metrics for ordinal clinical AI triage classification.md` live in `context/nexwave-rd-context/`. The 6 new research reports and 4 deliverable docs follow the same pattern.
- **Task files link to context docs via wikilinks** — see how `rd-20260403-001.md` and `rd-20260403-002.md` reference `[[inbox-helper-task-spec]]` and `[[care-gap-finder-task-spec]]`. Sprint 2 tasks should do the same.
- **Dashboard Dataviewjs tables auto-query** — no manual sprint list updates needed. Updating frontmatter on task files (`status: done`) is enough to propagate to both the sprint file and the nexwave-rd dashboard.
- **No inline checkboxes anywhere** — keep all work in `tasks/open/` rows, not bullet lists in sprint or project files.
- **Weekly progress log in `dashboards/nexwave-rd.md`** — add a "Week of 13 April" and "Week of 20 April" entry on Sprint 2 close, for the MBIE audit trail.
- **R&D isolation rule** — research outputs stay in the vault. Any code implementation belongs in `C:\Users\reonz\Cursor\nexwave-rd`, not here. MBIE grant clause: R&D must be in NZ.
- **Frontmatter on new deliverable docs** — match the existing pattern used in `inbox-helper-task-spec.md`:
  ```yaml
  ---
  title: Sprint 2 — Literature Review
  type: context
  project: nexwave-rd
  objective: obj-1
  step: step-2
  created: 2026-04-25
  status: final
  ---
  ```

---

## Handoff prompt for the new Claude Code session

Once the 7 research reports are saved in `context/nexwave-rd-context/`, start a fresh session in the vault and use a prompt like this:

```
I'm executing Sprint 2 for nexwave-rd Objective 1 (2026-04-rd-sprint-2). 
Step 1 is done. Seven research reports from Claude.ai Research mode are filed in 
context/nexwave-rd-context/ (research-r1-*.md through research-r7-*.md).

Please read:
1. projects/nexwave-rd-obj-1.md (the roadmap and deliverables)
2. sprints/active/2026-04-rd-sprint-2.md (the sprint file)  
3. context/nexwave-rd-context/inbox-helper-task-spec.md (locked task spec)
4. context/nexwave-rd-context/care-gap-finder-task-spec.md (locked task spec)
5. All 7 research-r*.md files (R1 benchmarks, R2 NZ sovereignty, 
   R3 architecture shortlist, R4 Care Gap sub-tasks, R5 synthetic data, 
   R6 PMS integration, R7 open-source self-hosted LLM track)

Then produce these 4 Sprint 2 deliverables in context/nexwave-rd-context/:
- sprint-2-literature-review.md (from R1 + R2)
- sprint-2-architecture-shortlist.md (from R3 + R4 + R7, exactly 4 candidates 
  including at least one Bedrock-NZ-hosted Claude candidate AND at least one 
  open-source self-hosted candidate as EQUAL first-class options, must preserve 
  AI reasoning + ALEX differentiator)
- sprint-2-data-requirements.md (from R6 + R4, with variable mapping table)
- sprint-2-synthetic-dataset-schema.md (from R5, executable 2-week protocol, 
  includes contextual-reasoning stress items)

Then append a Progress section to each Sprint 2 task file in tasks/open/ 
(rd-20260329-003, -006, -010, -011, -022) linking to the deliverable. 
Then add a Week of 20 April entry to dashboards/nexwave-rd.md weekly progress log.

Use wikilinks for all cross-references. Follow the frontmatter pattern 
from inbox-helper-task-spec.md. Don't write code — the vault holds 
what-to-do; code belongs in the nexwave-rd repo.
```
