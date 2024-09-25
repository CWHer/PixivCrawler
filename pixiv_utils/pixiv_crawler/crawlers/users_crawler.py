from typing import Set, Union

from pixiv_utils.pixiv_crawler.collector import Collector, collect, selectUser
from pixiv_utils.pixiv_crawler.config import user_config
from pixiv_utils.pixiv_crawler.downloader import Downloader
from pixiv_utils.pixiv_crawler.utils import printInfo


class UserCrawler:
    """
    Collect all artworks from a single artist

    Sample URL: "https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh"
    """

    def __init__(self, artist_id: str, capacity: float = 1024):
        """
        Args:
            artist_id: Artist's ID.
            capacity: Flow capacity. Defaults to 1024.
        """
        self.artist_id = artist_id

        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def collect(self):
        url = f"https://www.pixiv.net/ajax/user/{self.artist_id}/profile/all?lang=zh"
        additional_headers = {
            "Referer": f"https://www.pixiv.net/users/{self.artist_id}/illustrations",
            "x-user-id": user_config.user_id,
            "COOKIE": user_config.cookie,
        }
        image_ids = collect(url, selectUser, additional_headers)
        if image_ids is not None:
            self.collector.add(image_ids)
        printInfo(f"===== Collect user {self.artist_id} complete =====")

    def run(self) -> Union[Set[str], float]:
        """
        Run the user crawler

        Returns:
            Union[Set[str], float]: artwork urls or download traffic usage
        """
        self.collect()
        self.collector.collect()
        return self.downloader.download()
