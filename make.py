#!/usr/bin/env python3
import os
import sys
import select
import pty
from subprocess import Popen
from time import time, sleep
import typer


options = {
    "DEVICE_PATH": "/dev/ttyUSB0",
    "BUFFER_SIZE": 512,
    "VERBOSE": False,
    "MICROPYTHON": "./micropython/esp32-idf4-20210202-v1.14.bin"
}


class Base:
    # Foreground:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    NC = '\x1b[0m'  # No Color


def run_bash_cmd(cmd, echo=False, interaction={}, return_lines=True, return_code=False, cr_as_newline=False):
    if options["VERBOSE"]:
        echo = True
    if echo:
        print("CMD:", cmd)
    master_fd, slave_fd = pty.openpty()
    line = ""
    lines = []
    with Popen(cmd, shell=True, preexec_fn=os.setsid, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, universal_newlines=True) as p:
        while p.poll() is None:
            r, w, e = select.select([sys.stdin, master_fd], [], [], 0.01)
            if master_fd in r:
                o = os.read(master_fd, 10240).decode("UTF-8")
                if o:
                    for c in o:
                        if cr_as_newline and c == "\r":
                            c = "\n"
                        if c == "\n":
                            if line and line not in interaction.values():
                                clean = line.strip().split('\r')[-1]
                                lines.append(clean)
                                if echo:
                                    print("STD:", line)
                            line = ""
                        else:
                            line += c
            if line:  # pass password to prompt
                for key in interaction:
                    if key in line:
                        if echo:
                            print("PMT:", line)
                        sleep(1)
                        os.write(master_fd, ("%s" % (interaction[key])).encode())
                        os.write(master_fd, "\r\n".encode())
                        line = ""
        if line:
            clean = line.strip().split('\r')[-1]
            lines.append(clean)

    os.close(master_fd)
    os.close(slave_fd)

    if return_lines and return_code:
        return lines, p.returncode
    elif return_code:
        return p.returncode
    else:
        return lines


def get_base_command():
    return "rshell -p %s --buffer-size %d" % (options["DEVICE_PATH"], options["BUFFER_SIZE"])


app = typer.Typer(help="Awesome CLI micropython.")


@app.command()
def repl():
    cmd = "%s repl" % (get_base_command())
    os.system(cmd)


@app.command()
def shell():
    cmd = "%s" % (get_base_command())
    os.system(cmd)


@app.command()
def flash():
    cmd = "%s rsync ./src /pyboard/" % (get_base_command())
    lines = run_bash_cmd(cmd)
    for line in lines:
        if "timed out or error" in line:
            print("%sERROR:%s while flashing" % (Base.FAIL, Base.END))


@app.command()
def flash_micropython():
    cmd = "esptool.py --chip esp32 --port %s write_flash -z 0x1000 %s" % (options["DEVICE_PATH"], options["MICROPYTHON"])
    lines = run_bash_cmd(cmd)
    result = any("Hash of data verified." in line for line in lines)
    if not result:
        print("%sERROR:%s while flashing" % (Base.FAIL, Base.END))
    return result


@app.command()
def erase():
    cmd = "esptool.py --port %s erase_flash" % (options["DEVICE_PATH"])
    lines = run_bash_cmd(cmd)
    result = any("Chip erase completed successfully" in line for line in lines)
    if not result:
        print("%sERROR:%s while erase" % (Base.FAIL, Base.END))
    return result


@app.callback()
def main(verbose: bool = True, device_path: str = ""):
    global options
    if verbose:
        options["VERBOSE"] = verbose
    if device_path:
        options["DEVICE_PATH"] = device_path


if __name__ == "__main__":
    app()
