from settings import *
import datetime
import time
from image_group import ImageGroup
import requests


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
        # size of image (MB)
        self.capacity = capacity
        self.size = 0

    def __nextday(self):
        self.date += datetime.timedelta(days=1)

    # download images
    def download(self):
        num = (ARTWORKS_PER - 1) // 50 + 1  #ceil
        ref = self.url + '&date=' + self.date.strftime("%Y%m%d")
        print("---start collect " + self.date.strftime("%Y-%m-%d") + '---')
        download_cnt = 0
        for i in range(num):
            url = ref + '&p=' + str(i + 1) + '&format=json'

            for j in range(FAIL_TIMES):
                headers = self.headers
                headers.update({'Referer': ref})
                try:
                    response = requests.get(url,
                                            headers=headers,
                                            proxies=PROXIES,
                                            cookies=self.cookie,
                                            timeout=4)
                    if response.status_code == 200:
                        for illust in response.json()['contents']:
                            group = ImageGroup(str(illust['illust_id']),
                                               self.cookie)
                            group.collect()
                            self.size += group.download()
                            download_cnt += 1
                            print("--collect " +
                                  self.date.strftime("%Y-%m-%d") + ' illust:' +
                                  str(download_cnt) + ' complete--')
                            if self.size >= self.capacity: break
                            if download_cnt == ARTWORKS_PER: break
                        break
                except Exception as e:
                    print(e)
                    print("check your proxy setting")
                    print("maybe it was banned.")
                    print("This is " + str(j + 1) + " attempt")
                    print("next attempt will start in 5 sec\n")
                    time.sleep(5)

                if self.size >= self.capacity: break
                if download_cnt == ARTWORKS_PER: break

            if self.size >= self.capacity: break
            if download_cnt == ARTWORKS_PER: break

        print("---collect " + self.date.strftime("%Y-%m-%d") + ' complete---')

    def run(self):
        print("---start download " + self.mode + " ranking---")
        print("start with " + self.date.strftime("%Y-%m-%d"))
        print("end with " + (self.date + datetime.timedelta(
            days=self.domain - 1)).strftime("%Y-%m-%d" + '\n'))
        time.sleep(0.5)

        for i in range(DOMAIN):
            self.download()
            self.__nextday()

        print("---download " + self.mode + " ranking complete---")
        return self.size
