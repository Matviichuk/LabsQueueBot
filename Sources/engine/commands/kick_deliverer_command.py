from typing import Optional
from .command import Command


class KickDelivererCommand(Command):
    name = "next"
    manual = "kick deliverer from room and invite next"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.kick_deliverer(self)
