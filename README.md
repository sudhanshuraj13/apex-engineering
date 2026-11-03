# APEX-ENGINEERING
### The Frontier SWE & 8-Department Enterprise SaaS Microkernel for AI Coding Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Benchmarks: 12/12 PASS](https://img.shields.io/badge/Benchmarks-12%2F12%20PASS-success.svg)](benchmarks/)
[![Token Footprint: <450](https://img.shields.io/badge/Token%20Footprint-%3C450%20tokens-orange.svg)](#boot-sequence)
[![Platforms: Antigravity | Claude | OpenCode | Codex | Cursor | BharatCode](https://img.shields.io/badge/Platforms-All%20CLI%20%26%20IDEs-purple.svg)](#-installation-by-platform-cli--ide)

> **100% Model & Editor Agnostic:** Works natively inside **Antigravity, Claude Code, Cursor, OpenCode, and Codex** with any model you already use (**Gemini 3.8 Flash, GPT-4o-mini, Claude Haiku, Llama 3.3, DeepSeek, or Qwen**).  
> Combines L1/L3 FSA memory, Python AST call-graph slicing, Claude-style Supervisor pre-flight gates, 64-rule SkillSpector SAST security, and deterministic Exit-Code-0 verification.

---

## ⚡ Quickstart via NPM (Zero Configuration)

If you have Node 18+ and Python 3.10+, you can inspect and evaluate `Apex-Engineering` immediately using standard `npm` scripts:

```bash
npm run status       # 📊 View live 8-Department SDLC pipeline & L1 memory
npm run benchmark    # 🧪 Run 4-Stage empirical token reduction benchmark
npm test             # 🛡️ Run all 12 hostile enterprise unit & SAST tests
npm run verify       # 🔒 Run deterministic scope guard + verification gate (Exit Code 0)
npm run shell        # 💻 Launch the interactive multi-editor agentic CLI shell
```

---

## 📥 Installation by Platform (CLI & IDE)

You can install `apex-engineering` globally via the `skills` CLI, mount it into any IDE/CLI agent in one command, or run its standalone interactive terminal harness.

### Option 0: Universal One-Command Mount (All Platforms at Once)
Clone the repository and run the universal installer inside your target project to wire **Antigravity, OpenCode, Claude Code, Codex, and Cursor** simultaneously:
```bash
git clone https://github.com/sudhanshuraj13/apex-engineering.git
python apex-engineering/scripts/bharat_harness.py --install all
```

---

### 1. Google Antigravity (IDE & CLI)
**Via `npx skills` CLI:**
```bash
npx skills add sudhanshuraj13/apex-engineering -a antigravity
```
**Via Apex CLI Installer (Project Workspace or Global Vault):**
```bash
# Mount into active project (.agents/skills/apex-engineering/SKILL.md)
python scripts/bharat_harness.py --install antigravity

# Or install globally for all Antigravity sessions
cp -r . ~/.gemini/config/skills/apex-engineering
```

---

### 2. Claude Code (Anthropic CLI & VS Code / JetBrains IDE Extension)
**Via `npx skills` CLI:**
```bash
npx skills add sudhanshuraj13/apex-engineering -a claude-code
```
**Via Apex CLI Installer (Auto-configures `CLAUDE.md` & `.agents/skills/`):**
```bash
python scripts/bharat_harness.py --install claude
```
* **In Claude Code CLI:** Run `claude` in your terminal; Claude automatically loads the `CLAUDE.md` microkernel pointer and executes `apex_ctl.py begin` before mutating files.
* **In Claude Code IDE Extension:** Open the Claude panel in VS Code or JetBrains—the Supervisor Pre-Flight Gate and `<450-token` department routing activate automatically on every prompt.

---

### 3. OpenCode (Terminal TUI & CLI Agent)
**Via `npx skills` CLI:**
```bash
npx skills add sudhanshuraj13/apex-engineering -a opencode
```
**Via Apex CLI Installer:**
```bash
python scripts/bharat_harness.py --install opencode
```
* Places the canonical `SKILL.md` router inside `.agents/skills/apex-engineering/SKILL.md` so OpenCode's TUI agent enforces L1 negative memory and Exit-Code-0 verification.

---

### 4. OpenAI Codex (Codex CLI & Editor Integration)
**Via `npx skills` CLI:**
```bash
npx skills add sudhanshuraj13/apex-engineering -a codex
```
**Via Apex CLI Installer (Auto-configures `AGENTS.md`):**
```bash
python scripts/bharat_harness.py --install codex
```
* Injects the deterministic boot and verification runbook directly into your project's `AGENTS.md` file read by `codex` CLI and IDE extensions.

---

### 5. Cursor & Windsurf (AI IDEs)
**Via `npx skills` CLI:**
```bash
npx skills add sudhanshuraj13/apex-engineering -a cursor
```
**Via Apex CLI Installer (Generates `.cursor/rules/apex-engineering.mdc`):**
```bash
python scripts/bharat_harness.py --install cursor
```
* Creates an `alwaysApply: true` rule in `.cursor/rules/apex-engineering.mdc` so Cursor Composer / Agent mode obeys the 8-department DAG and verification gates.

---

## 💻 Standalone CLI Control Plane (`bharat_harness.py` / `npx apex-engineering`)

Developers and non-developers can manage the entire 8-department software company directly from the terminal—without needing a paid IDE subscription.

### 1. Launch Interactive REPL Shell (Like `claude` or `opencode`)
```bash
python scripts/bharat_harness.py --shell
# Or via NPX:
npx apex-engineering --shell
```
Inside the interactive `apex>` shell, you have full terminal control:
* Type any feature, bug, or product idea to auto-route to the matching IT department.
* `/status` — Render the live **8-Department SDLC Pipeline**, L1 Negative Memory Blacklist, and Artifact Batons.
* `/build <idea>` — Run all **7 SDLC departments end-to-end** (Idea $\rightarrow$ PRD $\rightarrow$ Architecture $\rightarrow$ Postgres RLS $\rightarrow$ Backend API $\rightarrow$ React 19 UI $\rightarrow$ OWASP Audit $\rightarrow$ Docker/CI-CD Deploy).
* `/stage <01-08>` — Lock or switch the active IT department manually.
* `/absorb <url-or-path>` — Scan an external GitHub/community skill with the **64-pattern SkillSpector SAST scanner** and compress it into a `<250-token` cartridge.
* `/ledger` — Inspect `docs/WORKFORCE_LEDGER.md` and `docs/ISSUE_TRACKER.md`.
* `/verify` — Run the hard `git diff` scope guard and unit test suite (`Exit Code 0`).

### 2. Direct One-Line CLI Commands
```bash
# View the live 8-Department SDLC Pipeline & L1 Working Memory Dashboard
python scripts/bharat_harness.py --status

# Build an entire enterprise SaaS product across all 7 SDLC stages
python scripts/bharat_harness.py --build-product "Multi-Tenant Healthcare Portal" --dry-run --yes

# Execute a targeted engineering task with AST Call-Graph Slicing
python scripts/bharat_harness.py --task "Fix webhook replay race condition" --symbol "cmd_verify" --yes

# Auto-detects provider from .env (OpenAI, Gemini, Groq, OpenRouter, Ollama, BharatCode, or IDE-Native)
python scripts/bharat_harness.py --task "Design Postgres RLS schema for invoices"

# Or explicitly select provider & model
python scripts/bharat_harness.py --provider gemini --task "Design Postgres RLS schema"
python scripts/bharat_harness.py --provider bharatcode --model qwen-3.8-27b --task "Stripe webhook idempotency"
```

---

## 🇮🇳 BharatCode & Universal Provider Engine

`Apex-Engineering` includes a native universal engine (`scripts/bharat_harness.py`) that auto-detects your provider from `.env` across **BharatCode**, **Google Gemini**, **OpenAI**, **Groq**, **OpenRouter**, **Ollama**, or **IDE-Native Local Mode**:
1. **Queue-Saver Context Slicing ($98.6\%$ Reduction):** Slices repo context + AST call graphs + 1 department cartridge into **$<450$ tokens** so student/open-weight models execute in the fastest queue lane.
2. **Client-Side Stateless Memory (`"store": false`):** Complies with stateless inference requirements (BharatCode, Groq, Gemini) by maintaining persistent state locally on disk via `.apex/l1-register.json` (180-token FSA register) and `.apex/l3-archive.db` (SQLite FTS5 BM25).
3. **Zero 6-Try Debugging Loops:** Failed test runs automatically write to `blacklisted_attempts` in L1 memory so models never repeat a broken fix.

---

## 🏛️ Architecture: The 5-Layer Microkernel

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        USER PROMPT / TASK                              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: BOOT SEQUENCE & L1 WORKING MEMORY (scripts/apex_ctl.py begin) │
│ • Reads active phase & task goal from .apex/l1-register.json           │
│ • Slices target symbol & callers via Python AST + git grep (--symbol)  │
│ • Injects matched stack rules + active department rules (<450 tokens)  │
│ • Displays active blacklisted failure warnings                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: 8 IT DEPARTMENT CARTRIDGES (cartridges/01 to 08)             │
│ • Supervisor Pre-Flight Gate: 3 multiple-choice questions on high risk │
│ • Negative Constraints: forbidden anti-patterns (Apex Surgical Diffs)  │
│ • Canonical Code Skeletons: copy-paste enterprise production patterns  │
│ • Baton Artifacts: writes formal specs to .apex/artifacts/             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: ON-DEMAND SKILL ABSORPTION (scripts/ingest_skill.py)         │
│ • Gate 1: SkillSpector 64-pattern SAST security scanner                │
│ • Gate 2: Semantic Distiller strips narrative -> <250-token rules      │
│ • Gate 3: Auto-slots domain tags into .apex/skill-registry.json        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: DETERMINISTIC VERIFICATION GATE (scripts/apex_ctl.py verify)  │
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

## 🗂️ The 8 IT Department Cartridges

Every cartridge follows the **4-Block Canonical Format** ($<250$ tokens each) with negative constraints, copy-paste production skeletons, and deterministic handoff batons:

| Cartridge | Department Name | Key Fused Winners | Baton Handoff Artifact |
| :--- | :--- | :--- | :--- |
| **`01`** | **Product Strategy & PRD** | `idea-os`, `clarity-gate` | `.apex/artifacts/01-prd.md` |
| **`02`** | **System Architecture & C4** | `c4-architecture`, `openapi-spec` | `.apex/artifacts/02-contracts.md` |
| **`03`** | **Database & RLS Tenancy** | `saas-multi-tenant`, `postgres-best` | `.apex/artifacts/03-schema.sql` |
| **`04`** | **Backend APIs & Resilience** | `zod-validation`, `error-handling` | `.apex/artifacts/04-backend.diff` |
| **`05`** | **Frontend & UI Craft** | `vercel-react-best-practices`, `wcag` | `.apex/artifacts/05-frontend.diff` |
| **`06`** | **Security & Zero-Trust** | `security-audit`, `idor-testing` | `.apex/artifacts/06-sec-audit.json` |
| **`07`** | **DevOps, Docker & OTel** | `docker-expert`, `distributed-trace` | `.apex/artifacts/07-deploy.yaml` |
| **`08`** | **Deep Debugger & AST Trace** | `systematic-debugging`, `error-trace` | `.apex/artifacts/trace-ledger.md` |

---

## 🛡️ SkillSpector SAST Compiler (`scripts/ingest_skill.py`)

Ingest any external skill from GitHub, a local file, or synthesized plain English. Scans across **64 SAST threat signatures in 6 categories**:
1. Prompt Injection & System Prompt Overrides
2. Pipe-to-Shell & Remote Code Execution (`curl ... | bash`)
3. Credential Harvesting & `.env` Exfiltration
4. Dangerous Execution Primitives (`eval()`, `exec()`, `shell=True`)
5. Destructive System Commands (`rm -rf /`, `DROP DATABASE`)
6. Unicode Steganography & Homoglyphs

```bash
# Ingest and distill any external skill safely
python scripts/ingest_skill.py --from-url https://raw.githubusercontent.com/.../SKILL.md --name "redis-cache-pro"

# Synthesize a custom skill on the fly
python scripts/ingest_skill.py --synthesize "Enforce Strict RFC 3339 ISO Timestamps on all API responses" --name "iso-timestamp-strict" --domain "typescript"
```

---

## 🧪 Empirical Hostile Benchmark Suite (12/12 PASS)

### 🔬 Empirical Case Study — Why We Benchmark on a 27B Open-Weight Model (`qwen-3.8-27b` via BharatCode):
> **Anyone can pass enterprise tests using a \$20/month heavyweight model.**  
> To prove that `Apex-Engineering` puts the intelligence in the system harness rather than the model weights, we stress-tested our 4-stage hostile enterprise benchmark on a 27-billion parameter open-weight model (`qwen-3.8-27b`) over a stateless API (`store: false`).  
> **Result:** 98.6% token reduction and 12/12 security & concurrency tests passed (`Exit Code 0`). If Apex makes a 27B model perform like a Principal Engineer, it will supercharge whatever model you run in your IDE.

Run the 4-stage A/B benchmark suite and unit verification harness:

```bash
# Run 4-stage empirical token reduction benchmark
npm run benchmark
# Or: python scripts/bharat_harness.py --benchmark --dry-run

# Run hard verification gate (git diff scope + unit tests)
npm run verify
# Or: python scripts/apex_ctl.py verify
```

| Benchmark Stage | Hostile Challenge Tested | Raw Repo Tokens | Apex Sliced Tokens | Token Saved | Verification Result |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Stage 1: DB Tenancy** | Cross-tenant invoice leak via `SELECT *` | `58,728` | **`797`** | **`98.6%`** | **PASS (Exit 0)** |
| **Stage 2: Resilience** | Double-charge race condition on webhook retry | `60,528` | **`877`** | **`98.6%`** | **PASS (Exit 0)** |
| **Stage 3: Security** | 5 OWASP CVEs (Hardcoded keys, timing HMAC, BOLA, SQLi, RCE) | `61,128` | **`802`** | **`98.7%`** | **PASS (Exit 0)** |
| **Stage 4: Debugger** | Hidden data corruption at Hop 1 of 3-hop pipeline | `61,828` | **`877`** | **`98.6%`** | **PASS (Exit 0)** |
| **TOTAL** | **All 4 Hostile Enterprise Challenges** | **`242,212`** | **`3,353`** | **`98.6%`** | **PASS (12/12 Tests, Exit Code 0)** |

---

## 📁 Repository Structure

```text
apex-engineering/                           # GitHub Repo Root
├── BharatCode.txt                          # BharatCode Build League verification file
├── README.md                               # Platform installation & CLI documentation
├── LICENSE                                 # MIT License
├── .gitignore                              # Ignores runtime memory & caches
├── package.json                            # Enables `npx apex-engineering` CLI execution
├── bin/
│   └── apex.js                             # Cross-platform Node wrapper for NPX CLI
├── SKILL.md                                # Root Skill Entrypoint (for `npx skills add`)
├── company-dag.json                        # 8-Department State Machine & Supervisor Gates
├── cartridges/                             # Canonical Set of 8 Department Cartridges (<250 tokens)
│   ├── 01-product-discovery.md ... 08-deep-debugger.md
│   └── custom/                             # On-demand distilled custom cartridges
├── scripts/                                # Microkernel Automation & CLI Harness
│   ├── apex_ctl.py                         # Controller (boot turn, AST slicer, verify gate)
│   ├── bharat_harness.py                   # Interactive CLI, Multi-IDE Mounter & BharatCode Engine
│   ├── index_local_skills.py               # Vault isolator & classifier
│   └── ingest_skill.py                     # 64-pattern SkillSpector SAST + Distiller
├── benchmarks/                             # Phase 5 Hostile Benchmark Suite (12/12 PASS)
│   ├── fixtures_broken.py
│   └── test_benchmark_suite.py
└── docs/                                   # Audit Trails & Deep Dives
    ├── APEX_ENGINEERING_ARCHITECTURE.md    # Complete architectural blueprint
    ├── BENCHMARK_REPORT.md                 # Auto-generated A/B token & test report
    ├── ISSUE_TRACKER.md                    # Root-cause debugging ledger
    └── WORKFORCE_LEDGER.md                 # Append-only chronological audit trail
```

---

## 📄 License
MIT © 2026 Sudhanshu Raj