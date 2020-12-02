from typing import Optional
from .command import Command
from .utils import Url


def _parse_room_url(msg: str) -> Optional[Url]:
    command_name_len = len(AllocateRoomCommand.name)
    args = msg[command_name_len + 1:]
    try:
        return Url(args)
    except ValueError:
        return None


class AllocateRoomCommand(Command):
    name = "allocate"
    manual = "use for allocate new room at url"

    def __init__(self, user, message: str, context):
        super().__init__(user, message, context)
        self._location = _parse_room_url(message)

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.allocate_room(self)

    @property
    def location(self) -> Optional[Url]:
        return self._location
