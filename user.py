from enum import Enum


class UserRole(Enum):
    STUDENT = 0,
    TEACHER = 1,


class User(object):
    _user_id: int
    _user_name: str
    _role: UserRole

    def __init__(self, user_id: int, user_name: str, role: UserRole):
        super().__init__()
        self._user_id = user_id
        self._user_name = user_name
        self._role = role

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def name(self) -> str:
        return self._user_name

    @property
    def role(self) -> UserRole:
        return self._role
