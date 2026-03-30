---
id: referral-images
status: active
type: product
repo: clinicpro-saas
stack: [nextjs, typescript, tailwind, vercel, neon, clerk, stripe]
---

## Description
Referral image tool for GPs. Transitioning from free to paid on 6 April 2026. Existing users grandfathered.

## Tasks

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS Task,
  status,
  priority,
  due
FROM "tasks/open"
WHERE project = "referral-images"
SORT priority DESC, due ASC
```
