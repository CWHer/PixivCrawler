# download personal public bookmarks
from settings import *
import requests
import re
import sys
import time
from image_group import ImageGroup


class BookmarkCrawler():
    # count-badge sample:
    #   </h1><span class="count-badge">3069.</span>
    # artworks sample:
    #   href="/artworks/83348083
    # url sample:
    #   https://www.pixiv.net/bookmark.php?rest=show&p=1
    #   rest=show for public/ rest=hide for private
    #   note that 20 artworks per p
    # maxnum replace capacity in this code
    # max number of downloads
    def __init__(self, cookie, maxnum=200):
        self.num = maxnum
        self.cookie = cookie
        self.url = "https://www.pixiv.net/bookmark.php?rest=show"
        self.headers = BROWSER_HEADER
        self.size = 0
        self.download_cnt = 0

    # get count-badge
    def collect(self):
        print("---start collect bookmark count---")
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
                    print("---collect bookmark count complete---")
                    return
            except Exception as e:
                print(e)
                print("check your proxy setting")
                print("maybe it was banned.")
                print("This is " + str(i + 1) + " attempt")
                print("next attempt will start in " + str(FAIL_DELAY) +
                      " sec\n")
                time.sleep(FAIL_DELAY)
        print("---fail to collect bookmark count---")
        sys.exit(0)

    # download per page
    def __download(self, response):
        artworks = set(re.findall("artworks/(\d+)", response.text))
        for artwork in artworks:
            group = ImageGroup(artwork, self.cookie)
            group.collect()
            self.size += group.download()
            self.download_cnt += 1
            print("--download bookmark artwork:" + str(self.download_cnt) +
                  ' complete--')
            if self.download_cnt == self.num: return

    def run(self):
        print("---start download " + PIXIV_ID + "\'s bookmarks---")
        # note that 20 artworks per p
        num = (self.num - 1) // 20 + 1
        for i in range(num):
            url = self.url + '&p=' + str(i + 1)
            print("***total flow used: " + str(self.size) + "MB***")
            # collect p=i+1
            for j in range(FAIL_TIMES):
                try:
                    response = requests.get(url,
                                            headers=self.headers,
                                            proxies=PROXIES,
                                            cookies=self.cookie,
                                            timeout=4)
                    if response.status_code == 200:
                        self.__download(response)
                        break
                except Exception as e:
                    print(e)
                    print("check your proxy setting")
                    print("maybe it was banned.")
                    print("This is " + str(j + 1) + " attempt")
                    print("next attempt will start in " + str(FAIL_DELAY) +
                          " sec\n")
                    time.sleep(FAIL_DELAY)

            if self.download_cnt == self.num: break

        print("---download bookmarks complete---")
        return self.size
