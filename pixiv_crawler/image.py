# image class
from settings import *
import requests
import re
import time
from requests import exceptions
import os


class Image():
    def __init__(self, url):
        # url sample: https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg
        self.url = url
        self.name = self.url[self.url.rfind('/') + 1:len(self.url)]
        self.id = re.search("/(\d+)_", self.url).group(1)
        self.ref = 'https://www.pixiv.net/artworks/' + self.id
        self.headers = {'Referer': self.ref}
        self.headers.update(BROWSER_HEADER)

    # return size of image (MB)
    def download(self):
        if os.path.exists(IMAGES_STORE_PATH + self.name):
            print(self.name + 'already exists')
            return 0

        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        timeout=4)
                if response.status_code == 200:
                    with open(IMAGES_STORE_PATH + self.name, "wb") as f:
                        f.write(response.content)
                    print("download " + self.name + " successfully")
                    time.sleep(DOWNLOAD_DELAY)
                    return len(response.content) / 1024 / 1024

            except (exceptions.ConnectTimeout, exceptions.ProxyError,
                    exceptions.SSLError) as e:
                print(e)
                print("check your proxy setting")
                print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt")
                print("next attempt will start in 5 sec\n")
                time.sleep(5)

        print("fail to download " + self.name)
        return 0