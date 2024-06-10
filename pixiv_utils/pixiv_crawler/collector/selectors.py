import json
import re
from typing import List, Set

from bs4 import BeautifulSoup
from requests.models import Response

from pixiv_utils.pixiv_crawler.utils import writeFailLog


def selectTag(response: Response) -> List[str]:
    """
    Collect all tags from (artwork.html)
    Sample url: https://www.pixiv.net/artworks/xxxxxx

    Returns:
        List[str]: tags
    """
    result = re.search(r"artworks/(\d+)", response.url)
    assert result is not None, f"Bad response in selectTag for URL: {response.url}"

    illust_id = result.group(1)
    content = json.loads(
        BeautifulSoup(response.text, "html.parser").find(id="meta-preload-data").get("content")
    )

    return [
        tag["translation"]["en"] if "translation" in tag else tag["tag"]
        for tag in content["illust"][illust_id]["tags"]["tags"]
    ]


def selectPage(response: Response) -> Set[str]:
    """
    Collect all image urls from (page.json)
    Sample url: https://www.pixiv.net/ajax/illust/xxxx/pages?lang=zh

    Returns:
        Set[str]: urls
    """
    group = set()
    for url in response.json()["body"]:
        group.add(url["urls"]["original"])
    return group


def selectRanking(response: Response) -> Set[str]:
    """
    Collect all illust_id (image_id) from (ranking.json)
    Sample url: https://www.pixiv.net/ranking.php?mode=daily&date=20200801&p=1&format=json

    Returns:
        Set[str]: illust_id (image_id)
    """
    image_ids = [artwork["illust_id"] for artwork in response.json()["contents"]]
    return set(map(str, image_ids))


def selectUser(response: Response) -> Set[str]:
    """
    Collect all illust_id (image_id) from (user.json)
    Sample url: https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh

    Returns:
        Set[str]: illust_id (image_id)
    """
    return set(response.json()["body"]["illusts"].keys())


def selectBookmark(response: Response) -> Set[str]:
    """
    Collect all illust_id (image_id) from (bookmark.json)
    Sample url: https://www.pixiv.net/ajax/user/xxx/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh

    Returns:
        Set[str]: illust_id (image_id)
    """
    # NOTE: id of disabled artwork is int (not str)
    id_group: Set[str] = set()
    for artwork in response.json()["body"]["works"]:
        illust_id = artwork["id"]
        if isinstance(illust_id, str):
            id_group.add(artwork["id"])
        else:
            writeFailLog(f"Disabled artwork {illust_id}.")
    return id_group


def selectKeyword(response: Response) -> Set[str]:
    """
    Collect all illust_id (image_id) from (keyword.json)
    Sample url: https://www.pixiv.net/ajax/search/artworks/{xxxxx}?word={xxxxx}&order=popular_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"

    Returns:
        Set[str]: illust_id (image_id)
    """
    # NOTE: id of disable artwork is int (not str)
    id_group: Set[str] = set()
    for artwork in response.json()["body"]["illustManga"]["data"]:
        id_group.add(artwork["id"])
    return id_group
