import numpy as np
import random
from mpi4py import MPI

def calculate_fitness(route, distance_matrix):
    """
    Calculate the total distance traveled by the car (fitness function).

    Parameters:
        - route (list): A list representing the order of nodes visited in the route.
        - distance_matrix (numpy.ndarray): A matrix of the distances between nodes.

    Returns:
        - float: The negative total distance traveled (to minimize the distance).
          Returns a large negative penalty if the route is infeasible.
    """
    num_cities = len(distance_matrix)
    if len(route) != num_cities:
        print(f"Error: Route length ({len(route)}) does not match the number of cities ({num_cities})")
        return -1e6  # Large negative penalty for invalid routes

    total_distance = 0
    
    for i in range(len(route) - 1):
        distance = distance_matrix[route[i]][route[i + 1]]
        if distance == 100000:  # Infeasible route (represented by a high number)
            return -1e6  # Large negative penalty for infeasible routes
        total_distance += distance
    
    # Return to the starting city
    total_distance += distance_matrix[route[-1]][route[0]]
    
    return -total_distance  # Negative for minimization (lower distance is better)

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    """
    Tournament selection for genetic algorithm. Selects individuals from the population
    based on their fitness scores, using a tournament selection method.

    Parameters:
        - population (list): The current population of routes.
        - scores (np.array): The calculate_fitness scores corresponding to each individual in the population.
        - number_tournaments (int): The number of tournaments to run in the population.
        - tournament_size (int): The number of individuals to compete in the tournaments.

    Returns:
        - list: A list of selected individuals for crossover.
    """
    selected = []
    
    for _ in range(number_tournaments):
        # Randomly select tournament_size individuals to compete
        idx = np.random.choice(len(population), tournament_size, replace=False)
        # Select the individual with the highest score in the tournament
        best_idx = np.argmax(scores[idx])
        selected.append(population[idx[best_idx]])  # Append the best individual in the tournament
    
    return selected

def order_crossover(parent1, parent2):
    """
    Perform order crossover (OX) between two parents to produce a child.

    Parameters:
        - parent1 (list): The first parent (route).
        - parent2 (list): The second parent (route).

    Returns:
        - list: The child route formed by crossover.
    """
    size = len(parent1)
    child = [-1] * size  # Initialize an empty child route

    start, end = sorted(random.sample(range(size), 2))  # Randomly choose a crossover segment

    # Copy a slice from parent1 to the child
    child[start:end + 1] = parent1[start:end + 1]

    # Fill the remaining positions with genes from parent2, preserving their order
    child_pos = end + 1
    parent2_pos = end + 1

    while -1 in child:
        city = parent2[parent2_pos % size]  # Wrap around to the start of parent2 if necessary
        if city not in child:
            child[child_pos % size] = city  # Place city in the next available position
            child_pos += 1
        parent2_pos += 1

    return child

def mutate(route, mutation_rate):
    """
    Perform mutation on a route by swapping two random cities with a certain probability.

    Parameters:
        - route (list): The route to be mutated.
        - mutation_rate (float): The probability of mutation.

    Returns:
        - list: The mutated route.
    """
    if random.random() < mutation_rate:  # Mutate with the given probability
        i, j = random.sample(range(len(route)), 2)  # Randomly select two indices
        route[i], route[j] = route[j], route[i]  # Swap the two cities
    return route

def elite_selection(population, fitness_values, elite_size):
    """
    Select the top elite individuals from the population based on their fitness values.

    Parameters:
        - population (list): The population of individuals (routes).
        - fitness_values (list or np.array): The fitness values corresponding to the population.
        - elite_size (int): The number of elite individuals to select.

    Returns:
        - list: A list of the elite individuals.
    """
    # Sort population by fitness values (descending order, better fitness comes first)
    sorted_population = [x for _, x in sorted(zip(fitness_values, population), key=lambda pair: pair[0], reverse=True)]
    return sorted_population[:elite_size]  # Return the top elite_size individuals

def evaluate_population_mpi(population, distance_matrix):
    """
    Evaluate the fitness of the population using MPI for parallel processing.

    Parameters:
        - population (list): The population of individuals (routes).
        - distance_matrix (numpy.ndarray): The distance matrix to calculate the fitness of each route.

    Returns:
        - np.array: A numpy array containing the fitness values of the population.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes

    # Split the population across available processes
    chunk_size = len(population) // size
    local_population = population[rank * chunk_size:(rank + 1) * chunk_size]  # Local population for the current process

    # Calculate fitness for the local population
    local_fitness = np.array([calculate_fitness(route, distance_matrix) for route in local_population])

    # Gather all fitness values to the root process
    all_fitness = None
    if rank == 0:
        all_fitness = np.empty(len(population), dtype=float)  # Prepare space to collect all fitness values
    comm.Gather(local_fitness, all_fitness, root=0)  # Gather all local fitness values to the root process

    return all_fitness if rank == 0 else None  # Return the fitness values only to the root process


