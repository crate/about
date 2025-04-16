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
    ]


class Settings:
    """
    Configure the language model to support conversations about CrateDB.
    """

    llms_txt_url = "https://raw.githubusercontent.com/crate/about/6876fedee57f59b693f37996e04f53c6446f2ad6/build/llm/llms-ctx.txt"
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
        return cls.prompt
