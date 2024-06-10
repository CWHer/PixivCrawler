import concurrent.futures as futures
import functools
import json
import os
from typing import Dict, Iterable, List, Set

import tqdm

from pixiv_utils.pixiv_crawler.config import download_config, user_config
from pixiv_utils.pixiv_crawler.downloader import Downloader
from pixiv_utils.pixiv_crawler.utils import printInfo

from .collector_unit import collect
from .selectors import selectPage, selectTag


class Collector:
    """
    Collect all image ids in each artwork, and send to downloader
    NOTE: An artwork may contain multiple images.
    """

    def __init__(self, downloader: Downloader):
        self.id_group: Set[str] = set()  # illust_id
        self.downloader = downloader

    def add(self, image_ids: Iterable[str]):
        for image_id in image_ids:
            self.id_group.add(image_id)

    def collectTags(self, file_name: str = "tags.json"):
        """
        Collect artwork tags and save in tags.json
        """
        printInfo("===== Tag collector start =====")

        self.tags: Dict[str, List] = dict()
        additional_headers = {"Referer": "https://www.pixiv.net/bookmark.php?type=user"}
        collect_tag_fn = functools.partial(
            collect, selector=selectTag, additional_headers=additional_headers
        )
        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(self.id_group), desc="Collecting tags") as pbar:
                urls = [
                    f"https://www.pixiv.net/artworks/{illust_id}" for illust_id in self.id_group
                ]
                for illust_id, tags in zip(
                    self.id_group,
                    executor.map(
                        collect_tag_fn,
                        urls,
                    ),
                ):
                    if tags is not None:
                        self.tags[illust_id] = tags
                    pbar.update()

        file_path = os.path.join(download_config.store_path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.tags, indent=4, ensure_ascii=False))

        printInfo("===== Tag collector complete =====")

    def collect(self):
        """
        Collect all image ids in each artwork, and send to downloader
        NOTE: an artwork may contain multiple images
        """
        if download_config.with_tag:
            self.collectTags()

        printInfo("===== Collector start =====")
        printInfo("NOTE: An artwork may contain multiple images.")

        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(self.id_group), desc="Collecting urls") as pbar:
                urls = [
                    f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh"
                    for illust_id in self.id_group
                ]
                additional_headers = [
                    {
                        "Referer": f"https://www.pixiv.net/artworks/{illust_id}",
                        "x-user-id": user_config.user_id,
                    }
                    for illust_id in self.id_group
                ]
                url_futures = [
                    executor.submit(collect, url, selectPage, headers)
                    for url, headers in zip(urls, additional_headers)
                ]
                for future in futures.as_completed(url_futures):
                    urls = future.result()
                    if urls is not None:
                        self.downloader.add(urls)
                    pbar.update()

        printInfo("===== Collector complete =====")
        printInfo(f"Number of images: {len(self.downloader.url_group)}")
