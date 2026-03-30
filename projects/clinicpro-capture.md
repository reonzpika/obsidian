---
id: clinicpro-capture
status: active
type: product
repo: clinicpro-medtech
stack: [nextjs, typescript, tailwind, vercel, supabase, aws-lightsail-bff]
---

## Description
Mobile web app that photographs clinical images and commits them to patient records in Medtech Evolution via the ALEX API. All ALEX calls route through BFF at api.clinicpro.co.nz.

## Current goals
- Ship /about-capture landing page
- Await Medtech production sign-off
- Onboard first paying practices after sign-off

## Key decisions
- Routes: /medtech/capture (app), /about-capture (landing page)
- Auth: Supabase OTP (6-digit code, no magic link)
- Pricing: FTE-based tiers, 30-day free trial
- BFF mandatory: never call ALEX directly from Vercel

## Tasks

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS Task,
  status,
  priority,
  due
FROM "tasks/open"
WHERE project = "clinicpro-capture"
SORT priority DESC, due ASC
```
