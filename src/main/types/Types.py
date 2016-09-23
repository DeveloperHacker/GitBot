import re
from abc import ABCMeta

import github.Gist
import github.Repository
import github.NamedUser
import github.AuthenticatedUser
from sphinx.util.pycompat import NoneType
from src.main.Utils import subclasses as _subclasses
from src.main.nlp.Number import Number


class Type(metaclass=ABCMeta):
    @property
    def blocks(self) -> tuple:
        return self._blocks

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, *args):
        if len(args) == 0: raise Exception("Illegal type name")
        self._blocks = tuple(args)
        self._name = self._blocks[0]
        self._generic = Type.valueOf(self._blocks[1:]) if len(self._blocks) > 1 else None

    def __str__(self) -> str:
        return ' '.join(self._blocks)

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
        types = {subclass.__name__.lower() for subclass in _subclasses(Type)}
        for word in words:
            if not isinstance(word, str): continue
            word = word.lower()
            blocks = ["list", word[:-1]] if len(word) > 1 and word[-1] == "s" and word[:-1] in types else [word]
            for type_name in types:
                if type_name == blocks[0]:
                    _type = Type.valueOf(blocks)
                    if _type is not None: result.append(_type)
                    break
        return result

    @staticmethod
    def type(element) -> 'Type':
        result = None
        for subclass in _subclasses(Type):
            if subclass.isinstance(element) and (result is None or result.mass > subclass.mass):
                result = subclass
        if result is None: raise Exception("{} object's type not found".format(element.__name__))
        result = result()
        result._blocks = result._blocks + tuple(result.get_generic(element))
        return result

    _mass = 0

    _inner = NoneType

    _primitive = True

    @classmethod
    def isinstance(cls, element) -> bool:
        return isinstance(element, cls._inner)

    @classmethod
    def isprimitive(cls) -> bool:
        return cls._primitive

    @staticmethod
    def valueOf(blocks: list) -> 'Type':
        if len(blocks) == 0: return Null()
        for subclass in _subclasses(Type):
            if subclass.__name__.lower() == blocks[0].lower():
                result = subclass()
                if len(blocks) > 1: result = result.set_generic(Type.valueOf(blocks[1:]))
                return result
        return Null()

    @staticmethod
    def get_generic(element) -> 'Type': return ()


class List(Type):
    @property
    def generic(self):
        return self._generic

    def __init__(self, generic=None):
        if generic is None: generic = []
        self._generic = generic
        super().__init__("list", *list(generic))
        List._primitive = self._generic.isprimitive()
        List._inner = list

    def __str__(self) -> str:
        return "{}s".format(str(self._generic))

    @staticmethod
    def get_generic(element) -> 'Type':
        generic = None
        for elem in list(element):
            _type = Type.type(elem)
            if generic is None:
                generic = _type
            elif generic != _type:
                generic = None
                break
        return Any() if generic is None else generic

    @staticmethod
    def create(element) -> 'List':
        return List(List.get_generic(element))


class String(Type):
    _instance = None

    def __new__(cls) -> 'String':
        return object.__new__(String) if String._instance is None else String._instance

    def __init__(self):
        if String._instance is None:
            String._instance = self
            super().__init__("string")
            String._inner = str
            String._mass = 3


class Any(Type):
    _instance = None

    def __new__(cls) -> 'Any':
        return object.__new__(Any) if Any._instance is None else Any._instance

    def __init__(self):
        if Any._instance is None:
            Any._instance = self
            super().__init__("any")
            Any._inner = object
            Any._mass = float("inf")


class Null(Type):
    _instance = None

    def __new__(cls) -> 'Null':
        return object.__new__(Null) if Null._instance is None else Null._instance

    def __init__(self):
        if Null._instance is None:
            Null._instance = self
            super().__init__("null")


class Integer(Type):
    _instance = None

    def __new__(cls) -> 'Integer':
        return object.__new__(Integer) if Integer._instance is None else Integer._instance

    def __init__(self):
        if Integer._instance is None:
            Integer._instance = self
            super().__init__("integer")
            Integer._inner = Number


class Email(Type):
    _instance = None

    def __new__(cls) -> 'Email':
        return object.__new__(Email) if Email._instance is None else Email._instance

    def __init__(self):
        if Email._instance is None:
            Email._instance = self
            super().__init__("email")
            Email._inner = str
            Email._primitive = False

    @classmethod
    def isinstance(cls, element) -> bool:
        return isinstance(element, cls._inner) and Type.isemail(element)


class Url(Type):
    _instance = None

    def __new__(cls) -> 'Url':
        return object.__new__(Url) if Url._instance is None else Url._instance

    def __init__(self):
        if Url._instance is None:
            Url._instance = self
            super().__init__("url")
            Url._inner = str
            Url._primitive = False

    @classmethod
    def isinstance(cls, element) -> bool:
        return isinstance(element, cls._inner) and Type.isurl(element)


class Id(Type):
    _instance = None

    def __new__(cls) -> 'Id':
        return object.__new__(Id) if Id._instance is None else Id._instance

    def __init__(self):
        if Id._instance is None:
            Id._instance = self
            super().__init__("id")
            Id._inner = (str, int)
            Id._primitive = False


class Key(Type):
    _instance = None

    def __new__(cls) -> 'Key':
        return object.__new__(Key) if Key._instance is None else Key._instance

    def __init__(self):
        if Key._instance is None:
            Key._instance = self
            super().__init__("key")
            Key._inner = str
            Key._primitive = False


class Login(Type):
    _instance = None

    def __new__(cls) -> 'Login':
        return object.__new__(Login) if Login._instance is None else Login._instance

    def __init__(self):
        if Login._instance is None:
            Login._instance = self
            super().__init__("login")
            Login._inner = str
            Login._primitive = False


class Name(Type):
    _instance = None

    def __new__(cls) -> 'Name':
        return object.__new__(Name) if Name._instance is None else Name._instance

    def __init__(self):
        if Name._instance is None:
            Name._instance = self
            super().__init__("name")
            Name._inner = str
            Name._primitive = False


class Gist(Type):
    _instance = None

    def __new__(cls) -> 'Gist':
        return object.__new__(Gist) if Gist._instance is None else Gist._instance

    def __init__(self):
        if Gist._instance is None:
            Gist._instance = self
            super().__init__("gist")
            Gist._inner = github.Gist.Gist
            Gist._primitive = False


class Repo(Type):
    _instance = None

    def __new__(cls) -> 'Repo':
        return object.__new__(Repo) if Repo._instance is None else Repo._instance

    def __init__(self):
        if Repo._instance is None:
            Repo._instance = self
            super().__init__("repo")
            Repo._inner = github.Repository.Repository
            Repo._primitive = False


class User(Type):
    _instance = None

    def __new__(cls) -> 'User':
        return object.__new__(User) if User._instance is None else User._instance

    def __init__(self):
        if User._instance is None:
            User._instance = self
            super().__init__("user")
            User._inner = (github.NamedUser.NamedUser, github.AuthenticatedUser.AuthenticatedUser)
            User._primitive = False
