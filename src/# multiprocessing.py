# multiprocessing.py
import multiprocessing

def process_sum(start, end, result, index):
    """Calculates sum for a process's range."""
    partial_sum = sum(range(start, end + 1))
    result[index] = partial_sum

def parallel_sum_multiprocessing(n, num_processes):
    """Calculates sum using multiprocessing."""
    processes = []
    result = multiprocessing.Array('i', num_processes)
    step = n // num_processes
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step if i != num_processes - 1 else n
        process = multiprocessing.Process(target=process_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return sum(result)
