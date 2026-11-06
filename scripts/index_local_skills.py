#!/usr/bin/env python3
"""
APEX-ENGINEERING v3.2 — Phase 2: 1,507 Local Skills Indexer & Cold-Vault Isolator.
Matches the exact STACK_SIGNATURES schema used by scripts/apex_ctl.py.
Zero external dependencies.
"""

from pathlib import Path
import os
import re
import sys
import json
import shutil
import argparse
from datetime import datetime

# 1. SKILL_ROOT: Where this skill package lives (Read-only assets & skill registry)
SKILL_ROOT = Path(__file__).resolve().parent.parent
DAG_PATH = SKILL_ROOT / "company-dag.json"
CARTRIDGES_DIR = SKILL_ROOT / "cartridges"
CUSTOM_CARTRIDGES_DIR = CARTRIDGES_DIR / "custom"
SKILL_REGISTRY_PATH = SKILL_ROOT / ".apex" / "skill-registry.json"

# 2. PROJECT_ROOT: The user's active codebase where the command is executed
PROJECT_ROOT = Path(os.environ.get("APEX_PROJECT_ROOT", Path.cwd())).resolve()
APEX_STATE_DIR = PROJECT_ROOT / ".apex"
ARTIFACTS_DIR = APEX_STATE_DIR / "artifacts"
L1_PATH = APEX_STATE_DIR / "l1-register.json"
L3_DB_PATH = APEX_STATE_DIR / "l3-archive.db"
DOCS_DIR = PROJECT_ROOT / "docs"
LEDGER_PATH = DOCS_DIR / "WORKFORCE_LEDGER.md"
ISSUES_PATH = DOCS_DIR / "ISSUE_TRACKER.md"

DEFAULT_SKILLS_DIR = Path("C:/Users/Sudhanshu raj/.agents/skills")
DEFAULT_VAULT_DIR = Path("C:/Users/Sudhanshu raj/.agents/skills-vault")
DEFAULT_PROJECT_DIR = PROJECT_ROOT

PROTECTED_ACTIVE_SKILLS = {
    "apex-engineering",
    "apex_engineering_skill",
    "apex-company-os"
}

# Pass 1: Quarantine Patterns (Non-SaaS, Roleplay, ERP, Unused Language SDKs)
QUARANTINE_PATTERNS = [
    r"^odoo-", r"^sankhya-", r"^makepad-", r"^hig-", r"leiloeiro", r"advogado",
    r"psychologist", r"health-analyzer", r"sexual-health", r"tcm-constitution",
    r"sleep-analyzer", r"daily-gift", r"elon-musk", r"steve-jobs", r"yann-lecun",
    r"filosofia", r"seo-aeo", r"astrology", r"tarot", r"recipe", r"workout",
    r"^azure-.*-(java|dotnet|rust|cpp|go|php|ruby)$"
]

# Maps your top skills directly to the exact STACK_SIGNATURES tags in apex_ctl.py
SKILL_TO_DOMAIN_TAG = {
    "nextjs-app-router-patterns": ("nextjs", "05-frontend-craft"),
    "nextjs-supabase-auth":       ("nextjs", "06-security-zero-trust"),
    "deploy-to-vercel":           ("nextjs", "07-devops-cloud-cicd"),
    "vercel-react-best-practices":("react", "05-frontend-craft"),
    "composition-patterns":       ("react", "05-frontend-craft"),
    "tanstack-query-expert":      ("react", "05-frontend-craft"),
    "zustand-store-ts":           ("react", "05-frontend-craft"),
    "shadcn":                     ("tailwind", "05-frontend-craft"),
    "tailwind-design-system":     ("tailwind", "05-frontend-craft"),
    "impeccable":                 ("react", "05-frontend-craft"),
    "hallmark":                   ("tailwind", "05-frontend-craft"),
    "nodejs-backend-patterns":    ("express", "04-backend-resilience"),
    "prisma-expert":              ("prisma", "03-database-tenancy"),
    "drizzle-orm-expert":         ("drizzle", "03-database-tenancy"),
    "stripe-integration":         ("stripe", "04-backend-resilience"),
    "pci-compliance":             ("stripe", "06-security-zero-trust"),
    "zod-validation-expert":      ("typescript", "04-backend-resilience"),
    "test-driven-development":    ("vitest", "04-backend-resilience"),
    "playwright-skill":           ("jest", "06-security-zero-trust"),
    "fastapi-pro":                ("fastapi", "04-backend-resilience"),
    "pydantic-models-py":         ("pydantic", "04-backend-resilience"),
    "postgres-best-practices":    ("sqlalchemy", "03-database-tenancy"),
    "database-migrations-sql-migrations": ("alembic", "03-database-tenancy"),
    "bullmq-specialist":          ("celery", "04-backend-resilience"),
}

