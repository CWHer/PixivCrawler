from settings import *
from login import Login
from ranking_crawler import RankingCrawler
from bookmark_crawler import BookmarkCrawler
from users_crawler import UserCrawler

# fetch cookies
# browser = Login()
# browser.fetch()

checkfolder()

# # download artworks from ranking
# # 2nd parameter is flow capacity, default is 1024MB
# app = RankingCrawler(load_cookie(), 200)
# app.run()

# # download artworks from bookmark
# # 2nd parameter is max download number, default is 200
# # 3nd parameter is flow capacity, default is 1024MB
# app = BookmarkCrawler(load_cookie(), 40, 4096)
# app.run()

# download all artworks from a single artist
# 2nd parameter is flow capacity, default is 1024MB
# app = UserCrawler('2509595', load_cookie(), 2000)
# app.run()
