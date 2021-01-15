from .user import User
from typing import Optional


class Cache(object):
    def __init__(self):
        self._users = {}

    def user(self, user_id: int) -> Optional[User]:
        if user_id in self._users:
            return self._users[user_id]
        return None

    def insert_user(self, user: User):
        self._users[user.identifier] = user