# Core Department Winners (Always fused into the 8 Department Cartridges)
CORE_WINNERS = {
    "gravitas": "00-cognitive-kernel",
    "graphify": "00-cognitive-kernel",
    "ponytail": "00-cognitive-kernel",
    "hierarchical-agent-memory": "00-cognitive-kernel",
    "anti-sycophancy": "00-cognitive-kernel",
    "verification-before-completion": "00-cognitive-kernel",
    "idea-os": "01-product-discovery",
    "product-manager-toolkit": "01-product-discovery",
    "ask-questions-if-underspecified": "01-product-discovery",
    "clarity-gate": "01-product-discovery",
    "c4-architecture-c4-architecture": "02-principal-architect",
    "architecture-decision-records": "02-principal-architect",
    "openapi-spec-generation": "02-principal-architect",
    "saas-multi-tenant": "03-database-tenancy",
    "postgresql-optimization": "03-database-tenancy",
    "backend-architect": "04-backend-resilience",
    "api-design-principles": "04-backend-resilience",
    "error-handling-patterns": "04-backend-resilience",
    "wcag-audit-patterns": "05-frontend-craft",
    "web-performance-optimization": "05-frontend-craft",
    "impeccable": "05-frontend-craft",
    "hallmark": "05-frontend-craft",
    "security-audit": "06-security-zero-trust",
    "backend-security-coder": "06-security-zero-trust",
    "auth-implementation-patterns": "06-security-zero-trust",
    "idor-testing": "06-security-zero-trust",
    "sql-injection-testing": "06-security-zero-trust",
    "docker-expert": "07-devops-cloud-cicd",
    "container-security-hardening": "07-devops-cloud-cicd",
    "github-actions-templates": "07-devops-cloud-cicd",
    "distributed-tracing": "07-devops-cloud-cicd",
    "systematic-debugging": "08-deep-debugger",
    "phase-gated-debugging": "08-deep-debugger",
    "error-debugging-error-trace": "08-deep-debugger",
}


def parse_skill_md(skill_md: Path) -> dict:
    try:
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"description": "", "rigor": 0, "rules": []}

    desc = ""
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if fm:
        m = re.search(r"description:\s*(.+)", fm.group(1))
        if m:
            desc = m.group(1).strip().strip('"\'')[:180]

    has_code = 30 if "```" in text else 0
    has_rules = min(40, len(re.findall(r"\b(MUST|NEVER|ALWAYS|FORBIDDEN|REQUIRED|DO NOT)\b", text)) * 5)
    has_cli = 30 if re.search(r"\b(npm|npx|pytest|tsc|git|docker|python)\b", text) else 0
    rigor = has_code + has_rules + has_cli

    bullets = re.findall(r"^\s*[-*]\s+(.+)$", text, re.MULTILINE)
    rules = []
    for b in bullets:
        clean = re.sub(r"[`*_]+", "", b).strip()
        if 25 <= len(clean) <= 140 and any(k in clean.upper() for k in ["MUST", "NEVER", "ALWAYS", "USE", "AVOID", "ENSURE", "DO NOT"]):
            rules.append(clean)
        if len(rules) >= 4:
            break

    if not rules and bullets:
        for b in bullets[:3]:
            clean = re.sub(r"[`*_]+", "", b).strip()
            if 20 <= len(clean) <= 140:
                rules.append(clean)

    return {"description": desc, "rigor": rigor, "rules": rules}


def infer_domain_tag(name: str, desc: str) -> str:
    combined = f"{name} {desc}".lower()
    for keyword, tag in [
        ("next", "nextjs"), ("react", "react"), ("tailwind", "tailwind"),
        ("prisma", "prisma"), ("drizzle", "drizzle"), ("stripe", "stripe"),
        ("fastapi", "fastapi"), ("pydantic", "pydantic"), ("django", "django"),
        ("flask", "flask"), ("sqlalchemy", "sqlalchemy"), ("pytest", "pytest"),
        ("vitest", "vitest"), ("jest", "jest"), ("express", "express"),
        ("fastify", "fastify"), ("trpc", "trpc"), ("typescript", "typescript")
    ]:
        if keyword in combined:
            return tag
    return "core"


