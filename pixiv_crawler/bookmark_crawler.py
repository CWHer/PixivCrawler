# download personal public bookmarks
from settings import *
import requests
import re
import sys
import time
from collector import Collector
from page import Page


class BookmarkCrawler():
    # count-badge sample:
    #   </h1><span class="count-badge">3069.</span>
    # artworks sample:
    #   href="/artworks/83348083
    # url sample:
    #   https://www.pixiv.net/bookmark.php?rest=show&p=1
    #   rest=show for public/ rest=hide for private
    #   note that 20 artworks per p
    # max number of downloads
    # flow capacity
    def __init__(self, cookie, maxnum=200, capacity=1024):
        self.num = maxnum
        self.cookie = cookie
        self.url = "https://www.pixiv.net/bookmark.php?rest=show"
        self.headers = BROWSER_HEADER
        self.collect_cnt = 0
        self.collector = Collector(cookie, capacity)

    # get count-badge
    def get_count(self):
        print("---start collecting bookmark count---")

        for i in range(FAIL_TIMES):
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    cnt = re.search('count-badge.*?(\d+)',
                                    response.text).group(1)
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
    def collect(self):
        # note that 20 artworks per page
        num = (self.num - 1) // 20 + 1
        pool = []
        print("---start collecting " + PIXIV_ID + "\'s bookmarks---")
        # store all pages' url in self.group
        self.group = set()
        for i in range(num):
            url = self.url + '&p=' + str(i + 1)
            self.group.add(Page(url, self.cookie))

        while len(self.group) or len(pool):
            time.sleep(0.05)
            # send page to parallel pool
            while len(pool) < MAX_THREADS and len(self.group):
                pool.append(self.group.pop())
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                page = pool[i]
                if not page.isAlive():
                    for illust_id in page.group:
                        self.collector.add(illust_id)
                    print("--send page " + page.url + " to collector--")
                    pool.remove(page)
                    continue
                i += 1

        print("---collecting bookmark complete---")

    def run(self):
        self.get_count()
        self.collect()
        self.collector.collect()
        return self.collector.download()
