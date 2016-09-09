import os
import sys
import fcntl
from src.main import Utils
from getpass import getpass


def write(obj, form="{}"):
    sys.stdout.write(form.format(Utils.string(obj)))
    sys.stdout.flush()


def writeln(obj, form="{}"):
    sys.stdout.write(form.format(Utils.string(obj)) + '\n')
    sys.stdout.flush()


def readln(prompt: str) -> str:
    write(prompt)
    return sys.stdin.readline()[:-1]


def read(prompt: str) -> str:
    write(prompt)
    fcntl.fcntl(sys.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    data = sys.stdout.read()
    return data


def hreadln(prompt: str) -> str:
    return getpass(prompt)


def debug(obj, form="{}"):
    if os.getenv("DEBUG") == "true": writeln(obj, form)
