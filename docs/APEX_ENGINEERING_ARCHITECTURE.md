# Apex Engineering (v3.2) — Enterprise Architecture & Codebase Guide

> **Frontier Software Engineering & Enterprise SaaS Microkernel for AI Coding Agents**  
> Enables agile, cost-effective models (such as Gemini 3.8 Flash, GPT-4o-mini, and open-weights models) to perform with the architectural discipline, multi-tenant security, and verification rigor of frontier models like Claude Opus.

---

## 1. Executive Summary & Core Paradigm

Traditional AI coding assistants rely on **raw model intuition**: when prompted with *"Build a multi-tenant SaaS application,"* an unconstrained model writes unstructured code in one shot, hallucinates that tests passed, omits PostgreSQL Row-Level Security (RLS), leaves payment webhooks vulnerable to replay attacks, and enters infinite retry loops when encountering compiler errors.

**Apex Engineering** replaces model intuition with an **externalized deterministic microkernel**:
1. **Compound Agent System:** The intelligence resides in the *system architecture*—strict negative constraints, mechanical 20-line production skeletons, hard verification gates, and AST call-graph tracing.
2. **Zero-Token Cold Vault:** 1,500+ local skills are indexed and quarantined into cold storage (`~/.agents/skills-vault/`), eliminating IDE startup token bloat. Only the 2–3 skills that match active project manifests (`package.json`, `pyproject.toml`) are injected into working memory on demand.
3. **Turn-by-Turn Context Budget:** Startup context is strictly capped at **<450 tokens**, ensuring fast inferences and preventing context drift over long multi-turn sessions.
4. **Hard Verification Gates:** Prose claims of success are forbidden. A task is complete only when `apex_ctl.py verify` exits with code `0`, enforcing `git diff` scope boundaries and deterministic unit/typecheck tests.

---

## 2. Complete Codebase Structure

Below is the canonical directory structure of the `apex-engineering` repository:

```text
apex-engineering/                           # GitHub Repo Root
├── README.md                               # Badges, Architecture Diagram, Quickstart & Benchmark Table
├── LICENSE                                 # MIT License
├── .gitignore                              # Ignores .apex/l1-register.json, .apex/l3-archive.db, __pycache__
├── package.json                            # Enables `npx apex-engineering` CLI execution
├── SKILL.md                                # Root Skill Entrypoint (for direct `npx skills add`)
├── company-dag.json                        # 8-Department State Machine & Supervisor Gates
├── cartridges/                             # Single Canonical Set of 8 Department + Custom Cartridges (<250 tokens)
│   ├── 01-product-discovery.md             # Stage 01: PRD, scope, non-goals & supervisor gate
│   ├── 02-principal-architect.md           # Stage 02: C4 architecture, ADRs & API contracts
│   ├── 03-database-tenancy.md              # Stage 03: PostgreSQL RLS & scoped tenant transactions
│   ├── 04-backend-resilience.md            # Stage 04: Zod validation, timeouts & Redis idempotency
│   ├── 05-frontend-craft.md                # Stage 05: React 19 RSC, optimistic forms & WCAG
│   ├── 06-security-zero-trust.md           # Stage 06: BOLA guards, timing-safe HMAC & zero SQLi
│   ├── 07-devops-cloud-cicd.md             # Stage 07: Rootless Dockerfile, healthz & graceful drain
│   ├── 08-deep-debugger.md                 # Stage 08: Multi-hop backward AST root-cause loop
│   └── custom/                             # On-demand distilled external/custom skills
│       ├── graphql-architect.md            # Ingested from vault (79 words)
│       ├── iso-timestamp-strict.md         # Synthesized strict ISO timestamp standard
│       └── rfc7807-problem-details.md      # Synthesized custom error standard (51 words)
├── scripts/                                # Single Canonical Set of Controllers & Compilers
│   ├── apex_ctl.py                         # Microkernel CLI (begin, verify, scope guard)
│   ├── index_local_skills.py               # 1,507 skill scanner, classifier & vault isolator
│   └── ingest_skill.py                     # SkillSpector 64-pattern SAST & compiler pipeline
├── benchmarks/                             # Phase 5 Hostile Benchmark Suite (12/12 PASS)
│   ├── fixtures_broken.py                  # 4 enterprise stages (RLS, Idempotency, 5-CWE, Hop-Trace)
│   └── test_benchmark_suite.py             # 12 unit & AST security verification tests
├── docs/                                   # Audit Trails & Persistent Ledgers
│   ├── APEX_ENGINEERING_ARCHITECTURE.md    # Complete architectural blueprint (this file)
│   ├── ISSUE_TRACKER.md                    # Root-cause debugging ledger
│   └── WORKFORCE_LEDGER.md                 # Append-only chronological audit trail of all gates
└── .apex/                                  # Runtime FSA State, Memory & Vault Registry
    ├── artifacts/                          # Handoff baton artifacts between departments
    │   ├── 01-prd.md                       # Product requirements & scope contract
    │   ├── 02-contracts.md                 # API endpoints, C4 architecture & schemas
    │   ├── 06-sec-audit.json               # Zero-trust SAST & OWASP audit report
    │   └── trace-ledger.md                 # 3-hop backward AST root-cause trace
    ├── l1-register.json                    # L1 working memory: current phase, goal, blacklist
    ├── l3-archive.db                       # L3 SQLite full-text memory database
    └── skill-registry.json                 # Curated catalog of active stack skills & triggers
```

