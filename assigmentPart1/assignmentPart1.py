import time
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# Function to compute the square of a number
def square(n):
    """
    This function takes a number and returns its square.

    Args:
        n (int): The number to be squared.

    Returns:
        int: The square of the input number.
    """
    return n ** 2

# Function to run the tests and time the execution of different parallel processing methods
def run_tests(number_count):
    """
    This function generates a list of random numbers, and times the execution
    of four different methods to compute the square of each number:
    1. Sequential for loop
    2. Multiprocessing pool with map()
    3. Concurrent.futures ProcessPoolExecutor (Synchronous)
    4. Concurrent.futures ProcessPoolExecutor (Asynchronous)
    
    Args:
        number_count (int): The number of random numbers to generate and square.

    Returns:
        dict: A dictionary containing the execution times for each method.
    """
    
    # Generate a list of random numbers to test the square function
    numbers = [random.randint(1, 100) for _ in range(number_count)]

    # Measure time for sequential for loop
    start_time = time.time()
    results_sequential = [square(n) for n in numbers]
    sequential_time = time.time() - start_time
    print(f"Sequential for loop time: {sequential_time:.6f} seconds")

    # Measure time for multiprocessing pool with map
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        results_map = pool.map(square, numbers)
    multiprocessing_pool_map_time = time.time() - start_time
    print(f"Multiprocessing pool with map() time: {multiprocessing_pool_map_time:.6f} seconds")

    # Measure time for concurrent.futures ProcessPoolExecutor (Synchronous)
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results_executor_sync = list(executor.map(square, numbers))
    concurrent_executor_sync_time = time.time() - start_time
    print(f"Concurrent.futures ProcessPoolExecutor (Synchronous) time: {concurrent_executor_sync_time:.6f} seconds")

    # Measure time for concurrent.futures ProcessPoolExecutor (Asynchronous)
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        # Submit tasks asynchronously
        futures = [executor.submit(square, n) for n in numbers]
        results_executor_async = [f.result() for f in futures]  # Collect results
    concurrent_executor_async_time = time.time() - start_time
    print(f"Concurrent.futures ProcessPoolExecutor (Asynchronous) time: {concurrent_executor_async_time:.6f} seconds")

    # Return a dictionary of execution times for each method
    return {
        "sequential_time": sequential_time,
        "multiprocessing_pool_map_time": multiprocessing_pool_map_time,
        "concurrent_executor_sync_time": concurrent_executor_sync_time,
        "concurrent_executor_async_time": concurrent_executor_async_time,
    }

# Function to test and run the performance with different input sizes
def test_run():
    """
    This function runs the tests with  (10^6  )
    and prints the results .

    The test will input sizes to demonstrate the performance
    of sequential and parallel processing methods.
    """
    # Run the test with 10^6 numbers
    print("Testing with 10^6 numbers:")
    results_1M = run_tests(10**6)  # Run the tests with 1 million numbers
    print("\nResults for 10^6 numbers:", results_1M)
    
 

# Main entry point of the program
if __name__ == "__main__":
    """
    This block runs the tests with input sizes (10^6 numbers).
    It prints the results showing the execution times for each method.
    """
    test_run()



    





