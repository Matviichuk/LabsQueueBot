from typing import Optional
import aiogram
import bot_config
from engine import SecurityEngine, SecurityEngineDelegate, User, Cache


class Bot(object):
    class Notifier(SecurityEngineDelegate):
        def __init__(self, bot: aiogram.Bot):
            self._worker = bot

        async def notify_user(self, user: User, message: str):
            await self._worker.send_message(user.identifier, message)

    def __init__(self):
        self._bot = aiogram.Bot(bot_config.API_TOKEN)
        self._dispatcher = aiogram.Dispatcher(self._bot)
        self._executor = aiogram.executor
        self._engine = SecurityEngine()
        self._notifier = Bot.Notifier(self._bot)
        self._engine.delegate = self._notifier
        self._cache = Cache()

        self._setup_dispatched_commands()

    def _setup_dispatched_commands(self):
        async def handle_command(name: Optional, message: aiogram.types.message):
            user = self._obtain_user_from_message(message)
            raw_message = message.text
            result = await self._engine.handle_command(name, user, raw_message)
            if result is not None:
                await message.reply(result)

        for command_name in self._engine.supported_command_names():
            @self._dispatcher.message_handler(commands=[command_name])
            async def handler(message: aiogram.types.message):
                handled_command = message.text.split(" ", 1)[0]
                name = handled_command[1:]
                await handle_command(name, message)

        @self._dispatcher.message_handler()
        async def default_handler(message: aiogram.types.message):
            await handle_command(None, message)

    def _obtain_user_from_message(self, message: aiogram.types.message) -> User:
        sender = message.from_user
        sender_id = sender.id
        user = self._cache.user(sender_id)
        if user is not None:
            return user
        sender_name = sender.full_name
        sender_nickname = sender.username
        user = User(sender_id, sender_name, sender_nickname)
        self._cache.insert_user(user)
        return user

    def start_run_loop(self):
        self._executor.start_polling(self._dispatcher, skip_updates=True)
