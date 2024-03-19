from aiogram.types import BotCommand
from aiogram import Bot
from handbook import handbook_menu

async def create_keyboard_menu(bot: Bot):
    commands = [BotCommand(
        command=key,
        description=value
    ) for key, value in handbook_menu.items()]
    await bot.set_my_commands(commands)