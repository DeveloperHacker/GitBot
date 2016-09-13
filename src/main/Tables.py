from src.main.nlp.Number import Number
from src.main.tree import Types
from src.main import Simplifier

synonyms = {
    "print": "show",
    "view": "show",
    "authorise": "login",
    "repository": "repo",
    "project": "repo",
    "storage": "repo",
    "repositories": "repos",
    "projects": "repos",
    "recruited": "hireable",
    "organisations": "orgs",
    "remember": "store",
    "quit": "bye",
    "disconnect": "bye",
    "close": "bye",
    "hi": "hello",
    "o/": "hello",
    "username": "login",
    "sign": "log"
}


def create_type_builders_mpa(get_git_connector) -> dict:
    flat_map = {
        "user": {"A": [Types.String()],
                 "T": Types.User(),
                 "B": lambda login: get_git_connector().user(login)},
        "repo": {"A": [Types.String()],
                 "T": Types.Repo(),
                 "B": lambda _id: get_git_connector().repo(_id)},
        "gist": {"A": [Types.String()],
                 "T": Types.Gist(),
                 "B": lambda _id: get_git_connector().gist(_id)},
        "name": {"A": [Types.String()],
                 "T": Types.Name(),
                 "B": lambda _str: _str},
        "login": {"A": [Types.String()],
                  "T": Types.Login(),
                  "B": lambda _str: _str},
        "key": {"A": [Types.String()],
                "T": Types.Key(),
                "B": lambda _str: _str},
        "id": {"A": [Types.String()],
               "T": Types.Id(),
               "B": lambda _str: _str},
        "url": {"A": [Types.String()],
                "T": Types.Url(),
                "B": lambda _str: _str},
        "email": {"A": [Types.String()],
                  "T": Types.Email(),
                  "B": lambda _str: _str}
    }
    return flat_map


def create_storeds_map() -> dict:
    flat_map = {
        Types.User(): None,
        Types.Repo(): None,
        Types.Gist(): None
    }
    return flat_map


def create_functions_map(get_git_handler) -> dict:
    flat_map = {
        "show": get_git_handler().show,
        "store": get_git_handler().store,
        "login": get_git_handler().login,
        "logout": get_git_handler().logout,
        "log": get_git_handler().log,
        "hello": get_git_handler().hello,
        "bye": get_git_handler().bye
    }
    return flat_map


