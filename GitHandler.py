from Tools.scripts.treesync import raw_input
from getpass import getpass

import Parser
from GitConnector import GitConnector
from Simplifies import simplify


def format_nick(nick, max_len) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._authorised = False
        self._connector = GitConnector()
        self._commands = {
            "show": self.show,
            "login": self.login,
            "unlogin": self.unlogin,
            "close": self.close
        }
        self._bot_nick = bot_nick
        self._nick = default_nick
        self._default_nick = default_nick
        self._max_nick_len = max_nick_len

    def start(self):
        self._connect = True
        while self._connect: self.handle()

    def stop(self):
        self._connect = False

    def print(self, obj):
        print(format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + obj.__str__())

    def read(self) -> str:
        return raw_input(format_nick(self._nick, self._max_nick_len) + "  ::  ")[:-1]

    def handle(self):
        data = self.read()
        parse = Parser.parse_string(data)
        print(parse)
        if parse is None: return
        for action in parse.actions:
            name = simplify(action.name)
            if name in self._commands: self._commands[name](action)

    def n_print(self, preps: list, foo):
        if len(preps) == 0 and self._authorised:
            self.print(foo())
        elif len(preps) == 1:
            self.print(foo(preps[0][0]))
        else:
            for prep in preps: self.print(prep[0] + ": " + foo(prep[0]))

    def show(self, action: Parser.Action):
        for obj in action.objects:
            obj = simplify(obj)
            if obj == "repos":
                self.n_print(action.preps, lambda n=None: ", ".join([repo.name for repo in self._connector.repositories(n)]))
            elif obj == "url":
                self.n_print(action.preps, lambda n=None: self._connector.url(n))

    def login(self, parse: Parser.Action):
        self.print("login:")
        login = self.read()
        self.print("password:")
        pword = self.read()
        self._nick = self._connector.login(login, pword)
        self._authorised = True
        if self._nick is None:
            self._authorised = False
            self._nick = self._default_nick
            self.print("Incorrect input: login or password")

    def unlogin(self, parse: Parser.Action):
        self._connector.unlogin()
        self._authorised = False
        self._nick = self._default_nick

    def close(self, parse: Parser.Action):
        self.stop()
