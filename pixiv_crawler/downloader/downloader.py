import concurrent.futures as futures
from typing import Iterable, Set

from config import DOWNLOAD_CONFIG
from tqdm import tqdm
from utils import printInfo

from .download_image import downloadImage


class Downloader:
    """[summary]
    download controller
    """

    def __init__(self, capacity):
        self.url_group: Set[str] = set()
        self.capacity = capacity

    def add(self, urls: Iterable[str]):
        for url in urls:
            self.url_group.add(url)

    def download(self):
        flow_size = 0.0
        printInfo("===== downloader start =====")

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(self.url_group), desc="downloading") as pbar:
                for image_size in executor.map(downloadImage, self.url_group):
                    flow_size += image_size
                    pbar.update()
                    pbar.set_description(f"downloading / flow {flow_size:.2f}MB")
                    if flow_size > self.capacity:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

        printInfo("===== downloader complete =====")
        return flow_size
