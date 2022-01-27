from typing import Optional
from .command import Command


class StopNotifyQueueChangeCommand(Command):
    name = "unsubscribe"
    manual = "unsubscribe from notifications about moving in queue"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.stop_notifying_about_moving_in_queue(self)
