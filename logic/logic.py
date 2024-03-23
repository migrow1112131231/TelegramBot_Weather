import requests
from config import Config, add_config
from handbook import handbook
import schedule
import time
import asyncio

config = add_config()


def _get_info_about_weather(command: str, city: str) -> str:
    if command == '/weather':
        url = f"http://api.weatherapi.com/v1/current.json?key={config.telegram_bot.weather_api_key}&q={city}"
    elif command == '/today':
        url = f"http://api.weatherapi.com/v1/forecast.json?key={config.telegram_bot.weather_api_key}&q={city}&days=1"
    elif command == '/tomorrow':
        url = f"http://api.weatherapi.com/v1/forecast.json?key={config.telegram_bot.weather_api_key}&q={city}&days=2"
    elif command == '/week':
        url = f"http://api.weatherapi.com/v1/forecast.json?key={config.telegram_bot.weather_api_key}&q={city}&days=8"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error', response.status_code)
        return


def _formation_message_about_weather_now(weather: str) -> str:
    city = weather['location']['name']
    time = weather['location']['localtime']
    temp_c = weather['current']['temp_c']
    feelslike_c = weather['current']['feelslike_c']
    precip_mm = weather['current']['precip_mm']
    return handbook['formation_message_about_weather_now'](
        city, time, temp_c, feelslike_c, precip_mm
    )


def _formation_message_about_weather_today(weather: str, command: str = '/today') -> str:
    n = 0 if command == '/today' else 1
    city = weather['location']['name']
    day = weather['forecast']['forecastday'][n]['date']
    mintemp_c = weather['forecast']['forecastday'][n]['day']['mintemp_c']
    maxtemp_c = weather['forecast']['forecastday'][n]['day']['maxtemp_c']
    avgtemp_c = weather['forecast']['forecastday'][n]['day']['avgtemp_c']
    totalprecip_mm = weather['forecast']['forecastday'][n]['day']['totalprecip_mm']
    return handbook['formation_message_about_weather_today'](
        city, day, mintemp_c, maxtemp_c,
        avgtemp_c, totalprecip_mm)


def _formation_message_about_weather_week(weather: str) -> dict:
    city = weather['location']['name']
    # Определяем форматированное сообщение для каждого дня недели
    message_for_day_1 = handbook['for_week'](
        weather['forecast']['forecastday'][1]['day']['mintemp_c'],
        weather['forecast']['forecastday'][1]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][1]['day']['totalprecip_mm']
    )
    message_for_day_2 = handbook['for_week'](
        weather['forecast']['forecastday'][2]['day']['mintemp_c'],
        weather['forecast']['forecastday'][2]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][2]['day']['totalprecip_mm']
    )
    message_for_day_3 = handbook['for_week'](
        weather['forecast']['forecastday'][3]['day']['mintemp_c'],
        weather['forecast']['forecastday'][3]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][3]['day']['totalprecip_mm']
    )
    message_for_day_4 = handbook['for_week'](
        weather['forecast']['forecastday'][4]['day']['mintemp_c'],
        weather['forecast']['forecastday'][4]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][4]['day']['totalprecip_mm']
    )
    message_for_day_5 = handbook['for_week'](
        weather['forecast']['forecastday'][5]['day']['mintemp_c'],
        weather['forecast']['forecastday'][5]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][5]['day']['totalprecip_mm']
    )
    message_for_day_6 = handbook['for_week'](
        weather['forecast']['forecastday'][6]['day']['mintemp_c'],
        weather['forecast']['forecastday'][6]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][6]['day']['totalprecip_mm']
    )
    message_for_day_7 = handbook['for_week'](
        weather['forecast']['forecastday'][7]['day']['mintemp_c'],
        weather['forecast']['forecastday'][7]['day']['maxtemp_c'],
        weather['forecast']['forecastday'][7]['day']['totalprecip_mm']
    )

    return {
        'city': city,
        1: message_for_day_1,
        '1_date': weather['forecast']['forecastday'][1]['date'],
        2: message_for_day_2,
        '2_date': weather['forecast']['forecastday'][2]['date'],
        3: message_for_day_3,
        '3_date': weather['forecast']['forecastday'][3]['date'],
        4: message_for_day_4,
        '4_date': weather['forecast']['forecastday'][4]['date'],
        5: message_for_day_5,
        '5_date': weather['forecast']['forecastday'][5]['date'],
        6: message_for_day_6,
        '6_date': weather['forecast']['forecastday'][6]['date'],
        7: message_for_day_7,
        '7_date': weather['forecast']['forecastday'][7]['date'],
    }


def send_info_about_weather(command: str, city: str) -> str:
    weather = _get_info_about_weather(command, city)
    if command == '/weather':
        result = _formation_message_about_weather_now(weather)
    elif command == '/today':
        result = _formation_message_about_weather_today(weather)
    elif command == '/tomorrow':
        result = _formation_message_about_weather_today(weather, command)
    elif command == '/week':
        result = _formation_message_about_weather_week(weather)

    return result

async def scheduler():
    while True:
        # Проверяем расписание и выполняем запланированные задачи
        schedule.run_pending()
        await asyncio.sleep(60)  # Ждем 60 секунд перед следующей проверкой расписания
