# ALEX API Documentation

Reference for the Medtech ALEX FHIR API — used by all ClinicPro Medtech tools.

**Current product using this API**: [[clinicpro-capture]]

---

## Source

- **Live docs site**: https://alexapidoc.medtechglobal.com/
- **Scraped output**: `C:\Users\reonz\Cursor\scraper\output\alex-api-docs\`
- **Raw collection JSON**: `C:\Users\reonz\Cursor\scraper\output\alex_collection_raw.json`
- **Scraper code**: `C:\Users\reonz\Cursor\scraper\` — see [[repos]] for full scraper entry
- **Last scraped**: 2026-03-31
- **Current ALEX version**: v2.10 (released 25 Feb 2026)

---

## How to re-scrape

```bash
cd C:\Users\reonz\Cursor\scraper

# Use cached collection (fast — re-parses existing JSON):
python run_scraper.py

# Re-fetch from live site (slow — use when Medtech releases a new version):
python run_scraper.py --refresh

# Skip static pages:
python run_scraper.py --no-static
```

---

## Coverage

**261 endpoints** across 24 resource folders + **7 static doc pages**.

### Endpoint folders

| Folder | FHIR Resource | Notes |
|--------|--------------|-------|
| Authentication | — | Token endpoint (UAT) |
| Patient (Patient, PractitionerRole) | Patient | Search + write-back (POST/PUT) |
| Patient V2 (Patient, PractitionerRole) | Patient | V2 search endpoints |
| Provider (Practitioner) | Practitioner | HPI CPN, Med Council ID |
| Provider V2 (Practitioner) | Practitioner | V2 + Nursing Council ID, HPI filters |
| Practice (Location) | Location | Facility details, online form config |
| Medication (MedicationRequest) | MedicationRequest | Rx retrieval + write-back |
| Immunisation (Immunization) | Immunization | Retrieval only |
| Medical Warning (Allergy Intolerance) | AllergyIntolerance | Retrieval only |
| Screening (Observation) | Observation | Retrieval + write-back |
| Classification (Condition) | Condition | Retrieval + write-back |
| Appointments (Slot, Appointment) | Slot, Appointment | **New in v1.4 AU** — slot retrieval, book, arrive, cancel |
| Lab Results (Diagnostic Report) | DiagnosticReport | Retrieval + unfiled inbox results (new in v2.10) |
| Consultation (Document Reference) | DocumentReference | Retrieval + note write-back |
| Patient Summary | — | NHI-based summary |
| Scan Folder (Document Reference) | DocumentReference | RSD-style scan retrieval |
| RSD (Document Reference, Binary) | DocumentReference, Binary | File retrieval + blobkey attachment |
| Inbox Write Back (Communication/Media) | Communication, Media | Post media, messages, prescriptions, document reference |
| Inbox Retrieval (Communication/Media) | Communication, Media | Retrieve messages, attachments |
| Outbox (Communication) | Communication | Web form records |
| Invoice | Invoice | Retrieval + write-back (single/multiple services) |
| ChargeItem | ChargeItem | Service details by practice/location |
| Task | Task | Staff and patient task retrieval + write-back |
| Accident Details (ExplanationOfBenefit) | ExplanationOfBenefit | ACC accident details |
| Account Balance (Account) | Account | Patient account balance |

### Static doc pages

Located at `scraper/output/alex-api-docs/static/`:

| File | Content |
|------|---------|
| `introduction.md` | Overview of the ALEX FHIR API |
| `changelog.md` | Version history (v2.1 → v2.10) |
| `high-level-design.md` | Architecture and design principles |
| `integration-connectivity-uat.md` | UAT environment setup |
| `requirements-integration-connectivity.md` | Server connectivity requirements |
| `vendor-partner-authentication-process.md` | OAuth/Azure AD auth flow |
| `subsequent-requests-post-authorisation.md` | Request headers, UAT/PROD endpoints |

---

## Key facts for building

- **Auth**: Azure AD OAuth2 (client credentials). Token acquired by BFF, cached 55 min.
- **BFF mandatory**: All ALEX calls must go through `api.clinicpro.co.nz` — Vercel's IP is not allow-listed.
- **UAT facility IDs**: F99669-C (local), F2N060-E (hosted)
- **V2 endpoints**: Prefer V2 for Patient and Provider where available — better structured responses.
- **Appointments**: In ALEX AU UAT as of v1.4 (25 Mar 2026). Expected in PROD ~April 8 2026. New roles required — request via alexsupport@medtechglobal.com.
- **Lab Results (v2.10)**: New provider-based retrieval (NZMC, NZNC, HPI CPN) + unfiled inbox results with date range.
