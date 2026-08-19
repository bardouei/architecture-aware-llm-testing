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
        temperature: Optional[float] = None,
        max_completion_tokens: Optional[int] = None,
        reasoning_format: Optional[str] = None,
        reasoning_effort: Optional[str] = None,
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
        self.request_settings = {
            "temperature": temperature,
            "max_completion_tokens": max_completion_tokens,
            "reasoning_format": reasoning_format,
            "reasoning_effort": reasoning_effort,
        }
        self.last_metadata: dict[str, Any] = {}

    def generate(self, prompt: str) -> str:
        started = self.clock()
        request: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if self.request_settings["temperature"] is not None:
            request["temperature"] = self.request_settings["temperature"]
        if self.request_settings["max_completion_tokens"] is not None:
            request["max_completion_tokens"] = self.request_settings[
                "max_completion_tokens"
            ]
        reasoning_options = {
            key: self.request_settings[key]
            for key in ("reasoning_format", "reasoning_effort")
            if self.request_settings[key] is not None
        }
        if reasoning_options:
            request["extra_body"] = reasoning_options
        response = self.client.chat.completions.create(**request)
        elapsed_ms = round((self.clock() - started) * 1000, 2)
        usage = getattr(response, "usage", None)
        self.last_metadata = {
            "provider": "groq",
            "request_id": getattr(response, "id", None),
            "model": getattr(response, "model", self.model),
            "latency_ms": elapsed_ms,
            "usage": usage.model_dump() if hasattr(usage, "model_dump") else usage,
            "base_url": self.BASE_URL,
            "request_settings": self.request_settings,
            "finish_reason": getattr(response.choices[0], "finish_reason", None),
        }
        return response.choices[0].message.content or ""
