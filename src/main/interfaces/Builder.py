from abc import ABCMeta, abstractmethod

from main.types.Node import Root


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def build(self, root: Root) -> list: pass
