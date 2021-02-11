import datetime
import json
import sys
import os

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
DOWNLOAD_DELAY = 1
# wait seconds between each fail
FAIL_DELAY = 1
# max parallel threads number
MAX_THREADS = 12
# delay between start threads
THREAD_DELAY = 0.05

# image store path
# only change name is OK, don't modify '\'
IMAGES_STORE_PATH = 'user/'

# start date
START_DATE = datetime.date(2021, 2, 1)
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
