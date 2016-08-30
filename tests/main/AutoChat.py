import os
import subprocess
import time
from src import IO


class AutoChat():
    DELAY = 5

    chat = [
        "show a id at developerhacker's repo with name GitBot",
        "developerhacker's repos",
        "repos of jgahkjgdskjgas",
        "login me",
        "developerhacker",
        "pword",
        "repos at developerhacker",
        "the avatar url",
        "store a user with the name aezakme",
        "a name for this user",
        "show the repos and gists of developerhacker and AndreiChugunov, and the avatar url at saloed, and name at this user and developerhacker",
        "remember me",
        "show a name at this user",
        "login me",
        "logout me",
        "login me",
        "adssadasd",
        "adssadasd",
        "show the name at developerhacker",
        "the name at Saloed",
        "disconnect"
    ]

    @staticmethod
    def run():
        directory = "/".join(os.path.realpath(__file__).split("/")[:-3]) + "/src/run.py"
        start = time.time()
        process = subprocess.Popen("python " + directory, shell=True, stdin=subprocess.PIPE)
        for mes in AutoChat.chat:
            time.sleep(AutoChat.DELAY)
            process.stdin.write(bytes(mes + "\n", "utf8"))
            process.stdin.flush()
            IO.writeln(mes)
        time.sleep(AutoChat.DELAY)
        end = time.time()
        IO.writeln(time.strftime("\nruntime: %Mm %Ss", time.gmtime(3 * 3600 + end - start)))
        process.kill()
