"""Make one minimal, non-experimental request to validate API credentials."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.llm.openai_client import OpenAIResponsesClient


def explain_api_error(error: Exception) -> str:
    code = getattr(error, "code", None)
    if code == "insufficient_quota":
        return (
            "OpenAI API reached the account, but this API project has no available "
            "quota. Add API billing/credits and verify project spending limits, "
            "then retry."
        )
    if code == "model_not_found":
        return (
            "The configured AALLT_MODEL is not available to this API project. "
            "Choose an enabled model ID and retry."
        )
    return f"OpenAI API request failed: {error}"


def main() -> None:
    try:
        client = OpenAIResponsesClient()
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
