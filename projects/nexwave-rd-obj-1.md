---
id: nexwave-rd-obj-1
status: active
type: rd
repo: nexwave-rd
stack: [aws-bedrock, claude-haiku, claude-sonnet, python]
---

# NexWave R&D — Objective 1: Foundation AI Architecture

| Field | Detail |
|---|---|
| Period | Months 1–6 \| March–June 2026 |
| Status | Active |
| Budget | $177,396 |
| Contract | CONT-109091-N2RD-NSIWKC |

---

## High-Level Objective

Pick the right AI architecture that works for NZ GPs under sovereignty rules, and prove it works on synthetic data by end of June 2026.

---

## Context: The Two Products Being Built

**Inbox Helper** — reads incoming clinical documents (lab results, hospital letters, radiology reports, patient messages) and suggests urgency and action. GP makes every decision; AI surfaces information faster.

**Care Gap Finder** — scans a GP's patient list and identifies patients overdue for important health checks (e.g. diabetic patient with no HbA1c in 12 months).

Key rule: AI assists only. Never makes a clinical decision.

---

## Key Deliverables (due end of June 2026)

| Deliverable | Status |
|---|---|
| Medtech and Indici sandbox environments connected | Not Started |
| Architecture selected with documented evidence | Not Started |
| Data requirements documented (types and volumes) | Not Started |
| Triage prototype hitting ≥90% accuracy on synthetic data | Not Started |
| CVDRA prototype hitting ≥95% accuracy on synthetic data | Not Started |

---

## The Four Goals

| Goal | Description | Owner | Due | Status |
|---|---|---|---|---|
| Goal A — Sandbox Environments Connected | Connect Medtech and Indici sandbox environments | Ryo | — | In Progress |
| Goal B — Architecture Decision Made and Documented | Evaluate RAG vs fine-tune vs prompt-engineering vs hybrid. Document decision with evidence for MBIE. | Ryo | April 2026 | Not Started |
| Goal C — Data Requirements Documented | Document what data types and volumes the AI needs | Ryo | — | Not Started |
| Goal D — Triage and CVDRA Prototypes Hitting Accuracy Targets | Prototypes on synthetic data: ≥90% triage, ≥95% CVDRA accuracy. Evidence required for Q1 MBIE claim. | Both | June 2026 | Not Started |

---

## Execution Roadmap

Sequential steps to achieve Objective 1.

### Step 1: Define the Problems Clearly

Lock in precise definitions for both tasks:

**Triage task:** What are the inputs (lab results, discharge summaries, etc.)? What are the outputs (urgency level, suggested action)? What counts as success (≥90% accuracy on what, exactly)?

**Care Gap Detection task:** What data do you need? What's the clinical logic? What are the edge cases? What counts as success (≥95% accuracy)?

Deliverable: Clear written definition of both tasks with success criteria.

### Step 2: Literature Review and Architecture Research

Research what's already been done:
- Clinical NLP and LLM benchmarks in similar domains
- Sovereign AI options available in NZ
- AWS Bedrock capabilities within data residency constraints (ap-southeast-2)
- RAG vs fine-tune vs prompt-engineering vs hybrid trade-offs

Deliverable: Literature review document.

### Step 3: Shortlist Architecture Candidates (3–4 approaches)

Document for each:
- How it meets triage and care gap requirements
- Trade-offs (accuracy, speed, cost, sovereignty compliance)
- Why it's worth evaluating

Deliverable: Architecture shortlist with documented rationale.

### Step 4: Evaluate Candidates on Synthetic Data

Run systematic experiments on synthetic data for each candidate:
- Triage: aim for ≥90% accuracy
- CVDRA/care gap: aim for ≥95% accuracy
- Log all results

Deliverable: Experiment results, systematically logged.

### Step 5: Make the Architecture Decision

Pick one. Document:
- Why you picked it
- Evidence from Step 4
- How it meets sovereignty requirements
- What data it needs to progress to real GP data

Deliverable: Architecture decision document for MBIE.

---

## Compliance & Key Dates

| Item | Date |
|---|---|
| PAYE evidence for Ting | 30 April 2026 |
| Q1 MBIE claim due | 31 May 2026 |
| Obj 1 deliverables due | End of June 2026 |

MBIE contact: Lisa Pritchard (Callaghan Innovation). All experiments must be logged.

---

## Sprints

```dataviewjs
const active = dv.pages('"sprints/active"')
  .where(p => p.objective === "obj-1");
const archived = dv.pages('"sprints/archive"')
  .where(p => p.objective === "obj-1");
const pages = active.concat(archived).sort(p => p.start);
const headers = ['Sprint', 'Goal', 'Start', 'End', 'Status'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.id), p.goal, p.start, p.end, p.status
]));
```
