from copy import deepcopy
from github import GithubException

from src.main.interfaces.Builder import Builder, Closure
from src.main.types import Types
from src.main.types.Node import *
from src.main.types.Shell import Shell
from src.main.types.Object import Object, Null
from src.main.types.Function import WFunction, NullFunction, Function
from src.main import Simplifier
from src.main import Tables
from src import IO


class EvaluationBuilder(Builder):

    class NotFoundException(Exception):
        @property
        def think(self):
            return self._think

        def __init__(self, think):
            super().__init__(str(think))
            self._think = think

    def __init__(self, get_connector, get_stored):
        self._builders = Tables.create_builders_map(get_connector, get_stored)
        self._type_builders = Tables.create_type_builders_mpa(get_connector)

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

    def build(self, root: Root) -> list:
        if root is None: return
        closures = []
        for vp in root.vps:
            args = [self._build(node, []) for node in vp.nps] if len(vp.nps) > 0 else [Null()]
            closures.extend([Closure(Simplifier.simplify_word(vb.text), arg) for arg in args for vb in vp.vbs])
        return closures

    @staticmethod
    def _execute(foo: Function, args: list):
        try:
            data = foo.run(*[arg.object for arg in args])
            if data is None: raise EvaluationBuilder.NotFoundException(foo.result)
        except GithubException as ex:
            raise EvaluationBuilder.NotFoundException(foo.result) if ex.status == 404 else ex
        else:
            return Object.create(foo.result, data)

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
