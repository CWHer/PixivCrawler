import time
from typing import Callable, Dict, Iterable, Optional

import requests
from config import debug_config, download_config, network_config
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
    headers = network_config.header
    if additional_headers is not None:
        headers.update(additional_headers)

    if debug_config.verbose:
        printInfo(f"Collecting {url}")
    time.sleep(download_config.thread_delay)

    for i in range(download_config.retry_times):
        try:
            response = requests.get(
                url, headers=headers, proxies=network_config.proxy, timeout=network_config.timeout
            )

            if response.status_code == requests.status_codes.codes.ok:
                id_group = selector(response)
                if debug_config.verbose:
                    printInfo(f"{url} complete")
                return id_group

        except Exception as e:
            assertWarn(not debug_config.show_error, e)
            assertWarn(not debug_config.show_error, f"This is {i} attempt to collect {url}")

            time.sleep(download_config.fail_delay)

    assertWarn(not debug_config.show_error, f"Fail to collect {url}")
    writeFailLog(f"Fail to collect {url}.")
