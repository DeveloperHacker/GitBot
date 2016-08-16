import re, os
from nltk.parse.stanford import StanfordDependencyParser, StanfordParser

stanford_dir = os.getenv("HOME") + "/NLP"
os.environ["STANFORD_DIR"] = stanford_dir
os.environ["STANFORD_MODELS"] = "{0}/stanford-postagger-full/models:{0}/stanford-ner/classifiers".format(stanford_dir)
os.environ["CLASSPATH"] = "{0}/stanford-postagger-full/stanford-postagger.jar:{0}/stanford-ner/stanford-ner.jar:{0}/stanford-parser-full/stanford-parser.jar:{0}/stanford-parser-full/stanford-parser-3.5.2-models.jar".format(stanford_dir)

sp = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sdp = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

phrase_level = {
    "ADJP", "ADVP", "CONJR", "FRAG", "INTJ", "LST", "NAC", "NP", "NX", "PP", "PRN", "PRT", "QP", "RRC", "UCP", "VP",
    "WHADJP", "WHAVP", "WHNP", "WHPP", "X"
}

word_level = {
    "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP",
    "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"
}


def _subtrees(tree, labels: list) -> list:
    return [node for node in tree if not isinstance(node, str) and node.label() in labels]


def _trees(tree, labels: list) -> list:
    trees = [t for node in tree if not isinstance(node, str) for t in _trees(node, labels)]
    return _subtrees(tree, labels) + trees


def _parse_collocations(tree) -> list:
    nps = [[]]
    for np in tree:
        label = np.label()
        if label == "CC" or label == "," or label == ".":
            nps.append([])
        elif label not in phrase_level:
            nps[-1].extend(np.flatten())
    sdp_trees = [next(sdp.raw_parse(" ".join(words))) for words in nps if len(words) > 0]
    collocations = []
    for sdp_tree in sdp_trees:
        subject = {"NN": None, "JJ": []}
        for i, node in sdp_tree.nodes.items():
            if node["word"] is None: continue
            if node["head"] == 0:
                subject["NN"] = node["word"]
            else:
                subject["JJ"].append(node["word"])
        collocations.append(subject)
    return collocations


def _parse_subjects(tree):
    nps = _subtrees(tree, ["NP"])
    if len(nps) == 0: return {"COL": _parse_collocations(tree)}
    pps = _parse_prepositional(tree)
    subjects = []
    for np in nps:
        subj = _parse_subjects(np)
        if "COL" in subj:
            for collocation in subj["COL"]: subjects.append({**collocation, **{"PP": pps}})
        else:
            subjects.extend(subj)
    return subjects


def _parse_prepositional(tree) -> list:
    return [{"IN": prep[0][0], "SS": _parse_subjects(prep)} for prep in _subtrees(tree, ["PP"])]


def _parse_sentence(tree) -> dict:
    sentence = {"SS": [], "AA": []}
    for np in _subtrees(tree, ["NP"]):
        sentence["SS"].extend(_parse_subjects(np))
    for vp in _trees(tree, ["VP"]):
        for act in [vb[0] for vb in _subtrees(vp, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])]:
            sentence["AA"].append({
                "VV": act,
                "SS": _parse_subjects(vp)
            })
    return sentence


def parse(text: str) -> dict:
    strings = re.split("[\.;]", text)
    root = {"S": []}
    for string in strings:
        if len(string.split()) == 0: continue
        sp_tree = next(sp.raw_parse(string))[0]
        if sp_tree.label() in ["NP", "FRAG"]:
            string = "show " + string
            sp_tree = next(sp.raw_parse(string))[0]
        # print(sp_tree)
        root["S"].append(_parse_sentence(sp_tree) if sp_tree.label() == "S" else None)
    return root
