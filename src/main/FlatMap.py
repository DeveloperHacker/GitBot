def create(self) -> dict:
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
                {"A": ["repo"], "B": (lambda repo: {"T": ["name"], "O": repo.name})}
            ]},
        ],
        "login": [
            {"JJ": [], "F": [
                {"A": ["user"], "B": (lambda user: {"T": ["login"], "O": user.login})}
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
                {"A": ["str"], "B": (lambda login: {"T": ["user"], "O": self.connector.user(login)})},
                {"A": ["login"], "B": (lambda login: {"T": ["user"], "O": self.connector.user(login)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda: {"T": ["user"], "O": self.stored["user"]})}
            ]}
        ],
        "repo": [
            {"JJ": [], "F": [
                {"A": ["user", "str"], "B": (lambda user, name: {"T": ["url"], "O": user.get_repo(name)})},
                {"A": ["user", "name"], "B": (lambda user, name: {"T": ["url"], "O": user.get_repo(name)})},
                {"A": ["int"], "B": (lambda _id: {"T": ["repo"], "O": self.connector.repo(_id)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda: {"T": ["repo"], "O": self.stored["repo"]})}
            ]}
        ],
        "gist": [
            {"JJ": [], "F": [
                {"A": ["int"], "B": (lambda _id: {"T": ["gist"], "O": self.connector.gist(_id)})},
                {"A": ["id"], "B": (lambda _id: {"T": ["gist"], "O": self.connector.gist(_id)})}
            ]},
            {"JJ": ["this"], "F": [
                {"A": [], "B": (lambda stored: {"T": ["gist"], "O": stored["gist"]})}
            ]}
        ],
        "id": [
            {"JJ": [], "F": [
                {"A": ["repo"], "B": (lambda repo: {"T": ["id"], "O": repo.id})},
                {"A": ["gist"], "B": (lambda gist: {"T": ["id"], "O": gist.id})}
            ]},
        ]
    }
    return flat_map
