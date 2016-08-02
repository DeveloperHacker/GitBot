from github import Github, NamedUser, GithubException


class GitConnector:
    def __init__(self):
        self._git = Github()

    def login(self, login: str, pword: str) -> str:
        self._git = Github(login, pword)
        try:
            nick = self.user().login
        except GithubException:
            return None
        else:
            return nick

    def unlogin(self):
        self._git = Github()

    def user(self, login=None) -> NamedUser:
        return self._git.get_user() if login is None else self._git.get_user(login)

    def repos(self, login=None):
        return self.user(login).get_repos()

    def public_repos(self, login=None):
        return self.user(login).public_repos

    def owned_private_repos(self, login=None):
        return self.user(login).owned_private_repos

    def total_private_repos(self, login=None):
        return self.user(login).total_private_repos

    def url(self, login: str):
        return self.user(login).url

    def organizations_url(self, login: str):
        return self.user(login).organizations_url

    def repos_url(self, login: str):
        return self.user(login).repos_url

    def subscriptions_url(self, login: str):
        return self.user(login).subscriptions_url

    def following_url(self, login: str):
        return self.user(login).following_url

    def received_events_url(self, login: str):
        return self.user(login).received_events_url

    def gists_url(self, login: str):
        return self.user(login).gists_url

    def avatar_url(self, login: str):
        return self.user(login).avatar_url

    def events_url(self, login: str):
        return self.user(login).events_url

    def followers_url(self, login: str):
        return self.user(login).followers_url

    def starred_url(self, login: str):
        return self.user(login).starred_url

