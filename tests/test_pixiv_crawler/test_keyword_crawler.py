import os
import random
import shutil
import unittest

from pixiv_utils.pixiv_crawler import (
    KeywordCrawler,
    checkDir,
    debug_config,
    download_config,
    network_config,
    user_config,
)


class TestKeywordCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        download_config.store_path = "TEST_KEYWORD_CRAWLER"
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
        download_config.with_tag = True

        checkDir(download_config.store_path)
        app = KeywordCrawler(
            keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
            order=False,
            mode=["safe", "r18", "all"][-1],
            n_images=5,
            capacity=10,
        )

        if random.choice([True, False]):
            # Download images
            app.run()

            self.assertGreater(len(app.downloader.url_group), 20)
            self.assertTrue("tags.json" in os.listdir(download_config.store_path))
            self.assertGreater(len(os.listdir(download_config.store_path)), 5)
        else:
            # Only download urls
            url_group = app.run(url_only=True)

            self.assertGreater(len(url_group), 20)
            self.assertEqual(url_group, app.downloader.url_group)
            self.assertTrue("tags.json" in os.listdir(download_config.store_path))
            self.assertEqual(len(os.listdir(download_config.store_path)), 1)


if __name__ == "__main__":
    unittest.main()
