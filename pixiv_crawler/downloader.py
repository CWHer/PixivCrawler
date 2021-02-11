# download controller
# Image --> downloader (queue) --> download
#   multiple thread downloader
from settings import *
from utils import print_bar
from image import Image
from parallelpool import ParallelPool
import time


class Downloader():
    def __init__(self, capacity):
        # group of url
        self.group = set()
        self.capacity = capacity

    # add url from image_group_selector
    def add(self, group):
        self.group |= group

    def download(self):
        # stop downloading once exceeding capacity
        flow_flag = 0
        pool = ParallelPool(len(self.group), 0)
        print("---downloader start---")
        while (len(self.group) or not pool.empty()) and not flow_flag:
            time.sleep(THREAD_DELAY)
            # send image to parallel pool
            while not pool.full() and len(self.group):
                pool.add(Image(self.group.pop()))
            # remove complete thread
            finished = pool.finished_item()
            while True:
                try:
                    image = next(finished)
                    pool.flow += image.size
                except StopIteration:
                    break
            flow_flag = pool.flow >= self.capacity

        # clear pool
        if not pool.empty():
            pool.wait()
            finished = pool.finished_item()
            while True:
                try:
                    image = next(finished)
                    pool.flow += image.size
                except StopIteration:
                    break
        print("\n---downloader complete---")
        return pool.flow
