from Tools.scripts.treesync import raw_input

import github.GithubObject
from github import GithubException

from GitConnector import GitConnector
from Parser import parse_string
from Simplifies import simplify_word, simplify_exp
from Tree import Action


def format_nick(nick, max_len) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._connector = GitConnector()
        self._commands = {
            "count": self.count,
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
        print(format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + str(obj))

    def read(self) -> str:
        return raw_input(format_nick(self._nick, self._max_nick_len) + "  ::  ")[:-1]

    def handle(self):
        data = self.read()
        parse = parse_string(data)
        print(parse)
        if parse is None: return
        for sentence in parse.sentences:
            for action in sentence.actions:
                verb = simplify_word(action.verb)
                if verb in self._commands: self._commands[verb](action)

    def login(self, action: Action):
        self.print("login:")
        login = self.read()
        self.print("password:")
        pword = self.read()
        self._nick = self._connector.authorise(login, pword)
        if self._nick is None:
            self._nick = self._default_nick
            self.print("Incorrect input: login or password")

    def unlogin(self, action: Action):
        self._connector.unlogin()
        self._nick = self._default_nick

    def close(self, action: Action):
        self.stop()

    #     Warning
    #     I do not know how I it writen

    # ToDo: something with this bullshit

    def n_print(self, preps: list, foo):
        if len(preps) == 0 and self._connector.authorised() is not None:
            self.print(foo(self._connector.authorised()))
        elif len(preps) == 1:
            try:
                self.print(foo(preps[0].noun))
            except GithubException as ex:
                if ex.status == 404: self.print("User with login=\"" + preps[0].noun + "\" not found")
        else:
            for prep in preps:
                try:
                    self.print(prep.noun + ": " + str(foo(prep.noun)))
                except GithubException as ex:
                    if ex.status == 404: self.print("User with login=\"" + prep.noun + "\" not found")
                    
    def count(self, action: Action):
        for subj in action.subjects:
            name = simplify_word(subj.noun)
            adjectives = simplify_exp(subj.adjectives)
            foo = None
            if name == "repos":
                if "public" in adjectives:
                    foo = (lambda login: self._connector.public_repos(login))
                elif "private" in adjectives:
                    if "owned" in adjectives:
                        foo = (lambda login: self._connector.owned_private_repos(login))
                    else:
                        foo = (lambda login: self._connector.total_private_repos(login))
                else:
                    foo = (lambda login: self._connector.public_repos(login) + self._connector.total_private_repos(login))
            elif name == "gists":
                if "public" in adjectives:
                    foo = (lambda login: self._connector.public_gists(login))
                elif "private" in adjectives:
                    foo = (lambda login: self._connector.private_gists(login))
                else:
                    foo = (lambda login:
                           "public: " + str(self._connector.public_gists(login)) +
                           " private: " + str(self._connector.private_gists(login)))
            elif name == "following":
                foo = (lambda login: self._connector.following(login))
            elif name == "collaborators":
                foo = (lambda login: self._connector.collaborators(login))
            elif name == "followers":
                foo = (lambda login: self._connector.followers(login))
            if foo is not None: self.n_print(action.prepositional, foo)

    def show(self, action: Action):
        for subj in action.subjects:
            name = simplify_word(subj.noun)
            adjectives = simplify_exp(subj.adjectives)
            foo = None
            if name == "repos":
                if "starred" in adjectives:
                    def foo(login):
                        repos = list(self._connector.get_starred_repos(login))
                        if len(repos) == 0: return None
                        return ", ".join([repo.name for repo in repos])
                else:
                    def foo(login):
                        repos = list(self._connector.get_repos(login))
                        if len(repos) == 0: return None
                        return ", ".join([repo.name for repo in repos])
            if name == "gists":
                # if "starred" in adjectives:
                #     def foo(login):
                #         gists = list(self._connector.get_starred_gists(login))
                #         if len(gists) == 0: return None
                #         return ", ".join([gist.id for gist in gists])
                # else:
                def foo(login):
                    gists = list(self._connector.get_gists(login))
                    if len(gists) == 0: return None
                    return ", ".join([gist.id for gist in gists])
            if name == "keys":
                def foo(login):
                    keys = list(self._connector.get_keys(login))
                    if len(keys) == 0: return None
                    return ", ".join(["(id: " + str(key.id) + " key: " + key.key + ") " for key in keys])
            if name == "orgs":
                def foo(login):
                    orgs = list(self._connector.get_orgs(login))
                    if len(orgs) == 0: return None
                    return ", ".join([org.login for org in orgs])
            # if name == "emails":
            #     def foo(login):
            #         emails = list(self._connector.get_emails(login))
            #         if len(emails) == 0: return None
            #         return ", ".join([email.login for email in emails])
            elif name == "url":
                if "organizations" in adjectives:
                    foo = (lambda login: self._connector.organizations_url(login))
                elif "repos" in adjectives:
                    foo = (lambda login: self._connector.repos_url(login))
                elif "subscriptions" in adjectives:
                    foo = (lambda login: self._connector.subscriptions_url(login))
                elif "following" in adjectives:
                    foo = (lambda login: self._connector.following_url(login))
                elif "gists" in adjectives:
                    foo = (lambda login: self._connector.gists_url(login))
                elif "avatar" in adjectives:
                    foo = (lambda login: self._connector.avatar_url(login))
                elif "events" in adjectives:
                    if "received" in adjectives:
                        foo = (lambda login: self._connector.received_events_url(login))
                    else:
                        foo = (lambda login: self._connector.events_url(login))
                elif "followers" in adjectives:
                    foo = (lambda login: self._connector.followers_url(login))
                elif "starred" in adjectives:
                    foo = (lambda login: self._connector.starred_url(login))
                elif "html" in adjectives:
                    foo = (lambda login: self._connector.url(login))
                else:
                    foo = (lambda login: self._connector.url(login))
            elif name == "followings":
                def foo(login):
                    followings = list(self._connector.get_followings(login))
                    if len(followings) == 0: return None
                    return ", ".join([following.login for following in followings])
            elif name == "name":
                foo = (lambda login: self._connector.name(login))
            elif name == "bio":
                foo = (lambda login: self._connector.bio(login))
            elif name == "type":
                foo = (lambda login: self._connector.type(login))
            elif name == "email":
                foo = (lambda login: self._connector.email(login))
            elif name == "blog":
                foo = (lambda login: self._connector.blog(login))
            elif name == "data":
                if "raw" in adjectives:
                    foo = (lambda login: self._connector.raw_data(login))
            elif name == "etag":
                foo = (lambda login: self._connector.etag(login))
            elif name == "id":
                if "gravatar" in adjectives:
                    foo = (lambda login: self._connector.gravatar_id(login))
                else:
                    foo = (lambda login: self._connector.id(login))
            elif name == "company":
                foo = (lambda login: self._connector.company(login))
            elif name == "followers":
                def foo(login):
                    followers = list(self._connector.get_followers(login))
                    if len(followers) == 0: return None
                    return ", ".join([follower.login for follower in followers])
            elif name == "plan":
                if "collaborators" in adjectives:
                    def foo(login):
                        plan = self._connector.plan(login)
                        if plan is not None: return plan.collaborators
                elif "repos" in adjectives and "private" in adjectives:
                    def foo(login):
                        plan = self._connector.plan(login)
                        if plan is not None: return plan.private_repos
                elif "space" in adjectives:
                    def foo(login):
                        plan = self._connector.plan(login)
                        if plan is not None: return plan.space
                elif "name" in adjectives:
                    def foo(login):
                        plan = self._connector.plan(login)
                        if plan is not None: return plan.name
                else:
                    def foo(login):
                        plan = self._connector.plan(login)
                        if plan is not None: return plan.name
            elif name == "hireable":
                foo = (lambda login: self._connector.hireable(login))
            elif name == "login":
                foo = (lambda login: self._connector.login(login))
            elif name == "location":
                foo = (lambda login: self._connector.location(login))
            elif name == "headers":
                if "raw" in adjectives:
                    foo = (lambda login: self._connector.raw_headers(login))
            elif name == "date":
                if "creation" in adjectives:
                    foo = (lambda login: self._connector.created_at(login))
                elif "update" in adjectives:
                    foo = (lambda login: self._connector.updated_at(login))
                elif "modification" in adjectives and "last" in adjectives:
                    foo = (lambda login: self._connector.last_modified(login))
            if foo is not None: self.n_print(action.prepositional, foo)
