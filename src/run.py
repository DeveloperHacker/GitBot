from src.main.GitHandler import GitHandler
from src import IO

IO.DEBUG = True

handler = GitHandler(bot_nick="PythonBot")
handler.start()
