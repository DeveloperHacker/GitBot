synonyms = {
    "print": "show",
    "view": "show",
    "authorise": "login",
    "disconnect": "close",
    "repository": "repo",
    "project": "repo",
    "repositories": "repos",
    "projects": "repos",
    "storage": "repo",
    "recruited": "hireable",
    "organisations": "orgs",
    "remember": "store",
    "quit": "close"
}


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in synonyms: word = synonyms[word]
    return word


def simplify_exp(exp: list) -> list:
    return [simplify_word(word) for word in exp]


types = {
    "user",
    "repo",
    "gist",
    "name",
    "login",
    "key",
    "id",
    "str",
    "int"
}

types_synonyms = {
    "user": {"T": "login", "C": (lambda user: user.login)},
    "repo": {"T": "id", "C": (lambda repo: repo.id)},
    "gist": {"T": "id", "C": (lambda gist: gist.id)},
    "name": {"T": "str", "C": (lambda name: str(name))},
    "login": {"T": "str", "C": (lambda login: str(login))},
    "key": {"T": "str", "C": (lambda key: str(key))},
    "id": {"T": "int", "C": (lambda _id: int(_id))},
}


def extract_types(words: list) -> list:
    result = []
    for word in words:
        word = word.lower()
        if word in types: result.append(word)
    return result


def lower_type(_type: str) -> str:
    _type.lower()
    if _type in types_synonyms: _type = types_synonyms[_type]["T"]
    return _type


def lower_object(_object: dict) -> dict:
    if _object["T"] in types_synonyms:
        synonym = types_synonyms[_object["T"]]
        return {"T": synonym["T"], "O": synonym["C"](_object["O"])}
    return None
