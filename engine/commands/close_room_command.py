from typing import Optional
from .command import Command


class CloseRoomCommand(Command):
    name = "close"
    manual = "close exist room for delivery lab"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.close_room(self)
