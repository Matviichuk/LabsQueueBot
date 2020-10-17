from bot_config import API_TOKEN
from aiogram import Bot, Dispatcher

assert API_TOKEN, "Api token is not defined"

# Initialize bot and dispatcher
BOT = Bot(token=API_TOKEN)
DISPATCHER = Dispatcher(BOT)
