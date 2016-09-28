from copy import deepcopy

from nltk.parse.stanford import StanfordDependencyParser

from src.main.interfaces.Corrector import Corrector
from src.main.types.Node import Adjective, LeafNounPhrase, Noun, NounPhrase, PrepositionalPhrase, Root, Verb, VerbPhrase
from src.main.nlp.StanfordParser import Node


class StanfordCorrector(Corrector):
    parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    phrase_level = {
        "ADJP", "ADVP", "CONJR", "FRAG", "INTJ", "LST", "NAC", "NP", "NX", "PP", "PRN", "PRT", "QP", "RRC", "UCP", "VP",
        "WHADJP", "WHAVP", "WHNP", "WHPP", "X"
    }

    clause_level = {
        "S", "SBAR", "SBARQ", "SINV", "SQ"
    }

    word_level = {
        "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS",
        "PRP",
        "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"
    }

    conjunction_level = {"CC", ","}

    fixable_sentence = {"NP", "FRAG", "UCP", "PP", "ADJP", "INTJ"}

    @staticmethod
    def collocation(collocation: list) -> LeafNounPhrase:
        if len(collocation) == 0: raise Exception()
        if len(collocation) == 1: return LeafNounPhrase(collocation[0])
        np = LeafNounPhrase()
        for i, node in next(StanfordCorrector.parser.raw_parse(" ".join(collocation))).nodes.items():
            if node["word"] is None: continue
            if node["head"] == 0:
                np.nn = Noun(node["word"])
            else:
                np.jjs.append(Adjective(node["word"]))
        return np

    @staticmethod
    def pp(tree: Node) -> list:
        pps = []
        for pp in tree.children(label="PP"):
            _in = [_in[0] for _in in pp.children(label="IN")]
            len_pps = len(pp.children(label="PP"))
            len_in = len(_in)
            if len_pps > 0 and len_in == 0:
                pps.extend(StanfordCorrector.pp(pp))
            elif len_pps == 0 and len_in > 0:
                (_nps, _rpp) = StanfordCorrector.np(pp)
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
                pps.append(PrepositionalPhrase(_in, [StanfordCorrector.collocation(collocation)]))
        return pps

    @staticmethod
    def combine(inp: list) -> list:
        if len(inp) == 0: return [[]]
        result = deepcopy(inp)
        while len(result) > 1:
            result[0] = [i + j for i in result[0] for j in result[1]]
            del result[1]
        return result[0]

    @staticmethod
    def lnp(tree: Node) -> (list, list):
        rpp = []
        collocations = [[]]
        jjsss = []
        for node in tree:
            label = node.label
            if label in StanfordCorrector.conjunction_level:
                collocations.append([])
            elif label in StanfordCorrector.word_level:
                collocations[-1].append(node)
            elif label == "ADJP":
                jjss = [[]]
                for jj in node:
                    label = jj.label
                    if label in StanfordCorrector.conjunction_level:
                        jjss.append([])
                    elif label in StanfordCorrector.word_level:
                        jjss[-1].append(jj[0])
                jjsss.append([jjs for jjs in jjss if len(jjs) != 0])
        jjss = StanfordCorrector.combine([jjss for jjss in jjsss if len(jjss) != 0])
        collocations = [collocation for collocation in collocations if len(collocation) != 0]
        nps = []
        for collocation in collocations:
            _in = []
            _collocation = []
            for node in collocation:
                if node.label == "POS":
                    _in.append(node[0])
                else:
                    _collocation.append(node[0])
            if len(_in) > 0:
                rpp.append(PrepositionalPhrase(_in[0], [StanfordCorrector.collocation(_collocation)]))
            else:
                parsed = StanfordCorrector.collocation(_collocation)
                noun = parsed.nn.text
                jjs = [jj.text for jj in parsed.jjs]
                nps.extend([LeafNounPhrase(noun, jjs + _jjs) for _jjs in jjss])
        return nps, rpp

    @staticmethod
    def np(tree: Node) -> (list, list):
        result = []
        rpp = []
        for node in tree:
            label = node.label
            if label == "NP":
                (nps, _rpp) = StanfordCorrector.lnp(node)
                rpp.extend(_rpp)
                (_nps, pps) = StanfordCorrector.np(node)
                nps.extend(_nps)
                pps.extend(StanfordCorrector.pp(node))
                result.extend(nps if len(pps) == 0 else [NounPhrase(nps, pps)])
            elif label in (StanfordCorrector.phrase_level | StanfordCorrector.clause_level) - {"VP", "PP"}:
                result.append(StanfordCorrector.collocation(node.flatten()))
        return result, rpp

    @staticmethod
    def sentence(tree: Node) -> Root:
        (_nps, _rpp) = StanfordCorrector.np(tree)
        root = Root(_nps if len(_rpp) == 0 else [NounPhrase(_nps, _rpp)])
        for vp in tree.sub_children(label="VP"):
            (nps, pps) = StanfordCorrector.np(vp)
            pps.extend(StanfordCorrector.pp(vp))
            verb_phrase = VerbPhrase()
            verb_phrase.nps = nps if len(pps) == 0 else [NounPhrase(nps, pps)]
            verb_phrase.vbs = [Verb(vb[0]) for vb in vp.children(labels=["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])]
            root.vps.append(verb_phrase)
        return root

    def correct(self, parsed: Node) -> Root:
        root = None
        if parsed.label in ["S", "SINV"]:
            root = StanfordCorrector.sentence(parsed)
            if root.label == "SINV":
                for vp in root.vps: vp.nps.extend(root.nps)
                root.nps = []
        return root
