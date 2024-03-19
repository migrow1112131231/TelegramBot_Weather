from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from handbook import handbook
from keyboards import create_keyboard_of_contacts
from logic import send_info_about_weather


router = Router()


@router.message(F.text == '/start')
async def process_command_start(message: Message):
    await message.answer(
        text=handbook['/start'],
        parse_mode='HTML'
    )


@router.message(F.text == '/help')
async def process_command_help(message: Message):
    await message.answer(
        text=handbook['/help'],
        parse_mode='HTML'
    )


@router.message(F.text == '/info')
async def process_command_info(message: Message):
    await message.answer(
        text=handbook['/info'],
        parse_mode='HTML'
    )


@router.message(F.text == '/contacts')
async def process_command_contacts(message: Message):
    await message.answer(
        text=handbook['/contacts'],
        parse_mode='HTML',
        reply_markup=create_keyboard_of_contacts()
    )


@router.message(F.text.startswith('/weather'))
async def process_command_weather(message: Message):
    if message.text == '/weather':
        await message.answer(
            text=handbook['error_form_of_weather']
        )
    else:
        city = message.text.split()[1]
        try:
            await message.answer(
                text=send_info_about_weather(city=city)
            )
        except:
            await message.answer(
                text=handbook['error_weather']
            )
