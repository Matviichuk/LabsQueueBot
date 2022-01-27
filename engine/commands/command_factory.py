from .command import Command
from .commands_list import *


class CommandFactory:
    build_classes = \
        {
            StartCommand.name: StartCommand,
            RegistrationCommand.name: RegistrationCommand,
            UnregistrationCommand.name: UnregistrationCommand,
            UnavailableCommand.name: UnavailableCommand,
            HelpCommand.name: HelpCommand,
            AskCommand.name: AskCommand,
            StartNotifyQueueChangeCommand.name: StartNotifyQueueChangeCommand,
            StopNotifyQueueChangeCommand.name: StopNotifyQueueChangeCommand,
            AllocateRoomCommand.name: AllocateRoomCommand,
            CloseRoomCommand.name: CloseRoomCommand,
            KickDelivererCommand.name: KickDelivererCommand,
            ReviewListCommand.name: ReviewListCommand,
        }

    @staticmethod
    def build_command_with_(command_name: str, user, message: str, context) -> Command:
        if command_name not in CommandFactory.build_classes:
            command_name = UnavailableCommand.name
        return CommandFactory.build_classes[command_name](user, message, context)
