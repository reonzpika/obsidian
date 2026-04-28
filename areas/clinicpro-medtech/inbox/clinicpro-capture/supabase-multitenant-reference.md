# Supabase Multi-Tenancy Reference

**Context:** ClinicPro Capture, Next.js 14+ / Supabase / Vercel. Each GP practice = one tenant. RLS currently disabled, no tenant_id, three tables: `tenants`, `captures`, `audit_log`.

**Research date:** April 2026. Sources verified against current Supabase documentation and community practice.

---

## 1. Supabase's Current Recommended Approach

**As of April 2026, Supabase's canonical recommendation is RLS + shared tables + tenant_id column.** This has not changed since mid-2025. Supabase does not recommend schema-per-tenant or project-per-tenant for new SaaS builds. The official documentation, community guides, and third-party SaaS frameworks (e.g. Makerkit, published January 2026) all converge on this pattern.

Platform changes since mid-2025 worth noting:

- **Declarative Schemas** (GA): define schema as SQL files, Supabase CLI diffs and generates migrations. Simplifies managing shared-table schema evolution. Does not address schema-per-tenant.
- **Custom Access Token Hook** (available Free/Pro): runs before every JWT is issued, injects custom claims including `tenant_id`. This is now the standard mechanism for baking tenant context into the JWT. No external token service required.
- **Supabase Branching**: for dev/staging/preview environments only. It is not a multi-tenancy mechanism and has no bearing on the tenant isolation decision.
- **HIPAA BAA**: available on Team and Enterprise plans. Required if storing NZ health data subject to equivalent obligations.

No Supabase platform feature released in late 2025 or early 2026 makes schema-per-tenant meaningfully more practical. Dynamic schema creation still requires superuser privileges, which managed Supabase projects do not expose.

---

## 2. Comparison Table

| Criterion | RLS + tenant_id | Schema-per-tenant | Project-per-tenant |
|---|---|---|---|
| **Isolation level** | Row-level (logical). Breach requires policy misconfiguration. | Schema-level (logical). Stronger separation but same DB instance. | Full physical isolation. Separate DB, auth, storage. |
| **Complexity** | Low-medium. Standard Postgres. RLS policies can be subtle. | High. Migrations must run per-schema. No Supabase tooling support. Requires superuser for dynamic schema creation. | Very high. Each tenant = separate project. No unified management plane. |
| **Performance at scale** | Good with proper indexing. See Section 3. | Slightly lower query overhead per-tenant (no RLS evaluation). Does not scale past ~a few hundred schemas without operational pain. | No shared-resource contention. Scales linearly but at high cost. |
| **Cost** | One project. Fixed compute. Scales with data, not tenant count. | One project. Same cost structure as RLS approach. | ~$25+/month per tenant project on Pro. 100 practices = ~$2,500+/month minimum, plus compute per project. |
| **Migration from current state** | Moderate. Add tenant_id columns, backfill, enable RLS, add policies, add index. Incremental. | Large. Requires schema-splitting all data. No Supabase tooling. Risk is high. | Largest. Data export/import per tenant. Separate auth systems. Essentially a rewrite. |
| **Supabase platform support** | First-class. Declarative Schemas, Custom Access Token Hook, Supabase Studio RLS editor. | Minimal. Custom schemas must be manually added to PostgREST exposed schemas. No migration tooling. | Supported but not designed for this use case. No cross-project management. |

---

## 3. RLS + tenant_id Deep Dive

### How tenant_id flows

```
User logs in
    -> Supabase Auth issues JWT
    -> Custom Access Token Hook fires (Postgres function or Edge Function)
    -> Hook reads tenant_id from auth.users.app_metadata
    -> Hook injects tenant_id into JWT claims
    -> Client receives JWT containing tenant_id
    -> Every DB request from client includes JWT
    -> RLS policy extracts tenant_id from JWT, filters rows
```

### auth.uid() vs custom JWT claims for tenant resolution

Two approaches:

**Option A: JWT claim via Custom Access Token Hook (recommended)**

Store `tenant_id` in `app_metadata` when a user is assigned to a practice. The hook promotes it into the JWT top-level claims. RLS reads it with a stable helper function. One DB call per login, zero per query.

**Option B: Join to a memberships table in the RLS policy**

The policy joins `auth.uid()` against a `practice_memberships` table to find the tenant. Correct but slower: the join executes on every query. Only use this if a user can belong to multiple tenants simultaneously and the active tenant changes without re-login.

For ClinicPro Capture (one user = one practice), Option A is correct.

**Critical:** always use `app_metadata`, never `user_metadata`. `user_metadata` can be modified by the authenticated user. `app_metadata` is server-only and cannot be self-modified.

