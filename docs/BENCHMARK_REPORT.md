# ApexHarness — BharatCode Build League Empirical Benchmark Report

- **Timestamp:** `2026-11-03 17:19 IST`
- **Target Model:** `qwen-3.8-27b` via `https://bharatcode.ai/api/model/v1/chat/completions` (`store: false`)
- **Verification Suite Status:** `PASS (12/12 Tests, Exit Code 0)`
- **Overall Queue & Context Token Reduction:** **`98.7%`** (`253500` raw tokens -> `3353` Apex sliced tokens)

## Why This Matters for BharatCode Infrastructure
1. **Shared Queue Acceleration:** BharatCode uses shared queue capacity where heavier requests wait longer. By slicing payloads to `<450 tokens`, `ApexHarness` lets `qwen-3.8-27b` execute in the fast lane.
2. **Stateless API Memory (`store: false`):** BharatCode's API does not persist conversation state server-side. `ApexHarness` maintains state locally via `.apex/l1-register.json` (180-token FSA) and `.apex/l3-archive.db` (SQLite BM25).
3. **Zero 6-Try Loops:** Failed verifications automatically populate `blacklisted_attempts` in L1 memory so `qwen-3.8-27b` never repeats a broken fix.

## Stage-by-Stage Token & Reliability Scorecard

| Stage | Challenge Description | Active Cartridge | Raw Prompt Tokens | Apex Sliced Tokens | Token & Queue Saved | Boot Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | Multi-Tenant Postgres RLS Isolation | `03-database-tenancy.md` | `61550` | **`797`** | **`98.7%`** | `317 ms` |
| **Stage 2** | Stripe Webhook Redis Idempotency & Circuit Breaker | `08-deep-debugger.md` | `63350` | **`877`** | **`98.6%`** | `346 ms` |
| **Stage 3** | Hostile 5-CWE OWASP Security & SkillSpector Gate | `03-database-tenancy.md` | `63950` | **`802`** | **`98.7%`** | `352 ms` |
| **Stage 4** | 3-Hop Async Bug Trace (AST Slicer + Negative Memory) | `08-deep-debugger.md` | `64650` | **`877`** | **`98.6%`** | `300 ms` |
| **TOTAL** | **All 4 Enterprise Hostile Stages** | **Dynamic 8-Dept Router** | **`253500`** | **`3353`** | **`98.7%`** | **Verified `Exit Code 0`** |
