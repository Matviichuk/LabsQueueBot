from abc import ABC
from typing import Optional


class Command(ABC):
    name: str
    manual: str

    def __init__(self, user, message: str, context):
        self._user = user
        self._message = message
        self._context = context

    async def execute(self) -> Optional[str]:
        return None

    @property
    def user(self):
        return self._user

    @property
    def message(self) -> str:
        return self._message

    @property
    def context(self):
        return self._context
