import asyncio
import logging
from typing import cast

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from dishka import FromDishka, make_async_container
from dishka.integrations.aiogram import inject, setup_dishka

from src.application.create_user.interactor import CreateUser, CreateUserInput
from src.infrastructure.config import load_telegram_config
from src.presentation.telegram.di.providers import DatabaseProvider, InteractorProvider
from src.presentation.telegram.start.dialog import start
from src.presentation.telegram.states import StartSG

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)


@inject  # type: ignore[misc]
async def cmd_start(
    msg: Message,
    dialog_manager: DialogManager,
    create_user_uc: FromDishka[CreateUser],
) -> None:
    await create_user_uc(CreateUserInput(tg_id=cast(types.User, msg.from_user).id))
    await dialog_manager.start(StartSG.main, mode=StartMode.RESET_STACK)


async def main() -> None:
    config = load_telegram_config()

    bot = Bot(config.telegram.bot_token)
    storage = RedisStorage.from_url(
        config.redis.make_dsn(), key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    dp = Dispatcher(storage=storage, events_isolation=storage.create_isolation())

    dp.message.register(cmd_start, CommandStart())
    dp.message.filter(F.chat.type == ChatType.PRIVATE)

    dp.include_routers(start)
    setup_dialogs(dp)

    setup_dishka(
        make_async_container(DatabaseProvider(config.postgres), InteractorProvider()),
        dp,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
