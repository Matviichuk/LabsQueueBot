from bot_shared import DISPATCHER, BOT
from aiogram import types
# import user_roles_filter
# from urllib.parse import urlparse

from managing_context import SHARED_CONTEXT
from student import Student, UserRole

_student_help = "available commands:\n" \
                "/register - for review registration\n" \
                "/unregister - for leave from queue \n"


def _register_student_to_context_if_necessary(message: types.message) -> Student:
    user_id = message.from_user.id
    managed_user = SHARED_CONTEXT.get_user_with_id(user_id)
    if managed_user is None:
        user_full_name = message.chat.full_name
        managed_user = Student(user_id, user_full_name)
        SHARED_CONTEXT.register_user(managed_user)
    return managed_user


@DISPATCHER.message_handler(commands=["register"], user_role=UserRole.STUDENT)
async def _student_meeting_register_handler(message: types.message):
    student = _register_student_to_context_if_necessary(message)

    if student.register_to_meeting_queue():
        await message.answer(f"successfully registered")
    else:
        await message.answer(f"bad flow call")


@DISPATCHER.message_handler(commands=["unregister"], user_role=UserRole.STUDENT)
async def _student_meeting_unregister_handler(message: types.message):
    student = _register_student_to_context_if_necessary(message)

    if student.unregister_from_meetings_queue():
        await message.answer(f"successfully unregister")
    else:
        await message.answer(f"bad flow call")


@DISPATCHER.message_handler(commands=["start"], user_role=UserRole.STUDENT)
async def _student_start_handler(message: types.message):
    student = _register_student_to_context_if_necessary(message)
    await message.answer(f"Hi {student.name}!\n{_student_help}")


@DISPATCHER.message_handler(commands=["help"], user_role=UserRole.STUDENT)
async def _print_help_student(message: types.message):
    _register_student_to_context_if_necessary(message)
    await message.reply(_student_help)


@DISPATCHER.message_handler()
async def _default_handler(message: types.message):
    await message.reply("command unavailable use /help for review commands")
