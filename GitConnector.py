
from github import Github
from github.GithubException import BadCredentialsException


class GitConnector:
    def __init__(self):
        self._git = Github()
        self._authorised = None

    def authorise(self, login: str, pword: str) -> str:
        self._git = Github(login, pword)
        try:
            self._authorised = self._git.get_user().login
        except BadCredentialsException:
            return False
        else:
            return True

    def unlogin(self):
        self._authorised = None
        self._git = Github()

    def authorised(self) -> str:
        return self._authorised

    def user(self, login=None):
        if self._authorised and (not login or login.lower() == self._authorised.lower()):
            return self._git.get_user()
        else:
            return self._git.get_user(login)
