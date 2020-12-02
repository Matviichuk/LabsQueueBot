from abc import ABC
from typing import List, Type, Optional
from .commands import *
from .user import User
from .meetings_scheduler import MeetingsScheduler, MeetingsSchedulerDelegate


class CommandContextExecutorDelegate(ABC):
    def available_commands_for_user(self, user: User) -> List[Type[Command]]:
        pass

    async def notify_user(self, user: User, msg: str):
        pass


class CommandContextExecutor(Context):
    class SchedulerDelegate(MeetingsSchedulerDelegate):
        def __init__(self, delegate: CommandContextExecutorDelegate):
            super().__init__()
            self._delegate = delegate

        async def notify(self, user: User, msg: str):
            await self.delegate.notify_user(user, msg)

        @property
        def delegate(self) -> CommandContextExecutorDelegate:
            return self._delegate

        @delegate.setter
        def delegate(self, value):
            self._delegate = value

    def __init__(self):
        super().__init__()
        self._scheduler = MeetingsScheduler()
        self._delegate = None
        self._scheduler_utils = CommandContextExecutor.SchedulerDelegate(self.delegate)
        self.scheduler.delegate = self._scheduler_utils

    @property
    def delegate(self) -> Optional[CommandContextExecutorDelegate]:
        return self._delegate

    @delegate.setter
    def delegate(self, value):
        self._delegate = value
        self._scheduler_utils.delegate = value

    @property
    def scheduler(self) -> MeetingsScheduler:
        return self._scheduler

    async def register_for_delivery(self, cmd: RegistrationCommand) -> Optional[str]:
        result = await self.scheduler.insert_deliverer(cmd.user)
        if result is not None:
            return f"Queue number {result}"
        # You find free room, room send invite
        return None

    async def unregister_from_delivery(self, cmd: UnregistrationCommand) -> Optional[str]:
        observer = await self.scheduler.remove_queue_observer(cmd.user)
        exist = await self.scheduler.remove_deliverer(cmd.user)
        if exist:
            if observer:
                return "Successfully unsubscribed and unregistered"
            else:
                return "Successfully unregistered"
        else:
            return "You not in queue"

    async def supported_command_help(self, cmd: Command) -> Optional[str]:
        if self.delegate is None:
            return None
        commands = self.delegate.available_commands_for_user(cmd.user)
        result = ""
        for c in commands:
            result += f"/{c.name} - {c.manual}\n"
        return result

    async def ask(self, cmd: AskCommand) -> Optional[str]:
        # TODO implement review list
        return "TODO: not implemented"

    async def start_notify_about_moving_in_queue(self, cmd: StartNotifyQueueChangeCommand):
        if await self.scheduler.insert_queue_observer(cmd.user):
            return "Successfully subscribed"
        return "Can`t subscribe, /register to queue before use"

    async def stop_notifying_about_moving_in_queue(self, cmd: StopNotifyQueueChangeCommand):
        if await self.scheduler.remove_queue_observer(cmd.user):
            return "Successfully unsubscribed"
        return "You not observe queue now"
