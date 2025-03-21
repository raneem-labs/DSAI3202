import numpy as np
import time
import argparse
from mpi4py import MPI
from genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament, order_crossover, mutate, elite_selection, evaluate_population_mpi
)

# Function to load the distance matrix from a CSV file
def load_distance_matrix(file_path):
    """
    Loads the city distance matrix from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing the distance matrix.

    Returns:
        np.ndarray: A 2D numpy array representing the distance matrix, or None if loading failed.
    """
    try:
        # Load the CSV file and convert it to a numpy array
        distance_matrix = np.loadtxt(file_path, delimiter=",")
        distance_matrix = distance_matrix[1:, :]  # Slice to remove the first row (headers)
        return distance_matrix
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error: Could not load distance matrix from {file_path}. {e}")
        return None

# Main genetic algorithm function
def genetic_algorithm(distance_matrix, population_size=200, generations=60, mutation_rate=0.02):
    """
    Runs the genetic algorithm to solve the Traveling Salesman Problem (TSP).

    Args:
        distance_matrix (np.ndarray): The distance matrix representing the cities and their distances.
        population_size (int): The number of individuals in the population (default: 200).
        generations (int): The number of generations to run the algorithm (default: 60).
        mutation_rate (float): The rate of mutation applied to offspring (default: 0.02).
    """
    # Initialize MPI for parallel computing
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    num_cities = len(distance_matrix)

    # Generate initial population of random routes (permutations of city indices)
    population = [np.random.permutation(num_cities).tolist() for _ in range(population_size)]

    best_solution = None
    best_fitness = -np.inf

    # Start the timer to measure execution time
    start_time = time.time()

    # Main loop for the genetic algorithm over multiple generations
    for generation in range(generations):
        # Evaluate the fitness of each individual (route) in the population
        fitness_values = evaluate_population_mpi(population, distance_matrix)

        if fitness_values is not None:
            # Select elites (top individuals) and copy them to the new population
            elites = elite_selection(population, fitness_values, elite_size=5)
            new_population = elites.copy()

            # Perform crossover and mutation to generate offspring
            while len(new_population) < population_size:
                parent1 = select_in_tournament(population, fitness_values)[0]
                parent2 = select_in_tournament(population, fitness_values)[0]
                child = order_crossover(parent1, parent2)  # Combine parents' routes
                child = mutate(child, mutation_rate)  # Mutate the child route
                new_population.append(child)

            population = new_population  # Update the population with new individuals

            # Track the best fitness in the current generation
            current_best_fitness = max(fitness_values)

            # Update the best solution if we found a better one
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = population[np.argmax(fitness_values)]

            # Print the best fitness at every 10th generation (if root process)
            if rank == 0 and generation % 10 == 0:
                print(f"Generation {generation}: Best Fitness = {best_fitness}")

    # End the timer to measure execution time
    end_time = time.time()

    # If this is the root process, print the final solution and execution time
    if rank == 0:
        print("Best Solution:")
        print(best_solution)
        print(f"Total Distance: {-best_fitness}")
        print(f"Execution Time: {end_time - start_time:.2f} seconds")

# Main entry point of the script
if __name__ == "__main__":
    # Initialize MPI (parallel computing framework)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Set up argument parser for command-line input
    parser = argparse.ArgumentParser(description="Run a genetic algorithm for the TSP.")
    parser.add_argument("--file_path", type=str, default="data/city_distances.csv",
                        help="Path to the distance matrix CSV file.")
    args = parser.parse_args()

    if rank == 0:
        # Load the distance matrix from the specified file path
        distance_matrix = load_distance_matrix(args.file_path)
        if distance_matrix is None:
            exit()  # Exit if the matrix could not be loaded
        num_cities = len(distance_matrix)
        print(f"Loaded distance matrix with {num_cities} cities.")
    else:
        distance_matrix = None

    # Broadcast the distance matrix to all processes (so they all have access to it)
    distance_matrix = comm.bcast(distance_matrix, root=0)

    # Run the genetic algorithm with the loaded distance matrix
    genetic_algorithm(distance_matrix)














