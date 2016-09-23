from main.types.Function import Function
from src.main.types.Types import *
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
        "user": Function([String()], User(), lambda login: get_git_connector().user(login)),
        "repo": Function([String()], Repo(), lambda _id: get_git_connector().repo(_id)),
        "gist": Function([String()], Gist(), lambda _id: get_git_connector().gist(_id)),
        "name": Function([String()], Name(), lambda _str: _str),
        "login": Function([String()], Login(), lambda _str: _str),
        "key": Function([String()], Key(), lambda _str: _str),
        "id": Function([String()], Id(), lambda _str: _str),
        "url": Function([String()], Url(), lambda _str: _str),
        "email": Function([String()], Email(), lambda _str: _str)
    }
    return flat_map


def create_storeds_map() -> dict:
    flat_map = {
        User(): None,
        Repo(): None,
        Gist(): None
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
                Function([String()], List(Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([Login()], List(Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([User()], List(Repo()), lambda user: list(user.get_repos()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], List(Repo()), lambda: list(get_git_connector().user().get_repos()))
            ]},
            {"JJ": ["starred"], "F": [
                Function([String()], List(Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([Login()], List(Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([User()], List(Repo()), lambda user: list(user.get_starred()))
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                Function([String()], List(Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([Login()], List(Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([User()], List(Gist()), lambda user: list(user.get_gists()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], List(Gist()), lambda: list(get_git_connector().user().get_gists()))
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                Function([String()], Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([Login()], Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([User()], Key(), lambda user: list(user.get_keys()))
            ]},
            {"JJ": ["my"], "F": [
                Function([], Key(), lambda: list(get_git_connector().user().get_keys()))
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                Function([String()], Name(), lambda login: get_git_connector().user(login).name),
                Function([Login()], Name(), lambda login: get_git_connector().user(login).name),
                Function([User()], Name(), lambda user: user.name),
                Function([Repo()], Name(), lambda repo: repo.name)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Name(), lambda: get_git_connector().user().name)
            ]}
        ],
        "email": [
            {"JJ": [], "F": [
                Function([String()], Email(), lambda login: get_git_connector().user(login).isemail),
                Function([Login()], Email(), lambda login: get_git_connector().user(login).isemail),
                Function([User()], Email(), lambda user: user.isemail),
                Function([Email()], Email(), lambda email: email)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Email(), lambda: get_git_connector().user().isemail)
            ]}
        ],
        "login": [
            {"JJ": [], "F": [
                Function([String()], Login(), lambda login: get_git_connector().user(login).login),
                Function([Login()], Login(), lambda login: get_git_connector().user(login).login),
                Function([User()], Login(), lambda user: user.login)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Login(), lambda: get_git_connector().user().login)
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                Function([String()], Url(), lambda login: get_git_connector().user(login).isurl),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).isurl),
                Function([User()], Url(), lambda user: user.isurl),
                Function([Url()], Url(), lambda url: url)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Url(), lambda: get_git_connector().user().isurl)
            ]},
            {"JJ": ["orgs"], "F": [
                Function([String()], Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([User()], Url(), lambda user: user.organizations_url)
            ]},
            {"JJ": ["my", "orgs"], "F": [
                Function([],
                         ["url"], lambda: get_git_connector().user().organizations_url)
            ]},
            {"JJ": ["avatar"], "F": [
                Function([String()], Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([User()], Url(), lambda user: user.avatar_url)
            ]},
            {"JJ": ["my", "avatar"], "F": [
                Function([], Url(), lambda: get_git_connector().user().avatar_url)
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                Function([String()], User(), lambda login: get_git_connector().user(login)),
                Function([Login()], User(), lambda login: get_git_connector().user(login)),
                Function([List(User()), String()], User(), lambda _list, _str: _list[Simplifier.number(_str)]),
                Function([List(User()), Integer()], User(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], User(), lambda: get_stored(User()))
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                Function([String(), String()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([String(), Name()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([String(), Id()], Repo(), lambda login, _id: get_git_connector().user(login).get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([Login(), String()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Login(), Name()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Login(), Id()], Repo(), lambda login, _id: get_git_connector().user(login).get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([User(), String()], Repo(), lambda user, name: user.get_repo(name)),
                Function([User(), Name()], Repo(), lambda user, name: user.get_repo(name)),
                Function([User(), Id()], Repo(), lambda user, _id: user.get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([String()], Repo(), lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None),
                Function([Id()], Repo(), lambda _id: get_git_connector().repo(int(_id)) if _id.isnumeric() else None),
                Function([List(Repo()), String()], Repo(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([List(Repo()), Integer()], Repo(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], Repo(), lambda: get_stored(Repo()))
            ]},
            {"JJ": ["my"], "F": [
                Function([String()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Name()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Id()], Repo(), lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name) if _id.isnumeric() else None)
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                Function([String(), String()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([String(), Id()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Login(), String()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Login(), Id()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([User(), String()], Gist(), lambda user, _id: user.get_gist(_id)),
                Function([User(), Id()], Gist(), lambda user, _id: user.get_gist(_id)),
                Function([String()], Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([Id()], Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([List(Gist()), String()], Gist(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([List(Gist()), Integer()], Gist(), lambda _list, number: _list[number.value])
            ]},
            {"JJ": ["this"], "F": [
                Function([], Repo(), lambda: get_stored(Repo()))
            ]},
            {"JJ": ["my"], "F": [
                Function([String()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Name()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Id()], Repo(), lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name))
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                Function([String()], Id(), lambda login: get_git_connector().user(login).id),
                Function([Login()], Id(), lambda login: get_git_connector().user(login).id),
                Function([User()], Id(), lambda user: user.id),
                Function([Repo()], Id(), lambda repo: repo.id),
                Function([Gist()], Id(), lambda gist: gist.id),
                Function([Key()], Id(), lambda key: key.id)
            ]},
            {"JJ": ["my"], "F": [
                Function([], Id(), lambda: get_git_connector().user().id)
            ]}
        ],
        "key": [
            {"JJ": [], "F": [
                Function([String()], Key(), lambda _str: _str)
            ]}
        ]
    }
    return flat_map
