from src.main.tree.Type import Type
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

NONE = {"T": Type("none"), "O": None}

similar_types = {
    Type("user"): {"T": Type("login"), "C": lambda user: user.login},
    Type("repo"): {"T": Type("id"), "C": lambda repo: repo.id},
    Type("gist"): {"T": Type("id"), "C": lambda gist: gist.id},
    Type("name"): {"T": Type("str"), "C": lambda name: str(name)},
    Type("login"): {"T": Type("str"), "C": lambda login: str(login)},
    Type("url"): {"T": Type("str"), "C": lambda url: str(url)},
    Type("email"): {"T": Type("str"), "C": lambda email: str(email)},
    Type("key"): {"T": Type("str"), "C": lambda key: str(key)},
    Type("id"): {"T": Type("str"), "C": lambda _id: str(_id)}
}


def create_type_builders_mpa(get_git_connector) -> dict:
    flat_map = {
        "user": {"A": [Type("str")],
                 "T": Type("user"),
                 "B": lambda login: get_git_connector().user(login)},
        "repo": {"A": [Type("str")],
                 "T": Type("repo"),
                 "B": lambda _id: get_git_connector().repo(_id)},
        "gist": {"A": [Type("str")],
                 "T": Type("gist"),
                 "B": lambda _id: get_git_connector().gist(_id)},
        "name": {"A": [Type("str")],
                 "T": Type("name"),
                 "B": lambda _str: _str},
        "login": {"A": [Type("str")],
                  "T": Type("login"),
                  "B": lambda _str: _str},
        "key": {"A": [Type("str")],
                "T": Type("key"),
                "B": lambda _str: _str},
        "id": {"A": [Type("str")],
               "T": Type("id"),
               "B": lambda _str: _str},
        "url": {"A": [Type("str")],
                "T": Type("url"),
                "B": lambda _str: _str},
        "email": {"A": [Type("str")],
                  "T": Type("email"),
                  "B": lambda _str: _str}
    }
    return flat_map


