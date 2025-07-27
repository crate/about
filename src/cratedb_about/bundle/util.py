import json
import logging
import os
from pathlib import Path

import tiktoken

logger = logging.getLogger(__name__)


def count_tokens(file: Path):
    prompt = file.read_text()

    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(prompt)
    token_count_gpt = len(tokens)

    token_count_sonnet = -1
    if "ANTHROPIC_API_KEY" in os.environ:
        import anthropic

        client = anthropic.Anthropic()
        response = client.messages.count_tokens(
            model="claude-sonnet-4-20250514",
            system=prompt,
            messages=[
                {
                    "role": "user",
                    "content": "No-op.",
                }
            ],
        )
        token_count_sonnet = json.loads(response.json())["input_tokens"]

    logger.info(
        f"Token count for file {file}: {token_count_gpt} (GPT), {token_count_sonnet} (Sonnet)"
    )
    threshold = 200_000
    if token_count_gpt >= threshold or token_count_sonnet >= threshold:
        logger.warning(
            "Attention: Token count is larger than 200_000. "
            "This means LLMs like Anthropic Claude or Opus will reject processing."
        )
