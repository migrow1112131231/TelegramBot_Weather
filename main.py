import asyncio
import logging
from config import add_config, Config
from aiogram import Dispatcher, Bot
from keyboards import create_keyboard_menu
from handlers import user_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config: Config = add_config()
    dp = Dispatcher()
    bot = Bot(token=config.telegram_bot.token)

    dp.include_router(user_handlers.router)
    dp.startup.register(create_keyboard_menu)

    # удаляем все прошлые апдейты, так как у нас тестовый бот,
    await bot.delete_webhook(drop_pending_updates=True)
    # нам не нужно обрабатывать прошлые апдейты
    await dp.start_polling(bot)

asyncio.run(main())
