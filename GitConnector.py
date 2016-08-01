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

    def repositories(self, login=None):
        return self.user(login).get_repos()

    def url(self, login: str):
        return self.user(login).url

