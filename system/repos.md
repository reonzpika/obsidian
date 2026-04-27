# Repo & Folder Map

Full picture of everything in `C:\Users\reonz\cursor\`. Last verified: 2026-03-29.

---

## Active product repos

### clinicpro-saas
Main ClinicPro web app at www.clinicpro.co.nz. Next.js (App Router), TypeScript, Tailwind, Clerk auth, Neon/Drizzle DB, Vercel.

| Feature | Route | What it does |
|---------|-------|-------------|
| AI Scribe | `/ai-scribe/consultation` | Records consultations via mic (desktop or mobile via Ably), transcribes with Deepgram, generates SOAP notes via Claude. Right-sidebar has clinical tools, plan/safety-netting, examination checklist, agent chat drawer. |
| Referral Images | `/referral-images/capture` | Camera-based image capture. Compresses to JPEG, uploads to S3, shareable links. Mobile PWA. |
| 12-Month Prescriptions | `/12-month-prescriptions` | NZ repeat prescription management tool. |
| ACC Tools | `/acc` | ACC45 form helpers: employer lookup + occupation code search. |
| OpenMailer | `/openmailer` | Internal email marketing system — campaigns, subscribers, click tracking, PHO campaign tooling. |
| Templates | `/ai-scribe/templates` | Customisable note templates with a DSL; managed via DB migrations. |
| Mobile | `/ai-scribe/mobile` | Mobile companion for the scribe; pairs with desktop session via Ably. |

Other notable folders:
- `lightsail-bff/` — NOT here; lives in clinicpro-medtech.
- `healthify/` — Stub. Shared types only (`ScrapedPage`, etc.); old RAG scrapers not migrated.
- `database/schema/` — 30+ Drizzle schema files covering: users, patient sessions, templates, images, openmailer tables, prompt versioning, RAG, usage/cost tracking.
- `scripts/` — One-off migration and campaign scripts (TypeScript, run with tsx).

---

### clinicpro-medtech
Separate Next.js app for **ClinicPro Capture** — mobile PWA that photographs clinical images and writes them into Medtech Evolution patient records via the ALEX FHIR API.

| Layer | Location | What it does |
|-------|----------|-------------|
| PWA app | `/medtech/capture/*` | Login (Supabase OTP), patient search by NHI, camera capture, confirm, progress, review. Supabase auth. |
| Landing page | `/about-capture` | Marketing landing page for ClinicPro Capture (the product). |
| BFF | `lightsail-bff/` | Express.js on AWS Lightsail. Holds the static allow-listed IP (13.236.58.12). Acquires Azure AD OAuth token (55-min cache), proxies FHIR `DocumentReference` POST to ALEX API. Never bypassed. |
| ALEX reference | `lightsail-bff/ALEX_API_Reference.md` | Live-tested ALEX endpoint docs. `Media` POST = Inbox Media; `DocumentReference` POST = Inbox Scan (legacy-compatible). |
| API routes | `app/api/(integration)/medtech/*` | capabilities, document-reference, launch-session, locations, test, token-info |

Auth: Supabase OTP (6-digit code). No magic link. facilityId + practitionerId stored in user metadata; used to route to search vs setup on load.

---

## Side projects

### eguchi-family
Private Japanese-language family workspace for Ryo, Yoko, Haruhi, Natsumi, Motoharu. Next.js + Supabase + Clerk (invite-only, no public signup). Members paste AI output; app polishes via OpenAI GPT-4o and saves as private ideas or public living documents.

Routes: feed, ideas, missions, projects (living docs), showcase, learning hub, discussions, onboarding, tools, notifications.

---

### cloud9japan
Static Next.js marketing site for **Cloud Nine** — Yoko's brand of handmade bags from Kurume Kasuri fabric targeting Japanese equestrian buyers. Pre-commerce. Built for Horse Messe 2026 (Feb 21-23, Booth F6). No backend.

---

### gp-community
Single-file HTML/CSS/JS prototype of a **ClinicPro Community** forum. Simulates a mobile app shell (390×844px iPhone frame) in the browser. No backend, no framework. Served locally via `serve`.

---

### ahuru
SEO automation for **ahurucandles.co.nz** (a candle shop, not ClinicPro). Python pipeline:
1. Pull Google Search Console data (weekly 7d + 90d, monthly 28d + YoY)
2. Claude analyses → Markdown report saved to `reports/`
3. Email highlights via Resend
4. Generate SEO meta update tasks → `seo_tasks.json`
5. Approved tasks → pushed to Shopify Admin API

Runs via GitHub Actions (Monday 08:00 NZST). GitHub Pages dashboard for reviewing/approving tasks.

---

## Automation / tooling

### LinkedIn
Autonomous LinkedIn content engine for Dr Ryo. Python WAT-framework repo.

| Layer | Directory | Contents |
|-------|-----------|---------|
| Knowledge | `knowledge/` | Voice profile, NZ health context, algorithm SOP, hashtag library, mention library, playbook, performance history |
| Agents | `agents/` | researcher, scout, architect, strategist, analyst, image_architect |
| Tools | `tools/` | browser (Playwright), executor (Golden Hour posting), scheduler, search |
| Scripts | `scripts/` | plan_from_url, research, scout, pick_targets, draft, assemble_session_state, collect_analytics, analyse_performance |
| Outputs | `outputs/` | Per-session folders (not committed) |

Flow: `linkedin-post-create` skill → plan → research → scout → draft → approve → execute → 48hr review → analyst scores → proposes knowledge/system updates → bulk approve/reject.

---

### scraper
Two scrapers:
1. `alex_scraper/` — Scraper for the ALEX API docs site. Intercepts the Postman collection JSON via Playwright, parses all endpoints (including nested folders), and writes one Markdown file per endpoint. Also extracts static doc pages from the collection description. Output: `scraper/output/alex-api-docs/` (261 endpoints, 7 static pages). Run: `python run_scraper.py` (cached) or `--refresh` (re-fetch live). Full reference: [[alex-api-docs]].
2. `gp_clinic_scraper.py` — Crawl4AI scraper for Healthpoint GP clinic listings → CSV.

---

## R&D / planning

### nexwave-rd
Near-empty code workspace for the **NexWave** MBIE R&D programme (grant CONT-109091-N2RD-NSIWKC). Objective 1: inbox triage (AWS Bedrock, Claude Haiku/Sonnet) + CVDRA (deterministic NZ PREDICT equation). Tasks live in `obsidian/tasks/open/` with prefix `rd-`. Must stay isolated from commercial ClinicPro work.

---

### obsidian (this vault)
Central task/project management across all repos. AI agents write here; Obsidian reads via Dataview.

| Folder | Purpose |
|--------|---------|
| `projects/` | One file per product (ai-scribe, clinicpro-capture, referral-images, 12-month-prescription, nexwave-rd) |
| `sprints/active/` | Active sprint files (Dataview-powered task tables) |
| `tasks/open/` | All open task files; prefixed by repo |
| `dashboards/` | Per-repo dashboards (clinicpro-saas, clinicpro-medtech, nexwave-rd, home) |
| `context/` | Reference files: people, stack, nz-health, repos (this file) |
| `inbox/` | Brain dump / capture |

---

## Config & support folders

| Folder | Purpose |
|--------|---------|
| `memory/` | Claude Code persistent memory for this workspace (context/, people/, projects/, glossary.md) |
| `skills-update/` | Compiled Claude Code `.skill` files: `done.skill` (session-end sync), `skill-creator.skill` |
| `Archives/ClinicProNZ (archived)/` | Old monorepo before saas/medtech split. Larger codebase, includes old lightsail-bff. Reference only. |
| `Product Strategist / Solo Founder Adviser/` | Empty placeholder. |
| `.cursor/skills-cursor/` | Cursor skill files: create-rule, create-skill, create-subagent, migrate-to-skills, update-cursor-settings |
| `.crawl4ai/` | Cache from Crawl4AI scraper runs |
| `.claude/` | Claude Code workspace settings |
| `.aws/` | AWS credentials/config |
