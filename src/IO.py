import os
import sys
import fcntl
from src.main import Utils
from getpass import getpass

out = os.getenv("OUTPUT")
out_file = open(out, "a") if out is not None else None
inp = os.getenv("INPUT")
inp_file = open(inp, "r") if inp is not None else None


def write(obj, form="{}"):
    if out_file is None:
        sys.stdout.write(form.format(Utils.string(obj)))
        sys.stdout.flush()
    else:
        out_file.write(form.format(Utils.string(obj)))
        out_file.flush()


def writeln(obj, form="{}"):
    if out_file is None:
        sys.stdout.write(form.format(Utils.string(obj)) + '\n')
        sys.stdout.flush()
    else:
        out_file.write(form.format(Utils.string(obj)) + '\n')
        out_file.flush()


def read(prompt: str) -> str:
    if inp_file is None:
        write(prompt)
        fcntl.fcntl(sys.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        data = sys.stdout.read()
        return data
    else:
        data = inp_file.read()
        write(prompt + data)
        return data


def readln(prompt: str) -> str:
    if inp_file is None:
        write(prompt)
        return sys.stdin.readline()[:-1]
    else:
        data = inp_file.readline()
        write(prompt + data)
        return data


def hreadln(prompt: str) -> str:
    if inp_file is None:
        return getpass(prompt)
    else:
        return inp_file.readline()


def debug(obj, form="{}"):
    if os.getenv("DEBUG") == "true": writeln(obj, form)
