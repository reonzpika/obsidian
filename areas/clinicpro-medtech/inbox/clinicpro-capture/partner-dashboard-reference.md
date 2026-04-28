# Partner Dashboard Reference: ClinicPro Capture / Medtech Global

**Purpose:** Architecture decision reference for the Medtech Global distributor dashboard.
**Audience:** Solo technical founder making an implementation choice at AU launch stage.
**Date:** April 2026

---

## 1. Partner Dashboard vs Internal Admin Dashboard

The distinction is about data ownership, trust boundaries, and commercial sensitivity.

### What the internal admin (ClinicPro) sees

- All tenants across all regions and channels
- Raw user activity logs, error logs, audit trails
- Individual user accounts (names, emails, login history)
- Revenue, billing events, churn signals
- Support tickets, onboarding friction metrics
- Infrastructure costs per tenant

### What a partner/distributor sees

The partner is a reseller, not an operator. They need enough data to:

1. Confirm their referred practices are onboarded and active
2. Reconcile their monthly billing (which practices do they owe you for, or do you owe them credit for)
3. Flag churning practices before they become a dispute

They do not need:

- PII beyond practice name and ID (individual clinician names, emails, usage patterns tied to a person)
- Data on practices not in their bundle
- ClinicPro's internal margins, cost structure, or direct-channel customers
- Raw logs, error rates, or infrastructure data
- Practices from other distributors or regions

### The boundary rule

The partner's data scope is: **practices tagged to their partner account, aggregated to practice level, for the current and trailing billing period.** Nothing else crosses the boundary.

This is both a privacy posture (NZ/AU health context, Privacy Act obligations apply) and a commercial posture (you do not reveal your direct-channel business to a reseller).

---

## 2. How Real B2B SaaS Products Handle This

### Stripe Connect (most relevant pattern)

Stripe separates the platform account (you) from connected accounts (practices, in analogy) and the partner is somewhere between. The key pattern: **the platform controls what each party sees, data is scoped by account relationship, not by role alone.**

Relevant for ClinicPro: the practice is the tenant, Medtech is an intermediary with a scoped read view. Stripe enforces this at the API key level: a restricted key for connected accounts cannot read platform-level data.

**Takeaway:** scope at the database/API layer, not just the UI.

### Vercel Team Billing

Vercel exposes team-level usage (deployments, bandwidth, seat count) to team owners without exposing other teams' data. The billing owner sees aggregate usage and invoice line items. Individual members' activity is visible only in aggregate or stripped of personal attribution for non-owners.

**Takeaway:** billing-reconciliation views should show counts and totals, not individual user rows, unless the partner has a legitimate need for the individual row.

### Shopify Partner Portal

Partners see their referred merchants: install status, active/inactive, plan tier, and a revenue share calculation. They cannot see merchant revenue, product catalogue, or customer data. The portal is entirely separate from the merchant admin.

**Takeaway:** a fully separate portal (separate subdomain, separate auth) is the dominant B2B pattern for reseller/distributor relationships. It signals clearly where the trust boundary is and avoids accidental over-exposure as the app evolves.

### Twilio Subaccounts

Twilio lets resellers create subaccounts that roll up under a master account. Usage per subaccount is visible to the master; individual end-customer data stays in the subaccount. The reseller billing view shows usage totals per subaccount without exposing the subaccount's internals.

**Takeaway:** the aggregation model (roll up to distributor, not drill down into tenant) is the right posture for a health context.

### Xero Advisor Portal (most analogous to health/NZ context)

Xero Partners (accounting firms) get a practice manager view: their client organisations listed with subscription status, user count, last active date, and a quick-access link. They cannot see another firm's clients. Xero's trust model is: the partner sees their book of clients, never a cross-partner view.

**Takeaway:** this is the closest analogue. A practice manager view scoped to Medtech Global's referred practices, with status and usage at practice level, is exactly what you need.

---

## 3. What Medtech Global Realistically Needs

Based on the AUD 30/active practice/month billing model, Lawrence's team needs to:

- Verify which practices are live (to invoice ClinicPro or confirm credits)
- Confirm activity for the billing period (to define "active")
- Track onboarding of new referrals (to know when a pipeline referral converts)

### Dashboard sections and data

#### 3.1 Summary bar (top of page)

| Metric | Definition |
|---|---|
| Total practices in bundle | Count of practices with `partner_id = medtech_global`, any status |
| Active this month | Practices with at least 1 capture submitted in the current calendar month |
| Inactive this month | Practices in bundle with 0 captures this calendar month |
| New this month | Practices whose `onboarded_at` falls in the current calendar month |

#### 3.2 Practice list (main table)

One row per practice. Sortable by status, last active, captures.

| Column | Definition |
|---|---|
| Practice name | Display name set at onboarding |
| Practice ID | Internal ID (for dispute resolution reference) |
| Region/State | AU state for their records |
| Status | `active` / `inactive` / `onboarding` |
| Onboarded date | Date the practice completed onboarding |
| Active users (MTD) | Count of distinct user IDs who submitted captures this month |
| Captures (MTD) | Total capture submissions this month |
| Captures (prior month) | Total capture submissions last calendar month (billing reference) |
| Last capture date | Most recent capture timestamp, date only |
| Billable (prior month) | Boolean: did this practice have at least 1 capture in the prior month? Used for invoice reconciliation |

#### 3.3 Billing reconciliation export

A downloadable CSV covering the prior calendar month. One row per practice. Columns: Practice ID, Practice name, Captures (prior month), Billable (yes/no), Onboarded date.

This is what Lawrence's team needs to reconcile the monthly invoice. It does not require a live dashboard view.

