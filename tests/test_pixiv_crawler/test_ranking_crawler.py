import datetime
import os
import random
import shutil
import unittest

from pixiv_utils.pixiv_crawler import (
    RankingCrawler,
    checkDir,
    debug_config,
    download_config,
    network_config,
    ranking_config,
    user_config,
)


class TestRankingCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        download_config.store_path = "TEST_RANKING_CRAWLER"
        assert not os.path.exists(download_config.store_path)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(download_config.store_path)

    def test_run(self):
        debug_config.show_error = True
        proxy = os.getenv("https_proxy") or os.getenv("HTTPS_PROXY")
        if proxy is not None:
            network_config.proxy["https"] = proxy
        user_config.user_id = ""
        user_config.cookie = ""
        download_config.with_tag = False
        ranking_config.start_date = datetime.date(2024, 5, 1)
        ranking_config.range = 2
        ranking_config.mode = "weekly"
        ranking_config.content_mode = "illust"
        ranking_config.num_artwork = 50

        checkDir(download_config.store_path)
        app = RankingCrawler(capacity=10)

        if random.choice([True, False]):
            # Download images
            app.run()

            self.assertGreater(len(app.downloader.url_group), 50)
            self.assertGreater(len(os.listdir(download_config.store_path)), 5)
        else:
            # Only download urls
            url_group = app.run(url_only=True)

            self.assertGreater(len(url_group), 50)
            self.assertEqual(url_group, app.downloader.url_group)
            self.assertEqual(len(os.listdir(download_config.store_path)), 0)


if __name__ == "__main__":
    unittest.main()
