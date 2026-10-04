import os
import unittest
from unittest.mock import AsyncMock, Mock, patch

from backend.main import llm_summary


class TestOptionalAiProvider(unittest.IsolatedAsyncioTestCase):
    async def test_no_key_uses_rule_based_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(await llm_summary("message", {"signals": []}, "en"))

    async def test_gemini_key_uses_gemini_and_returns_text(self):
        response = Mock()
        response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Verify the claim independently."}]}}]
        }
        client = AsyncMock()
        client.__aenter__.return_value = client
        client.post.return_value = response

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            with patch("backend.main.httpx.AsyncClient", return_value=client):
                summary = await llm_summary("test message", {"signals": []}, "en")

        self.assertEqual(summary, "Verify the claim independently.")
        args, kwargs = client.post.call_args
        self.assertIn("models/gemini-3.8-flash:generateContent", args[0])
        self.assertEqual(kwargs["headers"]["x-goog-api-key"], "test-key")
        self.assertIn("systemInstruction", kwargs["json"])