from abc import ABC
from typing import Optional
from .registration_command import RegistrationCommand
from .unregistration_command import UnregistrationCommand
from .ask_command import AskCommand
from .start_notify_queue_change_command import StartNotifyQueueChangeCommand
from .stop_notify_queue_change_command import StopNotifyQueueChangeCommand
from .allocate_room_command import AllocateRoomCommand
from .close_room_command import CloseRoomCommand
from .kick_deliverer_command import KickDelivererCommand
from .review_list_command import ReviewListCommand

class Context(ABC):
    async def register_for_delivery(self, cmd: RegistrationCommand) -> Optional[str]:
        pass

    async def unregister_from_delivery(self, cmd: UnregistrationCommand) -> Optional[str]:
        pass

    async def supported_command_help(self, cmd) -> Optional[str]:
        pass

    async def ask(self, cmd: AskCommand) -> Optional[str]:
        pass

    async def start_notify_about_moving_in_queue(self, cmd: StartNotifyQueueChangeCommand):
        pass

    async def stop_notifying_about_moving_in_queue(self, cmd: StopNotifyQueueChangeCommand):
        pass

    async def allocate_room(self, cmd: AllocateRoomCommand):
        pass

    async def close_room(self, cmd: CloseRoomCommand):
        pass

    async def kick_deliverer(self, cmd: KickDelivererCommand):
        pass

    async def review_list(self, cmd: ReviewListCommand):
        pass
