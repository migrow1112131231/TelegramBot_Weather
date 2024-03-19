import requests
from config import Config, add_config

config = add_config()


def _get_info_about_weather(city: str):
    url = f"http://api.weatherapi.com/v1/current.json?key={config.telegram_bot.weather_api_key}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error', response.status_code)
        return


def send_info_about_weather(city: str) -> str:
    weather = _get_info_about_weather(city=city)
    city = weather['location']['name']
    time = weather['location']['localtime']
    temp_c = weather['current']['temp_c']
    feelslike_c = weather['current']['feelslike_c']
    precip_mm = weather['current']['precip_mm']
    text = f'''🏙️ Город {city}
🕓 Время {time}
🌡️ Температура {int(temp_c)} градусов
💁‍♀️ Ощущается как {feelslike_c} градусов
🌧️ Количество осадков за последний час {precip_mm} мм'''

    return text
