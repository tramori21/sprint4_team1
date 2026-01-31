import os
from functools import lru_cache


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value


PROJECT_NAME = _get_env("PROJECT_NAME", "Async API")

SECRET_KEY = _get_env("SECRET_KEY")

ALLOWED_HOSTS = [
    host.strip()
    for host in _get_env("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

API_HOST = _get_env("API_HOST", "0.0.0.0")
API_PORT = int(_get_env("API_PORT", "8000"))

POSTGRES_DB = _get_env("POSTGRES_DB")
POSTGRES_USER = _get_env("POSTGRES_USER")
POSTGRES_PASSWORD = _get_env("POSTGRES_PASSWORD")
POSTGRES_HOST = _get_env("POSTGRES_HOST")
POSTGRES_PORT = int(_get_env("POSTGRES_PORT", "5432"))

POSTGRES_DSN = (
    f"dbname={POSTGRES_DB} "
    f"user={POSTGRES_USER} "
    f"password={POSTGRES_PASSWORD} "
    f"host={POSTGRES_HOST} "
    f"port={POSTGRES_PORT}"
)

ES_HOST = _get_env("ES_HOST")
ES_PORT = int(_get_env("ES_PORT", "9200"))
ES_SCHEMA = _get_env("ES_SCHEMA", "http://")

REDIS_HOST = _get_env("REDIS_HOST")
REDIS_PORT = int(_get_env("REDIS_PORT", "6379"))
CACHE_EXPIRE_SECONDS = int(_get_env("CACHE_EXPIRE_SECONDS", "300"))

ETL_POLL_SECONDS = int(_get_env("ETL_POLL_SECONDS", "10"))
ETL_BATCH_SIZE = int(_get_env("ETL_BATCH_SIZE", "100"))
STATE_PATH = _get_env("STATE_PATH", "/state/state.json")
