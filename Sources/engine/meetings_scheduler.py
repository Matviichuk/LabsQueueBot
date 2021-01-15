from abc import ABC
from typing import List, Optional
import asyncio
from .user import User
from engine.commands.utils import Url


class MeetingsSchedulerDelegate(ABC):
    async def notify(self, user: User, msg: str):
        pass


class MeetingRoom:
    def __init__(self, owner: User, location: Url):
        self._deliverer = None
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
            if user in self.pending_queue_observers:
                return False
            else:
                self.pending_queue_observers.append(user)
                return True
        return False

    async def remove_queue_observer(self, user: User) -> bool:
        if user in self.pending_queue_observers:
            self.pending_queue_observers.remove(user)
            return True
        return False

    def _get_room_for_owner(self, owner: User) -> Optional[MeetingRoom]:
        for room in self.rooms:
            if room.owner is owner:
                return room
        return None

    async def allocate_room(self, owner: User, location: Url) -> Optional[MeetingRoom]:
        owned_room = self._get_room_for_owner(owner)
        if owned_room is not None:
            return owned_room
        new_room = MeetingRoom(owner, location)
        self.rooms.append(new_room)
        await self._try_deliver()
        return new_room

    async def kick_deliverer_from_room(self, owner: User) -> bool:
        owned_room = self._get_room_for_owner(owner)
        if owned_room is not None:
            owned_room.deliverer = None
            await self._try_deliver()
            return True
        return False

    async def close_room(self, owner: User) -> Optional[MeetingRoom]:
        owned_room = self._get_room_for_owner(owner)
        if owned_room is not None:
            self.rooms.remove(owned_room)
            return owned_room
        return None

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

        async def notify(deliverer: User, number: int):
            msg = f"New queue number is: {number + 1}"
            await self.delegate.notify(deliverer, msg)
        send_operations = list()
        for user in self.pending_queue_observers:
            try:
                index = self.pending_queue.index(user)
                send_operations.append(notify(user, index))
            except ValueError:
                self.pending_queue_observers.remove(user)
        await asyncio.gather(*send_operations)

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
            await self.remove_deliverer(deliverer)
            free_room.deliverer = deliverer
            await self._notify_participants(free_room)
            await self._notify_observers()
