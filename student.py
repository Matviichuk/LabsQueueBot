from utils import Machine, TransitionRecord as t_row
from enum import Enum
from user import User, UserRole
from managing_context import SHARED_CONTEXT


class _StudentStates(Enum):
    AWAY = 0,
    PENDING_MEETING = 1,
    ON_MEETING = 2,


class _StudentEvents(Enum):
    REGISTER_MEETING = 0,
    UNREGISTER_MEETING = 1,
    JOIN_MEETING = 2,
    FINISH_MEETING = 3,


class Student(User):
    _machine = Machine[_StudentStates, _StudentEvents]

    def register_to_meeting_queue(self) -> bool:
        return self._machine.handle_event(_StudentEvents.REGISTER_MEETING)

    def unregister_from_meetings_queue(self) -> bool:
        return self._machine.handle_event(_StudentEvents.UNREGISTER_MEETING)

    def join_meeting(self) -> bool:
        return self._machine.handle_event(_StudentEvents.JOIN_MEETING)

    def finish_meeting(self) -> bool:
        return self._machine.handle_event(_StudentEvents.FINISH_MEETING)

    def __init__(self, user_id: int, user_name: str):
        super().__init__(user_id, user_name, UserRole.STUDENT)
        self._machine = Machine[_StudentStates, _StudentEvents](_StudentStates.AWAY, [
            t_row(_StudentStates.AWAY, _StudentEvents.REGISTER_MEETING, _StudentStates.PENDING_MEETING, self._register_on_meeting),
            t_row(_StudentStates.PENDING_MEETING, _StudentEvents.UNREGISTER_MEETING, _StudentStates.AWAY, self._unregister_from_meeting),
            t_row(_StudentStates.PENDING_MEETING, _StudentEvents.JOIN_MEETING, _StudentStates.ON_MEETING, self._join_meeting, self._should_join_meeting),
            t_row(_StudentStates.ON_MEETING, _StudentEvents.FINISH_MEETING, _StudentStates.AWAY, self._finish_meeting),
        ])

    def _register_on_meeting(self):
        SHARED_CONTEXT.register_user_on_review(self)

    def _unregister_from_meeting(self):
        SHARED_CONTEXT.unregister_user_from_review(self)

    def _join_meeting(self):
        pass

    def _should_join_meeting(self) -> bool:
        return False

    def _finish_meeting(self):
        pass
