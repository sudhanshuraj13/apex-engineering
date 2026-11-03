# 02 — Principal Architecture & Contracts Cartridge
**Fused Winners:** `c4-architecture`, `architecture-decision-records`, `openapi-spec-generation`

## 1. Negative Constraints (FORBIDDEN)
- NEVER create 4-layer Hexagonal/DDD ceremony (Factory -> Port -> AbstractInterface) for simple CRUD calls (Ponytail YAGNI).
- NEVER leave API payloads untyped; define strict input/output schemas before backend/frontend coding starts.
- NEVER store architectural choices only in chat history; persist them to `.apex/artifacts/02-contracts.md`.

## 2. Canonical Contract Skeleton (`.apex/artifacts/02-contracts.md`)
```yaml
# Architecture Decision & API Contract Baton
stack:
  runtime: "Next.js App Router / FastAPI"
  db_isolation: "PostgreSQL + Row-Level Security (tenant_id)"
  queue_cache: "Redis + BullMQ"

endpoints:
  POST /api/v1/resource:
    auth: "Bearer JWT + Tenant-ID Header"
    idempotency_Header: "X-Idempotency-Key (Required)"
    request_schema:
      tenantId: "uuid"
      amountCents: "integer > 0"
    response_200: "{ id: uuid, status: 'PROCESSED' }"
    error_rfc7807: "{ type: string, title: string, status: number, detail: string }"
```

## 3. Exit Gate & Handoff
- **Artifact Written:** `.apex/artifacts/02-contracts.md`
- **Gate Check:** Validate contract schemas match `.apex/artifacts/01-prd.md`.
- **Next Recommended Skill:** `03-database-tenancy`
