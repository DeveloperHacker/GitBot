import re


class Type:

    @property
    def blocks(self) -> tuple:
        return self._blocks

    def __init__(self, *args):
        self._blocks = tuple(Type.parse(list(args)))
        if len(self._blocks) == 0: raise Exception("Created empty type")

    def __str__(self) -> str:
        if len(self._blocks) == 0: return ""
        if self._blocks[0] == "list":
            return str(Type(*self._blocks[1:])) + "s"
        else:
            return " ".join(self._blocks).lower()

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
    def isurl(string: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, string) is not None

    @staticmethod
    def isemail(string: str) -> bool:
        regex = re.compile("[^@]+@[^@]+\.[^@]+")
        return re.match(regex, string) is not None

    @staticmethod
    def extract(words: list) -> list:
        result = []
        for word in words:
            word = word.lower()
            if word in Type.type_synonyms or word in Type.types:
                result.append(Type(word))
        return result

    def isprimitive(self) -> bool:
        return all([block in Type.primitive_types for block in self._blocks])

    types = {
        "user", "repo", "gist", "name", "login", "key", "id", "url", "email", "number",
        "null", "list", "str"
    }

    primitive_types = {
        "null", "list", "str"
    }

    type_synonyms = {
        "users": ["list", "user"],
        "repos": ["list", "repo"],
        "gists": ["list", "gist"],
        "keys": ["list", "key"]
    }