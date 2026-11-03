# 01 — Product Strategy & PRD Cartridge
**Fused Winners:** `idea-os`, `product-manager-toolkit`, `ask-questions-if-underspecified`, `clarity-gate`

## 1. Negative Constraints (FORBIDDEN)
- NEVER write application code during Stage 01.
- NEVER invent vague personas or marketing fluff; keep total PRD under 350 tokens.
- NEVER proceed if Core 3 Specs (Data Model, Tenant/Auth Boundary, Billing/Edge Cases) are ambiguous—trigger the 3-Question Supervisor Gate first.

## 2. Canonical PRD Baton Skeleton (`.apex/artifacts/01-prd.md`)
```markdown
# PRD Baton: [Product/Feature Name]
## 1. Problem & Core Value (Max 3 lines)
- Target User & Pain Point:
- Primary Outcome Metric:

## 2. Strict Scope & Non-Goals
- IN SCOPE (MVP): [Max 4 bullet points]
- OUT OF SCOPE (YAGNI): [Explicitly excluded features]

## 3. Core User Stories & Acceptance Criteria
- [US-01]: As a [tenant_role], when I [action], system [deterministic result] (Verify: [test check]).

## 4. Security & Tenancy Invariants
- Isolation: [Shared DB + RLS | Separate Schema]
- Critical Blast-Radius Systems: [Auth / Billing / External APIs]
```

## 3. Exit Gate & Handoff
- **Artifact Written:** `.apex/artifacts/01-prd.md`
- **Gate Check:** Verify `.apex/artifacts/01-prd.md` exists and is approved by user.
- **Next Recommended Skill:** `02-principal-architect`
