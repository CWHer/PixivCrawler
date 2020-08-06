# download artworks from ranking
from settings import *
import datetime
import time
import requests
from collector import Collector


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
        self.headers.update(BROWSER_HEADER)
        self.collector = Collector(cookie, capacity)

    def __nextday(self):
        self.date += datetime.timedelta(days=1)

    # collect p=K&format=json
    # K is "p=x"
    def __collect(self, K):
        ref = self.url + '&date=' + self.date.strftime("%Y%m%d")
        headers = self.headers
        headers.update({'Referer': ref})
        url = ref + '&' + K + '&format=json'
        print('---start collecting ' + self.date.strftime("%Y-%m-%d ") + K +
              '---')
        for i in range(FAIL_TIMES):
            try:
                response = requests.get(url,
                                        headers=headers,
                                        proxies=PROXIES,
                                        cookies=self.cookie,
                                        timeout=4)
                if response.status_code == 200:
                    for artwork in response.json()['contents']:
                        self.collector.add(str(artwork['illust_id']))
                        self.download_cnt += 1
                        print('--send ' + self.date.strftime("%Y-%m-%d") +
                              ' artwork:' + str(self.download_cnt) +
                              ' to collector--')
                        if self.download_cnt == ARTWORKS_PER: break
                    print('---collect ' + self.date.strftime("%Y-%m-%d ") + K +
                          ' complete---')
                    time.sleep(DOWNLOAD_DELAY)
                    return

            except Exception as e:
                print(e)
                print("check your proxy setting")
                # print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt to collect " +
                      self.date.strftime("%Y-%m-%d ") + K)
                print("next attempt will start in " + str(FAIL_DELAY) +
                      " sec\n")
                time.sleep(FAIL_DELAY)

        print('---faile to collect ' + self.date.strftime("%Y-%m-%d ") + K +
              '---')
        write_fail_log('faile to collect ' + self.date.strftime("%Y-%m-%d ") +
                       K + '\n')

    # collect daily images
    def collect(self):
        # note that 50 artworks per p
        num = (ARTWORKS_PER - 1) // 50 + 1  #ceil
        self.download_cnt = 0
        print("---start collecting " + self.date.strftime("%Y-%m-%d") + '---')
        for i in range(num):
            self.__collect('p=' + str(i + 1))
            if self.download_cnt == ARTWORKS_PER: break
        print("---collect " + self.date.strftime("%Y-%m-%d") + ' complete---')

    def run(self):
        print("---start collecting " + self.mode + " ranking---")
        print("start with " + self.date.strftime("%Y-%m-%d"))
        print("end with " + (self.date + datetime.timedelta(
            days=self.domain - 1)).strftime("%Y-%m-%d" + '\n'))
        for i in range(DOMAIN):
            self.collect()
            self.__nextday()
        print("---collect " + self.mode + " ranking complete---")

        self.collector.collect()
        return self.collector.download()
