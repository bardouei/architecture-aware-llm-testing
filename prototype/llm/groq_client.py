"""Groq API adapter using its OpenAI-compatible chat endpoint."""

from __future__ import annotations

import os
import time
from typing import Any, Callable, Optional

from prototype.llm.llm_client import LLMClient


class GroqClient(LLMClient):
    BASE_URL = "https://api.groq.com/openai/v1"

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        client: Any = None,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        self.model = model or os.environ.get("AALLT_MODEL")
        if not self.model:
            raise ValueError("AALLT_MODEL is required")

        if client is None:
            resolved_api_key = api_key or os.environ.get("GROQ_API_KEY")
            if not resolved_api_key:
                raise ValueError("GROQ_API_KEY is required")
            try:
                from openai import OpenAI
            except ImportError as error:
                raise RuntimeError(
                    "OpenAI-compatible SDK is missing. Run .venv/bin/python "
                    "-m pip install -r requirements.txt"
                ) from error
            client = OpenAI(api_key=resolved_api_key, base_url=self.BASE_URL)

        self.client = client
        self.clock = clock
        self.last_metadata: dict[str, Any] = {}

    def generate(self, prompt: str) -> str:
        started = self.clock()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed_ms = round((self.clock() - started) * 1000, 2)
        usage = getattr(response, "usage", None)
        self.last_metadata = {
            "provider": "groq",
            "request_id": getattr(response, "id", None),
            "model": getattr(response, "model", self.model),
            "latency_ms": elapsed_ms,
            "usage": usage.model_dump() if hasattr(usage, "model_dump") else usage,
            "base_url": self.BASE_URL,
        }
        return response.choices[0].message.content or ""
