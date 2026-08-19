"""Make one minimal, non-experimental request to validate API credentials."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.llm.openai_client import OpenAIResponsesClient


def main() -> None:
    try:
        client = OpenAIResponsesClient()
    except ValueError as error:
        raise SystemExit(
            f"Configuration error: {error}. Export the missing variable and retry."
        ) from error
    output = client.generate("Reply with exactly: CONNECTION_OK")
    print(output.strip())
    print(client.last_metadata)


if __name__ == "__main__":
    main()
