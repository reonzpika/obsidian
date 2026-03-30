---
id: ai-scribe
status: active
type: product
repo: clinicpro-saas
stack: [nextjs, typescript, tailwind, vercel, neon, clerk]
---

## Description
AI-powered clinical scribe tool. Active development.

## Tasks

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS Task,
  status,
  priority,
  due
FROM "tasks/open"
WHERE project = "ai-scribe"
SORT priority DESC, due ASC
```
