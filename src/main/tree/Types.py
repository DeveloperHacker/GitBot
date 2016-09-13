import re
from abc import ABCMeta, abstractmethod

import github.Gist
import github.Repository
import github.NamedUser

from main.nlp.Number import Number as _Number


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
        function.__isabstractmethod__ = True

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
            elif len(word) > 1 and word[-1] == "s" and word[:-1] in types:
                result.extend(["list", word[:-1]])
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
        types = {_class.__name__.lower(): _class for _class in subclasses(Type)}
        for word in words:
            if not isinstance(word, str): continue
            word = word.lower()
            blocks = ["list", word[:-1]] if len(word) > 1 and word[-1] == "s" and word[:-1] in types else [word]
            for _type_name, _class in types.items():
                if _type_name == blocks[0]:
                    _type = _class.valueOf(blocks)
                    if _type is not None: result.append(_type)
                    break
        return result

    @staticmethod
    def type(_object) -> 'Type':
        _type = None
        for _class in subclasses(Type):
            if _class.isinstance(_object) and (_type is None or _type.mass() > _class.mass()):
                _type = _class
        return Any.create(_object) if _type is None else _type.create(_object)

    @abstractstaticmethod
    def mass() -> float:
        return None

    @abstractstaticmethod
    def isinstance(_object) -> bool:
        return Null()

    @abstractstaticmethod
    def valueOf(blocks: list) -> 'Type':
        if len(blocks) == 0: return Null()
        for _class in subclasses(Type):
            if _class.__name__.lower() == blocks[0].lower():
                _type = _class.valueOf(blocks[0:])
                if _type is not None: return _type
                break
        return Null()

    @abstractstaticmethod
    def create(_object) -> 'Type':
        return Null()

    @abstractmethod
    def isprimitive(self) -> bool:
        return None


class List(Type):
    def __init__(self, generic: Type):
        self._generic = generic
        super().__init__("list", *list(generic))

    def __str__(self) -> str:
        return "{}s".format(str(self._generic))

    @staticmethod
    def create(_object) -> 'List':
        generic = None
        for elem in list(_object):
            _type = Type.type(elem)
            if generic is None:
                generic = _type
            elif generic != _type:
                generic = Any()
        if generic is None: generic = Any
        return List(generic)

    @staticmethod
    def valueOf(blocks: list) -> 'List':
        if len(blocks) <= 1 or blocks[0].lower() != "list": return Null()
        for _class in subclasses(Type):
            if _class.__name__.lower() == blocks[1].lower():
                _type = _class.valueOf(blocks[1:])
                if _type is not None:
                    return List(_type)
                break
        return Null()

    def isprimitive(self) -> bool:
        return self._generic.isprimitive()

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, List): return True
        return isinstance(_object, list)

    @staticmethod
    def mass() -> float:
        return 0


class String(Type):
    def __init__(self):
        super().__init__("string")

    def __str__(self) -> str:
        return "string"

    @staticmethod
    def create(_object) -> 'String':
        return String()

    @staticmethod
    def valueOf(blocks: list) -> 'String':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "string": return Null()
        return String()

    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return 2

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, String): return True
        return isinstance(_object, str)


class Any(Type):
    def __init__(self):
        super().__init__("any")

    def __str__(self) -> str:
        return "any"

    @staticmethod
    def create(_object) -> 'Any':
        return Any()

    @staticmethod
    def valueOf(blocks: list) -> 'Any':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "any": return Null()
        return Any()

    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return float("inf")

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Any): return True
        return False


class Null(Type):
    def __init__(self):
        super().__init__("null")

    def __str__(self) -> str:
        return "null"

    @staticmethod
    def create(_object) -> 'Null':
        return Null()

    @staticmethod
    def valueOf(blocks: list) -> 'Null':
        return Null()

    def isprimitive(self) -> bool:
        return True

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Null): return True
        return _object is None


