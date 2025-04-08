from mpi4py import MPI
import socket

def square(n,rank): 
    print(f"rank {rank} calculating square of {n}")
    return n**2

def parallel_square(n):
    comm = MPI.COMM_WORLD 
    rank = comm.Get_rank()
    size= comm.Get_size()
    host_name= socket.gethostname()


    chunk_size = n // size
    start = rank * chunk_size + 1
    end = start + chunk_size if rank != size - 1 else n + 1

    print(f"Process {rank} on {host_name} is getting squares from {start} to  {end}...")
    local_squares = [square(i,rank) for i in range(start, end)]

    all_squares = comm.gather(local_squares, root=0)
    print()
    if rank == 0:
        # Flatten the list of squares
        result = [item for sublist in all_squares for item in sublist]
        print("Squares from 1 to", n)
        print(result)

if __name__ == "__main__":
    n = 100  # Example number
    parallel_square(n)
