# download controller
# Image --> downloader (queue) --> download
#   multiple thread downloader
from settings import *
from image import Image
import time


class Downloader():
    def __init__(self, capacity):
        # group of Image()
        self.group = set()
        self.size = 0
        self.capacity = capacity

    # add Image() from ImageGroup
    # group in ImageGroup is list
    def add(self, group):
        self.group |= set(group)

    def download(self):
        # stop downloading once exceeding capacity
        flow_flag = 0
        pool = []
        print("---downloader start---")
        while (len(self.group) or len(pool)) and not flow_flag:
            time.sleep(DOWNLOAD_DELAY)
            # send image to parallel pool
            while len(pool) < MAX_THREADS and len(self.group):
                pool.append(self.group.pop())
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                image = pool[i]
                if not image.isAlive():
                    self.size += image.size
                    pool.remove(image)
                    continue
                i += 1
            if self.size >= self.capacity: flow_flag = 1
        # clear pool
        if len(pool) != 0:
            for image in pool:
                image.join()
                self.size += image.size
        print("---downloader complete---")
        return self.size
