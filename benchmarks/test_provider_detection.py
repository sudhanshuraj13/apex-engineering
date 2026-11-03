#!/usr/bin/env python3
"""
Unit tests for Universal AI Provider Auto-Detection in scripts/bharat_harness.py
Verifies provider resolution across BharatCode, Gemini, OpenAI, Groq, OpenRouter, Ollama, and IDE-Native.
"""

import os
import unittest
from unittest.mock import patch

from scripts.bharat_harness import resolve_provider_config


class TestUniversalProviderDetection(unittest.TestCase):

    def test_explicit_provider_overrides(self):
        providers_expected = [
            ("bharatcode", "qwen-3.8-27b"),
            ("gemini", "gemini-2.5-flash"),
            ("openai", "gpt-4o-mini"),
            ("groq", "llama-3.3-70b-versatile"),
            ("openrouter", "meta-llama/llama-3.3-70b-instruct:free"),
            ("ollama", "qwen2.5-coder:7b"),
            ("ide-native", "universal-ide-agent"),
        ]
        for prov_id, expected_model in providers_expected:
            cfg = resolve_provider_config(cli_provider=prov_id)
            self.assertEqual(cfg["provider"], prov_id)
            self.assertEqual(cfg["model"], expected_model)

    def test_explicit_model_override(self):
        cfg = resolve_provider_config(cli_provider="gemini", cli_model="gemini-1.5-pro")
        self.assertEqual(cfg["provider"], "gemini")
        self.assertEqual(cfg["model"], "gemini-1.5-pro")

    def test_auto_detect_gemini(self):
        clean_env = {
            "BHARATCODE_API_KEY": "",
            "GEMINI_API_KEY": "test_gemini_key_123",
            "OPENAI_API_KEY": "",
            "GROQ_API_KEY": "",
            "OPENROUTER_API_KEY": "",
            "OLLAMA_MODEL": ""
        }
        with patch.dict(os.environ, clean_env, clear=False):
            # Patch load_dotenv inside test so it does not re-read disk .env
            with patch("scripts.bharat_harness.load_dotenv"):
                cfg = resolve_provider_config()
                self.assertEqual(cfg["provider"], "gemini")
                self.assertEqual(cfg["model"], "gemini-2.5-flash")
                self.assertEqual(cfg["api_key"], "test_gemini_key_123")

    def test_auto_detect_openai(self):
        clean_env = {
            "BHARATCODE_API_KEY": "",
            "GEMINI_API_KEY": "",
            "OPENAI_API_KEY": "sk-proj-test12345",
            "GROQ_API_KEY": "",
            "OPENROUTER_API_KEY": "",
            "OLLAMA_MODEL": ""
        }
        with patch.dict(os.environ, clean_env, clear=False):
            with patch("scripts.bharat_harness.load_dotenv"):
                cfg = resolve_provider_config()
                self.assertEqual(cfg["provider"], "openai")
                self.assertEqual(cfg["model"], "gpt-4o-mini")
                self.assertEqual(cfg["api_key"], "sk-proj-test12345")

    def test_auto_detect_groq(self):
        clean_env = {
            "BHARATCODE_API_KEY": "",
            "GEMINI_API_KEY": "",
            "OPENAI_API_KEY": "",
            "GROQ_API_KEY": "gsk_test12345678",
            "OPENROUTER_API_KEY": "",
            "OLLAMA_MODEL": ""
        }
        with patch.dict(os.environ, clean_env, clear=False):
            with patch("scripts.bharat_harness.load_dotenv"):
                cfg = resolve_provider_config()
                self.assertEqual(cfg["provider"], "groq")
                self.assertEqual(cfg["model"], "llama-3.3-70b-versatile")
                self.assertEqual(cfg["api_key"], "gsk_test12345678")

    def test_fallback_to_ide_native_when_keys_missing_or_placeholder(self):
        clean_env = {
            "BHARATCODE_API_KEY": "your_bharatcode_key",
            "GEMINI_API_KEY": "your_gemini_key",
            "OPENAI_API_KEY": "your_openai_key",
            "GROQ_API_KEY": "",
            "OPENROUTER_API_KEY": "",
            "OLLAMA_MODEL": ""
        }
        with patch.dict(os.environ, clean_env, clear=False):
            with patch("scripts.bharat_harness.load_dotenv"):
                cfg = resolve_provider_config()
                self.assertEqual(cfg["provider"], "ide-native")
                self.assertEqual(cfg["model"], "universal-ide-agent")
                self.assertEqual(cfg["base_url"], "local")


if __name__ == "__main__":
    unittest.main()
