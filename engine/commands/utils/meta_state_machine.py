from typing import TypeVar, Generic, Callable, List

_state_type = TypeVar('S')
_event_type = TypeVar('E')


class TransitionRecord(Generic[_state_type, _event_type]):
    _initial_state: _state_type
    _event: _event_type
    _target_state: _state_type
    _guard: Callable[[], bool]
    _action: Callable

    def __init__(self, initial_state: _state_type, event: _event_type, target_state: _state_type, action: Callable, guard: Callable[[], bool] = lambda: True):
        self._initial_state = initial_state
        self._event = event
        self._target_state = target_state
        self._action = action
        self._guard = guard

    @property
    def initial_state(self) -> _state_type:
        return self._initial_state

    @property
    def event(self) -> _event_type:
        return self._event

    @property
    def target_state(self) -> _state_type:
        return self._target_state

    @property
    def guard(self) -> Callable[[], bool]:
        return self._guard

    @property
    def action(self) -> Callable:
        return self._action


class Machine(Generic[_state_type, _event_type]):
    _current_state: _state_type
    _transitions: List[TransitionRecord[_state_type, _event_type]]

    def __init__(self, initial_state: _state_type, transitions: List[TransitionRecord[_state_type, _event_type]]):
        self._current_state = initial_state
        self._transitions = transitions

    def handle_event(self, event: _event_type) -> bool:
        for transition in self._transitions:
            if transition.initial_state == self.state and transition.event is event and transition.guard():
                self._current_state = transition.target_state
                transition.action()
                return True
        return False

    @property
    def state(self):
        return self._current_state

