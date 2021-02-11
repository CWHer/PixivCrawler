from settings import IMAGES_STORE_PATH
import re
import threading
import os
import requests
import json
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


# url:https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh
# collect all artworks
# return illust_id
# note that disable artwork'id is num not str...
def page_selector(response):
    group = set()
    for artwork in response.json()['body']['works']:
        if isinstance(artwork['id'], str):
            group.add(artwork['id'])
        else:
            write_fail_log('disable artwork ' + str(artwork['id']) + '\n')
    return group


# ---selector end---
