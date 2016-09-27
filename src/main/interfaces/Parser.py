from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    @property
    def children(self) -> tuple:
        return tuple(self._children)

    @property
    def label(self) -> str:
        return self._label

    def __init__(self, label: str):
        self._label = label
        self._children = []

    def isleaf(self) -> bool:
        return len(self._children) == 0

    def add_child(self, child: 'Node'):
        self._children.append(child)

    def add_children(self, children: list):
        self._children.extend(children)

    def get_children(self, **kwargs) -> list:
        labels = Node.__labels(**kwargs)
        return [child for child in self._children if child.label in labels]

    def get_all_children(self, **kwargs) -> list:
        labels = Node.__labels(**kwargs)
        children = [ch for child in self._children if child.label in labels for ch in child.get_all_children(**kwargs)]
        return children + self.get_children(**kwargs)

    def remove_children(self, **kwargs):
        if "index" in kwargs:
            index = [kwargs["index"]]
            del self._children[index]
            return
        labels = Node.__labels(**kwargs)
        self._children = [child for child in self._children if child.label not in labels]

    @staticmethod
    def __labels(**kwargs) -> list:
        if "labels" in kwargs: return kwargs["labels"]
        elif "label" in kwargs: return [kwargs["label"]]
        else: raise TypeError()


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, string: str) -> Node: pass
