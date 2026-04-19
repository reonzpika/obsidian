---
title: ClinicPro Capture - AU Bundle Proposal for Medtech Global
type: proposal
audience: external
counterparty: Medtech Global Australia
author: Dr Ryo Eguchi
date: 2026-04-19
status: draft
project: clinicpro-capture
---

# ClinicPro Capture: Australian Market Bundle Proposal

**From**: Dr Ryo Eguchi, Founder, ClinicPro (NexWave Solutions Ltd, NZ)
**To**: Lawrence Peterson, GM Integration & Infrastructure, Medtech Global
**Date**: 19 April 2026
**Reference**: Follow-up to email thread "AU market for Capture app"

---

## Proposal summary

ClinicPro Capture, bundled white-label into Medtech Evolution Australia as a practice value-add. Per-active-practice pricing with annual minimum commitments over a 3-year initial term. Target launch: aligned with Medtech Evolution AU G2M, May to June 2026.

## Scope

**Included**: mobile web image capture, server-side compression and JPEG-in-TIFF conversion, FHIR POST to Medtech ALEX `/DocumentReference` via ClinicPro BFF, user authentication, audit logging.

**Excluded**: any features beyond image capture and ALEX post. Additional modules (for example, inbox triage, care gap workflows) are out of scope for this agreement and require separate commercial terms.

## Pricing

**AUD 30 per active practice per month** (AUD 360 per practice per year).

*Active practice* = one with at least one registered user AND at least one successful capture commit in the billing month.

## Annual minimum commitment

Medtech commits to a minimum of **75 active practices per year, equivalent to AUD 27,000 annually**, for each of the 3 years of the initial term.

Where onboarded active practices exceed 75 in any year, the full per-active-practice fee applies to all practices above the minimum. Where onboarded practices fall short, the minimum payment still applies.

## Payment structure

- Annual minimum billed **quarterly in advance**, in equal instalments (25% per quarter).
- Per-active-practice fees above the minimum invoiced **quarterly in arrears** (true-up).
- Payment terms: 30 days from invoice date.
- All amounts in AUD, exclusive of GST where applicable.

## One-off setup fee

**AUD 4,000 on contract execution**, to cover AU onboarding and compliance setup. Offsets against Year 1 minimum.

## Term and renewal

- **Initial term**: 3 years, locked, from contract execution. Neither party may terminate for convenience during this period.
- **After the initial term**: the agreement continues on a rolling 12-month basis unless either party gives 90 days written notice to terminate.
- **Pricing review**: annual adjustment indexed to Australian CPI during and after the initial term.

## Support model

- **Tier 1 (practice-facing)**: Medtech Australia support team
- **Tier 2 (escalations)**: ClinicPro, response within 2 business days NZT
- **Incident management**: OAIC-compliant Notifiable Data Breach process, co-ordinated with Medtech

## Data residency and compliance

- All data processing in AWS ap-southeast-2 (Sydney) and Vercel syd1 (Sydney). No processing outside Australia.
- **Zero PHI at rest**: images are pass-through only (client to BFF to ALEX).
- Audit log uses HMAC-SHA256 hashed patient identifiers; no plaintext PHI is stored.
- Annual penetration test by a CREST Australia New Zealand-approved provider.
- AU Privacy Impact Assessment completed pre-launch.

## Branding

Medtech Australia may white-label the product within Evolution AU. ClinicPro requires a "Powered by ClinicPro" attribution visible in the in-app about or help panel. No other brand presence required.

## Tax treatment

Australian tax law requires a 5% withholding on cross-border software licence payments under the NZ-AU Double Tax Agreement. The contract will include a gross-up provision so that Medtech pays enough to cover the withholding, and ClinicPro receives the fees set out above in full.

## Delivery

AU regionalisation engineering work commences on contract execution. Launch window May to June 2026.



---

*This proposal is subject to contract. All figures exclusive of GST where applicable.*
