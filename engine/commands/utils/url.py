class Url:
    def __init__(self, path: str):
        # TODO add validation for urls here
        self._path = path

    @property
    def location(self) -> str:
        return self._path
