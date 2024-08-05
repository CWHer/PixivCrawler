# Pixiv Utils

## 关于

`Pixiv Utils` 使用 `Python`实现，包含`Pixiv`爬虫以及马赛克拼图，支持排行榜、个人收藏、画师作品、关键词搜索等筛选功能，并提供高性能的多线程并行下载。

运行示例，正常速度，

![](./assets/procedure.gif)

## 功能

- **Pixiv 爬虫**

  - 每日/月/年的不同排行榜

  - 个人收藏

  - 特定画师的作品

  - 特定关键词的作品（支持高级关键词搜索，例如`(Lucy OR 边缘行者) AND (5000users OR 10000users)`）

  - 多线程并行下载

- **马赛克拼图**

  ![](./assets/mixture.png)

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install pixiv-utils
```

### 从源码安装

```bash
git clone git@github.com:CWHer/PixivCrawler.git
pip install -v .
```

## 快速开始

请参考[教程](./tutorial.py)以获取全面的指导。

注意：此部分仅包含**Pixiv 爬虫**的使用。马赛克拼图的使用请参考[马赛克拼图文档](./docs/IMAGE_MIX.md)。

```python
import datetime

from pixiv_utils.pixiv_crawler import (
    RankingCrawler,
    checkDir,
    displayAllConfig,
    download_config,
    network_config,
    ranking_config,
    user_config,
)

if __name__ == "__main__":
    network_config.proxy["https"] = "127.0.0.1:7890"
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False
    ranking_config.start_date = datetime.date(2024, 5, 1)
    ranking_config.range = 2
    ranking_config.mode = "weekly"
    ranking_config.content_mode = "illust"
    ranking_config.num_artwork = 50

    displayAllConfig()
    checkDir(download_config.store_path)

    app = RankingCrawler(capacity=200)
    app.run()
```

### 了解配置

配置文件位于[`config.py`](./pixiv_utils/config.py)，其中包含几个可能需要修改的项目，用 :warning: 表示。你可以简单地导入这些配置，像上面的例子一样修改它们，然后使用 `displayAllConfig()` 检查它们是否正确。

- `RankingConfig`

  ```python
  import ranking_config from pixiv_utils.pixiv_crawler
  ```

  **注意：** 该配置仅在下载排行榜时激活。

  - `ranking_config.start_date: datetime.date`： 排行榜的开始日期 :warning：

  - `ranking_config.range: int`： 排行榜的日期范围 :warning: `[start, start + range - 1]`。

  - `ranking_config.mode: str`： 排行榜的类型 :warning: ，可以从以下选项中选择

    ```python
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
    ```

  - `ranking_config.content_mode: str`： 排行榜中的内容类型 :warning:，可从以下选项中选择

    ```python
    content_modes: Tuple = ("all", "illust", "manga", "ugoira")
    ```

  - `ranking_config.num_artwork: int`: 每个排行榜中要下载的作品数量 :warning：

- `NetworkConfig`

  ```python
  import network_config from pixiv_utils.pixiv_crawler
  ```

  - ``network_config.proxy： Dict`： 代理配置 :warning：

    ```python
    # For example, to turn off the proxy
    network_config.proxy["https"] = ""
    ```

    默认 `proxy["https"]` 值为 `127.0.0.1:7890`，即 clash 的默认代理端口，需要根据实际的代理设置进行变更。**如果您使用的是普通 VPN 或无需代理，请将 https 属性置为""。**

  - `network_config.headers： Dict`： 请求中使用的标头。

- `UserConfig`

  ```python
  import user_config from pixiv_utils.pixiv_crawler
  ```

  **注意：** 下载个人书签或 R18 内容时，需要填写用户配置。

  - `user_config.user_id: str`： Pixiv 账户的用户 ID :warning:。您可以在个人资料页面的 URL 中找到它，即 `https://www.pixiv.net/users/{UID}`。

  - `user_config.cookie: str`： Pixiv 帐户的 cookie :warning：

    1. 打开浏览器的 `DevTools`（通常为 F12），切换到 `Network` 选项卡。

    2. 访问排名列表并刷新页面。在`DevTools`中找到`ranking.php`。

    ![](./assets/cookie.png)

    将 `cookie:` 后面的所有字符（如红框所示）复制到 `COOKIE` 配置中

