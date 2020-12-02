class User:
    def __init__(self, identifier: int, name: str, nickname: str):
        self._id = identifier
        self._name = name
        self._nickname = nickname

    @property
    def identifier(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def nickname(self) -> str:
        return self._nickname
