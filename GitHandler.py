from Tools.scripts.treesync import raw_input

from GitConnector import GitConnector
from Parser import parse_string
from Simplifies import simplify_word, simplify_exp
from Tree import Action


def format_nick(nick, max_len) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._authorised = False
        self._connector = GitConnector()
        self._commands = {
            "show": self.show,
            "login": self.login,
            "unlogin": self.unlogin,
            "close": self.close
        }
        self._bot_nick = bot_nick
        self._nick = default_nick
        self._default_nick = default_nick
        self._max_nick_len = max_nick_len

    def start(self):
        self._connect = True
        while self._connect: self.handle()

    def stop(self):
        self._connect = False

    def print(self, obj):
        print(format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + obj.__str__())

    def read(self) -> str:
        return raw_input(format_nick(self._nick, self._max_nick_len) + "  ::  ")[:-1]

    def handle(self):
        data = self.read()
        parse = parse_string(data)
        # print(parse)
        if parse is None: return
        for sentence in parse.sentences:
            for action in sentence.actions:
                verb = simplify_word(action.verb)
                if verb in self._commands: self._commands[verb](action)

    def n_print(self, preps: list, foo):
        if len(preps) == 0 and self._authorised:
            self.print(foo())
        elif len(preps) == 1:
            self.print(foo(preps[0].noun))
        else:
            for prep in preps: self.print(prep.noun + ": " + foo(prep.noun))

    def show(self, action: Action):
        for subj in action.subjects:
            name = simplify_word(subj.noun)
            adjectives = simplify_exp(subj.adjectives)
            if name == "repos":
                if "public" in adjectives:
                    foo = (lambda n=None: self._connector.public_repos(n))
                elif "private" in adjectives:
                    if "owned" in adjectives:
                        foo = (lambda n=None: self._connector.owned_private_repos(n))
                    else:
                        foo = (lambda n=None: self._connector.total_private_repos(n))
                else:
                    foo = (lambda n=None: ", ".join([repo.name for repo in self._connector.repos(n)]))
                self.n_print(action.prepositional, foo)
            elif name == "url":
                if "organizations" in adjectives:
                    foo = (lambda n=None: self._connector.organizations_url(n))
                elif "repos" in adjectives:
                    foo = (lambda n=None: self._connector.repos_url(n))
                elif "subscriptions" in adjectives:
                    foo = (lambda n=None: self._connector.subscriptions_url(n))
                elif "following" in adjectives:
                    foo = (lambda n=None: self._connector.following_url(n))
                elif "gists" in adjectives:
                    foo = (lambda n=None: self._connector.gists_url(n))
                elif "avatar" in adjectives:
                    foo = (lambda n=None: self._connector.avatar_url(n))
                elif "events" in adjectives:
                    if "received" in adjectives:
                        foo = (lambda n=None: self._connector.received_events_url(n))
                    else:
                        foo = (lambda n=None: self._connector.events_url(n))
                elif "followers" in adjectives:
                    foo = (lambda n=None: self._connector.followers_url(n))
                elif "starred" in adjectives:
                    foo = (lambda n=None: self._connector.starred_url(n))
                else:
                    foo = (lambda n=None: self._connector.url(n))
                self.n_print(action.prepositional, foo)

    def login(self, action: Action):
        self.print("login:")
        login = self.read()
        self.print("password:")
        pword = self.read()
        self._nick = self._connector.login(login, pword)
        self._authorised = True
        if self._nick is None:
            self._authorised = False
            self._nick = self._default_nick
            self.print("Incorrect input: login or password")

    def unlogin(self, action: Action):
        self._connector.unlogin()
        self._authorised = False
        self._nick = self._default_nick

    def close(self, action: Action):
        self.stop()
