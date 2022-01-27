from typing import Optional
from .command import Command


class StartCommand(Command):
    name = "start"
    manual = "start bot dialogue"

    async def execute(self) -> Optional[str]:
        await super().execute()
        available_commands = await self.context.supported_command_help(self)
        return f"Hi!!\n" \
               f"{available_commands}"
