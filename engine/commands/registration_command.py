from typing import Optional
from .command import Command


def _parse_lab_number(message: str) -> Optional[int]:
    command_name_len = len(RegistrationCommand.name)
    command_part = message.find(RegistrationCommand.name) + command_name_len
    tail = message[command_part:]
    try:
        return int(tail)
    except ValueError:
        return None


class RegistrationCommand(Command):
    name = "register"
    manual = "registration for delivery lab"

    def __init__(self, user, message: str, context):
        super().__init__(user, message, context)
        self._lab_number = _parse_lab_number(message)

    async def execute(self) -> Optional[str]:
        await super().execute()
        return await self.context.register_for_delivery(self)

    @property
    def lab_number(self) -> Optional[int]:
        return self._lab_number
