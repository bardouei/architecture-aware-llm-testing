"""OpenAI Responses API adapter for real test generation."""

from __future__ import annotations

import os
import time
from typing import Any, Callable, Optional

from prototype.llm.llm_client import LLMClient


class OpenAIResponsesClient(LLMClient):
    """Generate text through the OpenAI Responses API.

    The adapter keeps the existing string-returning ``LLMClient`` contract while
    exposing request metadata for the experiment provenance layer.
    """

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
            resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
            if not resolved_api_key:
                raise ValueError("OPENAI_API_KEY is required")
            try:
                from openai import OpenAI
            except ImportError as error:
                raise RuntimeError(
                    "OpenAI SDK is missing. Run .venv/bin/python -m pip install "
                    "-r requirements.txt"
                ) from error
            client = OpenAI(api_key=resolved_api_key)

        self.client = client
        self.clock = clock
        self.last_metadata: dict[str, Any] = {}

    def generate(self, prompt: str) -> str:
        started = self.clock()
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            store=False,
        )
        elapsed_ms = round((self.clock() - started) * 1000, 2)
        usage = getattr(response, "usage", None)
        self.last_metadata = {
            "provider": "openai",
            "request_id": getattr(response, "id", None),
            "model": getattr(response, "model", self.model),
            "latency_ms": elapsed_ms,
            "usage": usage.model_dump() if hasattr(usage, "model_dump") else usage,
            "store": False,
        }
        return response.output_text
