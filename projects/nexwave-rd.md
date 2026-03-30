---
id: nexwave-rd
status: active
type: rd
repo: nexwave-rd
stack: [aws-bedrock, claude-haiku, claude-sonnet, python, nextjs]
---

## Description
MBIE-funded R&D programme (N2RD grant CONT-109091-N2RD-NSIWKC). Developing NZ-sovereign clinical LLM for GP workflow. Objective 1: Foundation AI Architecture (months 1-6). Managed with Ting (R&D Programme Manager).

## Current goals
- Objective 1: inbox triage + CVDRA use cases
- PAYE evidence for Ting due 30 April 2026
- Q1 MBIE claim due 31 May 2026

## Key decisions
- Inbox triage: AWS Bedrock (Claude Haiku/Sonnet, AU Cross-Region Inference)
- CVDRA: deterministic Python, NZ PREDICT equation — not LLM
- Data residency: AWS Auckland (ap-southeast-6)

## Tasks

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS Task,
  objective,
  owner,
  status,
  priority,
  due
FROM "tasks/open"
WHERE project = "nexwave-rd"
SORT priority DESC, due ASC
```
