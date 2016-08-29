import re

from src import IO
from src.main import Simplifier
from src.main import Tables
from src.main.GitConnector import Connector
from src.main.nlp import Corrector


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._connector = Connector()
        self._stored = {
            "user": None,
            "repo": None,
            "gist": None
        }
        self._object_builders_map = Tables.create_object_builders_map((lambda: self._connector),
                                                                      (lambda _type: self._stored[_type]))
        self._functions = {
            "show": self._show,
            "store": self._store,
            "login": self._login,
            "logout": self._logout,
            "close": self._close
        }
        self._bot_nick = bot_nick
        self._nick = default_nick
        self._default_nick = default_nick
        self._max_nick_len = max_nick_len

    def start(self):
        self._connect = True
        self._print("hello")
        while self._connect: self._handle()

    def stop(self):
        self._connect = False

    @staticmethod
    def format_nick(nick: str, max_len: int) -> str:
        return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick

    def _print(self, obj):
        IO.writeln(self.format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + str(obj))

    def _read(self) -> str:
        return IO.readln(self.format_nick(self._nick, self._max_nick_len) + "  ::  ")

    def _hide_read(self) -> str:
        return IO.readln(self.format_nick(self._nick, self._max_nick_len) + "  ::  ")
        # return IO.hreadln(format_nick(self._nick, self._max_nick_len) + "  ::  ") # not work in pycharm console

    def _handle(self):
        data = self._read()
        parse = Corrector.parse(data)

        IO.writeln(Corrector.tree(parse))

        if parse is None: return
        for vp in parse["VP"]:
            for node in vp["NP"]:
                args = self._build(node, [])
                for vb in vp["VB"]:
                    if vb not in self._functions: return
                    for arg in args: self._functions[vb](arg)

    @staticmethod
    def distance(list1: list, list2: list) -> float:
        return abs(len(list1) - len(list2))

    def _build(self, node: dict, args: list) -> list:
        if "NN" in node:
            name = node["NN"]
            noun = Simplifier.simplify_word(name)
            adjectives = Simplifier.simplify_exp(node["JJ"])
            relevant_shells = []
            if noun in self._object_builders_map:
                shells = self._object_builders_map[noun]
                for shell in shells:
                    set_shell_adjectives = set(shell["JJ"])
                    conjunction = set_shell_adjectives & set(adjectives)
                    if len(conjunction) == len(set_shell_adjectives):
                        relevant_shells.append(shell)
            constructed_object = None
            if len(relevant_shells) != 0:
                min_shell = relevant_shells[0]
                min_dist = self.distance(adjectives, min_shell["JJ"])
                for i, shell in enumerate(relevant_shells):
                    if i == 0: continue
                    distance = self.distance(adjectives, shell["JJ"])
                    if distance < min_dist:
                        min_dist = distance
                        min_shell = shell
                shell = min_shell
                for function in shell["F"]:
                    # ToDo:
                    pass
            if constructed_object is None:
                types = Simplifier.extract_types(adjectives)
                if name.isnumeric():
                    _type = "int"
                    _value = int(name)
                elif Simplifier.is_url(name):
                    _type = "url"
                    _value = name
                else:
                    _type = "str"
                    _value = name
                if len(types) == 1 and types[0] in self._object_builders_map:
                    shells = self._object_builders_map[types[0]]
                    functions = []
                    for shell in shells:
                        if len(shell["JJ"]) == 0:
                            functions = shell["F"]
                            break
                    for function in functions:
                        _args = function["A"]
                        if len(_args) == 1 and _args[0] == _type:
                            constructed_object = function["B"](_value)
                            break
                if constructed_object is None:
                    constructed_object = {"T": [_type], "O": _value}
            return [constructed_object]
        else:
            _args = [{**{"IN": pp["IN"]}, **arg} for pp in node["PP"] for np in pp["NP"] for arg in self._build(np, [])]
            return [arg for np in node["NP"] for arg in self._build(np, args + _args)]

    @staticmethod
    def string(obj, _type="") -> str:
        if _type == "user":
            if obj is None: return "User ───║───"
            login = GitHandler.string(obj.login, "login")
            name = GitHandler.string(obj.name, "name")
            email = GitHandler.string(obj.email, "email")
            return "{}({}) {}".format(login, name, email)
        elif _type == "repo":
            if obj is None: return "Repo ───║───"
            login = GitHandler.string(obj.ovner.login, "login")
            name = GitHandler.string(obj.name, "name")
            _id = GitHandler.string(obj.id, "id")
            return "{}'s {}({})".format(login, name, _id)
        elif _type == "gist":
            if obj is None: return "Gist ───║───"
            login = GitHandler.string(obj.ovner.login, "login")
            _id = GitHandler.string(obj.id, "id")
            return "{}'s gist id:{}".format(login, _id)
        elif _type == "name":
            if obj is None: return "───║───"
            return str(obj).title()
        elif _type == "email":
            if obj is None: return "<───║───>"
            return '<' + str(obj) + '>'
        elif _type == "str":
            if obj is None: return '"───║───"'
            return '"' + str(obj) + '"'
        else:
            return str(obj)

    def _show(self, obj: dict):
        _type = obj["T"]
        if _type[0] == "list":
            for elem in obj["O"]: self._print(self.string(elem, _type[1]))
        else:
            self._print(self.string(obj["O"], _type[0]))

    def _store(self, obj: dict):
        _type = obj["T"]
        if _type in self._stored:
            self._stored[_type] = obj
            self._print("I remember it")
        else:
            self._print("I don't know who are you")

    def _login(self, _: dict):
        if self._connector.authorised():
            self._print("you need to unlogin before you login again")
        else:
            self._print("login:")
            login = self._read()
            self._print("password:")
            password = self._hide_read()
            if not self._connector.authorise(login, password):
                self._nick = self._default_nick
                self._print("Incorrect input: login or password")
            else:
                self._nick = self._connector.authorised()

    def _logout(self, _: dict):
        if self._connector.authorised():
            self._connector.logout()
            self._nick = self._default_nick

    def _close(self, _: dict):
        self._print("bye")
        self.stop()
