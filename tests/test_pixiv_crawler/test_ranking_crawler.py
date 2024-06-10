import unittest

from config import DOWNLOAD_CONFIG
from crawlers.ranking_crawler import RankingCrawler
from utils import checkDir


class TestRankingCrawler(unittest.TestCase):
    def test_run(self):
        checkDir(DOWNLOAD_CONFIG["STORE_PATH"])
        app = RankingCrawler(capacity=10)
        app.run()


if __name__ == "__main__":
    unittest.main()
