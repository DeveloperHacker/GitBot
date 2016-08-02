class Sentence:
    def __init__(self, subjects=None, actions=None):
        if actions is None: actions = []
        if subjects is None: subjects = []
        self.subjects = subjects
        self.actions = actions

    def __str__(self) -> str:
        subjects = ", ".join([subject.__str__() for subject in self.subjects])
        actions = ", ".join([action.__str__() for action in self.actions])
        return "Sentence(subjects=[{}], actions=[{}])".format(subjects, actions)


class Subject:
    def __init__(self, noun: str, adjectives=None):
        if adjectives is None: adjectives = []
        self.noun = noun
        self.adjectives = adjectives

    def __str__(self) -> str:
        adjectives = ", ".join([adjective.__str__() for adjective in self.adjectives])
        return "Subject(noun={}, adjectives=[{}])".format(self.noun, adjectives)


class Action:
    def __init__(self, verb: str, subjects=None, prepositional=None):
        if subjects is None: subjects = []
        if prepositional is None: prepositional = []
        self.verb = verb
        self.subjects = subjects
        self.prepositional = prepositional

    def __str__(self) -> str:
        subjects = ", ".join([subject.__str__() for subject in self.subjects])
        prepositional = ", ".join([prep.__str__() for prep in self.prepositional])
        return "Action(verb={}, subjects=[{}], prepositional=[{}])".format(self.verb, subjects, prepositional)


class Preposition(Subject):

    @staticmethod
    def create(direct: str, subject: Subject) -> 'Preposition':
        return Preposition(direct, subject.noun, subject.adjectives)

    def __init__(self, direct: str, noun: str, adjectives=None):
        super().__init__(noun, adjectives)
        self.direct = direct

    def __str__(self) -> str:
        adjectives = ", ".join([adjective.__str__() for adjective in self.adjectives])
        return "Preposition(direct={}, noun={}, adjectives=[{}])".format(self.direct, self.noun, adjectives)


class Parse:
    def __init__(self, sentences=None):
        if sentences is None: sentences = []
        self.sentences = sentences

    def __str__(self) -> str:
        sentences = ", ".join([sentence.__str__() for sentence in self.sentences])
        return "Parse(sentences=[{}])".format(sentences)
