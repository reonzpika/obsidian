---
title: ClinicPro Capture — problem statement (vendor landscape analysis)
source: Google Drive — ClinicPro_Capture_Problem_Statement (docx)
source-id: 1S-gkQyOsSvaEx7gB_yXKcIdEb5ZG580f
source-date: 2026-03
migrated: 2026-04-15
confidentiality: prepared for Medtech Global
---

# Problem statement — clinical photo capture in NZ general practice

> Summarises the clinical workflow problem, the limitations of existing tools, and how ClinicPro Capture solves it via the ALEX FHIR API.

## 1. The workflow problem

Getting a clinical photo from a GP's phone into a patient record in Medtech Evolution is harder than it should be.

The two main tools available to NZ practices — MedImage and QuickShot — have significant limitations. For practices without either, the fallback workarounds are worse.

Real-world workarounds GPs describe in NZ clinician Facebook threads:

- Emailing to a practice email account
- Saving to a named folder on a shared drive
- Using Celo (third-party messaging app) as an intermediary
- Simply omitting photos from referrals when the process is too slow

## 2. MedImage (AtomJump)

Most established clinical image capture tool for Medtech practices in NZ. Open source, affordable, genuine GP advocates. Core architecture designed for an on-premise world.

### How it works

Two components: a PWA on the GP's phone, and a Windows-based Node.js server that must run on a PC at the practice. Photos travel phone → Windows server via either AtomJump's cloud relay or direct local WiFi.

To get photos into Medtech Evolution specifically, practices purchase the **EHR Connector add-on (NZ$680, one-time fee)**. This connector runs SQL queries directly against the Medtech database via ODBC: `SELECT` for patient lookup, `INSERT` into the `ATTACHMENTSMGR` table. The queries are publicly documented in the MedImage GitHub repository.

### The cloud Medtech problem

The ODBC integration requires direct network connectivity between the Windows MedImage Server and the Medtech SQL Server database. That works on-premise.

Medtech is moving to cloud hosting. 75%+ of NZ general practices already use Medtech, and Medtech waived all cloud migration fees in early 2023. Cloud-hosted Medtech delivers Medtech Evolution as a remote/hosted desktop session — the SQL Server database runs in a remote data centre, not on the practice's local network. The ODBC connection MedImage's EHR Connector depends on cannot cross that gap.

### The referral workflow problem

MedImage's EHR Connector guide explicitly states that for versions before 0.7.0, photos are added to the "Attachments window of MedTech, but not the Inbox window". The **Inbox Scan** is the folder that feeds HealthLink and ERMS referral attachment pickers automatically. Photos in the Attachments window must be manually located and attached when building a referral.

The optional image resize add-on (NZ$60) is required to manage file sizes. Without it, full-resolution phone camera photos may exceed ERMS attachment size limits.

### Certification status

MedImage submitted its Medtech Evolution add-on for formal code review in March 2018. As of the MedImage website, this review has not been completed. Not a formally certified Medtech add-on, though open source and queries publicly available.

## 3. QuickShot (IntelliMed)

Module within the IntelliMed suite (Houston Productivity, NZ). IntelliMed is listed as an official ALEX Partner on Medtech's partner page. Cleaner UX than MedImage.

### How it works

Web app accessed via mobile browser. Four steps: enter NHI → confirm patient → take photo → submit. IntelliMed describes photos landing at "the correct patient and provider inboxes" — which, if accurate, would mean Inbox Scan rather than just Attachments.

### What is known and what is not

Very limited public technical documentation. Based only on publicly available info:

- Listed as ALEX Partner — suggests some ALEX API use.
- IntelliMed's other modules (EzyScan, patient kiosks) use automation techniques that may also apply to QuickShot.
- Pricing not public. Quote on request.
- Output file format not documented publicly. One GP in the Facebook discussion reported receiving photos only as PDFs, which specialist referral services then rejected and asked to be resent as JPEG.
- No independent GP reviews available publicly. IntelliMed's own testimonials focus on other modules.

## 4. The structural gap

Three constraints define the gap neither existing tool reliably fills.

### Cloud Medtech compatibility

NZ market is shifting to cloud-hosted Medtech. Medtech describes cloud as its strategic direction, waived migration fees to accelerate adoption. Any tool requiring local network access to the Medtech database or workstation becomes less relevant as this migration continues. The **ALEX FHIR API** — cloud-native, authenticated over the internet, accessible from any network — is the only integration path that works regardless of deployment model.

### Images must land in Inbox Scan, not just Attachments

HealthLink and ERMS pull attachments from Medtech Inbox Scan automatically. Photos in the Attachments window require manual selection at referral time. This extra step is what GPs describe as the most frustrating part of their current workflow — and it is the step that causes referrals to be sent without photos when time is short.

### Format and size

The ALEX DocumentReference (Scan) endpoint accepts **only TIFF or PDF — not JPEG**. Phone camera photos must be converted before commit. File size must be under 8 MB per document, and ERMS imposes its own attachment size limits. A tool that commits photos in the correct format, compressed to a clinically appropriate size, eliminates the compatibility failures GPs describe.

## 5. How ClinicPro Capture addresses this

Mobile web app that commits clinical photos directly to Medtech Evolution Inbox Scan via the ALEX FHIR DocumentReference endpoint. No local software, no Windows server, no local network access.

### Cloud compatibility

Because ClinicPro Capture communicates exclusively via the ALEX API over the internet, it works identically whether the practice's Medtech is on-premise, cloud-hosted by Medtech, or hosted by a third party. Static IP allowlisting that ALEX requires is handled by a Sydney-based proxy, not by anything at the practice.

### Direct to Inbox Scan

Photos committed via ALEX DocumentReference (Scan) appear directly in the patient's Inbox Scan folder. Automatically available in HealthLink and ERMS referral attachment pickers. No manual retrieval step.

### Format and compression

Client-side mozjpeg compression (max 1920px, quality 82), then server-side conversion to JPEG-in-TIFF. Typical output under 1 MB per image, well within the ALEX 8 MB limit and ERMS constraints.

## 6. Comparison summary

Based on publicly available information:

| | MedImage | QuickShot | Email to self | **ClinicPro Capture** |
|---|---|---|---|---|
| Works on cloud Medtech | No (ODBC local) | Unknown | N/A | **Yes** |
| Lands in Inbox Scan | No (Attachments, pre-0.7.0) | Unclear | No | **Yes** |
| Local software required | Yes (Windows server) | No | No | **No** |
| Format suitable for ERMS/HealthLink | Partial | Unclear (PDF reports) | No | **Yes (TIFF)** |
| Audit trail | Partial | Unknown | No | **Full** |
| Medtech-certified | Submitted 2018, not confirmed | ALEX Partner listed | — | ALEX integration, pilot stage |

QuickShot entries marked "unclear" or "unknown" reflect publicly unavailable information. ClinicPro Capture's cloud compatibility and Inbox Scan delivery confirmed via ALEX API testing on Medtech UAT.
