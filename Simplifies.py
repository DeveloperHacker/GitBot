synonyms = {
    "print": "show",
    "view": "show",
    "authorise": "login",
    "disconnect": "close",
    "repository": "repo",
    "repositories": "repos",
    "storage": "repos"
}


def simplify(word: str) -> str:
    word = word.lower()
    if word in synonyms: word = synonyms[word]
    return word