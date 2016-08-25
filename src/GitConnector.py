from github import Github
from github.Gist import Gist
from github.GithubException import BadCredentialsException
from github.NamedUser import NamedUser
from github.Repository import Repository


class GitConnector:
    def __init__(self):
        self._git = Github()
        self._authorised = None

    def authorise(self, login: str, pword: str) -> bool:
        self._git = Github(login, pword)
        try:
            self._authorised = self._git.get_user().login
        except BadCredentialsException:
            self._git = Github()
            return False
        else:
            return True

    def logout(self):
        self._authorised = None
        self._git = Github()

    def authorised(self) -> str:
        return self._authorised

    def user(self, login=None) -> NamedUser:
        if self._authorised and (not login or login.lower() == self._authorised.lower()):
            return self._git.get_user()
        else:
            return self._git.get_user(login)

    def repo(self, id) -> Repository:
        return self._git.get_repo(id)

    def gist(self, id) -> Gist:
        return self._git.get_gist(id)
