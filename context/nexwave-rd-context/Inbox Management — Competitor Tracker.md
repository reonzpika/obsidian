# Inbox Management — Competitor Tracker

> This page tracks competitors in the GP inbox management space as it relates to Nexwave's **Inbox Helper** and **Care Gap Finder** R&D objectives. Scope is deliberately narrow: inbox triage, filing, and clinical decision support on incoming documents. Scribe tools are excluded unless expanding into inbox workflows.

The key differentiator to track for every competitor: **integration method** (API vs RPA vs native). This determines their ceiling.

**Last updated:** 25 March 2026

---

## Competitors

### 1. Health Accelerator — RPA Inbox Bots
> **Threat level: 🔴 High**

| Field | Detail |
| --- | --- |
| **What they are** | JV of Pegasus, Pinnacle, ProCare, and Tū Ora Compass Health — 500+ practices, 2M patients across NZ |
| **Product** | RPA-based "digital assistants" (rule-based, not AI) — two inbox bots live |
| **Integration method** | RPA — robotic process automation, rule-based, no AI reasoning |
| **PMS coverage** | Indici now; actively negotiating with Medtech Global |
| **Stage** | Live and scaling. Launched July 2025. |
| **Team / backing** | Funded JV of four major PHOs. CEO Paul Roseman. Institutional distribution. |
| **Overlap with Nexwave** | Inbox filing and triage — same workflow, different approach |
| **Key vulnerability** | Rule-based only. Cannot handle edge cases or clinical reasoning. Brittle to PMS UI changes. |
| **Watch trigger** | Medtech Global partnership announcement — if RPA bots go live on Medtech, they reach your primary market first |

---

### 2. Medtech AI
> **Threat level: 🔴 High**

| Field | Detail |
| --- | --- |
| **What they are** | First-party AI product from Medtech Global, built natively into Medtech Evolution |
| **Product** | Real-time transcription, structured clinical notes. Currently a scribe product. |
| **Integration method** | Native — built directly into the PMS |
| **PMS coverage** | Medtech Evolution only (~75–85% of NZ general practices) |
| **Stage** | Live |
| **Team / backing** | Medtech Global — established, first-party advantage |
| **Overlap with Nexwave** | Adjacent now (scribe). Becomes existential if they extend into inbox triage and care gap detection. |
| **Key vulnerability** | Medtech moves slowly. First-party products historically lag third-party innovation. Vendor lock-in some practices resist. |
| **Watch trigger** | Any Medtech AI announcement including inbox triage, result annotation, or care gap identification |

---

### 3. Inbox Magic
> **Threat level: 🟡 Medium**

| Field | Detail |
| --- | --- |
| **What they are** | Auckland startup. Founders: SunKee Hong, Jerry Kim. Both full-time. |
| **Product** | AI-driven inbox triage: summarises discharge letters, annotates abnormals, schedules recalls, files safe normals (excludes PSA) |
| **Integration method** | Screen-scrape / browser automation — no API, no PMS partnership |
| **PMS coverage** | Indici only |
| **Stage** | 3 pilot practices, ~3–4 months in. Actively seeking investment. |
| **Funding** | Pre-revenue, raising now. Has completed a PIA via Collaborative Aotearoa. |
| **Overlap with Nexwave** | Direct — inbox triage is their exact product |
| **Key vulnerability** | Architecturally locked out of Medtech (your primary market). Screen-scraping fragile to UI updates. No scalable path without a PMS partnership. |
| **Watch trigger** | ALEX API access or any Medtech partnership — changes threat level to High immediately |
| **Source** | Direct founder meeting, 25 March 2026 |

---

### 4. BPAC CS Inbox Manager
> **Threat level: 🟢 Low–Medium**

| Field | Detail |
| --- | --- |
| **What they are** | BPAC Clinical Solutions — clinically-led health informatics, NZ/AU/UK. Non-profit shareholder structure. |
| **Product** | Rule-based inbox management for Medtech Evolution. Developed with South Link Health. |
| **Integration method** | Direct Medtech interface. Requires Medtech Evolution 6.0+, Windows 10+, single database only. |
| **PMS coverage** | Medtech only. Does not support multi-database practices. |
| **Stage** | Live, established |
| **Overlap with Nexwave** | Same workflow, no AI. Rule-based decision support vs Nexwave's AI reasoning layer. |
| **Key vulnerability** | Not AI — purely rule-based. No cloud hosting. Single-database constraint. Architecturally legacy. |
| **Watch trigger** | Any BPAC announcement of AI integration or cloud support |

---

### 5. Heidi Health (via Health Accelerator)
> **Threat level: 🟢 Low (for inbox specifically)**

| Field | Detail |
| --- | --- |
| **What they are** | Australian AI scribe. Endorsed by Te Whatu Ora. Distributed via Health Accelerator exclusive pricing deal. |
| **Product** | Real-time consultation transcription and clinical note generation. Scribe only — not inbox management. |
| **Integration method** | Audio capture + LLM, writes structured notes back to PMS |
| **PMS coverage** | Multiple (cloud-native) |
| **Stage** | Live and scaling in NZ |
| **Overlap with Nexwave** | Indirect only. Competing for same GP attention and budget, not the same workflow. |
| **Key vulnerability** | Australian product — NZ data sovereignty concerns. Not focused on inbox triage. |
| **Watch trigger** | Any expansion into post-consultation inbox workflows or result management |

---

## Structural Observations

- **Nobody is using ALEX FHIR API for AI inbox triage yet.** Every current player is either RPA-based or native. This is Nexwave's structural opening.
- **Health Accelerator's Medtech negotiation is the most important thing to watch.** If RPA bots go live on Medtech at scale, they normalise the workflow before Nexwave reaches Obj 4 deployment.
- **Medtech AI is the slow-burn existential risk.** They have the distribution and first-party access — but move slowly. That's the window.
- **Inbox Magic confirms the market exists.** A full-time founding team raising investment validates the pain point. Their architectural constraint is Nexwave's advantage.
- **The moat Nexwave is building (AI reasoning + clinical accuracy + ALEX integration) is not replicable by rule-based RPA tools.** That's the differentiation to protect.

---

## Intel Log

| Date | Source | Competitor | Intel |
| --- | --- | --- | --- |
| 25 Mar 2026 | Direct founder meeting | Inbox Magic | Screen-scrape only. Indici only. No API. No PMS partnerships. 3 pilot practices at ~3–4 months. Actively seeking investment. Both founders full-time. |
