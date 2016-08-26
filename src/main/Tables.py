synonyms = {
    "print": "show",
    "view": "show",
    "authorise": "login",
    "disconnect": "close",
    "repository": "repo",
    "project": "repo",
    "repositories": "repos",
    "projects": "repos",
    "storage": "repo",
    "recruited": "hireable",
    "organisations": "orgs",
    "remember": "store",
    "quit": "close"
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
    "str",
    "int"
}

primitive_types = {
    "str",
    "int"
}

types_synonyms = {
    "user": {"T": "login", "C": (lambda user: user.login)},
    "repo": {"T": "id", "C": (lambda repo: repo.id)},
    "gist": {"T": "id", "C": (lambda gist: gist.id)},
    "name": {"T": "str", "C": (lambda name: str(name))},
    "login": {"T": "str", "C": (lambda login: str(login))},
    "url": {"T": "str", "C": (lambda url: str(url))},
    "email": {"T": "str", "C": (lambda email: str(email))},
    "key": {"T": "str", "C": (lambda key: str(key))},
    "id": {"T": "int", "C": (lambda _id: int(_id))},
}


def create_object_builders_map(get_git_connector, get_stored) -> dict:
    flat_map = {
        "repos": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["list", "repo"], "O": user.get_repos()})}
            ]}
        ],
        "gists": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["list", "gist"], "O": user.get_gists()})}
            ]}
        ],
        "keys": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["list", "key"], "O": user.get_keys()})}
            ]}
        ],
        "name": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["name"], "O": user.name})},
                {"A": ["repo"], "B": (lambda repo: {"T": ["name"], "O": repo.name})},
                {"A": ["str"], "B": (lambda _str: {"T": ["name"], "O": _str})}
            ]},
        ],
        "login": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["login"], "O": user.login})},
                {"A": ["str"], "B": (lambda _str: {"T": ["login"], "O": _str})}
            ]}
        ],
        "url": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["url"], "O": user.url})}
            ]},
            {"JJ": ["orgs"], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["url"], "O": user.organizations_url})}
            ]},
            {"JJ": ["avatar"], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["url"], "O": user.avatar_url})}
            ]}
        ],
        "user": [
            {"JJ": [], "F": [
                {"A": ["str"], "B": (lambda login: {"T": ["user"], "O": get_git_connector().user(login)})},
                {"A": ["login"], "B": (lambda login: {"T": ["user"], "O": get_git_connector().user(login)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda: {"T": ["user"], "O": get_stored("user")})}
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                {"A": ["user", "str"], "B": (lambda user, name: {"T": ["repo"], "O": user.get_repo(name)})},
                {"A": ["user", "name"], "B": (lambda user, name: {"T": ["repo"], "O": user.get_repo(name)})},
                {"A": ["int"], "B": (lambda _id: {"T": ["repo"], "O": get_git_connector().repo(_id)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda: {"T": ["repo"], "O": get_stored("repo")})}
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                {"A": ["int"], "B": (lambda _id: {"T": ["gist"], "O": get_git_connector().gist(_id)})},
                {"A": ["id"], "B": (lambda _id: {"T": ["gist"], "O": get_git_connector().gist(_id)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda stored: {"T": ["gist"], "O": stored["gist"]})}
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                {"A": ["repo"], "B": (lambda repo: {"T": ["id"], "O": repo.id})},
                {"A": ["gist"], "B": (lambda gist: {"T": ["id"], "O": gist.id})},
                {"A": ["int"], "B": (lambda _int: {"T": ["id"], "O": _int})}
            ]},
        ],
        "key": [
            {"JJ": [], "F": [
                {"A": ["str"], "B": (lambda _str: {"T": ["key"], "O": _str})}
            ]}
        ]
    }
    return flat_map
