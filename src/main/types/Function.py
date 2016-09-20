from src.main.types.Types import Type, Null
from src.main import Utils


class Function:
    @property
    def result(self) -> Type:
        return self._result

    @property
    def args(self) -> tuple:
        return self._args

    @property
    def body(self):
        return self._body

    def __init__(self, args: list, result: Type, body):
        self._result = result
        self._args = tuple(args)
        self._body = body

    def run(self, *args):
        return self._body(*args)

    def __str__(self):
        return Utils.format("Function(args={}, result={}, body={})", self._args, self._result, self._body)


class WFunction(Function):
    @property
    def mass(self):
        return self._mass

    @property
    def relevant_args(self):
        return self._relevant_args

    def __init__(self, mass: float, relevant_args: list, function: Function):
        super().__init__(function.args, function.result, function.body)
        self._mass = mass
        self._relevant_args = tuple(relevant_args)

    def __str__(self):
        return Utils.format("WFunction(mass={}, relevant_args={}, args={}, result={}, body={})",
                            self._mass, self._relevant_args, self._args, self._result, self._body)


class NullFunction(WFunction):
    @property
    def result(self) -> Type:
        raise Exception("Unsupported operation")

    @property
    def args(self) -> tuple:
        raise Exception("Unsupported operation")

    @property
    def body(self):
        raise Exception("Unsupported operation")

    @property
    def relevant_args(self):
        raise Exception("Unsupported operation")

    def __init__(self):
        super().__init__(float("inf"), [], Function(Null(), [], None))

    def __str__(self):
        return Utils.format("NullFunction(mass={})", self._mass)
