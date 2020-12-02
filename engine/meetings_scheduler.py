from abc import ABC
from typing import List, Optional
import asyncio
from .user import User
from .url import Url


class MeetingsSchedulerDelegate(ABC):
    async def notify(self, user: User, msg: str):
        pass


class MeetingRoom:
    def __init__(self, deliverer: User, owner: User, location: Url):
        self._deliverer = deliverer
        self._owner = owner
        self._location = location

    @property
    def is_free(self):
        return self._deliverer is None

    @property
    def deliverer(self) -> Optional[User]:
        return self._deliverer

    @deliverer.setter
    def deliverer(self, value):
        self._deliverer = value

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def location(self) -> Url:
        return self._location


class MeetingsScheduler:
    def __init__(self):
        self._review_pending_queue = []
        self._review_list_observers = []
        self._rooms = []
        self._delegate = None

    @property
    def delegate(self) -> Optional[MeetingsSchedulerDelegate]:
        return self._delegate

    @delegate.setter
    def delegate(self, value):
        self._delegate = value

    @property
    def rooms(self) -> List[MeetingRoom]:
        return self._rooms

    @property
    def pending_queue(self) -> List[User]:
        return self._review_pending_queue

    @property
    def pending_queue_observers(self) -> List[User]:
        return self._review_list_observers

    async def insert_deliverer(self, user: User) -> Optional[int]:
        try:
            return self.pending_queue.index(user)
        except ValueError:
            future_index = len(self.pending_queue)
            self.pending_queue.append(user)
            if await self._try_deliver():
                return None
            return future_index

    async def remove_deliverer(self, user: User) -> bool:
        if user in self.pending_queue:
            self.pending_queue.remove(user)
            return True
        return False

    async def insert_queue_observer(self, user: User) -> bool:
        if user in self.pending_queue:
            self.pending_queue_observers.append(user)
            return True
        return False

    async def remove_queue_observer(self, user: User) -> bool:
        if user in self.pending_queue_observers:
            self.pending_queue_observers.remove(user)
            return True
        return False

    async def _notify_participants(self, room):
        if self.delegate is None:
            return
        owner_msg = f"connect: {room.deliverer.name}\n" \
                    f"nickname: {room.deliverer.nickname}"
        deliverer_msg = f"Your turn now\n" \
                        f"Room link: {room.location.location}"
        await self.delegate.notify(room.owner, owner_msg)
        await self.delegate.notify(room.deliverer, deliverer_msg)

    async def _notify_observers(self):
        if self.delegate is None:
            return

        async def notify(user: User, index: int):
            msg = f"New queue number is: {index}"
            self.delegate.notify(user, msg)
        send_operations = []
        for user in self.pending_queue_observers:
            index = self.pending_queue.index(user)
            send_operations.append(notify(user, index))
        await asyncio.gather(send_operations)

    async def _try_deliver(self) -> bool:
        free_room = None
        deliverer = None
        for room in self.rooms:
            if room.is_free:
                free_room = room
                break
        if self.pending_queue:
            deliverer = self.pending_queue[0]

        if free_room is not None and deliverer is not None:
            self.remove_deliverer(deliverer)
            free_room.deliverer = deliverer
            await self._notify_participants(free_room)
            await self._notify_observers()
