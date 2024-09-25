import concurrent.futures as futures
import functools
import time
from typing import Set, Union

import requests
import tqdm

from pixiv_utils.pixiv_crawler.collector import Collector, collect, selectBookmark
from pixiv_utils.pixiv_crawler.config import (
    debug_config,
    download_config,
    network_config,
    user_config,
)
from pixiv_utils.pixiv_crawler.downloader import Downloader
from pixiv_utils.pixiv_crawler.utils import assertError, assertWarn, printInfo


class BookmarkCrawler:
    """
    Download images from user's public bookmarks
    """

    def __init__(self, n_images: int = 200, capacity: float = 1024):
        """
        Args:
            n_images: Number of images to download. Defaults to 200.
            capacity: Flow capacity. Defaults to 1024.
        """
        self.n_images = n_images
        self.uid = user_config.user_id
        self.user_url = f"https://www.pixiv.net/ajax/user/{self.uid}/illusts"

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def _requestCount(self):
        """
        Get the number of bookmarks of the user
        Sample URL: "https://www.pixiv.net/ajax/user/xxxx/illusts/bookmark/tags?lang=zh"
        """

        url = self.user_url + "/bookmark/tags?lang=zh"
        printInfo("===== Requesting bookmark count =====")

        headers = {"COOKIE": user_config.cookie}
        headers.update(network_config.headers)
        for i in range(download_config.retry_times):
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    proxies=network_config.proxy,
                    timeout=download_config.timeout,
                )

                if response.status_code == requests.codes.ok:
                    n_total = int(response.json()["body"]["public"][0]["cnt"])
                    self.n_images = min(self.n_images, n_total)
                    printInfo(f"Select {self.n_images}/{n_total} artworks")
                    printInfo("===== Request bookmark count complete =====")
                    return

            except Exception as e:
                assertWarn(not debug_config.show_error, e)
                assertWarn(
                    not debug_config.show_error, f"This is {i} attempt to request bookmark count"
                )

                time.sleep(download_config.fail_delay)

        assertWarn(False, "Please check your cookie configuration")
        assertError(False, "===== Fail to get bookmark count =====")

    def collect(self, artworks_per_json: int = 48):
        """
        Collect illust_id from bookmark

        Sample URL: "https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh"
        NOTE: [offset + 1, offset + limit]
        NOTE: id of disable artwork is int (not str)

        Args:
            artworks_per_json: Number of artworks per bookmark.json. Defaults to 48.
        """

        n_page = (self.n_images - 1) // artworks_per_json + 1  # ceil
        printInfo(f"===== Start collecting {self.uid}'s bookmarks =====")

        urls: Set[str] = set()
        for i in range(n_page):
            urls.add(
                self.user_url
                + "/bookmarks?"
                + "&".join(
                    [
                        f"tag=",
                        f"offset={i * artworks_per_json}",
                        f"limit={artworks_per_json}",
                        f"rest=show",
                        f"lang=zh",
                    ]
                )
            )

        additional_headers = {"COOKIE": user_config.cookie}
        collect_bookmark_fn = functools.partial(
            collect, selector=selectBookmark, additional_headers=additional_headers
        )
        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(urls), desc="Collecting ids") as pbar:
                image_ids_futures = [executor.submit(collect_bookmark_fn, url) for url in urls]
                for future in futures.as_completed(image_ids_futures):
                    image_ids = future.result()
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo("===== Collect bookmark complete =====")
        printInfo(f"Number of downloadable artworks: {len(self.collector.id_group)}")

    def run(self) -> Union[Set[str], float]:
        """
        Run the bookmark crawler

        Returns:
            Union[Set[str], float]: artwork urls or download traffic usage
        """
        self._requestCount()
        self.collect()
        self.collector.collect()
        return self.downloader.download()
