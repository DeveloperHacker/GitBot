import os
import sys
import fcntl
from getpass import getpass


def write(obj):
    sys.stdout.write(str(obj))
    sys.stdout.flush()


def writeln(obj):
    sys.stdout.write(str(obj) + "\n")
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
