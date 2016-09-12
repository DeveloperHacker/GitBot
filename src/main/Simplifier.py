from src.main.nlp.Number import Number
from src.main import Tables


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in Tables.synonyms: word = Tables.synonyms[word]
    return word


def simplify_exp(exp: list) -> list:
    return [simplify_word(word) for word in exp]


def number(string: str) -> int:
    return int(Number(string.split())) - 1 if string != "last" else -1
