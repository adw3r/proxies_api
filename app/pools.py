import abc
import json
import pathlib
from random import shuffle
from typing import NoReturn

from config import PROXIES_FOLDER, FACTORIES_JSON


def dump_factories_file(model: dict):
    with open(FACTORIES_JSON, 'w') as file:
        json.dump(model, file)


def get_factories_file():
    with open(FACTORIES_JSON, 'rb') as file:
        return json.load(file)


class Pool(abc.ABC):
    pool: list = []

    def get_pool(self) -> list:
        return self.pool

    def __len__(self) -> int:
        return len(self.pool)

    @abc.abstractmethod
    def pop(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def info(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    def reload(self) -> NoReturn:
        raise NotImplementedError


class FilePool(Pool):
    def info(self) -> dict:
        return {'amount': len(self)}

    def pop(self) -> str:
        if len(self.pool) == 0:
            self.reload()
        value = self.pool.pop()
        return value

    def __init__(self, path: pathlib.Path):
        self.path = path
        if not self.path.exists():
            self.path.write_text('')
        self.reload()

    def get_pool(self) -> list:
        self.reload()
        return self.pool

    def reload(self) -> NoReturn:
        with open(self.path, encoding='latin-1') as file:
            self.pool = file.read().split('\n')
            shuffle(self.pool)
            if '' in self.pool:
                self.pool.remove('')

    def clear(self) -> None:
        self.pool.clear()


class Factories:

    def keys(self):
        return self.factories.keys()

    def __init__(self):
        self.reload_pools()

    def reload_pools(self):
        items = get_factories_file().items()
        self.factories = {key: FilePool(pathlib.Path(PROXIES_FOLDER, value)) for key, value in items}

    def get(self, pool: str):
        return self.factories.get(pool)

    def items(self) -> list[tuple[str, FilePool]]:
        return self.factories.items()
