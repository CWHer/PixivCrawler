# collect single user's all illustrations
#   url sample: https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh
from settings import USER_ID
from utils import user_selector
from collector import Collector
from collector_unit import CollectorUnit


class UserCrawler():
    def __init__(self, artist_id, cookie, capacity=1024):
        self.url = 'https://www.pixiv.net/ajax/user/' + artist_id + '/profile/all?lang=zh'
        self.ref = 'https://www.pixiv.net/users/' + artist_id + '/illustrations'
        self.headers = {'x-user-id': USER_ID}
        self.headers.update({'Referer': self.ref})
        self.cookie = cookie
        self.collector = Collector(cookie, capacity)

    def collect(self):
        user = CollectorUnit(self.url, self.cookie, user_selector,
                             self.headers)
        user.start()
        user.join()
        self.collector.add(user.group)
        print("--send user " + user.url + " to collector--")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.collector.download()
