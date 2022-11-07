from config import DOWNLOAD_CONFIG
from crawlers.bookmark_crawler import BookmarkCrawler
from crawlers.keyword_crawler import KeywordCrawler
from crawlers.ranking_crawler import RankingCrawler
from crawlers.users_crawler import UserCrawler
from utils import checkDir


if __name__ == "__main__":

    checkDir(DOWNLOAD_CONFIG["STORE_PATH"])

    # case 1: (need cookie !!!)
    #   download artworks from rankings
    #   the only parameter is flow capacity, default is 1024MB
    app = RankingCrawler(capacity=200)
    app.run()

    # case 2: (need cookie !!!)
    #   download artworks from bookmark
    #   1st parameter is max download number, default is 200
    #   2nd parameter is flow capacity, default is 1024MB
    app = BookmarkCrawler(n_images=20, capacity=200)
    app.run()

    # case 3: (need cookie for R18 images !!!)
    #   download artworks from a single artist
    #   2nd parameter is flow capacity, default is 1024MB
    app = UserCrawler(artist_id="32548944", capacity=200)
    app.run()

    # case 4: (need premium & cookie !!!)
    #   download search results of a keyword (sorted by popularity if order=True)
    #   support advanced search, e.g. "(Lucy OR 边缘行者) AND (5000users OR 10000users)"
    #       refer to https://www.pixiv.help/hc/en-us/articles/235646387-I-would-like-to-know-how-to-search-for-content-on-pixiv-
    #   1st parameter is keyword
    #   2nd parameter is order (default is False, standing for order by date, True for order by popularity)
    #   3rd parameter is mode (support ["safe", "r18", "all"], default is "safe")
    #   4th parameter is max download number
    #   5th parameter is flow capacity
    app = KeywordCrawler(keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
                         order=False, mode=["safe", "r18", "all"][-1], n_images=20, capacity=200)
    app.run()
