import concurrent.futures as futures
from typing import Set

from collector.collector import Collector
from collector.collector_unit import collect
from collector.selectors import selectKeyword
from config import DOWNLOAD_CONFIG, USER_CONFIG
from downloader.downloader import Downloader
from tqdm import tqdm
from utils import printInfo
from urllib.parse import quote


class TagsCrawler():
    """[summary]
    download search results of tags (sorted by popularity)
    """
    def __init__(self, tags: str, n_images=200, capacity=1024, order=False):
        self.tags = tags
        self.n_images = n_images
        self.order = order

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def collect(self):
        """[summary]
        collect illust_id from keyword result
        url sample: "https://www.pixiv.net/ajax/search/artworks/
        (女装 OR 男の娘) 制服
        ?word=(女装 OR 男の娘) 制服
        &order=date_d&mode=all&p=5&s_mode=s_tag&type=all&lang=zh"
        """

        # each keyword.json contains 60 artworks
        ARTWORK_PER = 60
        n_page = (self.n_images - 1) // ARTWORK_PER + 1  # ceil
        printInfo(f"===== start collecting {self.tags} =====")

        urls: Set[str] = set()
        if self.order:
            url = "https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=popular_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh"
        else:
            url = "https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh"
        filename = quote(self.tags, safe='()')
        word = quote(self.tags.replace(' ', '+'), safe='+')

        for i in range(n_page):
            urls.add(url.format(filename, word, i + 1))

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(urls), desc="collecting ids") as pbar:
                additional_headers = {"COOKIE": USER_CONFIG["COOKIE"]}
                for image_ids in executor.map(collect, zip(
                        urls, [selectKeyword] * len(urls),
                        [additional_headers] * len(urls))):
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== collect {self.tags} complete =====")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.downloader.download()
