# collect Image() from illust_id (using ImageGroup)
#   and send Image() to downloader
from settings import *
from collector_unit import CollectorUnit
from downloader import Downloader
import time


class Collector():
    def __init__(self, cookie, capacity):
        # group of illust_id
        self.group = set()
        self.cookie = cookie
        self.downloader = Downloader(capacity)

    # add illust_id from page/json_selector
    def add(self, group):
        self.group |= group

    # collect image from self.group
    #   and send to self.downloader
    def collect(self):
        pool = []
        print("---collector start---")

        while len(self.group) or len(pool):
            time.sleep(0.05)
            # send json_collector to parallel pool
            while len(pool) < MAX_THREADS and len(self.group):
                illust_id = self.group.pop()
                ref = 'https://www.pixiv.net/artworks/' + illust_id
                url = 'https://www.pixiv.net/ajax/illust/' + illust_id + '/pages?lang=zh'
                headers = {'Referer': ref, "x-user-id": USER_ID}
                pool.append(
                    CollectorUnit(url, self.cookie, image_group_selector,
                                  headers))
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                image_group = pool[i]
                if not image_group.isAlive():
                    self.downloader.add(image_group.group)
                    pool.remove(image_group)
                    continue
                i += 1

        print("---collector complete---")

    # self.downloader.download()
    def download(self):
        return self.downloader.download()

    # def run(self):
    #     self.collect()
    #     return self.download()
