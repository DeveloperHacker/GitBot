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


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in synonyms: word = synonyms[word]
    return word


def simplify_exp(exp: list) -> list:
    return [simplify_word(word) for word in exp]
