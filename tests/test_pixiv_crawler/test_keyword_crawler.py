import unittest

from config import DOWNLOAD_CONFIG
from crawlers.keyword_crawler import KeywordCrawler
from utils import checkDir


class TestKeywordCrawler(unittest.TestCase):
    def test_run(self):
        checkDir(DOWNLOAD_CONFIG["STORE_PATH"])
        app = KeywordCrawler(
            keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
            order=False,
            mode=["safe", "r18", "all"][-1],
            n_images=5,
            capacity=10,
        )
        app.run()


if __name__ == "__main__":
    unittest.main()