#### 3.4 Onboarding pipeline (optional, low priority)

If Medtech Global refers practices that are not yet live, a simple table of referred-but-not-onboarded practices: referred date, contact name (practice manager only, not clinicians), current step in onboarding. Omit if onboarding is ClinicPro-managed end to end.

### What to withhold

- Individual clinician names or emails
- Capture content or clinical metadata
- Error rates or failed uploads
- Any practice not tagged to `partner_id = medtech_global`
- Direct-channel NZ practices

---

## 4. Implementation Options: Supabase + Next.js

### Option A: Separate partner portal

A distinct Next.js app (or a separate route group under `/partner`) with its own Supabase auth flow. Medtech Global users sign in with a separate credential (Supabase magic link or email/password under a `partner_users` table). All queries in this app are scoped by `partner_id` at the RLS level.

**Implementation sketch:**

- Supabase RLS policy on a `partner_practice_view` (materialised or regular view): `WHERE partner_id = auth.jwt() ->> 'partner_id'`
- Partner JWT carries `partner_id` as a custom claim set at sign-in via a Supabase Edge Function or auth hook
- Next.js route group `/partner/**` with its own layout and middleware checking for `role = partner`
- Billing export: a Supabase Edge Function that generates and returns a signed CSV URL

**Complexity:** medium. Adds a second auth flow and a set of scoped views. About 2-3 days of focused build.

**Security trade-offs:** clean separation. Partner credentials cannot touch practice-level app routes. RLS enforces the boundary at the database layer, not just the UI. Easiest to audit.

**Suitability:** good. Scales to multiple partners later (add rows to `partners` table, issue credentials). Shopify and Xero both use this model. The cost is a slightly higher initial build.

### Option B: Role-based access within the existing app

Add a `partner` role to the existing Supabase auth. Partner users log in at the same URL, see a filtered view of the existing admin UI. RLS policies scope their queries to their `partner_id`.

**Implementation sketch:**

- Add `role: partner` and `partner_id` to user metadata
- Middleware redirects `partner` role to `/dashboard/partner/*` routes
- Reuse existing components with conditional rendering based on role
- RLS policies gate partner-role users to their scoped view

**Complexity:** lower initial build (reuses auth and UI scaffolding), but higher ongoing cognitive overhead.

**Security trade-offs:** the trust boundary is enforced by middleware and RLS, not by auth domain separation. A misconfigured route or missing RLS policy could expose internal-admin views to a partner user. Harder to audit as the app grows. Also mixes partner UX with internal UX, which creates pressure to over-expose features.

**Suitability:** acceptable for a single partner at launch if build time is the constraint. Becomes messy as the app evolves. Not recommended if you anticipate more than one distributor.

### Option C: Data export / scheduled report

No live dashboard. A scheduled Supabase Edge Function or Vercel cron job generates a CSV or PDF report each month (or on demand via a simple auth-gated URL) and emails it or drops it in a shared Google Drive folder.

**Implementation sketch:**

- Supabase Edge Function querying `captures` grouped by `practice_id` for the prior month, filtered by `partner_id = medtech_global`
- Output: CSV attached to an email via Resend, or written to a Drive folder via service account
- Auth gate: a signed URL or a shared password-protected link (Vercel password protection on a `/partner/report` route)

**Complexity:** lowest. A single Edge Function plus a cron schedule. Build time is hours, not days.

**Security trade-offs:** no live session to compromise. The attack surface is the signed URL or password. If the CSV is emailed, it enters Medtech Global's email environment, which you cannot control. No PII in the export mitigates this.

**Suitability:** entirely appropriate for a new AU market with one distributor and a straightforward billing model. Medtech Global's team wants a number to reconcile an invoice, not a live dashboard. A monthly CSV plus a billing-period summary email is sufficient until volume or complexity demands more.

---

## 5. Recommendation

At AU launch with a single distributor and a per-active-practice billing model, start with Option C: a scheduled monthly CSV export plus an on-demand signed report URL. Build the Supabase Edge Function to generate the scoped report, schedule it to run on the 1st of each month for the prior month, and deliver via Resend to Lawrence's nominated billing contact. This takes hours to build, is auditable, has minimal attack surface, and directly answers the only real need: invoice reconciliation. The data in the export maps directly to the billing table in section 3.2 (prior month columns only).

If Medtech Global grows to 20+ practices and requests live visibility, or if you add a second distributor, graduate to Option A (separate portal with scoped RLS view). The RLS policy and partner-scoped view you write for Option C become the foundation for Option A with minimal rework. Do not build a live portal for a distributor who does not yet have enough practices to need one.

---

## Appendix: Supabase schema notes

Practices need a `partner_id` column (nullable, `uuid` or `text` referencing a `partners` table). RLS policy on any billing/usage view:

```sql
-- On partner_usage_view
CREATE POLICY "partner sees own practices"
ON partner_usage_view
FOR SELECT
USING (
  partner_id = (auth.jwt() ->> 'partner_id')::uuid
  OR (auth.jwt() ->> 'role') = 'admin'
);
```

Custom JWT claim `partner_id` set via Supabase auth hook (Edge Function triggered on `auth.sign_in`):

```typescript
// supabase/functions/custom-claims/index.ts
const partnerUser = await supabase
  .from('partner_users')
  .select('partner_id')
  .eq('user_id', event.user.id)
  .single()

if (partnerUser.data) {
  return {
    ...event,
    claims: {
      ...event.claims,
      partner_id: partnerUser.data.partner_id,
      role: 'partner',
    },
  }
}
```

This pattern works for both Option A and Option B if you later graduate from Option C.
