from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class PostgresConfig:
    host: str = getenv('PG_HOST', 'postgres')
    port: int = int(getenv('PG_PORT', '5432'))
    db: str = getenv('PG_DB', 'movies')
    user: str = getenv('PG_USER', 'app')
    password: str = getenv('PG_PASSWORD', 'app')


@dataclass(frozen=True)
class ElasticsearchConfig:
    host: str = getenv('ES_HOST', 'elasticsearch')
    port: int = int(getenv('ES_PORT', '9200'))


@dataclass(frozen=True)
class EtlConfig:
    poll_seconds: int = int(getenv('ETL_POLL_SECONDS', '10'))
    batch_size: int = int(getenv('ETL_BATCH_SIZE', '100'))
    state_path: str = getenv('STATE_PATH', '/state/state.json')


PG = PostgresConfig()
ES = ElasticsearchConfig()
ETL = EtlConfig()
