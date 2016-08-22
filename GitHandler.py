from Tools.scripts.treesync import raw_input
from getpass import getpass

from github import GithubException
from github.NamedUser import NamedUser

import Corrector
from GitConnector import GitConnector
from Simplifies import simplify_word, simplify_exp


def format_nick(nick, max_len) -> str:
    return nick[max_len - 3] + "..." if len(nick) > max_len else " " * (max_len - len(nick)) + nick


class GitHandler:
    def __init__(self, bot_nick="Bot", default_nick="User", max_nick_len=20):
        self._connect = False
        self._connector = GitConnector()
        self._commands = {
            "count": self.count,
            "show": self.show,
            "store": self.store,
            "login": self.login,
            "unlogin": self.unlogin,
            "close": self.close
        }
        self._stored = {
            "user": None,
            "repo": None,
            "gist": None
        }
        self._bot_nick = bot_nick
        self._nick = default_nick
        self._default_nick = default_nick
        self._max_nick_len = max_nick_len

    def start(self):
        self._connect = True
        self.print("Hello")
        while self._connect: self.handle()

    def stop(self):
        self._connect = False

    def print(self, obj):
        print(format_nick(self._bot_nick, self._max_nick_len) + "  ::  " + str(obj))

    def read(self) -> str:
        return raw_input(format_nick(self._nick, self._max_nick_len) + "  ::  ")[:-1]

    def hide_read(self) -> str:
        return getpass(format_nick(self._nick, self._max_nick_len) + "  ::  ")

    def handle(self):
        data = self.read()
        sentence = Corrector.parse(data)
        # print(Corrector.tree(sentence))
        if sentence is None: return
        for vp in sentence["VP"]:
            verb = simplify_word(vp["VB"])
            if verb in self._commands: self._commands[verb](vp)

    def login(self, _):
        if self._connector.authorised():
            self.print("you need to unlogin before you login again")
        else:
            self.print("login:")
            login = self.read()
            self.print("password:")
            pword = self.hide_read()
            if not self._connector.authorise(login, pword):
                self._nick = self._default_nick
                self.print("Incorrect input: login or password")
            else:
                self._nick = self._connector.authorised()

    def unlogin(self, _):
        if self._connector.authorised():
            self._connector.unlogin()
            self._nick = self._default_nick

    def close(self, _):
        self.print("Bye")
        self.stop()

    #     Warning
    #     I do not know how I it writen

    # ToDo: something

    def execute(self, command: str, pps, foo):
        nps = [np for pp in pps if pp["IN"].lower() in Corrector.belongs_words for np in pp["NP"]]
        if len(nps) == 0 and self._connector.authorised() is not None:
            user = self._connector.user()
            value = foo(user)
            self.print("{}: {}".format(command, value if value else "\"Access closed\""))
        else:
            for np in nps:
                if "NN" in np: noun = simplify_word(np["NN"])
                else: continue
                try:
                    if noun == "user" and ("this" in np["JJ"] or "stored" in np["JJ"]):
                        user = self._stored["user"]
                        if user is None:
                            self.print("I did not remember any user")
                            continue
                    else:
                        user = self._connector.user(noun)
                    noun = user.login
                    value = foo(user)
                    self.print("{} at {}: {}".format(command, noun, value if value else "\"Access closed\""))
                except GithubException as ex:
                    if ex.status == 404:
                        self.print("User with login of \"{}\" not found".format(noun))
                    elif ex.status == 403:
                        self.print(ex.data["message"])
                    else:
                        raise ex

    def count(self, vp):
        for np in vp["NP"]:
            pps = np["PP"]
            for np in np["NP"]:
                noun = simplify_word(np["NN"]) if "NN" in np else None
                adjectives = simplify_exp(np["JJ"]) if "JJ" in np else []
                foo = None
                if noun == "repos":
                    if "public" in adjectives:
                        foo = (lambda user: user.public_repos)
                        command = "public repositories"
                    elif "private" in adjectives:
                        if "owned" in adjectives:
                            foo = (lambda user: user.owned_private_repos)
                            command = "owned private repositories"
                        else:
                            foo = (lambda user: user.total_private_repos)
                            command = "private repositories"
                    else:
                        def foo(user: NamedUser):
                            public = user.public_repos
                            private = user.total_private_repos
                            return "{}(public) and {}(private)".format(public, private if private else "\"Access closed\"")
                        command = "repositories"
                elif noun == "gists":
                    if "public" in adjectives:
                        foo = (lambda user: user.public_gists)
                        command = "public gists"
                    elif "private" in adjectives:
                        foo = (lambda user: user.private_gists)
                        command = "private gists"
                    else:
                        def foo(user: NamedUser):
                            public = user.public_gists
                            private = user.private_gists
                            return "{}(public) and {}(private)".format(public, private if private else "\"Access closed\"")

                        command = "gists"
                elif noun == "following":
                    foo = (lambda user: user.following)
                    command = "following"
                elif noun == "collaborators":
                    foo = (lambda user: user.collaborators)
                    command = "collaborators"
                elif noun == "followers":
                    foo = (lambda user: user.followers)
                    command = "followers"
                if foo is not None:
                    self.execute(command, pps, foo)

    def show(self, vp):
        for np in vp["NP"]:
            pps = np["PP"]
            for np in np["NP"]:
                noun = simplify_word(np["NN"]) if "NN" in np else None
                adjectives = simplify_exp(np["JJ"]) if "JJ" in np else []
                foo = None
                if noun == "repos":
                    def foo(user: NamedUser):
                        repos = list(user.get_repos())
                        if len(repos) == 0: return None
                        return ", ".join([repo.name for repo in repos])

                    command = "repositories"
                elif noun == "gists":
                    def foo(user: NamedUser):
                        gists = list(user.get_gists())
                        if len(gists) == 0: return None
                        return ", ".join([gist.id for gist in gists])

                    command = "gists"
                elif noun == "keys":
                    def foo(user: NamedUser):
                        keys = list(user.get_keys())
                        if len(keys) == 0: return None
                        return ", ".join(["(id: " + str(key.id) + " key: " + key.key + ") " for key in keys])

                    command = "keys"
                elif noun == "orgs":
                    def foo(user: NamedUser):
                        orgs = list(user.get_orgs())
                        if len(orgs) == 0: return None
                        return ", ".join([org.login for org in orgs])

                    command = "organisations"
                elif noun == "url":
                    if "orgs" in adjectives:
                        foo = (lambda user: user.organizations_url)
                        command = "organisations url"
                    elif "repos" in adjectives:
                        foo = (lambda user: user.repos_url)
                        command = "repositories url"
                    elif "subscriptions" in adjectives:
                        foo = (lambda user: user.subscriptions_url)
                        command = "subscriptions url"
                    elif "following" in adjectives:
                        foo = (lambda user: user.following_url)
                        command = "following url"
                    elif "gists" in adjectives:
                        foo = (lambda user: user.gists_url)
                        command = "gists url"
                    elif "avatar" in adjectives:
                        foo = (lambda user: user.avatar_url)
                        command = "avatar url"
                    elif "events" in adjectives:
                        foo = (lambda user: user.events_url)
                        command = "events url"
                    elif "followers" in adjectives:
                        foo = (lambda user: user.followers_url)
                        command = "events url"
                    elif "starred" in adjectives:
                        foo = (lambda user: user.starred_url)
                        command = "starred url"
                    elif "html" in adjectives:
                        foo = (lambda user: user.url)
                        command = "html url"
                    else:
                        foo = (lambda user: user.url)
                        command = "url"
                elif noun == "following":
                    def foo(user: NamedUser):
                        followings = list(user.get_following())
                        if len(followings) == 0: return None
                        return ", ".join([following.login for following in followings])

                    command = "following"
                elif noun == "name":
                    foo = (lambda user: user.name)
                    command = "name"
                elif noun == "bio":
                    foo = (lambda user: user.bio)
                    command = "bio"
                elif noun == "type":
                    foo = (lambda user: user.type)
                    command = "type"
                elif noun == "email":
                    foo = (lambda user: user.email)
                    command = "email"
                elif noun == "blog":
                    foo = (lambda user: user.blog)
                    command = "blog"
                elif noun == "data":
                    if "raw" in adjectives:
                        foo = (lambda user: user.raw_data)
                        command = "raw data"
                elif noun == "etag":
                    foo = (lambda user: user.etag)
                    command = "etag"
                elif noun == "id":
                    if "gravatar" in adjectives:
                        foo = (lambda user: user.gravatar_id)
                        command = "gravatar id"
                    else:
                        foo = (lambda user: user.id)
                        command = "id"
                elif noun == "company":
                    foo = (lambda user: user.company)
                    command = "company"
                elif noun == "followers":
                    def foo(user: NamedUser):
                        followers = list(user.get_followers())
                        if len(followers) == 0: return None
                        return ", ".join([follower.login for follower in followers])

                    command = "followers"
                elif noun == "plan":
                    if "collaborators" in adjectives:
                        def foo(user: NamedUser):
                            plan = user.plan
                            if plan is not None: return plan.collaborators

                        command = "collaborators plan"
                    elif "repos" in adjectives and "private" in adjectives:
                        def foo(user: NamedUser):
                            plan = user.plan
                            if plan is not None: return plan.private_repos

                        command = "repositories plan"
                    elif "space" in adjectives:
                        def foo(user: NamedUser):
                            plan = user.plan
                            if plan is not None: return plan.space

                        command = "space plan"
                    elif "name" in adjectives:
                        def foo(user: NamedUser):
                            plan = user.plan
                            if plan is not None: return plan.name

                        command = "name plan"
                    else:
                        def foo(user: NamedUser):
                            plan = user.plan
                            if plan is not None: return plan.name

                        command = "plan"
                elif noun == "hireable":
                    foo = (lambda user: user.hireable)
                    command = "hireable"
                elif noun == "login":
                    foo = (lambda user: user.login)
                    command = "login"
                elif noun == "location":
                    foo = (lambda user: user.location)
                    command = "login"
                elif noun == "headers":
                    if "raw" in adjectives:
                        foo = (lambda user: user.raw_headers)
                        command = "raw headers"
                elif noun == "date":
                    if "creation" in adjectives:
                        foo = (lambda user: user.created_at)
                        command = "creation date"
                    elif "update" in adjectives:
                        foo = (lambda user: user.updated_at)
                        command = "update date"
                    elif "modification" in adjectives and "last" in adjectives:
                        foo = (lambda user: user.last_modified)
                        command = "modification date"
                if foo is not None:
                    self.execute(command, pps, foo)

    def store(self, vp):
        for nps in vp["NP"]:
            for np in nps["NP"]:
                if "NN" in np:
                    noun = simplify_word(np["NN"])
                else:
                    continue
                if noun == "user":
                    features = [np for pp in nps["PP"] if pp["IN"] == "with" for np in pp["NP"]]
                    for feature in features:
                        if "NN" in feature:
                            noun = simplify_word(feature["NN"])
                            adjectives = simplify_exp(feature["JJ"])
                        else:
                            continue
                        if "name" in adjectives or "login" in adjectives:
                            login = noun
                            try:
                                self._stored["user"] = self._connector.user(login)
                                self.print("I remember it")
                            except GithubException as ex:
                                if ex.status == 404:
                                    self.print("User with login of \"{}\" not found".format(login))
                elif noun == "me":
                    if self._connector.authorised() is not None:
                        self._stored["user"] = self._connector.user()
                        self.print("I remember it")
                    else:
                        self.print("I don't know who are you")
                elif noun == "repo":
                    pass
                elif noun == "gist":
                    pass

