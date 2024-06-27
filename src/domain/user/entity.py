from dataclasses import dataclass

from src.domain.common.entity import Entity


@dataclass(kw_only=True)
class User(Entity):
    tg_id: int
