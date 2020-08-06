# collect artworks from a classical page
#   e.g. https://www.pixiv.net/bookmark.php?rest=show&p=1
#   and collect all artworks/xxxxx
from settings import *
import time
import re
import threading
import requests


class Page(threading.Thread):
    # default ref:
    def __init__(self, url, cookie, ref=None):
        threading.Thread.__init__(self)

        self.url = url
        self.cookie = cookie
        self.headers = BROWSER_HEADER
        if ref != None:
            self.headers.update({"Referer": ref})

    def run(self):
        print("---start collecting page " + self.url + '---')

        time.sleep(DOWNLOAD_DELAY)
        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    self.group = set(
                        re.findall("artworks/(\d+)", response.text))
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

        print("---fail to collect page " + self.url + '---')
        write_fail_log('fail to collect page ' + self.url + '\n')