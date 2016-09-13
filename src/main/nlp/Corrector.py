from copy import deepcopy
from nltk.parse.stanford import StanfordParser, StanfordDependencyParser
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


def _subtrees(tree, labels: list) -> list:
    return [node for node in tree if not isinstance(node, str) and node.label() in labels]


def _trees(tree, labels: list) -> list:
    trees = [t for node in tree if not isinstance(node, str) for t in _trees(node, labels)]
    return _subtrees(tree, labels) + trees


def _parse_collocation(collocation: list) -> dict:
    if len(collocation) == 0: raise Exception()
    if len(collocation) == 1: return {"NN": collocation[0], "JJ": []}
    np = {"NN": None, "JJ": []}
    for i, node in next(sdp.raw_parse(" ".join(collocation))).nodes.items():
        if node["word"] is None: continue
        if node["head"] == 0:
            np["NN"] = node["word"]
        else:
            np["JJ"].append(node["word"])
    return np


def _parse_pp(tree) -> (list, list):
    result = []
    rpp = []
    for pp in _subtrees(tree, ["PP"]):
        _in = [_in[0] for _in in _subtrees(pp, ["IN"])]
        len_pps = len(_subtrees(pp, ["PP"]))
        len_in = len(_in)
        if len_pps > 0 and len_in == 0:
            (_pp, _rpp) = _parse_pp(pp)
            result.extend(_rpp)
            result.extend(_pp)
        elif len_pps == 0 and len_in > 0:
            (_np, _rpp) = _parse_np(pp)
            result.extend(_rpp)
            result.append({"IN": _in[0], "NP": _np})
        else:
            _in = _in[0]
            collocation = []
            first_in = True
            for word in list(pp.flatten()):
                if first_in and word == _in:
                    first_in = False
                else:
                    collocation.append(word)
            result.append({"IN": _in, "NP": [_parse_collocation(collocation)]})
    return result, rpp


def combine(inp: list) -> list:
    result = inp
    while len(result) > 1:
        result[0] = [i + j for i in result[0] for j in result[1]]
        del result[1]
    return result[0]


def _parse_np(tree) -> (list, list):
    result = []
    rpp = []
    for node in tree:
        label = node.label()
        if label == "NP":
            collocations = [[]]
            jjss = [[[]]]
            for inner_node in node:
                label = inner_node.label()
                if label in conjunction_level:
                    collocations.append([])
                elif label in word_level:
                    collocations[-1].append(inner_node)
                elif label == "ADJP":
                    jjs = [[]]
                    for jj in inner_node:
                        label = jj.label()
                        if label in conjunction_level:
                            jjs.append([])
                        elif label in word_level:
                            jjs[-1].append(jj[0])
                    jjss.append([jj for jj in jjs if len(jj) != 0])
            jjss = [jjs for jjs in jjss if len(jjs) != 0]
            nps = []
            pps = []
            for collocation in collocations:
                if len(collocation) == 0: continue
                _in = []
                _collocation = []
                for inner_node in collocation:
                    if inner_node.label() == "POS":
                        _in.append(inner_node[0])
                    else:
                        _collocation.append(inner_node[0])
                if len(_in) > 0:
                    rpp.append({"IN": _in[0], "NP": [_parse_collocation(_collocation)]})
                else:
                    nps.append(_parse_collocation(_collocation))
            nps = [{"NN": np["NN"], "JJ": (np["JJ"] + jjs)} for np in nps for jjs in combine(jjss)]
            (_np, _rpp) = _parse_np(node)
            nps.extend(_np)
            pps.extend(_rpp)
            (_pp, _rpp) = _parse_pp(node)
            pps.extend(_rpp)
            pps.extend(_pp)
            if len(pps) == 0:
                result.extend(nps)
            else:
                result.append({"NP": nps, "PP": pps})
        elif (label in phrase_level or label in clause_level) and label not in ["VP", "PP"]:
            result.append(_parse_collocation(list(node.flatten())))
    return result, rpp


def _parse_sentence(tree) -> dict:
    (_np, _rpp) = _parse_np(tree)
    if len(_rpp) > 0:
        sentence = {"NP": [{"NP": _np, "PP": _rpp}], "VP": []}
    else:
        sentence = {"NP": _np, "VP": []}
    for vp in _trees(tree, ["VP"]):
        vps = {}
        pps = []
        (_np, _rpp) = _parse_np(vp)
        pps.extend(_rpp)
        (_pp, _rpp) = _parse_pp(vp)
        pps.extend(_rpp)
        pps.extend(_pp)
        if len(pps) > 0:
            vps["NP"] = [{"NP": _np, "PP": pps}]
        else:
            vps["NP"] = _np
        vps["VB"] = [vb[0] for vb in _subtrees(vp, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])]
        sentence["VP"].append(vps)
    return sentence


# ToDo:
def _hard_convert(tree) -> dict:
    return None


def parse(string: str) -> dict:
    if len(string.split()) == 0: return None
    sp_tree = next(sp.raw_parse(string))[0]
    tmp = sp_tree
    if sp_tree.label() in fixable_sentence or sp_tree.label() == "S" and len(_subtrees(sp_tree, ["VP"])) == 0:
        string = "show " + string
        sp_tree = next(sp.raw_parse(string))[0]

    if sp_tree.label() in clause_level:
        file = open(sp_tree.label().lower() + ".txt", "a")
        file.write(str(sp_tree) + "\n")
        file.flush()
        file.close()

    IO.debug(sp_tree)

    if sp_tree.label() in ["S", "SINV"]:
        _parse = _parse_sentence(sp_tree)
        if sp_tree.label() == "SINV":
            for vp in _parse["VP"]:
                vp["NP"].extend(_parse["NP"])
            _parse["NP"] = []
        return _parse
    else:
        return _hard_convert(tmp)


def tree(root: dict, shift=0) -> str:
    if root is None: return 'None'
    result = ["{\n"]
    for i, (key, col) in enumerate(sorted(root.items())):
        result.append("\t" * shift)
        result.append("'" + str(key) + "': ")
        if key in {"NN", "JJ", "VB", "IN"} or len(col) == 0:
            result.append(str(col))
        else:
            result.append("[")
            for j, value in enumerate(col):
                if isinstance(value, dict):
                    result.append(tree(value, shift + 1))
                else:
                    result.append(str(value))
                if j < len(col) - 1: result.append(", ")
            result.append("]")
        if i < len(root) - 1:
            result.append(",\n")
        else:
            result.append("\n")
    result.append("\t" * shift)
    result.append("}")
    return "".join(result)
