from settings import *
from login import Login
import requests
import os
import sys
from image_group import ImageGroup
from ranking_crawler import RankingCrawler


# load cookies from cookies.json
def load_cookie():
    ret = requests.cookies.RequestsCookieJar()
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            ret.set(cookie['name'], cookie['value'])
    return ret


# create folder
def checkfolder():
    if not os.path.exists(IMAGES_STORE_PATH):
        os.makedirs(IMAGES_STORE_PATH)
        print("create " + IMAGES_STORE_PATH + " folder  ")


# 2nd parameter is flow capacity, default is 1024MB
app = RankingCrawler(load_cookie(), 200)
print("total flow used: " + str(app.run()) + 'MB')
