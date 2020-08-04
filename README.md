# Pixiv crawler

一个pixiv的爬虫

~~本来是想用scrapy写的，奈何太高级了用不来~~

[TOC]

#### 部署方法

#### 基本功能

`to do`

- [x] ~~模拟登录~~

  使用selenium抓取已登录的cookies

- [ ] cookies

- [ ] 爬取pixiv第一张图片

- [ ] 热榜

- [ ] 个人收藏

- [ ] 关注

- [ ] 画师搜索

- [ ] 标签搜索

- [ ] 多线程

- [ ] 流量控制

- [ ] 数据库构建

- [ ] cookies池

- [ ] proxy池

#### 主要模块

`main.py`

`login.py`：使用selenium抓取已登录的cookies并保存在cookies.json

`ranking_crawler.py`

`bookmark_crawler.py`

`downloader.py`

`settings.json`