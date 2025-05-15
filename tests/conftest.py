import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def prune_environ():
    """Prevent environment variables from leaking into software tests"""
    candidates = [
        "ABOUT_CONTEXT_URL",
        "ABOUT_OUTLINE_URL",
        "OPENAI_API_KEY",
        "OUTDIR",
    ]
    for candidate in candidates:
        os.environ.pop(candidate, None)
