from user import User, UserRole
from typing import List, Optional, Dict


class ManagingContext:
    _users: List[User]
    _requests_queue: List[User]
    _reviews_queue: List[User]

    def __init__(self):
        self._requests_queue = []
        self._reviews_queue = []
        self._users = []

    def _filter_users_with_role(self, role: UserRole) -> List[User]:
        result = []
        for user in self._users:
            if user.role is role:
                result.append(user)
        return result

    def register_user_on_review(self, user: User):
        if user not in self._requests_queue:
            self._requests_queue.append(user)

    def unregister_user_from_review(self, user: User):
        if user in self._requests_queue:
            self._requests_queue.remove(user)

    def get_user_with_id(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.user_id == user_id:
                return user

    def register_user(self, user: User):
        self._users.append(user)


SHARED_CONTEXT = ManagingContext()
