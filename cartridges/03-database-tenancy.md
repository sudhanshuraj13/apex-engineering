# 03 — Database Schema & Multi-Tenant RLS Cartridge
**Fused Winners:** `saas-multi-tenant`, `postgres-best-practices`, `postgresql-optimization`, `database-migrations-sql-migrations`

## 1. Negative Constraints (FORBIDDEN)
- NEVER query multi-tenant tables without `tenant_id` indexed and enforced via PostgreSQL Row-Level Security (RLS).
- NEVER use `SELECT *` or run unindexed foreign key joins.
- NEVER write destructive migrations (`DROP COLUMN` / `DROP TABLE`) without explicit Supervisor Gate approval and a rollback down-migration.

## 2. Canonical Code Skeleton (Postgres RLS + Safe Tenant Transaction)
```sql
-- 1. Migration: Enable RLS & Force Tenant Isolation
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions FORCE ROW LEVEL SECURITY;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_subs_tenant_id ON subscriptions(tenant_id);

CREATE POLICY tenant_isolation_policy ON subscriptions
  USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
```
```typescript
// 2. Runtime Wrapper: Scoped Tenant Transaction (Prisma / SQL)
export async function withTenant<T>(db: PrismaClient, tenantId: string, fn: (tx: Prisma.TransactionClient) => Promise<T>): Promise<T> {
  return db.$transaction(async (tx) => {
    await tx.$executeRaw`SELECT set_config('app.current_tenant_id', ${tenantId}, true)`;
    return fn(tx);
  });
}
```

## 3. Exit Gate & Handoff
- **Gate Check:** Schema validation (`npx prisma validate` or SQL syntax check) + `python scripts/apex_ctl.py verify`.
- **Next Recommended Skill:** `04-backend-resilience`
