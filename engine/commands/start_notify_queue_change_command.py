from typing import Optional
from .command import Command


class StartNotifyQueueChangeCommand(Command):
    name = "subscribe"
    manual = "subscribe to notifying about moving in queue"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.start_notify_about_moving_in_queue(self)