---

## 3. The 5-Layer Architectural Microkernel

```
┌────────────────────────────────────────────────────────────────────────┐
│                        USER PROMPT / TASK                              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: BOOT SEQUENCE & L1 WORKING MEMORY                             │
│ (skills/apex-engineering/scripts/apex_ctl.py begin)                    │
│ • Reads active phase & task goal from .apex/l1-register.json           │
│ • Detects dependencies in package.json / pyproject.toml                │
│ • Injects matched stack rules + active department rules (<450 tokens)  │
│ • Displays active blacklisted failure warnings                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: 8 IT DEPARTMENT CARTRIDGES                                    │
│ (skills/apex-engineering/cartridges/01 to 08)                          │
│ • Negative Constraints: Apex Surgical Diffs (Strict YAGNI)            │
│ • Canonical Code Skeletons: copy-paste enterprise production patterns  │
│ • Baton Artifacts: writes formal specs to .apex/artifacts/             │
│ • Next Stage Pointer: hardcoded DAG transition                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: ON-DEMAND SKILL ABSORPTION                                    │
│ (skills/apex-engineering/scripts/ingest_skill.py)                      │
│ • Gate 1: SkillSpector 64-pattern SAST security scanner                │
│ • Gate 2: Semantic Distiller strips narrative -> <250-token rules      │
│ • Gate 3: Auto-slots domain tags into .apex/skill-registry.json        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: DETERMINISTIC VERIFICATION GATE                               │
│ (skills/apex-engineering/scripts/apex_ctl.py verify)                   │
│ • Scope Guard: git diff checked against allowed_write_scope            │
│ • Test Runner: runs package.json, pyproject.toml, or benchmark suites  │
│ • Binary Gate: Exit Code 0 required (Self-attestation forbidden)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 5: PERSISTENT MEMORY FEEDBACK LOOP                              │
│ • PASS (Code 0): Clears blacklists, records to docs/WORKFORCE_LEDGER.md│
│ • FAIL (Non-Zero): Appends command failure to L1 blacklisted_attempts  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Component Specifications

### 4.1. L1 & L3 Memory Subsystem (`.apex/`)
* **L1 FSA State Register (`.apex/l1-register.json`):**
  Maintains ephemeral, turn-by-turn state:
  * `current_phase`: Current department ID in `company-dag.json` (e.g., `04-backend-resilience`).
  * `active_goal`: High-level user objective.
  * `allowed_write_scope`: Glob patterns of files the agent is authorized to touch (e.g., `["src/api/**", "tests/**"]`).
  * `blacklisted_attempts`: Failed command signatures or invalid approaches. If the agent fails a test, it is strictly forbidden from retrying the exact same fix.
* **L3 SQLite Full-Text Search Archive (`.apex/l3-archive.db`):**
  Persistent SQLite database containing `memory_fts` for storing long-term architectural decisions, tenant configurations, and debug hops across turns.

---

### 4.2. The 8 IT Department Cartridges (`cartridges/`)

Each cartridge enforces a **4-Block Canonical Structure** designed specifically for high-precision generation:

| Department ID | Cartridge File | Fused Core Winners | Key Enterprise Invariants Enforced |
| :--- | :--- | :--- | :--- |
| **01** | `01-product-discovery.md` | `idea-os`, `product-manager-toolkit`, `clarity-gate` | No code allowed; PRD baton under 350 tokens; 3-question Supervisor gate on ambiguity. |
| **02** | `02-principal-architect.md` | `c4-architecture`, `adr`, `openapi-spec-generation` | Apex Surgical Diffs (Strict YAGNI) (no multi-layer Hexagonal bloat for CRUD); OpenAPI schemas required. |
| **03** | `03-database-tenancy.md` | `saas-multi-tenant`, `postgres-best-practices` | Mandatory `tenant_id` index; PostgreSQL RLS policies; scoped tenant transaction wrappers. |
| **04** | `04-backend-resilience.md` | `backend-architect`, `zod-validation-expert`, `tdd` | Zod schema validation on controllers; atomic Redis idempotency lock (`SET NX EX 86400`). |
| **05** | `05-frontend-craft.md` | `vercel-react-best-practices`, `wcag-audit-patterns` | RSC on layouts (no unnecessary `"use client"`); no `useEffect` fetching; WCAG aria labels. |
| **06** | `06-security-zero-trust.md` | `security-audit`, `auth-patterns`, `idor-testing` | BOLA session checks; timing-safe HMAC (`crypto.timingSafeEqual`); zero SQL injection. |
| **07** | `07-devops-cloud-cicd.md` | `docker-expert`, `distributed-tracing`, `otel` | Rootless Docker container execution; pinned image tags; `/readyz` probes & `SIGTERM` drain. |
| **08** | `08-deep-debugger.md` | `systematic-debugging`, `error-debugging-trace` | 3-step scientific debugging loop; backward AST caller hop tracing; zero band-aid null checks. |

---

### 4.3. The SkillSpector Compiler Pipeline (`scripts/ingest_skill.py`)

A security-first pipeline to absorb skills from GitHub, local paths, or vaults:

1. **Gate 1 — SkillSpector Static Security Scanner (64 Patterns):**
   * **Prompt Injection (12 patterns):** Catches `ignore previous instructions`, `bypass safety gates`, etc.
   * **Pipe-to-Shell RCE (12 patterns):** Catches `curl ... | bash`, `wget ... | sh`, `Invoke-Expression`, encoded PowerShell.
   * **Secret Exfiltration (12 patterns):** Catches `cat .env | curl`, webhook exfiltration, reading `~/.ssh/id_rsa`.
   * **Unsafe Primitives (10 patterns):** Catches `subprocess(shell=True)`, `eval(compile())`, `os.system()`.
   * **Destructive Ops (10 patterns):** Catches `rm -rf /`, `DROP DATABASE`, unverified force pushes.
   * **Steganography (8 patterns):** Catches zero-width unicode spaces (`\u200b`), bidi overrides, hidden comments.
   * *Threshold:* Any skill with `Risk Score >= 25` is immediately **BLOCKED**.
2. **Gate 2 — Semantic Distiller & Conflict Stripper:**
   * Removes conversational prose, badges, and conflicting instructions (e.g., *"always rewrite the entire file"*).
   * Distills imperative rules and a 15-line code block into `<250-token` cartridges saved in `skills/apex-engineering/cartridges/custom/<name>.md`.
3. **Gate 3 — Auto-Slotting:**
   * Automatically maps the skill to stack tags (`nextjs`, `react`, `prisma`, `stripe`, `fastapi`, `typescript`).
   * Registers the skill in `.apex/skill-registry.json` and logs to `docs/WORKFORCE_LEDGER.md`.

---

### 4.4. The Controller & Verification Gate (`skills/apex-engineering/scripts/apex_ctl.py`)

* **`begin --task "<goal>"`:**
  1. Updates active goal in `.apex/l1-register.json`.
  2. Scans project manifest (`package.json`, `pyproject.toml`) for dependencies.
  3. Loads active department cartridge and matching stack add-ons from `.apex/skill-registry.json`.
  4. Warns on active `blacklisted_attempts`.
  5. Outputs compact working memory in **<450 tokens**.
* **`verify`:**
  1. **Scope Guard:** Compares `git diff` against `allowed_write_scope` using glob matching.
  2. **Test Runner Execution:** Runs `npm test`, `pytest`, or Python benchmark suites.
  3. **Feedback:** If exit code is `0`, records `PASS` in `docs/WORKFORCE_LEDGER.md` and clears blacklists. If non-zero, appends failure to `blacklisted_attempts` and exits with code `1`.

---

## 5. End-to-End Operational Lifecycle Walkthrough

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. SKILL ABSORPTION (One-Time Ingestion)                               │
│    python skills/apex-engineering/scripts/ingest_skill.py --from-url...│
│    -> Scanned across 64 SAST patterns (Blocks malicious payloads)      │
│    -> Fluff stripped -> <250-token cartridge in cartridges/custom/     │
│    -> Metadata indexed in .apex/skill-registry.json (0 startup tokens) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. BOOT & JUST-IN-TIME INJECTION (Every Turn)                          │
│    python skills/apex-engineering/scripts/apex_ctl.py begin --task ... │
│    -> Scans dependencies -> detects "stripe"                           │
│    -> Injects matching rules + 04-backend-resilience.md (<450 tokens)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. ENTERPRISE CODE GENERATION                                          │
│    Model generates code adhering strictly to injected rules:           │
│    - Zod boundary validation                                           │
│    - Atomic Redis idempotency lock (SET NX EX 86400)                   │
│    - crypto.timingSafeEqual for webhook signatures                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. DETERMINISTIC VERIFICATION & LEDGER ADVANCE                         │
│    python scripts/apex_ctl.py verify                                   │
│    - Scope Guard verifies no out-of-scope files were edited            │
│    - Unit & typecheck tests execute                                    │
│    - On PASS (Code 0): Logged to docs/WORKFORCE_LEDGER.md              │
│    - On FAIL: Error logged to blacklisted_attempts; loop blocked       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Empirical Validation (Phase 5 Benchmark Suite)

The system is empirically proven via [`benchmarks/test_benchmark_suite.py`](../benchmarks/test_benchmark_suite.py):

| Test Stage | Flaw Tested | Enforcement Mechanism | Result |
| :--- | :--- | :--- | :--- |
| **Stage 1: DB Tenancy** | Missing RLS query scoping | `TenantInvoiceRepo` validates positive amount and scopes SQL with `WHERE tenant_id = ?` | **PASS** |
| **Stage 2: Resilience** | Double-charge on retry / missing validation | `process_stripe_webhook` validates inputs, checks `idemp:{id}` in Redis, releases on transient failure | **PASS** |
| **Stage 3: Security** | CWE-798, CWE-208, CWE-639, CWE-89, CWE-78 | Parameterized SQL, BOLA check (`session_id == requested_id`), `hmac.compare_digest`, `shell=False` | **PASS** |
| **Stage 4: Debugger** | Multi-hop payload key mismatch & mutable list leak | 3-hop trace table in `.apex/artifacts/trace-ledger.md`, default `batch=None`, root cause in `docs/ISSUE_TRACKER.md` | **PASS** |

---

## 7. Summary

**Apex Engineering (v3.3)** bridges the frontier gap not through parameter count, but through **deterministic architectural governance**:
* **High Speed & Low Cost:** Ultra-compact prompt injection (<450 tokens) keeps turns fast and cost-effective.
* **Enterprise Invariants:** PostgreSQL RLS, idempotency locks, timing-safe auth, and rootless containers are enforced on every run.
* **Deterministic Completion:** Work is finished only when automated compilers and test suites pass.

