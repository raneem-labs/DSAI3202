# main.py
import time
from sequential import sequential_sum
from threading import parallel_sum_threaded
from multiprocessing import parallel_sum_multiprocessing

def main():
    # Define the large number N
    N = 10**6  # Example large number
    num_threads = 4  # Number of threads for parallel thread approach
    num_processes = 4  # Number of processes for parallel multiprocessing approach

    # Sequential Summation
    print("Sequential Summation:")
    start_time = time.time()
    total_sum = sequential_sum(N)
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sum: {total_sum}")
    print(f"Execution Time: {sequential_time} seconds\n")

    # Threaded Summation
    print("Threaded Summation:")
    start_time = time.time()
    total_sum_threaded = parallel_sum_threaded(N, num_threads)
    end_time = time.time()
    threaded_time = end_time - start_time
    print(f"Sum (Threaded): {total_sum_threaded}")
    print(f"Execution Time (Threaded): {threaded_time} seconds\n")

    # Multiprocessing Summation
    print("Multiprocessing Summation:")
    start_time = time.time()
    total_sum_multiprocessing = parallel_sum_multiprocessing(N, num_processes)
    end_time = time.time()
    multiprocessing_time = end_time - start_time
    print(f"Sum (Multiprocessing): {total_sum_multiprocessing}")
    print(f"Execution Time (Multiprocessing): {multiprocessing_time} seconds\n")

    # Performance comparison
    print("Performance Comparison:")
    print(f"Speedup (Threaded): {sequential_time / threaded_time}")
    print(f"Speedup (Multiprocessing): {sequential_time / multiprocessing_time}")
    print(f"Efficiency (Threaded): {sequential_time / threaded_time / num_threads}")
    print(f"Efficiency (Multiprocessing): {sequential_time / multiprocessing_time / num_processes}")

if __name__ == "__main__":
    main()