def main() -> int:
    parser = argparse.ArgumentParser(description="Apex Phase 2 Local Skills Indexer & Vault Isolator")
    parser.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR)
    parser.add_argument("--vault-dir", type=Path, default=DEFAULT_VAULT_DIR)
    parser.add_argument("--project-dir", type=Path, default=DEFAULT_PROJECT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    if args.restore:
        if not args.vault_dir.exists():
            print("Vault directory not found.")
            return 0
        count = 0
        for item in args.vault_dir.iterdir():
            if item.is_dir():
                dest = args.skills_dir / item.name
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                    count += 1
        print(f"Restored {count} skills back to {args.skills_dir}")
        return 0

    scan_roots = [p for p in (args.skills_dir, args.vault_dir) if p.exists()]
    if not scan_roots:
        print(f"ERROR: Skills directory not found at {args.skills_dir}")
        return 1

    folders = {}
    for r in scan_roots:
        for item in r.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                folders[item.name] = item

    # Schema compatible with apex_ctl.py (`registry.get("skills", {})`)
    registry = {
        "version": "3.2.0",
        "generated_at": datetime.now().isoformat(),
        "vault_path": str(args.vault_dir),
        "stats": {
            "total_scanned": 0,
            "core_winners": 0,
            "stack_mapped": 0,
            "quarantined": 0,
            "moved_to_vault": 0
        },
        "skills": {},
        "quarantined_skills": []
    }

    for name, folder in sorted(folders.items()):
        if name in PROTECTED_ACTIVE_SKILLS:
            continue

        registry["stats"]["total_scanned"] += 1
        skill_md = folder / "SKILL.md"
        meta = parse_skill_md(skill_md) if skill_md.exists() else {"description": "", "rigor": 0, "rules": []}
        lower_name = name.lower()

        # Pass 1: Quarantine check
        if any(re.search(p, lower_name) or re.search(p, meta["description"].lower()) for p in QUARANTINE_PATTERNS):
            registry["stats"]["quarantined"] += 1
            registry["quarantined_skills"].append(name)
            continue

        # Pass 2 & 3: Stack Add-ons & Core Winners
        if lower_name in SKILL_TO_DOMAIN_TAG:
            domain_tag, dept = SKILL_TO_DOMAIN_TAG[lower_name]
            registry["stats"]["stack_mapped"] += 1
            registry["skills"][name] = {
                "domain": domain_tag,
                "department": dept,
                "tier": "stack_addon",
                "description": meta["description"],
                "rules": meta["rules"]
            }
        elif lower_name in CORE_WINNERS:
            dept = CORE_WINNERS[lower_name]
            registry["stats"]["core_winners"] += 1
            registry["skills"][name] = {
                "domain": "core",
                "department": dept,
                "tier": "core_winner",
                "description": meta["description"],
                "rules": meta["rules"]
            }
        elif meta["rigor"] >= 45:
            domain_tag = infer_domain_tag(lower_name, meta["description"])
            if domain_tag != "core":
                registry["stats"]["stack_mapped"] += 1
                registry["skills"][name] = {
                    "domain": domain_tag,
                    "department": "04-backend-resilience",
                    "tier": "indexed",
                    "description": meta["description"],
                    "rules": meta["rules"]
                }
            else:
                registry["stats"]["quarantined"] += 1
                registry["quarantined_skills"].append(name)
        else:
            registry["stats"]["quarantined"] += 1
            registry["quarantined_skills"].append(name)

    # Move raw skills to ~/.agents/skills-vault/ on --execute
    if args.execute and not args.dry_run:
        args.vault_dir.mkdir(parents=True, exist_ok=True)
        if args.skills_dir.exists():
            for item in list(args.skills_dir.iterdir()):
                if item.is_dir() and item.name not in PROTECTED_ACTIVE_SKILLS and not item.name.startswith("."):
                    target = args.vault_dir / item.name
                    if target.exists():
                        shutil.rmtree(target)
                    shutil.move(str(item), str(target))
                    registry["stats"]["moved_to_vault"] += 1

    apex_dir = args.project_dir / ".apex"
    apex_dir.mkdir(parents=True, exist_ok=True)
    out_file = apex_dir / "skill-registry.json"
    out_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    # Log to docs/WORKFORCE_LEDGER.md
    ledger = args.project_dir / "docs" / "WORKFORCE_LEDGER.md"
    if ledger.exists():
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        mode = "LIVE" if (args.execute and not args.dry_run) else "DRY-RUN"
        with ledger.open("a", encoding="utf-8") as lf:
            lf.write(
                f"| {ts} | 00-Kernel-Indexer | `.apex/skill-registry.json` "
                f"| Phase 2 ({mode}): Scanned {registry['stats']['total_scanned']}, "
                f"Active {len(registry['skills'])}, Quarantined {registry['stats']['quarantined']} | `PASS` |\n"
            )

    print("=== APEX PHASE 2 SKILL INDEXER COMPLETE ===")
    print(f"  Total Scanned     : {registry['stats']['total_scanned']}")
    print(f"  Core Winners      : {registry['stats']['core_winners']}")
    print(f"  Stack-Mapped      : {registry['stats']['stack_mapped']}")
    print(f"  Quarantined Noise : {registry['stats']['quarantined']}")
    print(f"  Moved to Vault    : {registry['stats']['moved_to_vault']}")
    print(f"  Registry Saved    : {out_file}")
    print("===========================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
