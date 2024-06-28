from typing import cast

from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.repositories.user import UserRepository
from src.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists_with_tg_id(self, tg_id: int) -> bool:
        return cast(
            bool,
            await self.session.scalar(
                exists().where(UserModel.tg_id == tg_id).select()
            ),
        )

    async def create(self, tg_id: int) -> None:
        self.session.add(UserModel(tg_id=tg_id))
