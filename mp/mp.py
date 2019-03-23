from multiprocessing import Process, Manager
from queue import Queue
import psutil
from task import sorter, random, generate_data
import time


class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.process_ram = 0

    def memory_test(self, func, data):
        return_dict = Manager().dict()
        proc = Process(target=func, args=(data,))
        proc.start()
        proc1 = Process(target=self.max_ram, args=(proc.pid, return_dict))
        proc1.start()
        proc.join()
        proc1.join()
        self.process_ram = return_dict['process_ram']

    def max_ram(self, pid, return_dict):
        max_ram = 0
        try:
            while psutil.pid_exists(pid):
                result = psutil.Process(pid).memory_info().rss / 2 ** 20
                if result > max_ram:
                    max_ram = result
        except psutil.NoSuchProcess:
            pass
        return_dict['process_ram'] = max_ram

    def map(self, func, bid_data):
        self.memory_test(func, bid_data.get())
        print(f"The process takes {self.process_ram} MB")
        process_amount = int(self.mem_usage / self.process_ram)
        procs = []
        if process_amount > self.max_workers:
            process_amount = self.max_workers
        elif process_amount < self.min_workers:
            raise Exception('Not enough RAM')
        print(f"Max amount of workers = {process_amount}")

        start_time = time.perf_counter()

        for _ in range(process_amount):
            proc = Process(target=func, args=(bid_data.get(),))
            procs.append(proc)
            proc.start()
        while not bid_data.empty():
            for idx, proc in enumerate(procs):
                if not proc.is_alive():
                    if bid_data.empty():
                        break
                    new_proc = Process(target=func, args=(bid_data.get(),))
                    new_proc.start()
                    procs[idx] = new_proc
        for proc in procs:
            proc.join()

        time_need = time.perf_counter() - start_time
        print(f"Time need: {time_need} sec")
        return process_amount, self.process_ram

if __name__ == '__main__':
	q = generate_data()
	result = ProcessPool()
	pool = result.map(sorter, q)
	