from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    @property
    def label(self) -> str:
        return self._label

    @abstractmethod
    def flatten(self) -> list: pass

    def __init__(self, label: str):
        self._label = label
        self._children = []

    def __getitem__(self, index):
        return self._children[index]

    @abstractmethod
    def isleaf(self) -> bool: pass

    def append(self, child: 'Node'):
        self._children.append(child)

    def extend(self, children: list):
        self._children.extend(children)

    def children(self, **kwargs) -> list:
        labels = Node.__labels(**kwargs)
        return self._children if labels is None else [child for child in self._children if child.label in labels]

    def sub_children(self, **kwargs) -> list:
        labels = Node.__labels(**kwargs)
        if labels is None:
            children = self._children
        else:
            children = [child for child in self._children if child.label in labels]
            children = [ch for child in children for ch in child.sub_children(**kwargs)]
        return children + self.children(**kwargs)

    def remove(self, **kwargs):
        if "index" in kwargs:
            index = [kwargs["index"]]
            del self._children[index]
            return
        labels = Node.__labels(**kwargs)
        self._children = [] if labels is None else [child for child in self._children if child.label not in labels]

    @staticmethod
    def __labels(**kwargs) -> list:
        if "labels" in kwargs: return kwargs["labels"]
        elif "label" in kwargs: return [kwargs["label"]]
        else: return None


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, string: str) -> Node: pass
