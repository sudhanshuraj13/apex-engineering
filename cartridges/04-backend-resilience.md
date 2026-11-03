# 04 — Backend APIs, Zod Validation & Resilience Cartridge
**Fused Winners:** `backend-architect`, `api-design-principles`, `zod-validation-expert`, `error-handling-patterns`, `test-driven-development`

## 1. Negative Constraints (FORBIDDEN)
- NEVER trust `req.body`, `req.query`, or webhook payloads without strict schema parsing (Zod / Pydantic) at the controller boundary.
- NEVER process payment/state-mutating webhooks without an atomic idempotency lock.
- NEVER call external HTTP APIs without an explicit timeout (`AbortSignal.timeout(5000)`).
- NEVER swallow errors with empty `catch {}` blocks; return RFC 7807 structured JSON errors.

## 2. Canonical Code Skeleton (Validated + Idempotent Endpoint)
```typescript
import { z } from "zod";

const PayloadSchema = z.object({
  eventId: z.string().min(1),
  tenantId: z.string().uuid(),
  amountCents: z.number().int().positive(),
});

export async function handleWebhook(rawBody: unknown, redis: RedisClient) {
  const parsed = PayloadSchema.safeParse(rawBody);
  if (!parsed.success) {
    return { status: 400, body: { title: "Validation Failed", issues: parsed.error.flatten() } };
  }
  const { eventId, tenantId, amountCents } = parsed.data;

  // Atomic Idempotency Lock (SET NX EX 86400)
  const locked = await redis.set(`idemp:${eventId}`, "PROCESSING", "NX", "EX", 86400);
  if (!locked) return { status: 200, body: { status: "DUPLICATE_IGNORED" } };

  try {
    await processLedgerUpdate(tenantId, amountCents);
    await redis.set(`idemp:${eventId}`, "COMPLETED", "EX", 86400);
    return { status: 200, body: { status: "OK" } };
  } catch (err) {
    await redis.del(`idemp:${eventId}`); // Release lock on transient failure
    throw err;
  }
}
```

## 3. Exit Gate & Handoff
- **Gate Check:** Typecheck (`tsc --noEmit` / `mypy`) + Unit Tests + `python scripts/apex_ctl.py verify` = `Exit Code 0`.
- **Next Recommended Skill:** `05-frontend-craft`
