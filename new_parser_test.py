import NewParser

root = NewParser.parse("show a user of developerhacker")
# root = NewParser.parse("show a name, id and orgs url of this repo, this user's repo with the name gitbot and of repo gitbot of this user")
print(root)
print(NewParser.tree(root))
