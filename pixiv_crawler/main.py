from settings import *
from login import Login
from requests.cookies import RequestsCookieJar


# load cookies from cookies.json
def load_cookie():
    ret = RequestsCookieJar()
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            ret.set(cookie['name'], cookie['value'])
    return ret


Login().fetch()
print(load_cookie())