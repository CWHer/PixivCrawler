# collect illust id from json/page
#   e.g.: user.json/page.json/rank.json
#   use different selector to function accordingly
from settings import *
import time
import threading
import requests


class CollectorUnit(threading.Thread):
    # note that selector is a function
    def __init__(self, url, cookie, selector, headers=None):
        threading.Thread.__init__(self)

        self.url = url
        self.cookie = cookie
        self.selector = selector
        self.headers = BROWSER_HEADER
        if headers != None:
            self.headers.update(headers)
        self.group = set()

    def run(self):
        print('---start collecting ' + self.url + '---')

        time.sleep(DOWNLOAD_DELAY)
        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    self.group = self.selector(response)
                    print('---collect ' + self.url + " complete---")
                    return

            except Exception as e:
                print(e)
                print("check your proxy setting")
                # print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt to collect " +
                      self.url)
                print("next attempt will start in " + str(FAIL_DELAY) +
                      " sec\n")
                time.sleep(FAIL_DELAY)

        print('---fail to collect ' + self.url + '---')
        write_fail_log('fail to collect ' + self.url + '\n')
