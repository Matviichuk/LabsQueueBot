from .command import Command
from typing import Optional


class UnregistrationCommand(Command):
    name = "unregister"
    manual = "unregistration from delivery lab"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self._context.unregister_from_delivery(self)
