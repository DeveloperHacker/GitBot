import os
import sys
import fcntl
from src.main import Utils
from getpass import getpass

out = os.getenv("OUTPUT")
out_file = open(out, "a") if out is not None else None
inp = os.getenv("INPUT")
inp_file = open(inp, "r") if inp is not None else None


def log(file_name: str, form, *args):
    data = form.format(*[Utils.string(arg) for arg in list(args)]) if len(list(args)) > 0 else Utils.string(form)
    file = open(file_name, "a")
    file.write(data + "\n")
    file.flush()
    file.close()


def write(form, *args):
    data = form.format(*[Utils.string(arg) for arg in list(args)]) if len(list(args)) > 0 else Utils.string(form)
    if out_file is None:
        sys.stdout.write(data)
        sys.stdout.flush()
    else:
        out_file.write(data)
        out_file.flush()


def writeln(form, *args):
    data = form.format(*[Utils.string(arg) for arg in list(args)]) if len(list(args)) > 0 else Utils.string(form)
    if out_file is None:
        sys.stdout.write(data + '\n')
        sys.stdout.flush()
    else:
        out_file.write(data + '\n')
        out_file.flush()


def read(prompt: str) -> str:
    write(prompt)
    if inp_file is None:
        fcntl.fcntl(sys.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        data = sys.stdout.read()
    else:
        data = inp_file.read()
        write(data)
    return data


def line(input_stream) -> str:
    data = input_stream.readline()
    if len(data) > 0 and data[-1] == '\n':
        data = data[:-1]
    elif len(data) > 1 and data[-2:] == '\r\n':
        data = data[:-2]
    return data


def readln(prompt: str) -> str:
    write(prompt)
    if inp_file is None:
        data = line(sys.stdin)
    else:
        data = line(inp_file)
        writeln(data)
    return data


def hreadln(prompt: str) -> str:
    if inp_file is None:
        return getpass(prompt)
    else:
        return line(inp_file)


def debug(form, *args):
    if os.getenv("DEBUG") == "true": writeln(form, *args)
