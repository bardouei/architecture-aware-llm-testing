"""Make one minimal request to validate the Groq API configuration."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.llm.groq_client import GroqClient


def explain_api_error(error: Exception) -> str:
    code = getattr(error, "code", None)
    status = getattr(error, "status_code", None)
    if status == 401 or code in {"invalid_api_key", "authentication_error"}:
        return "Groq rejected GROQ_API_KEY. Create or export a valid key and retry."
    if status == 429:
        return "Groq free-tier rate limit was reached. Wait for the limit to reset."
    if status == 404 or code in {"model_not_found", "model_decommissioned"}:
        return "AALLT_MODEL is unavailable on Groq. Select an active model ID."
    return f"Groq API request failed: {error}"


def main() -> None:
    try:
        client = GroqClient()
    except ValueError as error:
        raise SystemExit(
            f"Configuration error: {error}. Export the missing variable and retry."
        ) from error
    try:
        output = client.generate("Reply with exactly: CONNECTION_OK")
    except Exception as error:
        raise SystemExit(explain_api_error(error)) from error
    print(output.strip())
    print(client.last_metadata)


if __name__ == "__main__":
    main()
