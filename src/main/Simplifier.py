import re
from src.main import Tables


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in Tables.synonyms: word = Tables.synonyms[word]
    return word


def simplify_exp(exp: list) -> list:
    return [simplify_word(word) for word in exp]


def extract_types(words: list) -> list:
    result = []
    for word in words:
        word = word.lower()
        if word in Tables.type_synonyms or word in Tables.types:
            result.append(word)
    return result


def get_object(string: str):
    if string.isnumeric():
        _type = "int"
        _value = int(string)
    elif is_url(string):
        _type = "url"
        _value = string
    else:
        _type = "str"
        _value = string
    return {"T": [_type], "O": _value}


def simplify_object(obj: dict) -> dict:
    _type = obj["T"][0]
    if _type in Tables.similar_types:
        synonym = Tables.similar_types[_type]
        obj["T"] = synonym["T"]
        obj["O"] = synonym["C"](obj["O"])
    return obj


def is_url(string: str) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    match = re.match(regex, string)
    return match is not None