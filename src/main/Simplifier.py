import re

from main.nlp.Number import Number
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
    if is_url(string):
        _type = "url"
    elif is_email(string):
        _type = "email"
    elif string.isnumeric():
        _type = "id"
    else:
        _type = "str"
    return {"T": [_type], "O": string}


def simplify_object(obj: dict) -> dict:
    _type = obj["T"][0]
    if _type in Tables.similar_types:
        synonym = Tables.similar_types[_type]
        obj["T"] = synonym["T"]
        obj["O"] = synonym["C"](obj["O"])
    return obj


def is_url(string: str) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, string) is not None


def is_email(string: str) -> bool:
    regex = re.compile("[^@]+@[^@]+\.[^@]+")
    return re.match(regex, string) is not None


def number(string: str) -> int:
    return int(Number(string.split())) - 1 if string != "last" else -1
