# download artworks from ranking
from settings import *
from utils import ranking_selector, print_bar
import re
import datetime
import time
import requests
from collector import Collector
from collector_unit import CollectorUnit
from parallelpool import ParallelPool


class RankingCrawler():
    # flow capacity (MB)
    def __init__(self, cookie, capacity=1024):
        self.date = START_DATE
        self.domain = DOMAIN
        self.mode = PIXIV_MODES[PIXIV_MODE]
        # url sample: https://www.pixiv.net/ranking.php?mode=daily&date=20200801&p=1&format=json
        # ref url sample: https://www.pixiv.net/ranking.php?mode=daily&date=20200801
        self.url = 'https://www.pixiv.net/ranking.php?mode=' + self.mode
        self.cookie = cookie
        self.headers = {'x-requested-with': 'XMLHttpRequest'}
        self.collector = Collector(cookie, capacity)

    def __nextday(self):
        self.date += datetime.timedelta(days=1)

    # collect illust_id from daily json
    def collect(self):
        # note that 50 artworks per p=x
        page_num = (ARTWORKS_PER - 1) // 50 + 1  #ceil
        print("---start collecting " + self.mode + " ranking---")
        print("start with " + self.date.strftime("%Y-%m-%d"))
        print("end with " + (self.date + datetime.timedelta(
            days=self.domain - 1)).strftime("%Y-%m-%d" + '\n'))
        # store all jsons' url in self.group
        self.group = set()
        for _i in range(DOMAIN):
            for j in range(page_num):
                self.group.add(self.url + '&date=' +
                               self.date.strftime("%Y%m%d") + '&p=' +
                               str(j + 1) + '&format=json')
            self.__nextday()
        pool = ParallelPool(len(self.group))
        while len(self.group) or not pool.empty():
            time.sleep(THREAD_DELAY)
            # send ranking_json to parallel pool
            while not pool.full() and len(self.group):
                url = self.group.pop()
                ref = re.search('(.*)&p', url).group(1)
                headers = self.headers.update({'Referer': ref})
                pool.add(
                    CollectorUnit(url, self.cookie, ranking_selector, headers))
            # remove complete thread
            finished = pool.finished_item()
            while True:
                try:
                    ranking_json = next(finished)
                    self.collector.add(ranking_json.group)
                    if MOST_OUTPUT:
                        print("--send page " + ranking_json.url +
                              " to collector--")
                except StopIteration:
                    break

        print("\n---collect " + self.mode + " ranking complete---")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.collector.download()
