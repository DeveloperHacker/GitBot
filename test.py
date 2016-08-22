import os

from nltk.parse.stanford import StanfordParser, StanfordDependencyParser

stanford_dir = os.getenv("HOME") + "/NLP"
os.environ["STANFORD_DIR"] = stanford_dir
os.environ["STANFORD_MODELS"] = "{0}/stanford-postagger-full/models:{0}/stanford-ner/classifiers".format(stanford_dir)
os.environ[
    "CLASSPATH"] = "{0}/stanford-postagger-full/stanford-postagger.jar:{0}/stanford-ner/stanford-ner.jar:{0}/stanford-parser-full/stanford-parser.jar:{0}/stanford-parser-full/stanford-parser-3.5.2-models.jar".format(
        stanford_dir)

sp = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sdp = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

l = [
    "show his name",
    "show developerhacker's name",
    "show this user's name",
    "show stored user's name",
    "show name of developerhacker",
    "show name of this user",
    "show name of stored user",

    "show his repos",
    "show developerhacker's repos",
    "show this user's repos",
    "show stored user's repos",
    "show repos of developerhacker",
    "show repos of this user",
    "show repos of stored user",

    "store his repo with the name gitbot",
    "store his repo gitbot",
    "store a developerhacker's repo with the name gitbot",
    "store a developerhacker's repo gitbot",
    "store this user's repo with the name gitbot",
    "store this user's repo gitbot",
    "store stored user's repo with the name gitbot",
    "store stored user's repo gitbot",
    "store a repo with the name gitbot of developerhacker",
    "store a repo gitbot of developerhacker",
    "store a repo with the name gitbot of this user",
    "store a repo gitbot of this user",
    "store a repo with the name gitbot of stored user",
    "store a repo gitbot of stored user",

    "show name of this repo and id of this repo",
    "show name and id of this repo",
    "show name , id and contributors of this repo and repo gitbot of stored user"
]

# for el in l: print(next(sp.raw_parse(el)))

next(sp.raw_parse("show a name and this user's black repo and white repo of lealsa")).draw()

# print(next(sdp.raw_parse("show a name of of this user")).tree())