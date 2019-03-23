import random
from queue import Queue

def sorter(*args, **kwargs):
    array = [random.randint(0, 100) for _ in range(1000000)]
    array.sort()
    

def generate_data(len_q = 300, len_list = 700):
        q = Queue()
        for _ in range(len_q):
            array = [random.randint(0, 1) for _ in range(len_list)]
            q.put(array)
        return q

