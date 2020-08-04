# Pixiv crawler

一个pixiv的爬虫

~~本来是想用scrapy写的，奈何太高级了用不来~~

[TOC]

#### 部署方法

##### 1.安装依赖库

- request

  `pip install requests`

- selenium

  `pip install selenium`

- chrome driver

  下载地址[Link](http://npm.taobao.org/mirrors/chromedriver/)，下载chrome对映的版本

  在windows环境建议直接把chromedriver.exe放入python的scripts目录

##### 2.运行

##### 3.注意事项:warning::warning::warning:

- 确保chrome已经登录pixiv.net

  login模块使用selenium模拟chrome抓取cookies

- 在运行login模块时需要关闭所有chrome窗口

- 需要手动检查cookies.json是否为空

  selenium模块处理状态码比较困难

  没有很好的办法判断网页是请求成功，还是无法访问，而且这里不会报错

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