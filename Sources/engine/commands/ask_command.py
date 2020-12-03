from typing import Optional
from .command import Command


class AskCommand(Command):
    name = "ask"
    manual = "ask question"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.ask(self)
