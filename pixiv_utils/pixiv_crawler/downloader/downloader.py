import concurrent.futures as futures
from typing import Iterable, Set

import tqdm

from pixiv_utils.pixiv_crawler.config import download_config
from pixiv_utils.pixiv_crawler.utils import assertWarn, printInfo

from .download_image import downloadImage


class Downloader:
    """
    Downloader download images from urls
    """

    def __init__(self, capacity: float):
        """
        Initialize the Downloader object.

        Args:
            capacity (float): The download capacity in MB.

        """
        self.url_group: Set[str] = set()
        self.capacity = capacity

    def add(self, urls: Iterable[str]):
        for url in urls:
            self.url_group.add(url)

    def getUrls(self) -> Set[str]:
        return self.url_group

    def download(self):
        download_traffic = 0.0
        printInfo("===== Downloader start =====")

        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(self.url_group), desc="Downloading") as pbar:
                image_size_futures = [executor.submit(downloadImage, url) for url in self.url_group]
                for future in futures.as_completed(image_size_futures):
                    download_traffic += future.result()
                    pbar.set_description(f"Downloading {download_traffic:.2f} MB")
                    pbar.update()

                    if download_traffic > self.capacity:
                        executor.shutdown(wait=False, cancel_futures=True)
                        assertWarn(False, "Download capacity reached!")
                        break

        printInfo("===== Downloading complete =====")
        return download_traffic
