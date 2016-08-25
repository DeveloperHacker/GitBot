import re
import IO
import FlatMap
import Corrector
from GitConnector import GitConnector


def format_nick(nick, max_len) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick


def string(obj, _type="") -> str:
    if _type == "user":
        login = obj.login
        name = obj.name
        email = obj.email
        return "{}({}) {}".format(login, name if name else "───║───", email)
    elif _type == "repo":
        _id = obj.id
        name = obj.name
        login = obj.ovner.login
        return "{}'s {}({})".format(login, name, _id)
    elif _type == "gist":
        _id = obj.id
        login = obj.ovner.login
        return "{}'s gist id:{}".format(login, _id)
    else:
        return str(obj)


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self.connector = GitConnector()
        self.stored = {
            "user": None,
            "repo": None,
            "gist": None
        }
        self._flat_map = FlatMap.create(self)
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

    def _print(self, obj):
        IO.writeln(format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + str(obj))

    def _read(self) -> str:
        return IO.readln(format_nick(self._nick, self._max_nick_len) + "  ::  ")[:-1]

    def _hide_read(self) -> str:
        return IO.hreadln(format_nick(self._nick, self._max_nick_len) + "  ::  ")
    
    def _handle(self):
        data = self._read()
        parse = Corrector.parse(data)

        IO.writeln(Corrector.tree(parse))

        for vp in parse["VP"]:
            for node in vp["NP"]:
                args = self._build(node, [])
                for vb in vp["VB"]:
                    if vb not in self._functions: return
                    for arg in args: self._functions[vb](arg)

    # ToDo:
    def _build(self, node: dict, args: list) -> list:
        if "NN" in node:
            IO.writeln("───║───║───║───")
            IO.writeln(node)
            IO.writeln(args)
            return [{"T": "type", "O": "object"}]
        else:
            _args = [{**{"IN": pp["IN"]}, **arg} for pp in node["PP"] for np in pp["NP"] for arg in self._build(np, [])]
            return [arg for np in node["NP"] for arg in self._build(np, args + _args)]

    def _show(self, obj: dict):
        _type = obj["T"]
        match = re.match(r"list<(\w*)>", _type)
        if match:
            generic = match.group(1)
            for elem in obj["O"]: self._print(string(elem, generic))
        else:
            self._print(string(obj["O"], obj["T"]))

    def _store(self, obj: dict):
        _type = obj["T"]
        if _type in self.stored:
            self.stored[_type] = obj
            self._print("I remember it")
        else:
            self._print("I don't know who are you")

    def _login(self, _: dict):
        if self.connector.authorised():
            self._print("you need to unlogin before you login again")
        else:
            self._print("login:")
            login = self._read()
            self._print("password:")
            password = self._hide_read()
            if not self.connector.authorise(login, password):
                self._nick = self._default_nick
                self._print("Incorrect input: login or password")
            else:
                self._nick = self.connector.authorised()

    def _logout(self, _: dict):
        if self.connector.authorised():
            self.connector.logout()
            self._nick = self._default_nick

    def _close(self, _: dict):
        self._print("bye")
        self.stop()
