from main.types.Node import LeafNounPhrase
from src.main.types.Types import Type
from src.main.nlp.Number import Number
from src.main import Tables


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in Tables.synonyms: word = Tables.synonyms[word]
    return word


def simplify_adjectives(jjs: list) -> list:
    return [simplify_word(jj.text) for jj in jjs]


def simplify(node: LeafNounPhrase) -> (str, str, list, list):
    string = node.nn.text
    noun = simplify_word(string)
    adjectives = simplify_adjectives(node.jjs)
    types = Type.extract(adjectives)
    return string, noun, adjectives, types


def number(string: str) -> int:
    return int(Number(string.split())) - 1 if string != "last" else -1
