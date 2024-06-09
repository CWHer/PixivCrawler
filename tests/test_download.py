from downloader.downloader import Downloader

image_url = "https://i.pximg.net/img-original/" + "img/2022/05/11/00/00/12/98259515_p0.jpg"
# downloadImage(url=image_url)

downloader = Downloader(capacity=1024)
downloader.add((image_url,))
print(downloader.download())
