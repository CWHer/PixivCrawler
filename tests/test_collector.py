from collector.collector import Collector
from downloader.downloader import Downloader

downloader = Downloader(capacity=1024)
collector = Collector(downloader)
collector.add(("89362167", "85275328"))
collector.collect()
