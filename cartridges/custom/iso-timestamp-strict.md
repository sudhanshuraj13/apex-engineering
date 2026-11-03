# Custom Cartridge: iso-timestamp-strict
**Domain Tag:** `typescript` | **Department:** `04-backend-resilience` | **SkillSpector Risk:** `0/100 (SAFE)`

## 1. Mandatory Mechanical Rules
- MUST enforce: Enforce Strict RFC 3339 ISO Timestamps on all API responses
- NEVER return unstructured plain-text errors or unvalidated payloads.
- ALWAYS verify compliance via deterministic unit tests before completion.

## 3. Verification Gate
- Run `python scripts/apex_ctl.py verify` (`Exit Code 0`).
