# Privacy Policy

**ClinicPro Capture** | capture.clinicpro.co.nz
Operated by NexWave Solutions Limited, Auckland, New Zealand
Last updated: April 2026

---

## Who we are

ClinicPro Capture is a mobile web application that lets New Zealand GPs photograph clinical images and commit them directly to a patient record in Medtech Evolution, using the ALEX FHIR API. It is operated by NexWave Solutions Limited (Auckland, NZ). Questions? Email us at ryo@clinicpro.co.nz.

---

## What data we collect

We collect the minimum data required to operate the service.

**Authentication data**
When you sign in via one-time passcode (OTP), Supabase creates a user record associated with your email address. We also store two identifiers linked to your account: your facility ID and your practitioner ID. These allow the app to route image commits to the correct Medtech Evolution instance.

**Audit log**
Every successful image commit is recorded in our audit log (`medtech_image_commit_audit`). This log captures who committed the image, when, and to which facility and patient record. It does not store the image itself.

**No clinical images are retained**
This is the most important thing to understand about how ClinicPro Capture works. When you photograph a clinical image and confirm the commit, the image is transmitted directly to Medtech Evolution via the ALEX FHIR API. Once the commit succeeds, the image is gone from ClinicPro systems. We do not store, cache, or process clinical images beyond the time needed to complete the upload.

---

## How we use your data

| Data | Purpose |
|---|---|
| Email address | Sign-in authentication (OTP delivery) |
| Facility ID, practitioner ID | Route image commits to the correct Medtech instance |
| Audit log entries | Accountability record; confirms each commit was made by an authorised user |

We do not use your data for marketing, analytics, or any purpose other than operating the service.

---

## Who we share data with

**Medtech Global / ALEX FHIR API**
Clinical image data is transmitted to Medtech Evolution on your behalf. This is the core function of the app. All ALEX API calls route through our backend proxy at `api.clinicpro.co.nz`, hosted on AWS Lightsail. No data is stored at the proxy layer; it forwards requests and responses only.

**Supabase**
Authentication and user metadata (facility ID, practitioner ID) are stored with Supabase, our authentication provider. Supabase is SOC 2 Type II certified. Their privacy policy is available at supabase.com/privacy.

**No other third parties**
We do not sell, rent, or share your data with advertisers, analytics providers, or any other third parties.

---

## Retention periods

| Data | Retention |
|---|---|
| Supabase user account | Held while your account is active. Deleted on request. |
| Facility ID, practitioner ID | Held while your account is active. Deleted with your account. |
| Audit log entries | Retained for a minimum of 10 years, in line with health record obligations under the Health (Retention of Health Information) Regulations 1996. |
| Clinical images | Not retained. Committed to Medtech Evolution and immediately removed from our systems. |

---

## Your rights

Under the New Zealand Privacy Act 2020 and the Health Information Privacy Code 2020, you have the right to:

- Request access to personal information we hold about you.
- Request correction of any inaccurate information.
- Ask us to delete your account and associated data (subject to legal retention obligations for the audit log).
- Raise a complaint if you believe we have handled your information incorrectly.

To exercise any of these rights, contact us at ryo@clinicpro.co.nz. We will respond within 20 working days, as required by the Privacy Act 2020.

If you are not satisfied with our response, you can contact the Office of the Privacy Commissioner at privacy.org.nz.

---

## Security

- All data in transit is encrypted via TLS.
- Authentication uses short-lived OTP codes; no passwords are stored.
- The backend proxy does not persist any data.
- Access to audit logs and user records is restricted to authorised NexWave personnel.

---

## Note for Australian users

ClinicPro Capture may be accessed by Australian users via white-label deployments. Where Australian health information is involved, we handle it in accordance with the Australian Privacy Act 1988 and the Australian Privacy Principles (APPs). This includes obligations around collection, use, disclosure, and cross-border data transfer. Australian users have the same rights to access and correct their information as described above. Contact ryo@clinicpro.co.nz with any Australian privacy queries.

---

## Changes to this policy

We will post any changes to this page with an updated date at the top. For material changes, we will notify active users by email.

---

## Contact

NexWave Solutions Limited
Auckland, New Zealand
ryo@clinicpro.co.nz
capture.clinicpro.co.nz
