from copy import deepcopy

from nltk.parse.stanford import StanfordParser, StanfordDependencyParser

from src.main.interfaces.Corrector import Corrector
from src.main.types.Node import *
from src import IO

sp = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sdp = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

phrase_level = {
    "ADJP", "ADVP", "CONJR", "FRAG", "INTJ", "LST", "NAC", "NP", "NX", "PP", "PRN", "PRT", "QP", "RRC", "UCP", "VP",
    "WHADJP", "WHAVP", "WHNP", "WHPP", "X"
}

clause_level = {
    "S", "SBAR", "SBARQ", "SINV", "SQ"
}

word_level = {
    "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP",
    "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"
}

conjunction_level = {"CC", ","}

belongs_words = {"in", "into", "at", "for", "of", "'s"}

fixable_sentence = {"NP", "FRAG", "UCP", "PP", "ADJP", "INTJ"}


class StanfordCorrector(Corrector):
    def correct(self, parsed: Node) -> Root:
        root = None
        if parsed.label in ["S", "SINV"]:
            root = _parse_sentence(parsed)
            if root.label == "SINV":
                for vp in root.vps: vp.nps.extend(root.nps)
                root.nps = []
        return root


def _subtrees(tree, labels: list) -> list:
    return [node for node in tree if not isinstance(node, str) and node.label() in labels]


def _trees(tree, labels: list) -> list:
    trees = [t for node in tree if not isinstance(node, str) for t in _trees(node, labels)]
    return _subtrees(tree, labels) + trees


def _parse_collocation(collocation: list) -> LeafNounPhrase:
    if len(collocation) == 0: raise Exception()
    if len(collocation) == 1: return LeafNounPhrase(collocation[0])
    np = LeafNounPhrase()
    for i, node in next(sdp.raw_parse(" ".join(collocation))).nodes.items():
        if node["word"] is None: continue
        if node["head"] == 0:
            np.nn = Noun(node["word"])
        else:
            np.jjs.append(Adjective(node["word"]))
    return np


def _parse_pp(tree) -> list:
    pps = []
    for pp in _subtrees(tree, ["PP"]):
        _in = [_in[0] for _in in _subtrees(pp, ["IN"])]
        len_pps = len(_subtrees(pp, ["PP"]))
        len_in = len(_in)
        if len_pps > 0 and len_in == 0:
            pps.extend(_parse_pp(pp))
        elif len_pps == 0 and len_in > 0:
            (_nps, _rpp) = _parse_np(pp)
            pps.extend(_rpp)
            pps.append(PrepositionalPhrase(_in[0], _nps))
        else:
            _in = _in[0]
            collocation = []
            first_in = True
            for word in list(pp.flatten()):
                if first_in and word == _in:
                    first_in = False
                else:
                    collocation.append(word)
            pps.append(PrepositionalPhrase(_in, [_parse_collocation(collocation)]))
    return pps


def combine(inp: list) -> list:
    if len(inp) == 0: return [[]]
    result = deepcopy(inp)
    while len(result) > 1:
        result[0] = [i + j for i in result[0] for j in result[1]]
        del result[1]
    return result[0]


def _parse_lnp(tree) -> (list, list):
    rpp = []
    collocations = [[]]
    jjsss = []
    for node in tree:
        label = node.label()
        if label in conjunction_level:
            collocations.append([])
        elif label in word_level:
            collocations[-1].append(node)
        elif label == "ADJP":
            jjss = [[]]
            for jj in node:
                label = jj.label()
                if label in conjunction_level:
                    jjss.append([])
                elif label in word_level:
                    jjss[-1].append(jj[0])
            jjsss.append([jjs for jjs in jjss if len(jjs) != 0])
    jjss = combine([jjss for jjss in jjsss if len(jjss) != 0])
    collocations = [collocation for collocation in collocations if len(collocation) != 0]
    nps = []
    for collocation in collocations:
        _in = []
        _collocation = []
        for node in collocation:
            if node.label() == "POS":
                _in.append(node[0])
            else:
                _collocation.append(node[0])
        if len(_in) > 0:
            rpp.append(PrepositionalPhrase(_in[0], [_parse_collocation(_collocation)]))
        else:
            parsed = _parse_collocation(_collocation)
            noun = parsed.nn.text
            jjs = [jj.text for jj in parsed.jjs]
            nps.extend([LeafNounPhrase(noun, jjs + _jjs) for _jjs in jjss])
    return nps, rpp


def _parse_np(tree) -> (list, list):
    result = []
    rpp = []
    for node in tree:
        label = node.label()
        if label == "NP":
            (nps, _rpp) = _parse_lnp(node)
            rpp.extend(_rpp)
            (_nps, pps) = _parse_np(node)
            nps.extend(_nps)
            pps.extend(_parse_pp(node))
            result.extend(nps if len(pps) == 0 else [NounPhrase(nps, pps)])
        elif label in (phrase_level | clause_level) - {"VP", "PP"}:
            result.append(_parse_collocation(node.flatten()))
    return result, rpp


def _parse_sentence(tree) -> Root:
    (_nps, _rpp) = _parse_np(tree)
    root = Root(_nps if len(_rpp) == 0 else [NounPhrase(_nps, _rpp)])
    for vp in _trees(tree, ["VP"]):
        (nps, pps) = _parse_np(vp)
        pps.extend(_parse_pp(vp))
        verb_phrase = VerbPhrase()
        verb_phrase.nps = nps if len(pps) == 0 else [NounPhrase(nps, pps)]
        verb_phrase.vbs = [Verb(vb[0]) for vb in _subtrees(vp, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])]
        root.vps.append(verb_phrase)
    return root


# ToDo:
def _hard_convert(tree) -> Root:
    return None


def parse(string: str) -> Root:
    if len(string.split()) == 0: return None
    sp_tree = next(sp.raw_parse(string))[0]
    label = sp_tree.label()
    tmp = sp_tree
    if label in fixable_sentence | {"S"} and len(_subtrees(sp_tree, ["VP"])) == 0:
        sp_tree = next(sp.raw_parse("show " + string))[0]
        label = sp_tree.label()
    if label in clause_level:
        IO.log(label.lower() + ".txt", str(sp_tree))
    if label in ["S", "SINV"]:
        root = _parse_sentence(sp_tree)
        if label == "SINV":
            for vp in root.vps: vp.nps.extend(root.nps)
            root.nps = []
    else:
        root = _hard_convert(tmp)
    IO.debug(sp_tree)
    IO.debug(root)
    return root
