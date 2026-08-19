"""Normalize model output before writing generated Swift source."""

from __future__ import annotations

import re


THINKING_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
CODE_FENCE = re.compile(r"```(?:swift)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
OPENING_CODE_FENCE = re.compile(r"^```(?:swift)?\s*", re.IGNORECASE)


def clean_generated_code(raw_output: str) -> str:
    """Remove reasoning blocks and return the first fenced Swift block when present."""
    without_thinking = THINKING_BLOCK.sub("", raw_output).strip()
    fenced = CODE_FENCE.search(without_thinking)
    code = (
        fenced.group(1)
        if fenced
        else OPENING_CODE_FENCE.sub("", without_thinking).removesuffix("```")
    )
    return code.strip() + "\n"
