
if __name__ == "__main__":
    # from src.GitHandler import GitHandler
    from src.NewGitHandler import GitHandler
    handler = GitHandler(bot_nick="PythonBot")
    handler.start()
