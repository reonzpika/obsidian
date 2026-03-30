---
id: 12-month-prescription
status: active
type: product
repo: clinicpro-saas
stack: [nextjs, typescript, tailwind, vercel, neon, clerk]
---

## Description
12-month prescription tool for GPs. Currently in beta.

## Tasks

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS Task,
  status,
  priority,
  due
FROM "tasks/open"
WHERE project = "12-month-prescription"
SORT priority DESC, due ASC
```
