import os
import re
import time

import requests
from config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG
from utils import printError, printInfo, printWarn, writeFailLog


def downloadImage(url: str) -> float:
    """[summary]
    download image

    Returns: image size (MB)

    NOTE: url sample "https://i.pximg.net/
        img-original/img/2022/05/11/00/00/12/98259515_p0.jpg"
    """

    image_name = url[url.rfind("/") + 1:]
    result = re.search("/(\d+)_", url)
    printError(result is None, "bad url in image downloader")
    image_id = result.group(1)
    headers = {"Referer": f"https://www.pixiv.net/artworks/{image_id}"}
    headers.update(NETWORK_CONFIG["HEADER"])

    verbose_output = OUTPUT_CONFIG["VERBOSE"]
    error_output = OUTPUT_CONFIG["PRINT_ERROR"]
    if verbose_output:
        printInfo(f"downloading {image_name}")
    time.sleep(DOWNLOAD_CONFIG["THREAD_DELAY"])

    image_path = DOWNLOAD_CONFIG["STORE_PATH"] + image_name
    if os.path.exists(image_path):
        printWarn(verbose_output, f"{image_path} exists")
        return 0

    wait_time = 10
    for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
        try:
            response = requests.get(
                url, headers=headers,
                proxies=NETWORK_CONFIG["PROXY"],
                timeout=(4, wait_time))

            if response.status_code == 200:
                image_size = int(
                    response.headers["content-length"])
                # deletc incomplete image
                if len(response.content) != image_size:
                    time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])
                    wait_time += 2
                    continue

                with open(image_path, "wb") as f:
                    f.write(response.content)
                if verbose_output:
                    printInfo(f"{image_name} complete")
                return image_size / (1 << 20)

        except Exception as e:
            printWarn(error_output, e)
            printWarn(error_output,
                      f"This is {i} attempt to download {image_name}")

            time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

    printWarn(error_output, f"fail to download {image_name}")
    writeFailLog(f"fail to download {image_name} \n")
    return 0
