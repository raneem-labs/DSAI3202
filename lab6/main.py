from mpi4py import MPI
import socket
import numpy as np

def run_square_simulation():
    def square(n, rank):
        print(f"rank {rank} calculating square of {n}")
        return n**2

    def parallel_square(n):
        comm = MPI.COMM_WORLD 
        rank = comm.Get_rank()
        size = comm.Get_size()
        host_name = socket.gethostname()

        chunk_size = n // size
        start = rank * chunk_size + 1
        end = start + chunk_size if rank != size - 1 else n + 1

        print(f"Process {rank} on {host_name} is getting squares from {start} to {end}...")
        local_squares = [square(i, rank) for i in range(start, end)]

        all_squares = comm.gather(local_squares, root=0)
        print()
        if rank == 0:
            result = [item for sublist in all_squares for item in sublist]
            print("Squares from 1 to", n)
            print(result)

    n = 100
    parallel_square(n)

def run_virus_simulation():
    def spread_virus(population, spread_chance, vaccination_rate):
        new_population = population.copy()
        for i in range(len(population)):
            if population[i] == 1:
                for j in range(len(population)):
                    if population[j] == 0 and np.random.rand() < spread_chance and np.random.rand() > vaccination_rate:
                        new_population[j] = 1
        return new_population

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    population_size = 100
    spread_chance = 0.3
    vaccination_rate = np.random.uniform(0.1, 0.5)

    population = np.zeros(population_size, dtype=int)
    if rank == 0:
        infected_indices = np.random.choice(population_size, int(0.1 * population_size), replace=False)
        population[infected_indices] = 1

    num_steps = 10
    for step in range(num_steps):
        population = spread_virus(population, spread_chance, vaccination_rate)
        
        if rank != 0:
            comm.send(population, dest=0, tag=rank)
        else:
            populations = [population]
            for source_rank in range(1, size):
                populations.append(comm.recv(source=source_rank, tag=source_rank))
            combined_population = np.concatenate(populations)
            infected_count = np.sum(combined_population == 1)
            print(f"Step {step + 1}: {infected_count} infected individuals across all processes.")

if __name__ == "__main__":
    # Choose which simulation to run
    simulation = "virus"  # Change to "square" if you want the other one

    if simulation == "square":
        run_square_simulation()
    elif simulation == "virus":
        run_virus_simulation()
    else:
        print("Invalid simulation choice!")
