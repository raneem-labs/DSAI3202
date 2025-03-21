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
    Load a distance matrix from a CSV file. The CSV should contain a square matrix of distances
    between cities, with the first row being headers (which are removed).

    Args:
    file_path (str): Path to the CSV file containing the distance matrix.

    Returns:
    np.ndarray: A numpy array representing the distance matrix.
    """
    try:
        # Load the distance matrix using numpy, skipping the first row (headers)
        distance_matrix = np.loadtxt(file_path, delimiter=",")
        distance_matrix = distance_matrix[1:, :]  # Slice to remove the first row
        return distance_matrix
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error: Could not load distance matrix from {file_path}. {e}")
        return None

# Genetic algorithm function adapted for 5 cars
def genetic_algorithm_5_cars(distance_matrix, population_size=200, generations=60, mutation_rate=0.02):
    """
    Run a genetic algorithm to solve the Traveling Salesperson Problem (TSP) with the added complexity
    of dividing the solution into 5 car routes.

    Args:
    distance_matrix (np.ndarray): Matrix representing the distances between cities.
    population_size (int): Number of individuals in the population. Default is 200.
    generations (int): Number of generations for the genetic algorithm. Default is 60.
    mutation_rate (float): Probability of mutation for each individual. Default is 0.02.

    Returns:
    None: The function prints the best solution and execution time to the console.
    """
    # MPI communication setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_cities = len(distance_matrix)  # Number of cities in the TSP problem
    
    # Initialize the population with random permutations of city indices
    population = [np.random.permutation(num_cities).tolist() for _ in range(population_size)]

    best_solution = None
    best_fitness = -np.inf

    start_time = time.time()  # Track the start time for performance measurement

    # Main genetic algorithm loop for specified generations
    for generation in range(generations):
        # Evaluate the fitness of the current population using MPI
        fitness_values = evaluate_population_mpi(population, distance_matrix)

        if fitness_values is not None:
            # Select elite individuals based on fitness to preserve good solutions
            elites = elite_selection(population, fitness_values, elite_size=5)
            new_population = elites.copy()  # Start new population with elites

            # Generate new individuals via crossover and mutation until population is full
            while len(new_population) < population_size:
                parent1 = select_in_tournament(population, fitness_values)[0]
                parent2 = select_in_tournament(population, fitness_values)[0]
                child = order_crossover(parent1, parent2)  # Order-based crossover
                child = mutate(child, mutation_rate)  # Apply mutation to the child
                new_population.append(child)

            # Update the population with the newly generated population
            population = new_population
            current_best_fitness = max(fitness_values)  # Track the best fitness in the current generation

            # Update the best solution if the current generation has a better fitness
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = population[np.argmax(fitness_values)]  # The best route (with minimum distance)

            # Periodically print progress for the root process (rank 0)
            if rank == 0 and generation % 10 == 0:
                print(f"Generation {generation}: Best Fitness = {best_fitness}")

    end_time = time.time()  # Track the end time for performance measurement

    # Only print the final best solution in the root process (rank 0)
    if rank == 0:
        # Split the best solution into 5 car routes
        chunk_size = len(best_solution) // 5
        routes = [best_solution[i * chunk_size:(i + 1) * chunk_size] for i in range(5)]

        print("Best Solution for 5 Cars:")
        for i, route in enumerate(routes):
            print(f"Car {i + 1}: {route}")  # Print the route for each car
        print(f"Total Distance: {-best_fitness}")  # Print the total distance of the solution
        print(f"Execution Time: {end_time - start_time:.2f} seconds")  # Print the execution time

# Main entry point for the program
if __name__ == "__main__":
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Set up argument parser to get file path for the distance matrix
    parser = argparse.ArgumentParser(description="Run a genetic algorithm for the TSP with 5 cars.")
    parser.add_argument("--file_path", type=str, default="data/city_distances.csv",
                        help="Path to the distance matrix CSV file.")
    args = parser.parse_args()

    # Load the distance matrix if the process has rank 0
    if rank == 0:
        distance_matrix = load_distance_matrix(args.file_path)
        if distance_matrix is None:
            exit()  # Exit if the distance matrix could not be loaded
        num_cities = len(distance_matrix)
        print(f"Loaded distance matrix with {num_cities} cities.")
    else:
        distance_matrix = None

    # Broadcast the distance matrix to all processes
    distance_matrix = comm.bcast(distance_matrix, root=0)

    # Run the genetic algorithm for 5 cars
    genetic_algorithm_5_cars(distance_matrix)


