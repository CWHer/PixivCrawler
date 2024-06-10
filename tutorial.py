import datetime
import os

from pixiv_utils.pixiv_crawler import (
    BookmarkCrawler,
    KeywordCrawler,
    RankingCrawler,
    UserCrawler,
    checkDir,
    displayAllConfig,
    download_config,
    network_config,
    ranking_config,
    user_config,
)


def downloadRanking():
    """
    Download artworks from rankings

    NOTE: Require cookie for R18 images!

    Args:
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False
    ranking_config.start_date = datetime.date(2024, 5, 1)
    ranking_config.range = 2
    ranking_config.mode = "weekly"
    ranking_config.content_mode = "illust"
    ranking_config.num_artwork = 50

    displayAllConfig()
    checkDir(download_config.store_path)

    app = RankingCrawler(capacity=200)
    app.run()


def downloadBookmark():
    """
    Download artworks from bookmark

    NOTE: Require cookie!

    Args:
        n_images (int): max download number, default is 200
        capacity (int): flow capacity, default is 1024MB
    """
    download_config.with_tag = False
    user_config.user_id = "[TODO]: Your user_id here"
    user_config.cookie = "[TODO]: Your cookie here"

    displayAllConfig()
    checkDir(download_config.store_path)

    app = BookmarkCrawler(n_images=20, capacity=200)
    app.run()


def downloadUser():
    """
    Download artworks from a single artist

    NOTE: Require cookie for R18 images!

    Args:
        artist_id (str): artist id
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False

    displayAllConfig()
    checkDir(download_config.store_path)

    app = UserCrawler(artist_id="32548944", capacity=200)
    app.run()


def downloadKeyword():
    """
    Download search results of a keyword (sorted by popularity if order=True)
    Support advanced search, e.g. "(Lucy OR 边缘行者) AND (5000users OR 10000users)", refer to https://www.pixiv.help/hc/en-us/articles/235646387-I-would-like-to-know-how-to-search-for-content-on-pixiv

    NOTE: Require cookie for R18 images!

    Args:
        keyword (str): search keyword
        order (bool): order by popularity or not, default is False
        mode (str): content mode, default is "safe", support ["safe", "r18", "all"]
        n_images (int): max download number, default is 200
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False

    displayAllConfig()
    checkDir(download_config.store_path)

    app = KeywordCrawler(
        keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
        order=False,
        mode=["safe", "r18", "all"][-1],
        n_images=20,
        capacity=200,
    )
    app.run()


def loadEnv():
    """
    Load environment variables for proxy, cookie, and user_id
    """
    # Use system proxy settings
    proxy = os.getenv("https_proxy") or os.getenv("HTTPS_PROXY")
    if proxy is not None:
        network_config.proxy["https"] = proxy

    # Use system user_id and cookie
    cookie = os.getenv("PIXIV_COOKIE")
    uid = os.getenv("PIXIV_UID")
    if cookie is not None:
        user_config.cookie = cookie
    if uid is not None:
        user_config.user_id = uid


if __name__ == "__main__":
    # loadEnv()

    downloadRanking()
    downloadBookmark()
    downloadUser()
    downloadKeyword()