class Integer(Type):
    def __init__(self):
        super().__init__("integer")

    def __str__(self) -> str:
        return "integer"

    @staticmethod
    def create(_object) -> 'Integer':
        return Integer()

    @staticmethod
    def valueOf(blocks: list) -> 'Integer':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "integer": return Null()
        return Integer()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Integer): return True
        return _Number.isnumber(_object)


class Email(Type):
    def __init__(self):
        super().__init__("email")

    def __str__(self) -> str:
        return "email"

    @staticmethod
    def create(_object) -> 'Email':
        return Email()

    @staticmethod
    def valueOf(blocks: list) -> 'Email':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "email": return Null()
        return Email()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Email): return True
        return Type.isemail(_object) if isinstance(_object, str) else False


class Url(Type):
    def __init__(self):
        super().__init__("url")

    def __str__(self) -> str:
        return "url"

    @staticmethod
    def create(_object) -> 'Url':
        return Url()

    @staticmethod
    def valueOf(blocks: list) -> 'Url':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "url": return Null()
        return Url()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Url): return True
        return Type.isurl(_object) if isinstance(_object, str) else False


class Id(Type):
    def __init__(self):
        super().__init__("id")

    def __str__(self) -> str:
        return "id"

    @staticmethod
    def create(_object) -> 'Id':
        return Id()

    @staticmethod
    def valueOf(blocks: list) -> 'Id':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "id": return Null()
        return Id()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        return isinstance(_object, Id)


class Key(Type):
    def __init__(self):
        super().__init__("key")

    def __str__(self) -> str:
        return "key"

    @staticmethod
    def create(_object) -> 'Key':
        return Key()

    @staticmethod
    def valueOf(blocks: list) -> 'Key':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "key": return Null()
        return Id()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        return isinstance(_object, Key)


class Login(Type):
    def __init__(self):
        super().__init__("login")

    def __str__(self) -> str:
        return "login"

    @staticmethod
    def create(_object) -> 'Login':
        return Login()

    @staticmethod
    def valueOf(blocks: list) -> 'Login':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "login": return Null()
        return Login()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        return isinstance(_object, Login)


class Name(Type):
    def __init__(self):
        super().__init__("name")

    def __str__(self) -> str:
        return "name"

    @staticmethod
    def create(_object) -> 'Name':
        return Name()

    @staticmethod
    def valueOf(blocks: list) -> 'Name':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "name": return Null()
        return Name()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        return isinstance(_object, Name)


class Gist(Type):
    def __init__(self):
        super().__init__("gist")

    def __str__(self) -> str:
        return "gist"

    @staticmethod
    def create(_object) -> 'Gist':
        return Gist()

    @staticmethod
    def valueOf(blocks: list) -> 'Gist':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "gist": return Null()
        return Gist()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Gist): return True
        return isinstance(_object, github.Gist.Gist)


class Repo(Type):
    def __init__(self):
        super().__init__("repo")

    def __str__(self) -> str:
        return "repo"

    @staticmethod
    def create(_object) -> 'Repo':
        if not isinstance(_object, github.Repository.Repository): raise Exception("Object {} is not repo".format(_object))
        return Repo()

    @staticmethod
    def valueOf(blocks: list) -> 'Repo':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "repo": return Null()
        return Repo()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, Repo): return True
        return isinstance(_object, github.Repository.Repository)


class User(Type):
    def __init__(self):
        super().__init__("user")

    def __str__(self) -> str:
        return "user"

    @staticmethod
    def create(_object) -> 'User':
        return User()

    @staticmethod
    def valueOf(blocks: list) -> 'User':
        if len(blocks) != 1: return Null()
        if blocks[0].lower() != "user": return Null()
        return User()

    def isprimitive(self) -> bool:
        return False

    @staticmethod
    def mass() -> float:
        return 1

    @staticmethod
    def isinstance(_object) -> bool:
        if isinstance(_object, User): return True
        return isinstance(_object, github.NamedUser.NamedUser)
