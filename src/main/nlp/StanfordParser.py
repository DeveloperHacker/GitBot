from nltk import Tree
from nltk.parse.stanford import StanfordParser as SParser

from src import IO
from src.main.interfaces.Parser import Parser, Node


class StanfordNode(Node):

    def __init__(self, label: str):
        super().__init__(label)

    def _pformat_flat(self, node_separator, brackets, first):
        if self.isleaf(): return '{}{}'.format(self._label, node_separator)
        child_strings = [child._pformat_flat(node_separator, brackets, False) for child in self.children()]
        if first: return '{}{} {}'.format(self._label, node_separator, ' '.join(child_strings))
        return '{}{}{} {}{}'.format(brackets[0], self._label, node_separator, ' '.join(child_strings), brackets[1])

    def pformat(self, margin=80, indent=0, node_separator='', brackets="()"):
        string = self._pformat_flat(node_separator, brackets, True)
        if len(string) + indent < margin: return string
        string = "{}{}".format(self._label, node_separator)
        for i, child in enumerate(self.children()):
            edge = '├─ ' if i < len(self.children()) - 1 else '└─ '
            string += '\n' + ' ' * indent + edge + child.pformat(margin, indent + 3, node_separator, brackets)
        return string + brackets[1]

    def __str__(self) -> str:
        return self.pformat()

    def isleaf(self) -> bool:
        return all([isinstance(child, str) for child in self.children()])

    def flatten(self) -> list:
        return [word for child in self.children() for word in ([child] if isinstance(child, str) else child.flatten())]


class StanfordParser(Parser):
    fixable_sentence = {"NP", "FRAG", "UCP", "PP", "ADJP", "INTJ"}

    parser = SParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    @staticmethod
    def convert(tree: Tree) -> Node:
        root = StanfordNode(tree.label())
        for child in tree: root.append(child if isinstance(child, str) else StanfordParser.convert(child))
        return root

    def parse(self, string: str) -> Node:
        if len(string.split()) == 0: return None
        root = next(StanfordParser.parser.raw_parse(string))[0]
        label = root.label()
        children = [node for node in root if not isinstance(node, str) and node.label() in ["VP"]]
        if label in StanfordParser.fixable_sentence | {"S"} and len(children) == 0:
            root = next(StanfordParser.parser.raw_parse("show " + string))[0]
        IO.log(root.label().lower() + ".txt", str(root))
        return StanfordParser.convert(root)
