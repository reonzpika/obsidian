---
title: ClinicPro Capture — product overview
source: Google Drive — ClinicPro_Capture_Overview_Medtech (doc)
source-id: 1ZVD8bShRQi7B5MIN9FEhUA06OZ7H6ETro6hPMhP5qvM
source-date: 2026-03
migrated: 2026-04-15
confidentiality: prepared for Medtech Global
---

# ClinicPro Capture — product overview

> Clinical image capture for Medtech Evolution.
> Prepared for Medtech Global by NexWave Solutions Limited (trading as ClinicPro).

## 1. The problem

GPs routinely need to capture clinical photos during or after a consultation and attach them to a patient record in Medtech Evolution. Common scenarios: skin lesions, wound assessments, post-operative sites, pre-referral documentation.

Existing tools have a critical limitation:

| Tool | Limitation |
|---|---|
| MedImage / AtomJump | Requires local network access to the Medtech workstation. Fails on cloud-hosted Medtech. |
| QuickShot / Intellimed | Same constraint. Local network only. Not viable for hosted Medtech. |
| Email to self | No audit trail. Manual copy-paste into Medtech. HIPC risk if using personal email. |
| Shared Google Drive | No Medtech integration. Manual filing. No patient linkage. Privacy risk. |

**The gap:** no tool that works with cloud-hosted Medtech, requires no local software, and commits images directly to the correct patient record via the ALEX API.

## 2. What ClinicPro Capture does

ClinicPro Capture is a mobile web app. A GP opens it on their phone, looks up a patient by NHI, takes one or more clinical photos, adds a description, and commits them directly to that patient's Inbox Scan folder in Medtech Evolution via the ALEX API.

Images appear immediately in Medtech Evolution's Inbox Scan, and are therefore available in HealthLink and ERMS referral attachment pickers.

**Key capabilities:**

- Works anywhere with internet access, including cloud-hosted Medtech
- No desktop software, no local network configuration, no installation
- NHI-based patient lookup via ALEX FHIR API
- Patient identity confirmation screen before any capture is permitted
- Multi-image capture from camera or gallery, with parallel compression
- Per-image metadata: side (Right/Left/N/A), description, image type
- Images committed to Medtech Inbox Scan as TIFF via ALEX DocumentReference
- Per-image progress tracking with retry on failure

## 3. How it works

Six-step linear flow designed for use between consultations.

1. **Sign in** — GP authenticates via Clerk. Facility ID and Practitioner ID configured once per user.
2. **NHI search** — ALEX FHIR Patient endpoint lookup. Returns name and date of birth.
3. **Confirm patient** — name, DOB, NHI displayed for explicit confirmation before capture.
4. **Capture** — phone camera or gallery. Client-side compression via mozjpeg WASM (max 1920px, quality 82).
5. **Review** — per-image metadata: anatomical side, required description, optional image type. Subject line previewed.
6. **Commit** — server-side JPEG-in-TIFF conversion (sharp, quality 80). Sequential commit to ALEX DocumentReference (Scan). Per-image progress with retry.

### Technical architecture

| Layer | Tech |
|---|---|
| Frontend | Next.js 16, App Router, TypeScript strict, Tailwind, Vercel Sydney |
| Authentication | Clerk — per-user facility and practitioner config |
| API | Medtech ALEX FHIR R4 — Patient read, DocumentReference write |
| Static IP proxy | AWS Lightsail Sydney — required for ALEX IP allowlisting |
| Image format | JPEG-in-TIFF via sharp — only format accepted by ALEX DocumentReference (Scan) |
| Session storage | Browser sessionStorage only. No server-side persistence of patient data. |

> **Note:** this doc was prepared for Medtech Global and references Clerk. The production clinicpro-medtech repo has migrated from Clerk to Supabase Auth. Keep that distinction in mind when writing public-facing copy.

## 4. Security and privacy

Designed with HIPC compliance as a first-class constraint.

### Data minimisation and transit
- Patient identifiers never in URLs. Server-side session tokens only.
- Image data held in browser sessionStorage during capture workflow, cleared immediately after commit.
- No patient data written to any server-side database.
- Images live only in Medtech Evolution after commit. ClinicPro holds no copy.

### Infrastructure
- App hosted on Vercel Sydney (syd1).
- ALEX proxy on AWS Lightsail Sydney. All data transits within NZ/AU.
- AWS NZ Notifiable Data Breach Addendum in place.
- TLS on all transmission.

### EXIF and metadata
Stripped at two points: client-side during mozjpeg compression, and server-side by sharp before TIFF conversion.

### Audit logging
- Every commit logged server-side: user ID, facility ID, practitioner ID, timestamp, document ID returned from ALEX.
- NHI and patient ID stored as HMAC-SHA256 hashes only. Not reversible, queryable for accountability.
- Answers "who committed to which patient, when" without holding PHI.

### Legal framework
- Data Processing Agreement available per practice.
- ClinicPro acts as agent of the practice under s11 Privacy Act 2020.
- Breach notification chain: AWS → ClinicPro within 24h; ClinicPro → practice within 24h; practice → Privacy Commissioner within 72h if serious harm threshold met.

### On the roadmap: session binding
Short-lived code displayed in Medtech Evolution that the mobile user enters before NHI search is permitted. Proves physical co-location with the Medtech workstation.

## 5. ALEX API integration

Two ALEX endpoints in use:

| Endpoint | Use |
|---|---|
| `GET /FHIR/Patient` | NHI → Patient resource lookup. Returns name and DOB for confirmation. |
| `POST /FHIR/DocumentReference` | Writes TIFF image to patient's Inbox Scan folder. Requires DocumentReference (Scan) write scope. Immediately visible in Medtech Evolution and in HealthLink/ERMS referral attachment pickers. |

### Constraints and design decisions

- ALEX DocumentReference (Scan) accepts TIFF or PDF only. ClinicPro converts JPEG → JPEG-in-TIFF server-side via sharp.
- Each DocumentReference attachment must be under 8 MB. Target under 1 MB per image at quality 80, automatic retry at quality 70 if first pass exceeds 1 MB.
- ALEX requires a static source IP for allowlisting. All ALEX calls route through AWS Lightsail Sydney (fixed IP).
- `facilityId` passed as `mt-facilityid` header on every ALEX request. `practitionerId` used as author reference on DocumentReference — routes documents to the GP's own Inbox Scan.

## 6. Current status (as of March 2026)

| | |
|---|---|
| Status | MVP. Validated against Medtech UAT environment. |
| ALEX scopes | Patient read + DocumentReference (Scan) write — tested on UAT. |
| Production scopes | Pending enablement by Medtech for production environment. |
| Next step | Pilot deployment with first GP practice following production scope enablement. |
| Competing tools | MedImage (AtomJump), QuickShot (Intellimed) — both local-network only. |

## 7. About ClinicPro

ClinicPro is a product of NexWave Solutions Limited, a NZ company building workflow software for general practice. ClinicPro Capture is one of several products integrating with Medtech Evolution via ALEX.

Contact: ryo@clinicpro.co.nz
