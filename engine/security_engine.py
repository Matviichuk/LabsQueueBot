from abc import ABC
from typing import List, Optional
from .user import User
from .privilege_controller import PrivilegeController
from .commands import CommandFactory, UnavailableCommand
from .command_context_executor import CommandContextExecutor, CommandContextExecutorDelegate


class SecurityEngineDelegate(ABC):
    async def notify_user(self, user: User, message: str):
        pass


class SecurityEngine:
    class PrivilegedListInfoDelegate(CommandContextExecutorDelegate):
        def __init__(self, privilege_controller: PrivilegeController, notification_provider: SecurityEngineDelegate):
            self._controller = privilege_controller
            self._notification_provider = notification_provider

        def available_commands_for_user(self, user: User):
            user_policy = self._controller.policy_for_user(user)
            return self._controller.supported_commands_for_policy(user_policy)

        async def notify_user(self, user: User, msg: str):
            await self.notification_provider.notify_user(user, msg)

        @property
        def notification_provider(self) -> SecurityEngineDelegate:
            return self._notification_provider

        @notification_provider.setter
        def notification_provider(self, value):
            self._notification_provider = value

    def __init__(self):
        self._privilege_controller = PrivilegeController()
        self._factory = CommandFactory()
        self._executor = CommandContextExecutor()
        self._utils = SecurityEngine.PrivilegedListInfoDelegate(self._privilege_controller, None)
        self._executor.delegate = self._utils
        self._delegate = None

    @property
    def delegate(self) -> Optional[SecurityEngineDelegate]:
        return self._delegate

    @delegate.setter
    def delegate(self, value: Optional[SecurityEngineDelegate]):
        self._delegate = value
        self._utils.notification_provider = value

    async def handle_command(self, command_identifier: str, user: User, message: str) -> Optional[str]:
        user_policy = self._privilege_controller.policy_for_user(user)
        allowed_commands = self._privilege_controller.supported_commands_for_policy(user_policy)
        allowed_identifiers = map(lambda value: value.name, allowed_commands)
        if command_identifier not in allowed_identifiers:
            command_identifier = UnavailableCommand.name
        command = self._factory.build_command_with_(command_identifier, user, message, self._executor)
        return await command.execute()

    def supported_command_names(self) -> List[str]:
        commands = self._privilege_controller.supported_commands()
        return list(map(lambda value: value.name, commands))
