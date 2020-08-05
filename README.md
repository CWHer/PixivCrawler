# Pixiv crawler

一个pixiv的爬虫

~~本来是想用scrapy写的，奈何太高级了用不来~~

[TOC]

### 部署方法

Windows限定，~~不保证在其它平台可以使用~~

#### 1.安装依赖库

总之少哪个装哪个

- request

  `pip install requests`

- selenium

  `pip install selenium`

- chrome driver

  下载地址[Link](http://npm.taobao.org/mirrors/chromedriver/)，下载chrome对映的版本

  在windows环境建议直接把chromedriver.exe放入python的scripts目录

#### 2.运行

0. `settings.py`的设置

   > 这里没提到的都不用改
   >
   > `USER_ID`:warning:: 这里改成自己的uid，在profile页面的url里可以找到
   >
   > `name/password`:warning::
   >
   > ​	在同目录下新建一个userdata.json，填入以下内容
   >
   > ​	其实这块目前好像用不上，~~但是先留着看看...~~
   >
   > ​	运行时载入成功会有'load userdata.json successfully!'反馈
   >
   > ```json
   > {
   >     "name":"xxxx",
   >     "password":""
   > }
   > ```
   >
   > `FAIL_TIMES`: 失败后尝试请求次数
   >
   > `DOWNLOAD_DELAY`: 下载延迟
   >
   > `IMAGES_STORE_PATH`: 图片保存目录，相对路径
   >
   > `START_DATE/DOMAIN`:warning:: 抓取排行榜开始日期与范围
   >
   > `PIXIV_MODE`:warning:: 设置排行榜类型
   >
   > `ARTWORKS_PER`:warning:: 榜的前x幅作品
   >
   > `PROXIES`:warning:: 填入自己的proxy设置，ss/ssr默认设置的话无需改动​ 
   >
   > `USER_DATA_DIR`:warning:: chrome个人配置的目录，用于login是调整chrome设置
   >
   > ​	一般来说是'C:\\Users\\xxxxx\\AppData\\Local\\Google\\Chrome\\User Data'

1. 获取cookies

   使用`login.py`，运行Login().login()

   ```python
   from login import Login
   Login().login()
   ```

   运行一次即可，保存在cookie.json

   务必先阅读注意事项1-4

2. 排行榜的抓取

   见当前的`main.py`，需要提前配置好`settings.py`

#### 3.注意事项:warning::warning::warning:

1. 确保chrome已经登录pixiv.net

   login模块使用selenium模拟chrome抓取cookies，会有弹窗

2. 在运行login模块时需要关闭所有chrome窗口

3. 需要手动检查cookies.json是否为空

   selenium模块处理状态码比较困难

   没有很好的办法判断网页是请求成功，还是无法访问，而且这里不会报错

4. cookies的过期时间很长

   基本上几天内用同一个cookie不会有大问题，等过期了再次抓取即可

### 基本功能

- [x] ~~模拟登录~~

  使用selenium抓取已登录的cookies

- [x] cookies

- [x] 爬取pixiv第一张图片

- [ ] proxy池

- [x] 多图 image_group

- [x] 排行榜 ranking_crawler

- [ ] 个人收藏

- [ ] 关注

- [ ] 画师搜索

- [ ] 标签搜索

- [x] 多线程

  image.py 现在使用了threading，现在每个page并发image.download

- [x] 流量控制

- [ ] 数据库构建

- [ ] cookies池

### 主要模块

- json sample

> `rank.json`:  ranking
>
> ​	request ".../ranking.php?p=1&format=json"
>
> ​	
>
> `page.json`: used in image_group.py
>
> ​	from ".../artworks/xxxx"
>
> ​	request "..../ajax/illust/xxxx"

- `settings.json`: 所有设置都在这里，见**部署方法**

- `login.py`:

​	无需传入参数 

​	使用selenium抓取已登录的cookies并保存在cookies.json

- `image.py`: 

​	传入类似"https://i.pximg.net/img-original/img/2020/08/02/02/55/48/83383450_p0.jpg"的url

​	图片类，提供下载方法，可以多线程执行

- `image_group.py`: 

​	传入illust_id和cookie，其中illust_id就是下面xxxx部分的数字

​	从".../artworks/xxxx"网页收集所有图片

- `main.py`

- `ranking_crawler.py`

​	需要传入cookie和capacity=1024

​	其中capacity为流量限制，默认1024MB，只计算图片大小而忽略request的一些占用	

​	爬取排行榜

- `bookmark_crawler.py`

