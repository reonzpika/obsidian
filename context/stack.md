# Tech Stack Reference

## clinicpro-saas
- Framework: Next.js (App Router), TypeScript, Tailwind
- Database: Neon (Postgres), Drizzle ORM
- Auth: Clerk
- Payments: Stripe
- Deploy: Vercel (clinicpro.co.nz)

## clinicpro-medtech
- Framework: Next.js (App Router), TypeScript, Tailwind
- Database: Supabase Postgres (Sydney, ap-southeast-2)
- Auth: Supabase Auth (OTP — signInWithOtp + verifyOtp, no magic link)
- Deploy: Vercel (/medtech/* path)
- BFF: AWS Lightsail (api.clinicpro.co.nz, static IP)
- Critical: ALL Medtech ALEX API calls must route through BFF. Never call ALEX directly from Vercel.

## nexwave-rd
- AI: AWS Bedrock (Claude Haiku/Sonnet, AU Cross-Region Inference, ap-southeast-6)
- CVDRA: Deterministic Python (NZ PREDICT equation — not LLM)
- Data residency: AWS Auckland (ap-southeast-6)

## GitHub
- Account: reonzpika
- Workflow: main branch only. No PRs/issues workflow.
