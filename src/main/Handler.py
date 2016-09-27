from copy import deepcopy
from github import GithubException

from src.main.types import Types
from src.main.types.Node import *
from src.main.types.Shell import Shell
from src.main.types.Object import Object, Null
from src.main.types.Function import WFunction, NullFunction, Function
from src.main.Connector import Connector, NotAutorisedUserException
from src.main.nlp import Corrector
from src.main import Simplifier
from src.main import Tables
from src.main import Utils
from src import IO


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

    def _init_build(self, root: Root) -> list:
        if root is None: return
        result = []
        for vp in root.vps:
            if len(vp.nps) == 0:
                for vb in vp.vbs:
                    vb = Simplifier.simplify_word(vb.text)
                    if vb not in self._functions: continue
                    result.append((self._functions[vb], Null()))
            else:
                for node in vp.nps:
                    args = self._build(node, [])
                    for vb in vp.vbs:
                        vb = Simplifier.simplify_word(vb.text)
                        if vb not in self._functions: continue
                        result.extend([(self._functions[vb], arg) for arg in args])
        return result

    def _handle(self):
        try:
            data = self._read()
            root = Corrector.parse(data)
            functions = self._init_build(root)
            for function in functions: function[0](function[1])
        except GithubException as ex:
            if ex.status == 403:
                self._print(ex.data["message"])
            else:
                raise ex

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
        set_adjectives = set(adjectives)
        if noun in self._builders:
            shells = self._builders[noun]
            for shell in shells:
                set_shell_adjectives = set(shell.adjectives)
                conjunction = set_shell_adjectives & set_adjectives
                if len(conjunction) == len(set_shell_adjectives): relevant_shells.append(shell)
        return relevant_shells

    def _get_relevant_shell(self, noun: str, adjectives: list) -> Shell:
        relevant_shells = self._get_relevant_shells(noun, adjectives)
        if len(relevant_shells) == 0: return None
        min_shell = relevant_shells[0]
        min_dist = min_shell.distance(adjectives)
        for i, shell in enumerate(relevant_shells):
            if i == 0: continue
            distance = shell.distance(adjectives)
            if distance < min_dist:
                min_dist = distance
                min_shell = shell
        return min_shell

    @staticmethod
    def _get_arguments(arguments: list, holes: list):
        arguments = list(deepcopy(arguments))
        relevant_arguments = []
        mass = 0
        primitives = False
        idle = False
        fine = 1
        while not (idle and primitives) and len(holes) > 0 and len(arguments) > 0:
            primitives = True
            idle = True
            for i, argument in enumerate(arguments):
                if not argument.type.isprimitive(): primitives = False
                if argument.type == holes[0]:
                    del holes[0]
                    del arguments[i]
                    relevant_arguments.append(argument)
                    mass += (i + 1) * fine
                    idle = False
                    break
            if idle:
                arguments = [argument.simplify() for argument in arguments]
                fine += 4
            IO.debug("primitives = {}", primitives)
            IO.debug("idle = {}", idle)
            IO.debug("holes = {}", holes)
            IO.debug("arguments = {}", arguments)
            IO.debug("---------------------------")
        return relevant_arguments, mass

    def _get_relevant_function(self, noun: str, adjectives: list, functions: list, arguments: list) -> WFunction:
        relevant_function = NullFunction()
        for function in functions:
            holes = list(deepcopy(function.args))
            IO.debug(holes)
            IO.debug(arguments)
            IO.debug(adjectives)
            IO.debug(list(reversed([Object.valueOf(jj) for jj in adjectives])))
            relevant_arguments, mass = self._get_arguments(arguments, holes)
            if noun in self._type_builders and len(holes) == 1 and len(function.args) == 1:
                temp_function = self._type_builders[noun]
                if holes == list(temp_function.args): function = temp_function
            pair = self._get_arguments(list(reversed([Object.valueOf(jj) for jj in adjectives])), holes)
            relevant_arguments.extend(pair[0])
            mass += pair[1] - 2 * len(function.args)
            IO.debug("function = {}", function)
            IO.debug("relevant_arguments = {}", relevant_arguments)
            IO.debug("relevant_function = {}", relevant_function)
            IO.debug("mass = {}", mass if len(holes) == 0 else float("inf"))
            IO.debug("+++++++++++++++++++++++++++")
            if len(holes) == 0 and relevant_function.mass > mass:
                relevant_function = WFunction(mass, relevant_arguments, function)
        return relevant_function

    def _build(self, node: NounPhrase, args: list) -> list:
        if isinstance(node, LeafNounPhrase):
            string = node.nn.text
            noun = Simplifier.simplify_word(string)
            adjectives = Simplifier.simplify_adjectives(node.jjs)
            type_names = [str(type) for type in Types.Type.extract(adjectives)]
            if len(type_names) == 1 and type_names[0] in self._builders and noun not in self._builders:
                adjectives.remove(type_names[0])
                adjectives.append(string)
                noun = type_names[0]
            constructed_object = None
            function = NullFunction()
            shell = self._get_relevant_shell(noun, adjectives)
            if shell is not None:
                adjectives = shell.difference(adjectives)
                function = self._get_relevant_function(noun, adjectives, shell.functions, args)
                if function.mass < float("inf"): constructed_object = self._execute(function, function.relevant_args)
            if constructed_object is None: constructed_object = Object.valueOf(string)
            IO.debug("relevant_function = {}", function)
            IO.debug("===========================")
            return [constructed_object]
        else:
            _args = [arg.mark(pp.pretext) for pp in node.pps for np in pp.nps for arg in self._build(np, [])]
            return [arg for np in node.nps for arg in self._build(np, args + _args)]

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
