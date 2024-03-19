from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from handbook import handbook
from config import Config, add_config

config = add_config()

def create_keyboard_of_contacts():
    kb_builder = InlineKeyboardBuilder()
    button_vk = InlineKeyboardButton(
        text=handbook['button_vk'],
        url=config.contacts.vk
    )
    button_telegram = InlineKeyboardButton(
        text=handbook['button_telegram'],
        url=config.contacts.telegram
    )
    kb_builder.row(button_vk, button_telegram, width=1)

    return kb_builder.as_markup()