def create_storeds_map() -> dict:
    flat_map = {
        Type("user"): None,
        Type("repo"): None,
        Type("gist"): None
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
                {"A": [Type("str")],
                 "T": Type("repos"),
                 "B": lambda login: list(get_git_connector().user(login).get_repos())},
                {"A": [Type("login")],
                 "T": Type("repos"),
                 "B": lambda login: list(get_git_connector().user(login).get_repos())},
                {"A": [Type("user")],
                 "T": Type("repos"),
                 "B": lambda user: list(user.get_repos())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("repos"),
                 "B": lambda: list(get_git_connector().user().get_repos())}
            ]},
            {"JJ": ["starred"], "F": [
                {"A": [Type("str")],
                 "T": Type("repos"),
                 "B": lambda login: list(get_git_connector().user(login).get_starred())},
                {"A": [Type("login")],
                 "T": Type("repos"),
                 "B": lambda login: list(get_git_connector().user(login).get_starred())},
                {"A": [Type("user")],
                 "T": Type("repos"),
                 "B": lambda user: list(user.get_starred())}
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("gists"),
                 "B": lambda login: list(get_git_connector().user(login).get_gists())},
                {"A": [Type("login")],
                 "T": Type("gists"),
                 "B": lambda login: list(get_git_connector().user(login).get_gists())},
                {"A": [Type("user")],
                 "T": Type("gists"),
                 "B": lambda user: list(user.get_gists())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("gists"),
                 "B": lambda: list(get_git_connector().user().get_gists())}
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("keys"),
                 "B": lambda login: list(get_git_connector().user(login).get_keys())},
                {"A": [Type("login")],
                 "T": Type("keys"),
                 "B": lambda login: list(get_git_connector().user(login).get_keys())},
                {"A": [Type("user")],
                 "T": Type("keys"),
                 "B": lambda user: list(user.get_keys())}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("keys"),
                 "B": lambda: list(get_git_connector().user().get_keys())}
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("name"),
                 "B": lambda login: get_git_connector().user(login).name},
                {"A": [Type("login")],
                 "T": Type("name"),
                 "B": lambda login: get_git_connector().user(login).name},
                {"A": [Type("user")],
                 "T": Type("name"),
                 "B": lambda user: user.name},
                {"A": [Type("repo")],
                 "T": Type("name"),
                 "B": lambda repo: repo.name}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("name"),
                 "B": lambda: get_git_connector().user().name}
            ]}
        ],
        "email": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("email"),
                 "B": lambda login: get_git_connector().user(login).email},
                {"A": [Type("login")],
                 "T": Type("email"),
                 "B": lambda login: get_git_connector().user(login).email},
                {"A": [Type("user")],
                 "T": Type("email"),
                 "B": lambda user: user.email},
                {"A": [Type("email")],
                 "T": Type("email"),
                 "B": lambda email: email}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("email"),
                 "B": lambda: get_git_connector().user().email}
            ]}
        ],
        "login": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("login"),
                 "B": lambda login: get_git_connector().user(login).login},
                {"A": [Type("login")],
                 "T": Type("login"),
                 "B": lambda login: get_git_connector().user(login).login},
                {"A": [Type("user")],
                 "T": Type("login"),
                 "B": lambda user: user.login}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("login"),
                 "B": lambda: get_git_connector().user().login}
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).url},
                {"A": [Type("login")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).url},
                {"A": [Type("user")],
                 "T": Type("url"),
                 "B": lambda user: user.url},
                {"A": [Type("url")],
                 "T": Type("url"),
                 "B": lambda url: url}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("url"),
                 "B": lambda: get_git_connector().user().url}
            ]},
            {"JJ": ["orgs"], "F": [
                {"A": [Type("str")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [Type("login")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [Type("user")],
                 "T": Type("url"),
                 "B": lambda user: user.organizations_url}
            ]},
            {"JJ": ["my", "orgs"], "F": [
                {"A": [],
                 "T": ["url"],
                 "B": lambda: get_git_connector().user().organizations_url}
            ]},
            {"JJ": ["avatar"], "F": [
                {"A": [Type("str")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [Type("login")],
                 "T": Type("url"),
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [Type("user")],
                 "T": Type("url"),
                 "B": lambda user: user.avatar_url}
            ]},
            {"JJ": ["my", "avatar"], "F": [
                {"A": [],
                 "T": Type("url"),
                 "B": lambda: get_git_connector().user().avatar_url}
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("user"),
                 "B": lambda login: get_git_connector().user(login)},
                {"A": [Type("login")],
                 "T": Type("user"),
                 "B": lambda login: get_git_connector().user(login)}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Type("user"),
                 "B": lambda: get_stored(Type("user"))}
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                {"A": [Type("str"), Type("str")],
                 "T": Type("repo"),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Type("str"), Type("name")],
                 "T": Type("repo"),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Type("str"), Type("id")],
                 "T": Type("repo"),
                 "B": lambda login, _id: get_git_connector().user(login).get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Type("login"), Type("str")],
                 "T": Type("repo"),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Type("login"), Type("name")],
                 "T": Type("repo"),
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [Type("login"), Type("id")],
                 "T": Type("repo"),
                 "B": lambda login, _id: get_git_connector().user(login).get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Type("user"), Type("str")],
                 "T": Type("repo"),
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [Type("user"), Type("name")],
                 "T": Type("repo"),
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [Type("user"), Type("id")],
                 "T": Type("repo"),
                 "B": lambda user, _id: user.get_repo(
                     get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None},
                {"A": [Type("str")],
                 "T": Type("repo"),
                 "B": lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None},
                {"A": [Type("id")],
                 "T": Type("repo"),
                 "B": lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None},
                {"A": [Type("repos"), Type("str")],
                 "T": Type("repo"),
                 "B": lambda _list, _str: _list[Simplifier.number(_str)]}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Type("repo"),
                 "B": lambda: get_stored(Type("repo"))}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [Type("str")],
                 "T": Type("repo"),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Type("name")],
                 "T": Type("repo"),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Type("id")],
                 "T": Type("repo"),
                 "B": lambda _id: get_git_connector().user().get_repo(
                     get_git_connector().repo(_id).name) if _id.isnumeric() else None}
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                {"A": [Type("str"), Type("str")],
                 "T": Type("gist"),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Type("str"), Type("id")],
                 "T": Type("gist"),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Type("login"), Type("str")],
                 "T": Type("gist"),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Type("login"), Type("id")],
                 "T": Type("gist"),
                 "B": lambda login, name: get_git_connector().user(login).get_gist(name)},
                {"A": [Type("user"), Type("str")],
                 "T": Type("gist"),
                 "B": lambda user, _id: user.get_gist(_id)},
                {"A": [Type("user"), Type("id")],
                 "T": Type("gist"),
                 "B": lambda user, _id: user.get_gist(_id)},
                {"A": [Type("str")],
                 "T": Type("gist"),
                 "B": lambda _id: get_git_connector().gist(_id)},
                {"A": [Type("id")],
                 "T": Type("gist"),
                 "B": lambda _id: get_git_connector().gist(_id)}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": Type("repo"),
                 "B": lambda: get_stored(Type("repo"))}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [Type("str")],
                 "T": Type("repo"),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Type("name")],
                 "T": Type("repo"),
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [Type("id")],
                 "T": Type("repo"),
                 "B": lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name)}
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("id"),
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [Type("login")],
                 "T": Type("id"),
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [Type("user")],
                 "T": Type("id"),
                 "B": lambda user: user.id},
                {"A": [Type("repo")],
                 "T": Type("id"),
                 "B": lambda repo: repo.id},
                {"A": [Type("gist")],
                 "T": Type("id"),
                 "B": lambda gist: gist.id},
                {"A": [Type("key")],
                 "T": Type("id"),
                 "B": lambda key: key.id}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": Type("id"),
                 "B": lambda: get_git_connector().user().id}
            ]}
        ],
        "key": [
            {"JJ": [], "F": [
                {"A": [Type("str")],
                 "T": Type("key"),
                 "B": lambda _str: _str}
            ]}
        ],
        "element": [
            {"JJ": [], "F": [
                {"A": [Type("repos"), Type("str")],
                 "T": Type("repo"),
                 "B": lambda _list, _str: _list[Simplifier.number(_str)]}
            ]}
        ]
    }
    return flat_map
