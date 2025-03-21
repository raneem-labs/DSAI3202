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
        return -1e6

    total_distance = 0
    
    for i in range(len(route) - 1):
        distance = distance_matrix[route[i]][route[i + 1]]
        if distance == 100000:  # Infeasible route
            return -1e6  # Large negative penalty
        total_distance += distance
    
    # Return to the starting city
    total_distance += distance_matrix[route[-1]][route[0]]
    
    return -total_distance  # Return negative for minimization

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    """
    Tournament selection for genetic algorithm.

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
        idx = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = np.argmax(scores[idx])
        selected.append(population[idx[best_idx]])
    
    return selected

import random

def order_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    start, end = sorted(random.sample(range(size), 2))

    # Copy a slice from parent1
    child[start:end + 1] = parent1[start:end + 1]

    # Fill the remaining positions with parent2 genes, maintaining their order
    child_pos = end + 1
    parent2_pos = end + 1

    while -1 in child:
        city = parent2[parent2_pos % size]
        if city not in child:
            child[child_pos % size] = city
            child_pos += 1
        parent2_pos += 1

    return child

def mutate(route, mutation_rate):
    """
    Performs mutation on a route by swapping two random cities. 
    The mutation rate determines the probability of mutation.

    Args:
        route (list): A list representing a route.

    Returns:
        list: The mutated route.
    """
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]  # Swap two cities
    return route

def elite_selection(population, fitness_values, elite_size):
    sorted_population = [x for _, x in sorted(zip(fitness_values, population), key=lambda pair: pair[0], reverse=True)]
    return sorted_population[:elite_size]

def evaluate_population_mpi(population, distance_matrix):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Split population across available processes
    chunk_size = len(population) // size
    local_population = population[rank * chunk_size:(rank + 1) * chunk_size]

    # Calculate fitness locally
    local_fitness = np.array([calculate_fitness(route, distance_matrix) for route in local_population])

    # Gather all fitness values to the root process
    all_fitness = None
    if rank == 0:
        all_fitness = np.empty(len(population), dtype=float)
    comm.Gather(local_fitness, all_fitness, root=0)

    return all_fitness if rank == 0 else None

