import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def prune_environ():
    """Prevent environment variables from leaking into software tests"""
    os.environ.pop("OUTDIR", None)
