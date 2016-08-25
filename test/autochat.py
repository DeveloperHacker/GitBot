import os
import IO
import subprocess
import time

if __name__ == "__main__":

    DELAY = 5

    chat = [
        "show a id at developerhacker's repo with name GitBot",
        "developerhacker's repos",
        "repos of jgahkjgdskjgas",
        "count developerhacker's private gists ",
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

    directory = "/".join(os.getcwd().split("/")[:-1]) + "/src/__init__.py"
    IO.writeln(directory)

    start = time.time()
    process = subprocess.Popen("python " + directory, shell=True, stdin=subprocess.PIPE)
    for mes in chat:
        time.sleep(DELAY)
        process.stdin.write(bytes(mes + "\n", "utf8"))
        process.stdin.flush()
        IO.writeln(mes)
    time.sleep(DELAY)
    end = time.time()
    IO.writeln(time.strftime("\nruntime: %Mm %Ss", time.gmtime(3 * 3600 + end - start)))
    process.kill()
