from config import DOWNLOAD_CONFIG
from crawlers.bookmark_crawler import BookmarkCrawler
from crawlers.keyword_crawler import KeywordCrawler
from crawlers.ranking_crawler import RankingCrawler
from crawlers.users_crawler import UserCrawler
from crawlers.tag_crawler import TagsCrawler
from utils import checkDir


if __name__ == "__main__":

    checkDir(DOWNLOAD_CONFIG["STORE_PATH"])

    # case 1: (need cookie !!!)
    #   download artworks from rankings
    #   the only parameter is flow capacity, default is 1024MB
    # app = RankingCrawler(capacity=200)
    # app.run()

    # case 2: (need cookie !!!)
    #   download artworks from bookmark
    #   1st parameter is max download number, default is 200
    #   2nd parameter is flow capacity, default is 1024MB
    # app = BookmarkCrawler(n_images=20, capacity=200)
    # app.run()

    # case 3: (need cookie for R18 images !!!)
    #   download artworks from a single artist
    #   2nd parameter is flow capacity, default is 1024MB
    app = UserCrawler(artist_id="32548944", capacity=200)
    app.run()

    # case 4: (need premium & cookie !!!)
    #   download search results of a keyword (sorted by popularity)
    #   1st parameter is keyword
    #   2nd parameter is max download number
    #   3rd parameter is flow capacity
    # app = KeywordCrawler(keyword="女の子", n_images=20, capacity=200)
    # app.run()

    # case 5: (need premium & cookie !!!)
    #   download search results of advanced tags searching (sorted by popularity)
    #   1st parameter is tags (see https://www.pixiv.help/hc/zh-cn/articles/235646387-%E6%83%B3%E4%BA%86%E8%A7%A3%E5%A6%82%E4%BD%95%E5%9C%A8pixiv%E4%B8%8A%E6%90%9C%E7%B4%A2%E4%BD%9C%E5%93%81)
    #   2nd parameter is max download number
    #   3rd parameter is flow capacity
    #   4rd parameter is order (default is False, standing for order by date, True for order by popularity)
    # app = TagsCrawler(keyword="女の子", n_images=20, capacity=200)
    # app.run()


    
