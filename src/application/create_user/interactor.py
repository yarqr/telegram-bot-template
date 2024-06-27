from dataclasses import dataclass

from src.application.common.interactor import Interactor
from src.application.common.repositories.user import UserRepository
from src.application.common.unit_of_work import UnitOfWork


@dataclass(kw_only=True)
class CreateUserInput:
    tg_id: int


class CreateUser(Interactor[CreateUserInput, bool]):
    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, data: CreateUserInput) -> bool:
        if await self.user_repo.exists_with_tg_id(data.tg_id):
            return False
        await self.user_repo.create(data.tg_id)
        return True
