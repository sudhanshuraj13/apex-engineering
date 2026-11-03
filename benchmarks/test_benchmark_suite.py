#!/usr/bin/env python3
"""
APEX-ENGINEERING PHASE 5 — DETERMINISTIC 4-STAGE BENCHMARK TEST SUITE
Verifies all 4 enterprise stages + trace artifacts.
"""

import os
import ast
import hmac
import hashlib
import sqlite3
import inspect
import unittest
from pathlib import Path

from benchmarks import fixtures_broken as sut


class TestApexBenchmarkSuite(unittest.TestCase):

    # ── Stage 1: Database Tenancy & RLS Isolation ────────────────────────────
    def test_stage1_tenant_isolation_blocks_cross_tenant_leak(self):
        repo = sut.TenantInvoiceRepo()
        repo.create_invoice("tenant-alpha", "inv-1", 5000)
        repo.create_invoice("tenant-beta", "inv-2", 9000)

        alpha_rows = repo.list_invoices("tenant-alpha")
        self.assertEqual(len(alpha_rows), 1, "RLS Leak: Tenant Alpha saw Tenant Beta's invoices!")
        self.assertEqual(alpha_rows[0][1], "tenant-alpha")

    def test_stage1_rejects_invalid_tenant_or_negative_amount(self):
        repo = sut.TenantInvoiceRepo()
        with self.assertRaises(ValueError):
            repo.create_invoice("", "inv-bad", 100)
        with self.assertRaises(ValueError):
            repo.create_invoice("tenant-alpha", "inv-neg", -500)

    # ── Stage 2: Backend Webhook Validation, Idempotency & Lock Release ─────
    def test_stage2_webhook_validation_and_idempotency(self):
        redis_store = {}
        balances = {}
        valid_payload = {"event_id": "evt_101", "tenant_id": "tenant-1", "amount_cents": 2500}

        res1 = sut.process_stripe_webhook(valid_payload, redis_store, balances)
        self.assertEqual(res1["status"], 200)
        self.assertEqual(balances["tenant-1"], 2500)

        # Duplicate retry must be ignored without double-charging
        res2 = sut.process_stripe_webhook(valid_payload, redis_store, balances)
        self.assertEqual(res2["body"]["status"], "DUPLICATE_IGNORED")
        self.assertEqual(balances["tenant-1"], 2500)

        # Invalid payload must return 400
        bad_res = sut.process_stripe_webhook({"event_id": "", "tenant_id": "t1", "amount_cents": -10}, redis_store, balances)
        self.assertEqual(bad_res["status"], 400)

    def test_stage2_releases_idempotency_lock_on_transient_failure(self):
        redis_store = {}
        balances = {}
        payload = {"event_id": "evt_retry_1", "tenant_id": "tenant-2", "amount_cents": 4000}

        with self.assertRaises(RuntimeError):
            sut.process_stripe_webhook(payload, redis_store, balances, simulate_transient_error=True)

        # Subsequent retry after transient failure must succeed
        res = sut.process_stripe_webhook(payload, redis_store, balances, simulate_transient_error=False)
        self.assertEqual(res["status"], 200)
        self.assertEqual(balances["tenant-2"], 4000)

    # ── Stage 3: 5-CWE Security Audit (AST + Runtime Verification) ──────────
    def test_stage3_no_hardcoded_secrets_and_uses_timing_safe_hmac(self):
        src = inspect.getsource(sut)
        self.assertNotIn("sk_live_", src, "CWE-798 Violation: Hardcoded sk_live_ secret still in source!")
        self.assertIn("compare_digest", inspect.getsource(sut.verify_signature), "CWE-208 Violation: Must use hmac.compare_digest!")

        payload = b'{"event":"invoice.paid"}'
        secret = "test_webhook_secret_key"
        valid_sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        self.assertTrue(sut.verify_signature(payload, valid_sig, secret))
        self.assertFalse(sut.verify_signature(payload, "0" * len(valid_sig), secret))

    def test_stage3_blocks_bola_and_sql_injection(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id TEXT, email TEXT, tenant_id TEXT)")
        conn.execute("INSERT INTO users VALUES ('u1', 'alice@corp.com', 'tenant-A')")
        conn.execute("INSERT INTO users VALUES ('u2', 'bob@evil.com', 'tenant-B')")

        # BOLA check: Tenant B session requesting Tenant A record must raise PermissionError
        with self.assertRaises(PermissionError):
            sut.get_tenant_record(conn, "tenant-B", "tenant-A", "alice@corp.com")

        # SQL Injection check: malicious email payload must return None safely, not bypass filter
        sqli_email = "' OR '1'='1"
        row = sut.get_tenant_record(conn, "tenant-A", "tenant-A", sqli_email)
        self.assertIsNone(row, "CWE-89 Violation: SQL Injection bypassed email filter!")

    def test_stage3_blocks_command_injection_and_shell_true(self):
        fn_src = inspect.getsource(sut.check_host_reachability)
        self.assertNotIn("shell=True", fn_src, "CWE-78 Violation: shell=True is forbidden!")
        with self.assertRaises(ValueError):
            sut.check_host_reachability("example.com; rm -rf /")

    # ── Stage 4: Multi-Hop Deep Debugger Trace & Root-Cause Fix ─────────────
    def test_stage4_multihop_pipeline_and_trace_artifacts(self):
        res1 = sut.hop0_api_gateway({"tenant_id": "tenant-X", "amount_cents": 1500})
        self.assertEqual(res1, {"tenant-X": 1500})

        # Second call must not leak state from first call via mutable default argument
        res2 = sut.hop0_api_gateway({"tenant_id": "tenant-Y", "amount_cents": 3000})
        self.assertEqual(res2, {"tenant-Y": 3000}, "State leak: Mutable default list retained previous job!")

        # Verify Deep Debugger created trace-ledger.md and logged to ISSUE_TRACKER.md
        trace_file = Path(".apex/artifacts/trace-ledger.md")
        issue_file = Path("docs/ISSUE_TRACKER.md")
        self.assertTrue(trace_file.exists(), "08-deep-debugger violation: .apex/artifacts/trace-ledger.md missing!")
        self.assertIn("hop1_queue_serializer", trace_file.read_text(encoding="utf-8"))
        self.assertIn("hop1_queue_serializer", issue_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