### Implementation

**Step 1: Store tenant_id in app_metadata when assigning a user to a practice**

```typescript
// Server-side only (service role)
await supabase.auth.admin.updateUserById(userId, {
  app_metadata: { tenant_id: practiceId }
})
```

**Step 2: Custom Access Token Hook (Postgres function)**

Create this in Supabase SQL editor. It promotes `tenant_id` from `app_metadata` into the JWT top-level claims so RLS can read it without a nested JSON path.

```sql
create or replace function public.custom_access_token_hook(event jsonb)
returns jsonb
language plpgsql
stable
as $$
declare
  claims jsonb;
  tenant text;
begin
  claims := event -> 'claims';
  tenant := (event -> 'claims' -> 'app_metadata' ->> 'tenant_id');

  if tenant is not null then
    claims := jsonb_set(claims, '{tenant_id}', to_jsonb(tenant));
  end if;

  return jsonb_set(event, '{claims}', claims);
end;
$$;

-- Grant execute to supabase_auth_admin
grant execute on function public.custom_access_token_hook to supabase_auth_admin;
```

Then enable it in Supabase Dashboard: Authentication -> Hooks -> Custom Access Token.

**Step 3: Helper function for RLS policies**

```sql
create or replace function auth.tenant_id()
returns text
language sql
stable
as $$
  select nullif(
    current_setting('request.jwt.claims', true)::jsonb ->> 'tenant_id',
    ''
  )::text
$$;
```

The `stable` marker allows Postgres to cache the result within a query. Wrap in `(select auth.tenant_id())` inside policies for per-statement caching (see performance note below).

**Step 4: RLS policy for the `captures` table**

```sql
alter table captures enable row level security;

-- Authenticated users see only their practice's captures
create policy "captures: tenant read"
  on captures
  for select
  to authenticated
  using (tenant_id = (select auth.tenant_id()));

create policy "captures: tenant insert"
  on captures
  for insert
  to authenticated
  with check (tenant_id = (select auth.tenant_id()));

create policy "captures: tenant update"
  on captures
  for update
  to authenticated
  using  (tenant_id = (select auth.tenant_id()))
  with check (tenant_id = (select auth.tenant_id()));

create policy "captures: tenant delete"
  on captures
  for delete
  to authenticated
  using (tenant_id = (select auth.tenant_id()));
```

**Step 5: RLS policy for the `audit_log` table**

Audit logs should be insert-only for authenticated users. No update or delete. Only the service role (backend) should query across tenants.

```sql
alter table audit_log enable row level security;

-- Users can read their own practice's audit log
create policy "audit_log: tenant read"
  on audit_log
  for select
  to authenticated
  using (tenant_id = (select auth.tenant_id()));

-- Users (via app) can insert audit events for their own tenant
create policy "audit_log: tenant insert"
  on audit_log
  for insert
  to authenticated
  with check (tenant_id = (select auth.tenant_id()));

-- No update or delete policies: audit log is append-only for tenants
-- Service role bypasses RLS and can query all rows
```

**Step 6: Index**

```sql
-- Add to every tenant-scoped table
create index ix_captures_tenant_id on captures using btree (tenant_id);
create index ix_audit_log_tenant_id on audit_log using btree (tenant_id);
```

### Service role bypass

The Supabase service role key bypasses all RLS. This is intentional and correct for admin operations (cross-tenant analytics, support queries, backfilling tenant_id during migration). Risks and rules:

- Never expose the service role key to the browser or client-side code.
- Never pass it through Vercel environment variables accessible to client bundles (use `SUPABASE_SERVICE_ROLE_KEY` only in server-side API routes or Edge Functions, not in `NEXT_PUBLIC_*` variables).
- In Next.js API routes and Server Actions, create a separate `supabaseAdmin` client using the service role key. Keep it isolated from the user-facing `supabase` client that uses the anon key.
- When using the service role for admin queries, always add an explicit `WHERE tenant_id = ?` filter in the query. RLS is off but your application logic should still scope queries defensively.

```typescript
// Server-side only (API route / Server Action)
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // never NEXT_PUBLIC_
  { auth: { autoRefreshToken: false, persistSession: false } }
)

// Always scope explicitly even when bypassing RLS
const { data } = await supabaseAdmin
  .from('captures')
  .select('*')
  .eq('tenant_id', targetTenantId) // defensive filter
```

---

## 4. Performance Characteristics of RLS at Scale

Formal Supabase benchmarks for specific tenant counts are not publicly published. The following is derived from documented optimisation guidance and community production reports.

