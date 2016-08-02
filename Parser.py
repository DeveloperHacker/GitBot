import re

from nltk.parse.stanford import StanfordDependencyParser, StanfordParser

from Tree import Sentence, Action, Parse, Subject, Preposition

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


def _get_trees(tree, labels: list) -> list:
    return _get_subtrees(tree, labels) + [t for node in tree if not isinstance(node, str) for t in _get_trees(node, labels)]


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
    sdp_trees = [next(sdp.raw_parse(" ".join(words))) for words in nps if len(words) > 0]
    subjects = []
    for sdp_tree in sdp_trees:
        subject = Subject("")
        for i, node in sdp_tree.nodes.items():
            if node["word"] is None: continue
            if node["head"] == 0: subject.noun = node["word"]
            elif node["tag"] != "DT": subject.adjectives.append(node["word"])
        subjects.append(subject)
    return subjects


def _get_prepositional(tree) -> list:
    return [Preposition.create(pp[0].label(), subj) for pp in _get_trees(tree, ["PP"]) for subj in _get_subjects(pp)]


def _get_actions(vp) -> list:
    vbs = _get_subtrees(vp, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    return [vb[0] for vb in vbs]


def _parse_simple_sentence(tree) -> Sentence:
    if tree.label() != "S": return None
    nps = _get_subtrees(tree, ["NP"])
    sentence = Sentence(subjects=[subj for np in nps for subj in _get_subjects(np)])
    vps = _get_trees(tree, ["VP"])
    sentence.actions = [Action(act, _get_subjects(vp), _get_prepositional(vp)) for vp in vps for act in _get_actions(vp)]
    return sentence


def _parse_sentence_with_guessing_verb(tree) -> Sentence:
    if tree.label() not in ["NP", "FRAG"]: return None
    sentence = Sentence(actions=[Action("show", _get_subjects(tree), _get_prepositional(tree))])
    return sentence


sp = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sdp = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


def parse_string(text: str) -> Parse:
    strings = re.split("[\.;]", text)
    parse = Parse()
    for string in strings:
        if len(string.split()) == 0: continue
        sp_tree = next(sp.raw_parse(string))[0]
        # print(sp_tree)
        sentence = _parse_simple_sentence(sp_tree)
        if sentence is not None: parse.sentences.append(sentence)
        sentence = _parse_sentence_with_guessing_verb(sp_tree)
        if sentence is not None: parse.sentences.append(sentence)
    return parse
