# image class
# download image from url
#   like https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg
from settings import *
import requests
import threading
import re
import time
import os


class Image(threading.Thread):
    def __init__(self, url):
        # url sample: https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg
        threading.Thread.__init__(self)
        self.url = url
        self.name = self.url[self.url.rfind('/') + 1:len(self.url)]
        self.id = re.search("/(\d+)_", self.url).group(1)
        self.ref = 'https://www.pixiv.net/artworks/' + self.id
        self.headers = {'Referer': self.ref}
        self.headers.update(BROWSER_HEADER)
        self.size = 0

    # download image
    # return size of image (MB)
    def run(self):
        print("---start download " + self.name + '---')
        time.sleep(1)

        if os.path.exists(IMAGES_STORE_PATH + self.name):
            print(self.name + ' already exists')
            time.sleep(DOWNLOAD_DELAY)
            return

        time.sleep(DOWNLOAD_DELAY)
        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        timeout=6)
                if response.status_code == 200:
                    with open(IMAGES_STORE_PATH + self.name, "wb") as f:
                        f.write(response.content)
                    print("---download " + self.name + " successfully---")
                    time.sleep(DOWNLOAD_DELAY)
                    self.size = len(response.content) / 1024 / 1024
                    return

            except Exception as e:
                print(e)
                print("check your proxy setting")
                print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt to download " +
                      self.name)
                print("next attempt will start in " + str(FAIL_DELAY) +
                      " sec\n")
                time.sleep(FAIL_DELAY)

        print("---fail to download " + self.name + '---')
