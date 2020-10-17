from utils import DEFAULT_STORAGE
from bot_shared import DISPATCHER
from aiogram import executor
import bot_command_handlers

if __name__ == '__main__':
    executor.start_polling(DISPATCHER, skip_updates=True)
