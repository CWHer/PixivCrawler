import datetime
import json
import sys
import threading
import os
import requests
import re
from pyquery import PyQuery as pq

# threadinglock used in write_fail_log
WRITE_FAIL_LOG_LOCK = threading.Lock()


# append text in fail_log.txt
def write_fail_log(text):
    WRITE_FAIL_LOG_LOCK.acquire()
    with open("fail_log.txt", "a+") as f:
        f.write(text)
    WRITE_FAIL_LOG_LOCK.release()


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


# ---selector begin---
# url:https://www.pixiv.net/ajax/illust/xxxx/pages?lang=zh
# collect all images' url from (page.json)
# return url
def image_group_selector(response):
    group = set()
    for url in response.json()['body']:
        group.add(url['urls']['original'])
    return group


# url:https://www.pixiv.net/artworks/xxxxxx
# collect image tags
# return a list of tags
def tags_selector(response):
    group = []
    doc = pq(response.text)
    illust_id = re.search('artworks/(\d+)', response.url).group(1)
    content = json.loads(doc('#meta-preload-data').attr('content'))
    tags = content['illust'][illust_id]['tags']['tags']
    for tag in tags:
        translation = tag.get('translation')
        if translation == None:
            group.append(tag['tag'])
        else:
            group.append(translation['en'])
    return group


# url:https://www.pixiv.net/ranking.php?mode=daily&date=20200801&p=1&format=json
# collect all illust_id from (ranking.json)
# return illust_id
def ranking_selector(response):
    group = set()
    for artwork in response.json()['contents']:
        group.add(str(artwork['illust_id']))
    return group


# url:https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh
# collect all illust_id from (user.json)
# return illust_id
def user_selector(response):
    return set(response.json()['body']['illusts'].keys())


# url:https://www.pixiv.net/bookmark.php?rest=show&p=1
# collect all artworks/xxxx
# return illust_id
def page_selector(response):
    return set(re.findall("artworks/(\d+)", response.text))


# ---selector end---

# user id
# access your pixiv user profile to find this
# it should be something like https://www.pixiv.net/users/xxxx
# change following string into your id
USER_ID = '22821761'

# note that the name and password are required in 'userdata.json'
# it should be something like
# {
#     "name": "xxx",
#     "password": "xxx"
# }
PIXIV_ID = ""
try:
    with open('userdata.json') as f:
        user = json.load(f)
        PIXIV_ID = user['name']
except FileNotFoundError:
    print("---do not find userdata.json---")
    sys.exit(0)
else:
    print("---load userdata.json successfully!---")

# abort request/download after 5(default) unsuccessful attempts
FAIL_TIMES = 20

# wait seconds between each download
# note that it should better be greater than 0.2 sec
DOWNLOAD_DELAY = 0.5
# wait seconds between each fail
FAIL_DELAY = 1
# max parallel threads number
MAX_THREADS = 20

# image store path
# only change name is OK, don't modify '\'
IMAGES_STORE_PATH = 'images/'

# start date
START_DATE = datetime.date(2020, 7, 25)
# date domain
# [start,start+domain-1]
DOMAIN = 2

# crawl mode for ranking crawler
PIXIV_MODES = [
    'daily', 'weekly', 'monthly', 'male', 'female', 'daily_r18', 'weekly_r18',
    'male_r18', 'female_r18'
]
# [0,7]
PIXIV_MODE = 0
# download artworks per mode based request
# suggest to be divisible by 50
ARTWORKS_PER = 2

# proxy setting
# you should customize your proxy setting accordingly
# note that for ss/ssr no need to change
#   if you use default ss/ssr settings
PROXIES = {'https': '127.0.0.1:1080'}

# browser header
# default: chrome
BROWSER_HEADER = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

# chrome user data direction for selenium
# replace the following string with your own user name
# it should be something like
# C:\\Users\\xxxxx\\.....
# note that you can remove (it's now removed)
#   'options.add_argument("--headless")' in login.py
#   to check if chrome can implement correctly with this
USER_DATA_DIR = 'C:\\Users\\cwher\\AppData\\Local\\Google\\Chrome\\User Data'
