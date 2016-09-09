import re

from src.main.nlp.Number import Number
from src.main.tree.Type import Type
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
        if word in Type.type_synonyms or word in Type.types:
            result.append(word)
    return result


def get_object(string: str):
    if is_url(string):
        type_name = "url"
    elif is_email(string):
        type_name = "email"
    elif string.isnumeric():
        type_name = "id"
    else:
        type_name = "str"
    return {"T": Type(type_name), "O": string}


def simplify_object(obj: dict) -> dict:
    _type = obj["T"]
    if _type in Tables.similar_types:
        synonym = Tables.similar_types[_type]
        obj["T"] = synonym["T"]
        obj["O"] = synonym["C"](obj["O"])
    elif _type[0] == "list":
        simple_type = "none"
        result = []
        for elem in obj["O"]:
            simple = simplify_object({"T": Type(*_type[1:]), "O": elem})
            simple_type = simple["T"]
            result.append(simple)
        obj["T"] = simple_type
        obj["O"] = result
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
