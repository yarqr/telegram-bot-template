from abc import ABC, abstractmethod

from src.application.common.repository import Repository


class UserRepository(Repository, ABC):
    @abstractmethod
    async def exists_with_tg_id(self, tg_id: int) -> bool: ...

    @abstractmethod
    async def create(self, tg_id: int) -> None: ...
