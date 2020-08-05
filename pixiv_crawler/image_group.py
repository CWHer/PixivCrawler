# image group
# collect several images in a web
#   like https://www.pixiv.net/artworks/83398062
from settings import *
from image import Image
import requests
from requests import exceptions
import time
import re


class ImageGroup():
    def __init__(self, url, cookie):
        # url sample: https://www.pixiv.net/artworks/83398062
        self.ref = url
        self.id = re.search("/(\d+)$", url).group(1)
        self.url = 'https://www.pixiv.net/ajax/illust/' + self.id + '/pages?lang=zh'
        self.cookie = cookie
        self.headers = {'Referer': self.ref, "x-user-id": USER_ID}
        # I don't know whether 'x-user-id' is crucial
        # but to make headers more realistic I choose to keep it
        self.headers.update(BROWSER_HEADER)
        self.group = []

    # request 'page' to collect all images' url
    # return a dict of url
    def collect(self):
        print("start collect " + self.ref)

        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    for url in response.json()['body']:
                        self.group.append(Image(url['urls']['original']))
                    print("collect " + self.ref + " complete")
                    time.sleep(DOWNLOAD_DELAY)
                    return

            except (exceptions.ConnectTimeout, exceptions.ProxyError,
                    exceptions.SSLError) as e:
                print(e)
                print("check your proxy setting")
                print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt")
                print("next attempt will start in 5 sec\n")
                time.sleep(5)

        print("fail to collect " + self.ref)

    # download images in self.group
    # return size of image (MB)
    def download(self):
        ret = 0
        for image in self.group:
            image.start()
        for image in self.group:
            image.join()
            ret += image.size
        return ret