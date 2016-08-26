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
        if word in Tables.types: result.append(word)
    return result


def lower_type(_type: str) -> str:
    _type.lower()
    if _type in Tables.types_synonyms: _type = Tables.types_synonyms[_type]["T"]
    return _type


def lower_object(_object: dict) -> dict:
    if _object["T"] in Tables.types_synonyms:
        synonym = Tables.types_synonyms[_object["T"]]
        return {"T": synonym["T"], "O": synonym["C"](_object["O"])}
    return None


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
