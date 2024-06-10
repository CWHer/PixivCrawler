import concurrent.futures as futures
import functools
import time
from typing import Set

import requests
import tqdm
from collector.collector import Collector
from collector.collector_unit import collect
from collector.selectors import selectBookmark
from config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG, USER_CONFIG
from downloader.downloader import Downloader
from utils import assertError, assertWarn, printInfo


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
        self.uid = USER_CONFIG["USER_ID"]
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

        headers = {"COOKIE": USER_CONFIG["COOKIE"]}
        headers.update(NETWORK_CONFIG["HEADER"])
        error_output = OUTPUT_CONFIG["PRINT_ERROR"]
        for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
            try:
                response = requests.get(
                    url, headers=headers, proxies=NETWORK_CONFIG["PROXY"], timeout=4
                )

                if response.status_code == requests.codes.ok:
                    n_total = int(response.json()["body"]["public"][0]["cnt"])
                    self.n_images = min(self.n_images, n_total)
                    printInfo(f"Select {self.n_images}/{n_total} artworks")
                    printInfo("===== Request bookmark count complete =====")
                    return

            except Exception as e:
                assertWarn(not error_output, e)
                assertWarn(not error_output, f"This is {i} attempt to request bookmark count")

                time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

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

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        additional_headers = {"COOKIE": USER_CONFIG["COOKIE"]}
        collect_bookmark_fn = functools.partial(
            collect, selector=selectBookmark, additional_headers=additional_headers
        )
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm.trange(len(urls), desc="Collecting ids") as pbar:
                image_ids_futures = [executor.submit(collect_bookmark_fn, url) for url in urls]
                for future in futures.as_completed(image_ids_futures):
                    image_ids = future.result()
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo("===== Collect bookmark complete =====")
        printInfo(f"Number of downloadable artworks: {len(self.collector.id_group)}")

    def run(self):
        self._requestCount()
        self.collect()
        self.collector.collect()
        return self.downloader.download()