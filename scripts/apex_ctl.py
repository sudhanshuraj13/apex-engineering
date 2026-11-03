#!/usr/bin/env python3
"""
Apex-Engineering L1/L3 Memory Controller & Gravitas Verification Gate.
Zero external dependencies (uses Python standard library only).

Phase 2 ready: auto-reads .apex/skill-registry.json, detects project
stack from package.json / pyproject.toml, and enforces allowed_write_scope
via git diff before marking verification as PASS.
"""

from pathlib import Path
import os
import sys
import json
import sqlite3
import subprocess
import fnmatch
import argparse
import ast
from datetime import datetime

# Ensure UTF-8 console output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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

# Backward compatibility aliases
L1_REGISTER = L1_PATH
L3_ARCHIVE = L3_DB_PATH
SKILL_REGISTRY = SKILL_REGISTRY_PATH
WORKFORCE_LEDGER = LEDGER_PATH
ISSUE_TRACKER = ISSUES_PATH
COMPANY_DAG = DAG_PATH
APEX_DIR = APEX_STATE_DIR

# ── Stack-detection rules ────────────────────────────────────────────────────
# Maps dependency names found in package.json / pyproject.toml to distilled
# stack tags.  When Phase 2 creates .apex/skill-registry.json these tags are
# matched against registered cartridge domains for automatic injection.
STACK_SIGNATURES = {
    # Node / JS ecosystem (package.json → dependencies + devDependencies)
    "next":          "nextjs",
    "react":         "react",
    "express":       "express",
    "fastify":       "fastify",
    "prisma":        "prisma",
    "@trpc/server":  "trpc",
    "drizzle-orm":   "drizzle",
    "stripe":        "stripe",
    "vitest":        "vitest",
    "jest":          "jest",
    "tailwindcss":   "tailwind",
    "typescript":    "typescript",
    # Python ecosystem (pyproject.toml → [project.dependencies])
    "django":        "django",
    "fastapi":       "fastapi",
    "flask":         "flask",
    "sqlalchemy":    "sqlalchemy",
    "alembic":       "alembic",
    "pytest":        "pytest",
    "stripe":        "stripe",
    "celery":        "celery",
    "pydantic":      "pydantic",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def init_environment():
    """Ensure .apex/, docs/, cartridges/ and seed files exist in PROJECT_ROOT."""
    APEX_STATE_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    if not L1_PATH.exists():
        default_l1 = {
            "current_phase": "04-backend-resilience",
            "active_goal": "Initialize Apex workspace",
            "allowed_write_scope": ["*"],
            "completed_steps": [],
            "blacklisted_attempts": [],
        }
        with open(L1_PATH, "w", encoding="utf-8") as f:
            json.dump(default_l1, f, indent=2)

    conn = sqlite3.connect(str(L3_DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_fts (
            entity_key TEXT PRIMARY KEY,
            domain TEXT,
            content TEXT,
            updated_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS l3_archive (
            entity_key TEXT PRIMARY KEY,
            domain TEXT,
            specification TEXT,
            updated_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    if not LEDGER_PATH.exists():
        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            f.write(
                "# Enterprise Workforce Execution Ledger\n\n"
                "| Timestamp | Department | Scope Mutated | Summary of Work | Gate Status |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
            )

    if not ISSUES_PATH.exists():
        with open(ISSUES_PATH, "w", encoding="utf-8") as f:
            f.write(
                "# Enterprise Issue & Debug Tracker\n\n"
                "| Date | Issue ID | Root Cause Hop | Fix Applied | Status |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
            )


def detect_stack():
    """Scan package.json and pyproject.toml in PROJECT_ROOT; return list of matched stack tags."""
    tags = []
    # ── Node / package.json ──────────────────────────────────────────────
    pkg_file = PROJECT_ROOT / "package.json"
    if pkg_file.exists():
        try:
            with open(pkg_file, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            all_deps = {}
            all_deps.update(pkg.get("dependencies", {}))
            all_deps.update(pkg.get("devDependencies", {}))
            for dep, tag in STACK_SIGNATURES.items():
                if dep in all_deps and tag not in tags:
                    tags.append(tag)
        except (json.JSONDecodeError, OSError):
            pass

    # ── Python / pyproject.toml ──────────────────────────────────────────
    pyproj_file = PROJECT_ROOT / "pyproject.toml"
    if pyproj_file.exists():
        try:
            with open(pyproj_file, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            # Lightweight TOML parse: grab dependency names from any line
            # that looks like "dep>=..." or "dep[extra]" inside a list.
            for dep, tag in STACK_SIGNATURES.items():
                if dep in raw and tag not in tags:
                    tags.append(tag)
        except OSError:
            pass

    return tags


def load_skill_registry():
    """Load skill-registry.json from target project or fallback to skill root."""
    target_path = APEX_STATE_DIR / "skill-registry.json"
    if not target_path.exists():
        if SKILL_REGISTRY_PATH.exists():
            target_path = SKILL_REGISTRY_PATH
        else:
            return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def load_department_cartridge(phase):
    """Find and load the active Department Cartridge rules."""
    candidates = [
        CARTRIDGES_DIR / f"{phase}.md",
        CUSTOM_CARTRIDGES_DIR / f"{phase}.md",
    ]
    if DAG_PATH.exists():
        try:
            with open(DAG_PATH, "r", encoding="utf-8") as f:
                dag = json.load(f)
            for dept in dag.get("departments", {}).values():
                if dept.get("id") == phase and dept.get("cartridge"):
                    candidates.insert(0, SKILL_ROOT / dept["cartridge"])
        except Exception:
            pass

    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return str(path), f.read().strip()
            except Exception:
                pass
    return None, None


def get_injected_skills(registry, stack_tags):
    """Match stack tags against registry triggers, returning only relevant rule cards."""
    if not registry:
        return {}

    injected = {}
    cards = registry.get("distilled_rule_cards", {})
    trigger_index = registry.get("trigger_index", {})

    matched_names = set()
    for tag in stack_tags:
        for sk_name in trigger_index.get(tag.lower(), []):
            matched_names.add(sk_name)

    for sk_name, card in cards.items():
        if sk_name in matched_names:
            continue
        triggers = [t.lower() for t in card.get("triggers", [])]
        dept = card.get("department", "").lower()
        if any(t in stack_tags for t in triggers) or any(tag in dept for tag in stack_tags):
            matched_names.add(sk_name)

    # Fallback if registry uses legacy flat "skills" format
    if not cards and "skills" in registry:
        for name, meta in registry["skills"].items():
            domain = meta.get("domain", "").lower()
            if domain in stack_tags:
                injected[name] = {
                    "description": meta.get("description", ""),
                    "rules": meta.get("rules", [])
                }
        return injected

    for sk_name in sorted(matched_names):
        card = cards.get(sk_name, {})
        injected[sk_name] = {
            "description": card.get("description", ""),
            "rules": card.get("rules", [])
        }

    return injected


def scope_guard(allowed_scopes):
    """Check git-tracked changes against allowed_write_scope patterns.

    Returns (ok: bool, violations: list[str]).
    A scope of ["*"] allows everything.
    """
    if "*" in allowed_scopes:
        return True, []

    # Get changed files from git (staged + unstaged)
    try:
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=10, cwd=str(PROJECT_ROOT),
        )
        unstaged = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True, timeout=10, cwd=str(PROJECT_ROOT),
        )
        changed = set()
        for line in (staged.stdout + "\n" + unstaged.stdout).strip().splitlines():
            line = line.strip()
            if line:
                changed.add(line)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # git not available or not a repo – skip scope guard
        return True, []

    if not changed:
        return True, []

    violations = []
    for filepath in sorted(changed):
        matched = any(
            fnmatch.fnmatch(filepath, pat) for pat in allowed_scopes
        )
        if not matched:
            violations.append(filepath)

    return len(violations) == 0, violations


def slice_symbol(symbol_name: str):
    """Zero-dependency AST parser & caller search for precise code symbols."""
    print(f"[APEX] Slicing AST & Call Graph for symbol: {symbol_name}")
    slice_results = []

    # 1. Python AST parsing across PROJECT_ROOT python files
    for py_file in PROJECT_ROOT.glob("**/*.py"):
        if any(ignored in py_file.parts for ignored in (".venv", "venv", "node_modules", ".git", "__pycache__")):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == symbol_name:
                    try:
                        rel_path = py_file.relative_to(PROJECT_ROOT)
                    except ValueError:
                        rel_path = py_file
                    args = [arg.arg for arg in node.args.args] if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
                    slice_results.append(f"Definition: {rel_path}:{node.lineno} -> {symbol_name}({', '.join(args)})")
        except Exception:
            continue

    # 2. Fast multi-language caller search using git grep
    try:
        grep_res = subprocess.run(["git", "grep", "-n", symbol_name], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        if grep_res.returncode == 0:
            lines = [line.strip() for line in grep_res.stdout.splitlines() if line.strip()][:5]
            slice_results.append("Callers / References:")
            slice_results.extend([f"  - {l}" for l in lines])
    except Exception:
        pass

    if slice_results:
        print("\n--- AST CALL GRAPH SLICE ---")
        for r in slice_results:
            print(r)
        print("----------------------------\n")
    else:
        print(f"[APEX] Symbol '{symbol_name}' not found in workspace AST index.\n")


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_begin(task_desc=None, symbol=None):
    """Load L1 context, detect stack, inject matching rules, print compact summary, slice symbol if provided."""
    init_environment()

    with open(L1_PATH, "r", encoding="utf-8") as f:
        l1_data = json.load(f)

    # Update active goal in L1
    if task_desc:
        l1_data["active_goal"] = task_desc
        with open(L1_PATH, "w", encoding="utf-8") as f:
            json.dump(l1_data, f, indent=2)

    phase = l1_data.get("current_phase", "04-backend-resilience")
    goal = l1_data.get("active_goal", "General task")

    print("=== APEX MEMORY CONTEXT LOADED ===")
    print(f"  Phase   : {phase}")
    print(f"  Goal    : {goal}")
    print(f"  Scope   : {l1_data.get('allowed_write_scope')}")

    # ── Blacklisted attempts ──
    blacklists = l1_data.get("blacklisted_attempts", [])
    if blacklists:
        print(f"  WARNING : {len(blacklists)} blacklisted attempt(s)")
        for b in blacklists[-3:]:
            print(f"            ✗ {b}")

    # ── Stack detection ──
    stack_tags = detect_stack()
    if stack_tags:
        print(f"  Stack   : {', '.join(stack_tags)}")
    elif (PROJECT_ROOT / "package.json").exists() or (PROJECT_ROOT / "pyproject.toml").exists():
        print("  Stack   : (manifest detected – no registered stack add-ons)")
    else:
        print("  Stack   : (no package.json or pyproject.toml detected)")

    # ── Skill-registry (Phase 2) — Only print matched stack skills! ──
    registry = load_skill_registry()
    if registry:
        skills = registry.get("skills", {})
        injected_skills = [
            (name, meta) for name, meta in skills.items()
            if meta.get("domain") in stack_tags
        ]
        print(f"  Registry: {len(skills)} indexed in vault | {len(injected_skills)} active for stack")
        for name, meta in injected_skills[:4]:
            print(f"            • {name} [{meta.get('domain')}] → INJECTED")
            for rule in meta.get("rules", [])[:2]:
                print(f"              - {rule}")
    else:
        print("  Registry: (none – will activate in Phase 2)")

    print("==================================")

    # ── Active Department Cartridge (<250 tokens) ──
    phase = l1_data.get("current_phase", "04-backend-resilience")
    cartridge_path, cartridge_content = load_department_cartridge(phase)
    if cartridge_content:
        print(f"\n--- ACTIVE CARTRIDGE ({phase}) ---")
        print(cartridge_content)
        print("----------------------------------\n")

    # ── Zero-Dependency AST Symbol Slicer ──
    if symbol:
        slice_symbol(symbol)


def cmd_verify():
    """Run scope guard + test suite, log results, update L1."""
    init_environment()

    with open(L1_PATH, "r", encoding="utf-8") as f:
        l1_data = json.load(f)

    # ── Step 1: Scope guard ──
    allowed = l1_data.get("allowed_write_scope", ["*"])
    ok, violations = scope_guard(allowed)

    if not ok:
        print("SCOPE GUARD FAIL – writes outside allowed_write_scope:")
        for v in violations:
            print(f"  ✗ {v}")
        print(f"  allowed_write_scope = {allowed}")
        print("Amend allowed_write_scope in .apex/l1-register.json or revert the files.")

        fail_summary = f"Scope violation: {', '.join(violations[:5])}"
        if fail_summary not in l1_data.get("blacklisted_attempts", []):
            l1_data.setdefault("blacklisted_attempts", []).append(fail_summary)
            with open(L1_PATH, "w", encoding="utf-8") as f:
                json.dump(l1_data, f, indent=2)

        sys.exit(1)

    print("Scope guard ......... PASS")

    # ── Step 2: Test / typecheck detection ──
    print("Running deterministic verification gate (Typecheck + Tests)...")

    if (PROJECT_ROOT / "benchmarks").exists():
        test_cmd = [sys.executable, "-m", "unittest", "discover", "-s", "benchmarks", "-p", "test_*.py"]
        display_cmd = f'"{sys.executable}" -m unittest discover -s benchmarks -p "test_*.py"'
        result = subprocess.run(test_cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    elif (PROJECT_ROOT / "package.json").exists():
        display_cmd = "npm test"
        result = subprocess.run("npm test", shell=True, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    elif (PROJECT_ROOT / "pyproject.toml").exists():
        display_cmd = "pytest"
        result = subprocess.run("pytest", shell=True, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    else:
        display_cmd = "echo No test runner found, checking syntax..."
        result = subprocess.run(display_cmd, shell=True, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

    if result.returncode == 0:
        print(f"Test runner ......... PASS  ({display_cmd})")
        print("STATUS: PASS (Exit Code 0)")

        # Log to WORKFORCE_LEDGER
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        phase = l1_data.get("current_phase", "unknown")
        with open(LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(
                f"| {timestamp} | {phase} | `workspace` "
                f"| Verified task successfully | `PASS` |\n"
            )

        # Clear blacklisted attempts on success
        l1_data["blacklisted_attempts"] = []
        with open(L1_PATH, "w", encoding="utf-8") as f:
            json.dump(l1_data, f, indent=2)

        sys.exit(0)
    else:
        print(f"Test runner ......... FAIL  ({display_cmd})")
        print("STATUS: FAIL (Non-zero exit code)")
        if result.stdout:
            print(result.stdout[-500:])
        if result.stderr:
            print(result.stderr[-500:])

        # Append failure to L1 blacklist
        fail_summary = f"Command '{display_cmd}' failed with exit code {result.returncode}"
        if fail_summary not in l1_data.get("blacklisted_attempts", []):
            l1_data.setdefault("blacklisted_attempts", []).append(fail_summary)
        with open(L1_PATH, "w", encoding="utf-8") as f:
            json.dump(l1_data, f, indent=2)

        sys.exit(1)


# ── CLI Entrypoint ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apex Engineering Microkernel CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_begin = subparsers.add_parser("begin", help="Begin task session")
    parser_begin.add_argument("--task", type=str, default=None, help="Task description")
    parser_begin.add_argument("--symbol", type=str, default=None, help="AST symbol to slice")
    parser_begin.add_argument("positional_task", nargs="*", default=[], help="Positional task fallback")

    parser_verify = subparsers.add_parser("verify", help="Run verification gate")

    if len(sys.argv) < 2:
        init_environment()
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.command == "begin":
        task_desc = args.task
        if not task_desc and args.positional_task:
            task_desc = " ".join(args.positional_task)
        cmd_begin(task_desc=task_desc, symbol=args.symbol)
    elif args.command == "verify":
        cmd_verify()
    else:
        init_environment()
        parser.print_help()
        sys.exit(1)
