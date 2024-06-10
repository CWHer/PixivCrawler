import datetime

# TODO: something like gpc
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
    "PROXY": {"https": "192.168.124.10:7890"},
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
    # "COOKIE": "",
    "COOKIE": "first_visit_datetime_pc=2022-07-14+00%3A14%3A49; p_ab_id=5; p_ab_id_2=6; p_ab_d_id=523929040; yuid_b=OXc4glk; privacy_policy_notification=0; a_type=0; b_type=1; login_ever=yes; __utmz=235335808.1689250497.41.28.utmcsr=github.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=22821761=1^9=p_ab_id=5=1^10=p_ab_id_2=6=1^11=lang=zh=1; c_type=23; _gcl_au=1.1.962925723.1712045886; cc1=2024-06-09%2016%3A12%3A50; __cf_bm=zIPxWXC0i8dnGzXIP3FnwPRDL1dmARTRE3yV54ffsSM-1717917170-1.0.1.1-TilAje7PwAvVFFqG8NVVUr4mv.vcplOapZlfhTk7BkB7EQvXHo1dLO37f3jfimCku2yQ0mGi7A3Y6tzzOBMUNDrHYqjgIK3pHbgjkiU7Wd8; __utma=235335808.671812743.1657725304.1712045633.1717917173.44; __utmc=235335808; __utmt=1; cf_clearance=o1s1G6pTwG.RQ9K_eqrI..mT2WsBODsc4un5Q0c0kOc-1717917173-1.0.1.1-HzrP19bu8HVZeZYkX3.pLtTYukIp5Rh1iyw57H.pBn0dWToH4lKDDrh_NoNgHT6eEttlsI5QYjj.rwwQrT7CyQ; _ga=GA1.1.1175690.1657725304; PHPSESSID=22821761_coolaDAZ0TxnBu6Ehm06Lqf662oB9IzB; device_token=040a864d60c7ff1c74caca5fb0c3114a; _ga_MZ1NL4PHH0=GS1.1.1717917183.9.1.1717917456.0.0.0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; privacy_policy_agreement=7; _ga_75BBYNYN9J=GS1.1.1717917173.47.1.1717917476.0.0.0; __utmb=235335808.3.10.1717917173",
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
