from src.main.tree.Types import Type


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

    def __init__(self, result_type: Type, arg_types: list, body):
        self._result = result_type
        self._args = tuple(arg_types)
        self._body = body

    def run(self, *args):
        return self._body(*args)
