import time
import random
import multiprocessing

class ConnectionPool:
    """
    A class that simulates a pool of database connections, using a semaphore
    to manage access to the pool. It ensures that a limited number of connections
    can be accessed at any given time.

    Attributes:
        pool_size (int): The number of connections in the pool.
        semaphore (multiprocessing.Semaphore): A semaphore to limit access to the pool.
        connections (multiprocessing.Manager.list): A managed list representing the database connections.
    """
    def __init__(self, pool_size, manager):
        """
        Initializes the ConnectionPool with a given number of connections and a semaphore.

        Args:
            pool_size (int): The number of connections in the pool.
            manager (multiprocessing.Manager): The manager used to manage shared resources.
        """
        self.pool_size = pool_size
        self.semaphore = manager.Semaphore(pool_size)
        self.connections = manager.list([f"Connection {i+1}" for i in range(pool_size)])

    def get_connection(self):
        """
        Acquires a connection from the pool, limiting access using the semaphore.

        Returns:
            str: A connection from the pool.

        Raises:
            Exception: If no connections are available.
        """
        self.semaphore.acquire()  # Acquire the semaphore to ensure limited access
        if self.connections:
            connection = self.connections.pop()  # Pops the last connection
            print(f"Acquired: {connection}")
            return connection
        else:
            raise Exception("No available connections")

    def release_connection(self, connection):
        """
        Releases a connection back into the pool, signaling the semaphore.

        Args:
            connection (str): The connection to release back into the pool.
        """
        self.connections.append(connection)  # Add the connection back to the pool
        print(f"Released: {connection}")
        self.semaphore.release()  # Release the semaphore to allow another process to acquire a connection


def access_database(pool):
    """
    Simulates a process performing a database operation.

    This function:
    - Acquires a connection from the pool.
    - Prints a message indicating that it has the connection.
    - Sleeps for a random duration to simulate work.
    - Releases the connection and prints a message.

    Args:
        pool (ConnectionPool): The connection pool to get and release connections.
    """
    try:
        # Acquire a connection from the pool
        connection = pool.get_connection()
        # Simulate some work with the connection
        print(f"Using {connection} for a database operation...")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work by sleeping for a random time
        # Release the connection back into the pool
        pool.release_connection(connection)
    except Exception as e:
        print(f"Error: {e}")


def main():
    pool_size = 3  # Define the pool size (limited number of connections)
    manager = multiprocessing.Manager()
    pool = ConnectionPool(pool_size, manager)

    # Create a pool of processes that simulate performing database operations
    processes = []
    for i in range(5):  # Let's simulate 5 workers trying to access the database
        p = multiprocessing.Process(target=access_database, args=(pool,))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All processes have finished.")


if __name__ == "__main__":
    main()






