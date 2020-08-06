# collect Image() from illust_id (using ImageGroup)
#   and send Image() to downloader
from settings import *
from image_group import ImageGroup
from downloader import Downloader


class Collector():
    def __init__(self, cookie, capacity):
        # group of illust_id
        self.group = set()
        self.cookie = cookie
        self.downloader = Downloader(capacity)

    def add(self, illust_id):
        self.group.add(ImageGroup(illust_id, self.cookie))

    # collect image from self.group
    #   and send to self.downloader
    def collect(self):
        pool = []
        print("---collector start---")

        while len(self.group) or len(pool):
            # send imagegroup to parallel pool
            while len(pool) < MAX_THREADS and len(self.group):
                pool.append(self.group.pop())
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                page = pool[i]
                if not page.isAlive():
                    self.downloader.add(page.group)
                    pool.remove(page)
                    continue
                i += 1

        print("---collector complete---")

    # self.downloader.download()
    def download(self):
        return self.downloader.download()

    # def run(self):
    #     self.collect()
    #     return self.download()
