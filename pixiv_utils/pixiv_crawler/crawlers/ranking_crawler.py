import concurrent.futures as futures
import datetime
import re
from typing import Set, Union

import tqdm

from pixiv_utils.pixiv_crawler.collector import Collector, collect, selectRanking
from pixiv_utils.pixiv_crawler.config import download_config, ranking_config, user_config
from pixiv_utils.pixiv_crawler.downloader import Downloader
from pixiv_utils.pixiv_crawler.utils import printInfo


class RankingCrawler:
    def __init__(self, capacity: float = 1024):
        """
        RankingCrawler download artworks from ranking

        Args:
            capacity (float, optional): The flow capacity in MB. Defaults to 1024.
        """
        self.date = ranking_config.start_date
        self.range = ranking_config.range
        self.mode = ranking_config.mode
        assert self.mode in ranking_config.ranking_modes, f"Invalid mode: {self.mode}"
        self.content = ranking_config.content_mode
        assert self.content in ranking_config.content_modes, f"Invalid content mode: {self.content}"

        # NOTE:
        #   1. url sample: "https://www.pixiv.net/ranking.php?mode=daily&content=all&date=20200801&p=1&format=json"
        #      url sample: "https://www.pixiv.net/ranking.php?mode=daily&content=illust&date=20220801&p=2&format=json"
        #   2. ref url sample: "https://www.pixiv.net/ranking.php?mode=daily&date=20200801"
        self.url_template = "https://www.pixiv.net/ranking.php?" + "&".join(
            [
                f"mode={self.mode}",
                f"content={self.content}",
                "date={}",
                "p={}",
                "format=json",
            ]
        )

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def _collect(self, artworks_per_json: int = 50):
        """
        Collect illust_id from ranking

        Args:
            artworks_per_json: Number of artworks per ranking.json. Defaults to 50.
        """
        num_page = (ranking_config.num_artwork - 1) // artworks_per_json + 1  # ceil

        def addDate(current: datetime.date, days):
            return current + datetime.timedelta(days)

        content = f"{self.mode}:{self.content}"
        printInfo(f"===== Start collecting {content} ranking =====")
        printInfo(
            "From {} to {}".format(
                self.date.strftime("%Y-%m-%d"),
                addDate(self.date, self.range - 1).strftime("%Y-%m-%d"),
            )
        )

        urls: Set[str] = set()
        for _ in range(self.range):
            for i in range(num_page):
                urls.add(self.url_template.format(self.date.strftime("%Y%m%d"), i + 1))
            self.date = addDate(self.date, 1)

        with futures.ThreadPoolExecutor(download_config.num_threads) as executor:
            with tqdm.trange(len(urls), desc="Collecting image ids") as pbar:
                additional_headers = [
                    {
                        "Referer": re.search("(.*)&p", url).group(1),
                        "x-requested-with": "XMLHttpRequest",
                        "Cookie": user_config.cookie,
                    }
                    for url in urls
                ]
                image_ids_futures = [
                    executor.submit(collect, url, selectRanking, additional_header)
                    for url, additional_header in zip(urls, additional_headers)
                ]
                for future in futures.as_completed(image_ids_futures):
                    image_ids = future.result()
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== Collect {content} ranking complete =====")

    def run(self) -> Union[Set[str], float]:
        """
        Run the ranking crawler

        Returns:
            Union[Set[str], float]: artwork urls or download traffic usage
        """
        self._collect()
        self.collector.collect()
        return self.downloader.download()
