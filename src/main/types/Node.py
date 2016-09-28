from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    @property
    def label(self) -> str:
        return self._label

    def __init__(self, label: str):
        self._label = label

    @abstractmethod
    def children(self) -> dict:
        pass

    def __str__(self, shift=0) -> str:
        result = ["{\n"]
        for i, (key, col) in enumerate(sorted(self.children().items())):
            result.append("\t" * shift)
            result.append("'" + key + "': ")
            if key in {"NN", "JJ", "VB", "IN"} or len(col) == 0:
                result.append(", ".join([word.text for word in col]))
            else:
                result.append("[")
                for j, element in enumerate(col):
                    if isinstance(element, Node):
                        result.append(element.__str__(shift + 1))
                    else:
                        result.append(str(element))
                    if j < len(col) - 1: result.append(", ")
                result.append("]")
            result.append(",\n" if i < len(self.children()) - 1 else "\n")
        result.append("\t" * shift)
        result.append("}")
        return "".join(result)


class VerbPhrase(Node):
    def __init__(self, nps=None, pps=None, vbs=None):
        super().__init__("VP")
        self.nps = [] if nps is None else nps
        self.pps = [] if pps is None else pps
        self.vbs = [Verb(vb) for vb in vbs] if vbs is not None else []

    def children(self) -> dict:
        return {"NP": self.nps, "PP": self.pps, "VB": self.vbs}


class NounPhrase(Node):
    def __init__(self, nps=None, pps=None):
        super().__init__("NP")
        self.nps = [] if nps is None else nps
        self.pps = [] if pps is None else pps

    def children(self) -> dict:
        return {"NP": self.nps, "PP": self.pps}


class LeafNounPhrase(Node):
    def __init__(self, nn=None, jjs=None):
        super().__init__("LNP")
        self.nn = Noun(nn)
        self.jjs = [Adjective(jj) for jj in jjs] if jjs is not None else []

    def children(self) -> dict:
        return {"NN": [self.nn], "JJ": self.jjs}


class PrepositionalPhrase(Node):
    def __init__(self, pretext=None, nps=None):
        super().__init__("PP")
        self.pretext = Pretext(pretext)
        self.nps = [] if nps is None else nps

    def children(self) -> dict:
        return {"IN": [self.pretext], "NP": self.nps}


class Root(Node):
    def __init__(self, nps=None, vps=None):
        super().__init__("R")
        self.nps = [] if nps is None else nps
        self.vps = [] if vps is None else vps

    def children(self) -> dict:
        return {"NP": self.nps, "VP": self.vps}


class Word(Node, metaclass=ABCMeta):
    def __init__(self, label: str, text: str):
        super().__init__(label)
        self.text = text

    def children(self) -> dict:
        return {}


class Noun(Word):
    def __init__(self, text: str):
        super().__init__("NN", text)


class Adjective(Word):
    def __init__(self, text: str):
        super().__init__("JJ", text)


class Verb(Word):
    def __init__(self, text: str):
        super().__init__("VB", text)


class Pretext(Word):
    def __init__(self, text: str):
        super().__init__("IN", text)
