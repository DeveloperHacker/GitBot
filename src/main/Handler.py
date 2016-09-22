from copy import deepcopy
from github import GithubException

from src.main.types.Function import WFunction, NullFunction, Function
from src.main.types.Object import Object, LabeledObject
from src.main.types.Object import Null
from src import IO
from src.main import Simplifier
from src.main import Tables
from src.main.nlp import Corrector
from src.main.types.Types import Type
from src.main.types import Types
from src.main.Connector import Connector, NotAutorisedUserException
from src.main.Utils import difference


class Handler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._connector = Connector()
        self._storeds = Tables.create_storeds_map()
        self._builders = Tables.create_builders_map(lambda: self._connector, lambda _type: self._storeds[_type])
        self._functions = Tables.create_functions_map(lambda: self)
        self._type_builders = Tables.create_type_builders_mpa(lambda: self._connector)
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
        for string in str(obj).split("\n"):
            if string == "": continue
            IO.writeln(self.format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + string)

    def _read(self) -> str:
        return IO.readln(self.format_nick(self._nick, self._max_nick_len) + "  ::  ")

    def _hide_read(self) -> str:
        return IO.readln(self.format_nick("password", self._max_nick_len) + "  ::  ")
        # return IO.hreadln(self.format_nick(self._nick, self._max_nick_len) + "  ::  ")  # not work in pycharm console

    def _custom_read(self, prompt: str):
        return IO.readln(self.format_nick(prompt, self._max_nick_len) + "  ::  ")

    def _init_build(self, parse):
        if parse is None: return
        for vp in parse["VP"]:
            if len(vp["NP"]) == 0:
                for vb in vp["VB"]:
                    vb = Simplifier.simplify_word(vb)
                    if vb not in self._functions: continue
                    self._functions[vb](Null())
            else:
                for node in vp["NP"]:
                    args = self._build(node, [])
                    for vb in vp["VB"]:
                        vb = Simplifier.simplify_word(vb)
                        if vb not in self._functions: continue
                        for arg in args: self._functions[vb](arg)

    def _handle(self):
        data = self._read()
        parse = Corrector.parse(data)

        IO.debug(Corrector.tree(parse))

        try:
            self._init_build(parse)
        except GithubException as ex:
            if ex.status == 403:
                self._print(ex.data["message"])
            else:
                raise ex

    @staticmethod
    def distance(list1: list, list2: list) -> float:
        return abs(len(list1) - len(list2))

    def _execute(self, foo: Function, args: list):
        try:
            data = foo.run(*[arg.object for arg in args])
            if data is None:
                self._print("{} not found".format(str(foo.result).title()))
                return Null()
            else:
                return Object.create(foo.result, data)
        except GithubException as ex:
            if ex.status == 404:
                self._print("{} not found".format(str(foo.result).title()))
            else:
                raise ex
        except NotAutorisedUserException as _:
            self._print("I don't know who are you")
        return Null()

    def _get_relevant_shells(self, noun: str, adjectives: list) -> list:
        relevant_shells = []
        if noun in self._builders:
            shells = self._builders[noun]
            for shell in shells:
                set_shell_adjectives = set(shell["JJ"])
                conjunction = set_shell_adjectives & set(adjectives)
                if len(conjunction) == len(set_shell_adjectives):
                    relevant_shells.append(shell)
        return relevant_shells

    def _get_relevant_function(self, noun: str, adjectives: list, args: list) -> WFunction:
        relevant_function = NullFunction()
        relevant_shells = self._get_relevant_shells(noun, adjectives)
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
            adjectives = difference(adjectives, shell["JJ"])
            for function in shell["F"]:
                holes = list(deepcopy(function.args))
                relevant_args = []
                _args = list(deepcopy(args))
                primitives = False
                idle = False
                mass = 0
                fine = 1
                while not (idle and primitives) and len(holes) > 0 and len(_args) > 0:
                    primitives = True
                    idle = True
                    for i, arg in enumerate(_args):
                        if not arg.type.isprimitive(): primitives = False
                        if arg.type == holes[0]:
                            del holes[0]
                            del _args[i]
                            relevant_args.append(arg)
                            mass += (i + 1) * fine
                            idle = False
                            break
                    if idle:
                        for arg in _args: arg.simplify()
                        fine += 4

                    IO.debug(primitives, "primitives = {}")
                    IO.debug(idle, "idle = {}")
                    IO.debug(holes, "holes = {}")
                    IO.debug(_args, "_args = {}")
                    IO.debug("---------------------------")

                mass += len(_args)
                _args = [Object.valueOf(jj) for jj in adjectives]
                idle = False
                fine = 1
                if noun in self._type_builders and len(holes) == 1 and len(holes) == len(function.args):
                    temp_function = self._type_builders[noun]
                    if holes == list(temp_function.args): function = temp_function
                while not idle and len(holes) > 0 and len(_args) > 0:
                    idle = True
                    for i, arg in enumerate(reversed(_args)):
                        if arg.type == holes[0]:
                            del holes[0]
                            relevant_args.append(arg)
                            mass += (i + 1) * fine
                            idle = False
                            break
                    if idle: fine += 4
                mass -= 2 * len(function.args)
                if len(holes) > 0: mass = float("Inf")

                IO.debug(relevant_args, "args = {}")
                IO.debug(function, "function = {}")
                IO.debug(mass, "mass = {}")
                IO.debug("+++++++++++++++++++++++++++")

                if relevant_function.mass > mass: relevant_function = WFunction(mass, relevant_args, function)
        return relevant_function

    def _build(self, node: dict, args: list) -> list:
        if "NN" in node:
            string = node["NN"]
            noun = Simplifier.simplify_word(string)
            adjectives = Simplifier.simplify_exp(node["JJ"])
            types = Type.extract(adjectives)
            if len(types) == 1:
                type_name = str(types[0])
                if type_name in self._builders and noun not in self._builders:
                    adjectives.remove(type_name)
                    adjectives.append(string)
                    noun = type_name
            function = self._get_relevant_function(noun, adjectives, args)

            IO.debug(function, "relevant_function = {}")
            IO.debug("===========================")

            if function.mass < float("Inf"):
                constructed_object = self._execute(function, function.relevant_args)
            else:
                constructed_object = Object.valueOf(string)
            return [constructed_object]
        else:
            _args = [LabeledObject(pp["IN"], arg) for pp in node["PP"] for np in pp["NP"] for arg in
                     self._build(np, [])]
            return [arg for np in node["NP"] for arg in self._build(np, args + _args)]

    def show(self, obj: Object):
        if obj.type == Types.String():
            word = Simplifier.simplify_word(str(obj.object))
            if word in self._functions: self._functions[word](obj)
        else:
            string = str(obj)
            if not (string + ' ').isspace(): self._print(string)

    def store(self, obj: Object):
        if obj.type == Types.String() and obj.object == "me":
            try:
                self._storeds[Types.User()] = self._connector.user()
                self._print("I remember it")
            except NotAutorisedUserException as _:
                self._print("I don't know who are you")
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
