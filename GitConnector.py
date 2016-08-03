
import github.GithubObject
from github import Github, GithubException


class GitConnector:
    def __init__(self):
        self._git = Github()
        self._authorised = None

    def authorise(self, login: str, pword: str) -> str:
        self._git = Github(login, pword)
        try:
            nick = self._git.get_user().login
        except GithubException:
            return None
        else:
            self._authorised = nick.lower()
            return nick

    def unlogin(self):
        self._authorised = None
        self._git = Github()

    def authorised(self) -> str:
        return self._authorised

    def user(self, login):
        return self._git.get_user(login)

    def get_repos(self, login):
        return self._git.get_user(login).get_repos()

    def get_starred_repos(self, login):
        return self._git.get_user(login).get_starred()

    def get_gists(self, login):
        return self._git.get_user(login).get_gists()
    
    # def get_starred_gists(self, login):
    #     if login.lower() != self._authorised: return []
    #     return self._git.get_user(login).get_starred_gists()

    # def get_emails(self, login):
    #     if login.lower() != self._authorised: return []
    #     return self._git.get_user().get_emails()
    
    def get_keys(self, login):
        return self._git.get_user(login).get_keys()

    def get_orgs(self, login):
        return self._git.get_user(login).get_orgs()

    def get_followings(self, login):
        return self._git.get_user(login).get_following()

    def get_followers(self, login):
        return self._git.get_user(login).get_followers()

    def get_events(self, login):
        return self._git.get_user(login).get_events()

    def public_repos(self, login):
        return self._git.get_user(login).public_repos

    def owned_private_repos(self, login):
        return self._git.get_user(login).owned_private_repos

    def total_private_repos(self, login):
        return self._git.get_user(login).total_private_repos

    def url(self, login: str):
        return self._git.get_user(login).url

    def organizations_url(self, login: str):
        return self._git.get_user(login).organizations_url

    def repos_url(self, login: str):
        return self._git.get_user(login).repos_url

    def subscriptions_url(self, login: str):
        return self._git.get_user(login).subscriptions_url

    def following_url(self, login: str):
        return self._git.get_user(login).following_url

    def received_events_url(self, login: str):
        return self._git.get_user(login).received_events_url

    def gists_url(self, login: str):
        return self._git.get_user(login).gists_url

    def avatar_url(self, login: str):
        return self._git.get_user(login).avatar_url

    def events_url(self, login: str):
        return self._git.get_user(login).events_url

    def followers_url(self, login: str):
        return self._git.get_user(login).followers_url

    def html_url(self, login: str):
        return self._git.get_user(login).html_url

    def starred_url(self, login: str):
        return self._git.get_user(login).starred_url

    def public_gists(self, login: str):
        return self._git.get_user(login).public_gists

    def private_gists(self, login: str):
        return self._git.get_user(login).private_gists

    def created_at(self, login: str):
        return self._git.get_user(login).created_at

    def updated_at(self, login: str):
        return self._git.get_user(login).updated_at

    def last_modified(self, login: str):
        return self._git.get_user(login).last_modified

    def following(self, login: str):
        return self._git.get_user(login).following

    def name(self, login: str):
        return self._git.get_user(login).name

    def bio(self, login: str):
        return self._git.get_user(login).bio

    def type(self, login: str):
        return self._git.get_user(login).type

    def email(self, login: str):
        return self._git.get_user(login).email

    def blog(self, login: str):
        return self._git.get_user(login).blog

    def collaborators(self, login: str):
        return self._git.get_user(login).collaborators

    def raw_data(self, login: str):
        return self._git.get_user(login).raw_data

    def etag(self, login: str):
        return self._git.get_user(login).etag

    def id(self, login: str):
        return self._git.get_user(login).id

    def gravatar_id(self, login: str):
        return self._git.get_user(login).gravatar_id

    def company(self, login: str):
        return self._git.get_user(login).company

    def followers(self, login: str):
        return self._git.get_user(login).followers

    def plan(self, login: str):
        return self._git.get_user(login).plan

    def hireable(self, login: str):
        return self._git.get_user(login).hireable

    def login(self, login: str):
        return self._git.get_user(login).login

    def location(self, login: str):
        return self._git.get_user(login).location

    def raw_headers(self, login: str):
        return self._git.get_user(login).raw_headers

