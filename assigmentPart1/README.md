
Part 1: Square Program and process sync semaphores

Objective

The goal of this part is to compute the square of a large list of numbers using different parallel processing techniques and compare their performance. The following methods were implemented and tested:

Sequential Execution: A simple for loop to compute squares one at a time.
Multiprocessing Pool with map(): A pool of worker processes to compute squares in parallel.
Concurrent.futures ProcessPoolExecutor (Synchronous): Using executor.map() for synchronous parallel execution.
Concurrent.futures ProcessPoolExecutor (Asynchronous): Using executor.submit() for asynchronous parallel execution.
Implementation

The squareFunction.py file contains the implementation of the square function and the run_tests function, which generates a list of random numbers and times the execution of each method. The results are printed and returned as a dictionary.

Key Functions: 

square(n): Computes the square of a number.
run_tests(number_count): Generates a list of random numbers and times the execution of each parallel processing method.
test_run(): Runs the tests with 10^6 numbers and prints the results.
Observations

Sequential Execution: This is the simplest approach but is generally the slowest because it processes one number at a time.
Multiprocessing Pool with map(): This method is faster than sequential execution because it distributes the workload across multiple processes. However, there is some overhead in creating and managing the pool.
Concurrent.futures ProcessPoolExecutor (Synchronous): This method is efficient and easy to use. It performs similarly to the multiprocessing pool with map() but requires less code.
Concurrent.futures ProcessPoolExecutor (Asynchronous): This method is slightly slower than the synchronous version due to the overhead of managing futures and collecting results asynchronously.
Conclusion

Best Performance: The concurrent.futures ProcessPoolExecutor (synchronous) is the most efficient and easiest to use for parallel processing tasks.
Overhead: Multiprocessing introduces some overhead, so it is most beneficial for large datasets or computationally intensive tasks.
