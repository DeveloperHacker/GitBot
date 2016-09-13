import re
from abc import ABCMeta, abstractmethod

from main.nlp.Number import Number


def subclasses(_class) -> set:
    _subclasses = set()
    work = [_class]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in _subclasses:
                _subclasses.add(child)
                work.append(child)
    return _subclasses


class abstractstaticmethod(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstaticmethod, self).__init__(function)
        function.__isAbstractMethod__ = True

    __isabstractmethod__ = True


class Type(metaclass=ABCMeta):
    @property
    def blocks(self) -> tuple:
        return self._blocks

    def __init__(self, *args):
        self._blocks = tuple(Type.parse(list(args)))
        if len(self._blocks) == 0: raise Exception("Created empty type")

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __getitem__(self, index):
        return self._blocks[index]

    def __eq__(self, other):
        if not isinstance(other, Type): return False
        if len(self._blocks) != len(other._blocks): return False
        return all([e1 == e2 for e1, e2 in zip(self._blocks, other._blocks)])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def parse(words: list) -> list:
        result = []
        types = [_class.__name__.lower() for _class in subclasses(Type)]
        for word in words:
            word = word.lower()
            if not word: continue
            if word in types:
                result.append(word)
            elif word in Type.type_synonyms:
                result.extend(Type.type_synonyms[word])
            else:
                raise Exception("Type \"{}\" not found".format(word))
        return result

    @staticmethod
    def isurl(string: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, string) is not None

    @staticmethod
    def isemail(string: str) -> bool:
        regex = re.compile("[^@]+@[^@]+\.[^@]+")
        return re.match(regex, string) is not None

    @staticmethod
    def extract(words: list) -> list:
        result = []
        types = [_class.__name__.lower() for _class in subclasses(Type)]
        for word in words:
            word = word.lower()
            if word in Type.type_synonyms or word in types:
                result.append(Type(word))
        return result

    types = {
        "user", "repo", "gist", "name", "login", "key", "id", "url", "email", "number"
    }

    type_synonyms = {
        "users": ["list", "user"],
        "repos": ["list", "repo"],
        "gists": ["list", "gist"],
        "keys": ["list", "key"]
    }

    @abstractstaticmethod
    def mass() -> float:
        pass

    @abstractmethod
    def isprimitive(self) -> bool:
        pass

    @abstractstaticmethod
    def isinstance(_object) -> bool:
        pass

    @staticmethod
    def type(_object) -> 'Type':
        _type = None
        for _class in subclasses(Type):
            if _class.isinstance(_object) and (_type is None or _type.mass() > _class.mass()):
                _type = _class
        return Any(_object) if _type is None else _type(_object)


class List(Type):
    def isprimitive(self) -> bool:
        return self._generic.isprimitive()

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, List): return True
        return isinstance(_object, list)

    @staticmethod
    def mass() -> float:
        return 0

    def __init__(self, _object):
        if not List.isinstance(_object): raise Exception("Object {} is not list".format(_object))
        self._generic = None
        for elem in list(_object):
            _type = Type.type(elem)
            if self._generic is None:
                self._generic = _type
            elif self._generic != _type:
                self._generic = Any(_object)
        if self._generic is None: self._generic = Any
        super().__init__("list", *list(self._generic))

    def __str__(self) -> str:
        return "{}s".format(str(self._generic))


class Integer(Type):
    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Integer): return True
        return Number.isnumber(_object)

    def __init__(self, _object):
        if not Integer.isinstance(_object): raise Exception("Object {} is not string".format(_object))
        super().__init__("integer")

    def __str__(self) -> str:
        return "integer"


class String(Type):
    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return 2

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, String): return True
        return isinstance(_object, str)

    def __init__(self, _object):
        if not String.isinstance(_object): raise Exception("Object {} is not string".format(_object))
        super().__init__("string")

    def __str__(self) -> str:
        return "string"


class Any(Type):
    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return float("inf")

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Any): return True
        return False

    def __init__(self, _):
        super().__init__("any")

    def __str__(self) -> str:
        return "any"


class Null(Type):
    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return 0

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Null): return True
        return _object is None

    def __init__(self, _):
        super().__init__("null")

    def __str__(self) -> str:
        return "null"


_type = Type.type([123, 12312])
print(_type)
print(_type.blocks)
print(_type.isprimitive())

_type = Type.type(["123asd", "12312asd"])
print(_type)
print(_type.blocks)
print(_type.isprimitive())
