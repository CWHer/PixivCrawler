# download personal public bookmarks
from settings import *
from utils import page_selector, print_bar
import requests
import re
import sys
import time
from parallelpool import ParallelPool
from collector import Collector
from collector_unit import CollectorUnit


class BookmarkCrawler():
    # count-badge sample:
    #   </h1><span class="count-badge">3069.</span>
    # artworks sample:
    #   href="/artworks/83348083

    # (out-dated) see def get_count & def collect for more
    # url sample:
    #   https://www.pixiv.net/bookmark.php?rest=show&p=1
    #   rest=show for public/ rest=hide for private
    #   note that 20 artworks per p

    # max number of downloads
    # flow capacity
    def __init__(self, cookie, maxnum=200, capacity=1024):
        self.num = maxnum
        self.cookie = cookie
        self.url = "https://www.pixiv.net/ajax/user/" + USER_ID + "/illusts"
        self.headers = BROWSER_HEADER
        self.collect_cnt = 0
        self.collector = Collector(cookie, capacity)

    # get count-badge
    # https://www.pixiv.net/ajax/user/xxxx/illusts/bookmark/tags?lang=zh
    def get_count(self):
        count_url = self.url + "/bookmark/tags?lang=zh"
        print("---start collecting bookmark count---")

        for i in range(FAIL_TIMES):
            try:
                response = requests.get(count_url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    # cnt = re.search('count-badge.*?(\d+)',
                    #                 response.text).group(1)
                    cnt = response.json()['body']['public'][0]['cnt']
                    self.num = min(self.num, int(cnt))
                    print("total count: " + cnt)
                    print("download count: " + str(self.num))
                    print("---collect bookmark count complete---")
                    return

            except Exception as e:
                print(e)
                print("check your proxy setting")
                # print("maybe it was banned.")
                print("This is " + str(i + 1) +
                      " attempt to collect bookmark count")
                print("next attempt will start in " + str(FAIL_DELAY) +
                      " sec\n")
                time.sleep(FAIL_DELAY)

        print("---fail to collect bookmark count---")
        sys.exit(0)

    # collect bookmark
    # https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh
    # [offset+1,offset+limit]
    # note that disable artwork'id is num not str...
    def collect(self):
        # default is 48, I just keep it.
        limit = 48
        page_num = (self.num - 1) // limit + 1
        pool = ParallelPool(page_num)
        print("---start collecting " + PIXIV_ID + "\'s bookmarks---")
        # store all pages' url in self.group
        self.group = set()
        for i in range(page_num):
            url = self.url + "/bookmarks?tag="
            url = url + "&offset=" + str(i * limit) + "&limit=" + str(limit)
            url = url + "&rest=show&lang=zh"
            self.group.add(url)

        while len(self.group) or not pool.empty():
            time.sleep(THREAD_DELAY)
            # send page to parallel pool
            while not pool.full() and len(self.group):
                pool.add(
                    CollectorUnit(self.group.pop(), self.cookie,
                                  page_selector))
            # remove complete thread
            finished = pool.finished_item()
            while True:
                try:
                    page = next(finished)
                    self.collector.add(page.group)
                    if MOST_OUTPUT:
                        print("--send page " + page.url + " to collector--")
                except StopIteration:
                    break

        print("\n---collecting bookmark complete---")
        print("downloadable artworks: " + str(len(self.collector.group)))

    def run(self):
        self.get_count()
        self.collect()
        self.collector.collect()
        return self.collector.download()
