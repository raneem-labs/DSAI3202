# threading.py
import threading

def thread_sum(start, end, result, index):
    """Calculates sum for a thread's range."""
    partial_sum = sum(range(start, end + 1))
    result[index] = partial_sum

def parallel_sum_threaded(n, num_threads):
    """Calculates sum using threading."""
    threads = []
    result = [0] * num_threads
    step = n // num_threads
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i != num_threads - 1 else n
        thread = threading.Thread(target=thread_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(result)

