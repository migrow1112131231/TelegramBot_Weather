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

def create_keyboard_of_week(day):
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(
        text=handbook['backward'],
        callback_data='backward'
    ),
    InlineKeyboardButton(
        text=day,
        callback_data='weather_page'
    ),
    InlineKeyboardButton(
        text=handbook['forward'],
        callback_data='forward'
    )]
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()

def create_keyboard_distribution():
    kb_builder = InlineKeyboardBuilder()
    button_no = InlineKeyboardButton(
        text=handbook['button_no'],
        callback_data='button_no'
    )
    button_yes = InlineKeyboardButton(
        text=handbook['button_yes'],
        callback_data='button_yes'
    )
    kb_builder.row(button_yes, button_no, width=2)
    return kb_builder.as_markup()

def create_keyboard_time_for_distribution():
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(
        text=handbook[f'time_{num}'],
        callback_data=f'time_{num}'
    ) for num in range(7,10)]
    buttons.extend([InlineKeyboardButton(
        text=handbook[f'time_{n}'],
        callback_data=f'time_{n}'
    ) for n in range(20, 23)])
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

def create_keyboard_distribution_on():
    kb_builder = InlineKeyboardBuilder()
    button_stay = InlineKeyboardButton(
        text='Оставить',
        callback_data='Оставить'
    )
    button_disable = InlineKeyboardButton(
        text='Отключить',
        callback_data='Отключить'
    )
    kb_builder.row(button_stay, button_disable, width=2)
    return kb_builder.as_markup()

def create_keyboard_distribution_off():
    kb_builder = InlineKeyboardBuilder()
    button_no_enable = InlineKeyboardButton(
        text='Не подключать рассылку',
        callback_data='Не подключать рассылку'
    )
    button_yes_enable = InlineKeyboardButton(
        text='Подключить рассылку',
        callback_data='Подключить рассылку'
    )
    kb_builder.row(button_yes_enable, button_no_enable, width=2)
    return kb_builder.as_markup()