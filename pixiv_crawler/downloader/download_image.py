import os
import re
import time

import requests
from config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG
from utils import assertError, assertWarn, printInfo, writeFailLog


def downloadImage(url: str, download_time: float = 10) -> float:
    """
    Download image from url

    Args:
        url (str): The URL of the image to download.
        download_time (float): The maximum time allowed for downloading the image. Defaults to 10.

    Returns:
        float: The size of the downloaded image in MB.

    NOTE: The URL should be in the format "https://i.pximg.net/img-original/img/2022/05/11/00/00/12/98259515_p0.jpg"
    """

    image_name = url[url.rfind("/") + 1 :]
    result = re.search(r"/(\d+)_", url)
    assertError(result is not None, "Bad url in image downloader")
    image_id = result.group(1)
    headers = {"Referer": f"https://www.pixiv.net/artworks/{image_id}"}
    headers.update(NETWORK_CONFIG["HEADER"])

    verbose_output = OUTPUT_CONFIG["VERBOSE"]
    error_output = OUTPUT_CONFIG["PRINT_ERROR"]
    if verbose_output:
        printInfo(f"downloading {image_name}")
    time.sleep(DOWNLOAD_CONFIG["THREAD_DELAY"])

    image_path = os.path.join(DOWNLOAD_CONFIG["STORE_PATH"], image_name)
    if os.path.exists(image_path):
        assertWarn(not verbose_output, f"{image_path} exists")
        return 0

    for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
        try:
            response = requests.get(
                url, headers=headers, proxies=NETWORK_CONFIG["PROXY"], timeout=(4, download_time)
            )

            if response.status_code == requests.status_codes.codes.ok:
                image_size = int(response.headers["content-length"])
                # detect incomplete image
                if len(response.content) != image_size:
                    time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])
                    download_time += 2
                    continue

                with open(image_path, "wb") as f:
                    f.write(response.content)
                if verbose_output:
                    printInfo(f"{image_name} complete")
                return image_size / 2**20

        except Exception as e:
            assertWarn(not error_output, e)
            assertWarn(not error_output, f"This is {i} attempt to download {image_name}")

            time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

    assertWarn(not error_output, f"Fail to download {image_name}")
    writeFailLog(f"Fail to download {image_name}.")
    return 0
