# 06 — OWASP Zero-Trust & BOLA Security Audit Cartridge
**Fused Winners:** `security-audit`, `backend-security-coder`, `auth-implementation-patterns`, `idor-testing`, `sql-injection-testing`

## 1. Negative Constraints (FORBIDDEN)
- NEVER trust `tenantId` or `userId` from request body/query params without verifying it against the authenticated session token (BOLA / IDOR prevention).
- NEVER compare webhook signatures, API keys, or HMAC digests using `===` or `==` (vulnerable to timing attacks); ALWAYS use `crypto.timingSafeEqual`.
- NEVER interpolate user input into raw SQL strings, shell commands (`exec`), or `eval()`.
- NEVER log raw tokens, passwords, PII, or `.env` secrets to `console.log`.

## 2. Canonical Code Skeleton (Timing-Safe Signature + BOLA Guard)
```typescript
import crypto from "node:crypto";

export function verifyWebhookSignature(payload: string, headerSig: string, secret: string): boolean {
  const expected = crypto.createHmac("sha256", secret).update(payload, "utf8").digest("hex");
  const a = Buffer.from(headerSig, "utf8");
  const b = Buffer.from(expected, "utf8");
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

export function assertTenantAccess(sessionTenantId: string | undefined, resourceTenantId: string): void {
  if (!sessionTenantId || sessionTenantId !== resourceTenantId) {
    throw new Error("FORBIDDEN_BOLA_VIOLATION: Cross-tenant access denied");
  }
}
```

## 3. Exit Gate & Handoff
- **Artifact Written:** `.apex/artifacts/06-sec-audit.json`
- **Gate Check:** Zero hardcoded secrets / dynamic SQL + `python scripts/apex_ctl.py verify` = `Exit Code 0`.
- **Next Recommended Skill:** `07-devops-cloud-cicd`
