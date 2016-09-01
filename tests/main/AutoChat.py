import os
import subprocess
import time
from src import IO


class AutoChat:
    DELAY = 10

    chat = [
        "show a id at developerhacker's repo with name GitBot",
        "developerhacker's repos",
        "repos of jgahkjgdskjgas",
        "log in",
        "developerhacker",
        "pword",
        "repos at developerhacker",
        "my avatar url",
        "store a user with the name aezakme",
        "the name for this user",
        "show my repos and my gists, the avatar url and orgs url of saloed, and this user's id",
        "store me",
        "a this user's name and login",
        "log in",
        "log out",
        "log in",
        "adssadasd",
        "adssadasd",
        "a developerhacker's repo 64680022",
        "the name at user Saloed",
        "a repo gitbot of developerhacker"
        "bye"
    ]

    @staticmethod
    def run():
        directory = "/".join(os.path.realpath(__file__).split("/")[:-3]) + "/src/run.py"
        start = time.time()
        process = subprocess.Popen("python " + directory, shell=True, stdin=subprocess.PIPE)
        first = True
        for mes in AutoChat.chat:
            if not first:
                time.sleep(AutoChat.DELAY)
            else:
                time.sleep(1)
            process.stdin.write(bytes(mes + "\n", "utf8"))
            process.stdin.flush()
            IO.writeln(mes)
            first = False
        end = time.time()
        IO.writeln(time.strftime("\nruntime: %Mm %Ss", time.gmtime(3 * 3600 + end - start)))
        process.kill()
