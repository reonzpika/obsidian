# ClinicPro Medtech — Area Context

Medical device capture product. ALEX FHIR API integration via Medtech Global partnership.

## Active products

- ClinicPro Capture (`clinicpro-capture.md`) — image capture for referrals
- ClinicPro Dashboard (`clinicpro-dashboard.md`) — billing completeness module
- AU bundle (`clinicpro-capture-au-bundle.md`) — Australia expansion via Medtech
- ALEX integration (`clinicpro-capture-integration.md`) — FHIR API wiring

## Architecture

- Frontend: Next.js on Vercel (`capture.clinicpro.co.nz`)
- BFF: Node.js on AWS Lightsail (proxies all ALEX calls, holds secrets)
- ALEX FHIR: OAuth via BFF SSH; use `/alex-endpoint-test`, `/bff-debug`, `/bff-deploy`, `/bff-rotate-secret`

## Context

- BFF reference: `context/medtech-context/lightsail-bff.md`
- Medtech glossary: `context/medtech-context/glossary.md`
- ALEX API docs: `[[alex-api-docs]]`

## Partner contacts

Medtech Global / Valentia: Dr Ahmad Javad (President Tech), Imran Rashid (product), info@valentiatech.com.
Use `/medtech-prep` before any call.

## Task prefix

`medtech-*`

## PHI rule

Never send real patient data to any AI API. Use synthetic test data only.
