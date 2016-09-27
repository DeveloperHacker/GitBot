from nltk import Tree
from nltk.parse.stanford import StanfordParser as SParser
from main.interfaces.Parser import Parser, Node
import src.main.nlp


class StanfordNode(Node):
    def __init__(self, label: str):
        super().__init__(label)

    def _pformat_flat(self, node_separator, brackets, first):
        if self.isleaf(): return '{}{}'.format(self._label, node_separator)
        child_strings = [child._pformat_flat(node_separator, brackets, False) for child in self.children]
        if first: return '{}{} {}'.format(self._label, node_separator, ' '.join(child_strings))
        return '{}{}{} {}{}'.format(brackets[0], self._label, node_separator, ' '.join(child_strings), brackets[1])

    def pformat(self, margin=80, indent=0, node_separator='', brackets="()"):
        string = self._pformat_flat(node_separator, brackets, True)
        if len(string) + indent < margin: return string
        string = "{}{}".format(self._label, node_separator)
        for i, child in enumerate(self.children):
            edge = '├─ ' if i < len(self.children) - 1 else '└─ '
            string += '\n' + ' ' * indent + edge + child.pformat(margin, indent + 3, node_separator, brackets)
        return string + brackets[1]

    def __str__(self) -> str:
        return self.pformat()


class StanfordParser(Parser):
    fixable_sentence = {"NP", "FRAG", "UCP", "PP", "ADJP", "INTJ"}

    parser = SParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    @staticmethod
    def convert(tree: Tree) -> Node:
        root = StanfordNode(tree.label())
        for child in tree:
            if isinstance(child, str):
                root.add_child(StanfordNode(child))
            else:
                root.add_child(StanfordParser.convert(child))
        return root

    def parse(self, string: str) -> Node:
        if len(string.split()) == 0: return None
        root = next(StanfordParser.parser.raw_parse(string))[0]
        label = root.label()
        children = [node for node in root if not isinstance(node, str) and node.label() in ["VP"]]
        if label in StanfordParser.fixable_sentence | {"S"} and len(children) == 0:
            root = next(StanfordParser.parser.raw_parse("show " + string))[0]
        return StanfordParser.convert(root)

print(StanfordParser().parse("This is very tricky str method"))
