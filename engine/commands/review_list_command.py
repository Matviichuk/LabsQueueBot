from typing import Optional
from .command import Command


class ReviewListCommand(Command):
    name = "list"
    manual = "show pending queue"

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.review_list(self)
