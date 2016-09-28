from abc import ABCMeta, abstractmethod

from main.types.Node import Root


class Closure:
    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self) -> list:
        return self._args

    def __init__(self, name: str, args: list):
        self._name = name
        self._args = args


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def build(self, root: Root) -> list: pass
