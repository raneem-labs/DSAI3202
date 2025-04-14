from mpi4py import MPI
import numpy as np

# Step 4: Implement Virus Spread Function
def spread_virus(population, spread_chance, vaccination_rate):
    new_population = population.copy()  # Copy the population to avoid modifying it while iterating
    for i in range(len(population)):
        # If the person is infected, try to infect others
        if population[i] == 1:
            for j in range(len(population)):
                if population[j] == 0 and np.random.rand() < spread_chance and np.random.rand() > vaccination_rate:
                    new_population[j] = 1  # Infect the uninfected person
    return new_population


# Step 1: Initialize the MPI Environment
comm = MPI.COMM_WORLD  # Initialize the MPI communicator
rank = comm.Get_rank()  # Rank (ID) of the current process
size = comm.Get_size()  # Total number of processes

# Step 2: Define Parameters
population_size = 100  # Size of the population in the simulation
spread_chance = 0.3  # Chance of virus spreading to others
vaccination_rate = np.random.uniform(0.1, 0.5)  # Random vaccination rate for each process

# Step 3: Initialize the Population
population = np.zeros(population_size, dtype=int)  # Initialize the population with zeros (uninfected)

# Randomly infect a small percentage of individuals (e.g., 10%)
if rank == 0:  # Only root process will initialize the infection
    infected_indices = np.random.choice(population_size, int(0.1 * population_size), replace=False)
    population[infected_indices] = 1  # Mark infected individuals with 1


# Step 5: Simulate Virus Spread
num_steps = 10  # Number of time steps to run the simulation
for step in range(num_steps):
    # Spread the virus based on current population
    population = spread_virus(population, spread_chance, vaccination_rate)
    
    # If the process is not the root (rank != 0), send its population to rank 0
    if rank != 0:
        comm.send(population, dest=0, tag=rank)
    
    # If the process is rank 0, gather data from other processes
    if rank == 0:
        # Collect population data from all processes
        populations = [population]  # Start with the population from rank 0
        for source_rank in range(1, size):
            populations.append(comm.recv(source=source_rank, tag=source_rank))
        
        # Combine all populations (this could be adjusted based on how you want to aggregate the data)
        combined_population = np.concatenate(populations)
        
        # Optionally, print the status of the population at each step
        infected_count = np.sum(combined_population == 1)
        print(f"Step {step + 1}: {infected_count} infected individuals across all processes.")