**Key principle:** RLS adds a `WHERE` clause to every query. Performance depends on whether the database can use an index to satisfy that clause. With a proper `btree` index on `tenant_id`, RLS overhead is minimal. Without it, Postgres performs a sequential scan.

| Scale | Behaviour with index | Behaviour without index |
|---|---|---|
| 100 tenants, small tables | Negligible overhead. Sub-millisecond policy evaluation. | Still fast if total rows are small. |
| 1,000 tenants, medium tables (100k rows each) | Fast. Index lookup isolates tenant rows immediately. Query time dominated by data retrieval, not policy. | Noticeable degradation. Queries scanning full table to find tenant rows. |
| 10,000 tenants (hypothetical) | Scales well. tenant_id index is as effective at 10k tenants as at 100. | Severe degradation. Sequential scans across millions of rows. |

**Additional performance rules:**

- Use `(select auth.tenant_id())` not `auth.tenant_id()` directly in policies. The `select` wrapper allows Postgres to evaluate the function once per statement rather than once per row.
- Add explicit `.eq('tenant_id', tenantId)` filters in client queries. This helps the query planner choose the index path even before evaluating the RLS clause.
- Avoid joins inside RLS policies. If the policy needs to check a membership table, wrap that in a `security definer` function so the join result can be cached.
- Community benchmark: a policy rewrite from subquery to function-based approach reduced query time from ~450ms to ~45ms on a 10,000-row table (10x improvement). Source: AntStack optimisation post.

---

## 5. Audit Requirements: Is RLS + tenant_id Sufficient?

Supabase's built-in auth audit log (`auth.audit_log_entries`) captures authentication events only: logins, signups, password resets, token refreshes, MFA events. It does not log data access (which rows were read, which captures were viewed).

For a health app with clinical data access requirements, the built-in auth log is necessary but not sufficient. You need an application-level audit log.

**ClinicPro Capture already has an `audit_log` table.** This is the right approach. RLS + tenant_id does not weaken your audit capability: the audit log records who did what at the application layer, and RLS ensures each practice can only read its own audit records.

**What RLS provides for audit:**
- Ensures a tenant cannot read another tenant's audit_log rows (policy above).
- Prevents a tenant from inserting audit events attributed to another tenant (with check clause).
- Service role retains full cross-tenant read for compliance reporting.

**What you must do in application code:**
- Every write to `captures` must also write a row to `audit_log` with: `tenant_id`, `user_id`, `action` (create/update/delete), `resource_id`, `timestamp`, and optionally `ip_address` and `user_agent` from the request.
- The audit_log write must happen in the same Postgres transaction as the primary action, or via a database trigger, to guarantee the log cannot be written without the event.

**Schema isolation is not required for audit sufficiency.** The audit trail is complete as long as your application writes it correctly and the append-only policy is enforced at the RLS layer.

---

## 6. Schema-per-Tenant: When Does It Make Sense?

Schema-per-tenant is worth considering only when:

- Tenants require genuinely different table structures (uncommon in GP SaaS).
- Regulatory requirements mandate physical schema separation (not standard NZ PHO requirements).
- Tenant count is small (under ~50) and each tenant has a very large data volume requiring dedicated tuning.

**In Supabase as of 2026, schema-per-tenant is not practical for new builds.** Reasons:

- Dynamic schema creation (e.g. `CREATE SCHEMA tenant_abc`) requires superuser, which Supabase managed projects do not expose.
- Each schema must be manually added to PostgREST's exposed schemas list in project settings. This cannot be automated via the Supabase platform API in a self-serve way.
- Migrations must be executed per-schema, which has no tooling support in Supabase CLI or Declarative Schemas.
- Supabase Studio, the RLS editor, and type generation all assume the `public` schema. Custom schemas are second-class.

If you genuinely need schema-per-tenant, the correct tool is a self-hosted Postgres instance (e.g. Neon, RDS) where you have superuser control. Not Supabase managed.

---

## 7. ClinicPro Capture Recommendation

Use **RLS + shared tables + tenant_id column**. The app has three tables, a small-to-medium projected tenant count (GP practices in a regional market), no requirement for per-tenant schema customisation, and an existing `tenants` table that already models the right concept. The migration path is incremental and reversible: add `tenant_id` columns, backfill existing rows (likely zero or minimal data at MVP stage), enable RLS, add policies, add indexes, enable the Custom Access Token Hook. Project-per-tenant is ruled out on cost alone: at 50 practices the minimum Supabase bill would be $1,250+/month before compute, which is unjustifiable. Schema-per-tenant is ruled out by Supabase platform constraints described above. RLS + tenant_id is the correct choice for this stack, this scale, and this timeline.

