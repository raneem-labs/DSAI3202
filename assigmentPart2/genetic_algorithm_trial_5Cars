import numpy as np
import random
import time
from typing import List, Tuple

# Generates a random distance matrix representing distances between cities
# The matrix is symmetrical and contains random integers between 1 and 1000.
# The diagonal elements are set to 0 (since the distance from a city to itself is 0).
def calculate_distance_matrix(num_cities: int) -> np.ndarray:
    np.random.seed(0)  # Set a seed for reproducibility
    distance_matrix = np.random.randint(1, 1000, size=(num_cities, num_cities))  # Random distances between cities
    np.fill_diagonal(distance_matrix, 0)  # Set diagonal to 0
    return distance_matrix


# Computes the total distance for a given route using the provided distance matrix
# The route is represented as a list of city indices, where each pair of consecutive cities 
# in the list contributes to the total distance.
def calculate_total_distance(route: List[int], distance_matrix: np.ndarray) -> int:
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]  # Sum the distances between consecutive cities
    return total_distance


# Initializes a population of random routes
# Each route starts with the city 0 (fixed start point), followed by a shuffled list of the remaining cities.
def initialize_population(population_size: int, num_cities: int) -> List[List[int]]:
    population = []
    for _ in range(population_size):
        individual = list(range(1, num_cities))  # Create a list of cities (excluding city 0)
        random.shuffle(individual)  # Shuffle cities to create a random route
        individual = [0] + individual  # Add city 0 at the start of the route
        population.append(individual)  # Add the individual route to the population
    return population


# Evaluates the fitness of each individual in the population
# Fitness is the negative of the total distance of the route (since shorter distances are better)
# The evaluated population is sorted in descending order of fitness (shorter distance is better).
def evaluate_population(population: List[List[int]], distance_matrix: np.ndarray) -> List[Tuple[List[int], int]]:
    evaluated_population = [(individual, -calculate_total_distance(individual, distance_matrix)) for individual in population]
    evaluated_population.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness (larger fitness = better solution)
    return evaluated_population


# Performs crossover between two parent routes to create a new child route
# The crossover process combines parts of the parents' routes to generate a new valid route.
def crossover(parent1: List[int], parent2: List[int]) -> List[int]:
    size = len(parent1)
    child = [-1] * size  # Initialize child with -1, indicating unfilled positions

    start, end = sorted(random.sample(range(size), 2))  # Randomly select a segment from parent1
    child[start:end] = parent1[start:end]  # Copy the segment to the child

    pos = end
    for gene in parent2:  # Fill in the remaining genes from parent2, maintaining the order
        if gene not in child:  # Only add genes that aren't already in the child
            if pos >= size:
                pos = 0
            child[pos] = gene  # Assign gene to the next available position in the child
            pos += 1

    return child


# Applies mutation to an individual route
# Mutation randomly swaps two cities in the route with a certain probability (mutation rate).
def mutate(individual: List[int], mutation_rate: float):
    for i in range(1, len(individual)):  # Skip city 0 since it's fixed as the start
        if random.random() < mutation_rate:  # Check if mutation should occur at this position
            j = random.randint(1, len(individual) - 1)  # Randomly choose another position
            individual[i], individual[j] = individual[j], individual[i]  # Swap the cities


# The main function to run the genetic algorithm
# The algorithm simulates a population of routes and evolves them over several generations using selection, crossover, and mutation.
def genetic_algorithm_5_cars(num_cities: int = 100, population_size: int = 200, generations: int = 60, mutation_rate: float = 0.02):
    distance_matrix = calculate_distance_matrix(num_cities)  # Generate the distance matrix
    population = initialize_population(population_size, num_cities)  # Initialize the population with random routes
    best_solution = None
    best_fitness = float('-inf')

    start_time = time.time()  # Record the start time of the algorithm

    # Main loop for the genetic algorithm
    for generation in range(1, generations + 1):
        evaluated_population = evaluate_population(population, distance_matrix)  # Evaluate the fitness of the population
        best_in_generation = evaluated_population[0]  # Best individual in this generation

        if best_in_generation[1] > best_fitness:  # If this individual is better than the previous best
            best_solution, best_fitness = best_in_generation  # Update the best solution and fitness

        # Output the best fitness at every 10th generation
        if generation % 10 == 0:
            print(f"Generation {generation}: Best fitness = {best_fitness}")

        new_population = []

        # Create the new population through crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(evaluated_population[:50], k=2)  # Select two parents from the top 50 individuals
            child = crossover(parent1[0], parent2[0])  # Perform crossover
            mutate(child, mutation_rate)  # Apply mutation
            new_population.append(child)  # Add the child to the new population

        population = new_population  # Set the new population as the current population

    end_time = time.time()  # Record the end time of the algorithm

    # Split the best solution into 5 separate routes (for each car)
    chunk_size = len(best_solution) // 5
    routes = [best_solution[i * chunk_size: (i + 1) * chunk_size] for i in range(5)]

    # Output the best solution for the 5 cars and total distance
    print("Best Solution for 5 Cars:")
    for i, route in enumerate(routes):
        print(f"Car {i + 1}: {route}")
    print(f"Total Distance: {-best_fitness}")  # Display the total distance (negated to get positive value)
    print(f"Execution Time: {end_time - start_time:.2f} seconds")  # Output the execution time

# Run the genetic algorithm with default parameters
genetic_algorithm_5_cars()

