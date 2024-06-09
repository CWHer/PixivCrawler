import datetime

# NOTE: MODE_CONFIG only applies to ranking crawler
MODE_CONFIG = {
    # start date
    "START_DATE": datetime.date(2022, 8, 1),
    # date range: [start, start + range - 1]
    "RANGE": 1,
    # which ranking list
    "RANKING_MODES": [
        "daily",
        "weekly",
        "monthly",
        "male",
        "female",
        "daily_ai",
        "daily_r18",
        "weekly_r18",
        "male_r18",
        "female_r18",
        "daily_r18_ai",
    ],
    "MODE": "daily",  # choose from the above
    # illustration, manga, or both
    "CONTENT_MODES": ["all", "illust", "manga"],  # download both illustrations & mangas
    "CONTENT_MODE": "all",  # choose from the above
    # download top x in each ranking
    #   suggested x be a multiple of 50
    "N_ARTWORK": 50,
}

OUTPUT_CONFIG = {
    # verbose / simplified output
    "VERBOSE": False,
    "PRINT_ERROR": False,
}

NETWORK_CONFIG = {
    # proxy setting
    #   you should customize your proxy setting accordingly
    #   default is for clash
    "PROXY": {"https": "127.0.0.1:7890"},
    # common request header
    "HEADER": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    },
}

USER_CONFIG = {
    # user id
    #   access your pixiv user profile to find this
    #   e.g. https://www.pixiv.net/users/xxxx
    "USER_ID": "22821761",
    "COOKIE": "TODO",
}


DOWNLOAD_CONFIG = {
    # image save path
    #   NOTE: DO NOT miss "/"
    "STORE_PATH": "images/",
    # abort request / download
    #   after 10 unsuccessful attempts
    "N_TIMES": 10,
    # need tag ?
    "WITH_TAG": True,
    # waiting time (s) after failure
    "FAIL_DELAY": 1,
    # max parallel thread number
    "N_THREAD": 12,
    # waiting time (s) after thread start
    "THREAD_DELAY": 1,
}
