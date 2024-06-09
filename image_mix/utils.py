import os
from functools import wraps


def printInfo(msg):
    print("[INFO]: {}".format(msg))


def assertWarn(expr: bool, msg):
    try:
        assert expr, f"[WARN]: {msg}"
    except AssertionError as e:
        print(e)


def assertError(expr: bool, msg):
    assert expr, f"[ERROR]: {msg}"


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        printInfo(f"Create {dir_path}")


def logTime(func):
    @wraps(func)
    def clockedFn(*args, **kwargs):
        import time

        start_time = time.time()
        ret = func(*args, **kwargs)
        printInfo(f"{func.__name__}() finishes after {time.time() - start_time:.2f} s")
        return ret

    return clockedFn
