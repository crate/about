import datetime as dt
import logging
import platform
import sqlite3
import typing as t
from collections import OrderedDict

import attr
import hishel
from attrs import define
from cattrs.preconf.json import make_converter as make_json_converter
from cattrs.preconf.pyyaml import make_converter as make_yaml_converter

from cratedb_about.settings import settings

logger = logging.getLogger()


@define
class Metadata:
    version: t.Union[float, None] = None
    type: t.Union[str, None] = None


@define
class DictTools:
    def to_dict(self) -> t.Dict[str, t.Any]:
        return attr.asdict(self, dict_factory=OrderedDict)

    @classmethod
    def from_dict(cls, data: t.Dict[str, t.Any]):
        return cls(**data)


@define
class Dumpable(DictTools):
    """
    Todo: Refactor to `pueblo.data`.
    """

    meta: t.Union[Metadata, None] = None

    def to_json(self) -> str:
        converter = make_json_converter(dict_factory=OrderedDict)
        return converter.dumps(self.to_dict())

    def to_yaml(self) -> str:
        converter = make_yaml_converter(dict_factory=OrderedDict)
        return converter.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        converter = make_json_converter(dict_factory=OrderedDict)
        return converter.loads(json_str, cls)

    @classmethod
    def from_yaml(cls, yaml_str: str):
        converter = make_yaml_converter(dict_factory=OrderedDict)
        return converter.loads(yaml_str, cls)


def get_cache_client(ttl: t.Optional[t.Union[int, float]] = settings.http_cache_ttl):
    """
    Return the configured cache client.
    https://hishel.com/
    """
    # Configure Hishel, a httpx client with caching.
    logger.info(f"Configuring cache. ttl={ttl}, path={settings.http_cache_path}")
    try:
        controller = hishel.Controller(allow_stale=True)
        storage = hishel.SQLiteStorage(
            connection=sqlite3.connect(settings.http_cache_path, check_same_thread=False),
            ttl=ttl,
        )
        return hishel.CacheClient(
            controller=controller, storage=storage, timeout=settings.http_timeout
        )
    except Exception as e:
        msg = (
            f"Failed to configure Hishel cache with SQLite. "
            f"ttl={ttl}, path={settings.http_cache_path}. Reason: {e}"
        )
        logger.exception(msg)
        raise e.__class__(msg) from e


def get_hostname() -> str:
    # https://stackoverflow.com/a/49840324
    return platform.node().split(".", 1)[0]


def get_now() -> str:
    return dt.datetime.now(tz=dt.timezone.utc).replace(microsecond=0).isoformat()
