import hishel
import pytest

from cratedb_about.util import get_cache_client


def test_get_cache_client_valid():
    client = get_cache_client()
    assert isinstance(client, hishel.CacheClient)


def test_get_cache_client_failure(mocker, caplog):
    def _raise(*_args, **_kwargs):
        raise Exception("Test error")

    mocker.patch.object(hishel.CacheClient, "__init__", _raise)
    with pytest.raises(Exception) as excinfo:
        get_cache_client()
    assert excinfo.match("Test error")
    assert excinfo.match("Failed to configure Hishel cache with SQLite")
    assert "Failed to configure Hishel cache with SQLite" in caplog.text
