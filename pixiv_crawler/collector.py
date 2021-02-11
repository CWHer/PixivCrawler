# collect Image() from illust_id (using ImageGroup)
#   and send Image() to downloader
from settings import *
from utils import image_group_selector, tags_selector, print_bar
from collector_unit import CollectorUnit
from downloader import Downloader
from parallelpool import ParallelPool
import re
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

    # optional function
    # collect images' tags
    #   and dump into tags.json
    def collect_tags(self):
        self.tags = dict()
        # a copy of self.group
        group = self.group.copy()
        pool = ParallelPool(len(group))
        print('---tags collector start---')
        while len(group) or not pool.empty():
            time.sleep(THREAD_DELAY)
            # send tags_collector to parallel pool
            while not pool.full() and len(group):
                illust_id = group.pop()
                ref = 'https://www.pixiv.net/bookmark.php?type=user'
                url = 'https://www.pixiv.net/artworks/' + illust_id
                headers = {'Referer': ref}
                pool.add(
                    CollectorUnit(url, self.cookie, tags_selector, headers))
            # remove complete thread
            finished = pool.finished_item()
            while True:
                try:
                    tag_group = next(finished)
                    illust_id = re.search('artworks/(\d+)',
                                          tag_group.url).group(1)
                    self.tags[illust_id] = tag_group.group
                except StopIteration:
                    break

        with open(IMAGES_STORE_PATH + 'tags.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.tags, indent=4, ensure_ascii=False))
        print('\n---tags collector complete---')

    # collect image from self.group
    #   and send to self.downloader
    def collect(self):
        if WITH_TAG:
            self.collect_tags()

        pool = ParallelPool(len(self.group))
        print("---collector start---")
        while len(self.group) or not pool.empty():
            time.sleep(THREAD_DELAY)
            # send json_collector to parallel pool
            while not pool.full() and len(self.group):
                illust_id = self.group.pop()
                ref = 'https://www.pixiv.net/artworks/' + illust_id
                url = 'https://www.pixiv.net/ajax/illust/' + illust_id + '/pages?lang=zh'
                headers = {'Referer': ref, "x-user-id": USER_ID}
                pool.add(
                    CollectorUnit(url, self.cookie, image_group_selector,
                                  headers))
            # remove complete thread
            finished = pool.finished_item()
            while True:
                try:
                    image_group = next(finished)
                    self.downloader.add(image_group.group)
                except StopIteration:
                    break

        print("\n---collector complete---")
        print("artworks: " + str(len(self.downloader.group)))

    # self.downloader.download()
    def download(self):
        return self.downloader.download()

    # def run(self):
    #     self.collect()
    #     return self.download()
