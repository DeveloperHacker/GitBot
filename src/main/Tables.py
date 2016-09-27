from src.main.types.Shell import Shell
from src.main.types.Function import Function
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
            Shell([], [
                Function([String()], List(Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([Login()], List(Repo()), lambda login: list(get_git_connector().user(login).get_repos())),
                Function([User()], List(Repo()), lambda user: list(user.get_repos()))
            ]),
            Shell(["my"], [
                Function([], List(Repo()), lambda: list(get_git_connector().user().get_repos()))
            ]),
            Shell(["starred"], [
                Function([String()], List(Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([Login()], List(Repo()), lambda login: list(get_git_connector().user(login).get_starred())),
                Function([User()], List(Repo()), lambda user: list(user.get_starred()))
            ])
        ],
        "gists": [
            Shell([], [
                Function([String()], List(Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([Login()], List(Gist()), lambda login: list(get_git_connector().user(login).get_gists())),
                Function([User()], List(Gist()), lambda user: list(user.get_gists()))
            ]),
            Shell(["my"], [
                Function([], List(Gist()), lambda: list(get_git_connector().user().get_gists()))
            ])
        ],
        "keys": [
            Shell([], [
                Function([String()], Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([Login()], Key(), lambda login: list(get_git_connector().user(login).get_keys())),
                Function([User()], Key(), lambda user: list(user.get_keys()))
            ]),
            Shell(["my"], [
                Function([], Key(), lambda: list(get_git_connector().user().get_keys()))
            ])
        ],
        "name": [
            Shell([], [
                Function([String()], Name(), lambda login: get_git_connector().user(login).name),
                Function([Login()], Name(), lambda login: get_git_connector().user(login).name),
                Function([User()], Name(), lambda user: user.name),
                Function([Repo()], Name(), lambda repo: repo.name)
            ]),
            Shell(["my"], [
                Function([], Name(), lambda: get_git_connector().user().name)
            ])
        ],
        "email": [
            Shell([], [
                Function([String()], Email(), lambda login: get_git_connector().user(login).isemail),
                Function([Login()], Email(), lambda login: get_git_connector().user(login).isemail),
                Function([User()], Email(), lambda user: user.isemail),
                Function([Email()], Email(), lambda email: email)
            ]),
            Shell(["my"], [
                Function([], Email(), lambda: get_git_connector().user().isemail)
            ])
        ],
        "login": [
            Shell([], [
                Function([String()], Login(), lambda login: get_git_connector().user(login).login),
                Function([Login()], Login(), lambda login: get_git_connector().user(login).login),
                Function([User()], Login(), lambda user: user.login)
            ]),
            Shell(["my"], [
                Function([], Login(), lambda: get_git_connector().user().login)
            ])
        ],
        "url": [
            Shell([], [
                Function([String()], Url(), lambda login: get_git_connector().user(login).isurl),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).isurl),
                Function([User()], Url(), lambda user: user.isurl),
                Function([Url()], Url(), lambda url: url)
            ]),
            Shell(["my"], [
                Function([], Url(), lambda: get_git_connector().user().isurl)
            ]),
            Shell(["orgs"], [
                Function([String()], Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).organizations_url),
                Function([User()], Url(), lambda user: user.organizations_url)
            ]),
            Shell(["my", "orgs"], [
                Function([],
                         ["url"], lambda: get_git_connector().user().organizations_url)
            ]),
            Shell(["avatar"], [
                Function([String()], Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([Login()], Url(), lambda login: get_git_connector().user(login).avatar_url),
                Function([User()], Url(), lambda user: user.avatar_url)
            ]),
            Shell(["my", "avatar"], [
                Function([], Url(), lambda: get_git_connector().user().avatar_url)
            ])
        ],
        "user": [
            Shell([], [
                Function([String()], User(), lambda login: get_git_connector().user(login)),
                Function([Login()], User(), lambda login: get_git_connector().user(login)),
                Function([List(User()), String()], User(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([List(User()), Integer()], User(), lambda _list, number: _list[int(number) - 1])
            ]),
            Shell(["this"], [
                Function([], User(), lambda: get_stored(User()))
            ])
        ],
        "repo": [
            Shell([], [
                Function([String(), String()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([String(), Name()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([String(), Integer()], Repo(), lambda login, number: get_git_connector().user(login).get_repo(get_git_connector().repo(int(number)).name)),
                Function([Login(), String()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Login(), Name()], Repo(), lambda login, name: get_git_connector().user(login).get_repo(name)),
                Function([Login(), Integer()], Repo(), lambda login, number: get_git_connector().user(login).get_repo(get_git_connector().repo(int(number)).name)),
                Function([User(), String()], Repo(), lambda user, name: user.get_repo(name)),
                Function([User(), Name()], Repo(), lambda user, name: user.get_repo(name)),
                Function([User(), Id()], Repo(), lambda user, _id: user.get_repo(get_git_connector().repo(int(_id)).name) if _id.isnumeric() else None),
                Function([String()], Repo(), lambda _str: get_git_connector().repo(int(Simplifier.number(_str))) if Number.isnumber(_str) else None),
                Function([Integer()], Repo(), lambda number: get_git_connector().repo(int(number))),
                Function([List(Repo()), String()], Repo(), lambda _list, _str: _list[Simplifier.number(_str)] if Number.isnumber(_str) else None),
                Function([List(Repo()), Integer()], Repo(), lambda _list, number: _list[int(number) - 1])
            ]),
            Shell(["this"], [
                Function([], Repo(), lambda: get_stored(Repo()))
            ]),
            Shell(["my"], [
                Function([String()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Name()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Integer()], Repo(), lambda number: get_git_connector().user().get_repo(get_git_connector().repo(int(number)).name))
            ])
        ],
        "gist": [
            Shell([], [
                Function([String(), String()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([String(), Id()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Login(), String()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([Login(), Id()], Gist(), lambda login, name: get_git_connector().user(login).get_gist(name)),
                Function([User(), String()], Gist(), lambda user, _id: user.get_gist(_id)),
                Function([User(), Id()], Gist(), lambda user, _id: user.get_gist(_id)),
                Function([String()], Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([Id()], Gist(), lambda _id: get_git_connector().gist(_id)),
                Function([List(Gist()), String()], Gist(), lambda _list, _str: _list[int(Simplifier.number(_str))] if Number.isnumber(_str) else None),
                Function([List(Gist()), Integer()], Gist(), lambda _list, number: _list[int(number) - 1])
            ]),
            Shell(["this"], [
                Function([], Repo(), lambda: get_stored(Repo()))
            ]),
            Shell(["my"], [
                Function([String()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Name()], Repo(), lambda name: get_git_connector().user().get_repo(name)),
                Function([Id()], Repo(), lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name))
            ])
        ],
        "id": [
            Shell([], [
                Function([String()], Id(), lambda login: get_git_connector().user(login).id),
                Function([Login()], Id(), lambda login: get_git_connector().user(login).id),
                Function([User()], Id(), lambda user: user.id),
                Function([Repo()], Id(), lambda repo: repo.id),
                Function([Gist()], Id(), lambda gist: gist.id),
                Function([Key()], Id(), lambda key: key.id)
            ]),
            Shell(["my"], [
                Function([], Id(), lambda: get_git_connector().user().id)
            ])
        ],
        "key": [
            Shell([], [
                Function([String()], Key(), lambda _str: _str)
            ])
        ]
    }
    return flat_map
