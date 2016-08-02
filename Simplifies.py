synonyms = {
    "print": "show",
    "view": "show",
    "authorise": "login",
    "disconnect": "close",
    "repository": "repo",
    "repositories": "repos",
    "storage": "repos"
}


def simplify_word(word: str) -> str:
    word = word.lower()
    if word in synonyms: word = synonyms[word]
    return word


def simplify_exp(exp: list) -> list:
    return [simplify_word(word) for word in exp]

