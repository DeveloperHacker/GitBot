import re

from src.main.nlp.Number import Number


class Type:
    def __init__(self, *args):
        self._blocks = Type.parse(list(args))
        if len(self._blocks) == 0: raise Exception("Created empty type")

    def __str__(self) -> str:
        return Type.string(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]

    def __eq__(self, other):
        if not isinstance(other, Type): return False
        if len(self._blocks) != len(other._blocks): return False
        return all([e1 == e2 for e1, e2 in zip(self._blocks, other._blocks)])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def parse(words: list) -> list:
        result = []
        for word in words:
            word = word.lower()
            if word in Type.types: result.append(word)
            elif word in Type.type_synonyms: result.extend(Type.type_synonyms[word])
            elif not word: continue
            else: raise Exception("Type \"{}\" not found".format(word))
        return result

    @staticmethod
    def type(string: str):
        if Type.url(string): return {"T": ["url"], "O": string}
        elif Type.email(string): return {"T": ["email"], "O": string}
        elif Number.is_number(string.split()): return {"T": ["number"], "O": string}
        elif string.isnumeric(): return {"T": ["id"], "O": string}
        else: return {"T": ["str"], "O": string}

    @staticmethod
    def url(string: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, string) is not None

    @staticmethod
    def email(string: str) -> bool:
        regex = re.compile("[^@]+@[^@]+\.[^@]+")
        return re.match(regex, string) is not None

    @staticmethod
    def string(words: list):
        if len(words) == 0: return ""
        if words[0] == "list":
            return Type.string(words[1:]) + "s"
        elif words[0] in Type.primitive_types:
            return " ".join(words).lower()
        else:
            return " ".join(words).title()

    def primitive(self) -> bool:
        return all([block in Type.primitive_types for block in self._blocks])

    types = {
        "user", "repo", "gist", "name", "login", "key", "id", "url", "email",
        "none", "list", "str"
    }

    primitive_types = {
        "none", "list", "str"
    }

    type_synonyms = {
        "repos": ["list", "repo"],
        "gists": ["list", "gist"],
        "keys": ["list", "key"]
    }