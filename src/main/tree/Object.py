from src.main.nlp.Number import Number
from src.main.tree.Function import Function
from src.main.tree.Type import Type


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
            result = [str(Object(Type(*self._type[1:]), elem)) for elem in self._object]
            if len(self._object) == 0:
                return "{} not found".format(str(self._type))
            else:
                return '\n'.join(result)
        elif self._type == Type("user"):
            login = str(Object(Type("login"), self._object.login))
            name = str(Object(Type("name"), self._object.name))
            email = str(Object(Type("email"), self._object.email))
            return "{}({}) <{}>".format(login, name, email)
        elif self._type == Type("repo"):
            login = str(Object(Type("login"), self._object.owner.login))
            name = str(Object(Type("name"), self._object.name))
            _id = str(Object(Type("id"), self._object.id))
            return "{}'s repo {}({})".format(login, name, _id)
        elif self._type == Type("gist"):
            login = str(Object(Type("login"), self._object.owner.login))
            _id = str(Object(Type("id"), self._object.id))
            return "{}'s gist {}".format(login, _id)
        elif self._type in [Type("url"), Type("id"), Type("email")]:
            _str = str(self._object) if self._object else "───║───"
            _type = str(self._type)
            return "{}:{}".format(_type, _str)
        elif self._type == Type("key"):
            key = str(self._object.key) if self._object else ""
            _id = str(self._object.id) if self._object else "───║───"
            _type = str(self._type)
            return "{}:{}({})".format(_type, _id, key)
        elif self._type == Type("str"):
            _str = str(self._object) if self._object else "───║───"
            return "'{}'".format(_str)
        elif self._type == Type("null"):
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
            return Object(Type("number"), Number(string.split()))
        elif string.isnumeric():
            return Object(Type("id"), string)
        else:
            return Object(Type("str"), string)

    def simplify(self) -> 'Object':
        if self._type in Object._similar_types:
            simple = Object._similar_types[self._type]
            self._type = simple.result
            self._object = simple.run(self._object)
        elif self._type[0] == "list":
            simple_type = Type("null")
            result = []
            self._object = list(self._object)
            for elem in self._object:
                simple = Object(Type(*self._type[1:]), elem).simplify()
                simple_type = simple._type
                result.append(simple._object)
            self._type = Type("list", *simple_type.blocks)
            self._object = result
        return self

    _similar_types = {
        Type("user"): Function(Type("login"), [Type("user")], lambda user: user.login),
        Type("repo"): Function(Type("id"), [Type("repo")], lambda repo: repo.id),
        Type("gist"): Function(Type("id"), [Type("gist")], lambda gist: gist.id),
        Type("name"): Function(Type("str"), [Type("name")], lambda name: str(name)),
        Type("login"): Function(Type("str"), [Type("login")], lambda login: str(login)),
        Type("url"): Function(Type("str"), [Type("url")], lambda url: str(url)),
        Type("email"): Function(Type("str"), [Type("email")], lambda email: str(email)),
        Type("key"): Function(Type("str"), [Type("key")], lambda key: str(key)),
        Type("id"): Function(Type("str"), [Type("id")], lambda _id: str(_id))
    }


class LabeledObject(Object):
    @property
    def label(self) -> str:
        return self._label

    def __init__(self, label: str, _object: Object):
        super().__init__(_object._type, _object._object)
        self._label = label


null = Object(Type("null"), None)
