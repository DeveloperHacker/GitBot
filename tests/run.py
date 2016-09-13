import os

os.environ["INPUT"] = os.getcwd() + "/chats/complex.txt"

from src.main.Handler import Handler

handler = Handler(bot_nick="PythonBot")
handler.start()