---

## 8. Migration Checklist: RLS Disabled to Multi-Tenant RLS

Ordered steps. Each step is independently deployable. Do not enable RLS on a table until its policies and indexes are ready.

### Phase 1: Foundation (no user impact)

- [ ] Add `tenant_id uuid not null references tenants(id)` to `captures` table.
- [ ] Add `tenant_id uuid not null references tenants(id)` to `audit_log` table.
- [ ] If there are existing rows, backfill `tenant_id` using service role (assign to the single existing practice or a seed tenant).
- [ ] Create btree indexes: `ix_captures_tenant_id`, `ix_audit_log_tenant_id`.
- [ ] Create the `auth.tenant_id()` helper function (SQL above).
- [ ] Create the `custom_access_token_hook` Postgres function (SQL above).

### Phase 2: Auth hook (low risk, no RLS yet)

- [ ] Enable the Custom Access Token Hook in Supabase Dashboard: Authentication -> Hooks -> Custom Access Token -> select `public.custom_access_token_hook`.
- [ ] Assign `tenant_id` to all existing users in `app_metadata` via service role script.
- [ ] Verify: log in as a test user, decode the JWT (jwt.io), confirm `tenant_id` claim is present.
- [ ] Verify: new user signup flow assigns `tenant_id` to `app_metadata` before or immediately after account creation.

### Phase 3: Update application writes

- [ ] Update all `captures` insert/update operations to include `tenant_id` from the authenticated user's session.
- [ ] Update all `audit_log` insert operations to include `tenant_id`.
- [ ] Test that existing rows and new rows all have correct `tenant_id` values.

### Phase 4: Enable RLS (reversible per table)

- [ ] Enable RLS on `captures`: `alter table captures enable row level security;`
- [ ] Add all four policies for `captures` (select, insert, update, delete) as shown above.
- [ ] Smoke test: log in as practice A user, confirm only practice A rows visible.
- [ ] Enable RLS on `audit_log`: `alter table audit_log enable row level security;`
- [ ] Add select and insert policies for `audit_log`. Do not add update or delete policies.
- [ ] Smoke test audit_log tenant isolation.
- [ ] Enable RLS on `tenants` table with appropriate policy (users can read their own tenant row).

### Phase 5: Harden service role usage

- [ ] Audit all server-side code (API routes, Server Actions) that uses the service role client.
- [ ] Confirm `SUPABASE_SERVICE_ROLE_KEY` is not in any `NEXT_PUBLIC_*` environment variable.
- [ ] Add explicit `tenant_id` filters to all service role queries as a defensive measure.
- [ ] Confirm Vercel production environment variables are set correctly.

### Phase 6: Verify and monitor

- [ ] Run Supabase Advisor (Dashboard -> Advisors) to check for RLS policy warnings.
- [ ] Review query performance in Supabase Dashboard -> Query Performance. Confirm tenant_id indexes are being used.
- [ ] Add an integration test that verifies a user from practice A cannot retrieve practice B rows (returns empty, not error).

---

## Sources

- [Supabase: Row Level Security docs](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase: Custom Access Token Hook docs](https://supabase.com/docs/guides/auth/auth-hooks/custom-access-token-hook)
- [Supabase: Auth Hooks overview](https://supabase.com/docs/guides/auth/auth-hooks)
- [Supabase: Auth Audit Logs](https://supabase.com/docs/guides/auth/audit-logs)
- [Supabase: Custom Claims and RBAC](https://supabase.com/docs/guides/database/postgres/custom-claims-and-role-based-access-control-rbac)
- [Supabase: Declarative Schemas feature](https://supabase.com/features/declarative-schemas)
- [Supabase RLS Best Practices: Production Patterns (Makerkit, January 2026)](https://makerkit.dev/blog/tutorials/supabase-rls-best-practices)
- [Supabase Multi Tenancy: Simple and Fast (Ryan O'Neill, Substack)](https://roughlywritten.substack.com/p/supabase-multi-tenancy-simple-and)
- [Multi-Tenant Applications with RLS on Supabase (AntStack)](https://www.antstack.com/blog/multi-tenant-applications-with-rls-on-supabase-postgress/)
- [Optimizing RLS Performance with Supabase (AntStack)](https://www.antstack.com/blog/optimizing-rls-performance-with-supabase/)
- [Multi-Tenant Authentication with Supabase: Production Implementation (Medium, March 2026)](https://medium.com/@kriryk/multi-tenant-authentication-with-supabase-a-production-implementation-0f6064f50d55)
- [Supabase Pricing 2026 (UI Bakery)](https://uibakery.io/blog/supabase-pricing)
