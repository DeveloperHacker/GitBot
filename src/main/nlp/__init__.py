import os

home = os.getenv("HOME")
stanford_dir = home + "/NLP"
os.environ["STANFORD_DIR"] = stanford_dir
os.environ["STANFORD_MODELS"] = "{0}/stanford-postagger-full/models:" \
                                "{0}/stanford-ner/classifiers".format(stanford_dir)
os.environ["CLASSPATH"] = "{0}/stanford-postagger-full/stanford-postagger.jar:" \
                          "{0}/stanford-ner/stanford-ner.jar:" \
                          "{0}/stanford-parser-full/stanford-parser.jar:" \
                          "{0}/stanford-parser-full/stanford-parser-3.5.2-models.jar".format(stanford_dir)