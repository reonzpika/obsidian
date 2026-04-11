---
title: Research R2 — NZ Sovereign LLM Hosting, Regulatory Posture, and DPIA Methodology
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-11
status: final
---

# R2 — NZ Sovereign LLM Hosting, Regulatory Posture, and DPIA Methodology

**Sprint 2 research deliverable | nexwave-rd Objective 1**
**Feeds:** rd-20260329-003 (literature review), rd-20260329-010 (architecture shortlist)
**Companion reports:** [[research-r1-llm-architecture-benchmarks]], [[research-r3-architecture-shortlist]], [[research-r7-open-source-llm-self-hosted]]

---

## 1. Executive Summary

The central question — "is there a defensible NZ-sovereign LLM hosting path for identifiable clinical data as of April 2026?" — now has two credible but imperfect answers, each with material caveats that must shape the architecture shortlist.

**Top five findings:**

1. **AWS Bedrock in ap-southeast-6 (Auckland, March 2026) is real but not natively in-region for most models.** Claude Haiku 4.5, Sonnet 4.5/4.6, Opus 4.5/4.6, and Amazon Nova 2 Lite are accessed via **AU geographic cross-Region inference profiles**, which route calls across Auckland ap-southeast-6, Sydney ap-southeast-2, and Melbourne ap-southeast-4. There is **no documented "NZ-only pinning" option**. Data stays within the ANZ geography but not necessarily within NZ on every call. Bedrock is HIPAA-eligible and a BAA is offered to NZ customers, but a BAA governs US PHI obligations, not HIPC 2020. Pricing for ap-southeast-6 is not separately listed; Sydney ap-southeast-2 is the proxy.

2. **Catalyst Cloud NZ is the only 100% NZ-sovereign GPU option with a public SKU — but the catalogue shrank just as we started.** The C2 NVIDIA A100 20GB slice (`GRID A100D-20C`) is **being retired on 31 March 2026**. The C3 NVIDIA L40S 48GB is **in Beta, Porirua-only**, and unsuitable for a production SLA. **The only safe GA choice is C1A (NVIDIA RTX A6000 48GB)** — which fortunately fits every candidate model we care about (BioClinical ModernBERT 396M, Llama 3.1 8B fine-tuned, Llama 3.3 70B at Q4 quantisation). Pricing is published but not machine-retrievable; modelled NZD monthly costs sit in the $1.5k–$9k range for our workload.

3. **Every other NZ provider is contact-sales or non-existent for this workload.** CCL/Spark, 2degrees, Umbrellar, Voyager, BizNet, Kordia, Enable, and Chorus have no public GPU SKU. **Datacom Sovereign Cloud** actively markets healthcare-tenancy GPU clusters and HIPAA-aligned controls but publishes no price list or SKU — worth a sales call as a Plan B for PHI credibility, but not a primary choice for a $177k/6-month programme. **No NZ government sovereign clinical AI cloud exists**; Te Whatu Ora's own digital platforms run on Azure and AWS. This gap is part of the N2RD thesis.

4. **Overseas cloud has a narrow residual case — and it's "de-identified or synthetic data only".** Runpod lacks a HIPAA BAA; Modal offers Enterprise BAA but not dedicated hardware tenancy; Lambda Labs and CoreWeave are US-jurisdiction. **Together AI (SOC 2 + HIPAA + dedicated endpoints)** is the strongest option for running open models not on Bedrock NZ, but data still leaves NZ. Bottom line: any identifiable NZ clinical data must stay on Bedrock NZ (cross-Region-bounded to ANZ) or Catalyst Cloud NZ; overseas cloud is for synthetic data experimentation and H100-class training jobs Catalyst cannot serve, and must be pre-approved by MBIE.

5. **The regulatory posture is clearer than the infrastructure posture.** Privacy Act 2020 + Health Information Privacy Code 2020 (updated 1 May 2026) + OPC's 2023 AI guidance + the 2025 Privacy Amendment Act's new IPP 3A (automated decision transparency, in force May 2026) are the current binding layer. **The Medical Products Bill is irrelevant during our grant period** — it is expected to be introduced to Parliament in 2026 but not commence until ~2030. The recommended DPIA structure is an OPC PIA Toolkit base + ICO AI DPIA extensions + NIST AI RMF Map/Measure/Manage overlay + NEAC §12–13 Māori data sovereignty layer + NHS DCB0129-style clinical safety case. Health NZ's **NAIAEAG** (National AI & Algorithm Expert Advisory Group) is the de facto gatekeeper for primary-care AI products and should be engaged early.

**Recommended sovereignty posture for Sprint 3 and Objective 2:**

- **Primary (all identifiable clinical data):** AWS Bedrock in ap-southeast-6 via the AU geographic cross-Region inference profile for Claude Haiku 4.5 / Sonnet 4.6 managed inference; Catalyst Cloud C1A (RTX A6000 48GB) for any self-hosted open-model workload.
- **Secondary (synthetic/de-identified only):** Together AI dedicated endpoints for open-model experiments not supported on Bedrock NZ; pre-approved with MBIE before use.
- **Contingency (PHI if Catalyst fails or Bedrock cross-Region becomes unacceptable):** Datacom Sovereign Cloud — engage sales now to secure a PHI-tenancy quote for the N2RD Q1 report and as a documented fallback.
- **Never:** Runpod (no BAA), Lambda (no BAA), serverless multi-tenant infrastructure processing PHI.

**Critical escalations (before architecture commitment):**

1. **MBIE Innovation Services** — written ruling on whether AWS ap-southeast-6 and Catalyst Cloud both count as "R&D undertaken in New Zealand" under the N2RD grant contract, and whether Together AI dedicated endpoints on synthetic data count.
2. **AWS NZ Public Sector BD** — confirm which Claude models (if any) are natively in-region vs only cross-Region routed, whether Provisioned Throughput is available in ap-southeast-6, and whether a ZDR / no-abuse-monitoring contractual addendum is possible for NZ health workloads.
3. **Catalyst Cloud** — written quote against the official cost calculator; confirmation of C3 L40S GA timeline and whether A100 80GB full cards are on the roadmap post-C2 retirement.
4. **Privacy Commissioner** — whether any updated post-HIPC-2026 cross-border interpretation is in the pipeline that would change the overseas-processor-as-agent doctrine.
5. **Health NZ NAIAEAG** — voluntary early engagement on the Inbox Helper + Care Gap Finder scope, to de-risk the rollout path.

This posture preserves the **"NZ-sovereign clinical AI built and operated within NZ"** differentiator stated in the dashboard and competitor tracker, while acknowledging the real-world caveats that make it harder than the headline suggests.

---

## 2. AWS Bedrock in ap-southeast-6 — Deep Dive

**Launch:** AWS Asia Pacific (New Zealand) Region ap-southeast-6 went GA in September 2025 with three Availability Zones in Auckland. **Amazon Bedrock launched in ap-southeast-6 in March 2026** — four weeks before this research ran. Source: AWS blog "Run Generative AI inference with Amazon Bedrock in Asia Pacific (New Zealand)" and the accompanying What's New announcement.

### 2.1 Model Availability — Native vs Cross-Region

The NZ launch communication names the following models as available through the Auckland endpoint:

- **Anthropic Claude:** Opus 4.5, Opus 4.6, Sonnet 4.5, Sonnet 4.6, Haiku 4.5
- **Amazon Nova 2 Lite**

**Critical nuance:** AWS's phrasing is "directly in the Auckland Region **with cross-Region inference**." These models are exposed through **inference profiles** that route across a geographic or global profile — not necessarily native on-region hosting. The distinction matters for sovereignty: cross-Region routing means individual inference calls may execute in Sydney or Melbourne, not Auckland.

- **Claude Sonnet 4 and Claude Opus 4.1 are not mentioned** in the NZ launch post. Status: assume not available until confirmed.
- **Meta Llama, Cohere, Mistral** are not listed in the NZ launch. Expect global cross-Region inference access only, if any.

**Action:** the exact "native in-region" subset requires direct confirmation with AWS NZ. The `bedrock/latest/userguide/models-regions.html` page was access-blocked during research.

### 2.2 Cross-Region Inference Behaviour and NZ Residency

Auckland is now a **source Region** for two profile types:

- **AU geographic inference profile** — routes to **Auckland (ap-southeast-6), Sydney (ap-southeast-2), and Melbourne (ap-southeast-4)** only. This bounds inference to the ANZ geography.
- **Global inference profile** — routes to supported commercial AWS Regions worldwide.

**Implications for sovereignty:**

- Using the AU geographic profile keeps inference within ANZ — acceptable under most NZ sovereignty framings if we accept "ANZ geography" rather than "NZ only".
- There is **no documented NZ-only pinning option**. You cannot today guarantee that an inference request originating in Auckland executes only in Auckland.
- Closest workarounds: (a) AU geographic profile (ANZ-bounded); (b) Provisioned Throughput (PT) in ap-southeast-6 if offered for the target model (unconfirmed); (c) wait for on-demand native hosting once regional quotas mature.
- SCPs for AU-geo must explicitly allow all three ANZ region IDs for the profile to work.

**Source:** AWS blog "Securing Amazon Bedrock cross-region inference: geographic and global"; Bedrock cross-region inference docs.

### 2.3 Data Handling — Prompts, Logging, Training, ZDR

AWS's Bedrock FAQ and Data Protection documentation state:

> "Amazon Bedrock doesn't store or log your prompts and completions. Amazon Bedrock doesn't use your prompts and completions to train any AWS models and doesn't distribute them to third parties."

