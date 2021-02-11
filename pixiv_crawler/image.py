# image class
# download image from url
#   like https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg
from settings import *
from utils import write_fail_log
import requests
import threading
import re
import time
import os


class Image(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)

        # url sample: https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg
        self.url = url
        self.name = self.url[self.url.rfind('/') + 1:len(self.url)]
        self.id = re.search("/(\d+)_", self.url).group(1)
        self.ref = 'https://www.pixiv.net/artworks/' + self.id
        self.headers = {'Referer': self.ref}
        self.headers.update(BROWSER_HEADER)
        # size of image (MB)
        self.size = 0

    # download image
    def run(self):
        if MOST_OUTPUT:
            print("---start downloading " + self.name + '---')
        time.sleep(2 / MAX_THREADS)

        if os.path.exists(IMAGES_STORE_PATH + self.name):
            if MOST_OUTPUT:
                print(self.name + ' already exists')
            return

        time.sleep(DOWNLOAD_DELAY)
        wait_time = 10
        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        timeout=(4, wait_time))
                if response.status_code == 200:
                    # avoid incomplete image
                    if len(response.content) != int(
                            response.headers['content-length']):
                        wait_time += 2
                        time.sleep(DOWNLOAD_DELAY)
                        continue
                    with open(IMAGES_STORE_PATH + self.name, "wb") as f:
                        f.write(response.content)
                    if MOST_OUTPUT:
                        print("---download " + self.name + " successfully---")
                    self.size = int(
                        response.headers['content-length']) / 1024 / 1024
                    return

            except Exception as e:
                if ALLOW_ERROR:
                    print(e)
                    print("check your proxy setting")
                    # print("maybe it was banned.")
                    print("This is " + str(i + 1) + " attempt to download " +
                          self.name)
                    print("next attempt will start in " + str(FAIL_DELAY) +
                          " sec\n")
                time.sleep(FAIL_DELAY)

        if ALLOW_ERROR:
            print("---fail to download " + self.name + '---')
        write_fail_log('fail to download ' + self.name + '\n')
