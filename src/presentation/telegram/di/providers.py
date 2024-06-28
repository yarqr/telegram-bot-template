from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.application.common.repositories.user import UserRepository
from src.application.common.unit_of_work import UnitOfWork
from src.application.create_user.interactor import CreateUser
from src.infrastructure.config import PostgresPart
from src.infrastructure.database.repositories.user import UserRepositoryImpl
from src.infrastructure.database.unit_of_work import UnitOfWorkImpl


class DatabaseProvider(Provider):
    def __init__(self, config: PostgresPart):
        super().__init__()
        self._config = config

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(self._config.make_dsn())
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    uow = provide(UnitOfWorkImpl, scope=Scope.REQUEST, provides=UnitOfWork)
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )


class InteractorProvider(Provider):
    create_user = provide(CreateUser, scope=Scope.REQUEST)