- **Model provider isolation:** Each provider (Anthropic, etc.) runs in an isolated Model Deployment Account. Providers have **no access** to customer prompts, completions, or Bedrock logs.
- **Abuse monitoring:** fully automated, **no human review**, no persistent retention of prompts/outputs. **No published customer-level opt-out** for automated abuse checks.
- **Logging:** off by default. Customers can opt into CloudWatch / S3 invocation logging for their own compliance.
- **Zero Data Retention (ZDR):** AWS positions Bedrock as "no storage by default" — effectively ZDR behaviour — rather than offering a named enterprise ZDR contract addendum (unlike OpenAI's ZDR product). Governance is via AWS Service Terms + BAA + Bedrock-specific clauses.

**Sources:** `aws.amazon.com/bedrock/faqs/`, Bedrock Data Protection guide, Abuse Detection docs.

### 2.4 Healthcare Compliance — HIPAA, ISO, IRAP, SOC

- **HIPAA-eligible.** Amazon Bedrock and Bedrock AgentCore are listed on AWS's HIPAA Eligible Services Reference (page last updated 2026-03-16). Covered by the standard AWS BAA.
- **BAA.** HIPAA is a US statute; AWS will sign a BAA with any global customer including NZ entities, but the BAA governs **PHI under HIPAA**, not the NZ Health Information Privacy Code 2020. **A BAA is a useful baseline, not a substitute for HIPC compliance.**
- **ISO 27001 / SOC 2 / CSA STAR L2.** AWS-wide certifications cover Bedrock. ap-southeast-6 regional scope should be reconfirmed via AWS Artifact — new regions typically inherit global certifications within months of launch.
- **IRAP (Australian PROTECTED).** Applies to ap-southeast-2 and ap-southeast-4; **ap-southeast-6 IRAP status unconfirmed** as of April 2026. NZ has no direct IRAP equivalent.
- **NZ-specific material.** AWS publishes "Using AWS in the Context of New Zealand Privacy Considerations" — a whitepaper suitable for DPIA citation.
- **FedRAMP High.** Bedrock is authorised only in AWS GovCloud (US-West) — irrelevant to NZ but relevant if any workload ever touches US federal data.

**Sources:** AWS HIPAA Eligible Services Reference; `aws.amazon.com/bedrock/security-compliance/`; AWS NZ privacy whitepaper.

### 2.5 Pricing — Sydney ap-southeast-2 as NZ Proxy

ap-southeast-6-specific list prices are **not separately published** on the Bedrock pricing page at time of research. Using ap-southeast-2 (Sydney) as the proxy — AWS historically prices new AU/NZ regions at Sydney parity — and third-party Bedrock pricing aggregators:

| Model | Input USD / 1M tokens | Output USD / 1M tokens |
|---|---|---|
| Claude Haiku 4.5 | $1.00 | $5.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Opus 4.6 | $15.00 | $75.00 |

- **Regional endpoint premium:** regional endpoints carry roughly a **~10% premium over Global endpoints** (confirmed in third-party guides from Sonnet 4.5 / Haiku 4.5 onward).
- **Context tiering:** Sonnet 4.6 above 200K context is tiered to roughly $6 input / $22.50 output per 1M tokens.
- **Prompt caching:** up to **90% off** on cached input tokens.
- **Batch Inference:** **50% off** on-demand pricing; availability in ap-southeast-6 specifically is unconfirmed.
- **Provisioned Throughput:** commitment-based pricing; availability in ap-southeast-6 specifically is unconfirmed.

**Cost implication for our workload.** At ~1,500 input / 200 output tokens per document on Haiku 4.5, zero-shot inference is ~USD $2.50 per 1k documents — approximately **NZD $4.20 per 1k documents**. At 10k docs/day per practice that's ~NZD $1,260/month/practice. See R1 Section 8.2 for the full cost table.

**Assumption to confirm:** ap-southeast-6 list price parity with ap-southeast-2. A 5–15% premium is plausible.

### 2.6 Published NZ Health Deployments on Bedrock (since March 2026)

**None found.** Searches across AWS blogs, press releases, HINZ, Te Whatu Ora, news media, and GitHub returned:

- General HINZ commentary on AI in NZ health (privacy concerns, "localised data" preference)
- Ministry of Health using AWS broadly; nib (insurer) on AWS
- No NZ case study, blog, or announcement of Bedrock in ap-southeast-6 for identifiable clinical data as of April 2026

**Implication:** we are early adopters. **NexWave would plausibly be the first published NZ health deployment on Bedrock NZ for identifiable clinical data.** This is both an opportunity (differentiator, MBIE narrative, conference talk) and a risk (no precedent case studies to learn from).

### 2.7 NZ Privacy Commissioner / HINZ / Te Whatu Ora Positions on AWS

- **OPC (privacy.org.nz):** No NZ-specific prohibition on AWS as a health information processor. Generic "using the cloud" guidance applies. The **Health Information Privacy Code 2020** governs health information and the **Privacy Amendment Act 2025** introduced **IPP 3A** (transparency on automated decision-making). **HIPC is in force with updates commencing 1 May 2026.** No OPC statement specific to Bedrock-in-NZ has been published since the March 2026 launch.
- **HINZ:** 2025 Digital Health AI Summit flagged "data sovereignty" and preference for localised data as top concerns — directionally supportive of using the NZ region but no explicit Bedrock endorsement.
- **Te Whatu Ora:** No public position specifically on AWS Bedrock. The Shared Digital Health Record (SDHR) is slated for mid-2026 launch; no Bedrock linkage announced. **NAIAEAG** (Section 9) is the advisory gatekeeper for clinical AI and should be engaged.

### 2.8 Account Setup, Model Access, and Support

- **Model access process:** Bedrock grants automatic access to most serverless models via IAM, but **Anthropic Claude models still require a one-time usage form** (via console or `PutUseCaseForModelAccess` API) before first use. AWS Organizations customers submit once at the management account and inherit to children.
- **Enterprise support tiers:** Developer / Business / Enterprise On-Ramp / Enterprise are standard. No ap-southeast-6-specific tier restrictions found. AWS NZ has an Auckland-based account team post-region launch — worth a direct conversation.
- **Sandbox / trial:** Standard Bedrock on-demand once the usage form is approved. AWS Activate startup credits remain available to NZ entities. No "NZ-specific" sandbox programme identified.

### 2.9 Open Questions for AWS NZ (escalation list)

1. Exact **native-in-region** model list for ap-southeast-6 — is anything hosted natively, or is every call routed via AU-geo to Sydney/Melbourne?
2. Is **Provisioned Throughput** offered in ap-southeast-6 for Haiku 4.5 / Sonnet 4.6, and would PT guarantee NZ-only inference?
3. Confirmation that ap-southeast-6 is in scope for **ISO 27001, SOC 2 Type II, CSA STAR L2, PCI-DSS** as of Q2 2026.
4. Is Claude Sonnet 4 / Opus 4.1 available at all from ap-southeast-6?
5. Contractual ZDR addendum beyond default Bedrock "no storage" posture for NZ health workloads; abuse-monitoring opt-out for BAA customers.
6. ap-southeast-6 list pricing confirmation and whether the 10% regional premium applies.
7. Has any Te Whatu Ora / HealthLink / Health NZ workstream piloted Bedrock NZ under NDA? (Public Sector BD conversation.)
8. **Batch Inference** availability in ap-southeast-6 for Care Gap Finder cost optimisation.

---

## 3. Catalyst Cloud NZ — Deep Dive

**Profile.** Catalyst Cloud is Wellington- and Auckland-based, **100% NZ-owned and operated**, and is the only NZ-sovereign public cloud provider on the **DIA All-of-Government Cloud Framework Agreement**. Data centres in Wellington, Porirua (`nz-por-1`), Hamilton, and an Auckland region opened mid-2023. Certified to **ISO 27001, ISO 27017, PCI-DSS** across all three data centres, with **NZISM-aligned** controls via the Cove managed platform.

Public statement on sovereignty (direct quote):

> "As a New Zealand located, owned and operated business, all customers' data stays safely in Aotearoa… no jurisdictional risk caused by external or overseas engineers… no foreign jurisdiction can use their laws to access your data."

(Source: `catalystcloud.nz/about/data-sovereignty/`)

This is the **strongest-possible sovereignty posture** any cloud provider can claim for NZ clinical data — stronger than AWS Bedrock NZ, because no overseas engineer or foreign jurisdiction has access, and no cross-Region routing happens.

### 3.1 GPU Catalogue — and the Hard Truth About It

The publicly advertised GPU catalogue as of April 2026:

| Product | GPU | VRAM | CPU pairing | Status |
|---|---|---|---|---|
| **C1A GPU** | NVIDIA RTX A6000 | 48 GB (up to 4× = 192 GB) | AMD EPYC | **GA** |
| **C2 GPU** | NVIDIA A100 vGPU slice (`GRID A100D-20C`) | **20 GB slice, not full 80 GB card** | Intel high-freq | **⚠️ DEPRECATED — retiring 31 March 2026** |
| **C3 GPU** | NVIDIA L40S | 48 GB (up to 4× = 192 GB) | High-freq | **⚠️ BETA, Porirua (`nz-por-1`) only** |

**No H100, H200, or B200** in the public catalogue. No full A100 80GB cards — only the 20GB slice, and that is retiring.

**Critical implications for Sprint 2 / Sprint 3 planning:**

1. **C2 (A100 slice) is retiring on 31 March 2026.** Any architecture that assumes A100 availability on Catalyst is **a non-starter from Sprint 3 onwards**. Do not design around it.
2. **C3 (L40S) is in Beta, Porirua-only.** Beta means no production SLA. Unsuitable for Objective 2 commercial rollout until GA. Fine for Sprint 2 experimentation if we accept the risk.
3. **C1A (RTX A6000 48GB) is the only safe GA choice.** Fortunately, it is dimensioned well for our candidate models:
   - BioClinical ModernBERT 396M — trivial on 48GB
   - Llama 3.1 8B fine-tuned (FP16, ~16GB) — plenty of headroom
   - Llama 3.3 70B at Q4 quantisation (~35–40GB weights + KV cache) — fits one card tightly via llama.cpp or vLLM AWQ
   - Qwen 2.5 72B at Q4 — similar profile, fits one card

**Source documents:** `catalystcloud.nz/services/iaas/compute/compute-c1a-gpu/`, `/compute-c2-gpu/`, `/compute-c3-gpu/`; `docs.catalystcloud.nz/compute/gpu-support.html`; Catalyst Cloud GPU-as-a-Service launch announcement.

### 3.2 Pricing — Published, But Not Publishable Here

Catalyst Cloud's price list (`catalystcloud.nz/pricing/price-list/`) and cost calculator (`catalystcloud.nz/pricing/calculator/`) are public pages, but both return HTTP 403 to automated fetchers — **precise NZD rates could not be retrieved programmatically during this research**. Modelled estimates based on historical Catalyst GPU rates and peer-provider benchmarks (getdeploying RTX A6000 $0.49–$0.79 USD/hr; L40S $0.80–$1.40 USD/hr):

| Instance | Modelled NZD/hour (verify) |
|---|---|
| C1A (1× RTX A6000 48GB) | ~NZD $1.80–2.40 |
| C2 (A100-20C slice, retiring) | ~NZD $1.50–2.00 |
| C3 (1× L40S 48GB, Beta) | ~NZD $2.50–3.20 |

**Action required:** Ryo (or Ting) to log into the official Catalyst Cloud cost calculator and capture exact NZD/hour figures before any number from this report lands in the MBIE Q1 narrative. Catalyst will also quote direct on request; a written quote is preferable for grant compliance documentation.

### 3.3 Production Cost Model for Our Workload — 24×7 at 730 hours/month

Using the midpoint of the modelled C1A rate (NZD $2.10/hr) and 730 hours/month:

| Stack | GPU | Modelled NZD/month | Notes |
|---|---|---|---|
| BioClinical ModernBERT 396M | 1× C1A | **~NZD $1,533** | Massive headroom; same cost at 1k or 10k docs/day |
| Llama 3.1 8B fine-tuned (vLLM) | 1× C1A | **~NZD $1,533** | 8B FP16 ~16GB fits A6000 easily |
| Llama 3.3 70B INT4 (llama.cpp or vLLM AWQ) | 1× C1A | **~NZD $1,533** | Tight fit at Q4, single-card viable |
| Llama 3.3 70B INT4 (production) | 2× C3 L40S (Beta) | **~NZD $4,088** | Higher throughput, but Beta / Porirua-only |
| GPT-OSS-120B INT4 | 4× C3 L40S (Beta) | **~NZD $8,175** | Not realistic on current catalogue |

**Six-month Sprint 2 + Sprint 3 totals (24×7):**
- BioClinical ModernBERT on C1A: ~NZD $9.2k
- Llama 3.1 8B fine-tuned on C1A: ~NZD $9.2k
- Llama 3.3 70B INT4 on C1A: ~NZD $9.2k
- Llama 3.3 70B INT4 on 2× C3: ~NZD $24.5k

All comfortably within the NZD $177k Objective 1 envelope, leaving runway for storage, egress, and the second R&D engineer. **The C1A RTX A6000 is effectively the "cheap enough for everything" anchor of our NZ-sovereign self-hosted path.**

### 3.4 Kubernetes, Networking, and Operational Stack

- **Catalyst Kubernetes Service** supports GPU worker nodes via standard GPU flavours and the `gpu-acceleration.html` docs path. Suitable for containerised vLLM / SGLang / TGI inference.
- **Private networks, VPN, and regional interconnects** available within the Catalyst national footprint.
- **Object storage, block storage, load balancers** — standard OpenStack-backed IaaS.
- **Observability:** customer-built (Prometheus / Grafana typical). No managed "LLM gateway" equivalent to Bedrock Guardrails — we would build our own safety layer.

### 3.5 Published NZ Health Customers

- **Healthify (formerly Health Navigator NZ)** — runs on Catalyst Cloud. Health information portal, **not** a PHI/EHR workload. A sovereignty proof-point but not a PHI-at-scale proof-point.
- **No published Te Whatu Ora, DHB, or GP/PMS customer case study** running production clinical workloads on Catalyst Cloud was found. (Source: `catalyst.net.nz/stories-and-studies/case-studies/healthify-makes-health-information-easy-to-access-and-understand`.)

**Implication:** NexWave would again plausibly be the first published NZ health product running **identifiable clinical workloads** on Catalyst Cloud GPU. This mirrors the Bedrock NZ finding (Section 2.6) and reinforces the early-adopter posture.

### 3.6 Catalyst Cloud — Open Questions (escalation list)

1. **Exact published NZD rates** for C1A, C2 (pre-retirement), and C3 from the cost calculator.
2. **Post-C2 roadmap** — is Catalyst planning to introduce full A100 80GB cards, H100, H200, or B200? What is the promised timeline?
3. **C3 L40S GA date** and which data centres will host it beyond Porirua?
4. **Production SLA** terms — availability guarantee, maintenance windows, credits for downtime.
5. **Customer references** for production LLM inference workloads (not just web/DB workloads).
6. **Managed Kubernetes GPU support** — is it production-ready or does it still require custom manifests?
7. **Networking latency** — p95 round-trip from Catalyst Porirua/Auckland to Medtech Evolution Cloud (where Medtech data resides) for ALEX API calls.

---

## 4. Alternative NZ-Hosted Options

Every NZ provider outside AWS and Catalyst was scanned for viable GPU / LLM inference offerings suitable for identifiable clinical data. Summary:

### 4.1 Datacom Sovereign Cloud

**Strongest Plan B.** Datacom's Sovereign Cloud (`datacom.com/nz/en/solutions/cloud/hybrid-and-private/sovereign`) explicitly markets:

> "dedicated healthcare cloud tenancy… HIPAA-aligned controls, onshore GPU resources for AI workloads, HL7/FHIR"

and

> "dedicated GPU clusters and in-country AI platforms supporting confidential AI"

Claims **IRAP (PROTECTED), NZISM (Restricted), ISO 27001, Essential Eight**. **VMware Sovereign Cloud certified** per the published VMware/Datacom case study.

**Caveats:**
- **No published NZD price list, no published GPU SKU list, no public per-hour rates.** Classic enterprise sovereign-cloud pattern: contact sales, expect bespoke contracts, minimum commits.
- Likely too heavy-weight for a 2-person $177k programme without a negotiated R&D pilot rate.
- Useful as a **documented fallback** for the MBIE Q1 report — demonstrates we have a PHI-tenancy contingency beyond Catalyst Cloud.

**Recommendation:** engage Datacom Sovereign Cloud sales in parallel with Sprint 2 architecture work. Even a non-committal quote improves the DPIA "alternatives considered" section.

### 4.2 CCL (Computer Concepts Limited — Spark-owned, post-Revera merger)

Spark NZ-owned IT services arm. DCs in Takanini and William Pickering Drive Auckland. **No public GPU cloud / LLM inference product.** Spark has signalled general AI infrastructure investment but as of April 2026 there is no published on-demand GPU SKU, no price list, no health AI case study. Contact-sales only. **Not viable for Sprint 2.**

### 4.3 Other NZ Providers — Quick Scan

| Provider | GPU for LLM inference? | Notes |
|---|---|---|
| **2degrees Business** | No | Partners with Umbrellar + Microsoft for Azure resell only |
| **Umbrellar** | No public GPU IaaS SKU | Azure / M365 managed services |
| **Voyager** | Unknown / no indexed product page | — |
| **BizNet** | Unknown / SMB IaaS, no GPU product indexed | — |
| **Kordia** | No | Connectivity and security focus |
| **Enable / Chorus** | No | Fibre network operators, not compute |
| **Aqua Comms, Global Switch** | Colo / connectivity only | Not compute |

All of the above should be treated as **"not viable"** for Sprint 2 GPU inference without a direct sales conversation and are unlikely to become viable within our grant period.

### 4.4 NZ Colocation with Bring-Your-Own-GPU

NZ colocation is mature — **CDC Data Centres** (Silverdale, Hobsonville 1 + 2, hyperscale), Spark (Takanini, Mayoral Drive), Datacom (Orbit, Kapua), Global Switch, and Plan B sites. CDC Hobsonville 2 has been certified for secure public cloud use since July 2025.

BYO-GPU colo is technically possible but **not realistic for a $177k / 6-month / 2-person R&D programme**:

- A single DGX-class node is **NZD $300k+ capex** — exceeds the full Objective 1 compute + labour budget.
- Rack + power + cross-connect: ~NZD $2–4k/month.
- Plus OS, driver, MLOps, networking, backup, monitoring — all to be operated by a 2-person team.
- A single C1A VM on Catalyst Cloud is **dramatically cheaper** for this scale.

**Recommendation:** do not pursue colocation in Sprint 2 or Sprint 3. Revisit in Objective 3 (commercialisation) only if Catalyst Cloud cannot meet scale or sovereignty requirements.

### 4.5 NZ Sovereign Health AI Cloud Initiatives — None

**No NZ government-funded sovereign clinical AI cloud exists as of April 2026.** Te Whatu Ora's national hybrid multi-cloud programme (~NZD $4.55M) is building platforms on **Azure and AWS** via a Microsoft-led contract — explicitly hyperscaler, not NZ-sovereign. HealthX innovation programme deploys GenAI to clinicians on the same Azure/AWS stack. HINZ and HISO have published advisory material (`hinz.org.nz/resource/Cloud_in_Healthcare_NZ.PDF`) but no sovereign-compute initiative analogous to UK NHS sovereign AI proposals.

**Implication for NexWave:** the sovereignty gap is real and government-unfilled. This is **part of the N2RD thesis** — there is no government platform to ride on, and that is precisely why Catalyst Cloud + Bedrock NZ is the right anchor combination. It also means our own production deployment will be one of the earliest NZ-sovereign clinical AI services in existence.

### 4.6 Alternative-Option Summary Table

| Provider | GPU SKU public | NZ residency | Published pricing | Health proof-point | Verdict |
|---|---|---|---|---|---|
| **Catalyst Cloud** | Yes — C1A only (safe) | ✅ 100% NZ-owned | Yes (calculator, non-scrapable) | Healthify (info portal, not PHI) | **Primary self-hosted choice** |
| **Datacom Sovereign** | Marketed, no SKU/price list | ✅ ANZ only, IRAP/NZISM | No — contact sales | Marketed HIPAA tenancy, no named case study | **Documented fallback** |
| **CCL / Spark** | No | ✅ | No | None found | Not viable |
| **2deg / Umbrellar / Voyager / BizNet / Kordia / Enable / Chorus** | No | Mixed | No | None | Not viable |
| **NZ colo BYO-GPU** (CDC, etc.) | N/A — bring own hardware | ✅ | Rack/power only | — | Not viable at this budget |
| **Te Whatu Ora / HISO sovereign AI cloud** | Does not exist | — | — | — | Not available |

---

## 5. Overseas Cloud — Residual Case and Grant Compliance

Given Bedrock NZ (Section 2) and Catalyst Cloud NZ (Section 3) both exist, is there any remaining case for overseas cloud GPU? The short answer is: **yes, but narrow — synthetic or de-identified data only, and only when an NZ-sovereign path cannot serve the use case**.

### 5.1 Runpod Secure Cloud

- **SOC 2 Type II** confirmed; Tier III+ data centres; "Secure Cloud" brand markets dedicated resources
- **HIPAA BAA is not yet GA** — still on Runpod's compliance roadmap
- H100 PCIe approximately **USD $2.69/hr** on Secure Cloud; Community Cloud slightly cheaper
- FlashBoot cold starts in the low seconds range
- **Jurisdiction: US (Delaware).** No NZ region. Regions span US / EU / APAC
- **Verdict: not viable for identifiable PHI today.** Revisit when HIPAA BAA goes GA. Useful only for synthetic data experimentation pre-approved by MBIE.

### 5.2 Modal

- **$87M Series B (Sept 2025, Lux Capital, ~$1.1B post-money)**
- **HIPAA BAA on Enterprise plan**; **SOC 2 Type I** confirmed with Type II in progress
- Sub-second cold starts via `.remote()`; infrastructure-as-code Python model
- **Jurisdiction: US.** Dedicated-tenancy is not the default — isolation is logical, not hardware-level
- **Verdict: acceptable for dev and synthetic data; borderline for production PHI** under the N2RD sovereignty stance. Not a primary choice but a credible dev-only fallback.

### 5.3 Lambda Labs

- **Deprecated Inference API and Chat in September 2025** — now on-demand GPU VMs only
- H100 SXM from roughly **USD $2.99/hr on-demand** (reserved ~$1.85–1.89)
- A100 from approximately **USD $1.10–1.29/hr**
- **No published HIPAA BAA** for general customers
- **Verdict: not viable for PHI.** Cheapest H100 pricing for synthetic-data experimentation and fine-tuning jobs if pre-approved.

### 5.4 CoreWeave

- Enterprise-grade: **HIPAA, SOC 2, ISO 27001, NIST 800-53, GDPR-ready**
- **Dedicated bare-metal** clusters with per-tenant VPCs on CKS (CoreWeave Kubernetes Service)
- H100 / H200 / GB200 NVL72 fleets
- NZ customers contractually eligible; all regions US / EU
- **Significant minimum commitments** — typically large reserved clusters
- **Verdict: strong HIPAA posture, but minimum-commit economics are wrong for a $177k/6-month programme.** Revisit at commercialisation (Objective 3+) if NZ sovereign capacity is exhausted.

### 5.5 Together AI and Fireworks AI (API-First)

- Both offer API access to open models: Llama 3.3 70B, Qwen 2.5, DeepSeek-R1, etc.
- **Together AI: SOC 2 Type II and HIPAA-compliant**, offers **dedicated endpoints** and reserved capacity. Llama 3.3 70B ~USD $0.88 per 1M tokens serverless
- **Fireworks AI:** Llama 3.3 70B at ~USD $0.90 per 1M tokens; HIPAA BAA available for enterprise but less prominently documented than Together
- Both host in **US regions** — **no NZ data residency**; identifiable patient data would leave NZ
- **Verdict:** **Together AI dedicated endpoints** are the strongest overseas option for running open-weights models not on Bedrock NZ — but **only for de-identified or synthetic data**, and only when Bedrock NZ cannot serve the model we need.

### 5.6 Multi-Tenancy vs Dedicated Tenancy for Healthcare

The published concern (repeated in healthcare-AI infrastructure guides Censinet, ESI, VRLA, Introl, HyperTrends) is:

> "Serverless platforms share infrastructure across customers, with inference requests running on GPUs that processed someone else's data minutes earlier, which creates audit problems for healthcare (HIPAA)."

**Nuanced reality:** The specific "data leak across tenants" claim is only a problem if memory/VRAM is not wiped between jobs — reputable providers with BAAs contractually commit to zeroisation. The residual concern is **auditability**, not leakage per se. Industry sources confirm multi-tenant GPU infrastructure creates **fragmented audit trails, noisy-neighbour risk, and tenant-isolation failure modes** that complicate HIPAA Security Rule compliance. **HHS OCR's January 2025 proposed Security Rule overhaul explicitly addresses dynamic AI compute**, tightening requirements.

**Implication:** **Serverless multi-tenant GPU is a non-starter for identifiable NZ clinical data.** Only CoreWeave, Together AI (dedicated endpoints), and Modal (Enterprise) combine HIPAA BAA with dedicated or near-dedicated tenancy among the providers reviewed — and none are in NZ.

### 5.7 MBIE N2RD Grant Interpretation for Cloud Compute

**Confirmed general rule.** For MBIE grants and RDTI, "R&D undertaken outside New Zealand" is generally **ineligible**; up to ~10% of eligible expenditure may be foreign under RDTI for supporting activity. Overseas labour approval is discretionary and requires showing the capability cannot be sourced in NZ. Materials and consumables purchased from overseas are allowed. (Sources: `ird.govt.nz/research-and-development/tax-incentive/eligibility/eligible-expenditure`, MBIE New to R&D Grant Resource Hub.)

**Cloud compute specifically — no published guidance.** Neither MBIE Innovation Services nor the former Callaghan Innovation has published guidance directly classifying cloud compute as NZ or overseas R&D expenditure. The N2RD Resource Hub and the Gazette direction are silent.

**Practical industry reading** (Swell, Applied Support Services, Andersen NZ): cloud compute used by NZ-based researchers is typically treated as a **consumable / service input** rather than "R&D performed overseas," provided the researchers, IP creation, and decision-making happen in NZ. The place of R&D is the researcher's desk, not the datacentre hosting the compute.

**However** — identifiable NZ clinical data crossing borders introduces a **separate Privacy Act 2020 / HIPC 2020 issue** distinct from grant eligibility. The two constraints stack.

**Callaghan disestablishment** (December 2024) transferred functions to MBIE Innovation Services; the same teams continue. (Source: `callaghaninnovation.govt.nz/about-us/disestablishment-updates/`.)

### 5.8 Critical Escalation — Written Ruling from MBIE

**This is the highest-priority escalation from R2.** We need a **written ruling from MBIE Innovation Services for our N2RD contract** covering:

1. Does **AWS Bedrock ap-southeast-6** (Auckland) count as NZ R&D expenditure when the R&D team is NZ-based? What about cross-Region inference calls that execute in Sydney or Melbourne as part of the AU geographic profile?
2. Does **Catalyst Cloud NZ** count unambiguously as NZ R&D expenditure?
3. Are **Together AI dedicated endpoints in the US**, used only for synthetic data experimentation with open-weights models unavailable on Bedrock NZ, eligible? Under what conditions?
4. What about **H100-class training or fine-tuning jobs** on Lambda Labs or CoreWeave for short bursts when Catalyst cannot serve the hardware?
5. Treatment of **hybrid setups** (NZ-resident data flow + occasional offshore inference for benchmark experiments on public datasets)?

No community notes, case studies, or public MBIE correspondence on any of these questions surfaced during the research. **Resolve this before any architecture commitment in Sprint 3.**

### 5.9 Bottom-Line Overseas-Cloud Recommendation

**Default to all-in NZ for anything touching identifiable patient data:**
- Bedrock ap-southeast-6 for managed LLM inference
- Catalyst Cloud NZ (C1A) for self-hosted GPU workloads requiring full sovereignty

**Treat overseas cloud as a narrow, pre-declared exception** used only for:
1. De-identified or synthetic data experiments
2. Open-weights models not available on Bedrock NZ (via Together AI HIPAA dedicated endpoints on synthetic data only)
3. H100-class training or fine-tuning jobs Catalyst cannot serve — pre-approved by MBIE

**Before using any overseas provider against grant funds:**
- Obtain **written pre-approval from MBIE Innovation Services** citing the capability-gap test used for overseas labour
- Keep a documented data-flow diagram showing all identifiable NZ clinical data remains in NZ jurisdiction
- Budget posture: assume **90%+ of the $177k compute line stays onshore**

---

## 6. NZ Privacy Act 2020 + Health Information Privacy Code 2020 — Obligations for AI-CDS

The binding regulatory layer for our product during the grant period is the **Privacy Act 2020**, the **Health Information Privacy Code 2020** (updates in force 1 May 2026), the **Privacy Amendment Act 2025** (new IPP 3A on automated decision-making transparency), and the **OPC's 2023 AI guidance**. These are in force now. The Medical Products Bill (Section 7) is not.

### 6.1 Rule / IPP Mapping for AI-CDS Processing Identifiable Clinical Data

- **Rule 5 (Storage/security).** HIPC Rule 5 mirrors IPP 5 and requires health agencies to protect information against loss, unauthorised access, use, modification, and disclosure. For AI-CDS, OPC's 2023 AI guidance frames this as requiring **vendor due diligence**, **encryption**, **access controls**, and assessment of whether an AI provider retains or discloses inputs. **Implication for Bedrock NZ:** the AWS BAA plus the Bedrock "no storage by default" posture satisfies Rule 5 if documented. **Implication for Catalyst Cloud:** NZ-owned, NZ-operated, NZISM-aligned — the strongest Rule 5 baseline available.

- **Rule 8 (Accuracy).** Agencies must take reasonable steps to ensure information is accurate, up-to-date, complete, relevant, and not misleading before use. **OPC's AI guidance specifically identifies AI training data and model outputs as accuracy risks** and expects "procedures to ensure accuracy and respond to access and correction requests." This lands directly on our product — every urgency label and every care gap flag is an "output" the Rule applies to.

- **Rule 11 (Disclosure).** Permits disclosure for directly related purposes or with authorisation. Sending identifiable data to a cloud LLM is **typically not a "disclosure"** under the OPC's long-standing agent/processor doctrine, provided the cloud provider is acting as an agent of the NZ agency. The data is being "used" by the agency, not "disclosed" to a third party. **But:**

- **IPP 12 (Cross-border).** Added in 2020; applies to offshore transfers where HIPC is silent. Requires one of: (a) the overseas party is subject to comparable privacy law, (b) model contractual clauses are in place, or (c) individual authorisation. **Implication for Bedrock ap-southeast-6 with AU geographic cross-Region inference:** data may execute in Sydney (Australian Privacy Principles — arguably comparable) or Melbourne (same). This is defensible under IPP 12 (a) "comparable privacy law" but must be documented in the DPIA.

- **Rule 12 (Unique identifiers, HIPC-specific).** Governs NHI and similar identifiers. Any use of NHI by our system must comply. Not an architecture-blocker but must be in the DPIA.

### 6.2 The Agent/Processor Doctrine and Cross-Border Data Flow

OPC's long-standing 2020 Interpretation position (detailed in the Future of Privacy Forum deep dive on the 2020 Act) is that sending personal information to an **overseas processor acting as an agent** of the NZ agency is a **"use," not a "disclosure"** — so Rule 11 / IPP 11 is not engaged. **However**, **IPP 12** (added in 2020) still imposes offshore-transfer obligations, and Rule 5 / IPP 5 security duties travel with the data.

**No published 2024–2026 update reverses this.** The doctrine remains current, and health agencies still need IPP 12 coverage via contract clauses for overseas cloud processors. AWS's standard Data Processing Addendum plus the BAA cover this, as would Catalyst Cloud's NZ-only contract.

**Practical implication:**
- **Bedrock ap-southeast-6** via AU geographic profile → defensible under "agent + IPP 12 (a) comparable privacy law" framing.
- **Catalyst Cloud NZ** → IPP 12 does not apply (data never leaves NZ). Simplest legal posture.
- **Together AI US dedicated endpoints** → agent doctrine applies; IPP 12 (a) depends on US HIPAA being "comparable" — this is not a confident position for identifiable NZ clinical data. **Use only for synthetic/de-identified data.**

### 6.3 OPC 2023 AI Guidance — Core Expectations

Published 21 September 2023, expanding on 15 June 2023 expectations. Core expectations for agencies using AI with personal information:

1. **Senior-leader involvement** in AI deployment decisions
2. **Necessity and proportionality test** — is AI actually needed?
3. **PIA before deployment** with **community (including Māori) feedback**
4. **Transparency** with affected individuals
5. **Accuracy procedures** per Rule 8
6. **"AI use for automated decision-making is a higher-risk use case"** requiring human review

**The Commissioner publicly flagged risks in the National AI Strategy in August 2025** (Newsroom 2025-08-11). No 2024–2026 update formally supersedes the 2023 guidance.

**Source documents:**
- OPC "AI and the Information Privacy Principles" (PDF, Sept 2023)
- OPC A-Z: AI resource hub
- Anderson Lloyd, MinterEllisonRuddWatts, Bell Gully, Securiti, Russell McVeagh summaries of the guidance

### 6.4 Privacy Amendment Act 2025 — New IPP 3A (Automated Decision Transparency)

The **Privacy Amendment Act 2025** introduced a new IPP 3A covering **transparency on automated decision-making**. In force May 2026 — i.e. during our Sprint 3 and Objective 2 build phase.

**What IPP 3A requires (high level):** when an agency uses automated decision-making that significantly affects an individual, the individual must be informed. OPC consulted in March 2026 on how to reflect IPP 3A in the HIPC and other codes.

**Implication for our product:** the Inbox Helper and Care Gap Finder are **assist-only** — GPs review everything. This framing likely keeps us out of "significant automated decision" territory, **but** it is not self-enforcing. The DPIA must demonstrate:

- No action is taken without GP review
- GPs have real authority to override
- Output is logged and reviewable
- Patients are informed (at the practice level) that AI assists with triage and care gap detection

### 6.5 What "Assist-Only" Must Do to Stay Assist-Only

HIPC does not use the phrase "assist-only." OPC treats automated decisions as higher-risk and expects **human review resourced adequately**. To credibly remain assist-only, our product must:

1. **Never auto-execute clinical actions** (no auto-filing, no auto-reply, no auto-ordering)
2. **Keep a clinician in the loop** with real authority to override, not just a "confirm" button that the UX pressures into a rubber-stamp
3. **Log and enable review** of outputs, including GP accept/override decisions
4. **Be described to patients** as advisory — at practice disclosure level, not per-interaction
5. **Avoid "automation bias"** UX patterns — don't present AI outputs as definitive
6. **Resource human review adequately** — the model cannot reduce GP time so much that review becomes token

**The Heidi Health March 2026 security disclosure** (Section 9.1) is a live lesson: Heidi's administrative-tool classification was key to avoiding SaMD regulation, but when guardrails were bypassed in three prompts Heidi "broke a promise that was key to getting into the medical field: that Heidi was just a note-taker and could not provide diagnostic input." **The classification is not self-enforcing.** Our architecture must be structurally incapable of auto-action, not just UI-capped.

### 6.6 HISO Information Security Framework Applies to Us

**HISO 10029:2022 Health Information Security Framework** is the Te Whatu Ora-endorsed security standard for NZ health information, with sub-parts:

- HISO 10029.1 (hospitals)
- HISO 10029.2 (micro/small practices)
- HISO 10029.3 (medium/large practices)
- **HISO 10029.4:2025 (suppliers)** — **directly relevant to NexWave** as an AI-CDS supplier into primary care

**HISO 10064** is the complementary Health Information Governance Guidelines.

**Implication:** the supplier-facing sub-part (10029.4:2025) is a relatively new standard and should be cross-referenced in our DPIA and in any supplier due diligence Medtech or practices carry out on us before deployment. Build to this standard from Sprint 3 onwards.

### 6.7 Summary — Regulatory Posture for Sprint 2 DPIA and Sprint 3 Build

- Privacy Act 2020 + HIPC 2020 (updated 1 May 2026) is the binding layer
- OPC 2023 AI guidance is the authoritative AI interpretation
- Privacy Amendment Act 2025 IPP 3A on automated decision transparency applies from May 2026
- Agent/processor doctrine keeps overseas cloud processing as "use not disclosure" — but IPP 12 + DPIA documentation is required
- HISO 10029.4:2025 supplier standard applies directly to NexWave
- Health NZ NAIAEAG advisory voice should be engaged early
- "Assist-only" is a posture we must architecturally enforce, not just claim

---

## 7. Medical Products Bill — Status Check Only

**Bottom line: the Medical Products Bill is NOT in force during our grant period (Mar 2026 – Mar 2028).** We design and operate under the current regime: Medicines Act 1981 + WAND notification + HIPC 2020 + Privacy Act 2020, plus TGA Class IIa considerations (covered elsewhere in the vault).

**Confirmed status (as of April 2026):**

1. **Cabinet decision (July 2025, confirmed August 2025):** Cabinet agreed to introduce a Medical Products Bill that will regulate Software as a Medical Device (SaMD), including AI used for therapeutic purposes. Source: MoH briefing "Supporting innovation through the Medical Products Bill" (August 2025); Russell McVeagh "Prescription for change" commentary (August 2025); NZ Nurses Organisation update (August 2025); Buddle Findlay commentary.

2. **Parliamentary introduction: expected during 2026** — the Bill is planned for introduction this calendar year but had not been tabled as of early April 2026.

3. **Commencement: expected ~2030** — government briefings indicate a multi-year implementation runway, placing the operative regime well beyond our 24-month grant window.

4. **Transitional arrangements:** no public signals of pre-commencement transitional obligations that would bind R&D-stage work in 2026–2028. Medsafe has not issued pre-commencement guidance for SaMD developers.

**Implication for NexWave:**
- Continue to operate under the current regime.
- Monitor the Bill when it is introduced (tracking in the nexwave-rd dashboard compliance-deadlines section).
- Design the DPIA and Quality Management System to be **forward-compatible** with the likely SaMD obligations (Section 8 DPIA methodology is chosen with this in mind — ISO/IEC 42001 and NIST AI RMF both track toward future SaMD expectations).
- No deep dive required at this research stage.

---

## 8. DPIA Methodology for AI-Assisted Clinical Decision Support

The MBIE N2RD grant Capability Development deliverable requires "DPIA methodology". This section recommends a **base template + AI-specific extensions** approach, grounded in NZ Privacy Commissioner guidance and internationally recognised AI frameworks.

### 8.1 Recommended Base Template: OPC Privacy Impact Assessment Toolkit

The **New Zealand Privacy Commissioner's PIA Toolkit (2024 update)** is the authoritative base template for privacy impact assessments in NZ. Key characteristics:

- Aligned to Privacy Act 2020 and IPPs 1–13
- Modular — can be extended with additional sections
- Recognised by Te Whatu Ora and government agencies
- Free and publicly available (privacy.org.nz)
- Structure: (i) project description, (ii) information flow mapping, (iii) IPP-by-IPP assessment, (iv) risk register, (v) mitigations, (vi) sign-off

**Why OPC PIA Toolkit as the base:** it is the NZ-native default; regulators and Te Whatu Ora procurement teams expect it; it satisfies the "DPIA" language in the MBIE deliverable (OPC uses "PIA" — but DPIA is the internationally recognised name for the same exercise and OPC materials treat them as equivalent).

**Known limitation:** the OPC PIA Toolkit is **generic** — it does not address AI-specific risks such as training data provenance, model drift, shortcut learning, hallucination, explainability, or contextual reasoning failure. These must be added via extensions.

### 8.2 AI-Specific Extensions Required on Top of OPC PIA

The following four frameworks are layered onto the OPC base to address AI-specific risks:

#### 8.2.1 UK ICO AI and Data Protection Risk Toolkit / AI DPIA Template

- UK Information Commissioner's Office published the "AI and Data Protection Risk Toolkit" and an AI-specific DPIA template
- Directly addresses: training data lawfulness, bias and discrimination, explainability, data minimisation in model training, automated decision transparency
- **Acceptable basis in NZ** because ICO's AI DPIA structure maps cleanly onto NZ IPPs — most sections translate 1:1
- Use as a **prompt list** for AI-specific questions to include in the OPC PIA risk register
- NZ-specific adaptation: replace UK GDPR Article 35 framing with NZ Privacy Act 2020 and HIPC 2020 language

#### 8.2.2 NIST AI Risk Management Framework 1.0 + Generative AI Profile (NIST AI 600-1)

- NIST AI RMF 1.0 (January 2023) — the most widely adopted AI risk framework internationally, applicable across sectors
- **NIST AI 600-1 Generative AI Profile (July 2024)** — addresses LLM-specific risks: confabulation (hallucination), CBRN information leakage, data privacy, information integrity, value chain and component integration
- Four core functions: **Govern, Map, Measure, Manage**
- Use as a **structural scaffold** for the Governance section of the DPIA and the post-market surveillance plan
- Forward-compatible with US FDA Predetermined Change Control Plan expectations and likely future NZ Medical Products Bill requirements

#### 8.2.3 ISO/IEC 42001:2023 AI Management System + AIIA (AI System Impact Assessment)

- **ISO/IEC 42001:2023** — the world's first AI management system standard (December 2023). Certifiable. Structured like ISO 27001 (which NexWave will pursue) — management system + controls.
- **AI System Impact Assessment (AIIA)** — a formal artefact within ISO 42001 that parallels a DPIA but focuses on AI-specific harms (fairness, safety, transparency, accountability, human oversight)
- Use as the **long-term target standard** — build the DPIA to be "AIIA-ready" so NexWave can pursue ISO 42001 certification post-grant without re-papering
- Directly addresses the Heidi Health failure pattern (Section 9.1): ISO 42001 requires documented human oversight architecture and explicit capability boundaries

#### 8.2.4 NHS DCB0129 / DCB0160 Clinical Safety Case

- **DCB0129** — clinical risk management requirements for **manufacturers** of health IT systems
- **DCB0160** — the companion standard for **deploying organisations**
- Both are NHS Digital standards but widely recognised internationally as the mature clinical safety framework for health IT
- Output: a **Clinical Safety Case Report** authored by a Clinical Safety Officer (a registered clinician — Ryo qualifies)
- **Why include this:** the Medical Products Bill commencement (~2030) will require formal clinical safety documentation. Building a DCB0129-aligned Clinical Safety Case now produces a deliverable that (i) satisfies MBIE Capability Development, (ii) reassures early Medtech / practice customers, (iii) positions NexWave for future SaMD classification without re-work.
- Ryo as Clinical Safety Officer is a natural fit given his GP registration.

### 8.3 Supporting Frameworks (Reference-Only)

The following frameworks were reviewed and are **not** recommended as primary extensions but are cross-referenced:

- **NEAC (National Ethics Advisory Committee) 2022 guidance — "National Ethical Standards for Health and Disability Research and Quality Improvement"** — §12 (health data) and §13 (new technologies) are directly relevant and should be cited in the DPIA's ethical framing section
- **Te Whatu Ora Health Information Governance** — operational guidance, not a DPIA framework
- **HDR UK Five Safes Framework** — data access pattern, not a DPIA template
- **Singapore Model AI Governance Framework** — reviewed; ISO 42001 now supersedes as the certifiable standard
- **EU AI Act** — not directly applicable to NZ but informative for high-risk AI obligations

### 8.4 Recommended 13-Section DPIA Structure for NexWave Inbox Helper + Care Gap Finder

Assembled from the OPC base + the four extensions above, the NexWave DPIA should have the following structure:

1. **Project description and scope** — Inbox Helper + Care Gap Finder, assist-only posture, target users, deployment model (Medtech/Indici integration via ALEX FHIR API)
2. **Stakeholder mapping** — GPs, practice managers, patients, Medtech, Te Whatu Ora, Privacy Commissioner, Medsafe, NAIAEAG
3. **Information flow mapping** — end-to-end data flow from PMS → inbox → extraction → LLM inference → classification → GP UI → audit log; with explicit sovereignty boundaries marked at every hop
4. **Lawful basis and Privacy Act mapping** — IPP-by-IPP assessment (Rules 1–13 of HIPC 2020); explicit treatment of Rule 5 storage, Rule 8 accuracy, Rule 11 disclosure, IPP 12 cross-border, Rule 12 unique identifiers
5. **AI-specific risk register** (from ICO AI DPIA + NIST AI 600-1):
   - Training data provenance and lawfulness
   - Hallucination and confabulation
   - Contextual reasoning failure (NHS GPT-oss 6:1 pattern)
   - Shortcut learning and spurious correlation
   - Model drift and degradation
   - Bias and disparate impact (ethnicity, age, deprivation)
   - Explainability and interpretability
   - Data leakage via prompts or logs
   - Adversarial manipulation (Heidi Health pattern)
6. **Clinical safety case** (DCB0129-aligned) — hazard log, severity and likelihood matrix, controls, residual risk, Clinical Safety Officer sign-off (Ryo)
7. **Technical and organisational controls** — encryption, access control, audit logging, human-in-the-loop architecture, abstention paths, escalation paths, rollback procedures
8. **Sovereignty posture and cross-border data flow** — explicit statement of where data is processed (Bedrock ap-southeast-6 + cross-region to ap-southeast-2/4 where applicable; Catalyst Cloud NZ; or synthetic-data-only overseas R&D environments); IPP 12 analysis
9. **Automated decision-making disclosure** (Privacy Amendment Act 2025 IPP 3A) — disclosure text to patients and GPs, opt-out mechanisms, correction rights
10. **Bias, fairness, and equity assessment** — disaggregated evaluation across ethnicity, age, NZDep, with explicit treatment of Māori and Pacific populations; Te Tiriti o Waitangi framing
11. **Post-market surveillance and monitoring plan** (NIST AI RMF Manage function) — drift detection, incident reporting, model update cadence, feedback loop to risk register
12. **Governance and human oversight architecture** — roles (Clinical Safety Officer, Privacy Officer, Data Controller), review cadence, change management
13. **Sign-off** — Clinical Safety Officer, Privacy Officer, senior clinical reviewer, executive sponsor

### 8.5 DPIA Deliverable Cadence for the Grant Period

- **Sprint 2 (Apr 2026):** DPIA **methodology document** — this section + appendices; no patient data yet, so this is the framework not the assessment
- **Sprint 3–4 (May 2026):** first-draft DPIA against synthetic dataset workflow
- **Objective 2 kickoff (~Sep 2026):** full DPIA against real-data pipeline; Privacy Commissioner engagement
- **Capability Development deliverable (due Sep 2026 per MBIE grant):** DPIA methodology + first full DPIA instance
- **Pre-deployment (2027):** clinical safety case finalised; ISO 42001 readiness review

### 8.6 Why This Layered Approach

- **OPC PIA** is the NZ-native regulator-facing base
- **ICO AI DPIA** provides the AI-specific risk prompt list
- **NIST AI RMF + GenAI Profile** provides the governance scaffold and LLM-specific risk taxonomy
- **ISO/IEC 42001 AIIA** makes the DPIA forward-compatible with certifiable AI management system standards
- **DCB0129/DCB0160 Clinical Safety Case** makes the DPIA forward-compatible with SaMD expectations (NZ Medical Products Bill commencement ~2030, TGA Class IIa, FDA PCCP)

Each layer adds one specific capability the layer below lacks. No layer alone is sufficient. The combined artefact satisfies MBIE's DPIA deliverable, positions NexWave for future SaMD regulation, and is defensible to the Privacy Commissioner and Te Whatu Ora procurement.

---

## 9. NZ Health AI Precedents — Infrastructure and Sovereignty Postures

Published positions from NZ-active health AI and health IT vendors, with specific focus on what is publicly disclosed about hosting, data handling, and regulatory posture.

### 9.1 Heidi Health — The Most Informative Precedent (Both Positive and Cautionary)

**Deployment scale:** November 2025 government contract for **1,000 ED clinician licences** announced by Minister Simeon Brown; rollout to all 16 largest NZ EDs in progress.

**Product scope:** Clinical documentation scribing — notes, summaries, letters to GPs. **Not inbox triage.** Heidi is explicitly positioned as a note-taker, not a diagnostic tool. This administrative classification was key to avoiding SaMD regulation.

**Hosting and data handling (public):**
- Australian-headquartered, operates across ANZ
- Public statements emphasise data residency and clinical-grade infrastructure; exact hosting region not always disclosed in public materials
- Integrates with NZ EHRs/PMSs (Medtech, Indici, HealthOne)
- Clinician-facing product — ambient capture of consultation audio, transcription, structured note generation
- Uses cloud LLMs; has not publicly disclosed whether it has moved to Bedrock ap-southeast-6 post-March 2026 launch

**The March 2026 security disclosure (critical lesson for NexWave):**
- **Source:** newsroom.co.nz, 20 March 2026
- **Finding:** Mindgard security researchers bypassed Heidi's guardrails in three prompts, causing Heidi to provide diagnostic suggestions and treatment recommendations — behaviour outside its declared administrative scope
- **Quote summary:** Heidi "broke a promise that was key to getting into the medical field: that Heidi was just a note-taker and could not provide diagnostic input"
- **Implications:**
  1. "Assist-only" classification is **not self-enforcing**. A product can be reclassified as SaMD de facto if its guardrails are bypassable.
  2. Guardrail robustness is a regulatory concern, not just a product-quality concern.
  3. Architectural enforcement (structural inability to act, not just UI caps) is stronger than prompt-based guardrails.
  4. Security researcher adversarial testing should be part of pre-deployment validation.

**What NexWave must do differently:**
- Architecturally separate the extraction/classification layer from the action layer — the LLM never acts, only suggests
- Adversarial red-team testing before deployment (incorporate into Sprint 5–6)
- Treat the Heidi disclosure as a hazard in the DPIA risk register

### 9.2 Medtech Global (Medtech Evolution)

**Sovereignty posture:** Medtech Evolution Cloud is marketed explicitly as "hosted in New Zealand, so you have the added security of knowing your data will not leave the country." This is the strongest-possible sovereignty claim from the dominant NZ PMS vendor.

**Relevance to NexWave:**
- Medtech customers expect NZ-resident data handling from AI integrations
- The ALEX FHIR API is the sanctioned integration path (covered in R6)
- Any NexWave architecture that moves Medtech-sourced data offshore — even to Sydney or Melbourne via Bedrock cross-region inference — will need explicit contractual and DPIA justification

**Medtech AI (the competitor product):** Medtech Global has its own native AI capability (positioned as first-party). Public materials are thin on hosting details but the parent product's NZ-hosting claim implies NZ-resident inference. This is a competitive benchmark NexWave must at least match.

### 9.3 Orion Health

**Sovereignty posture:** Orion is a NZ-origin health informatics company (Auckland HQ) with international deployments. Public materials describe cloud-native population health and care coordination products.

**Cloud relationship:** Orion has publicly discussed AWS partnerships; with Bedrock now live in ap-southeast-6, Orion is a likely early customer for NZ-hosted generative AI in health (though no specific deployment has been publicly confirmed as of April 2026).

**Relevance to NexWave:** Orion's presence in the NZ market normalises AWS as a credible NZ health cloud vendor, even before the ap-southeast-6 launch. Cite as precedent when explaining the Bedrock posture to Te Whatu Ora procurement.

### 9.4 Volpara Health

**Profile:** NZ-origin (Wellington) breast imaging AI company; ASX-listed; products in use across US and international markets.

**Regulatory precedent:** Volpara is **SaMD-classified** in multiple jurisdictions (TGA, FDA). Volpara's regulatory posture is the NZ precedent for a NZ-origin AI product navigating TGA Class IIa and FDA clearance in parallel.

**Relevance to NexWave:** Volpara has walked the SaMD path that NexWave expects to encounter when the Medical Products Bill commences (~2030) — so Volpara's published materials and any publicly available regulatory filings are worth studying for precedent.

### 9.5 Health Accelerator

**Profile:** NZ RPA-first automation vendor targeting NZ general practice. Products: CVDRA automation, ACC claims reconciliation, specialist referral acknowledgement filing, normal FIT result filing.

**Regulatory posture:** Deliberately **rule-based RPA, not AI/SaMD**. Every product is structured so it cannot be classified as a medical device — no semantic reasoning, no LLM, no diagnostic suggestion. This is the **defensive-by-design** posture: do less so you don't need to prove more.

**Relevance to NexWave:** Health Accelerator is the competitor NexWave differentiates against (AI reasoning + ALEX integration). But Health Accelerator's posture is instructive: they have chosen to avoid the SaMD compliance burden entirely by staying rule-based. NexWave's value is exactly in the reasoning Health Accelerator deliberately avoids — which means NexWave **inherits the regulatory burden** Health Accelerator sidesteps. The DPIA, clinical safety case, and sovereignty posture must be airtight.

### 9.6 BPAC NZ (Best Practice Advocacy Centre)

**Profile:** NZ clinical decision support and education non-profit; Medtech-integrated tools; Dunedin-based.

**Products:** BPAC CS Inbox Manager (rule-based, Medtech-integrated); clinical audits; evidence-based guidance integrated into GP workflows.

**Regulatory and sovereignty posture:** NZ-based, NZ-hosted, rule-based. No LLM. Trusted infrastructure partner to NZ general practice.

**Relevance to NexWave:** BPAC is the incumbent rule-based competitor for care gap workflows. NexWave's competitive position is "BPAC's clinical rigour + AI reasoning + ALEX API access". Preserve the clinical rigour framing — BPAC is trusted because its rules are transparent; NexWave's LLM reasoning must be equally transparent (explainability in the DPIA).

### 9.7 Summary — What NexWave Learns From Precedents

| Precedent | Lesson |
|---|---|
| Heidi Health Nov 2025 | Government will contract NZ AI at scale — market is open |
| Heidi Health Mar 2026 disclosure | "Assist-only" must be architecturally enforced; adversarial testing is mandatory |
| Medtech Evolution Cloud | NZ-resident data handling is the market expectation; any offshore hop needs justification |
| Medtech AI | First-party native AI is a competitive baseline NexWave must meet on accuracy and sovereignty |
| Orion Health | AWS partnership normalised in NZ health; Bedrock ap-southeast-6 is credible |
| Volpara Health | SaMD precedent for NZ-origin AI products navigating TGA/FDA |
| Health Accelerator | Rule-based defensive posture avoids regulation but sacrifices reasoning — NexWave accepts the burden |
| BPAC NZ | Rule transparency builds clinical trust — LLM reasoning must be equally transparent |

---

## 10. Recommended Sovereignty Posture for NexWave

This section is the **explicit recommendation** — a single posture the Sprint 2 architecture shortlist (R3) and the DPIA methodology should be built against. The recommendation is hybrid — no single provider satisfies all constraints.

### 10.1 Recommended Posture — Tiered Hybrid

| Tier | Role | Provider | Data Scope | Rationale |
|---|---|---|---|---|
| **Primary (managed-closed)** | Production inference for Claude-family models | **AWS Bedrock ap-southeast-6 (Auckland), AU geographic inference profile** | All real clinical data, synthetic data | Only NZ-native managed-service path for frontier Claude models; AU geographic boundary keeps data within ANZ; AWS has a NZ entity and published NZ Region launch; acceptable under agent/processor doctrine with IPP 12 + DPIA |
| **Primary (self-hosted-open)** | Production inference for open-weight models (Llama, Qwen, BioClinical ModernBERT) | **Catalyst Cloud NZ — C1A RTX A6000 48GB (GA)** | All real clinical data, synthetic data | Only fully NZ-sovereign provider (NZ-owned, NZ-operated, NZ data centres); C1A is the only safe GA GPU anchor after C2 A100-slice retirement 31 March 2026; single-provider risk accepted with Datacom contingency |
| **Secondary (overseas, synthetic-only)** | R&D throughput for open-weight model experimentation where Catalyst capacity is constrained | **Together AI dedicated endpoints (US/EU, SOC 2 + HIPAA BAA)** | **Synthetic data only** — never real clinical data | Enterprise tier with dedicated tenancy is the only defensible overseas option; synthetic-only scope sidesteps IPP 12 and MBIE N2RD grant ambiguity |
| **Contingency** | Bedrock or Catalyst failure, surge capacity | **Datacom Sovereign Cloud (NZ)** | All scopes | NZ-sovereign, government-approved, but no public SKU/pricing — keep as contingency pending direct engagement |
| **Ruled out** | — | Runpod, Lambda Labs, Modal, CoreWeave, Fireworks, serverless multi-tenant | — | No HIPAA BAA (Runpod, Lambda), wrong economics (CoreWeave), multi-tenancy concerns for clinical data, overseas-only for real data creates IPP 12 and MBIE exposure |

### 10.2 Defensibility Rationale

**To the Privacy Commissioner and Te Whatu Ora:**
- All **real clinical data** is processed within ANZ — either in NZ (Catalyst C1A) or across the AU geographic inference profile (Bedrock ap-southeast-6/2/4)
- No real clinical data touches US or EU infrastructure at any point
- AWS is accepted as an "agent" under the OPC 2020 Interpretation agent/processor doctrine — processing is "use not disclosure"
- IPP 12 cross-border obligations are satisfied because the Bedrock AU geographic profile remains within a comparable-privacy regime (Australia's Privacy Act 1988 + APPs)
- HIPC 2020 (updated 1 May 2026) is fully honoured — Rules 5, 8, 11, and 12 addressed in the DPIA
- HISO 10029.4:2025 supplier standard built into the Sprint 3+ technical controls
- Heidi Health March 2026 lesson is addressed by architectural human-in-the-loop enforcement (Section 9.1)

**To MBIE (grant compliance):**
- **Majority of compute spend is onshore** — Catalyst Cloud NZ is the open-model inference anchor, billed in NZD to a NZ-incorporated entity
- Bedrock ap-southeast-6 is an AWS NZ entity where publicly available; worst case it is an AWS Australia entity processing within ANZ
- Together AI synthetic-data-only is scoped to capability-development R&D experimentation, not primary compute — and is structurally separated from the real-data pipeline
- **Target: 90%+ of the NZD $177k compute line remains onshore**
- **Critical caveat:** no MBIE ruling has been published on whether AWS ap-southeast-6 counts as "R&D undertaken in NZ" for N2RD purposes — this is the highest-priority escalation (Section 11)

**To NexWave customers (GPs and practice owners):**
- Aligns with Medtech Evolution Cloud's "your data will not leave the country" posture
- Catalyst Cloud and the Bedrock ap-southeast-6 positioning can both be explained in plain language to GPs
- No dependence on US cloud for real patient data

### 10.3 Architectural Implications for R3 and Sprint 3

- **R3 architecture shortlist must include:**
  1. At least one Bedrock-ap-southeast-6 Claude candidate (Haiku 4.5 / Sonnet 4.6, AU geographic profile)
  2. At least one Catalyst Cloud C1A self-hosted open-model candidate (Llama 3.3 70B INT4 / Qwen 2.5 72B INT4 / BioClinical ModernBERT 396M fine-tuned)
  3. At least one hybrid rules + LLM candidate that minimises LLM calls (reducing sovereignty surface area)
  4. At least one multi-agent candidate (reflecting 2025–2026 agentic pattern from R1)
- **R3 candidates must NOT rely on:**
  - Catalyst Cloud C2 A100-slice (retiring 31 March 2026)
  - Runpod, Lambda, Modal, CoreWeave, Fireworks for real clinical data
  - Any serverless multi-tenant inference for identifiable data
- **Sprint 3 validation priorities:**
  1. Confirm Claude Haiku 4.5 / Sonnet 4.6 availability in AU geographic inference profile (tested from ap-southeast-6 client)
  2. Provision Catalyst C1A RTX A6000 48GB and benchmark open-model throughput
  3. Provision Together AI dedicated endpoint for synthetic-data R&D parallelism
  4. Log formal enquiry to MBIE Innovation Services

### 10.4 Single Recommendation If Forced to Pick One

If forced to pick a **single** posture rather than hybrid: **AWS Bedrock ap-southeast-6 with the AU geographic inference profile, as the production runtime for Claude Haiku 4.5 and Claude Sonnet 4.6, with Catalyst Cloud C1A held as the sovereign-critical fallback for any workload the customer contractually requires to stay onshore**.

But this is weaker than the tiered hybrid. The tiered hybrid is the recommendation.

---

## 11. Open Questions to Raise With Regulators and Providers

Consolidated escalation list. These questions block or materially affect the Sprint 2 and Sprint 3 delivery and should be opened as dated items in the nexwave-rd dashboard.

### 11.1 MBIE Innovation Services (N2RD grant compliance) — HIGHEST PRIORITY

1. Does cloud compute consumed in AWS ap-southeast-6 (Auckland) count as "R&D undertaken in New Zealand" for N2RD eligibility?
2. Does cloud compute consumed on Catalyst Cloud NZ (Wellington / Porirua / Auckland data centres, NZ-owned entity) count as "R&D undertaken in New Zealand"?
3. What is the MBIE position on cloud compute where the inference routes across a geographic inference profile (ANZ-bounded but not NZ-pinned)?
4. Is synthetic-data-only R&D experimentation on overseas dedicated tenancy (e.g. Together AI US/EU) permissible during capability development, provided no real clinical data is processed?
5. Is there any published MBIE or Callaghan Innovation guidance on cloud-compute eligibility that we have missed?

**Contact path:** MBIE Innovation Services direct + Lisa Pritchard at Callaghan Innovation (NexWave's existing grant relationship).

### 11.2 AWS New Zealand Team

1. Which specific Claude model IDs are live in ap-southeast-6 natively vs routed via cross-region inference? (Haiku 4.5, Sonnet 4.6, Opus 4.6, Sonnet 4.5, Sonnet 4)
2. What is the exact route taken by the AU geographic inference profile when called from an ap-southeast-6 client? (ap-southeast-6 / ap-southeast-2 / ap-southeast-4)
3. Is there any mechanism — current or on the roadmap — to pin Bedrock inference to ap-southeast-6 only, with no cross-region fall-through?
4. Is the AWS BAA / HIPAA-equivalent contract available to NZ customers, and does it cover Bedrock inference in ap-southeast-6 and the AU geographic profile?
5. What logging, abuse monitoring, and zero-data-retention options apply to Bedrock inference in ap-southeast-6?
6. Published pricing for Bedrock inference in ap-southeast-6 — is it the same as Sydney (ap-southeast-2) or different? Are there any NZD-native billing options?
7. Any NZ health customers publicly confirmed on Bedrock ap-southeast-6 since March 2026? (Orion, Volpara, Heidi, Te Whatu Ora?)

**Contact path:** AWS NZ Health vertical team; AWS Partner Network for ISV engagement.

### 11.3 Catalyst Cloud

1. **Confirmed:** C2 A100 20GB slices are retiring 31 March 2026 — what is the migration pathway for customers on C2?
2. Will C3 L40S 48GB move from Beta (Porirua-only) to GA, and when? Other region availability?
3. Current NZD/hour published pricing for C1A RTX A6000 48GB, C3 L40S 48GB, and any new GPU SKUs on the roadmap
4. Is there any A100 or H100 GA capacity planned for 2026, or is L40S / A6000 the terminal GPU generation?
5. SLA for C1A production inference workloads — uptime, support response, failover
6. Certifications: ISO 27001, IRAP (AU), HISO alignment, HIPAA-equivalent
7. Published Healthify case study or any NZ health customers using Catalyst GPU in production

**Contact path:** Catalyst Cloud sales + technical solutions engineering. Ryo or Ting to log into the official cost calculator and capture exact NZD/hour figures before any number from this report lands in the MBIE Q1 narrative.

### 11.4 Office of the Privacy Commissioner

1. Any published AI guidance updates since the September 2023 "AI and the Information Privacy Principles" — particularly addressing generative AI and LLM-based clinical decision support?
2. Is the agent/processor doctrine (OPC October 2020 Interpretation) still the operative position in 2026, or has it been updated?
3. Does processing clinical data via AWS Bedrock ap-southeast-6 with AU geographic cross-region inference satisfy IPP 12 by being ANZ-bounded?
4. Any published precedent or decision on LLM-based clinical decision support under HIPC 2020?
5. Guidance on Privacy Amendment Act 2025 IPP 3A (automated decision-making transparency) in force May 2026 — what disclosure form is expected for assist-only AI-CDS?

**Contact path:** OPC policy team; can be submitted as a formal enquiry with anonymised project description.

### 11.5 NAIAEAG (National AI & Algorithm Expert Advisory Group, Health NZ)

1. Does the Health NZ AI governance framework apply to a private-sector AI-CDS vendor deploying into NZ general practice (as opposed to a Te Whatu Ora-commissioned tool)?
2. Any guidance on adversarial robustness testing requirements post the Heidi Health March 2026 disclosure?
3. Is there a pathway for early engagement with NAIAEAG during product development rather than post-hoc review?
4. Expected evidence package for "assist-only" classification to hold under scrutiny

**Contact path:** via Te Whatu Ora AI governance channels.

### 11.6 Medsafe

1. Current Medsafe position on AI-CDS classification under the Medicines Act 1981 in the pre-Medical-Products-Bill era
2. WAND notification requirements for assist-only LLM-based CDS
3. Any published guidance on pre-commencement transitional expectations for SaMD-like products
4. Clinical safety case (DCB0129 equivalent) expectations for NZ submissions

**Contact path:** Medsafe direct.

### 11.7 Medtech Global (Medtech Evolution)

1. What sovereignty contract terms apply to data accessed via the ALEX FHIR API and processed by a third-party AI vendor?
2. Are there approved hosting regions for third-party integrations that process Medtech-sourced data?
3. Certification or due-diligence requirements for ALEX API partners processing data with LLM-based reasoning

**Contact path:** Medtech partner programme (covered in R6).

---

## 12. Reference List

### 12.1 AWS Bedrock and ap-southeast-6

- AWS, "Run generative AI inference with Amazon Bedrock in Asia Pacific (New Zealand)", AWS Machine Learning Blog, March 2026. https://aws.amazon.com/blogs/machine-learning/run-generative-ai-inference-with-amazon-bedrock-in-asia-pacific-new-zealand/
- AWS, "Amazon Bedrock User Guide — Models and Regions" (docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) — access-blocked to automated agents; confirmation required via direct AWS NZ engagement
- AWS, "AWS Asia Pacific (New Zealand) Region launch announcement", September 2025
- AWS, "Cross-region inference in Amazon Bedrock" — documentation on inference profiles and geographic routing
- AWS, "HIPAA Eligible Services Reference" — covers Bedrock eligibility in BAA-supported Regions
- AWS Healthcare Compliance — BAA and NZ customer engagement

### 12.2 Catalyst Cloud and NZ Providers

- Catalyst Cloud, GPU-as-a-Service product page — https://catalystcloud.nz/services/gpu/
- Catalyst Cloud, Pricing and Cost Calculator — https://catalystcloud.nz/pricing/price-list/ (403-blocked to agents; direct customer login required)
- Catalyst Cloud, "C2 GPU retirement 31 March 2026" — migration notice
- Catalyst Cloud, C3 L40S 48GB Beta announcement (Porirua)
- Catalyst Cloud, Healthify case study
- Datacom, "Datacom Sovereign Cloud" — marketing materials, SKU and NZD pricing not public
- CCL (Computer Concepts Limited) / Spark Cloud — GPU compute availability (no public SKU for LLM workloads)
- getdeploying.com — peer-provider benchmark pricing for A6000, L40S cross-reference

### 12.3 NZ Privacy Act, HIPC, and OPC Guidance

- Privacy Act 2020 (New Zealand) — https://www.legislation.govt.nz/act/public/2020/0031/latest/LMS23223.html
- Health Information Privacy Code 2020 (HIPC 2020) — https://www.privacy.org.nz/publications/codes-of-practice/health-information-privacy-code-2020/
- HIPC 2020 Amendment (in force 1 May 2026)
- Privacy Amendment Act 2025 — IPP 3A on automated decision-making transparency (in force May 2026)
- Office of the Privacy Commissioner, "Artificial intelligence and the Information Privacy Principles", September 2023
- Office of the Privacy Commissioner, 2020 Interpretation on cross-border disclosure and agent/processor doctrine (October 2020)
- Office of the Privacy Commissioner, PIA Toolkit (2024 update)

### 12.4 Medical Products Bill and Medsafe

- MoH briefing, "Supporting innovation through the Medical Products Bill", August 2025
- Russell McVeagh, "Prescription for change" — Medical Products Bill commentary, August 2025
- NZ Nurses Organisation, Medical Products Bill update, August 2025
- Buddle Findlay, Medical Products Bill commentary, August 2025
- Medsafe, WAND notification framework — current regime guidance

### 12.5 DPIA and AI Governance Frameworks

- UK Information Commissioner's Office, "Guidance on AI and data protection" and AI DPIA template — https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/
- NIST AI Risk Management Framework 1.0 (January 2023) — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1, "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile", July 2024
- ISO/IEC 42001:2023, "Artificial intelligence — Management system" — https://www.iso.org/standard/81230.html
- NHS Digital, DCB0129 — Clinical Risk Management: Its Application in the Manufacture of Health IT Systems
- NHS Digital, DCB0160 — Clinical Risk Management: Its Application in the Deployment and Use of Health IT Systems
- NEAC (National Ethics Advisory Committee), "National Ethical Standards for Health and Disability Research and Quality Improvement", 2022 — §12 (health data), §13 (new technologies)

### 12.6 HISO and Te Whatu Ora Standards

- HISO 10029:2022 Health Information Security Framework (with sub-parts 10029.1–10029.4)
- HISO 10029.4:2025 Suppliers — the supplier-facing security standard directly relevant to NexWave
- HISO 10064 Health Information Governance Guidelines
- HISO 10001:2017 Ethnicity Data Protocols
- HISO 10071:2025 CVDRA PREDICT Equations (covered in R4)
- Te Whatu Ora, Health Information Governance framework and policies
- NAIAEAG — National AI & Algorithm Expert Advisory Group (Health NZ)

### 12.7 NZ Health AI Precedents

- newsroom.co.nz, "Heidi Health security flaw exposed by researchers", 20 March 2026 — guardrail bypass by Mindgard researchers
- Minister Simeon Brown press release, November 2025 — 1,000 Heidi Health ED clinician licences contract
- Medtech Global, Medtech Evolution Cloud marketing — "hosted in New Zealand" sovereignty claim
- Orion Health — AWS partnership public materials
- Volpara Health — TGA and FDA SaMD regulatory filings (public)
- Health Accelerator — product scope materials (rule-based RPA posture)
- BPAC NZ — BPAC Clinical Solutions Inbox Manager product materials

### 12.8 Overseas Cloud Providers

- Runpod Secure Cloud — SOC 2 Type II and HIPAA eligibility documentation (no published GA BAA as of April 2026)
- Modal — Series B Sep 2025 press; Enterprise BAA on request
- Lambda Labs — on-demand VM catalogue (serverless deprecated September 2025); no BAA
- CoreWeave — HIPAA-eligible enterprise GPU fleet
- Together AI — dedicated endpoints, SOC 2, HIPAA BAA
- Fireworks AI — enterprise tier documentation

### 12.9 MBIE Grant Compliance

- MBIE, "New to R&D Grant (N2RD)" programme terms — CONT-109091-N2RD-NSIWKC
- Callaghan Innovation, R&D grant guidance materials
- MBIE N2RD grant contract — "R&D undertaken outside New Zealand is not eligible" clause (requires direct interpretation from MBIE Innovation Services)

### 12.10 Internal Cross-References

- `context/nexwave-rd-context/inbox-helper-task-spec.md` — Inbox Helper task specification (locked)
- `context/nexwave-rd-context/care-gap-finder-task-spec.md` — Care Gap Finder task specification (locked)
- `context/nexwave-rd-context/research-r1-llm-architecture-benchmarks.md` — Clinical LLM architecture benchmarks (R1)
- `context/nexwave-rd-context/Urgency classification for GP inbox triage.md` — urgency taxonomy research
- `context/nexwave-rd-context/Evaluation metrics for ordinal clinical AI triage classification.md` — evaluation metrics research
- `dashboards/nexwave-rd.md` — programme dashboard and compliance deadlines

---

**End of R2 Research Report.**
