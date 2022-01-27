from typing import Optional
from .command import Command


class UnavailableCommand(Command):
    name = "unavailable"
    manual = "this is unavailable command"

    async def execute(self) -> Optional[str]:
        await super().execute()
        is_command = self.message and self.message[0] == '/'
        key_word: str
        if is_command:
            key_word = self.message.split(' ', 1)[0]
        else:
            key_word = "messaging"
        help_message = await self.context.supported_command_help(self)
        return f"{key_word} is not available\n" \
               f"use command from list:\n" \
               f"{help_message}"
