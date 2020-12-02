from typing import List, Type
from .policies import Policy, UserPolicy, LecturerPolicy, PolicyIdentifier
from .user import User
from . import privileges_config
from . import commands as cmd


class PrivilegeController(object):
    def policy_for_user(self, user: User) -> Policy:
        # TODO move to own storage
        if user.identifier in privileges_config.PRIVILEGED_USERS:
            return LecturerPolicy()
        return UserPolicy()

    @staticmethod
    def supported_commands() -> List[Type[cmd.Command]]:
        commands = set()
        for identifier in PolicyIdentifier:
            policy = Policy.policy_with_identifier(identifier)
            policy_commands = PrivilegeController.supported_commands_for_policy(policy)
            commands.update(policy_commands)
        return list(commands)

    @staticmethod
    def supported_commands_for_policy(policy: Policy) -> List[Type[cmd.Command]]:
        if policy.is_lecturer_policy():
            return [
                cmd.StartCommand,
                # insert new commands here
                cmd.HelpCommand,
            ]
        elif policy.is_user_policy():
            return [
                cmd.StartCommand,
                cmd.AskCommand,
                cmd.RegistrationCommand,
                cmd.UnregistrationCommand,
                cmd.StartNotifyQueueChangeCommand,
                cmd.StopNotifyQueueChangeCommand,
                cmd.HelpCommand,
            ]
        return []
