from importlib.metadata import PackageNotFoundError, version

from .outline import CrateDbKnowledgeOutline
from .query import CrateDbKnowledgeConversation

__all__ = [
    "CrateDbKnowledgeConversation",
    "CrateDbKnowledgeOutline",
]

__appname__ = "cratedb-about"

try:
    __version__ = version(__appname__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
