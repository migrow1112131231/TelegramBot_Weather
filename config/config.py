from environs import Env
from dataclasses import dataclass

@dataclass
class TelegramBot:
    token: str
    admin: int
    weather_api_key: str
    time_for_distribution: int

@dataclass
class Contacts:
    vk: str
    telegram: str

@dataclass
class Config:
    telegram_bot: TelegramBot
    contacts: Contacts

def add_config():
    env = Env()
    env.read_env()

    return Config(
        telegram_bot=TelegramBot(
            token=env('BOT_TOKEN'),
            admin=env.int('ADMIN'),
            weather_api_key=env('WEATHER_API_KEY'),
            time_for_distribution=env.int('TIME_FOR_DISTRIBUTION')
        ),
        contacts=Contacts(
            vk=env('VK'),
            telegram=env('TELEGRAM')
        )
    )