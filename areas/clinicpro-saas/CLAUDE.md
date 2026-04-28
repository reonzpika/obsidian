# ClinicPro SaaS — Area Context

GP practice management platform. Next.js + Supabase + Vercel. Subscription model.

## Active products

- AI Scribe (`ai-scribe.md`) — clinical note generation
- Referral Images (`referral-images.md`) — referral image capture
- 12-Month Prescription (`12-month-prescription.md`) — repeat prescribing tool
- Dashboard (`clinicpro-dashboard.md`) — billing completeness and practice analytics

## Design system

`context/clinicpro-context/design-system/design-clinicpro-saas.md` is canonical. Read before any UI work.
Repo CLAUDE.md has the explicit path pointer. Do not invent tokens or class names.

## Tech notes

- Repo: `C:/Users/reonz/cursor/clinicpro-saas/`
- Auth: Clerk. Payments: Stripe (use `/stripe-webhook-debug` if webhooks fail).
- Deploy: Vercel (use `/deploy-to-vercel` for prod deploys).

## Task prefix

`saas-*`

## Key contacts

- Helen Yu: accounting (Xero, payroll, PAYE/GST). Financial queries only.
