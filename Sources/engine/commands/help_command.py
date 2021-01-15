from typing import Optional
from .command import Command


class HelpCommand(Command):
    name = "help"
    manual = "help command"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.supported_command_help(self)
