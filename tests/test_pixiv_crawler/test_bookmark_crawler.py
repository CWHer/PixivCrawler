import unittest

from config import DOWNLOAD_CONFIG, USER_CONFIG
from crawlers.bookmark_crawler import BookmarkCrawler
from utils import checkDir


class TestBookmarkCrawler(unittest.TestCase):
    @unittest.skipIf(USER_CONFIG["COOKIE"] == "", "No cookie")
    def test_run(self):
        checkDir(DOWNLOAD_CONFIG["STORE_PATH"])
        app = BookmarkCrawler(n_images=5, capacity=10)
        app.run()


if __name__ == "__main__":
    unittest.main()
