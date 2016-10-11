import IO


class Stream:

    def __init__(self):
        self._stream = []

    def add(self, function, validate=lambda *inp: all([elem is not None for elem in list(inp)])):
        self._stream.append((validate, function))

    def run(self, *args):
        result = list(args)
        for (validate, function) in self._stream:
            if not validate(*result): return result
            result = [function(*result)]
            for res in result: IO.debug(res)
        return result
