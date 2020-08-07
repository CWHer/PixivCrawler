from settings import *
from login import Login
from ranking_crawler import RankingCrawler
from bookmark_crawler import BookmarkCrawler

# fetch cookies
# Login.fetch()

checkfolder()

# # download artworks from ranking
# # 2nd parameter is flow capacity, default is 1024MB
# app = RankingCrawler(load_cookie(), 200)
# app.run()

# download artworks from bookmark
# 2nd parameter is max download number, default is 200
# 3nd parameter is flow capacity, default is 1024MB
app = BookmarkCrawler(load_cookie(), 40, 4096)
app.run()
