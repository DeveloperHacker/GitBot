from abc import ABCMeta, abstractmethod

from main.interfaces.Parser import Node
from main.types.Node import Root


class Corrector(metaclass=ABCMeta):
    @abstractmethod
    def correct(self, root: Node) -> Root: pass