from main.types.Function import Function
from src.main.nlp.Number import Number
from src.main.types import Types
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
        "user": Function([Types.String()], Types.User(), lambda login: get_git_connector().user(login)),
        "repo": Function([Types.String()], Types.Repo(), lambda _id: get_git_connector().repo(_id)),
        "gist": Function([Types.String()], Types.Gist(), lambda _id: get_git_connector().gist(_id)),
        "name": Function([Types.String()], Types.Name(), lambda _str: _str),
        "login": Function([Types.String()], Types.Login(), lambda _str: _str),
        "key": Function([Types.String()], Types.Key(), lambda _str: _str),
        "id": Function([Types.String()], Types.Id(), lambda _str: _str),
        "url": Function([Types.String()], Types.Url(), lambda _str: _str),
        "email": Function([Types.String()], Types.Email(), lambda _str: _str)
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
                Function([Types.String()], Types.List(Types.Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([Types.Login()], Types.List(Types.Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([Types.User()], Types.List(Types.Repo()), lambda user: list(user.get_repos()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.List(Types.Repo()), lambda: list(get_git_connector().user().get_repos()))
            ]},
            {"JJ": ["starred"], "F": [
                Function([Types.String()], Types.List(Types.Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([Types.Login()], Types.List(Types.Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([Types.User()], Types.List(Types.Repo()), lambda user: list(user.get_starred()))
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.List(Types.Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([Types.Login()], Types.List(Types.Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([Types.User()], Types.List(Types.Gist()), lambda user: list(user.get_gists()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.List(Types.Gist()), lambda: list(get_git_connector().user().get_gists()))
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([Types.Login()], Types.Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([Types.User()], Types.Key(), lambda user: list(user.get_keys()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Key(), lambda: list(get_git_connector().user().get_keys()))
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Name(), lambda login: get_git_connector().user(login).name),
                Function([Types.Login()], Types.Name(), lambda login: get_git_connector().user(login).name),
                Function([Types.User()], Types.Name(), lambda user: user.name),
                Function([Types.Repo()], Types.Name(), lambda repo: repo.name)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Name(), lambda: get_git_connector().user().name)
            ]}
        ],
        "email": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Email(), lambda login: get_git_connector().user(login).isemail),
                Function([Types.Login()], Types.Email(), lambda login: get_git_connector().user(login).isemail),
                Function([Types.User()], Types.Email(), lambda user: user.isemail),
                Function([Types.Email()], Types.Email(), lambda email: email)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Email(), lambda: get_git_connector().user().isemail)
            ]}
        ],
        "login": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Login(), lambda login: get_git_connector().user(login).login),
                Function([Types.Login()], Types.Login(), lambda login: get_git_connector().user(login).login),
                Function([Types.User()], Types.Login(), lambda user: user.login)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Login(), lambda: get_git_connector().user().login)
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Url(), lambda login: get_git_connector().user(login).isurl),
                Function([Types.Login()], Types.Url(), lambda login: get_git_connector().user(login).isurl),
                Function([Types.User()], Types.Url(), lambda user: user.isurl),
                Function([Types.Url()], Types.Url(), lambda url: url)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Url(), lambda: get_git_connector().user().isurl)
            ]},
            {"JJ": ["orgs"], "F": [
                Function([Types.String()], Types.Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([Types.Login()], Types.Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([Types.User()], Types.Url(), lambda user: user.organizations_url)
            ]},
            {"JJ": ["my", "orgs"], "F": [
                Function([],
                         ["url"], lambda: get_git_connector().user().organizations_url)
            ]},
            {"JJ": ["avatar"], "F": [
                Function([Types.String()], Types.Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([Types.Login()], Types.Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([Types.User()], Types.Url(), lambda user: user.avatar_url)
            ]},
            {"JJ": ["my", "avatar"], "F": [
                Function([], Types.Url(), lambda: get_git_connector().user().avatar_url)
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.User(), lambda login: get_git_connector().user(login)),
                Function([Types.Login()], Types.User(), lambda login: get_git_connector().user(login)),
                Function([Types.List(Types.User()), Types.String()], Types.User(), lambda _list, _str: _list[Simplifier.number(_str)]),
                Function([Types.List(Types.User()), Types.Integer()], Types.User(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], Types.User(), lambda: get_stored(Types.User()))
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                Function([Types.String(), Types.String()], Types.Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Types.String(), Types.Name()], Types.Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Types.String(), Types.Id()], Types.Repo(), lambda login, _id: get_git_connector().user(login).get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([Types.Login(), Types.String()], Types.Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Types.Login(), Types.Name()], Types.Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Types.Login(), Types.Id()], Types.Repo(), lambda login, _id: get_git_connector().user(login).get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([Types.User(), Types.String()], Types.Repo(), lambda user, name: user.get_repo(name)),
                Function([Types.User(), Types.Name()], Types.Repo(), lambda user, name: user.get_repo(name)),
                Function([Types.User(), Types.Id()], Types.Repo(), lambda user, _id: user.get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([Types.String()], Types.Repo(), lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None),
                Function([Types.Id()], Types.Repo(), lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None),
                Function([Types.List(Types.Repo()), Types.String()], Types.Repo(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([Types.List(Types.Repo()), Types.Integer()], Types.Repo(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], Types.Repo(), lambda: get_stored(Types.Repo()))
            ]},
            {"JJ": ["my"], "F": [
                Function([Types.String()], Types.Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Types.Name()], Types.Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Types.Id()], Types.Repo(), lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name) if _id.isnumeric() else None)
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                Function([Types.String(), Types.String()], Types.Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Types.String(), Types.Id()], Types.Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Types.Login(), Types.String()], Types.Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Types.Login(), Types.Id()], Types.Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Types.User(), Types.String()], Types.Gist(), lambda user, _id: user.get_gist(_id)),
                Function([Types.User(), Types.Id()], Types.Gist(), lambda user, _id: user.get_gist(_id)),
                Function([Types.String()], Types.Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([Types.Id()], Types.Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([Types.List(Types.Gist()), Types.String()], Types.Gist(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([Types.List(Types.Gist()), Types.Integer()], Types.Gist(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], Types.Repo(), lambda: get_stored(Types.Repo()))
            ]},
            {"JJ": ["my"], "F": [
                Function([Types.String()], Types.Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Types.Name()], Types.Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Types.Id()], Types.Repo(), lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name))
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Id(), lambda login: get_git_connector().user(login).id),
                Function([Types.Login()], Types.Id(), lambda login: get_git_connector().user(login).id),
                Function([Types.User()], Types.Id(), lambda user: user.id),
                Function([Types.Repo()], Types.Id(), lambda repo: repo.id),
                Function([Types.Gist()], Types.Id(), lambda gist: gist.id),
                Function([Types.Key()], Types.Id(), lambda key: key.id)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Types.Id(), lambda: get_git_connector().user().id)
            ]}
        ],
        "key": [
            {"JJ": [], "F": [
                Function([Types.String()], Types.Key(), lambda _str: _str)
            ]}
        ]
    }
    return flat_map
