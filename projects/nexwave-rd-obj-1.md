---
id: nexwave-rd-obj-1
status: active
type: rd
repo: nexwave-rd
stack: [aws-bedrock, claude-haiku, claude-sonnet, python]
title: "R&D Objective 1"
description: "Foundation AI architecture for NexWave Health."
phase: "Architecture research and synthetic data design"
dashboard: nexwave-rd
---

# NexWave Health R&D — Objective 1: Foundation AI Architecture

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

**Step 1 complete (5 April 2026):** Inbox Helper task spec and Care Gap Finder task spec both finalised. Stored in `nexwave-rd/docs/obj-1/output/`. Both constitute MBIE evidence for the Step 1 deliverable.

---

## The Four Goals

| Goal | Description | Owner | Due | Status |
|---|---|---|---|---|
| Goal A — Sandbox Environments Connected | Connect Medtech and Indici sandbox environments | Ryo | — | In Progress |
| Goal B — Architecture Decision Made and Documented | Evaluate RAG vs fine-tune vs prompt-engineering vs hybrid. Document decision with evidence for MBIE. | Ryo | April 2026 | In Progress (Sprint 2 shortlist + decision record filed; bake-off pending) |
| Goal C — Data Requirements Documented | Document what data types and volumes the AI needs | Ryo | — | Done (Sprint 2 data requirements filed) |
| Goal D — Triage and CVDRA Prototypes Hitting Accuracy Targets | Prototypes on synthetic data: ≥90% triage, ≥95% CVDRA accuracy. Evidence required for Q1 MBIE claim. | Both | June 2026 | Not Started |

---

## Execution Roadmap

Sequential steps to achieve Objective 1.

### Step 1: Define the Problems Clearly

Lock in precise definitions for both tasks:

**Triage task:** What are the inputs (lab results, discharge summaries, etc.)? What are the outputs (urgency level, suggested action)? What counts as success (≥90% accuracy on what, exactly)?

**Care Gap Detection task:** What data do you need? What's the clinical logic? What are the edge cases? What counts as success (≥95% accuracy)?

Deliverable: Clear written definition of both tasks with success criteria.

**Step 1 status (5 April 2026):** Complete. Both task specs finalised and filed in `nexwave-rd/docs/obj-1/output/`. GP clinical review outreach initiated before proceeding to Step 2 — seeking 2-3 practising NZ GPs to validate urgency taxonomy, boundary cases, and care gap trigger logic. Contacts: Brendan Duck (Health HB PHO), Gareth Roberts (Comprehensive Care PHO), Heidi Bubendorfer (RNZCGP). Tracked in task `rd-20260405-001`. Step 2 begins once at least 2 reviewers have responded.

### Step 2: Literature Review and Architecture Research

Research what's already been done:
- Clinical NLP and LLM benchmarks in similar domains
- Sovereign AI options available in NZ
- AWS Bedrock capabilities within data residency constraints (ap-southeast-2)
- RAG vs fine-tune vs prompt-engineering vs hybrid trade-offs

Deliverable: Literature review document.

**Step 2 status (14 April 2026):** Complete. Seven research reports (r1–r7) plus sprint-2-summary filed in `nexwave-rd/docs/obj-1/research/`. Internal digest delivered as `sprint-2-literature-review.md` in `output/`. Key findings: fine-tuned 8B beats zero-shot 120B at 300–500-item scale (r1); CoT degrades 86% of clinical LLMs (r1); Bedrock ap-southeast-6 cross-Region routes ANZ-wide (r2); Catalyst C1A is the only GA NZ GPU substrate (r2); IPP 3A automated-decision disclosure in force 1 May 2026 (r2).

### Step 3: Shortlist Architecture Candidates (3–4 approaches)

Document for each:
- How it meets triage and care gap requirements
- Trade-offs (accuracy, speed, cost, sovereignty compliance)
- Why it's worth evaluating

Deliverable: Architecture shortlist with documented rationale.

**Step 3 status (14 April 2026):** Complete. Four candidates evaluated in `sprint-2-architecture-shortlist.md`: C1 Bedrock Claude Haiku/Sonnet, C2 Catalyst Llama 3.3 70B + MedGemma + ModernBERT, C3 rules engine + BioClinical ModernBERT 396M / Llama 3.1 8B LoRA hybrid, C4 agentic pipeline. **Decision: C3 primary, C1 parallel reference for Sprint 3 bake-off; C2 and C4 deferred.** Data requirements (`sprint-2-data-requirements.md`) and synthetic dataset schema v0.1 (`sprint-2-synthetic-dataset-schema.md`, provisional pending `rd-20260405-001`) also filed. Step 4 begins once GP clinical review confirms taxonomy.

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

MBIE contact: Lisa Pritchard (MBIE Innovation Services). All experiments must be logged.

**Q1 claim prep (2026-04-15):** Email sent to Lisa Pritchard asking about time tracking format, progress report structure, and cost spreadsheet template. Awaiting response.

**Ting employment contract:** Hourly rate corrected to $58.33/hr in Google Doc (2026-04-15). Ting re-signature pending (task `rd-20260415-001`). PAYE submission blocked until signed.

**SaMD compliance outreach (2026-04-15):** Quotes requested from four firms — Elevate Medtech (Anne Arndt), Buddle Findlay (Catherine Miller), Aesculytics (Dr Arindam Bose), Bell Gully (Dr Laura Hardcastle). Tracked in `rd-20260415-002`.

**Programme brief:** One-page technical brief filed at `nexwave-rd/docs/programme/nexwave-health-brief.md`. Attached to all compliance outreach emails.

---

## Tasks

```dataviewjs
const mb = app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api;
const lifecycle = this.component;
const statusOpts = [
  { name: 'option', value: ['open'] },
  { name: 'option', value: ['in-progress'] },
  { name: 'option', value: ['blocked'] },
  { name: 'option', value: ['done'] }
];
const priorityOpts = [
  { name: 'option', value: ['high'] },
  { name: 'option', value: ['medium'] },
  { name: 'option', value: ['low'] }
];
function statusSelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('status', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--status'] }, ...statusOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function prioritySelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('priority', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--priority'] }, ...priorityOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
const all = dv.pages('"tasks/open"')
  .where(p => p.project === "nexwave-rd" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const groups = {};
const unassigned = [];
for (let p of all) {
  const m = p.milestone ?? "";
  if (m) {
    if (!groups[m]) groups[m] = [];
    groups[m].push(p);
  } else {
    unassigned.push(p);
  }
}
const render = (tasks) => dv.table(
  ['Task', 'Status', 'Priority', 'Due'],
  tasks.map(p => [dv.fileLink(p.file.path, false, p.title || p.file.name), statusSelect(p.file.path), prioritySelect(p.file.path), p.due])
);
for (const [m, tasks] of Object.entries(groups)) {
  dv.paragraph(`**${m}**`);
  render(tasks);
}
if (unassigned.length > 0) {
  if (Object.keys(groups).length > 0) dv.paragraph("**Backlog**");
  render(unassigned);
}
```
