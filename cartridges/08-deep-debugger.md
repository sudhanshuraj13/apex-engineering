# 08 — Multi-Hop Backward AST Tracer & Deep Debugger Cartridge
**Fused Winners:** `systematic-debugging`, `phase-gated-debugging`, `error-debugging-error-trace`

## 1. Negative Constraints (FORBIDDEN)
- NEVER guess a fix or edit application logic on Turn 1 when a bug is reported or a test fails.
- NEVER slap a band-aid null check (`if (!x) return`) at the crash site without tracing where `x` was corrupted upstream.
- NEVER retry a failed fix listed in `.apex/l1-register.json -> blacklisted_attempts`.

## 2. Mandatory 3-Step Scientific Debugging Loop
1. **Step 1 — Backward Hop Trace (`.apex/artifacts/trace-ledger.md`):**
   Trace callers backward from the crash line (`Hop 0 -> Hop 1 -> Hop 2`) using `ripgrep`/`graphify` and write the state table:
   ```markdown
   | Hop | File:Line | Function | Input Payload | Output / Mutation | Status |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | Hop 0 (Crash) | `billing.ts:84` | `chargeTenant` | `tenantId = undefined` | Throws TypeError | SYMPTOM |
   | Hop 1 (Caller) | `queue.ts:41` | `processJob` | `job.data.tenant_id` | Mapped wrong key `tenantId` | ROOT CAUSE |
   ```
2. **Step 2 — Binary Search Boundary Log & Red Test:**
   Write a standalone failing test that reproduces the exact bug (`RED`). If the bug spans >2 hops, inject a single `[APEX_TRACE_MIDPOINT]` log at the middle hop to bisect state in 1 run.
3. **Step 3 — Surgical Root-Cause Fix (`GREEN`):**
   Apply the minimal diff at the `ROOT CAUSE` hop, remove temporary trace logs, and log the resolution to `docs/ISSUE_TRACKER.md`.

## 3. Exit Gate & Handoff
- **Artifact Written:** `.apex/artifacts/trace-ledger.md` + `docs/ISSUE_TRACKER.md`
- **Gate Check:** `python scripts/apex_ctl.py verify` = `STATUS: PASS (Exit Code 0)`.
