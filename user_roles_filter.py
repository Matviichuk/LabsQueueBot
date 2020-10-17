from aiogram.dispatcher.filters import BoundFilter
from bot_shared import DISPATCHER
from aiogram import types
from utils import DEFAULT_STORAGE
from user import UserRole


class RolesFilter(BoundFilter):
    key = 'user_role'

    def __init__(self, user_role):
        self.user_role = user_role

    async def check(self, message: types.Message):
        user_id = message.from_user.id
        if self.user_role == UserRole.TEACHER:
            return DEFAULT_STORAGE.contain_privileged_user(user_id)
        elif self.user_role == UserRole.STUDENT:
            return True
        return False


DISPATCHER.filters_factory.bind(RolesFilter)
