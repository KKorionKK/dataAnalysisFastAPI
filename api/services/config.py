from dataclasses import dataclass
from dotenv import find_dotenv, dotenv_values
from functools import cache


@dataclass
class BaseConfig:
    DB_NAME: str
    PG_USER: str
    PG_PASSWORD: str
    DB_ADAPTER: str
    DB_HOST: str
    DB_PORT: str


@cache
def get_settings() -> BaseConfig:
    settings = dotenv_values(find_dotenv())
    return BaseConfig(**settings)


def get_connection_string() -> str:
    s = get_settings()
    return f"{s.DB_ADAPTER}://{s.PG_USER}:{s.PG_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"
