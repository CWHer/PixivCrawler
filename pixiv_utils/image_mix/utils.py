import os
from functools import wraps

from colorama import Fore, Style


def printInfo(msg):
    print(f"{Fore.GREEN}[INFO]:{Style.RESET_ALL} {msg}")


def assertWarn(expr: bool, msg):
    try:
        assert expr, f"{Fore.YELLOW}[WARN]:{Style.RESET_ALL} {msg}"
    except AssertionError as e:
        print(e)


def assertError(expr: bool, msg):
    assert expr, f"{Fore.RED}[ERROR]:{Style.RESET_ALL} {msg}"


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        printInfo(f"Create {os.path.abspath(dir_path)}")


def logTime(func):
    @wraps(func)
    def clockedFn(*args, **kwargs):
        import time

        start_time = time.time()
        ret = func(*args, **kwargs)
        printInfo(f"{func.__name__}() finishes after {time.time() - start_time:.2f} s")
        return ret

    return clockedFn
