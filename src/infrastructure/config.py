from dataclasses import asdict, dataclass
from typing import Any, Optional, TypeVar

from adaptix import NameStyle, Retort, name_mapping
from dynaconf import Dynaconf  # type: ignore[import-untyped]
from sqlalchemy import URL

Config = TypeVar("Config")


@dataclass
class RedisPart:
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[int] = 0

    def make_dsn(self) -> str:
        data = asdict(self)
        data["database"] = str(self.database)
        return URL.create("redis", **data).render_as_string(hide_password=False)


@dataclass
class PostgresPart:
    host: str
    port: int
    database: str
    username: Optional[str] = None
    password: Optional[str] = None

    def make_dsn(self) -> str:
        return URL.create("postgresql+asyncpg", **asdict(self)).render_as_string(
            hide_password=False
        )


@dataclass
class TelegramPart:
    bot_token: str


@dataclass
class MigrationsConfig:
    postgres: PostgresPart


@dataclass
class TelegramConfig:
    redis: RedisPart
    postgres: PostgresPart
    telegram: TelegramPart


def _load_data() -> dict[str, Any]:
    return Dynaconf(environments=True, load_dotenv=True).as_dict()  # type: ignore[no-any-return]


def _load_config(config: type[Config]) -> Config:
    return Retort(recipe=[name_mapping(config, name_style=NameStyle.UPPER)]).load(
        _load_data(), config
    )


def load_migrations_config() -> MigrationsConfig:
    return _load_config(MigrationsConfig)


def load_telegram_config() -> TelegramConfig:
    return _load_config(TelegramConfig)
