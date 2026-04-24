# Session Queue: 2026-04-24

Generated to burn remaining ~30% weekly Claude usage before reset. 6 projects scoped: referral-images, clinicpro-capture, clinicpro-dashboard, nexwave-rd-obj-1, founder-os, miozuki.

---

## Long-Running Sessions (ranked)

### Tier 1

**Session 1 — ClinicPro Dashboard billing module (recommended first)**
- Tasks: medtech-20260405-003 + medtech-20260408-001
- Scope: NLP prompt design, ExplanationOfBenefit/Task/Communication endpoint tests, appointment-driven billing flow, Invoice write-back stub
- Constraint: ALEX Invoice API has no patient search — only `_id` lookup. All ALEX calls go via BFF at api.clinicpro.co.nz.
- Duration: 2-3h

**Session 2 — NexWave R&D synthetic NZ GP inbox dataset (best token-burn)**
- Task: rd-20260329-023 (overdue Apr 25, high)
- Scope: 400 items, 5x4 stratification grid, 14 QA gates, parallel agent fan-out
- Caveat: schema v0.1 is provisional pending GP reviewer sign-off (rd-20260405-001). Confirm sign-off before starting.
- Duration: 3-4h

**Session 3 — Miozuki greenfield "#1 NZ fine jewellery" strategy**
- Scope: directory subdomain, AI chatbot, SEO strategy, UGC. Open with /board first, then Plan check, then deep dive.
- Note: separate from current 2.0 UI work (all blocked on Ting + Nano Banana Pro API key)
- Duration: 2-3h

### Tier 2

**Session 4 — NexWave R&D Sprint 3 bake-off protocol**
- Scope: C1 (Bedrock Claude Haiku 4.5/Sonnet 4.6) vs C3 (rules engine + BioClinical ModernBERT 396M + Llama 3.1 8B LoRA hybrid) harness design
- Duration: 1.5-2h

**Session 5 — ClinicPro Capture auth + tenancy architecture**
- Scope: Supabase OTP auth flow, admin dashboard data model, AU tenancy isolation
- Duration: 1.5-2h

**Session 6 — Founder OS Claude Code setup audit**
- Task: fo-20260423-001 (due Apr 27)
- Scope: "The Claude Code Setup Nobody Shows You" study + apply
- Duration: 2h

### Tier 3

**Session 7 — ClinicPro Capture landing page copy + design review**
- Task: medtech-20260419-001 (overdue, unblocks champion email)
- Duration: 1-1.5h

**Session 8 — Referral Images Contact + Work With Me pages**
- Task: saas-20260409-004 (in-progress)
- Duration: 1-1.5h

**Session 9 — Reviews back-fill + session-update queue clearance**
- Scope: weekly + monthly reviews for Founder OS and Miozuki; clear 2 pending /session-update sessions (cf9f2d0f, 90a49c88)
- Duration: 45-60 min

---

## Agent-Delegable (parallel fire, not new sessions)

| Task | Type | Note |
|------|------|------|
| medtech-20260416-003 | Champion email v1 | gmail-draft skill |
| medtech-20260416-004 | Demo Loom script + case-study template | generation task |
| medtech-20260329-005 | SEO metadata for capture pages | generation task |
| medtech-20260329-001 | /capture-privacy page content | generation task |
| medtech-20260418-007 | AU PIA (OAIC template) | generation task |
| medtech-20260418-008 | AU privacy policy + IRP adaptation | generation task |
| saas-20260407-001 | React setState warning fix | code task |
| saas-20260329-008 | Signup flow paid model update | code task |
| saas-20260408-003 | Visual QA landing page | browser agent |
| saas-20260409-002 | Tailwind config migration | code task |
| rd-20260423-002 | Buddle Findlay engagement email | gmail-draft, due Apr 27 |
| rd-20260329-013 | GST invoice template for MBIE | generation task |
| rd-20260329-021 | Document Medtech sandbox environment | generation task |
| rd-20260419-001 / 002 / rd-20260420-004 | Helen admin emails (R&D bank, credit card, employment contract) | gmail-draft batch |

---

## Blocked / Skip

- rd-20260421-003: GP sign-off pending on schema
- medtech-20260423-002: depends on lawyer quote replies
- medtech-20260418-003 / 004: external parties (insurance, WHT consult)