def create_builders_map(get_git_connector, get_stored) -> dict:
    flat_map = {
        "repos": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda login: list(get_git_connector().user(login).get_repos())},
                {"A": [Types.Login()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda login: list(get_git_connector().user(login).get_repos())},
                {"A": [Types.User()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda user: list(user.get_repos())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.List(Types.Repo()),
                 "B": lambda: list(get_git_connector().user().get_repos())}
            ]},
            {"JJ": ["starred"], "F": [
                {"A": [Types.String()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda login: list(get_git_connector().user(login).get_starred())},
                {"A": [Types.Login()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda login: list(get_git_connector().user(login).get_starred())},
                {"A": [Types.User()],
                 "T": Types.List(Types.Repo()),
                 "B": lambda user: list(user.get_starred())}
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.List(Types.Gist()),
                 "B": lambda login: list(get_git_connector().user(login).get_gists())},
                {"A": [Types.Login()],
                 "T": Types.List(Types.Gist()),
                 "B": lambda login: list(get_git_connector().user(login).get_gists())},
                {"A": [Types.User()],
                 "T": Types.List(Types.Gist()),
                 "B": lambda user: list(user.get_gists())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.List(Types.Gist()),
                 "B": lambda: list(get_git_connector().user().get_gists())}
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Key(),
                 "B": lambda login: list(get_git_connector().user(login).get_keys())},
                {"A": [Types.Login()],
                 "T": Types.Key(),
                 "B": lambda login: list(get_git_connector().user(login).get_keys())},
                {"A": [Types.User()],
                 "T": Types.Key(),
                 "B": lambda user: list(user.get_keys())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Key(),
                 "B": lambda: list(get_git_connector().user().get_keys())}
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Name(),
                 "B": lambda login: get_git_connector().user(login).name},
                {"A": [Types.Login()],
                 "T": Types.Name(),
                 "B": lambda login: get_git_connector().user(login).name},
                {"A": [Types.User()],
                 "T": Types.Name(),
                 "B": lambda user: user.name},
                {"A": [Types.Repo()],
                 "T": Types.Name(),
                 "B": lambda repo: repo.name}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Name(),
                 "B": lambda: get_git_connector().user().name}
            ]}
        ],
        "email": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Email(),
                 "B": lambda login: get_git_connector().user(login).isemail},
                {"A": [Types.Login()],
                 "T": Types.Email(),
                 "B": lambda login: get_git_connector().user(login).isemail},
                {"A": [Types.User()],
                 "T": Types.Email(),
                 "B": lambda user: user.isemail},
                {"A": [Types.Email()],
                 "T": Types.Email(),
                 "B": lambda email: email}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Email(),
                 "B": lambda: get_git_connector().user().isemail}
            ]}
        ],
        "login": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Login(),
                 "B": lambda login: get_git_connector().user(login).login},
                {"A": [Types.Login()],
                 "T": Types.Login(),
                 "B": lambda login: get_git_connector().user(login).login},
                {"A": [Types.User()],
                 "T": Types.Login(),
                 "B": lambda user: user.login}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Login(),
                 "B": lambda: get_git_connector().user().login}
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).isurl},
                {"A": [Types.Login()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).isurl},
                {"A": [Types.User()],
                 "T": Types.Url(),
                 "B": lambda user: user.isurl},
                {"A": [Types.Url()],
                 "T": Types.Url(),
                 "B": lambda url: url}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Url(),
                 "B": lambda: get_git_connector().user().isurl}
            ]},
            {"JJ": ["orgs"], "F": [
                {"A": [Types.String()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [Types.Login()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [Types.User()],
                 "T": Types.Url(),
                 "B": lambda user: user.organizations_url}
            ]},
            {"JJ": ["my", "orgs"], "F": [
                {"A": [],
                 "T": ["url"],
                 "B": lambda: get_git_connector().user().organizations_url}
            ]},
            {"JJ": ["avatar"], "F": [
                {"A": [Types.String()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [Types.Login()],
                 "T": Types.Url(),
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [Types.User()],
                 "T": Types.Url(),
                 "B": lambda user: user.avatar_url}
            ]},
            {"JJ": ["my", "avatar"], "F": [
                {"A": [],
                 "T": Types.Url(),
                 "B": lambda: get_git_connector().user().avatar_url}
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.User(),
                 "B": lambda login: get_git_connector().user(login)},
                {"A": [Types.Login()],
                 "T": Types.User(),
                 "B": lambda login: get_git_connector().user(login)},
                {"A": [Types.List(Types.User()), Types.String()],
                 "T": Types.User(),
                 "B": lambda _list, _str: _list[Simplifier.number(_str)]},
                {"A": [Types.List(Types.User()), Types.Integer()],
                 "T": Types.User(),
                 "B": lambda _list, number: _list[number.value]}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Types.User(),
                 "B": lambda: get_stored(Types.User())}
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                {"A": [Types.String(), Types.String()],
                 "T": Types.Repo(),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Types.String(), Types.Name()],
                 "T": Types.Repo(),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Types.String(), Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda login, _id: get_git_connector().user(login).get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Types.Login(), Types.String()],
                 "T": Types.Repo(),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Types.Login(), Types.Name()],
                 "T": Types.Repo(),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Types.Login(), Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda login, _id: get_git_connector().user(login).get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Types.User(), Types.String()],
                 "T": Types.Repo(),
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [Types.User(), Types.Name()],
                 "T": Types.Repo(),
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [Types.User(), Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda user, _id: user.get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Types.String()],
                 "T": Types.Repo(),
                 "B": lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None},
                {"A": [Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None},
                {"A": [Types.List(Types.Repo()), Types.String()],
                 "T": Types.Repo(),
                 "B": lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None},
                {"A": [Types.List(Types.Repo()), Types.Integer()],
                 "T": Types.Repo(),
                 "B": lambda _list, number: _list[number.value]}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Types.Repo(),
                 "B": lambda: get_stored(Types.Repo())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [Types.String()],
                 "T": Types.Repo(),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Types.Name()],
                 "T": Types.Repo(),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda _id: get_git_connector().user().get_repo(
                     get_git_connector().repo(_id).name) if _id.isnumeric() else None}
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                {"A": [Types.String(), Types.String()],
                 "T": Types.Gist(),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Types.String(), Types.Id()],
                 "T": Types.Gist(),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Types.Login(), Types.String()],
                 "T": Types.Gist(),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Types.Login(), Types.Id()],
                 "T": Types.Gist(),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Types.User(), Types.String()],
                 "T": Types.Gist(),
                 "B": lambda user, _id: user.get_gist(_id)},
                {"A": [Types.User(), Types.Id()],
                 "T": Types.Gist(),
                 "B": lambda user, _id: user.get_gist(_id)},
                {"A": [Types.String()],
                 "T": Types.Gist(),
                 "B": lambda _id: get_git_connector().gist(_id)},
                {"A": [Types.Id()],
                 "T": Types.Gist(),
                 "B": lambda _id: get_git_connector().gist(_id)},
                {"A": [Types.List(Types.Gist()), Types.String()],
                 "T": Types.Gist(),
                 "B": lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None},
                {"A": [Types.List(Types.Gist()), Types.Integer()],
                 "T": Types.Gist(),
                 "B": lambda _list, number: _list[number.value]}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Types.Repo(),
                 "B": lambda: get_stored(Types.Repo())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [Types.String()],
                 "T": Types.Repo(),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Types.Name()],
                 "T": Types.Repo(),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Types.Id()],
                 "T": Types.Repo(),
                 "B": lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name)}
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Id(),
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [Types.Login()],
                 "T": Types.Id(),
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [Types.User()],
                 "T": Types.Id(),
                 "B": lambda user: user.id},
                {"A": [Types.Repo()],
                 "T": Types.Id(),
                 "B": lambda repo: repo.id},
                {"A": [Types.Gist()],
                 "T": Types.Id(),
                 "B": lambda gist: gist.id},
                {"A": [Types.Key()],
                 "T": Types.Id(),
                 "B": lambda key: key.id}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Types.Id(),
                 "B": lambda: get_git_connector().user().id}
            ]}
        ],
        "key": [
            {"JJ": [], "F": [
                {"A": [Types.String()],
                 "T": Types.Key(),
                 "B": lambda _str: _str}
            ]}
        ]
    }
    return flat_map
