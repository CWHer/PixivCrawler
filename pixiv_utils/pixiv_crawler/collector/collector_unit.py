import time
from typing import Callable, Dict, Iterable, Optional

import requests
from config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG
from utils import assertWarn, printInfo, writeFailLog


def collect(
    url: str, selector: Callable, additional_headers: Optional[Dict]
) -> Optional[Iterable[str]]:
    """
    Collect metadata from the specified URL.
    NOTE: This function is used to collect metadata from templates such as user.json, page.json, etc.
    Different selectors can be used to select different elements.

    Args:
        args (Tuple[str, Callable, Optional[Dict]]): A tuple containing the URL, a selector function, and additional headers.

    """
    headers = NETWORK_CONFIG["HEADER"]
    if additional_headers is not None:
        headers.update(additional_headers)

    verbose_output = OUTPUT_CONFIG["VERBOSE"]
    error_output = OUTPUT_CONFIG["PRINT_ERROR"]
    if verbose_output:
        printInfo(f"Collecting {url}")
    time.sleep(DOWNLOAD_CONFIG["THREAD_DELAY"])

    for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
        try:
            response = requests.get(
                url, headers=headers, proxies=NETWORK_CONFIG["PROXY"], timeout=4
            )

            if response.status_code == requests.status_codes.codes.ok:
                id_group = selector(response)
                if verbose_output:
                    printInfo(f"{url} complete")
                return id_group

        except Exception as e:
            assertWarn(not error_output, e)
            assertWarn(not error_output, f"This is {i} attempt to collect {url}")

            time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

    assertWarn(not error_output, f"Fail to collect {url}")
    writeFailLog(f"Fail to collect {url}.")
