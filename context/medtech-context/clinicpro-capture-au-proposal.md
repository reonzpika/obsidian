---
title: ClinicPro Capture - AU Bundle Proposal for Medtech Global
type: proposal
audience: external
counterparty: Medtech Global Australia
author: Dr Ryo Eguchi
date: 2026-04-18
status: draft
project: clinicpro-capture
---

# ClinicPro Capture: Australian Market Bundle Proposal

**From**: Dr Ryo Eguchi, Founder, ClinicPro (ClinicPro Ltd, NZ)
**To**: Lawrence Peterson, GM Integration & Infrastructure, Medtech Global
**Date**: 18 April 2026
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

## Annual minimum commitments

| Year | Period | Min. active practices | Min. annual payment (AUD) |
|---|---|---|---|
| 1 | May 2026 - Apr 2027 | 150 | 54,000 |
| 2 | May 2027 - Apr 2028 | 250 | 90,000 |
| 3 | May 2028 - Apr 2029 | 400 | 144,000 |

Where onboarded active practices exceed the minimum in any given year, the full per-active-practice fee applies. Where onboarded practices fall short, the minimum payment applies, invoiced annually in advance with reconciliation at year-end.

## One-off setup fee

**AUD 15,000 on contract execution**. Offsets against Year 1 minimum. Covers:

- AU regionalisation engineering (IHI integration, AU facility ID formats, AU-specific ALEX endpoint testing)
- AU Privacy Impact Assessment (extension of existing NZ PIA to APP framework)
- AU-facing privacy policy and data processing agreement
- AU incident response plan

## Term and renewal

- **Initial term**: 3 years from contract execution
- **Renewal**: 12 months rolling, by mutual written agreement
- **Pricing review**: annual adjustment indexed to Australian CPI

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

Payments subject to the NZ-AU Double Tax Agreement royalty provisions. Contract to include a standard gross-up clause so that the fees set out above are received by ClinicPro net of any AU withholding tax deductions.

## Delivery

- AU regionalisation engineering: 6 to 8 weeks from contract execution
- Launch target: aligned with Medtech Evolution AU G2M, May to June 2026

## Open items requiring Medtech confirmation

Before final term sheet:

1. **Vendor security requirements**. Confirm whether Medtech AU requires formal certification (ISO 27001, SOC 2) or accepts SIG Lite / CAIQ self-attestation plus annual CREST ANZ pentest.
2. **My Health Record scope**. Confirm MHR integration remains Medtech-side; Capture does not write to MHR.
3. **Medtech AU entity details**. Confirm ABN and GST registration status (for correct GST and invoicing treatment).
4. **Governing law and dispute forum**. Medtech preference (Victoria, NSW, or other).

## Next steps

1. Medtech confirms the four open items above by end of April.
2. Term sheet signed by mid-May.
3. Full contract drafting and execution by end of May.
4. Engineering work commences on contract execution. Launch window May to June 2026.

---

*This proposal is subject to contract. All figures exclusive of GST where applicable.*
