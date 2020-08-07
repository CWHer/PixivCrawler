# download artworks from ranking
from settings import *
import datetime
import time
import requests
from collector import Collector
from collector_unit import CollectorUnit


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
        num = (ARTWORKS_PER - 1) // 50 + 1  #ceil
        pool = []
        print("---start collecting " + self.mode + " ranking---")
        print("start with " + self.date.strftime("%Y-%m-%d"))
        print("end with " + (self.date + datetime.timedelta(
            days=self.domain - 1)).strftime("%Y-%m-%d" + '\n'))
        # store all jsons' url in self.group
        self.group = set()
        for i in range(DOMAIN):
            for j in range(num):
                self.group.add(self.url + '&date=' +
                               self.date.strftime("%Y%m%d") + '&p=' +
                               str(j + 1) + '&format=json')
            self.__nextday()

        while len(self.group) or len(pool):
            time.sleep(0.05)
            # send ranking_json to parallel pool
            while len(pool) < MAX_THREADS and len(self.group):
                url = self.group.pop()
                ref = re.search('(.*)&p', url).group(1)
                headers = self.headers.update({'Referer': ref})
                pool.append(
                    CollectorUnit(url, self.cookie, ranking_selector, headers))
                pool[-1].start()
            # remove complete thread
            i = 0
            while i < len(pool):
                ranking_json = pool[i]
                if not ranking_json.isAlive():
                    self.collector.add(ranking_json.group)
                    print("--send page " + ranking_json.url +
                          " to collector--")
                    pool.remove(ranking_json)
                    continue
                i += 1

        print("---collect " + self.mode + " ranking complete---")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.collector.download()
