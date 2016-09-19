from abc import abstractmethod, ABCMeta
from copy import deepcopy

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

    def __init__(self, _type: Type, _object):
        self._type = _type
        self._object = _object

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
        if memo is None: memo = {}
        dpcpy = self.__class__(self._type, self._object)
        memo[id(self)] = dpcpy
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                setattr(dpcpy, attr, deepcopy(value, memo))
        return dpcpy

    @staticmethod
    def valueOf(string: str) -> 'Object':
        if Type.isurl(string):
            return Url(string)
        elif Type.isemail(string):
            return Email(string)
        elif Number.isnumber(string.split()):
            return Integer(Number(string.split()))
        elif string.isnumeric():
            return Id(string)
        else:
            return String(string)

    def simplify(self) -> 'Object':
        if self._type in Object._similar_types:
            simple = Object._similar_types[self._type]
            self._type = simple.result
            self._object = simple.run(self._object)
        elif self._type[0] == "list":
            simple_type = Types.Null()
            result = []
            self._object = list(self._object)
            for elem in self._object:
                simple = Object(Type.valueOf(self._type[1:]), elem).simplify()
                simple_type = simple._type
                result.append(simple._object)
            self._type = Types.List(simple_type)
            self._object = result
        return self

    _similar_types = {
        Types.User(): Function(Types.Login(), [Types.User()], lambda user: user.login),
        Types.Repo(): Function(Types.Id(), [Types.Repo()], lambda repo: repo.id),
        Types.Gist(): Function(Types.Id(), [Types.Gist()], lambda gist: gist.id),
        Types.Name(): Function(Types.String(), [Types.Name()], lambda name: str(name)),
        Types.Login(): Function(Types.String(), [Types.Login()], lambda login: str(login)),
        Types.Url(): Function(Types.String(), [Types.Url()], lambda url: str(url)),
        Types.Email(): Function(Types.String(), [Types.Email()], lambda email: str(email)),
        Types.Key(): Function(Types.String(), [Types.Key()], lambda key: str(key)),
        Types.Id(): Function(Types.String(), [Types.Id()], lambda _id: str(_id)),
        Types.Integer(): Function(Types.String(), [Types.Integer()], lambda _integer: _integer[0])
    }


class LabeledObject(Object):
    def __str__(self) -> str:
        pass

    @property
    def label(self) -> str:
        return self._label

    def __init__(self, label: str, _object: Object):
        super().__init__(_object._type, _object._object)
        self.__str__ = _object.__str__
        self._label = label

    def __deepcopy__(self, memo=None):
        if memo is None: memo = {}
        return self.__class__(self._label, self)


def __new__(cls, _type, _object, arg):
    if not _type.isinstance(arg): return Null()
    instance = object.__new__(cls)
    _object.__init__(instance, arg)
    return instance


class List(Object):
    @property
    def object(self) -> list:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.List, List, _object)

    def __init__(self, _object):
        super().__init__(Types.List.create(_object), _object)

    def __str__(self):
        self._object = list(self._object)
        result = [elem for elem in self._object]
        if len(self._object) == 0:
            return "{} not found".format(str(self._type))
        else:
            return '\n'.join(result)


class String(Object):
    @property
    def object(self) -> str:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.String, String, _object)

    def __init__(self, _object):
        super().__init__(Types.String(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return "'{}'".format(_str)


class Any(Object):
    @property
    def object(self):
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.String, String, _object)

    def __init__(self, _object):
        super().__init__(Types.String(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Null(Object):
    @property
    def object(self) -> None:
        return self._object

    def __init__(self):
        super().__init__(Types.Null(), None)

    def __str__(self) -> str:
        return ""


class Integer(Object):
    @property
    def object(self) -> Number:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Integer, Integer, _object)

    def __init__(self, _object):
        super().__init__(Types.Integer(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Email(Object):
    @property
    def object(self) -> str:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Email, Email, _object)

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

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Url, Url, _object)

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

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Id, Id, _object)

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

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Key, Key, _object)

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

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Login, Login, _object)

    def __init__(self, _object):
        super().__init__(Types.Login(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Name(Object):
    @property
    def object(self) -> str:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Name, Name, _object)

    def __init__(self, _object):
        super().__init__(Types.Name(), _object)

    def __str__(self) -> str:
        _str = str(self._object) if self._object else "───║───"
        return _str


class Gist(Object):
    @property
    def object(self) -> github.Gist.Gist:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Gist, Gist, _object)

    def __init__(self, _object):
        super().__init__(Types.Gist(), _object)

    def __str__(self) -> str:
        login = str(Login(self._object.owner.login))
        _id = str(Id(self._object.id))
        return "{}'s gist {}".format(login, _id)


class Repo(Object):
    @property
    def object(self) -> github.Repository.Repository:
        return self._object

    def __new__(cls, _object) -> Object:
        return __new__(cls, Types.Repo, Repo, _object)

    def __init__(self, _object):
        super().__init__(Types.Repo(), _object)

    def __str__(self) -> str:
        login = str(Login(self._object.owner.login))
        name = str(Name(self._object.name))
        _id = str(Id(self._object.id))
        return "{}'s repo {}({})".format(login, name, _id)


class User(Object):
    @property
    def object(self) -> github.NamedUser.NamedUser:
        return self._object

    def __new__(cls, _object) -> 'User':
        return __new__(cls, Types.User, User, _object)

    def __init__(self, _object):
        super().__init__(Types.User(), _object)

    def __str__(self) -> str:
        login = str(Login(self.object.login))
        name = str(Name(self.object.name))
        email = str(Email(self.object.email))
        return "{}({}) <{}>".format(login, name, email)
