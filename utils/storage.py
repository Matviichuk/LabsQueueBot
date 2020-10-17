import json
from pathlib import Path
from typing import List, Callable

_STORAGE_DEFAULT_PATH = Path("default_storage.json")


class PrivilegedStorage:
    _path: Path
    _user_ids: List[int]

    def __init__(self, path: Path):
        self._path = path
        self._load()

    def _load(self):
        if self._path.exists():
            stored_content = self._path.read_text()
            self._user_ids = json.loads(stored_content)
        else:
            self._user_ids = []

    def _flush(self):
        content = json.dumps(self._user_ids)
        self._path.write_text(content)

    def update_batch(self, updates: Callable):
        updates()
        self._flush()

    def register_privileged_user_with_id(self, user_id: int):
        self.update_batch(lambda: self._user_ids.append(user_id))

    def unregister_privileged_user_with_id(self, user_id: int):
        if user_id in self._user_ids:
            self.update_batch(lambda: self._user_ids.remove(user_id))

    def contain_privileged_user(self, user_id):
        return user_id in self._user_ids


DEFAULT_STORAGE = PrivilegedStorage(_STORAGE_DEFAULT_PATH)
