# store cookies
from settings import *
import requests
import json
import sys
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


# use selenium to fetch local cookies
# note that you must log in pixiv.net before run code
# besides, chrome is required
# and remember to close all chrome apps before run code
class Login():
    def __init__(self):
        self.cookie_url = "https://www.pixiv.net/setting_user.php"

    def fetch(self):
        print("it should take at most 30 sec to fetch cookies")
        print("----ignore output below----")
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument('--no-sandbox')
        options.add_argument("user-data-dir=" + USER_DATA_DIR)
        browser = webdriver.Chrome(options=options)
        # timeout=30s
        browser.set_page_load_timeout(30)
        try:
            browser.get(self.cookie_url)
            with open("cookies.json", "w") as f:
                f.write(json.dumps(browser.get_cookies(), indent=4))
            print("\n----ignore output above----")
            print("successfully store cookies in cookies.json")
            browser.close()
        except TimeoutException:
            print("\n----ignore output above----")
            print("time out when fetching cookies in login.py")
            browser.close()
            sys.exit(0)


# # deserted module
# # maybe v3_token is needed in form_data
# class Login():
#     def __init__(self):
#         self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
#         self.postkey_url = "https://accounts.pixiv.net/login"
#         self.session = requests.session()

#     def get_postkey(self):
#         headers = BROWSER_HEADER
#         try:
#             response = self.session.get(self.postkey_url,
#                                         headers=headers,
#                                         proxies=PROXIES,
#                                         timeout=4)
#             if response.status_code == 200:
#                 result = re.search('postkey":"(.*?)"', response.text, re.I)
#                 time.sleep(0.5)
#                 return result.group(1)
#         except requests.ConnectionError:
#             print("connect " + self.postkey_url + " failed check your proxy")
#         except requests.ConnectTimeout:
#             print("time out when getting post key")

#     def login(self):
#         post_key = self.get_postkey()
#         if post_key == None:
#             print("get post key failed")
#             sys.exit(0)
#         data = {
#             'pixiv_id': PIXIV_ID,
#             'password': PASSWORD,
#             'post_key': post_key,
#             'return_to': 'https://www.pixiv.net',
#         }
#         headers = {
#             "Referer":
#             "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
#         }
#         headers.update(BROWSER_HEADER)
#         response = self.session.post(self.login_url,
#                                      data=data,
#                                      headers=headers,
#                                      proxies=PROXIES,
#                                      timeout=4)
#         time.sleep(0.5)
