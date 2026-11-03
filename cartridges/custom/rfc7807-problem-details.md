# Custom Cartridge: rfc7807-problem-details
**Domain Tag:** `typescript` | **Department:** `04-backend-resilience` | **SkillSpector Risk:** `0/100 (SAFE)`

## 1. Mandatory Mechanical Rules
- NEVER return unstructured plain-text errors or unvalidated payloads.
- ALWAYS verify compliance via deterministic unit tests before completion.

## 3. Verification Gate
- Run `python scripts/apex_ctl.py verify` (`Exit Code 0`).
