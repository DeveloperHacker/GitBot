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
    "username": "login"
}

types = {
    "user",
    "repo",
    "gist",
    "name",
    "login",
    "key",
    "id",
    "url",
    "email",

    "none",
    "list",
    "str",
    "int"
}

type_synonyms = {
    "repos": ["list", "repo"],
    "gists": ["list", "gist"],
    "keys": ["list", "key"]
}

primitive_types = {
    "none",
    "list",
    "str",
    "int"
}


NONE = {"T": ["none"], "O": None}

similar_types = {
    "user": {"T": ["login"], "C": lambda user: user.login},
    "repo": {"T": ["id"], "C": lambda repo: repo.id},
    "gist": {"T": ["id"], "C": lambda gist: gist.id},
    "name": {"T": ["str"], "C": lambda name: str(name)},
    "login": {"T": ["str"], "C": lambda login: str(login)},
    "url": {"T": ["str"], "C": lambda url: str(url)},
    "email": {"T": ["str"], "C": lambda email: str(email)},
    "key": {"T": ["str"], "C": lambda key: str(key)},
    "id": {"T": ["int"], "C": lambda _id: int(_id)}
}


def create_storeds_map() -> dict:
    flat_map = {
        "user": None,
        "repo": None,
        "gist": None
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
                {"A": [["user"]],
                 "T": type_synonyms["repos"],
                 "B": lambda user: user.get_repos()},
                {"A": [["str"]],
                 "T": type_synonyms["repos"],
                 "B": lambda login: get_git_connector().user(login).get_repos()},
                {"A": [["login"]],
                 "T": type_synonyms["repos"],
                 "B": lambda login: get_git_connector().user(login).get_repos()}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": type_synonyms["repos"],
                 "B": lambda: get_git_connector().user().get_repos()}
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                {"A": [["user"]],
                 "T": type_synonyms["gists"],
                 "B": lambda user: user.get_gists()},
                {"A": [["str"]],
                 "T": type_synonyms["gists"],
                 "B": lambda login: get_git_connector().user(login).get_gists()},
                {"A": [["login"]],
                 "T": type_synonyms["gists"],
                 "B": lambda login: get_git_connector().user(login).get_gists()}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": type_synonyms["gists"],
                 "B": lambda: get_git_connector().user().get_gists()}
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                {"A": [["user"]],
                 "T": type_synonyms["keys"],
                 "B": lambda user: user.get_keys()},
                {"A": [["str"]],
                 "T": type_synonyms["keys"],
                 "B": lambda login: get_git_connector().user(login).get_keys()},
                {"A": [["login"]],
                 "T": type_synonyms["keys"],
                 "B": lambda login: get_git_connector().user(login).get_keys()}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": type_synonyms["keys"],
                 "B": lambda: get_git_connector().user().get_keys()}
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                {"A": [["user"]],
                 "T": ["name"],
                 "B": lambda user: user.name},
                {"A": [["repo"]],
                 "T": ["name"],
                 "B": lambda repo: repo.name},
                {"A": [["str"]],
                 "T": ["name"],
                 "B": lambda _str: _str}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": ["name"],
                 "B": lambda: get_git_connector().user().name}
            ]}
        ],
        "email": [
            {"JJ": [], "F": [
                {"A": [["user"]],
                 "T": ["email"],
                 "B": lambda user: user.email},
                {"A": [["str"]],
                 "T": ["email"],
                 "B": lambda _str: _str}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": ["email"],
                 "B": lambda: get_git_connector().user().email}
            ]}
        ],
        "login": [
            {"JJ": [], "F": [
                {"A": [["user"]],
                 "T": ["login"],
                 "B": lambda user: user.login},
                {"A": [["str"]],
                 "T": ["login"],
                 "B": lambda _str: _str}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": ["login"],
                 "B": lambda: get_git_connector().user().login}
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                {"A": [["str"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).url},
                {"A": [["login"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).url},
                {"A": [["user"]],
                 "T": ["url"],
                 "B": lambda user: user.url}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": ["url"],
                 "B": lambda: get_git_connector().user().url}
            ]},
            {"JJ": ["orgs"], "F": [
                {"A": [["str"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [["login"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).organizations_url},
                {"A": [["user"]],
                 "T": ["url"],
                 "B": lambda user: user.organizations_url}
            ]},
            {"JJ": ["my", "orgs"], "F": [
                {"A": [],
                 "T": ["url"],
                 "B": lambda: get_git_connector().user().organizations_url}
            ]},
            {"JJ": ["avatar"], "F": [
                {"A": [["str"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [["login"]],
                 "T": ["url"],
                 "B": lambda login: get_git_connector().user(login).avatar_url},
                {"A": [["user"]],
                 "T": ["url"],
                 "B": lambda user: user.avatar_url}
            ]},
            {"JJ": ["my", "avatar"], "F": [
                {"A": [],
                 "T": ["url"],
                 "B": lambda: get_git_connector().user().avatar_url}
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                {"A": [["str"]],
                 "T": ["user"],
                 "B": lambda login: get_git_connector().user(login)},
                {"A": [["login"]],
                 "T": ["user"],
                 "B": lambda login: get_git_connector().user(login)}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": ["user"],
                 "B": lambda: get_stored("user")}
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                {"A": [["str"], ["str"]],
                 "T": ["repo"],
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [["str"], ["name"]],
                 "T": ["repo"],
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [["login"], ["str"]],
                 "T": ["repo"],
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [["login"], ["name"]],
                 "T": ["repo"],
                 "B": lambda login, name: get_git_connector().user(login).get_repo(name)},
                {"A": [["user"], ["str"]],
                 "T": ["repo"],
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [["user"], ["name"]],
                 "T": ["repo"],
                 "B": lambda user, name: user.get_repo(name)},
                {"A": [["int"]],
                 "T": ["repo"],
                 "B": lambda _id: get_git_connector().repo(_id)},
                {"A": [["id"]],
                 "T": ["repo"],
                 "B": lambda _id: get_git_connector().repo(_id)}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": ["repo"],
                 "B": lambda: get_stored("repo")}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [["str"]],
                 "T": ["repo"],
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [["name"]],
                 "T": ["repo"],
                 "B": lambda name: get_git_connector().user().get_repo(name)},
                {"A": [["id"]],
                 "T": ["repo"],
                 "B": lambda _id: get_git_connector().user().get_repo(get_git_connector().repo(_id).name)}
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                {"A": [["int"]],
                 "T": ["gist"],
                 "B": lambda _id: get_git_connector().gist(_id)},
                {"A": [["id"]],
                 "T": ["gist"],
                 "B": lambda _id: get_git_connector().gist(_id)}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [],
                 "T": ["gist"],
                 "B": lambda stored: stored["gist"]}
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                {"A": [["str"]],
                 "T": ["id"],
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [["login"]],
                 "T": ["id"],
                 "B": lambda login: get_git_connector().user(login).id},
                {"A": [["user"]],
                 "T": ["id"],
                 "B": lambda user: user.id},
                {"A": [["repo"]],
                 "T": ["id"],
                 "B": lambda repo: repo.id},
                {"A": [["gist"]],
                 "T": ["id"],
                 "B": lambda gist: gist.id},
                {"A": [["int"]],
                 "T": ["id"],
                 "B": lambda _int: _int}
            ]},
            {"JJ": ["my"], "F": [
                {"A": [],
                 "T": ["id"],
                 "B": lambda: get_git_connector().user().id}
            ]}
        ],
        "key": [
            {"JJ": [], "F": [
                {"A": [["str"]],
                 "T": ["key"],
                 "B": lambda _str: _str}
            ]}
        ]
    }
    return flat_map
