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

    # optional function
    # collect images' tags
    #   and dump into tags.json
    def collect_tags(self):
        self.tags = dict()
        # a copy of self.group
        group = self.group.copy()
        pool = []
        print('---tags collector start---')

        while len(group) or len(pool):
            time.sleep(0.05)
            # send tags_collector to parallel pool
            while len(pool) < MAX_THREADS and len(group):
                illust_id = group.pop()
                ref = 'https://www.pixiv.net/bookmark.php?type=user'
                url = 'https://www.pixiv.net/artworks/' + illust_id
                headers = {'Referer': ref}
                pool.append(
                    CollectorUnit(url, self.cookie, tags_selector, headers))
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                tag_group = pool[i]
                if not tag_group.isAlive():
                    illust_id = re.search('artworks/(\d+)',
                                          tag_group.url).group(1)
                    self.tags[illust_id] = tag_group.group
                    pool.remove(tag_group)
                    continue
                i += 1

        with open(IMAGES_STORE_PATH + 'tags.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.tags, indent=4, ensure_ascii=False))
        print('---tags collector complete---')

    # collect image from self.group
    #   and send to self.downloader
    def collect(self):
        self.collect_tags()

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
