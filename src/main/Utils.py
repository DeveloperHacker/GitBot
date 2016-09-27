from copy import deepcopy


def subclasses(_class) -> set:
    _subclasses = set()
    work = [_class]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in _subclasses:
                _subclasses.add(child)
                work.append(child)
    return _subclasses


def string(collection) -> str:
    if type(collection) == list:
        result = ["'{}'".format(elem) if type(elem) == str else string(elem) for elem in collection]
        return "[{}]".format(', '.join(result))
    if type(collection) == tuple:
        result = ["'{}'".format(elem) if type(elem) == str else string(elem) for elem in collection]
        return "({})".format(', '.join(result))
    if type(collection) == set:
        result = ["'{}'".format(elem) if type(elem) == str else string(elem) for elem in collection]
        return "{{{}}}".format(', '.join(result))
    if type(collection) == dict:
        result = []
        for key, value in collection.items():
            key = "'{}'".format(key) if type(key) == str else string(key)
            value = "'{}'".format(value) if type(value) == str else string(value)
            result.append("{}: {}".format(key, value))
        return "{{{}}}".format(', '.join(result))
    else:
        return str(collection)


def format(form: str, *args):
    return form.format(*[string(arg) for arg in args])


def format_nick(nick: str, max_len: int) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick