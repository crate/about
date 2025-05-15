from pathlib import Path

import platformdirs


class Settings:
    """
    Application-wide settings bundle class.
    """

    http_timeout: float = 10.0
    http_cache_ttl: int = 3600

    @property
    def http_cache_path(self) -> Path:
        path = platformdirs.user_cache_path(appname="cratedb-about")
        path.mkdir(parents=True, exist_ok=True)
        return path / ".hishel.sqlite"


settings = Settings()
