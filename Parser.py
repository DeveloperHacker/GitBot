from nltk.parse.stanford import StanfordDependencyParser, StanfordParser


class Action:
    def __init__(self, name: str, objects: list, preps: list):
        self.name = name
        self.objects = objects
        self.preps = preps

    def __str__(self) -> str:
        return "Action(name={}, objects={}, ats={})".format(self.name, self.objects, self.preps)


class Parse:
    def __init__(self, subjects: list, actions: list):
        self.subjects = subjects
        self.actions = actions

    def __str__(self) -> str:
        acts = ", ".join([act.__str__() for act in self.actions])
        return "Parse(subjects={}, actions=[{}])".format(self.subjects, acts)


phrase_level = {
    "ADJP", "ADVP", "CONJR", "FRAG", "INTJ", "LST", "NAC", "NP", "NX", "PP", "PRN", "PRT", "QP", "RRC", "UCP", "VP",
    "WHADJP", "WHAVP", "WHNP", "WHPP", "X"
}

word_level = {
    "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP",
    "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"
}


def _get_subtrees(tree, labels: list) -> list:
    return [node for node in tree if not isinstance(node, str) and node.label() in labels]


def _get_subjects(tree) -> list:
    subj = [w for np in _get_subtrees(tree, ["NP"]) for w in _get_subjects(np)]
    if len(subj) != 0: return subj
    nps = [[]]
    for np in tree:
        label = np.label()
        if label == "CC" or label == "," or label == ".":
            nps.append([])
        elif label not in phrase_level:
            nps[-1].extend(np.flatten())
    sdp_trees = [next(sdp.raw_parse(" ".join(words))) for words in nps]
    return [node["word"] for sdp_tree in sdp_trees for i, node in sdp_tree.nodes.items() if node["head"] == 0]


def _get_prepositional(tree) -> list:
    preps = [w for pp in _get_subtrees(tree, ["PP"]) for w in _get_prepositional(pp)]
    if len(preps) != 0: return preps
    label = tree[0].label()
    return [(w, label) for w in _get_subjects(tree)]


def _get_actions(vp) -> list:
    vbs = _get_subtrees(vp, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    return [vb[0] for vb in vbs]


def _parse_simple_sentence(tree):
    if tree.label() != "S": return None
    nps = _get_subtrees(tree, ["NP"])
    parse = Parse(subjects=[w for np in nps for w in _get_subjects(np)], actions=[])
    vps = _get_subtrees(tree, ["VP"])
    for vp in vps:
        acts = _get_actions(vp)
        words = [w for np in _get_subtrees(vp, ["NP"]) for w in _get_subjects(np)]
        preps = [w for pp in _get_subtrees(vp, ["PP"]) for w in _get_prepositional(pp)]
        parse.actions.extend([Action(act, words, preps) for act in acts])
    return parse


def _parse_sentence_with_guessing_verb(tree) -> list:
    if tree.label() != "NP": return None
    preps = [w for pp in _get_subtrees(tree, ["PP"]) for w in _get_prepositional(pp)]
    parse = Parse(subjects=[], actions=[Action("show", [w for w in _get_subjects(tree)], preps)])
    return parse


sp = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sdp = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


def parse_string(string: str) -> Parse:
    if len(string.split()) == 0: return None
    sp_tree = next(sp.raw_parse(string))[0]
    # print(sp_tree)
    parse = _parse_simple_sentence(sp_tree)
    if parse is not None: return parse
    parse = _parse_sentence_with_guessing_verb(sp_tree)
    if parse is not None: return parse
    return Parse(subjects=[], actions=[])
