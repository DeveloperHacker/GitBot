
from GitHandler import GitHandler

handler = GitHandler(bot_nick="PythonBot")
handler.start()

# import inspect
# import NewParser
# import Parser
# from github import Github

# print(Parser.parse_string("Show the repositories at DeveloperHacker"))
# print(Parser.parse_string("Show the storage at DeveloperHacker"))
# print(Parser.parse_string("Authorise me in GitHub"))
# print(Parser.parse_string("Show the url at DeveloperHacker"))
# print(Parser.parse_string("Unlogin me in GitHub and Amigo"))
# print(Parser.parse_string("Show the storage at Saloed"))
# print(Parser.parse_string("the storage at Saloed"))
# print(Parser.parse_string("show a user with a login of DeveloperHacker."))
# print(Parser.parse_string("show his repos."))
# print(Parser.parse_string("show my repos."))

# def format_fun(name, attr):
#     spec = inspect.getfullargspec(attr)
#     args = spec.args
#     defaults = spec.defaults
#     args_len = len(args) if args is not None else 0
#     defs_len = len(defaults) if defaults is not None else 0
#     result = []
#     for i in range(1, args_len + 1):
#         if i <= defs_len:
#             result.append("{}={}".format(args[-i], defaults[-i]))
#         else:
#             result.append(args[-i])
#     result = [item for item in reversed(result)]
#     return "%30s     %s" % (name, str(result))
#
# git = Github()
# user = git.get_user("DeveloperHacker")
# repo = user.get_repo("GitBot")
# print("\n".join([format_fun(m[0], m[1]) for m in inspect.getmembers(repo, predicate=inspect.ismethod) if m[0][0] != "_"]))
# print([m for m in inspect.getmembers(repo, predicate=lambda attr: not inspect.ismethod(attr)) if m[0][0] != "_"])
# print([user.name for user in repo.get_assignees()])

# print(Parser.parse_string("show repos at this user"))
# print(Parser.parse_string("show repo with name of GitBot"))
# print(Parser.parse_string("show user with login of DeveloperHacker"))
# print(NewParser.parse("show repo in this repos with name of GitBot"))
# print(NewParser.parse("repo in this repos with name of GitBot"))
# print(Parser.parse_string(""))
