import subprocess
import sys


def get_commit_hash():
    process = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)
    return process.stdout.decode("utf-8").strip("\n")


def dump_git_diff_to_file(fp):
    subprocess.run(f"git diff > {fp}", stdout=subprocess.PIPE, shell=True)


def get_command_line() -> str:
    return " ".join(sys.argv)
