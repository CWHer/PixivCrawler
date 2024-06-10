import datetime
import os
import threading
from functools import wraps

# >>> log utils
log_lock = threading.Lock()  # output mutex lock


def writeFailLog(text: str, file_name: str = "failures.log"):
    """
    Append the specified text to the failures.log file.

    Parameters:
        text (str): The text to be appended to the failures.log file.
        file_name (str): The name of the file to which the text will be appended.

    """
    with log_lock and open(file_name, "a+") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S : ") + text + "\n")


def printInfo(msg):
    print(f"\x1b[32;20m[INFO]:\x1b[0m {msg}")


def assertWarn(expr: bool, msg):
    try:
        assert expr, f"\x1b[33;20m[WARN]:\x1b[0m {msg}"
    except AssertionError as e:
        print(e)


def assertError(expr: bool, msg):
    assert expr, f"\x1b[31;20m[ERROR]:\x1b[0m {msg}"


def logTime(func):
    @wraps(func)
    def clockedFn(*args, **kwargs):
        import time

        start_time = time.time()
        ret = func(*args, **kwargs)
        printInfo(f"{func.__name__}() finishes after {time.time() - start_time:.2f} s")
        return ret

    return clockedFn


# <<< log utils


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        printInfo(f"Create {os.path.abspath(dir_path)}")
