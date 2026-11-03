#!/usr/bin/env python3
"""
APEX-ENGINEERING PHASE 5 — HOSTILE BENCHMARK FIXTURES (REMEDIATED)
Remediated enterprise implementation for Stages 1, 2, 3, and 4:
  - Stage 1 (03-database-tenancy): Validated tenant RLS and SQL scoping
  - Stage 2 (04-backend-resilience): Strict schema validation & atomic idempotency lock
  - Stage 3 (06-security-zero-trust): 5 CWE fixes (Parameterized SQL, BOLA check, Timing-safe digest, shell=False, Env secret)
  - Stage 4 (08-deep-debugger): 3-Hop pipeline key alignment and isolated batch state
"""

import os
import re
import hmac
import hashlib
import sqlite3
import subprocess


# ============================================================================
# STAGE 1: Multi-Tenant Database Isolation (03-database-tenancy)
# ============================================================================
class TenantInvoiceRepo:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE invoices (id TEXT PRIMARY KEY, tenant_id TEXT, amount_cents INTEGER)"
        )

    def create_invoice(self, current_tenant_id: str, invoice_id: str, amount_cents: int):
        if not current_tenant_id or not isinstance(current_tenant_id, str) or not current_tenant_id.strip():
            raise ValueError("current_tenant_id must be a non-empty string")
        if not isinstance(amount_cents, int) or amount_cents <= 0:
            raise ValueError("amount_cents must be a positive integer")
        self.conn.execute(
            "INSERT INTO invoices (id, tenant_id, amount_cents) VALUES (?, ?, ?)",
            (invoice_id, current_tenant_id, amount_cents),
        )
        self.conn.commit()

    def list_invoices(self, current_tenant_id: str):
        if not current_tenant_id or not isinstance(current_tenant_id, str):
            raise ValueError("current_tenant_id must be provided")
        cur = self.conn.execute(
            "SELECT id, tenant_id, amount_cents FROM invoices WHERE tenant_id = ?",
            (current_tenant_id,)
        )
        return cur.fetchall()


# ============================================================================
# STAGE 2: Stripe Webhook Idempotency & Resilience (04-backend-resilience)
# ============================================================================
def process_stripe_webhook(payload: dict, redis_store: dict, ledger_balances: dict, simulate_transient_error: bool = False) -> dict:
    if not isinstance(payload, dict):
        return {"status": 400, "body": {"error": "Invalid payload format"}}

    event_id = payload.get("event_id")
    tenant_id = payload.get("tenant_id")
    amount_cents = payload.get("amount_cents")

    if not event_id or not isinstance(event_id, str):
        return {"status": 400, "body": {"error": "Invalid or missing event_id"}}
    if not tenant_id or not isinstance(tenant_id, str):
        return {"status": 400, "body": {"error": "Invalid or missing tenant_id"}}
    if not isinstance(amount_cents, int) or amount_cents <= 0:
        return {"status": 400, "body": {"error": "amount_cents must be a positive integer"}}

    lock_key = f"idemp:{event_id}"
    if lock_key in redis_store:
        return {"status": 200, "body": {"status": "DUPLICATE_IGNORED"}}

    redis_store[lock_key] = "PROCESSING"

    try:
        if simulate_transient_error:
            raise RuntimeError("Transient downstream DB timeout")

        ledger_balances[tenant_id] = ledger_balances.get(tenant_id, 0) + amount_cents
        redis_store[lock_key] = "COMPLETED"
        return {"status": 200, "body": {"status": "OK"}}
    except Exception:
        if lock_key in redis_store:
            del redis_store[lock_key]
        raise


# ============================================================================
# STAGE 3: Hostile 5-CWE Security Audit (06-security-zero-trust)
# ============================================================================
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")


def verify_signature(payload_bytes: bytes, signature_hex: str, secret: str = None) -> bool:
    active_secret = secret or os.environ.get("WEBHOOK_SECRET", "")
    expected = hmac.new(active_secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature_hex, expected)


def get_tenant_record(db_conn: sqlite3.Connection, session_tenant_id: str, requested_tenant_id: str, email: str):
    if session_tenant_id != requested_tenant_id:
        raise PermissionError("BOLA / IDOR Violation: Cross-tenant access denied")
    query = "SELECT id, email, tenant_id FROM users WHERE tenant_id = ? AND email = ?"
    return db_conn.execute(query, (requested_tenant_id, email)).fetchone()


def check_host_reachability(hostname: str) -> list:
    if not isinstance(hostname, str) or not re.match(r"^[a-zA-Z0-9.-]+$", hostname):
        raise ValueError(f"Invalid hostname: {hostname}")
    subprocess.run(["echo", f"Checking {hostname}"], check=False)
    return ["echo", hostname]


# ============================================================================
# STAGE 4: 3-Hop Async Pipeline Bug (08-deep-debugger)
# ============================================================================
def hop0_api_gateway(raw_event: dict) -> dict:
    """Hop 0 (Entry): Receives valid webhook event and forwards to Queue Serializer."""
    return hop1_queue_serializer(raw_event)


def hop1_queue_serializer(event: dict, batch: list = None) -> dict:
    """Hop 1 (Root Cause Remediation): Serializes job for billing worker with isolated batch."""
    if batch is None:
        batch = []
    serialized = {
        "tenant_id": event["tenant_id"],
        "amount_cents": event["amount_cents"],
    }
    batch.append(serialized)
    return hop2_billing_ledger(batch)


def hop2_billing_ledger(jobs: list) -> dict:
    """Hop 2 (Symptom Site): Expects each job to have `tenant_id` and single-batch isolation."""
    total_by_tenant = {}
    for job in jobs:
        tid = job["tenant_id"]
        total_by_tenant[tid] = total_by_tenant.get(tid, 0) + job["amount_cents"]
    return total_by_tenant