- `DownloadConfig`

  ```python
  import download_config from pixiv_utils.pixiv_crawler
  ```

  - `download_config.timeout: float`： 请求的超时时间。

  - `download_config.retry_times: int`： 请求失败后的重试次数。

  - `download_config.fail_delay：float`： 请求失败后的延迟时间。

  - `download_config.store_path: str`： 存储下载图像的路径 :warning：

  - `download_config.with_tag: bool`： 是否将图片标签下载到 `tags.json` 中：

  - `download_config.num_threads: int`： 并行下载的线程数 :warning：

  - `download_config.thread_delay: float`： 每个线程启动的延迟时间。

- `DebugConfig`

  ```python
  import debug_config from pixiv_utils.pixiv_crawler
  ```

  - `debug_config.verbose: bool`： 是否打印调试信息。

  - `debug_config.show_error: bool`： 是否打印详细的错误信息。

### 创建爬虫实例

- `RankingCrawler`: 下载排行榜作品

  ```python
  """
  Download artworks from rankings

  NOTE: Require cookie for R18 images!

  Args:
      capacity (int): flow capacity, default is 1024MB
  """
  app = RankingCrawler(capacity=200)
  app.run()
  ```

- `BookmarkCrawler`: 下载个人公开收藏的作品

  ```python
  """
  Download artworks from public bookmarks

  NOTE: Require cookie!

  Args:
      n_images (int): max download number, default is 200
      capacity (int): flow capacity, default is 1024MB
  """
  app = BookmarkCrawler(n_images=20, capacity=200)
  app.run()
  ```

- `UserCrawler`: 下载某位画师的作品

  ```python
  """
  Download artworks from a single artist

  NOTE: Require cookie for R18 images!

  Args:
      artist_id (str): artist id
      capacity (int): flow capacity, default is 1024MB
  """
  app = UserCrawler(artist_id="32548944", capacity=200)
  app.run()
  ```

- `KeywordCrawler`: 下载某个关键词的作品

  **注意：** 按照热门度排序需要 `premium` 账户。

  ```python
  """
  Download search results of a keyword (sorted by popularity if order=True)
  Support advanced search, e.g. "(Lucy OR 边缘行者) AND (5000users OR 10000users)", refer to https://www.pixiv.help/hc/en-us/articles/235646387-I-would-like-to-know-how-to-search-for-content-on-pixiv

  NOTE: Require cookie for R18 images!
  NOTE: Require premium account for popularity sorting!

  Args:
      keyword (str): search keyword
      order (bool): order by popularity or not, default is False
      mode (str): content mode, default is "safe", support ["safe", "r18", "all"]
      n_images (int): max download number, default is 200
      capacity (int): flow capacity, default is 1024MB
  """
  app = KeywordCrawler(
      keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
      order=False,
      mode=["safe", "r18", "all"][-1],
      n_images=20,
      capacity=200,
  )
  app.run()
  ```

### 运行

运行脚本即可 :laughing:

### 提示

- `COOKIE` 过期时间相对较长，可在几天内重复使用。

- 使用 `displayAllConfig()` 显示所有配置并检查它们是否正确。

### 文档

- [Tutorial](./tutorial.py)： Pixiv 爬虫快速入门教程

- [Configuration](./pixiv_utils/pixiv_crawler/config.py)： 配置 Pixiv 爬虫

- [Pixiv Crawler](./docs/PIXIV_CRAWLER.md)： Pixiv 爬虫的详细说明

- [Mosaic Puzzles](./docs/IMAGE_MIX.md)： 马赛克拼图的详细说明
