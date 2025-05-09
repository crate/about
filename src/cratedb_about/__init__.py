from importlib.metadata import PackageNotFoundError, version

from .outline import CrateDbKnowledgeOutline

__all__ = [
    "CrateDbKnowledgeOutline",
]

__appname__ = "cratedb-about"

try:
    __version__ = version(__appname__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
