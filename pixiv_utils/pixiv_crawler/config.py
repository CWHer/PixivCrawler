import dataclasses
import datetime
import pprint
from typing import Dict, Tuple

from .utils import printInfo


@dataclasses.dataclass
class RankingConfig:
    # Start date
    start_date: datetime.date = datetime.date(2022, 8, 1)
    # Date range: [start, start + range - 1]
    range: int = 1
    # Which ranking list
    ranking_modes: Tuple = (
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
    )
    mode: str = "daily"  # Choose from the above
    # Illustration, manga, ugoira, all
    content_modes: Tuple = ("all", "illust", "manga", "ugoira")
    content_mode: str = "all"  # Choose from the above
    # Download top k in each ranking
    num_artwork: int = 50

    def __post_init__(self):
        assert self.mode in self.ranking_modes, f"Mode {self.mode} not supported"
        assert (
            self.content_mode in self.content_modes
        ), f"Content mode {self.content_mode} not supported"


@dataclasses.dataclass
class DebugConfig:
    # Whether to print verbose debug information
    verbose: bool = False
    # Whether to print error information
    show_error: bool = False


@dataclasses.dataclass
class NetworkConfig:
    # Proxy setting, you should customize your proxy setting accordingly. Default is for clash
    proxy: Dict = dataclasses.field(default_factory=lambda: {"https": "127.0.0.1:7890"})
    # Common request header
    headers: Dict = dataclasses.field(
        default_factory=lambda: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
    )


@dataclasses.dataclass
class UserConfig:
    # Access your pixiv user profile to find this, e.g. https://www.pixiv.net/users/xxxx
    user_id: str = ""
    # Your cookie, you can find it in the browser developer tool (README for more details)
    cookie: str = ""


@dataclasses.dataclass
class DownloadConfig:
    timeout: float = 4  # Timeout for requests
    retry_times: int = 10  # Retry times for requests
    fail_delay: float = 1  # Waiting time (s) after failure
    store_path: str = "images"  # Image save path
    with_tag: bool = True  # Whether to download tags to a separate json file
    url_only: bool = False  # Only download artwork urls
    num_threads: int = 12  # Number of parallel threads
    thread_delay: float = 1  # Waiting time (s) after thread start


ranking_config = RankingConfig()
debug_config = DebugConfig()
network_config = NetworkConfig()
user_config = UserConfig()
download_config = DownloadConfig()


def displayAllConfig():
    infos = {
        "Ranking Config": dataclasses.asdict(ranking_config),
        "Debug Config": debug_config,
        "Network Config": network_config,
        "User Config": user_config,
        "Download Config": download_config,
    }
    for key, value in infos.items():
        printInfo(key + ":")
        pprint.pprint(value)
    print()
