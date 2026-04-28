# Lightsail BFF Reference

Express.js proxy service running on AWS Lightsail (Sydney). All ALEX FHIR API calls from Vercel route through here. Never call ALEX directly from Vercel.

**Version**: 0.2.0
**Repo path**: `clinicpro-medtech/lightsail-bff/`
**Active file**: `index.js` (1704 lines). `medtech-bff.js` is dead code, ignore it.

---

## Infrastructure

| Property | Value |
|---|---|
| Static IP | 13.236.58.12 (ap-southeast-2 Sydney) |
| Domain | `api.clinicpro.co.nz` |
| TLS | Let's Encrypt via Certbot (auto-renew) |
| Proxy | nginx (443 HTTPS → http://127.0.0.1:3000) |
| Process | systemd service `clinicpro-bff` |
| User | `deployer` (not root) |
| Working dir | `/home/deployer/app` |
| Env file | `/home/deployer/app/.env` (not in git) |

---

## Environment variables

All must be set in `/home/deployer/app/.env` on Lightsail. `BFF_INTERNAL_SECRET` must also be set in Vercel (Vercel sends it as a header, BFF validates it).

| Variable | Required | Purpose |
|---|---|---|
| `BFF_INTERNAL_SECRET` | YES (fail-closed) | Shared secret. BFF refuses to start if missing. |
| `MEDTECH_API_BASE_URL` | YES | ALEX base URL e.g. `https://alexapiuat.medtechglobal.com/FHIR` |
| `MEDTECH_CLIENT_ID` | YES | Azure AD client ID |
| `MEDTECH_CLIENT_SECRET` | YES | Azure AD client secret |
| `MEDTECH_TENANT_ID` | YES | Azure AD tenant ID |
| `MEDTECH_API_SCOPE` | YES | OAuth scope e.g. `api://.../.default` |
| `MEDTECH_FACILITY_ID` | No | Default HPI facility code (can override per-request) |
| `NODE_ENV` | No | Set to `production` on Lightsail |
| `PORT` | No | Default 3000 |

Missing `MEDTECH_*` vars (other than `MEDTECH_FACILITY_ID`) will crash at runtime when the first request hits OAuth/ALEX, not at startup.

---

## Systemd operations

```bash
# Status
sudo systemctl status clinicpro-bff --no-pager

# Start / stop / restart
sudo systemctl start clinicpro-bff
sudo systemctl stop clinicpro-bff
sudo systemctl restart clinicpro-bff

# Live logs
sudo journalctl -u clinicpro-bff -f

# Last 50 lines
sudo journalctl -u clinicpro-bff -n 50

# View service definition
sudo systemctl cat clinicpro-bff
```

To update an env var without editing `.env`, use a systemd override:

```bash
sudo systemctl edit clinicpro-bff.service --force
# Add under [Service]:
# Environment="VAR_NAME=value"
sudo systemctl daemon-reload
sudo systemctl restart clinicpro-bff
```

---

## Deploying code changes

```bash
# SSH into Lightsail
ssh deployer@13.236.58.12

# Pull latest
cd /home/deployer/app
git pull origin main

# Install deps (if package.json changed)
npm install

# Restart
sudo systemctl restart clinicpro-bff

# Verify
sudo journalctl -u clinicpro-bff -n 20
curl http://localhost:3000/health
```

---

## Auth model

### BFF_INTERNAL_SECRET (Vercel → BFF)

- Vercel sends `x-internal-secret: <value>` on every request to BFF
- BFF validates with constant-time XOR comparison (timing-attack safe)
- All 16 protected routes return 401 if missing or wrong
- Two unprotected routes: `GET /` and `GET /health`
- BFF refuses to boot if `BFF_INTERNAL_SECRET` env var is missing or empty

Generating a new secret:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```
Set the same value in both places: Vercel env var + Lightsail `.env`.

### OAuth 2.0 (BFF → ALEX)

- Azure AD client credentials flow
- Token cached for 55 minutes (auto-refreshes before expiry)
- If ALEX returns 401, token is refreshed once and request retried automatically
- Token refresh is deduplicated: concurrent requests share one refresh promise

---

## All endpoints

### Unprotected

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Service info (name, time, medtech status) |
| GET | `/health` | Health check (status, timestamp) |

### Protected (require `x-internal-secret`)

| Method | Path | ALEX call | Rate limit | Notes |
|---|---|---|---|---|
| GET | `/api/medtech/token-info` | none | none | OAuth token cache status + env info |
| GET | `/api/medtech/document-reference/:id` | `GET /DocumentReference/{id}` | none | Verify a committed doc exists |
| GET | `/api/medtech/launch/decode` | `GET /vendorforms/api/getlaunchcontextstring/{context}/{signature}` | none | Decode Evolution vendor form launch params |
| GET | `/api/medtech/test` | `GET /Patient?identifier=...` | none | Test OAuth + FHIR connectivity |
| POST | `/api/medtech/session/commit` | `POST /DocumentReference` per file | none | Batch commit images (legacy; still live) |
| POST | `/api/patient-lookup` | `GET /Patient?identifier=...` | 60/min | NHI lookup; returns candidates array |
| GET | `/api/practitioners` | `GET /Practitioner` | 30/min | List practitioners at facility |
| POST | `/api/commit-scan` | `POST /DocumentReference` per image | 30/min | Batch commit TIFF images (current) |
| GET | `/api/medtech/media` | `GET /Media?patient.identifier=...` | none | Search media by NHI |
| GET | `/api/medtech/documents` | `GET /DocumentReference?patient=...` | none | Consultation notes (diagnostic) |
| GET | `/api/medtech/labs` | `GET /DiagnosticReport?patient=...` | none | Lab results (diagnostic) |
| GET | `/api/medtech/prescriptions` | `GET /MedicationRequest?patient=...` | none | Prescriptions (diagnostic) |
| GET | `/api/medtech/communications` | `GET /Communication?patient=...` | none | Referrals/messages (diagnostic) |
| GET | `/api/medtech/tasks` | `GET /Task?patient=...` | none | Tasks (diagnostic) |

Rate limits are per source IP, in-memory (resets on restart). These are Vercel's IPs, not end-user IPs. Per-user rate limiting is handled in Next.js (Postgres-backed).

---

## Key design decisions (non-obvious)

**Two DocumentReference POST endpoints.** `/api/medtech/session/commit` (legacy) and `/api/commit-scan` (current) both exist and are both live. Different request/response shapes. The newer one (`/api/commit-scan`) is what Vercel calls for new commits.

**Media uses `patient.identifier` not `patient=`.** `GET /Media?patient=<id>` returned 403 in UAT. Workaround: `patient.identifier=NHI_SYSTEM|{nhi}`. This is intentional.

**Allowed content types.** Inbox Scan accepts only `image/tiff` and `application/pdf`. JPEG/PNG are rejected. Content type is sniffed from magic bytes, not trusted from client.

**NHI collisions (B10).** All patient-lookup and media endpoints return 409 with a count if ALEX returns multiple patients for one NHI. No PHI in logs, only counts.

**8 MB per attachment.** Checked both on raw base64 string and decoded bytes.

**FHIR reference base URL.** `MEDTECH_API_BASE_URL` ends with `/FHIR` (uppercase). ALEX FHIR references use `/fhir` (lowercase). BFF normalises automatically when constructing subject/author references.

---

## Security headers (Helmet defaults)

CSP, X-Frame-Options: DENY, HSTS, X-Content-Type-Options: nosniff, Referrer-Policy: no-referrer, Cross-Origin policies. All from Helmet v8.1.0 defaults.

CORS is `origin: false` (blocks all browser origins). BFF is server-to-server only.

---

## Logging

All to stdout, captured by systemd journal. Structured with `correlationId` on every ALEX interaction. No external log service (no Sentry, CloudWatch, etc.).

No PHI in logs: NHI collision warnings log counts only, not names/NHI/DOB.

---

## Known issues and gaps

- `medtech-bff.js` is dead code, should be deleted.
- No circuit breaker on OAuth: if Azure AD is slow, every request hangs up to 10s.
- Diagnostic endpoints (documents, labs, etc.) don't consistently return `correlationId` in responses.
- Constants (timeouts, size limits, URL patterns) are scattered across files; no central config.
- No TypeScript. Request/response shapes are inferred from code only.
