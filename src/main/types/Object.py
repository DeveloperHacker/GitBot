from abc import abstractmethod, ABCMeta
from copy import deepcopy

from src.main.Utils import subclasses
from src.main.nlp.Number import Number
from src.main.types.Function import Function
from src.main.types.Types import Type
from src.main.types import Types

import github.Gist
import github.Repository
import github.NamedUser


class Object(metaclass=ABCMeta):
    @property
    def type(self) -> Type:
        return self._type

    @property
    def object(self):
        return self._object

    @staticmethod
    def create(_type: Type, _object) -> 'Object':
        instance = None
        objects = {subclass.__name__.lower(): subclass for subclass in subclasses(Object)}
        type_name = _type[0].lower()
        for name, subclass in objects.items():
            if name == type_name:
                instance = subclass(_object)
                break
        if instance is None: raise Exception("Constructor with type {} not found".format(str(_type)))
        return instance

    def __init__(self, _type: Type, _object, simplifier=None):
        if not _type.isinstance(_object): raise Exception("Object is not {}".format(str(_type)))
        self._type = _type
        self._object = _object
        self._simplifier = Function([_type], Types.String(), lambda this: String(str(this))) if simplifier is None else simplifier

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Object): return False
        if self._type != other._type: return False
        return self._object == other._object

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))

    def __deepcopy__(self, memo=None):
        return Object.create(self._type, self._object)

    @staticmethod
    def valueOf(string: str) -> 'Object':
        if Type.isurl(string):
            return Url(string)
        elif Type.isemail(string):
            return Email(string)
        elif Number.isnumber(string):
            return Integer(Number(string.split()))
        else:
            return String(string)

    def simplify(self) -> 'Object':
        return self._simplifier.run(self._object)

    def mark(self, label: str) -> 'Object':
        labeled = deepcopy(self)
        setattr(labeled, "label", lambda: label)
        setattr(labeled, "__deepcopy__", lambda memo=None: deepcopy(self).mark(label))
        return labeled


class List(Object):
    @property
    def object(self) -> list:
        return self._object

    @property
    def type(self) -> Types.List:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.List.create(_object), _object)

    def __str__(self):
        self._object = list(self._object)
        if len(self._object) == 0:
            return "{} not found".format(str(self._type))
        else:
            return '\n'.join([str(Object.create(self.type.generic, element)) for element in self._object])

    def simplify(self) -> 'List':
        simple_type = Types.Null()
        result = []
        self._object = list(self._object)
        for elem in self._object:
            simple = Object.create(Type.valueOf(self._type[1:]), elem).simplify()
            simple_type = simple._type
            result.append(simple._object)
        self._type = Types.List(simple_type)
        self._object = result
        return self


class String(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.String:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.String(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return "'{}'".format(_str)


class Any(Object):
    @property
    def type(self) -> Types.Any:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Any(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Null(Object):
    @property
    def object(self) -> None:
        return self._object

    @property
    def type(self) -> Types.Null:
        return self._type

    _instance = None

    def __new__(cls, _object=None) -> 'Null':
        return object.__new__(Null) if Null._instance is None else Null._instance

    def __init__(self, _object=None):
        if Null._instance is None:
            Null._instance = self
            super().__init__(Types.Null(), _object)

    def __str__(self) -> str:
        return ""


class Integer(Object):
    @property
    def object(self) -> Number:
        return self._object

    @property
    def type(self) -> Types.Integer:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Integer(), _object, Function([Types.Integer()], Types.String(), lambda _integer: String(_integer[-1])))

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Email(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Email:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Email(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        _type = str(self._type)
        return "{}:{}".format(_type, _str)


class Url(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Url:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Url(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        _type = str(self._type)
        return "{}:{}".format(_type, _str)


class Id(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Id:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Id(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        _type = str(self._type)
        return "{}:{}".format(_type, _str)


class Key(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Key:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Key(), _object)

    def __str__(self):
        key = str(self._object.key) if self._object else ""
        _id = str(self._object.id) if self._object else "───║───"
        _type = str(self._type)
        return "{}:{}({})".format(_type, _id, key)


class Login(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Login:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Login(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Name(Object):
    @property
    def object(self) -> str:
        return self._object

    @property
    def type(self) -> Types.Name:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Name(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Gist(Object):
    @property
    def object(self) -> github.Gist.Gist:
        return self._object

    @property
    def type(self) -> Types.Gist:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Gist(), _object, Function([Types.Gist()], Types.Id(), lambda gist: Id(gist.id)))

    def __str__(self) -> str:
        login = str(Login(self._object.owner.login))
        _id = str(Id(self._object.id))
        return "{}'s gist {}".format(login, _id)


class Repo(Object):
    @property
    def object(self) -> github.Repository.Repository:
        return self._object

    @property
    def type(self) -> Types.Repo:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.Repo(), _object, Function([Types.Repo()], Types.Id(), lambda repo: Id(repo.id)))

    def __str__(self) -> str:
        login = str(Login(self._object.owner.login))
        name = str(Name(self.object.name)) if self.object.name is not None else ""
        _id = str(Id(self._object.id))
        return "{}'s repository {}({})".format(login, name, _id)


class User(Object):
    @property
    def object(self) -> github.NamedUser.NamedUser:
        return self._object

    @property
    def type(self) -> Types.User:
        return self._type

    def __init__(self, _object):
        super().__init__(Types.User(), _object, Function([Types.User()], Types.Login(), lambda user: Login(user.login)))

    def __str__(self) -> str:
        login = str(Login(self.object.login))
        name = "({})".format(str(Name(self.object.name))) if self.object.name is not None else ""
        email = "<{}>".format(str(Email(self.object.email))) if self.object.email is not None else ""
        return "{}{} {}".format(login, name, email)
