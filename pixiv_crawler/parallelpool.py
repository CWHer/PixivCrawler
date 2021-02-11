# naive parallel pool
# use a list to store threads
import threading
from settings import MAX_THREADS
from utils import print_bar


class ParallelPool():
    def __init__(self, total_num: int, flow: float = None):
        self.pool = []
        self.__finish_count = 0
        self.__total_num = total_num
        self.flow = flow

    def empty(self):
        return self.size() == 0

    def full(self):
        return self.size() >= MAX_THREADS

    def size(self):
        return len(self.pool)

    # add new Thread
    def add(self, item: threading.Thread):
        self.pool.append(item)
        self.pool[-1].start()

    # a generator of finished items
    def finished_item(self):
        idx = 0
        while idx < self.size():
            item = self.pool[idx]
            if not item.isAlive():
                yield item
                self.pool.remove(item)
                self.__finish_count += 1
                print_bar(self.__finish_count, self.__total_num, self.flow)
                continue
            idx += 1

    # wait until all items complete
    def wait(self):
        for item in self.pool:
            item.join()
