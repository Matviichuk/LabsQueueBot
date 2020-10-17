from utils import DEFAULT_STORAGE
from bot_shared import DISPATCHER
from aiogram import executor
import bot_command_handlers

# DEFAULT_STORAGE.register_privileged_user_with_id(374760184)
# DEFAULT_STORAGE.register_privileged_user_with_id(152433470)

if __name__ == '__main__':
    executor.start_polling(DISPATCHER, skip_updates=True)