from github import GithubException

from src.main.interfaces.Handler import Handler
from src.main.interfaces.Executor import Executor
from src.main.nlp.EvaluationBuilder import EvaluationBuilder
from src.main.nlp.StanfordCorrector import StanfordCorrector
from src.main.nlp.StanfordParser import StanfordParser
from src.main.types import Types
from src.main.types.Object import Object
from src.main.Connector import Connector, NotAutorisedUserException
from src.main import Simplifier
from src.main import Tables
from src.main import Utils
from src import IO


class Bot(Handler, Executor):

    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        super().__init__()
        self._bot_nick = bot_nick
        self._nick = default_nick
        self._default_nick = default_nick
        self._max_nick_len = max_nick_len
        self._connect = False
        self._connector = Connector()
        self._storeds = Tables.create_storeds_map()
        self._functions = Tables.create_functions_map(lambda: self)
        self._parser = StanfordParser()
        self._corrector = StanfordCorrector()
        self._builder = EvaluationBuilder(lambda: self._connector, lambda _type: self._storeds[_type])

    def _print(self, obj):
        for string in str(obj).split("\n"):
            if string == "": continue
            IO.writeln(Utils.format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + string)

    def _read(self) -> str:
        return IO.readln(Utils.format_nick(self._nick, self._max_nick_len) + "  ::  ")

    def _hide_read(self) -> str:
        return IO.readln(Utils.format_nick("password", self._max_nick_len) + "  ::  ")
        # return IO.hreadln(self.format_nick(self._nick, self._max_nick_len) + "  ::  ")  # not work in pycharm console

    def _custom_read(self, prompt: str):
        return IO.readln(Utils.format_nick(prompt, self._max_nick_len) + "  ::  ")

    def _start(self):
        self._print("hello")

    def _stop(self): pass

    def handle(self):
        try:
            data = self._read()
            parse = self._parser.parse(data)
            IO.debug(parse)
            root = self._corrector.correct(parse)
            IO.debug(root)
            closures = self._builder.build(root)
            IO.debug(closures)
            self.execute(closures)
        except NotAutorisedUserException as _:
            self._print("I don't know who are you")
        except GithubException as ex:
            if ex.status == 403:
                self._print(ex.data["message"])
            else:
                raise ex
        except EvaluationBuilder.NotFoundException as ex:
            self._print("{} not found".format(str(ex.think).title()))

    def execute(self, closures: list):
        closures = {closure.name: arg for closure in closures if closure.name in self._functions for arg in closure.args}
        for name, arg in closures.items(): self._functions[name](arg)

    def show(self, obj: Object):
        if obj.type == Types.String():
            word = Simplifier.simplify_word(str(obj.object))
            if word in self._functions: self._functions[word](obj)
        else:
            string = str(obj)
            if not (string + ' ').isspace(): self._print(string)

    def store(self, obj: Object):
        if obj.type == Types.String() and obj.object == "me":
            self._storeds[Types.User()] = self._connector.user()
            self._print("I remember it")
        elif obj.type in self._storeds:
            self._storeds[obj.type] = obj.object
            self._print("I remember it")
        else:
            self._print("I can not remember " + str(obj.type))

    def log(self, obj: Object):
        if obj.type != Types.String(): return
        value = obj.object
        if value == "out":
            self.logout(obj)
        elif value == "in":
            self.login(obj)

    def logout(self, _: Object):
        if self._connector.authorised():
            self._connector.logout()
            self._nick = self._default_nick

    def login(self, _: Object):
        if self._connector.authorised():
            self._print("logout before you login again")
        else:
            self._print("enter your login for github")
            login = self._custom_read("login")
            self._print("enter password")
            password = self._hide_read()
            if not self._connector.isauthorised(login, password):
                self._nick = self._default_nick
                self._print("incorrect login or password")
            else:
                self._nick = self._connector.authorised()

    def hello(self, _: Object):
        self._print("=)")

    def bye(self, _: Object):
        self._print("bye")
        self.stop()
