import concurrent.futures as futures
import functools
import urllib.parse as urlparse
from typing import Set, Union

import tqdm

from pixiv_utils.pixiv_crawler.collector import Collector, collect, selectKeyword
from pixiv_utils.pixiv_crawler.config import download_config, user_config
from pixiv_utils.pixiv_crawler.downloader import Downloader
from pixiv_utils.pixiv_crawler.utils import printInfo


class KeywordCrawler:
    """
    Download images from search results of a given keyword
    """

    def __init__(
        self,
        keyword: str,
        order: bool = False,
        mode: str = "safe",
        n_images: int = 200,
        capacity: float = 1024,
    ):
        """
        Args:
            keyword: Search keyword.
            order: Order by popularity if True, by date if False. Defaults to False.
            mode: Search mode. Defaults to "safe".
            n_images: Number of images to download. Defaults to 200.
            capacity: Flow capacity. Defaults to 1024.
        """
        assert mode in ["safe", "r18", "all"], f"mode {mode} not supported"

        self.keyword = keyword
        self.order = order
        self.mode = mode

        self.n_images = n_images

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def collect(self, artworks_per_json: int = 60):
        """
        Collect illust_id from keyword result

        Sample URL: "https://www.pixiv.net/ajax/search/artworks/{xxxxx}?word={xxxxx}&order=popular_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"

        Args:
            artworks_per_json: Number of artworks per json. Defaults to 60.
        """

        n_page = (self.n_images - 1) // artworks_per_json + 1  # ceil
        printInfo(f"===== Start collecting {self.keyword} =====")

        urls: Set[str] = set()
        url = (
            "https://www.pixiv.net/ajax/search/artworks/"
            + f"{urlparse.quote(self.keyword, safe='()')}?"
            + "&".join(
                [
                    f"word={urlparse.quote(self.keyword)}",
                    f"order={'popular_d' if self.order else 'date_d'}",
                    f"mode={self.mode}",
                    "p={}",
                    f"s_mode=s_tag",
                    f"type=all",
                    f"lang=zh",
                ]
            )
        )
        for i in range(n_page):
            urls.add(url.format(i + 1))

        additional_headers = {"COOKIE": user_config.cookie}
        collect_keyword_fn = functools.partial(
            collect, selector=selectKeyword, additional_headers=additional_headers
        )
        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(urls), desc="Collecting ids") as pbar:
                image_ids_futures = [executor.submit(collect_keyword_fn, url) for url in urls]
                for future in futures.as_completed(image_ids_futures):
                    image_ids = future.result()
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== Collect {self.keyword} complete =====")
        printInfo(f"Number of downloadable artworks: {len(self.collector.id_group)}")

    def run(self, url_only: bool = False) -> Union[Set[str], float]:
        """
        Run the keyword crawler

        Args:
            url_only: Only download urls. Defaults to False.

        Returns:
            Union[Set[str], float]: artwork urls or download traffic usage
        """
        self.collect()
        self.collector.collect()

        # Return urls only
        if url_only:
            return self.downloader.getUrls()

        # Download images
        return self.downloader.download()
