from abc import ABC
from enum import IntEnum


class PolicyIdentifier(IntEnum):
    UserPolicy = 0,
    LecturerPolicy = 1,


class Policy(ABC):
    identifier: PolicyIdentifier

    @staticmethod
    def policy_with_identifier(identifier: PolicyIdentifier):
        if identifier is PolicyIdentifier.LecturerPolicy:
            return LecturerPolicy()
        return UserPolicy()

    def is_user_policy(self):
        return self.identifier is PolicyIdentifier.UserPolicy

    def is_lecturer_policy(self):
        return self.identifier is PolicyIdentifier.LecturerPolicy


class UserPolicy(Policy):
    identifier = PolicyIdentifier.UserPolicy


class LecturerPolicy(Policy):
    identifier = PolicyIdentifier.LecturerPolicy
