import numpy as np
import time
import argparse
from mpi4py import MPI
from genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament, order_crossover, mutate, elite_selection, evaluate_population_mpi
)

def load_distance_matrix(file_path):
    try:
        distance_matrix = np.loadtxt(file_path, delimiter=",")
        distance_matrix = distance_matrix[1:, :]  # Slice to remove the first row
        return distance_matrix
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error: Could not load distance matrix from {file_path}. {e}")
        return None

def genetic_algorithm_5_cars(distance_matrix, population_size=200, generations=60, mutation_rate=0.02):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_cities = len(distance_matrix)
    
    # Ensure routes are permutations of indices from 0 to num_cities - 1
    population = [np.random.permutation(num_cities).tolist() for _ in range(population_size)]

    best_solution = None
    best_fitness = -np.inf

    start_time = time.time()

    for generation in range(generations):
        fitness_values = evaluate_population_mpi(population, distance_matrix)

        if fitness_values is not None:
            elites = elite_selection(population, fitness_values, elite_size=5)
            new_population = elites.copy()

            while len(new_population) < population_size:
                parent1 = select_in_tournament(population, fitness_values)[0]
                parent2 = select_in_tournament(population, fitness_values)[0]
                child = order_crossover(parent1, parent2)
                child = mutate(child, mutation_rate)
                new_population.append(child)

            population = new_population
            current_best_fitness = max(fitness_values)

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = population[np.argmax(fitness_values)]

            if rank == 0 and generation % 10 == 0:
                print(f"Generation {generation}: Best Fitness = {best_fitness}")

    end_time = time.time()

    if rank == 0:
        # Split the best solution into 5 routes (for 5 cars)
        chunk_size = len(best_solution) // 5
        routes = [best_solution[i * chunk_size:(i + 1) * chunk_size] for i in range(5)]

        print("Best Solution for 5 Cars:")
        for i, route in enumerate(routes):
            print(f"Car {i + 1}: {route}")
        print(f"Total Distance: {-best_fitness}")
        print(f"Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run a genetic algorithm for the TSP with 5 cars.")
    parser.add_argument("--file_path", type=str, default="data/city_distances.csv",
                        help="Path to the distance matrix CSV file.")
    args = parser.parse_args()

    if rank == 0:
        # Load the distance matrix
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

