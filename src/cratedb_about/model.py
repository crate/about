import os
import sys

import requests


class Example:
    """
    A few example questions to ask about CrateDB.
    """

    questions = [
        "What are the benefits of CrateDB?",
        "Tell me about why CrateDB is different.",
        "Tell me about CrateDB Cloud.",
        "How to use sequences with CrateDB?",
        "CrateDB does not seem to provide an AUTOINCREMENT feature?",
        "How do I apply sharding properly?",
        "How much data can CrateDB store?",
        "Please tell me how CrateDB stores data.",
        "Does CrateDB support SQLAlchemy and pandas?",
        "How to enumerate active jobs?",
        "How to enumerate elapsed jobs?",
        "How to inquire information about shards?",
        "How to inquire information about partitions?",
        "What about IoT?",
        "What about advanced operations on timeseries data?",
        "Can CrateDB store and retrieve vector data for ML workloads?",
        "What is the typical architecture of a CrateDB cluster?",
        "How much is a cluster with 3 TB storage per month?",
    ]


class Settings:
    """
    Configure the language model to support conversations about CrateDB.
    """

    default_context = (
        "CrateDB is a distributed SQL database that makes it simple to"
        "store and analyze massive amounts of data in real-time."
    )

    llms_txt_url = os.getenv(
        "CRATEDB_CONTEXT_URL",
        "https://cdn.crate.io/about/v1/llms-full.txt",
    )
    instructions = "You are a helpful and concise assistant."
    llms_txt = None
    prompt = None

    @classmethod
    def get_prompt(cls):
        if cls.llms_txt is None:
            try:
                cls.llms_txt = requests.get(cls.llms_txt_url, timeout=10).text
                cls.prompt = (
                    cls.llms_txt + "\n\nThe above is necessary context for the conversation."
                )
            except requests.RequestException as e:
                print(f"Error fetching context: {e}", file=sys.stderr)  # noqa: T201
                # Provide minimal fallback context.
                cls.llms_txt = cls.default_context
                cls.prompt = cls.llms_txt + "\n\nThe above is minimal context for the conversation."

        return cls.prompt
