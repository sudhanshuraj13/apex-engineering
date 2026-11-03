---
name: apex-engineering
description: "Frontier SWE & Enterprise SaaS Microkernel. Powers any model (including Gemini 3.8 Flash) with L1/L3 Memory, Gravitas 4-Tier Effort Routing, Claude-Style Supervisor Gating, and Deterministic Verification."
tags: [enterprise, saas, memory, gravitas, verification]
---

# Apex Engineering Microkernel

## BOOT SEQUENCE (Run on Every Turn)
Before writing any code or plan, execute:
```bash
python scripts/apex_ctl.py begin --task "$USER_PROMPT" [--symbol "$SYMBOL_NAME"]
```
This automatically loads your L1 FSA state, active blacklisted failures, required department rules, detected stack tags, skill-registry injections (<450 tokens), and lightweight zero-dependency AST symbol slices (<120 tokens).

---

## TIER-BASED EXECUTION (Gravitas 4-Tier Effort Engine)
Determine the task tier from your initial reconnaissance:
1. **`tier-1: direct`** (Trivial bugfix, CSS adjustment, variable rename): Skip all questions and department DAG. Edit in place, run `apex_ctl.py verify`, and finish. Scope guard still runs.
2. **`tier-2: compact`** (Standard feature, endpoint addition): Load single matching domain cartridge. Execute, verify, and log to `docs/WORKFORCE_LEDGER.md`.
3. **`tier-3: deep`** (New product, multi-tenant SaaS, high blast-radius): Run **Supervisor Clarifying Gate** before writing code.
4. **`tier-4: replan`** (Test failure or recursion): Unlock `08-deep-debugger.md` and backward AST hop tracing.

---

## CLAUDE-STYLE SUPERVISOR GATING
If Tier 3 (`deep`) is active OR if the task touches **DBMS/Migrations, Stripe/Billing, Auth/JWT, or Cloud Infra**, the Supervisor must output a **Maximum 3-Question Multiple-Choice Card with Smart Defaults** before proceeding. 

> **Supervisor Pre-Flight Check:**
> 1. **Auth / Tenancy:** Shared DB with RLS vs. Isolated Schemas? *(Default: RLS)*
> 2. **Billing / Webhooks:** Idempotent Stripe Webhooks + Redis Lock? *(Default: Yes)*
> 3. **Verification:** Vitest / Pytest suite required? *(Default: Yes)*

---

## VERIFICATION & COMPLETION
Never declare success in prose. After making edits, run:
```bash
python scripts/apex_ctl.py verify
```
* If `STATUS: PASS (Exit Code 0)`: The script automatically records the change in `docs/WORKFORCE_LEDGER.md`, clears L1 blacklists, and advances the workflow.
* If `STATUS: FAIL`: The error is automatically written to L1 `blacklisted_attempts`. You are forbidden from retrying the exact same fix.

