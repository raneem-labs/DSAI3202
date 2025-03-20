
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


Process Synchronization with Semaphores

Objective

The goal of this part is to implement a ConnectionPool class that simulates a pool of database connections. A semaphore is used to limit access to the connections, ensuring that only a fixed number of processes can access the pool at any given time.

Implementation

The processSyncSemaphores.py file contains the implementation of the ConnectionPool class and the access_database function, which simulates a process performing a database operation.
Key Components

ConnectionPool Class:
__init__(pool_size, manager): Initializes the pool with a fixed number of connections and a semaphore.
get_connection(): Acquires a connection from the pool using the semaphore.

release_connection(connection): Releases a connection back into the pool and signals the semaphore.
access_database(pool): Simulates a process acquiring a connection, performing a database operation, and releasing the connection.
Results

The program creates multiple processes that attempt to access the connection pool simultaneously. The semaphore ensures that only a limited number of processes can access the pool at any given time, while the rest wait for a connection to become available.

Observations

Semaphore Behavior: When more processes try to access the pool than there are available connections, the semaphore blocks the excess processes until a connection is released.
Race Condition Prevention: The semaphore ensures that only one process can acquire a connection at a time, preventing race conditions and ensuring safe access to the shared resource (the connection pool).
Process Synchronization: The program demonstrates how semaphores can be used to manage access to a limited resource in a multiprocessing environment.

Conclusion

Semaphores: Semaphores are an effective way to manage access to shared resources in a multiprocessing environment. They ensure that only a limited number of processes can access the resource at any given time, preventing race conditions and ensuring safe access.
Scalability: This approach is scalable and can be extended to manage larger pools of resources or more complex synchronization scenarios.


