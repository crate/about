import logging
import os
import typing as t
from pathlib import Path

from cratedb_about.settings import settings
from cratedb_about.util import get_cache_client

logger = logging.getLogger(__name__)


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
        '''Optimize this query: "SELECT * FROM movies WHERE release_date > '2012-12-1' AND revenue"''',  # noqa: E501
        "Tell me about the health of the cluster.",
        "What is the storage consumption of my tables, give it in a graph.",
        "How can I format a timestamp column to '2019 Jan 21'?",
        "Please tell me about integrations with CrateDB.",
        "How do I use SQLAlchemy with CrateDB?",
        "How do I use pandas with CrateDB?",
        "How do I optimally synchronize data between MongoDB and CrateDB?",
    ]


class KnowledgeContextLoader:
    """
    Load enhanced context (prompt payload) for improved conversations about a topic.
    """

    # Configure content for context (prompt payload).
    context_url: t.Optional[str] = None
    fallback_context: str = ""
    instructions = "You are a helpful and concise assistant."

    # Configure default cache lifetime to one hour.
    default_cache_ttl: int = settings.http_cache_ttl

    def __init__(self):
        self.http_client = get_cache_client(ttl=self.cache_ttl)

    @property
    def url(self) -> str:
        """
        Provide URL to context file.
        """
        url = os.getenv("ABOUT_CONTEXT_URL", self.context_url)
        if not url:
            raise ValueError(
                "Unable to operate without context URL. "
                "Please check `ABOUT_CONTEXT_URL` environment variable."
            )
        return url

    @property
    def cache_ttl(self) -> int:
        """
        Return configured cache lifetime in seconds.
        """
        try:
            ttl = int(os.getenv("ABOUT_CACHE_TTL", self.default_cache_ttl))
            if ttl <= 0:
                raise ValueError("Cache TTL must be positive")
            return ttl
        except ValueError as e:
            raise ValueError(f"Environment variable `ABOUT_CACHE_TTL` invalid: {e}") from e

    def fetch(self) -> str:
        """
        Retrieve payload of context file.

        TODO: Add third option `pueblo.to_io`, to load resources from anywhere.
              See `cratedb_about.outline.core`.
        """
        url = self.url
        path = Path(url)
        # Normalize path for cross-platform compatibility.
        path = path.expanduser().resolve()
        if path.exists() and path.is_file():
            return path.read_text()
        if url.startswith("http"):
            response = self.http_client.get(url)
            # Raise HTTPError for bad responses.
            response.raise_for_status()
            return response.text
        raise NotImplementedError(f"Unable to load context file. Source: {url}")

    def get_prompt(self) -> str:
        """
        Assemble and return prompt payload.

        Provide minimal fallback context when topic domain knowledge can not be acquired.
        """
        try:
            payload = self.fetch()
            return payload + "\n\nThe above is necessary context for the conversation."
        except Exception:
            logger.exception(f"Fetching context failed. Source: {self.url}")
            return self.fallback_context + "\n\nThe above is minimal context for the conversation."


class CrateDbKnowledgeContextLoader(KnowledgeContextLoader):
    """
    Configure the language model to support conversations about CrateDB.
    """

    # Configure content for context (prompt payload).
    context_url = "https://cdn.crate.io/about/v1/llms-full.txt"
    fallback_context = (
        "CrateDB is a distributed SQL database that makes it simple to"
        "store and analyze massive amounts of data in real-time."
    )
