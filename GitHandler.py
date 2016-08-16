from Tools.scripts.treesync import raw_input

from github import GithubException
from github.NamedUser import NamedUser

import Parser
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

    def handle(self):
        data = self.read()
        root = Parser.parse(data)
        # print(root)
        for sentence in root["S"]:
            if sentence is None: continue
            for action in sentence["AA"]:
                verb = simplify_word(action["VV"])
                if verb in self._commands: self._commands[verb](action)

    def login(self, action):
        if self._connector.authorised():
            self.print("you need to unlogin before you login again")
        else:
            self.print("login:")
            login = self.read()
            self.print("password:")
            pword = self.read()
            if not self._connector.authorise(login, pword):
                self._nick = self._default_nick
                self.print("Incorrect input: login or password")
            else:
                self._nick = self._connector.authorised()

    def unlogin(self, action):
        if self._connector.authorised():
            self._connector.unlogin()
            self._nick = self._default_nick

    def close(self, action):
        self.print("Bye")
        self.stop()

    #     Warning
    #     I do not know how I it writen

    # ToDo: something

    def execute(self, command: str, subjects, foo):
        if len(subjects) == 0 and self._connector.authorised() is not None:
            user = self._connector.user()
            value = foo(user)
            self.print("{}: {}".format(command, value if value else "\"Access closed\""))
        else:
            for subject in subjects:
                login = subject["NN"]
                try:
                    if login == "user" and "this" in subject["JJ"]:
                        user = self._stored["user"]
                        if user is None:
                            self.print("I did not remember any user")
                            continue
                    else:
                        user = self._connector.user(login)
                    login = user.login
                    value = foo(user)
                    self.print("{} at {}: {}".format(command, login, value if value else "\"Access closed\""))
                except GithubException as ex:
                    if ex.status == 404:
                        self.print("User with login of \"{}\" not found".format(login))
                    elif ex.status == 403:
                        self.print(ex.data["message"])
                    else:
                        raise ex
                    
    def count(self, action):
        for subj in action["SS"]:
            name = subj["NN"]
            adjectives = subj["JJ"]
            foo = None
            if name == "repos":
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
            elif name == "gists":
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
            elif name == "following":
                foo = (lambda user: user.following)
                command = "following"
            elif name == "collaborators":
                foo = (lambda user: user.collaborators)
                command = "collaborators"
            elif name == "followers":
                foo = (lambda user: user.followers)
                command = "followers"
            if foo is not None:
                subjects = [pp for pps in subj["PP"] if pps["IN"].lower() in {"in", "into", "at"} for pp in pps["SS"]]
                self.execute(command, subjects, foo)

    def show(self, action):
        for subj in action["SS"]:
            name = simplify_word(subj["NN"])
            adjectives = simplify_exp(subj["JJ"])
            foo = None
            if name == "repos":
                def foo(user: NamedUser):
                    repos = list(user.get_repos())
                    if len(repos) == 0: return None
                    return ", ".join([repo.name for repo in repos])
                command = "repositories"
            if name == "gists":
                def foo(user: NamedUser):
                    gists = list(user.get_gists())
                    if len(gists) == 0: return None
                    return ", ".join([gist.id for gist in gists])
                command = "gists"
            if name == "keys":
                def foo(user: NamedUser):
                    keys = list(user.get_keys())
                    if len(keys) == 0: return None
                    return ", ".join(["(id: " + str(key.id) + " key: " + key.key + ") " for key in keys])
                command = "keys"
            if name == "orgs":
                def foo(user: NamedUser):
                    orgs = list(user.get_orgs())
                    if len(orgs) == 0: return None
                    return ", ".join([org.login for org in orgs])
                command = "organisations"
            elif name == "url":
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
            elif name == "following":
                def foo(user: NamedUser):
                    followings = list(user.get_following())
                    if len(followings) == 0: return None
                    return ", ".join([following.login for following in followings])
                command = "following"
            elif name == "name":
                foo = (lambda user: user.name)
                command = "name"
            elif name == "bio":
                foo = (lambda user: user.bio)
                command = "bio"
            elif name == "type":
                foo = (lambda user: user.type)
                command = "type"
            elif name == "email":
                foo = (lambda user: user.email)
                command = "email"
            elif name == "blog":
                foo = (lambda user: user.blog)
                command = "blog"
            elif name == "data":
                if "raw" in adjectives:
                    foo = (lambda user: user.raw_data)
                    command = "raw data"
            elif name == "etag":
                foo = (lambda user: user.etag)
                command = "etag"
            elif name == "id":
                if "gravatar" in adjectives:
                    foo = (lambda user: user.gravatar_id)
                    command = "gravatar id"
                else:
                    foo = (lambda user: user.id)
                    command = "id"
            elif name == "company":
                foo = (lambda user: user.company)
                command = "company"
            elif name == "followers":
                def foo(user: NamedUser):
                    followers = list(user.get_followers())
                    if len(followers) == 0: return None
                    return ", ".join([follower.login for follower in followers])
                command = "followers"
            elif name == "plan":
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
            elif name == "hireable":
                foo = (lambda user: user.hireable)
                command = "hireable"
            elif name == "login":
                foo = (lambda user: user.login)
                command = "login"
            elif name == "location":
                foo = (lambda user: user.location)
                command = "login"
            elif name == "headers":
                if "raw" in adjectives:
                    foo = (lambda user: user.raw_headers)
                    command = "raw headers"
            elif name == "date":
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
                subjects = [pp for pps in subj["PP"] if pps["IN"].lower() in {"in", "into", "at", "for"} for pp in pps["SS"]]
                self.execute(command, subjects, foo)

    def store(self, action):
        for subj in action["SS"]:
            name = simplify_word(subj["NN"])
            features = [s for pp in subj["PP"] if pp["IN"] in {"with"} for s in pp["SS"]]
            if name == "user":
                for feature in features:
                    if "name" in feature["JJ"] or "login" in feature["JJ"]:
                        login = feature["NN"]
                        try:
                            self._stored["user"] = self._connector.user(login)
                            self.print("I remember it")
                        except GithubException as ex:
                            if ex.status == 404:
                                self.print("User with login of \"{}\" not found".format(login))
            elif name == "me":
                if self._connector.authorised() is not None:
                    self._stored["user"] = self._connector.user()
                    self.print("I remember it")
                else:
                    self.print("I don't know who are you")
            elif name == "repo":
                pass
            elif name == "gist":
                pass
