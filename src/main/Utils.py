

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

