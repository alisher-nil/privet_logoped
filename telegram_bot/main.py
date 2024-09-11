import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

import config
from constants import MENU_REFRESH_INTERVAL, RESPONSE_CHECK_INTERVAL
from middlewares.scheduler import SchedulerMiddleware
from middlewares.old_menu import CheckOldMenuMiddleware
from tasks import refresh_main_menu, send_answers_to_users
from handlers import (
    router,
)


async def bot_setup(dp: Dispatcher, bot: Bot):
    await refresh_main_menu()

    scheduler = AsyncIOScheduler(timezone=config.BOT_TIMEZONE)
    scheduler = ContextSchedulerDecorator(scheduler)
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    router.callback_query.middleware(CheckOldMenuMiddleware())
    scheduler.start()
    scheduler.add_job(
        send_answers_to_users,
        "interval",
        seconds=RESPONSE_CHECK_INTERVAL,
    )
    scheduler.add_job(
        refresh_main_menu,
        "interval",
        seconds=MENU_REFRESH_INTERVAL,
    )


async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)
    await bot_setup(dp=dp, bot=bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
