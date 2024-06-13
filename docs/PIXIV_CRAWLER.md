# Pixiv Crawler

This document mainly describes the design of the **Pixiv crawler**, yet may be outdated.

## Design

- Notations

  - `artwork_id`: "93172108"

  - `artwork_url`: "https://www.pixiv.net/artworks/93172108"

    Each `artwork` may contain multiple images.

  - `image_url`: "https://i.pximg.net/img-original/img/2021/10/02/18/47/29/93172108_p1.jpg"

- Pipeline design

  Collect `artwork url`, `image url` in different stages, and pass them to the next stage.

- High modularity and low coupling

  For example, if you already have `image url` (e.g., use with [Pxer](https://github.com/FoXZilla/Pxer)), you can consider passing it directly to the `downloader` for downloading.

- Modules

  ```mermaid
  graph LR;
      F[Start]-->A;
      A<==Run parallel==>A;
      A[Crawler]--Send artwork_url-->B[Collector];
      B<==Run parallel==>B;
      B--Send image url-->D[Downloader];
      D==Run parallel==>D;
      D-->E[End];
  ```

  ```
  pixiv_crawler
  │   config.py
  │   utils.py
  │
  ├───collector
  │   │   collector.py
  │   │   collector_unit.py
  │   └───selectors.py
  │
  ├───crawlers
  │   │   bookmark_crawler.py
  │   │   keyword_crawler.py
  │   │   ranking_crawler.py
  │   └───users_crawler.py
  │
  └───downloader
      │   downloader.py
      └───download_image.py
  ```

  - `collector/collector_unit.py`: Collect `artwork_url` and `image_url`.

    Passing different `selectors` to select different data.

  - `collector/selectors.py`: Functions for selecting different data from json or html.

  - `crawlers/*`: Implement different crawlers for different purposes.

  - `downloader/downloader_image.py`: Download images from `image_url`.

## Appendix

- `pixiv.net/robots.txt`

  ```
  User-agent: *
  Disallow: /cdn-cgi/
  Disallow: /rpc/index.php?mode=profile_module_illusts&user_id=*&illust_id=*
  Disallow: /ajax/illust/*/recommend/init
  Disallow: *return_to*
  Disallow: /?return_to=
  Disallow: /login.php?return_to=
  Disallow: /index.php?return_to=

  Disallow: /artworks/unlisted/*

  Disallow: /users/*/followers
  Disallow: /users/*/mypixiv
  Disallow: /users/*/bookmarks
  Disallow: /novel/comments.php?id=
  Disallow: /novels/unlisted/*

  Disallow: /en/group

  Disallow: /en/search/

  Disallow: /en/users/*/followers
  Disallow: /en/users/*/mypixiv
  Disallow: /en/users/*/bookmarks
  Disallow: /en/novel/comments.php?id=

  Disallow: /fanbox/search
  Disallow: /fanbox/tag

  Allow: /comic-indies/$
  Allow: /comic-indies/about
  Disallow: /comic-indies/
  ```
