import unittest

from config import DOWNLOAD_CONFIG
from crawlers.users_crawler import UserCrawler
from utils import checkDir


class TestUserCrawler(unittest.TestCase):
    def test_run(self):
        checkDir(DOWNLOAD_CONFIG["STORE_PATH"])
        app = UserCrawler(artist_id="32548944", capacity=10)
        app.run()


if __name__ == "__main__":
    unittest.main()
