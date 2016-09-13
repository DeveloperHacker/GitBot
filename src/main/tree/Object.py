from src.main.nlp.Number import Number
from src.main.tree.Function import Function
from src.main.tree.Types import Type
from src.main.tree import Types


class Object:
    @property
    def type(self):
        return self._type

    @property
    def object(self):
        return self._object

    def __init__(self, _type: Type, _object):
        self._type = _type
        self._object = _object

    def __str__(self) -> str:
        if self._type[0] == "list":
            self._object = list(self._object)
            result = [str(Object(Type.valueOf(self._type[1:]), elem)) for elem in self._object]
            if len(self._object) == 0:
                return "{} not found".format(str(self._type))
            else:
                return '\n'.join(result)
        elif self._type == Types.User():
            login = str(Object(Types.Login(), self._object.login))
            name = str(Object(Types.Name(), self._object.name))
            email = str(Object(Types.Email(), self._object.email))
            return "{}({}) <{}>".format(login, name, email)
        elif self._type == Types.Repo():
            login = str(Object(Types.Login(), self._object.owner.login))
            name = str(Object(Types.Name(), self._object.name))
            _id = str(Object(Types.Id(), self._object.id))
            return "{}'s repo {}({})".format(login, name, _id)
        elif self._type == Types.Gist():
            login = str(Object(Types.Login(), self._object.owner.login))
            _id = str(Object(Types.Id(), self._object.id))
            return "{}'s gist {}".format(login, _id)
        elif self._type in [Types.Url(), Types.Id(), Types.Email()]:
            _str = str(self._object) if self._object else "───║───"
            _type = str(self._type)
            return "{}:{}".format(_type, _str)
        elif self._type == Types.Key():
            key = str(self._object.key) if self._object else ""
            _id = str(self._object.id) if self._object else "───║───"
            _type = str(self._type)
            return "{}:{}({})".format(_type, _id, key)
        elif self._type == Types.String():
            _str = str(self._object) if self._object else "───║───"
            return "'{}'".format(_str)
        elif self._type == Types.Null():
            return ""
        else:
            _str = str(self._object) if self._object else "───║───"
            return _str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Object): return False
        if self._type != other._type: return False
        return self._object == other._object

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def valueOf(string: str) -> 'Object':
        if Type.isurl(string):
            return Object("url", string)
        elif Type.isemail(string):
            return Object("email", string)
        elif Number.isnumber(string.split()):
            return Object(Types.Integer(), Number(string.split()))
        elif string.isnumeric():
            return Object(Types.Id(), string)
        else:
            return Object(Types.String(), string)

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
    @property
    def label(self) -> str:
        return self._label

    def __init__(self, label: str, _object: Object):
        super().__init__(_object._type, _object._object)
        self._label = label


null = Object(Types.Null(), None)
