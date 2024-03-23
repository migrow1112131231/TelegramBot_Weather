from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from handbook import handbook
from keyboards import (create_keyboard_of_contacts,
                       create_keyboard_of_week,
                       create_keyboard_distribution,
                       create_keyboard_time_for_distribution,
                       create_keyboard_distribution_on,
                       create_keyboard_distribution_off)
from logic import (send_info_about_weather,
                   _get_info_about_weather,
                   scheduler)
from database import users
from config import add_config, Config
import asyncio
import schedule

config = add_config()
router = Router()


@router.message(F.text == '/start')
async def process_command_start(message: Message):
    users[message.from_user.id] = {
        'page': 1,
    }
    await message.answer(
        text=handbook['/start'],
        parse_mode='HTML'
    )
    await asyncio.sleep(config.telegram_bot.time_for_distribution)
    if not users[message.from_user.id]['is_distribution']:
        await message.answer(
            text=handbook['add_distribution'],
            reply_markup=create_keyboard_distribution()
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
        reply_markup=create_keyboard_of_contacts()
    )


@router.message(F.text.startswith('/weather'))
async def process_command_weather(message: Message):
    if message.text == '/weather' and not users[message.from_user.id].get('city'):
        await message.answer(
            text=handbook['error_form_of_weather']
        )
    else:
        command, *city = message.text.split() if len(message.text.split()) > 1 else (
            message.text, users[message.from_user.id]['city'])
        try:
            await message.answer(
                text=send_info_about_weather(command, ' '.join(city))
            )
        except:
            await message.answer(
                text=handbook['error_weather']
            )


@router.message(F.text.startswith('/today'))
async def process_command_weather(message: Message):
    if message.text == '/today' and not users[message.from_user.id].get('city'):
        await message.answer(
            text=handbook['error_form_of_today']
        )
    else:
        command, *city = message.text.split() if len(message.text.split()) > 1 else (
            message.text, users[message.from_user.id]['city'])
        try:
            await message.answer(
                text=send_info_about_weather(command, ' '.join(city))
            )
        except:
            await message.answer(
                text=handbook['error_weather']
            )


@router.message(F.text.startswith('/tomorrow'))
async def process_command_weather(message: Message):
    if message.text == '/tomorrow' and not users[message.from_user.id].get('city'):
        await message.answer(
            text=handbook['error_form_of_tomorrow']
        )
    else:
        command, *city = message.text.split() if len(message.text.split()) > 1 else (
            message.text, users[message.from_user.id]['city'])
        try:
            await message.answer(
                text=send_info_about_weather(command, ' '.join(city))
            )
        except:
            await message.answer(
                text=handbook['error_weather']
            )


@router.message(F.text.startswith('/week'))
async def process_command_weather(message: Message):
    if message.text == '/week' and not users[message.from_user.id].get('city'):
        await message.answer(
            text=handbook['error_form_of_week']
        )
    else:
        command, *city = message.text.split() if len(message.text.split()) > 1 else (
            message.text, users[message.from_user.id]['city'])
        users[message.from_user.id]['dict'] = send_info_about_weather(
            command, ' '.join(city))
        await message.answer(
            text=handbook['week_weather'](
                users[message.from_user.id]["dict"]["city"]),
            parse_mode='HTML')
        await message.answer(
            text=users[message.from_user.id]['dict'][users[message.from_user.id]['page']],
            reply_markup=create_keyboard_of_week(
                day=users[message.from_user.id]['dict']['1_date'])
        )


@router.message(F.text == '/distribution')
async def process_command_distribution(message: Message):
    if users[message.from_user.id].get('is_distribution'):
        await message.answer(
            text=handbook['distribution_on'],
            parse_mode='HTML',
            reply_markup=create_keyboard_distribution_on()
        )
    else:
        await message.answer(
            text=handbook['distribution_off'],
            parse_mode='HTML',
            reply_markup=create_keyboard_distribution_off()
        )


@router.callback_query(F.data == 'Оставить')
async def process_press_button_stay(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == 'Отключить')
async def process_press_button_disable(callback: CallbackQuery):
    del users[callback.from_user.id]['is_distribution']
    await callback.answer(
        text=handbook['distribution_disabled'],
        show_alert=True
    )
    await callback.message.delete()


@router.callback_query(F.data == 'Подключить рассылку')
async def process_press_button_yes_enable(callback: CallbackQuery):
    users[callback.from_user.id]['is_distribution'] = True
    await callback.message.edit_text(
        text=handbook['time_for_distribution'],
        reply_markup=create_keyboard_time_for_distribution()
    )

    async def _text():
        await callback.message.answer(
            text='text'
        )

    schedule.every().day.at("17:45").do(_text)
    asyncio.create_task(scheduler())


@router.callback_query(F.data == 'Не подключать рассылку')
async def process_press_button_no_enable(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == 'backward')
async def process_press_button_backward(callback: CallbackQuery):
    if users[callback.from_user.id]['page'] == 1:
        await callback.answer()
    else:
        users[callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(
            text=users[callback.from_user.id]['dict'][
                users[callback.from_user.id]['page']],
            reply_markup=create_keyboard_of_week(
                day=users[callback.from_user.id]['dict'][f'{users[callback.from_user.id]["page"]}_date'])
        )


@router.callback_query(F.data == 'weather_page')
async def process_press_button_weather(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'forward')
async def process_press_button_forward(callback: CallbackQuery):
    if users[callback.from_user.id]['page'] >= 7:
        await callback.answer()
    else:
        users[callback.from_user.id]['page'] += 1
        await callback.message.edit_text(
            text=users[callback.from_user.id]['dict'][
                users[callback.from_user.id]['page']],
            reply_markup=create_keyboard_of_week(
                day=users[callback.from_user.id]['dict'][f'{users[callback.from_user.id]["page"]}_date']
            )
        )


@router.callback_query(F.data == 'button_no')
async def process_press_button_no_distribution(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == 'button_yes')
async def process_press_button_yes_distribution(callback: CallbackQuery):
    users[callback.from_user.id]['is_distribution'] = True
    await callback.message.edit_text(
        text=handbook['time_for_distribution'],
        reply_markup=create_keyboard_time_for_distribution()
    )


@router.callback_query(F.data.startswith('time_'))
async def process_add_time_for_distribution(callback: CallbackQuery):
    users[callback.from_user.id]['time'] = handbook[callback.data]
    await callback.message.delete()
    await callback.message.answer(
        text=handbook['message_after_settings_distribution']
    )


@router.message()
async def process_reception_messages(message: Message):
    try:
        weather = _get_info_about_weather('/weather', message.text)
        city = weather['location']['name']
        users[message.from_user.id]['city'] = city
        await message.answer(
            text=handbook['remembered_city'](city),
            parse_mode='HTML'
        )
    except:
        await message.answer(
            text=handbook['no_command']
        )
